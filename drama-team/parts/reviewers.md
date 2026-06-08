# 审核系统（索引）

> v5.1 简化：Aligner 独立评分 + Agent 观众旁白（可选，不打分）。

| 文件 | 内容 | 何时读取 |
|------|------|---------|
| [`reviewers-agents.md`](reviewers-agents.md) | 十视角Agent定义+人设+观众旁白模式+Industry Ground Truth | 选观众旁白Agent时 |
| [`reviewers-aligners.md`](reviewers-aligners.md) | 审核系统文件索引 | 确认读取哪些文件时 |
| [`reviewers-scoring.md`](reviewers-scoring.md) | 三Aligner评分表+扣分规则+钩子等级+运镜分级+评分校准 | 评分时；扣分时 |
| [`reviewers-workflow.md`](reviewers-workflow.md) | 工作流+集间衔接+输出格式+架构说明 | 写审核报告时 |
| [`reviewers-patterns.md`](reviewers-patterns.md) | 创作法则+审核通过关键要素+常见陷阱+实战教训+示例 | 项目开始前；审核不通过时 |

### 快速路由
- **跑Aligner评分** → 读 `reviewers-scoring.md`
- **选观众旁白Agent** → 读 `reviewers-agents.md`
- **写审核报告** → 读 `reviewers-workflow.md`
- **查创作法则/踩坑** → 读 `reviewers-patterns.md`
- **全量审核** → 4个文件都读
