---
name: screenplay-hollywood-format
description: 将短剧分镜脚本转换为好莱坞标准格式剧本（DOCX）— LLM 逐集翻译为纯英文剧本，python-docx 排版输出；移除镜头指示、注入角色介绍、修复场景标题
version: 2.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [Screenplay, Hollywood-Format, DOCX, Format-Conversion, Short-Drama]
    related_skills: [drama-team, short-drama-production-index, seedance-prompt-optimizer]
---

# Screenplay Hollywood Format

> 将 `drama-team` 生成的分镜脚本（script/EP-XX.md）转换为好莱坞标准格式剧本（.docx）。
> **v1.0 起源**：2026-05-14 Lady Audley's Secret 两位编剧（Alex H + Dennis）BLOCKER 级反馈驱动创建。
> **v2.0**：LLM 翻译法成为唯一主线（词表映射法因长尾中文残留被淘汰，25 集验证 0 残留），删除幻影脚本引用。

## 核心问题（来自真实编剧审核）

| # | 问题 | 严重度 | 修复方案 |
|---|------|--------|---------|
| 1 | Action 行包含镜头类型（CLOSE UP / WIDE SHOT 等）| 🔴 BLOCKER | 移除所有镜头前缀，改为纯叙事动作 |
| 2 | 角色首次出场无年龄/外貌描述 | 🔴 BLOCKER | 首次出场自动注入 characters.md 的介绍行 |
| 3 | EP-01 缺故事设定交代 | 🔴 BLOCKER | 首集开场加设定段落（地点+关系+时间） |
| 4 | INT./EXT. 场景标题映射错误 | 🔴 BLOCKER | 用场景白名单+关键词推断，校验所有标题 |
| 5 | 跨集连续性错误（如 EP-02 引用 EP-01 未展示的信息）| 🟡 HIGH | 读取 continuity.md 校验引用合法性 |
| 6 | 对白机械/生硬 | 🟡 HIGH | 后处理：加省略号、破折号、口语化 |
| 7 | 集间空页过多 | 🟢 MEDIUM | 硬分页替代空行 |
| 8 | 早期 cliffhanger 不够强 | 🟢 MEDIUM | 首集结尾强化钩子（人工/LLM 辅助） |

## 好莱坞格式规范

### 排版标准
- **字体**：Courier New 12pt（行业标准）
- **纸张**：US Letter (8.5" × 11")
- **边距**：左 1.5"，右/上/下 1.0"
- **行距**：单倍行距，段间 0pt

### 元素格式
| 元素 | 格式 | 示例 |
|------|------|------|
| 场景标题 | 大写加粗，左对齐，段前24pt | **INT. AUDLEY COURT DRAWING ROOM - DAY** |
| 动作描述 | 左对齐，段前6pt | Lucy traces her fingertip along her lower lip. |
| 角色名 | 大写加粗，居中 | **LUCY GRAHAM** |
| 扩展指示 | 居中缩进，斜体 | *(V.O.)* / *(O.S.)* / *(continuing)* |
| 对白 | 左缩进3cm，右缩进3cm | They all love me. |
| 转场 | 右对齐，大写 | CUT TO: / FADE TO BLACK. |
| 首次出场 | 角色名行后紧跟描述 | LUCY GRAHAM (20s), stunningly beautiful... |

### 关键规则
1. **Action 行禁止镜头术语** — 不出现 CLOSE UP / WIDE SHOT / MEDIUM SHOT / EXTREME CLOSE UP / LOW ANGLE / OVER THE SHOULDER / TWO SHOT 等
2. **角色首次出场必须描述** — 格式：`CHARACTER NAME (age), brief description`
3. **场景标题必须准确** — INT./EXT. + 具体地点 + DAY/NIGHT，与实际内容一致
4. **对白用自然口语** — 允许省略号(...)、破折号(—)、未完成句
5. **集间硬分页** — 不用空行填充

## 转换流程（LLM 翻译法）

> 详细的 Prompt 结构、API 参数、txt→DOCX 解析规则见 `references/llm-translation-workflow.md`。
> 历史注记：v1.x 曾用词表映射法（ACTION_PHRASES / LOCATION_MAP 逐句匹配），因长尾问题（音效、闪回标记、复合动作总有 10-15 行中文残留）被淘汰。

**核心思路**：不维护词表，逐集调用 LLM 翻译成纯英文好莱坞格式文本，再解析排版为 DOCX。

```
script/EP-01.md ~ EP-XX.md
  → 对每集: LLM(格式规范 + 角色名映射 + 剧本原文) → screenplay-EP-XX.txt（纯英文）
  → 解析所有 .txt → python-docx 排版 → {ProjectName}_Screenplay.docx
```

### Step 1: 准备输入文件

确保项目目录包含：
```
project/
├── characters/characters.md    # 角色设定（含年龄、外貌）
├── scene_prop_data.json        # 场景映射数据
├── script/EP-01.md ~ EP-XX.md # 分镜脚本
├── continuity.md               # 连续性追踪（可选，用于校验）
└── outline.md                  # 大纲（可选，用于首集设定）
```

### Step 2: 主模型现写转换脚本并执行

角色映射、场景表、集数都是项目特定的，没有可复用的现成脚本——**主模型按 `references/llm-translation-workflow.md` 现写 `translate_to_screenplay.py` 到项目目录**，包含：

1. 逐集调用 LLM 翻译（Prompt 精简到 8 条规则 + 一行式角色名映射 + 最小示例）
2. 解析 LLM 输出的纯文本（按缩进识别元素类型，见 reference）
3. python-docx 排版输出（东亚字体设置代码见 reference 的 `add_run_with_font`）
4. 每集翻译完检查中文残留率（应 <1%）

