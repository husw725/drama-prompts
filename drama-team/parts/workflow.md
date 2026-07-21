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

## 阶段 0：小说改编（输入为小说/Idea 时）

> 详见 `parts/novel-adaptation.md`：原著分析 → 取舍决策 → 中式→欧美转译 → 集数规划 → 原著对照表（adaptation-map.md）。
> 输入已是大纲/剧本时可跳过；好莱坞格式剧本走 `parts/revision-workflows.md` 快速路径。

---

## 阶段 1-3：全局阶段

- **大纲** → 人工确认 → **人物** → 人工确认 → **视觉资产** → 人工确认（关键）
- 大纲阶段必须执行 Premise 自检（见 pitfalls.md#三）
- 视觉资产阶段见 `parts/reference-system.md` 三文件架构；确认后三文件就绪：characters.md + manifest.md + scene_prop_data.json

### 阶段 1 前置：类型DNA提取 🔥

> **在大纲生成前，先提取本项目的类型DNA**。类型DNA是编剧写大纲和剧本时的"基因"，确保从源头就对齐类型特征，减少Aligner事后纠偏。

**提取步骤**：
1. 确认项目类型（revenge/forced_love/sweet_romance/mary_sue/mystery/vampire_werewolf）
2. 从类型权重表（见 `parts/reviewers-scoring.md`）提取核心维度和权重
3. 提取该类型的**核心套路组合**和**禁忌模式**

**类型DNA模板（写入 outline.md 开头）**：
```markdown
## 类型DNA
- **项目类型**: revenge（复仇）
- **单集时长 (ep_duration)**: 90s（项目启动时问用户，未指定则默认 90s；全流程时间预算/校验以此为准）
- **总集数**: 60（商业规格 50-80 集；12/24 仅作 Demo/试水）
- **首个付费集 (paywall_ep)**: EP-08（项目启动时问用户，默认 EP-08；付费墙 Block、Spike 重定价集、Agent 08 激活均引用此值）
- **核心套路**: 三段式复仇（受辱→蛰伏→逐一打脸）+ 身份反转 + 不可逆代价
- **冲突升级模式**: 口头羞辱 → 肢体冲突 → 社会性死亡 → 生死对决
- **钩子偏好**: 危险钩子(3) + 不可逆钩子(7) + 后果链钩子(9)（复仇型偏高位钩子）
- **禁忌模式**: ①连续3集无打脸 ②原谅无前置铺垫 ③复仇目标模糊 ④蛰伏期超过4集
- **权力动态**: 主角从下位→上位，翻转点在第二幕中段
- **爽点节奏**: 每2集至少1个打脸/反转，蛰伏集用信息钩子补偿
```

> **用途**：编剧写大纲/剧本时读类型DNA，确保冲突模式、钩子选择、权力动态都从源头对齐。Aligner审核时对照类型DNA检查，而非凭"感觉"纠偏。

### 大纲标准结构（必须包含）

```markdown
# 故事大纲

## 类型DNA
[见上方模板]

## 三幕结构
### 第一幕：建立（EP-01 到 EP-N/3）
- 核心事件 / 角色建立 / 激励事件

### 第二幕：对抗（EP-N/3 到 EP-2N/3）
- 冲突升级节点 / 中段转折点 / 最低谷时刻

### 第三幕：解决（EP-2N/3 到 EP-N）
- 高潮构建 / 最终对决 / 结局（HE/BE/开放）

## 分集梗概
### EP-01: 标题
- **集定位**: 铺垫/转折/高潮/过渡/收束
- 核心事件（1-2句）
- 爽点类型（复仇/打脸/反转...）
- 结尾悬念
- **大纲承诺**：本集必须兑现的事件/揭示/转折（1-3项）
- **叙事预算**：新伏笔≤N个 / 新信息点≤N个 / 新角色≤N个
### EP-02: 标题
...

## 伏笔规划表
| ID | 描述 | 埋入集 | 回收集 | 重要性 |
|----|------|--------|--------|--------|
| F-01 | 紫色咬痕的秘密 | EP-01 | EP-04 | 🔴 核心 |

## 角色出场时间表
| 角色 | 首次出场 | 主要活跃集 | 退场集 | 备注 |
|------|---------|-----------|--------|------|
```

> **集定位说明**：
> - **铺垫集**：埋伏笔+建立信息，冲突≤1个，节奏偏慢，钩子偏信息型
> - **转折集**：关系/身份/认知发生不可逆变化，冲突≥1个且带代价，钩子偏不可逆型
> - **高潮集**：核心对决/揭示/爆发，冲突≥2个，节奏最快，钩子偏后果链型
> - **过渡集**：承接上集余波+推进下集铺垫，冲突≤1个小冲突，信息密度低
> - **收束集**：回收伏笔+收尾，冲突为解决性质，钩子为结局型（HE/BE/开放）

