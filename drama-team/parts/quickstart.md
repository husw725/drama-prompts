# Quickstart 速查卡

> 一页纸快速参考，详细内容见各 parts/ 文件。

---

## 写剧本时读这3个文件

1. **`pitfalls.md`** — 爆款原则 + Beat Engine + Premise + DI + 对白=行动 + 炫技防控
2. **`continuity.md`** — 上集Cliffhanger + 到期伏笔 + 角色状态（只读3项核心）
3. **`templates.md`** — 剧本模板 + 分镜模板

## 写分镜时读这3个文件

1. **`templates.md`** — 分镜模板 + Lighting/Atmosphere/SFX/BGM写法规范
2. **`continuity.md`** — visual_continuity（上集结尾视觉快照）
3. **`reference-system.md`** — 角色外观 + 场景/道具Reference

## 写Prompts时读这3个文件

1. **`reference-system.md`** — 三文件架构 + Reference注入规则
2. **`ai-tools.md`** — AI工具限制速查（写前必查）
3. **`templates.md`** — Prompt模板

## 审核时读这3个文件

1. **`reviewers-agents.md`** — 选哪几个Agent（按剧类型）
2. **`reviewers-scoring.md`** — 评分表 + 扣分规则 + 钩子等级表
3. **`reviewers-workflow.md`** — 输出格式 + 综合工作流

## 审核不通过时读这1个文件

1. **`reviewers-patterns.md`** — 创作法则 + 审核通过关键要素 + 常见陷阱 + 实战教训

---

## 核心规则速记

### Beat Engine（每集必遵）
```
Hook(0-15s) → Friction(15-60s) → Spike(60-90s) → Button(最后5-10s)
引爆不是铺垫    可拍摄冲突      重新定价+静音测试   问题前切断
```

### Premise（大纲阶段必检）
冲突内建于设定，不是场景制造。4种：Enemies-to-lovers / Forbidden proximity / Power imbalance / Arranged circumstance

### Dramatic Irony（EP2-3必建）
观众知道角色不知道 → 维持差距到付费墙后 → 比cliffhanger更强留存

### 对白=行动
每句推进冲突或压力下揭示角色。角色不解释感受，Subtext>Text

### 竖屏铁律
特写/近景≥50%，全景/中景≤30%。vertical drama lives in faces, not locations.

### 付费墙 3-7-21
| Block | 集数 | 策略 |
|-------|------|------|
| Block 1 | EP 1-3 | 免费，最强钩子 |
| Block 2 | EP 4-7 | 首次付费，沉没成本 |
| Block 3 | EP 8-21 | DI维持，允许更慢 |
| Block 4 | EP 22+ | 揭秘区 |

### 炫技防控
- 🟡运镜 ≤2个/集 + 必须写理由
- 钩子：能用单一的不用复合，能用低级的不用高级
- 核心冲击力(12分)最高权重：合规但无聊=不及格

---

## 七阶段工作流

```
1.大纲 → 2.人物 → 3.视觉资产(全局一次) → 4.逐集剧本(串行) → 5.批量分镜 → 6.批量Prompts → 7.工作台
```

- **阶段4必须串行**（叙事连续性不可妥协）
- **阶段5-6可批量**（分镜/Prompts间无叙事依赖）
- 每阶段结束 → 人工确认定稿

---

## 审核Agent快速选择

| 剧类型 | 轻量3人 |
|--------|---------|
| 复仇 | 02工人 + 05影评 + 08付费墙 |
| 强制爱 | 01主妇 + 04高知 + 08付费墙 |
| 玛丽苏 | 01主妇 + 03GenZ + 08付费墙 |
| 悬疑 | 05影评 + 10亚文化 + 08付费墙 |
| 甜宠 | 01主妇 + 03GenZ + 08付费墙 |
| 默认 | 01主妇 + 05影评 + 08付费墙 |

**08付费墙始终入选**（商业底线不可妥协）