**执行方式**：后台运行 + `notify_on_complete`，不要开子代理。

> ⚠️ **大项目（>15集）不要用子代理**：子代理读完 10 集就 token 耗尽，来不及写脚本就 max_iterations 超时。主模型直接写脚本、terminal 执行。
> ⚠️ **并发与 timeout 是环境相关的**：本地单机 LLM（如 qwen 系列 sGLang/vLLM 单实例）不支持并发，`MAX_CONCURRENT = 1` 串行、timeout 拉到 300s；云 API 可正常并发。

### Step 3: 检查输出

- `{ProjectName}_Screenplay.docx` — 好莱坞格式剧本
- 控制台日志：每集的中文残留检查、修复项记录

### Step 4: 人工审校

自动转换后必须人工检查：
- [ ] 角色首次出场描述是否完整准确
- [ ] 场景标题是否与动作内容一致
- [ ] 对白是否自然（自动后处理有限）
- [ ] 首集设定交代是否充分
- [ ] 连续性是否有断裂

## 常见陷阱

### A. 内容质量陷阱（编剧会打回的）

**A1. 场景标题映射错误（最常见 🔥）**
- 症状：`EXT. LONDON STREET - DAY` 但描述是 "Cellar filled with old boxes"；或标题残留中文 `EXT. 码头·重逢即暗涌`
- 根因：场景名映射不全，或关键词自动推断出错
- 修复：给 LLM 的 prompt 中提供显式的场景中英映射白名单（来自 scene_prop_data.json + 人工校验），如 `S-09 → INT. AUDLEY COURT CELLAR`。**每个项目必须人工校验一次映射表**（项目特定，不可复用）

**A2. 角色名不一致**
- 症状：同一角色在不同集用不同名（"Lucy" vs "LUCY GRAHAM" vs "LADY AUDLEY"）
- 修复：prompt 中给统一角色名映射表，所有变体指向同一个正式名

**A3. 首集设定交代不足**
- 症状：读者看完 EP-01 不知道"这些人是谁、什么关系"——分镜脚本假设读者已知背景，但好莱坞剧本必须自包含
- 修复：EP-01 开场（EPISODE 1 标题后、第一个场景标题前）交代：地点、时间、核心人物身份、核心关系。素材来自 outline.md + characters.md

**A4. 角色首次出场无介绍**
- 修复：首次出场时角色名后紧跟 `(age), brief description`，介绍行来自 characters.md。已出场角色不重复注入

**A5. 连续性错误**
- 症状：EP-02 引用 EP-01 中未展示的信息（如"Robert 被 Lucy 疤痕困扰"但 EP-01 中 Robert 没看到疤痕）——分镜脚本的"独处揭露"场景无法被其他角色引用
- 修复：读取 continuity.md 校验跨集引用合法性，或调整信息可见性

**A6. 对白机械感**
- 症状：编剧评价 "reads like an Ionesco play"、"robotic and stilted"——短剧格式每句对白都承载信息推进，缺少潜台词
- 修复：核心需人工润色。可辅助的方向：宣告句 → 观察句（"You're trembling." → "You're... shaking."）；转折点前加犹豫标记 "..."；允许答非所问

### B. 脚本编码陷阱（写 Python 时会踩的）

**B1. 正则 `re.sub(r'^.*?$', '', text, flags=re.MULTILINE)` 清空所有文本 🔥🔥🔥**
- 症状：生成的 DOCX 里 action 行全空——这个正则匹配每一行的全部内容
- 修复：**绝对不要用这个正则清理文本**。用具体目标：`re.sub(r'\|.*\|', '', text)` 清表格行，`re.sub(r'\*\*.*?\*\*', '', text)` 清 markdown 粗体
- 实际发生过的 bug，修复后正常

**B2. markdown 表格残留在 action 里**
- 修复：用 `table_start = content.find('| 角色 |')` 截断表格；画面描述用 `re.search(r'画面：(.+?)(?=\n\n|\n##|$)', text, re.DOTALL)` 非贪婪提取

**B3. python-docx 字体设置报错**
- 症状：`AttributeError: 'Paragraph' object has no attribute 'element'`——`p.element.rPr.rFonts.set(...)` 是错误 API
- 修复：通过 `run._element` 操作 rPr，见 reference 的 `add_run_with_font()` 通用代码

**B4. 本地 LLM 超时/并发失败**
- 症状：并发请求部分超时或返回空；单路也报 `Read timed out (read timeout=120)`
- 根因：本地推理服务单线程 + prompt 过长（100+ 行系统指令）拉长生成时间
- 修复：串行（`MAX_CONCURRENT = 1`）；精简 prompt 到 30-40 行格式规则；timeout 300s。云 API 无此限制

## 与 drama-team 的关系

```
drama-team（生成）
  → script/EP-XX.md（分镜脚本格式：含镜头术语）
  → storyboard/EP-XX.md
  → prompts/EP-XX.md

screenplay-hollywood-format（转换）⭐ 本技能
  → script/EP-XX.md + characters.md + scene_prop_data.json
  → {ProjectName}_Screenplay.docx（好莱坞标准格式）
```

**分工**：
- `drama-team`：创作内容（剧本+分镜+Prompts），面向 AI 制作流程
- `screenplay-hollywood-format`：格式转换，面向人类编剧/导演审阅

## 相关技能

- `drama-team` — 上游：生成分镜脚本（小说改编流程见其 novel-adaptation 模块）
- `short-drama-production-index` — 下游：工作台生成
- `seedance-prompt-optimizer` — 平行：视频生成 prompt 优化
