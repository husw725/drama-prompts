---
name: drama-team
description: 小说→欧美短剧全流程系统 — 小说改编方法论+叙事层串行+制作层批量分离+类型参数化+付费墙建模+模块化拆分，含剧集连续性追踪、伏笔管理、视觉一致性管控与独立审核机制
version: 5.2
author: Hermes Agent + User
license: MIT
metadata:
  hermes:
    tags: [Short-Drama, Scriptwriting, Creative-AI, Novel-Adaptation, Visual-Consistency, Continuity, Foreshadowing, Sequential-Generation]
    related_skills: [hermes-agent, writing-plans, short-drama-production-index]
---

# Drama Team 短剧编剧团队 v5.2

> 小说 → 优质欧美短剧全流程系统：从小说/Idea到剧本、分镜、AI生图Prompt。目标市场：**欧美竖屏短剧**（唯一）。
> **v5.2**: 结构修复+欧美聚焦 — 修复模块拆分残缺文件，templates补齐剧本/分镜格式契约，新增阶段0小说改编方法论(novel-adaptation)，评分体系统一为类型权重表单一真相源(每列合计100)，删除多区域矩阵彻底聚焦欧美
> **v5.1**: 审核系统简化 — Agent降级为观众旁白(不打分)，Aligner独立评分，Token消耗降60%
> **v4.x**: Beat Engine+Premise-Driven Conflict+Dramatic Irony+对白=行动+付费墙3-7-21 — 欧美爆款行业验证

---

## 文件索引（按需加载 ⭐）

> AI 按阶段按需加载，避免一次性读取全部内容。
> **速查**：先读 [`parts/quickstart.md`](parts/quickstart.md)（一页纸，告诉你每个阶段读哪些文件）

| 文件 | 行数 | 内容 | 何时读取 |
|------|------|------|---------|
| [`parts/quickstart.md`](parts/quickstart.md) | ~95 | 一页纸速查卡：每阶段读哪些文件 + 核心规则速记 | **每次新session首先读取** |
| [`parts/novel-adaptation.md`](parts/novel-adaptation.md) | ~135 | 阶段0：原著分析+支线取舍+压缩公式+中式→欧美转译+adaptation-map | **小说/Idea输入时必读**（阶段0） |
| [`parts/pitfalls.md`](parts/pitfalls.md) | ~148 | 执行纪律+硬规则+Beat Engine+Premise+DI+对白+炫技防控 | 项目开始前必读；批量任务前复习 |
| [`parts/workflow.md`](parts/workflow.md) | ~299 | 阶段0-7工作流+类型DNA+大纲结构+关系动力学+骨架生成+链式批量+文件依赖图 | 每阶段开始前 |
| [`parts/continuity.md`](parts/continuity.md) | ~320 | continuity格式+visual_continuity格式+伏笔状态机+付费墙+回退+增量方案 | 每集开始前/结束后；回退时 |
| [`parts/reviewers.md`](parts/reviewers.md) | ~20 | 审核系统索引+快速路由 | 选审核文件时 |
| [`parts/reviewers-scoring.md`](parts/reviewers-scoring.md) | ~354 | 欧美市场标准+类型权重表(唯一权重源)+三Aligner评分表+扣分规则+钩子等级+运镜分级 | 审核时；评分时 |
| [`parts/reviewers-workflow.md`](parts/reviewers-workflow.md) | ~115 | 审核工作流+集间衔接+输出格式 | 写审核报告时 |
| [`parts/reviewers-agents.md`](parts/reviewers-agents.md) | ~141 | 十视角Agent定义+观众旁白模式+激活策略 | 选观众旁白Agent时；关键集审核前 |
| [`parts/reviewers-patterns.md`](parts/reviewers-patterns.md) | ~77 | 创作法则+审核通过关键要素+常见陷阱+实战教训 | 审核不通过时；项目开始前 |
| [`parts/templates.md`](parts/templates.md) | ~138 | 剧本/分镜/Prompt模板（⚓格式契约）+时间预算+批量注意事项 | 写剧本/分镜/Prompts时 |
| [`parts/reference-system.md`](parts/reference-system.md) | ~173 | 三文件架构+Prompt视觉资产强制注入规则 | 阶段3视觉资产；写Prompts时 |
| [`parts/reference-impl.md`](parts/reference-impl.md) | ~138 | 角色/场景/道具Reference数据模型+帧级注入+时间匹配 | 实现细节需要时（按需） |
| [`parts/ai-tools.md`](parts/ai-tools.md) | ~32 | AI工具限制速查表（Seedance/Dreamina/Midjourney） | AI生图/生视频前；选工具时 |
| [`parts/revision-workflows.md`](parts/revision-workflows.md) | ~76 | 好莱坞剧本快速路径+导演修订更新+版本差异量化 | 输入为剧本时；收到修订版时 |
| [`parts/production.md`](parts/production.md) | ~144 | 批量验证清单+工作台生成(generate_index/build_html)+交付 | 批量生成后；生成工作台时 |
| [`parts/architecture.md`](parts/architecture.md) | ~73 | 核心问题+解决方案架构+竖屏视觉语法+目录结构 | 新项目启动时；架构决策时 |
| [`parts/decisions-log.md`](parts/decisions-log.md) | ~16 | 硬规则汇总（决策原理见 RATIONALE.md） | 调试/回溯决策原因时（按需） |

