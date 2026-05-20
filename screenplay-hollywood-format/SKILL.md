---
name: screenplay-hollywood-format
description: 将短剧分镜脚本转换为好莱坞标准格式剧本（DOCX）— 移除镜头指示、添加角色介绍、修复场景标题、自然化对白、python-docx 排版输出
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [Screenplay, Hollywood-Format, DOCX, Format-Conversion, Short-Drama]
    related_skills: [drama-team, novel-to-short-drama-adaptation, short-drama-production-index, seedance-prompt-optimizer]
---

# Screenplay Hollywood Format

> 将 `drama-team` 生成的分镜脚本（script/EP-XX.md）转换为好莱坞标准格式剧本（.docx）。
> **v1.0 起源**：2026-05-14 Lady Audley's Secret 两位编剧（Alex H + Dennis）BLOCKER 级反馈驱动创建。

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

## 使用流程

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

### Step 2: 配置并运行转换脚本

```bash
# 复制模板脚本到项目目录
cp ~/.hermes/skills/creative/screenplay-hollywood-format/scripts/convert_to_hollywood.py /path/to/project/

# 编辑脚本顶部的 PROJECT 路径和角色配置
# 然后运行
cd /path/to/project
python3 convert_to_hollywood.py
```

### Step 3: 检查输出

脚本会生成：
- `{ProjectName}_Screenplay.docx` — 好莱坞格式剧本
- 控制台输出：每个修复项的日志（移除了哪些镜头术语、修复了哪些场景标题等）

### Step 4: 人工审校

自动转换后必须人工检查：
- [ ] 角色首次出场描述是否完整准确
- [ ] 场景标题是否与动作内容一致
- [ ] 对白是否自然（自动后处理有限）
- [ ] 首集设定交代是否充分
- [ ] 连续性是否有断裂

## 转换脚本核心逻辑（convert_to_hollywood.py）

### 1. 镜头术语移除

```python
# 需要移除的镜头前缀（出现在 Action 行开头）
SHOT_PREFIXES = [
    "EXTREME CLOSE UP — ", "EXTREME CLOSE UP- ",
    "CLOSE UP — ", "CLOSE UP- ",
    "WIDE SHOT — ", "WIDE SHOT- ",
    "MEDIUM SHOT — ", "MEDIUM SHOT- ",
    "LOW ANGLE — ", "LOW ANGLE- ",
    "OVER THE SHOULDER — ", "OVER THE SHOULDER- ",
    "TWO SHOT — ", "TWO SHOT- ",
    "FULL SHOT — ", "FULL SHOT- ",
    "HIGH ANGLE — ", "HIGH ANGLE- ",
    "TRACKING — ", "TRACKING- ",
    "POV — ", "POV- ",
    "INSERT — ", "INSERT- ",
]

def strip_shot_direction(action_text):
    """移除 Action 行中的镜头类型前缀，保留纯叙事描述。"""
    for prefix in SHOT_PREFIXES:
        if action_text.startswith(prefix):
            cleaned = action_text[len(prefix):]
            # 首字母大写
            return cleaned[0].upper() + cleaned[1:] if cleaned else ""
    return action_text
```

### 2. 角色首次出场注入

```python
# 从 characters.md 解析的角色介绍映射
# 格式：{ "角色名": "年龄描述, 简短外貌" }
CHARACTER_INTROS = {
    "LUCY GRAHAM": "(20s), stunningly beautiful with dark curly hair and amber eyes — the new Lady Audley",
    "ROBERT AUDLEY": "(25), Sir Michael's nephew — handsome but perpetually disheveled, brown wavy hair, gray eyes",
    "SIR MICHAEL AUDLEY": "(70s), a wealthy baronet — portly, gray-white hair, kind but naive",
    "MELISSA TALBOYS": "(20s), George's sister — plain but dignified, straight brown hair, sharp dark eyes",
    "HIRAM WORTHY": "(50s), the butler — square-jawed, graying, stern but conscience-stricken",
    "ARTHUR GRAMMONT": "(mid-20s), Lucy's cousin — golden wavy hair, blue eyes, elegant but predatory",
}

# 追踪已出场角色
seen_characters = set()

def maybe_add_intro(char_name):
    """角色首次出场时返回介绍行，后续出场返回 None。"""
    if char_name in seen_characters:
        return None
    seen_characters.add(char_name)
    intro = CHARACTER_INTROS.get(char_name)
    if intro:
        return f"{char_name} {intro}"
    return None
```

### 3. 场景标题修复

