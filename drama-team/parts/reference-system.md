  缺点：需要严格的上下文压缩，不适合前 5 集
  验证：Count of Monte Cristo EP-24+EP-25，3 个子 Agent 并行，152s 完成
  注意：生成后必须做文件验证（见下方"生成后验证"）
```

**子 Agent 并行时上下文压缩（v3.0 ⭐ 关键）：**

```
# 坏（30K+ tokens，导致子 Agent 断掉）
- 读 outline.md 全文
- 读 characters.md 全文
- 读 manifest.md 全文
- 读 scene_prop_data.json 全文
- 读 script/EP-XX.md 全文
- 读 storyboard/EP-XX.md 全文
- 读 continuity.md 全文

# 好（~5K tokens，验证成功）
- 读 continuity.md（核心，含进度+伏笔+角色状态）
- 读 outline.md 中对应集梗概（只读相关段落）
- 读 characters.md 中本集出场角色的 base_prompt（只读相关角色）
- 读 manifest.md 中的色调规则（当前集所在幕）
- 提供上一集 script 结尾钩子（100-200字摘要）
- 提供分镜/Prompts 格式参考（描述格式，不读全文件）
```

**生成后验证（v3.0 ⭐ 必做）：**

```python
# 每次批量生成后立即运行
import os
base = "/path/to/project"
for i in range(1, TOTAL_EPS + 1):
    ep = f"EP-{i:02d}"
    for subdir in ["script", "storyboard", "prompts"]:
        fp = f"{base}/{subdir}/{ep}.md"
        if not os.path.exists(fp):
            print(f"MISSING: {subdir}/{ep}.md")
        else:
            # 验证非空（>500 bytes = 有内容）
            size = os.path.getsize(fp)
            if size < 500:
                print(f"SUSPECT: {subdir}/{ep}.md ({size} bytes, 可能为空)
```

**TASK.md 更新（v3.0 ⭐ 必做）：**
- 生成完成后必须更新 TASK.md 进度（✅ 标记完成的集）
- 更新项目状态（如 "Phase 2 全部完成"）
- 添加更新日志条目
- 不更新会导致下次续做时无法判断真实进度

### 🔥 时间预算管理（v2.5 ⭐ 新增）

> **核心缺陷修复**：每集 70 秒的硬性限制常被打破，后期合成时时间对不上。

**时间预算模板（每集编剧时必须遵守）：**

```
总时长：70s

预算分配：
├── 对白时间：35-40s（约 12-15 句 × 3s/句）
├── 纯动作时间：15-20s（开场 3s + 转场 + 结尾慢推）
├── 情感留白：5-8s（沉默/表情/反应镜头）
└── 转场/黑屏：2-5s

强制规则：
- 开场 3 秒：必须直接进入冲突（不能空镜铺垫）
- 结尾 5-10 秒：Cliffhanger 慢推（最长 10s）
- 单个镜头 ≤ 5s（悬念慢推除外）
```

**时间校验（编剧完成后自动检查）：**

```python
# 伪代码
total_time = sum(shot_duration for shot in shots)
assert abs(total_time - 70) <= 5, f"时间偏差过大：{total_time}s vs 70s"

dialogue_count = len([s for s in shots if s.get('dialogue')])
assert 12 <= dialogue_count <= 15, f"对白数量：{dialogue_count}（标准 12-15）"

max_shot = max(shots, key=lambda s: s['duration'])
assert max_shot['duration'] <= 10, f"镜头过长：{max_shot['duration']}s（最长 10s）"
```

**分镜时间校验（Storyboard 阶段）：**

| 集类型 | 镜头数 | 单镜平均 | 总时长 |
|--------|--------|---------|--------|
| 氛围集 | 16-18 | 3.9-4.4s | 70s |
| 标准集 | 18-22 | 3.2-3.9s | 70s |
| 恐怖集 | 20-24 | 2.9-3.5s | 70s |
| 高潮集 | 22-25 | 2.8-3.2s | 70s |

### 🔥 文件依赖关系图（v2.5 ⭐ 新增）

> **核心缺陷修复**：12+ 个文件，新手不知道改了哪个需要同步更新哪些。

**文件依赖关系：**

```
outline.md
  ├──→ characters.md（依赖大纲中的角色）
  │     ├──→ visual_assets/manifest.md（依赖角色设定）
  │     ├──→ scene_prop_data.json（依赖角色使用的场景/道具）
  │     └──→ script/EP-XX.md（依赖角色身份）
  │
  └──→ continuity.md（依赖大纲中的伏笔规划）
        └──→ script/EP-XX.md（依赖连续性信息）

visual_assets/manifest.md
  ├──→ prompts/EP-XX.md（依赖视觉规则）
  └──→ storyboard/EP-XX.md（依赖色调/光影）

scene_prop_data.json
  └──→ prompts/EP-XX.md（依赖场景/道具 Reference）

script/EP-XX.md
  ├──→ storyboard/EP-XX.md（依赖剧本内容）
  └──→ prompts/EP-XX.md（依赖剧本场景）

storyboard/EP-XX.md
  └──→ prompts/EP-XX.md（依赖分镜镜头）
```

**文件变更联动规则：**

| 修改了 | 必须同步更新 | 可选更新 |
|--------|-------------|---------|
| outline.md | continuity.md（伏笔规划） | characters.md（如果角色有变化） |
| characters.md | manifest.md（服装/表情） | scene_prop_data.json（如果新角色有新场景） |
| manifest.md | prompts/EP-XX.md | 无 |
| script/EP-XX.md | storyboard/EP-XX.md, prompts/EP-XX.md, continuity.md | 无 |
| storyboard/EP-XX.md | prompts/EP-XX.md | 无 |
| continuity.md | 下一集的 script/EP-XX.md | 无 |

---

### 阶段 0：输入处理（v2.5 ⭐ 新增）

> **核心缺陷修复**：用户输入形式多样（小说文本/PDF/Idea描述/灵感碎片），必须先标准化再进入大纲阶段。

**输入类型识别与处理策略：**

| 输入类型 | 处理方式 | 输出 |
|---------|---------|------|
| **完整小说**（文本/PDF） | 读全文 → 提取核心情节、角色、世界观 → 生成改编规划 | 改编规划 → 进入阶段1 |
| **小说片段/大纲** | 直接分析 → 补全缺失信息 → 生成改编规划 | 改编规划 → 进入阶段1 |
| **Idea描述**（文字/语音） | 澄清需求 → 扩写世界观 → 生成大纲草案 | 大纲草案 → 进入阶段1 |
| **灵感碎片**（图片/关键词） | 视觉分析 → 头脑风暴 → 生成Idea描述 | Idea描述 → 进入阶段1 |

**小说输入处理流程（最常见场景）：**

```
Step 0a: 读取输入
  - 文本/PDF → 提取全文
  - 判断类型：完整小说 / 章节片段 / 大纲
  
Step 0b: 内容分析
  - 提取核心角色（≥3个）
  - 提取主要冲突线
  - 提取世界观设定
  - 估算总字数 → 决定集数（每集70s ≈ 1000-1500字小说内容）
  
Step 0c: 改编规划
  - 确定改编策略（忠实原著 / 创意改编 / 大纲驱动）
  - 确定集数（12/24/36集）
  - 确定风格（哥特暗黑 / 甜宠 / 复仇 / 悬疑...）
  - 确定核心卖点（双女主 / 宿敌 / 禁忌之恋...）
  
Step 0d: 进入阶段1（大纲生成）
```

**Idea输入处理流程：**

```
Step 0a: 接收Idea（文字/语音转文本）
Step 0b: 澄清需求（如有缺失）
  - 风格？（哥特/甜宠/复仇...）
  - 集数？（12/24/36）
  - 核心关系？（双女主/宿敌...）
  - 结局类型？（HE/BE/开放）
Step 0c: 扩写世界观（世界观+设定+规则）
Step 0d: 生成大纲草案 → 进入阶段1
```

### 阶段 1-2：大纲 + 人物设定

标准流程 — 确定故事方向、核心角色、人物关系、结局类型。

**大纲标准结构（必须包含）：**
```markdown
# 故事大纲

## 三幕结构
### 第一幕：建立（EP-01 到 EP-N/3）
- 核心事件
- 角色建立
- 激励事件

### 第二幕：对抗（EP-N/3 到 EP-2N/3）
- 冲突升级节点
- 中段转折点
- 最低谷时刻

### 第三幕：解决（EP-2N/3 到 EP-N）
- 高潮构建
- 最终对决
- 结局（HE/BE/开放）

## 分集梗概
### EP-01: 标题
- 核心事件（1-2句）
- 爽点类型（复仇/打脸/反转...）
- 结尾悬念
### EP-02: 标题
...

## 伏笔规划表（v2.5 ⭐）
| ID | 描述 | 埋入集 | 回收集 | 重要性 |
|----|------|--------|--------|--------|
| F-01 | 紫色咬痕的秘密 | EP-01 | EP-04 | 🔴 核心 |
| F-02 | 名册上的名字 | EP-03 | EP-06-07 | 🟡 重要 |
```

### 阶段 3：视觉资产 — 三文件架构（v2.3 ⭐）

> **这是跨集视觉一致性的关键阶段。** 基于人物设定，创建三个职责单一的文件，后续所有 Prompts 必须引用这三份文件。

**三文件架构（单一职责原则）：**

```
characters.md          ← 角色是谁（性格、动机、弧光、关系）
scene_prop_data.json   ← 场景/道具 Reference Prompts（AI生图参考图）
manifest.md            ← 视觉规则（服装指南、表情库、色调/光影/构图）
```

**为什么三分离？**（2026-04-30 Count of Monte Cristo 项目验证）
- 旧版 manifest.md 塞了角色外观+场景描述+服装+道具 → 46KB 臃肿文件
- `characters.md` 已有角色外观，`scene_prop_data.json` 已有场景/道具 → manifest.md 大量重复
- 精简后 manifest.md 保留**不可替代的内容**：服装场景映射、表情关键词、色调/光影/构图规则 → 16KB
- 三文件互不重复，各司其职，维护清晰

**产出文件 1：`characters.md`**（同 v2.0，不变）

**产出文件 2：`scene_prop_data.json`**（v2.2 → v2.3 保持不变）

```json
{
  "scenes": [
    {
      "id": "S-01",
      "name": "Marseille Port Dock",
      "cn_name": "马赛港口码头",
      "prompt": "Gothic Korean manga style, 9:16 vertical, wide establishing shot, no characters, environmental scene reference, ...",
      "status": "pending"
    }
  ],
  "props": [
    {
      "id": "P-01",
      "name": "Iron Gate",
      "prompt": "Gothic Korean manga style, close-up still life, no characters, prop reference, ...",
      "status": "pending"
    }
  ]
}
```

**产出文件 3：`manifest.md`（精简版）**

```markdown
# 视觉资产清单 (Visual Asset Manifest)

> **用途**：全局视觉规则 + 服装指南 + 表情姿态库
> **角色外观** → 见 `characters.md`
> **场景/道具 Reference Prompts** → 见 `scene_prop_data.json`

---

## 场景引用速查（from scene_prop_data.json）

| ID | 场景名 | 中文名 |
|----|--------|--------|
| S-01 | Marseille Port Dock | 马赛港口码头 |
| ... | ... | ... |

> 完整 Reference Prompt 在 `scene_prop_data.json.scenes[].prompt`

---

## 道具引用速查（from scene_prop_data.json）

| ID | 道具名 |
|----|--------|
| P-01 | Iron Gate |
| ... | ... |

> 完整 Reference Prompt 在 `scene_prop_data.json.props[].prompt`

---

## 服装指南 (按角色×场景)

> 此部分是所有文件唯一来源。Prompt 中角色服装必须按此表匹配当前场景。

### [角色名]
| 阶段/场景 | 服装 |
|-----------|------|
| 入狱前 | 白色水手衬衫+蓝色裤子+棕色靴子 |
| 地牢 | 破碎棕色麻布囚服 |
| ... | ... |

---

## 表情/姿态关键词库

> 写 Prompt 时从对应角色选关键词，确保情绪准确。

### [角色名]
- **愤怒**：眉头紧锁、嘴唇紧抿、握拳
- **恐惧**：瞳孔放大、呼吸急促、后退
- ...

---

## 全局视觉规则 (Global Visual Rules)

### 色调规则 (Color Palette Rules)
| 情境 | 主色调 | 辅助色 |
|------|--------|--------|
| 入狱前（Ep1-2） | 金色暖光 | 蔚蓝, 纯白 |
| 地牢时期（Ep4-12） | 冷蓝灰 | 烛火橙黄, 铁锈红 |
| ... | ... | ... |

### 光影规则 / 构图规则 / 韩漫风格元素
（详见模板）

---

## 文件关系

```
characters.md          ← 角色是谁
scene_prop_data.json   ← 场景/道具 Reference Prompts
manifest.md (本文件)    ← 视觉规则（服装、表情、色调、光影、构图）
```

**Prompt 编写流程**：
1. `characters.md` → 确认角色身份
2. `scene_prop_data.json` → 取场景/道具 ID → `[ref: S-XX]` / `[ref: P-XX]`
3. `manifest.md` → 取服装（按场景）+ 表情（按情绪）
4. `manifest.md` → 取色调/光影/构图规则
```

**三文件创建顺序：**
1. 基于 `characters.md` → 视觉导演为每个角色写服装表 + 表情关键词
2. 遍历剧本场景头 → 提取唯一场景（去重后 ~10-15 个）→ 写 `scene_prop_data.json.scenes[]`
3. 识别关键道具 → 写 `scene_prop_data.json.props[]`
4. 编写 `manifest.md` → 场景/道具速查表 + 服装指南 + 表情库 + 全局规则
5. **人工确认** — 三文件必须经导演（用户）确认后进入剧本阶段

### 阶段 4-5：剧本 + 分镜

编剧完成三件套中的剧本和分镜，派独立 Aligner 审核。

### 阶段 6：AI Prompts（含视觉资产强制注入 ⭐）

> **每张图 Prompt 开头必须注入对应的角色外观描述（从 manifest.md 拉取）。**

**Prompts 模板：**

```markdown
# EP-XX: Title - AI Prompts

## Visual Asset References（从 manifest.md 拉取）
### 本集出场角色外观：
**Carmilla**: 哥特暗黑韩漫风格，175cm高挑女性吸血鬼，苍白肤色，及肩黑色微卷发，琥珀色瞳孔，尖牙，黑色长裙+银色项链
**Irina**: 哥特暗黑韩漫风格，22岁年轻女性，黑色直发及腰，深褐色瞳孔，白色衬衫+深色西装外套+百褶裙

### 本集场景：
**古堡卧室**: 哥特风格，石墙+烛台+天鹅绒窗帘，冷色调烛光照明

## Image Prompts (Dreamina) — [N] frames, one per shot
### Frame 1: [time] [shot_type]
**Prompt:** 哥特暗黑韩漫风格, 9:16 vertical, [shot_type], [action], 
[Carmilla: 苍白肤色, 及肩黑色微卷发, 琥珀色瞳孔, 黑色长裙+银色项链], 
[场景: 古堡卧室, 石墙+烛台, 冷色调烛光], [mood]

### Frame 2: ...

## Video Prompts (Seedance) — 每3-4个连续镜头合并为一段
### Shot [N]: [time_range]
**Prompt:** [action_sequence], camera [movement], [mood]
**Duration:** [N]s
```

**Prompt 注入规则：**
- 每张 frame prompt 开头 = 风格 + 画幅 + 角色外观描述 + 场景描述
- 角色外观描述**逐字复制**自 manifest.md，不可自由发挥
- 多角色同框时，每个角色的外观描述都要包含
- 新角色首次出场时，同时更新 manifest.md

### 帧级 Prompt 场景 + 道具批量注入（v2.1 ⭐ 2026-04-29 Carmilla 项目验证）

> **v3.2 升级（2026-05-15 导演反馈）**：
> - Image Prompt 中每个场景/道具引用后必须标注 `key props: [道具名]`，与 manifest 道具清单一致
> - Video Prompt 开头必须声明参考图：`@图片1: ep01/compressed/kf1_shot1_*.png`（Seedance 2.0 @语法）
> - 每个主要角色在 manifest.md 中必须有 3 视图 Prompt（front/side/back）
> - 全局资源（角色图/场景图/道具图）存 `visual_assets/`，分集资源（关键帧）存 `epXX/`

> 当剧本表格里所有行都只有 `S-01`（无场景名）时，帧 prompt 无法区分场景变化。需要**从动作描述推断场景切换**，并用**时间范围匹配**将帧映射到脚本行。

**场景推断规则（Action → Scene）：**
```
关键词映射示例：
"走廊" → 走廊 | "冲开门"/"打开门" → 走廊 | "走廊空" → 走廊空荡
"花园" → 花园 | "走出" → 城堡外 | "大厅" → 大厅
"书房" → 书房 | "楼梯" → 楼梯 | "厨房" → 厨房
"墓园" → 墓园 | "废墟" → 废墟 | "仪式" → 仪式室
```

**场景继承逻辑（关键！）：**
```
1. S-XX 带显式场景名（如 "S-01 Laura卧室"）→ 使用该场景，设为 prev_scene
2. S-XX 无显式名（如 "S-01"）→ 查 S-XX→name 映射表
   - 映射表有值 → 用映射值，但先用动作关键词检查是否场景切换
   - 映射表无值 → 从动作推断或继承 prev_scene
3. 一旦推断出场景变化，后续无关键词的行继承新场景
```

**时间匹配策略（不要用重叠面积！）：**
```
❌ 错误：用时间重叠面积匹配 → 大区间帧会匹配到前面的小区间脚本行
   例：Frame 53-57s 与脚本 46-50s 重叠4秒 > 与 55-58s 重叠2秒 → 选错场景

✅ 正确：用帧 start 时间距离脚本行 start 时间最近的匹配
   例：Frame 57-65s → 找 |57 - script_row.start| 最小的行 → 55-58s (dist=2)
   结果：正确匹配到走廊场景
```

**道具注入方法：**
```python
# 中文动作关键词 → 英文道具描述映射
PROP_KEYWORDS = {
    "镜子": "ornate antique full-length mirror with carved frame",
    "日记": "leather-bound diary with faded ink writing",
    "茶杯": "porcelain teacup on a wooden table",
    "照片": "old sepia-toned photograph in a silver frame",
    "匕首": "ornate silver dagger with engraved handle",
    "窗外": "tall Gothic arched window with moonlight streaming through",
    "脚印": "wet footprints on stone floor slowly evaporating",
    # ... 24+ props mapped
}

# 注入位置：scene 描述之后
# scene: [Gothic castle corridor, stone walls, ...], ornate silver dagger with engraved handle
```

**批量处理脚本模式：**
```
fix_prompts.py → parse_script_scenes() → match_frame_to_script() → fix_frame()
- parse_script_scenes: 解析脚本表格，建立 S-XX→name 映射 + 动作推断 + 场景继承
- match_frame_to_script: 按帧 start 时间最近匹配脚本行
- fix_frame: 替换 scene: [...] + 注入 props
- 正则：r'(### Frame (\\d+): ([\\d\\-]+s.*?)\\n\\*\\*Prompt:\\*\\*)(.*?)(?=\\n###|\\Z)'
```

**常见陷阱：**
- ❌ 帧时间含中文后缀（`46-50s 近景`）→ 需要 `clean_time()` 提取纯时间
- ❌ 脚本行有重叠时间段（52-55s 和 53-57s）→ start 时间匹配解决
- ❌ 道具已存在于 scene 描述中 → 注入前检查前3个词是否已有
- ❌ S-XX 映射被动作推断覆盖后，所有 S-XX 行都变新场景 → 仅在推断≠映射时更新


### AI 工具限制速查表（v3.7 ⭐ 新增）

> 写 Prompt 前必查：不同 AI 工具的能力边界和已知坑点。

| 限制项 | Seedance 2.0 (视频) | Dreamina (图片) | Midjourney v6 (图片) | 通用规避策略 |
|--------|---------------------|-----------------|---------------------|-------------|
| 多人同框 | ≤2人稳定，3人易变形 | ≤3人，4+人面部崩 | ≤2人推荐 | 关键帧≤2人，群戏用叠化/切分 |
| 手部 | 经常多指/变形 | 较好但仍需约束 | 较好 | "hands behind back" / "hands in pockets" |
| 文字生成 | 会生成乱码文字 | 偶尔可生成英文 | 偶尔可生成英文 | "no text, no letters, no words" |
| 镜面反射 | 镜中人变形 | 镜面可能空白 | 镜面效果不稳定 | "no mirrors, no reflective surfaces" |
| 复杂手势 | 手指交叉/握拳易崩 | 较好 | 较好 | "simple hand gesture, hands visible" |
| 动物 | 有限支持 | 较好 | 较好 | 非必要不用动物，"no animals" |
| 快速运动 | 运动模糊/拖影 | N/A | N/A | 拆为多段短运动+转场 |
| 液体/火焰 | 穿模/变形 | 较好 | 较好 | "no fluid simulation" / 静态替代 |
| 服装细节 | 纽扣/图案可能漂移 | 较好 | 较好 | 简化服装描述，避免复杂图案 |
| 面部微表情 | 有限，大表情更稳 | 较好 | 较好 | 用大表情关键词，避免"微微一笑" |

### 场景图 / 道具图 Reference 体系（v2.2 ⭐ 2026-04-29 新增）

> **背景**：视频生成工具（Plank/Seedance 等）支持参考图输入。为保持场景和关键道具的一致性，我们为每个场景和关键道具生成独立的 reference prompt（纯环境/静物图），然后在关键帧 prompt 中用引用标记指向它们，而非重复写完整描述。

**核心优势：**
- 场景只描述一次 → 全剧一致性
- 关键帧 prompt 大幅精简 → 节省 token
- 视频生成时参考图 + 精简 prompt 一起传入 → 效果更好

**数据模型（`project_data.json` 新增顶级字段）：**

```json
{
  "scenes": [
    {
      "id": "S-01",
      "name": "Laura卧室",
      "prompt": "Gothic Korean manga style, 9:16 vertical, wide establishing shot, no characters, environmental scene reference, Gothic Victorian bedroom, cool candlelight tones, heavy velvet curtains, carved Victorian bed with tall posts, ornate antique mirror, bedside candlestick, stone walls, moonlight through arched window",
      "status": "pending"
    }
  ],
  "props": [
    {
      "id": "P-01",
      "name": "日记",
      "prompt": "Gothic Korean manga style, close-up still life, no characters, prop reference, leather-bound diary with aged pages and old handwriting, open on dark wooden desk, candlelit",
      "status": "pending"
    }
  ]
}
```

**关键帧 Prompt 改造：**

```
改前（场景描述嵌在 prompt 里）：
Gothic Korean manga style, 9:16 vertical, close-up,
scene: [Gothic Victorian bedroom, cool candlelight tones, heavy velvet curtains...],
a 17-year-old girl waking in terror...

改后（用引用标记替代场景描述）：
Gothic Korean manga style, 9:16 vertical, close-up,
[ref: S-01],
a 17-year-old girl waking in terror, hand touching her neck, Victoria nightgown
```

**Image Prompt 新增字段：**
```json
{
  "frame": 1,
  "time": "0-2s 特写",
  "scene_ref": "S-01",
  "prop_refs": ["P-01", "P-02"],
  "prompt": "Gothic Korean manga style, 9:16 vertical, close-up, [ref: S-01], a girl..."
}
```

**场景 Reference Prompt 写法规则：**
- 开头：风格 + 画幅 + `wide establishing shot`
- 包含：`no characters, environmental scene reference`（纯环境，不含角色）
- 描述：场景的完整视觉特征（风格、色调、光源、标志性元素）
- 每个唯一场景写一个，全剧约 10-15 个

**道具 Reference Prompt 写法规则：**
- 只覆盖**关键道具**（跨集出现、需要一致性的）
- 开头：风格 + `close-up still life`
- 包含：`no characters, prop reference`（静物特写）
- 描述：形状、材质、颜色、摆放环境
- 典型关键道具：日记、匕首、画像、特效（金色/紫色光/雾）等
- 龙套道具（茶杯、毛毯等）不需要单独写

**执行流程：**
1. 遍历全部分镜 imagePrompts，提取唯一场景（去重后 ~10-15 个）
2. 为每个场景写 prompt（纯环境描述）
3. 从 manifest 道具清单筛选关键道具（出现 ≥2 集）
4. 为每个关键道具写 prompt（静物特写）
5. 改造关键帧 prompt：删除 `scene: [...]` 和重复的道具描述，替换为 `[ref: S-XX]` + `scene_ref` / `prop_refs` 字段
6. 将场景/道具 Reference Prompt 章节**追加到 manifest.md** 末尾
7. 生成 `scene_prop_data.json` 数据结构（scenes 数组 + props 数组）
8. 更新 `project_data.json` 结构
9. 更新 `build_html.py`：新增"场景管理"和"道具管理" Tab 页（见 references/v2.2-migration.md）
10. 重新生成 `index.html`

> **v2.2 执行检查清单 → v2.3 三文件检查清单（每轮必须验证）**：
> 1. `characters.md` 是否完整（角色性格、动机、关系）？
> 2. `scene_prop_data.json` 是否存在且含 scenes/props 数组（每个唯一场景一个 prompt）？
> 3. `manifest.md` 是否精简（只含服装指南、表情库、全局规则，不含角色外观/场景描述重复内容）？
> 4. Prompts 中的场景描述是否已替换为 `[ref: S-XX]` 引用标记？
> 5. 改造后每集的 `[ref: S-XX]` 标记数是否 ≥ 帧数？
> **任一未通过 → 必须先补完再继续分镜/生图。**

**迁移脚本模板见**：`scripts/migrate_v2.2.py`（可复用模板，编辑 SCENES/PROPS/KEYWORDS 后直接运行）

### 角色 Reference 体系（v2.3 ⭐ 2026-04-30 Carmilla 项目验证新增）

> **背景**：同场景/道具，角色外观描述在每个 prompt 中重复，导致 token 浪费 + 跨集角色漂移。将角色外观收敛为 `[ref: C-XX]` 引用，prompt 只保留服装 + 表情叠加。

**核心优势：**