> **叙事预算说明**：
> - 新伏笔：前期集（EP-01~N/3）允许2-3个/集，中期1-2个/集，后期0-1个/集（以回收为主）
> - 新信息点：每集≤3个（超过观众跟不上）
> - 新角色：前3集允许2-3个/集建立核心角色，之后≤1个/集，后期0个

### 阶段 2：关系动力学建模 🔥

> 人物设定不再只是静态描述，必须建模**关系动力学**——关系如何随冲突升级而变化。

**关系动力学模板（写入 characters.md）**：
```markdown
## 关系动力学

### Laura × Carmilla
- **初始状态**: 陌生人→猎物（EP-01）
- **关系弧线**: 恐惧→危险暧昧→信任动摇→对立→理解→共生
- **转折点**:
  | 集数 | 转折 | 触发事件 | 权力动态变化 |
  |------|------|---------|-------------|
  | EP-01 | 陌生人→猎物 | Carmilla吸血 | Carmilla上位 |
  | EP-05 | 好奇→暧昧 | 身份部分揭示 | 权力拉平 |
  | EP-08 | 暧昧→对立 | 真相完全揭示 | Laura上位 |
- **张力节奏**: 推(EP-01)→拉(EP-03)→推(EP-05)→拉(EP-07)→推(EP-08)→拉(EP-11)（推=靠近/拉=远离）
```

> **用途**：编剧写剧本时读关系动力学，确保关系转折有触发事件、权力动态有变化、张力有推拉节奏。Aligner检查"关系转折突兀"时对照此模型。

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
 4. 更新 skeleton_continuity.md（格式：每集两行——Cliffhanger + 伏笔操作）
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

 Step 3: 更新continuity.md（每集必更核心三项：Cliffhanger/伏笔操作/角色状态；全文件整理压缩每3集一次）
 ⚠️ 逾期/到期伏笔必须每集检查（检查依赖核心三项为最新——这是每集必更的原因）
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

**⚠️ FAIL 重写级联（硬规则）**：FAIL 集重写后，①重新更新该集结尾视觉快照 ②对其**后一集**重跑"跨集视觉承接"检查（仅 Storyboard-Aligner 维度9）——后一集是基于旧快照生成的，快照变了必须复检。

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

---

## 文件依赖关系图 🔥

> 改了哪个文件需要同步更新哪些，按此图判断。

```
adaptation-map.md（小说改编项目）
 └──→ outline.md（阶段1取材依据；Aligner"大纲承诺兑现"引用）

outline.md
 ├──→ characters.md（依赖大纲中的角色）
 │     ├──→ visual_assets/manifest.md（依赖角色设定）
 │     ├──→ scene_prop_data.json（依赖角色使用的场景/道具）
 │     └──→ script/EP-XX.md（依赖角色身份）
 └──→ continuity.md（依赖大纲中的伏笔规划）
       └──→ script/EP-XX.md（依赖连续性信息）

visual_assets/manifest.md
 ├──→ prompts/EP-XX.md（依赖视觉规则）
 └──→ storyboard/EP-XX.md（依赖色调/光影）

scene_prop_data.json
 └──→ prompts/EP-XX.md（依赖场景/道具 Reference）

script/EP-XX.md
 ├──→ treatment/EP-XX.md（Director's Treatment 依赖剧本）
 ├──→ storyboard/EP-XX.md（依赖剧本内容）
 └──→ prompts/EP-XX.md（依赖剧本场景）

storyboard/EP-XX.md
 ├──→ visual_continuity.md（每集分镜完成后立即写入结尾快照）
 └──→ prompts/EP-XX.md（依赖分镜镜头）

visual_continuity.md
 ├──→ 下一集/下一批 storyboard/EP-XX.md（生成前必读）
 └──→ prompts/EP-XX.md（注入上集结尾快照）

TASK.md ←── 各阶段写入进度/伏笔告警/Override记录（格式契约见 parts/production.md）
```

**文件变更联动规则：**

| 修改了 | 必须同步更新 | 可选更新 |
|--------|-------------|---------|
| adaptation-map.md | outline.md（取材映射变化） | 无 |
| outline.md | continuity.md（伏笔规划） | characters.md（如果角色有变化） |
| characters.md | manifest.md（服装/表情） | scene_prop_data.json（如果新角色有新场景） |
| manifest.md | prompts/EP-XX.md | 无 |
| script/EP-XX.md | storyboard/EP-XX.md, prompts/EP-XX.md, continuity.md, treatment/EP-XX.md | 无 |
| storyboard/EP-XX.md | **visual_continuity.md（该集结尾快照）**, prompts/EP-XX.md | 无 |
| continuity.md | 下一集的 script/EP-XX.md | 无 |
| visual_continuity.md | 下一集的 storyboard/EP-XX.md, prompts/EP-XX.md | 无 |