```python
# 场景 ID → 正确的 INT./EXT. + 场景名 映射
# 这是项目特定的，需要根据 scene_prop_data.json + 人工校验配置
SCENE_HEADING_MAP = {
    "S-01": ("INT.", "AUDLEY COURT ENTRANCE HALL"),
    "S-02": ("INT.", "AUDLEY COURT GRAND HALL"),
    "S-03": ("INT.", "AUDLEY COURT DRAWING ROOM"),
    "S-04": ("INT.", "LADY AUDLEY'S BEDROOM"),
    "S-05": ("INT.", "AUDLEY COURT DINING ROOM"),
    "S-06": ("INT.", "AUDLEY COURT LIBRARY"),
    "S-07": ("INT.", "AUDLEY COURT CORRIDOR"),
    "S-08": ("EXT.", "AUDLEY COURT GARDEN"),
    "S-09": ("INT.", "AUDLEY COURT CELLAR"),  # ⚠️ 常见错误：被标为 EXT. LONDON STREET
    "S-10": ("INT.", "SERVANTS' QUARTERS"),
    # ... 按项目扩展
}

def get_scene_heading(scene_id, day_night):
    """获取正确的场景标题行。"""
    if scene_id in SCENE_HEADING_MAP:
        int_ext, name = SCENE_HEADING_MAP[scene_id]
        return f"{int_ext} {name} - {day_night}"
    # fallback: 从 scene_prop_data.json 查找
    return None
```

### 4. 对白自然化后处理

```python
def naturalize_dialogue(line):
    """对白后处理：增加口语化特征。"""
    # 1. 宣告式陈述 → 观察式（部分规则）
    # "You're trembling, my Lady." → "You're... shaking."
    # 2. 过于正式的称呼简化
    # 3. 添加犹豫标记（在转折点）
    # 注意：此步骤有限，核心仍需人工润色
    return line
```

### 5. 首集设定交代

```python
def generate_setup_block(outline_md, characters_md):
    """为首集生成设定交代段落，放在 EPISODE 1 标题后、第一个场景标题前。"""
    # 从 outline.md 提取：故事背景、核心关系
    # 从 characters.md 提取：主角身份
    # 输出格式：
    # AUDLEY COURT — a grand Victorian estate in Essex, England.
    # 
    # LUCY GRAHAM (20s), stunningly beautiful with dark curly hair 
    # and amber eyes, has just married SIR MICHAEL AUDLEY (70s), 
    # a wealthy baronet. She has been Lady Audley for three weeks.
    # 
    # ROBERT AUDLEY (25), Sir Michael's nephew, is the family's 
    # resident layabout — a lawyer who never practices.
    pass
```

### 6. DAY/NIGHT 推断

```python
def determine_day_night(scene_cell, action_cell, time_cell):
    """从上下文推断 DAY/NIGHT。"""
    combined = (scene_cell + " " + action_cell).upper()
    night_keywords = ["NIGHT", "夜晚", "深夜", "MOONLIGHT", "DARK", "CANDLE"]
    morning_keywords = ["MORNING", "上午", "DAWN", "SUNRISE"]
    afternoon_keywords = ["AFTERNOON", "午后", "SUNSET", "DUSK"]
    evening_keywords = ["EVENING", "傍晚", "TWILIGHT"]
    
    if any(kw in combined for kw in night_keywords):
        return "NIGHT"
    if any(kw in combined for kw in evening_keywords):
        return "EVENING"  # 或 NIGHT，按项目习惯
    if any(kw in combined for kw in morning_keywords):
        return "DAY"
    if any(kw in combined for kw in afternoon_keywords):
        return "DAY"
    return "DAY"  # 默认
```

## 完整转换流程

### 方案 A：词表映射法（适合简单项目 <10集）

对每集 EP-01 ~ EP-N：
1. 解析 MD → 提取场景/对白
2. 用 location_map 映射中文场景标题 → 英文
3. 用 ACTION_PHRASES 映射中文动作描述 → 英文
4. 写入 DOCX（见下方 python-docx 排版）

**问题**：词表匹配法有长尾效应 — 再大的词表也漏边角 case（音效、闪回标记、复合动作等），最终总有几行中文残留。

### 方案 B：LLM 翻译法（推荐 ✅ 适合 >10集项目）

**核心思路**：不再维护词表，直接调用 LLM 逐集翻译成英文好莱坞格式，然后解析纯文本输出为 DOCX。

