# Quickstart 速查卡

> 一页纸快速参考，详细内容见各 parts/ 文件。目标市场：**欧美**（唯一）。

---

## 小说改编项目先读这1个文件

1. **`novel-adaptation.md`** — 阶段0：原著分析 + 支线取舍 + 中式→欧美转译 + adaptation-map

## 写剧本时读这4个文件

1. **`pitfalls.md`** — 爆款原则 + Beat Engine + Premise + DI + 对白=行动 + 炫技防控
2. **`continuity.md`** — 上集Cliffhanger + 到期伏笔 + 角色状态（只读3项核心）
3. **`templates.md`** — 剧本模板 + 时间预算
4. **`workflow.md` 阶段4** — 流程步骤/骨架模式；写 Cliffhanger 标注时查 `reviewers-scoring.md` 的**钩子等级表**

## 写分镜时读这4个文件

1. **`templates.md`** — 分镜模板 + Lighting/Atmosphere/SFX/BGM写法规范
2. **`continuity.md`** — visual_continuity（上集结尾视觉快照）
3. **`reference-system.md`** — 角色外观 + 场景/道具Reference
4. **`workflow.md` 阶段5** — 链式批量 + FAIL级联；Camera 列标注时查 `reviewers-scoring.md` 的**运镜分级表**；竖屏视觉语法见 `architecture.md`

## 写Prompts时读这3个文件

1. **`reference-system.md`** — 三文件架构 + Reference注入规则
2. **`ai-tools.md`** — AI工具限制速查（写前必查）
3. **`templates.md`** — Prompt模板

## 审核时读这2个文件

1. **`reviewers-scoring.md`** — Aligner评分表 + 扣分规则 + 钩子等级表
2. **`reviewers-workflow.md`** — 输出格式 + 工作流

## 关键集审核额外读1个文件

1. **`reviewers-agents.md`** — 选观众旁白Agent（首集→GenZ，付费墙集→付费墙精算师）

## 审核不通过时读这1个文件

1. **`reviewers-patterns.md`** — 创作法则 + 审核通过关键要素 + 常见陷阱

---

## 核心规则速记

### Beat Engine（每集必遵）
```
Hook(0-15s) → Friction(15-60s) → Spike(60-85s) → Button(最后5-10s)
引爆不是铺垫    可拍摄冲突      重新定价+静音测试   问题前切断
```

### Premise（大纲阶段必检）
冲突内建于设定，不是场景制造。**唯一判据：同框即张力**。已验证示例8种（Enemies-to-lovers / Forbidden proximity / Power imbalance / Arranged circumstance / Fated mates / Second chance / Secret baby / Victim's return），见 pitfalls.md#三

### Dramatic Irony（EP2-3必建）
观众知道角色不知道 → 维持差距到付费墙后 → 与cliffhanger互补的跨集留存（卡点靠cliffhanger，粘性靠DI）

### 对白=行动
每句推进冲突或压力下揭示角色。角色不解释感受，Subtext>Text

### 竖屏铁律
特写/近景≥50%，全景/中景≤30%。vertical drama lives in faces, not locations.

### 付费墙（paywall_ep 参数化，默认 EP-08）
免费区(EP1~paywall_ep-1)最强钩子，末集Spike重定价+全剧最强cliffhanger卡币 → 首付转化(+3集)DI拉大 → 深度绑定(中段)DI维持 → 揭秘区(最后1/4)
详见 `continuity.md` 付费墙规划

### 炫技防控
- 🟡运镜 ≤2个/集 + 必须写理由
- 钩子：能用单一的不用复合，能用低级的不用高级
- 核心冲击力(12分)最高权重：合规但无聊=不及格

### 每集收尾三件事（唯一需要记住的习惯）
1. 更新 continuity 核心三项（分镜完成另加 visual_continuity 快照）
2. `python3 <技能目录>/tools/validate_ep.py EP-XX --project .` → FAIL 不进下一集
3. 全绿 → `git commit -m "EP-XX: 定稿"`（回退/差异/恢复全靠 git）

---

## 工作流（阶段0-7）

```
0.小说改编 → 1.大纲 → 2.人物 → 3.视觉资产(全局一次) → 4.逐集剧本(串行) → 5.批量分镜 → 6.批量Prompts → 7.工作台
```

- **阶段0仅小说/Idea输入时执行**（产出 adaptation-map）
- **阶段4必须串行**（叙事连续性不可妥协）
- **阶段5-6可批量**（分镜/Prompts间无叙事依赖）
- 每阶段结束 → 人工确认定稿

---

## 审核模式（v5.1 简化）

逐集常规=仅Aligner；关键集（首集/付费墙集/超自然题材）+1个观众旁白Agent；全剧审查+3个。
**激活表唯一出处**：`reviewers-agents.md` 激活策略。
