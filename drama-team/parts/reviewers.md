# 审核系统（索引）

> v5.1：Aligner 独立评分（核心） + Agent 观众旁白（可选，不打分）。

| 文件 | 内容 | 何时读取 |
|------|------|---------|
| [`reviewers-scoring.md`](reviewers-scoring.md) | 欧美市场标准+类型权重表+三Aligner评分表+扣分规则+钩子等级+运镜分级+评分自检 | **审核时**（评分+扣分） |
| [`reviewers-workflow.md`](reviewers-workflow.md) | 工作流+集间衔接检查+输出格式+架构说明 | **写审核报告时** |
| [`reviewers-agents.md`](reviewers-agents.md) | 十视角Agent定义+人设+观众旁白格式+激活策略+Industry Ground Truth | **选观众旁白Agent时** |
| [`reviewers-patterns.md`](reviewers-patterns.md) | 创作法则+审核通过关键要素+常见陷阱+实战教训 | 项目开始前；审核不通过时 |

### 快速路由

| 场景 | 读取文件 |
|------|---------|
| 逐集审核 | `reviewers-scoring.md` |
| 关键集（首集/付费墙集） | `reviewers-scoring.md` + `reviewers-agents.md` |
| 审核不通过 | `reviewers-scoring.md` + `reviewers-patterns.md` |
| 写审核报告 | `reviewers-workflow.md` |
| 全剧审查 | 4 个文件全读 |