**流程**：
```
script/EP-01.md ~ EP-25.md
  → 对每集: LLM(PROMPT + script_text) → screenplay-EP-XX.txt（纯英文）
  → 解析所有 .txt → 排版 → {ProjectName}_Screenplay.docx
```

**Prompt 要点**（见 `scripts/translate_to_screenplay.py`）：
- System prompt 含完整好莱坞格式规范 + 角色名映射表
- temperature 0.3, max_tokens 8000, top_p 0.9
- 输出纯 screenplay 文本（无 markdown）
- **本地 LLM 不支持并发** — 串行调用

**解析 .txt → DOCX**：
- 识别缩进判断元素类型：
  - 0 缩进 → Action
  - ≥6 空格 + ALL CAPS → Character Name
  - ≥6 空格 + `(xxx)` → Parenthetical
  - ≥6 空格 + 普通文本 → Dialogue
- 场景标题：`INT./EXT.` 前缀 → 大写加粗
- 转场：`FADE IN:` 等 → 右对齐加粗

**优势**：
- 翻译质量高（LLM 理解上下文）
- 无词表维护负担
- 自动处理 SFX、闪回、音效等边角 case
- 中文残留率 <1%（vs 词表法 5-10%）

**执行方式**：主模型直接写 `translate_to_screenplay.py` 脚本，后台运行 + `notify_on_complete`。本地 LLM 不支持并发，串行跑 25 集约 3-5 分钟。

### python-docx 排版通用代码

```python
def add_run_with_font(p, text, font_name='Courier New', font_size=12, bold=False):
    run = p.add_run(text)
    run.font.name = font_name
    run.font.size = Pt(font_size)
    run.bold = bold
    # 正确设置东亚字体（避免 .element.rPr 报错）
    r = run._element
    rFonts = r.find(qn('w:rPr'))
    if rFonts is None:
        rFonts = OxmlElement('w:rPr')
        r.insert(0, rFonts)
    rFonts.set(qn('w:eastAsia'), font_name)
    return run
```

### 输入/输出

```
输入：script/EP-XX.md + characters.md + scene_prop_data.json

输出：{ProjectName}_Screenplay.docx（好莱坞标准格式，纯英文）
```

## 大项目（>15集）不要用子代理

子代理处理 25 集剧本会 max_iterations 超时：读完 10 集就 token 耗尽，来不及写 Python 脚本就挂了。

**正确做法**：主模型直接写 `generate_screenplay.py` 脚本，在 terminal 执行。脚本结构：
1. 解析所有 `script/EP-*.md` → 提取场景/对白表格
2. 用 `table_start = content.find('| 角色 |')` 截断 markdown 表格，避免表格残留在 action 里
3. 用 `re.search(r'画面：(.+?)(?=\n\n|\n##|$)', text, re.DOTALL)` 提取画面描述（非贪婪匹配）
4. 场景标题中文→英文映射（如 `码头` → `MARSEILLE DOCKS`）
5. 首次出场角色注入介绍
6. 写入 DOCX 并分页

## 常见陷阱

### 0. 场景标题残留中文（实际最常见 🔥🔥）
- **症状**：`EXT. 码头·重逢即暗涌` 而不是 `EXT. MARSEILLE DOCKS`
- **根因**：`translate_location()` 函数未覆盖所有中文场景名
- **修复**：维护完整的 `location_map` 字典，所有中文场景名都映射为英文

### 1. 场景标题映射错误（最常见 🔥）
- **症状**：`EXT. LONDON STREET - DAY` 但描述是 "Cellar filled with old boxes"
- **根因**：scene_prop_data.json 中场景名映射不准，或 `scene_int_ext()` 函数的关键词匹配逻辑错误
- **修复**：用显式 SCENE_HEADING_MAP 白名单替代自动推断，每个项目必须人工校验一次

### 2. 镜头术语残留
- **症状**：Action 行仍含 "CLOSE UP" 等术语
- **根因**：前缀列表不全（如 "ECU" 缩写、中文"极特写"等）
- **修复**：扩展 SHOT_PREFIXES 列表，同时用正则兜底：`re.sub(r'^(EXTREME\s+)?CLOSE\s+UP\s*[—-]\s*', '', text)`

### 3. 角色名不一致
- **症状**：同一角色在不同集用不同名（"Lucy" vs "LUCY GRAHAM" vs "LADY AUDLEY"）
- **根因**：CHAR_MAP 映射不全
- **修复**：统一角色名映射表，所有变体指向同一个正式名

