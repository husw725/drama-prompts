# 三文件架构与 Reference 体系

> 阶段3（视觉资产）与阶段6（写 Prompts）时读取。实现细节见 `parts/reference-impl.md`，AI 工具限制见 `parts/ai-tools.md`。

---

## 阶段 3：视觉资产 — 三文件架构

> **这是跨集视觉一致性的关键阶段。** 基于人物设定，创建三个职责单一的文件，后续所有 Prompts 必须引用这三份文件。

**三文件架构（单一职责原则）：**

```
characters.md         ← 角色是谁（性格、动机、弧光、关系、base_prompt/outfits/expressions）
scene_prop_data.json  ← 场景/道具 Reference Prompts（AI生图参考图）
manifest.md           ← 视觉规则（服装指南、表情库、色调/光影/构图）
```

**为什么三分离？**（2026-04-30 Count of Monte Cristo 项目验证）
- 旧版 manifest.md 塞了角色外观+场景描述+服装+道具 → 46KB 臃肿文件
- `characters.md` 已有角色外观，`scene_prop_data.json` 已有场景/道具 → manifest.md 大量重复
- 精简后 manifest.md 保留**不可替代的内容**：服装场景映射、表情关键词、色调/光影/构图规则 → 16KB
- 三文件互不重复，各司其职，维护清晰

**产出文件 1：`characters.md`**（角色身份 + base_prompt/outfits/expressions，数据模型见 `parts/reference-impl.md`）

**产出文件 2：`scene_prop_data.json`**

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

### 光影规则 / 构图规则 / 风格元素
（按项目风格填写）
```

**Prompt 编写流程**：
1. `characters.md` → 确认角色身份 → `[ref: C-XX]`
2. `scene_prop_data.json` → 取场景/道具 ID → `[ref: S-XX]` / `[ref: P-XX]`
3. `manifest.md` → 取服装（按场景）+ 表情（按情绪）
4. `manifest.md` → 取色调/光影/构图规则

**三文件创建顺序：**
1. 基于 `characters.md` → 视觉导演为每个角色写服装表 + 表情关键词
2. 遍历剧本场景头 → 提取唯一场景（去重后 ~10-15 个）→ 写 `scene_prop_data.json.scenes[]`
3. 识别关键道具（跨集出现≥2集）→ 写 `scene_prop_data.json.props[]`
4. 编写 `manifest.md` → 场景/道具速查表 + 服装指南 + 表情库 + 全局规则
5. **人工确认** — 三文件必须经导演（用户）确认后进入剧本阶段

---

## 阶段 6：Prompts 视觉资产强制注入 ⭐

> **每张图 Prompt 开头必须注入对应的角色外观描述（从三文件拉取）。**

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
[ref: C-01], black_dress, fear,
[ref: S-01], [mood]

### Frame 2: ...

## Video Prompts (Seedance) — 每3-4个连续镜头合并为一段
### Shot [N]: [time_range]
**Prompt:** [action_sequence], camera [movement], [mood]
**Duration:** [N]s
```

**Prompt 注入规则：**
- 每张 frame prompt 开头 = 风格 + 画幅 + 角色外观（`[ref: C-XX]` + 服装 + 表情）+ 场景（`[ref: S-XX]`）
- 角色外观描述**逐字复制/引用**自三文件，不可自由发挥
- 多角色同框时，每个角色的外观描述都要包含
- 新角色首次出场时，同时更新 characters.md + manifest.md

> 帧级 Prompt 批量注入、场景推断、时间匹配等实现细节见 `parts/reference-impl.md`
