# 审核系统索引

> v5.1 简化：Aligner 独立评分 + Agent 观众旁白（可选）。Agent 不再打分。

---

## 文件索引

| 文件 | 内容 | 何时读取 |
|------|------|---------|
| [`reviewers-scoring.md`](reviewers-scoring.md) | 三Aligner评分表+扣分规则+钩子等级表+运镜分级+评分校准 | **审核时**（评分+扣分） |
| [`reviewers-workflow.md`](reviewers-workflow.md) | 工作流+集间衔接检查+输出格式+架构说明 | **写审核报告时**（流程+格式） |
| [`reviewers-agents.md`](reviewers-agents.md) | 十视角Agent定义+人设+激活策略+观众旁白格式 | **选观众旁白Agent时** |

---

## 读取规则

| 场景 | 读取文件 |
|------|---------|
| 逐集审核 | `reviewers-scoring.md`（Aligner评分） |
| 关键集（首集/付费墙集） | `reviewers-scoring.md` + `reviewers-agents.md`（选旁白Agent） |
| 审核不通过 | `reviewers-scoring.md`（扣分规则） + `reviewers-patterns.md`（创作法则） |
| 写审核报告 | `reviewers-workflow.md`（输出格式） |
| 全剧审查 | 3个文件全读 |