---

## 快速开始

> 💡 **新session第一步**：读 [`parts/quickstart.md`](parts/quickstart.md)（一页纸速查卡）

### 新项目启动（按顺序读取）
1. 读 `parts/quickstart.md` — 速查卡（**首先读**）
2. 输入是小说/Idea → 读 `parts/novel-adaptation.md` 跑**阶段0**（改编规划+adaptation-map，人工确认）
3. 读 `parts/pitfalls.md` — 硬规则+爆款原则（**必读**）
4. 读 `parts/workflow.md` — 工作流+类型DNA+大纲结构
5. 读 `parts/architecture.md` — 架构和目录结构
6. 按阶段推进，每阶段开始前读对应文件（见上表）

### 单集创作
1. 读 `parts/continuity.md` → 读 `parts/templates.md` → 写剧本 → 跑**Aligner审核**（关键集可选观众旁白）
2. 写分镜 → 跑审核 → 写Prompts → 读 `parts/reference-system.md` 注入视觉资产 → 跑审核
3. 更新 continuity（增量delta或批量）

### 批量任务（分镜/Prompts）
1. 读 `parts/pitfalls.md` 的批量执行纪律
2. 读 `parts/ai-tools.md` 确认工具限制
3. 输出执行计划 → 确认 → 执行 → 按 `parts/production.md` 验证文件完整性

### 全剧审查
1. 读 `parts/reviewers-scoring.md` + `parts/reviewers-workflow.md` + `parts/reviewers-patterns.md` 跑**全量审核**
2. 读 `parts/continuity.md` 的回退机制处理问题

---

## 工作流概览（阶段0-7）

```
阶段0: 小说改编（小说/Idea输入时）→ adaptation-map → 人工确认
         ↓
阶段1: 大纲（类型DNA+Premise自检）→ 阶段2: 人物（关系动力学）→ 阶段3: 视觉资产（全局，只跑一次）
         ↓
阶段4: 逐集剧本（串行，叙事连续性不可妥协）→ 人工确认定稿
         ↓
阶段5: 批量分镜（剧本定稿后，含Director's Treatment）→ 人工确认定稿
         ↓
阶段6: 批量Prompts（分镜定稿后）→ 人工确认定稿
         ↓
阶段7: 工作台生成
```

> 详细流程见 [`parts/workflow.md`](parts/workflow.md)

---

## 核心机制速查

| 机制 | 一句话 | 详见 |
|------|--------|------|
| **小说改编（阶段0）** | Premise自检一票否决+支线砍合留+三幕→Block映射+中式→欧美转译 | `parts/novel-adaptation.md` |
| **叙事层/制作层分离** | 剧本串行（叙事连续性），分镜/Prompts批量（无叙事依赖） | `parts/workflow.md` |
| **visual_continuity.md** | 每集分镜完成后记录视觉状态快照，下集分镜/Prompts生成前必读 | `parts/continuity.md` |
| **类型DNA** | 项目类型核心套路+冲突升级模式+钩子偏好+禁忌模式，大纲阶段提取 | `parts/workflow.md` |
| **AI炫技防控** | 爆款第一原则：每秒都有情绪；合规但无聊=不及格 | `parts/pitfalls.md` |
| **Beat Engine** | 每集按Hook→Friction→Spike→Button四段写 | `parts/pitfalls.md` |
| **Premise-Driven Conflict** | 冲突内建于设定（4种Premise） | `parts/pitfalls.md` |
| **Dramatic Irony** | EP2-3建立观众信息优势，维持差距到付费墙后 | `parts/pitfalls.md` |
| **对白=行动** | 每句推进冲突或压力下揭示角色，Subtext>Text | `parts/pitfalls.md` |
| **🟡运镜收紧** | 🟡≤2个/集+必须写理由，🟢可靠/🟡有限/🔴赌博三级 | `parts/reviewers-scoring.md` |
| **钩子简单性** | 能用单一的不用复合，能用低级的不用高级，复合是高潮集特权 | `parts/reviewers-scoring.md` |
| **continuity精简** | 生成时只读3项核心（Last Cliffhanger+到期伏笔+角色状态） | `parts/workflow.md` |
| **付费墙建模** | 3-7-21 Block分层+免费/付费集策略差异 | `parts/continuity.md` |
| **Reference体系** | [ref: C-XX/S-XX/P-XX] 三重引用，改一处全局生效 | `parts/reference-system.md` |
| **类型权重表** | 唯一权重真相源，6类型×20维度，每列合计100 | `parts/reviewers-scoring.md` |
| **导演覆盖** | Green/Yellow/Red三色判定+导演override机制 | `parts/reviewers-scoring.md` |
| **审核系统** | Aligner独立评分（≥80 PASS）+关键集可选观众旁白（Agent不打分） | `parts/reviewers-workflow.md` |
| **竖屏视觉语法** | 纵向视线引导+画外空间叙事+特写/近景≥50% | `parts/architecture.md` |
| **格式契约** | 剧本/分镜/Prompt的⚓锚点标题与解析器正则逐一对应，不可改 | `parts/templates.md` |

