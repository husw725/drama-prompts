# 🎬 Drama Team — 小说 → 欧美短剧全流程编剧技能

> 从小说/Idea 到剧本、分镜、AI 生图 Prompt、离线工作台的一站式创作系统。
> 当前版本 **v5.4**，目标市场**欧美竖屏短剧**（ReelShort/DramaBox 类平台）。

## 入口

**一切从 [`SKILL.md`](./SKILL.md) 开始** — 它是模块索引，告诉你每个阶段读 `parts/` 下的哪个文件。

新 session 第一步：读 [`parts/quickstart.md`](./parts/quickstart.md)（一页纸速查卡）。

## 核心设计

- **七阶段工作流**：小说改编 → 大纲 → 人物 → 视觉资产 → 逐集剧本（串行）→ 批量分镜 → 批量 Prompts → 工作台
- **叙事层/制作层分离**：剧本必须串行（连续性不可妥协），分镜/Prompts 可批量
- **欧美爆款方法论**：Beat Engine（Hook→Friction→Spike→Button）+ Premise-Driven Conflict + Dramatic Irony + 付费墙 paywall_ep 参数化 Block 分层 + 竖屏特写优先
- **三 Aligner 审核**：Script/Storyboard/Prompt 三个专用审核员独立评分（≥80 PASS），关键集可选 Agent 观众旁白
- **视觉一致性**：characters.md + manifest.md + scene_prop_data.json 三文件架构 + `[ref: C-XX/S-XX/P-XX]` 引用体系 + visual_continuity.md 跨集追踪

## 相关文件

| 文件 | 用途 |
|------|------|
| [`SKILL.md`](./SKILL.md) | 技能入口 + 模块索引 |
| [`parts/`](./parts/) | 17 个按需加载的模块 |
| [`RATIONALE.md`](./RATIONALE.md) | 每条规则的来源、原因和行业验证（不参与运行时加载） |
| 同仓库 `short-drama-production-index/` | 工作台 SPA 模板与构建脚本 |

## 注意事项

- **AI 审核有局限** — Aligner 本身是 AI，必须人工最终把关
- **FAIL 成本** — 同一问题最多 3 轮，第 3 轮仍 FAIL 立即人工介入
- *AI 产出 60 分骨架，人工提升到 80 分精品*

## 许可证

MIT
