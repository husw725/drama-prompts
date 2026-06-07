# 七阶段工作流

> 每阶段开始前读取。生成策略/子代理策略见 `parts/pitfalls.md`。

---

## 流程总览

```
┌──────────┐ ┌──────────┐ ┌──────────────┐
│ 1.大纲 │ → │ 2.人物 │ → │ 3.视觉资产 │ ← 全局阶段（只跑一次）
└──────────┘ └──────────┘ └──────────────┘
 ✅ ✅ ✅
 人工确认 人工确认 人工确认（关键）

 ↓
 ┌───────────────────────────────────────────────────┐
 │ 叙事层：逐集剧本串行（核心！） │
 │ EP-01 → EP-02 → ... → EP-N │
 │ 每集：读continuity → 写剧本 → Aligner审核 → 更新 │
 └───────────────────────────────────────────────────┘
 ✅ 全部剧本定稿
 ↓
 ┌───────────────────────────────────────────────────┐
 │ 制作层：批量分镜 + 批量Prompts │
 │ 分镜：2-3集/批，链式读取visual_continuity │
 │ Prompts：2-3集/批，注入visual_continuity │
 └───────────────────────────────────────────────────┘
 ✅ 全部定稿 → 阶段7：工作台生成
```

**关键原则**：叙事层必须串行（连续性不可妥协）；制作层可批量（分镜/Prompts间无叙事依赖）。

---

## 阶段 1-3：全局阶段

- **大纲** → 人工确认 → **人物** → 人工确认 → **视觉资产** → 人工确认（关键）
- 大纲阶段必须执行 Premise 自检（见 pitfalls.md#三）
- 视觉资产确认后，三文件架构就绪：characters.md + manifest.md + scene_prop_data.json

---

## 阶段 4：叙事层 — 逐集剧本串行

> 唯一必须串行的阶段。剧本写完后进入人工确认，可反复修改直到定稿。

### 阶段 4a：骨架串行生成（提速方案 ⭐）

> 骨架是比大纲更细、比剧本更粗的中间层（~300字/集 vs 剧本~3000字/集）。先生成骨架经人工确认，剧本阶段只需填充。

**骨架格式**：
```markdown
### EP-04 骨架
- **集定位**: 转折集
- **开篇承接**: [回收上集Cliffhanger]
- **核心事件**: [本集核心事件]
- **冲突**: [冲突类型+不可逆代价]
- **关系转折**: [关系变化+触发点]
- **伏笔操作**: [回收/新埋]
- **大纲承诺兑现**: ✅/❌
- **Cliffhanger**: [悬念+钩子类型等级]
- **叙事预算**: 新伏笔N / 新信息点N / 新角色N
```

**骨架生成流程（串行 ⚠️）**：
```
for EP:
 1. 读 continuity.md + outline.md(集定位+类型DNA) + characters.md(关系动力学)
 2. 读 上一集骨架结尾（保证连续性）
 3. 生成骨架 → skeleton/EP-XX.md
 4. 更新 skeleton_continuity.md
 → 下一集
✅ 全部骨架 → 人工确认 → 阶段4b
```

**阶段4b：剧本填充**：读骨架 + continuity + 上集结尾 → 填充对白/动作/时长 → Aligner审核 → 更新continuity

**提速**：骨架~10s/集 vs 剧本30-60s/集，预估总提速30-40%

### 阶段 4 直接模式（不用骨架）

```
for EP:
 Step 0: 读取上下文（精简运行时 ⚠️）
 - continuity.md 核心三项：①Last Cliffhanger ②到期伏笔 ③角色状态
 - outline.md 对应集梗概 + 类型DNA
 - characters.md 关系动力学
 - continuity.md 付费墙Block策略
 - 上集script结尾
 - Premise自检 + Dramatic Irony状态
 ⚠️ 不读全量continuity.md

 Step 1: 编剧 → script/EP-XX.md
 - **爆款写法**（见 `pitfalls.md`）：Beat Engine + Premise自检 + 对白=行动 + 竖屏特写≥50%
 - 回收上集Cliffhanger（开篇3秒）
 - 处理到期伏笔
 - 结尾Cliffhanger标注钩子类型+等级

 Step 2: Aligner审核（含跨集连续性）
 - 检查：回收上集Cliffhanger？处理到期伏笔？冲突模式不重复？
 - FAIL → 重写 → 最多3轮，否则人工介入

 Step 3: 更新continuity.md（每3集批量更新，前3集逐集）
 ⚠️ 逾期/到期伏笔必须每集检查
```

---

## 阶段 5：制作层 — 批量分镜

> 前提：所有剧本已定稿。分镜间无叙事依赖，可批量生成。

### 阶段 5a：Director's Treatment

每集1页~500字：视觉策略+情绪弧线+Hero Shots+运镜策略+节奏策略 → 人工确认

**Treatment视觉衔接声明**：每集开头声明与上集的视觉衔接：
`## 视觉衔接：承接EP-XX结尾 — [色调]/[场景]/[角色位置]/[主光源]`

### 阶段 5b：执行分镜（链式批量 ⭐）

2-3集合并最佳，每批生成前读上一批尾集分镜 + visual_continuity.md，确保视觉不漂移。

**链式读取规则**：
- 第1批：读 visual_continuity.md + Treatment
- 第N批：读上一批尾集分镜 + visual_continuity.md + Treatment

→ Storyboard-Aligner批量审核 → FAIL集统一修改 → **每集分镜完成后立即更新 visual_continuity.md** → 人工确认

**⚠️ visual_continuity.md 更新节奏（硬规则）**：
- **每集分镜完成后立即更新**，不是批量结束后才更新
- 批量生成2-3集时，每写完1集就追加该集的结尾视觉快照
- 下批生成前必须读取已更新的 visual_continuity.md
- 原因：延迟更新会导致后续批次分镜与已生成分镜视觉不连续

---

## 阶段 6：制作层 — 批量 Prompts

> 前提：所有分镜已定稿。

**每集读取上下文**：script/EP-XX.md + characters.md + manifest.md + scene_prop_data.json + visual_continuity.md（上集结尾快照）

2-3集合并 → Prompt-Aligner批量审核 → FAIL集统一修改 → 人工确认

**⚠️ visual_continuity.md 读取（硬规则）**：
- 每集Prompts生成前必须读取 visual_continuity.md 中上集结尾快照
- 批量生成时，每集独立读取对应的上集快照（不是只读批次前最后一集）

---

## 阶段 7：工作台生成

见 `parts/production.md`
