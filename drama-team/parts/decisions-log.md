# 历史决策指针

> 执行时不需读取。本文件**不复述规则**（复述必漂移）——硬规则唯一出处：`pitfalls.md` §一；评分规则唯一出处：`reviewers-scoring.md`。
> 完整的"决策 → 根因 → 行业验证"记录见 [`../RATIONALE.md`](../RATIONALE.md)（尤其第九章"版本演进驱动力"）；版本演进表见 `SKILL.md`。

## 同步纪律

凡修改 parts/ 内的硬规则或评分规则，必须在**同一 commit** 中更新 RATIONALE.md 对应条目——否则运行时规则与理由文档会讲两个故事，且 RATIONALE 不在运行时加载路径，漂移不会立刻暴露。
