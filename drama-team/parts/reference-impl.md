# Reference 体系 — 实现细节

> 核心概念见 `parts/reference-system.md`，AI工具限制见 `parts/ai-tools.md`

---

## 帧级 Prompt 场景 + 道具注入

### 场景推断规则

```
关键词映射：
"走廊" → 走廊 | "冲开门" → 走廊 | "花园" → 花园 | "走出" → 城堡外
"书房" → 书房 | "楼梯" → 楼梯 | "墓园" → 墓园 | "仪式" → 仪式室
```

**场景继承逻辑**：
1. S-XX 带显式场景名 → 使用该场景，设为 prev_scene
2. S-XX 无显式名 → 从动作推断或继承 prev_scene
3. 推断出场景变化后，后续无关键词的行继承新场景

### 时间匹配（用帧start距离，不用重叠面积）

```
❌ 重叠面积匹配 → 大区间帧匹配到前面的小区间脚本行
✅ |frame.start - script_row.start| 最小的行
```

### 道具注入

- 中文动作关键词 → 英文道具描述映射（镜子/日记/匕首/窗外等24+个）
- 注入位置：scene 描述之后
- 注入前检查：道具是否已存在于 scene 描述中

---

## 场景图 / 道具图 Reference 体系

### 数据模型（`scene_prop_data.json`）

```json
{
  "scenes": [
    { "id": "S-01", "name": "Laura卧室", "prompt": "...", "status": "pending" }
  ],
  "props": [
    { "id": "P-01", "name": "日记", "prompt": "...", "status": "pending" }
  ]
}
```

### 关键帧 Prompt 改造

```
改前：scene: [Gothic Victorian bedroom, cool candlelight tones, ...], a girl...
改后：[ref: S-01], a girl...
```

### 写法规则

**场景 Reference**：风格 + 画幅 + `wide establishing shot` + `no characters, environmental scene reference` + 完整视觉特征。每个唯一场景写一个，全剧约10-15个。

**道具 Reference**：只覆盖关键道具（跨集出现≥2集）。风格 + `close-up still life` + `no characters, prop reference` + 形状/材质/颜色/摆放。

### 执行流程

1. 提取唯一场景（去重~10-15个）→ 写场景 prompt
2. 筛选关键道具 → 写道具 prompt
3. 改造关键帧 prompt：替换为 `[ref: S-XX]`
4. 追加到 `manifest.md` + 生成 `scene_prop_data.json`

### 三文件检查清单

1. `characters.md` 完整（角色性格、动机、关系）？
2. `scene_prop_data.json` 存在且含 scenes/props 数组？
3. `manifest.md` 精简（只含服装指南、表情库、全局规则）？
4. Prompts 中场景描述已替换为 `[ref: S-XX]`？

---

## 角色 Reference 体系

- 角色外观收敛为 `[ref: C-XX]` 引用，prompt 只保留服装 + 表情叠加
- 角色外观改 → 只改 `characters.md`
- 场景/道具改 → 只改 `scene_prop_data.json`
- 服装/情绪/色调改 → 只改 `manifest.md`

---

## 常见陷阱

- ❌ 帧时间含中文后缀（`46-50s 近景`）→ 需要 `clean_time()` 提取纯时间
- ❌ 脚本行有重叠时间段 → start 时间匹配解决
- ❌ 道具已存在于 scene 描述中 → 注入前检查
- ❌ S-XX 映射被动作推断覆盖后所有行都变新场景 → 仅在推断≠映射时更新