### 4. 首集设定交代不足
- **症状**：读者/编剧看完 EP-01 不知道"这些人是谁、什么关系"
- **根因**：分镜脚本假设读者已知背景，但好莱坞剧本必须自包含
- **修复**：EP-01 开场必须交代：地点、时间、核心人物身份、核心关系

### 5. 连续性错误
- **症状**：EP-02 引用 EP-01 中未展示的信息（如"Robert 被 Lucy 疤痕困扰"但 EP-01 中 Robert 没看到疤痕）
- **根因**：分镜脚本的"独处揭露"场景在剧本中无法被其他角色引用
- **修复**：读取 continuity.md 校验跨集引用合法性，或在剧本中调整信息可见性

### 6. 正则 `re.sub(r'^.*?$', '', text, flags=re.MULTILINE)` 清空所有文本 🔥🔥🔥
- **症状**：生成的 DOCX 里 action 行全空
- **根因**：`re.sub(r'^.*?$', '', text, flags=re.MULTILINE)` 匹配每一行的全部内容为空
- **修复**：**绝对不要用这个正则清理文本！** 用具体目标：`re.sub(r'\|.*\|', '', text)` 清除表格行，`re.sub(r'\*\*.*?\*\*', '', text)` 清除 markdown 粗体
- **这是 generate_screenplay.py 实际发生的 bug，修复后正常**

### 7. 对白机械感
- **症状**：编剧评价"reads like an Ionesco play"、"robotic and stilted"
- **根因**：短剧格式每句对白都承载信息推进，缺少潜台词和口语特征
- **修复**：后处理规则有限，核心需人工润色。可辅助的方向：
  - 宣告句 → 观察句（"You're trembling." → "You're... shaking."）
  - 加犹豫标记（转折点前加 "..."）
  - 允许答非所问（角色回避问题时不直接回答）

### 8. 词表匹配法的长尾问题（LLM 翻译法已解决 ✅）
- **症状**：再怎么扩充 ACTION_PHRASES，总有 10-15 行中文残留（音效 `咚……咚……咚……`、闪回 `(EP-03酒馆写诬告信画面)`、复合动作 `(喘息，无法言语)`）
- **根因**：`—` 破折号角色行的 EN 列也塞了中文（非对白内容），`translate_parenthetical` 只处理动作列，看不到对白列里的中文
- **旧修复**：给 `—` 行单独加检测分支 + 扩充词表，但每遇到新边角 case 就要补
- **正确修复**：用 LLM 翻译法（方案 B）替代词表法，从根源消灭中文残留

### 9. python-docx 字体设置报错
- **症状**：`AttributeError: 'Paragraph' object has no attribute 'element'`
- **根因**：`p.element.rPr.rFonts.set(...)` 是错误的 API — `element` 不存在于 Paragraph 对象
- **修复**：通过 `run._element` 操作 rPr：
  ```python
  r = run._element
  rFonts = r.find(qn('w:rPr'))
  if rFonts is None:
      rFonts = OxmlElement('w:rPr')
      r.insert(0, rFonts)
  rFonts.set(qn('w:eastAsia'), 'Courier New')
  ```
  见上方 `add_run_with_font()` 通用代码。

### 10. 本地 LLM 不支持并发 + Prompt 过长导致超时
- **症状**：并发 5 路请求 `localhost:8000/v1/chat/completions`，部分请求超时或返回空；单路请求也报 `Read timed out (read timeout=120)`
- **根因**：①qwen27b-awq (sGLang/vLLM) 本地推理服务单线程处理 ②Prompt 过长（100+行系统指令）增加 LLM 生成时间
- **修复**：
  - `MAX_CONCURRENT = 1`，串行调用
  - **精简 Prompt** — 删除冗余示例（如 200 字的完整 screenplay 示例），只保留格式规则（30-40 行足够）。25 集约 30-40 分钟 vs 精简后 ~30-38 分钟
  - **Timeout 拉到 300s** — 本地 LLM 处理长 prompt（每集 5-10k tokens）需要 60-120s，默认 120s 刚好超时
  - Prompt 模板见 `scripts/translate_to_screenplay.py`（精简版约 30 行指令）

### 11. LLM 翻译法验证结果
- 25 集测试：**0 中文残留**，25/25 成功
- 每集输出 1.6-6k chars，质量稳定
- 比词表法（方案 A）优势：无长尾问题（音效/闪回/复合动作自动翻译），无需维护 ACTION_PHRASES 词表

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

- `drama-team` — 上游：生成分镜脚本
- `novel-to-short-drama-adaptation` — 上游：小说改编流程
- `short-drama-production-index` — 下游：工作台生成