---

## 项目目录结构

```
project/
├── TASK.md                      # 任务进度跟踪
├── adaptation-map.md            # 原著对照表（小说改编项目）
├── outline.md                   # 故事大纲（含 project_type + paywall 配置）
├── continuity.md                # 剧集连续性追踪
├── characters/
│   └── characters.md            # 人物设定（base_prompt/outfits/expressions）
├── visual_assets/
│   └── manifest.md              # 视觉规则（服装指南、表情库、全局规则）
├── scene_prop_data.json         # 场景/道具 Reference Prompts
├── script/
│   └── EP-XX.md                 # 各集剧本
├── treatment/
│   └── EP-XX.md                 # 各集 Director's Treatment
├── storyboard/
│   └── EP-XX.md                 # 各集分镜
├── prompts/
│   └── EP-XX.md                 # 各集 AI Prompts
├── generate_index.py            # MD → JSON 解析脚本
├── build_html.py                # JSON → SPA 工作台
├── project_data.json            # 结构化数据
├── index.html                   # 离线工作台页面
└── script.progress.md           # 创作进度记录
```

---

## 版本演进

| 版本 | 核心变更 | 验证项目/驱动力 |
|------|---------|---------|
| v2.4 | 串行生成 + continuity.md | Lady Audley's Secret |
| v2.5 | 上下文管理 + 质量回退 + 文件依赖 | 系统性补全 |
| v3.0 | 三视角 + 三Aligner 审核系统 | — |
| v3.5 | 主模型直接写硬规则 + 叙事钩子10级 | Carmilla v2 |
| v3.6 | 叙事层/制作层分离 + 伏笔状态机 + AI瑕疵2026 | 架构评估 |
| v3.7 | 类型参数化 + 付费墙建模 + 导演覆盖 + Director's Treatment + 运镜分级 + 竖屏语法 | 好莱坞评估 |
| v3.8 | 模块化拆分（SKILL.md→入口索引+parts子文件） | 生产部署 |
| v3.9 | visual_continuity.md + 链式批量分镜 + 类型DNA + 集定位/大纲承诺/叙事预算 + 关系动力学 + 骨架串行生成 | 创作者反馈"分镜连续性有问题"+"生成慢" |
| v4.0 | AI炫技防控+核心冲击力(12分)+Lighting分层+🟡运镜收紧+钩子简单性+continuity精简运行时 | "合规但平庸"问题 |
| v4.1 | Beat Engine+Premise-Driven Conflict+Dramatic Irony+对白=行动+付费墙3-7-21 Block分层 | 欧美爆款行业验证（Filmustage/ReelShort/DramaBox） |
| v4.2 | 十视角MFLIX Agent评审团 + Agent激活策略 + 商业变现/亚文化维度 | 多Agent对抗模拟需求 |
| v5.0 | Agent结构化评分体系（100分制+维度锚点） | 主观分不可聚合不可校准 |
| v5.1 | 审核简化：Agent降级为观众旁白+Aligner独立评分+删除交叉验证/聚合公式 | Agent评分与Aligner高度冗余，Token降60% |
| v5.2 | 结构修复+欧美聚焦：修复拆分残缺文件+templates格式契约+阶段0小说改编+类型权重表统一评分+删多区域矩阵 | 全面审计：3处文件残缺+3套评分刻度矛盾+小说改编环节缺失 |
