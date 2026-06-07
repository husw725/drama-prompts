# 审核系统索引

> v4.2 拆分为3个文件，按需加载。Agent定义见 `parts/reviewers-agents.md`，创作法则见 `parts/reviewers-patterns.md`。

---

## 文件索引

| 文件 | 行数 | 内容 | 何时读取 |
|------|------|------|---------|
| [`reviewers-scoring.md`](reviewers-scoring.md) | ~450 | 三Aligner评分表+扣分规则+钩子等级表+运镜分级+评分校准 | **审核时**（评分+扣分） |
| [`reviewers-workflow.md`](reviewers-workflow.md) | ~140 | 综合工作流+集间衔接检查+输出格式+Reviewer-Combo关系 | **写审核报告时**（流程+格式） |
| [`reviewers-agents.md`](reviewers-agents.md) | ~234 | 十视角Agent定义+人设+激活策略 | **选审核Agent时** |

---

## 读取规则

| 场景 | 读取文件 |
|------|---------|
| 逐集轻量审核 | `reviewers-agents.md`(选人) + `reviewers-scoring.md`(评分) |
| 审核不通过 | `reviewers-scoring.md`(扣分规则) + `reviewers-patterns.md`(创作法则) |
| 写审核报告 | `reviewers-workflow.md`(输出格式) |
| 全剧审查 | 3个文件全读 |
