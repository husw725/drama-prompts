---
name: drama-team
description: 短剧编剧全流程系统 — 叙事层串行+制作层批量分离+类型参数化+付费墙建模+模块化拆分，含剧集连续性追踪、伏笔管理、视觉一致性管控与独立审核机制
version: 4.2
author: Hermes Agent + User
license: MIT
metadata:
  hermes:
    tags: [Short-Drama, Scriptwriting, Creative-AI, Visual-Consistency, Continuity, Foreshadowing, Sequential-Generation]
    related_skills: [hermes-agent, writing-plans, novel-to-short-drama-adaptation, short-drama-production-index]
---

# Hermes Agent 短剧编剧团队 v4.2

> 短剧编剧全流程系统：从小说/Idea到剧本、分镜、AI生图Prompt。
> **v4.2**: 十视角MFLIX Agent评审团(10个具象化人格) — 覆盖人口统计学+影视工业+跨文化合规+商业变现+亚文化考据，Agent激活策略按需调用
> **v4.1**: Beat Engine(Hook→Friction→Spike→Button)+Premise-Driven Conflict+Dramatic Irony+对白=行动+付费墙3-7-21 Block分层 — 欧美爆款行业验证

---

## 文件索引（按需加载 ⭐）

> SKILL.md 从单文件拆分为模块化结构。AI 按阶段按需加载，避免一次性读取全部内容。
> **速查**：先读 [`parts/quickstart.md`](parts/quickstart.md)（一页纸，告诉你每个阶段读哪些文件）

| 文件 | 行数 | 内容 | 何时读取 |
|------|------|------|---------|
| [`parts/quickstart.md`](parts/quickstart.md) | ~94 | 一页纸速查卡：每阶段读哪些文件 + 核心规则速记 | **每次新session首先读取** |
| [`parts/pitfalls.md`](parts/pitfalls.md) | ~148 | 执行纪律+硬规则+Beat Engine+Premise+DI+对白+炫技防控 | 项目开始前必读；批量任务前复习 |
| [`parts/workflow.md`](parts/workflow.md) | ~145 | 七阶段工作流+骨架生成+链式批量+上下文读取规则 | 每阶段开始前 |
| [`parts/continuity.md`](parts/continuity.md) | ~264 | continuity格式+visual_continuity格式+伏笔状态机+付费墙+回退+增量方案 | 每集开始前/结束后；回退时 |
| [`parts/reviewers.md`](parts/reviewers.md) | ~15 | 审核系统索引（指向下面文件） | 选审核文件时 |
| [`parts/reviewers-agents.md`](parts/reviewers-agents.md) | ~234 | 十视角Agent定义+人设+容忍度+国际化+激活策略+Industry Ground Truth | 选审核Agent时；审核前 |
| [`parts/reviewers-aligners.md`](parts/reviewers-aligners.md) | ~30 | 审核系统文件索引（评分表+工作流拆分后） | 确认读取哪些文件时 |
| [`parts/reviewers-scoring.md`](parts/reviewers-scoring.md) | ~450 | 三Aligner评分表+扣分规则+钩子等级表+运镜分级+评分校准（防膨胀） | 审核时；评分时 |
| [`parts/reviewers-workflow.md`](parts/reviewers-workflow.md) | ~140 | 综合工作流+集间衔接检查+输出格式+Reviewer-Combo关系 | 写审核报告时；全剧审查时 |
| [`parts/reviewers-patterns.md`](parts/reviewers-patterns.md) | ~212 | 创作法则+审核通过关键要素+常见陷阱+实战教训+示例 | 审核不通过时；项目开始前 |
| [`parts/reference-system.md`](parts/reference-system.md) | ~508 | 三文件架构+Reference体系+视觉资产+场景/道具/角色ref+Prompt注入规则 | 阶段3视觉资产；写Prompts时 |
| [`parts/reference-impl.md`](parts/reference-impl.md) | ~176 | 帧级Prompt批量注入+场景推断+时间匹配+批量脚本+迁移脚本 | 实现细节需要时（按需） |
| [`parts/templates.md`](parts/templates.md) | ~162 | 剧本模板+分镜模板+Prompt模板 | 写剧本/分镜/Prompts时 |
| [`parts/ai-tools.md`](parts/ai-tools.md) | ~120 | AI工具限制速查表+Carmilla验证案例 | AI生图/生视频前；选工具时 |
| [`parts/production.md`](parts/production.md) | ~80 | 工作台+generate_index+build_html+交付+注意事项+Drama Studio | 生成工作台时；交付时 |
| [`parts/architecture.md`](parts/architecture.md) | ~75 | 核心问题+解决方案架构+竖屏视觉语法+目录结构 | 新项目启动时；架构决策时 |
| [`parts/decisions-log.md`](parts/decisions-log.md) | ~173 | 历史决策+踩坑记录(v2.4→v4.2) | 调试/回溯决策原因时（按需） |

---

## 快速开始

> 💡 **新session第一步**：读 [`parts/quickstart.md`](parts/quickstart.md)（一页纸速查卡）

### 新项目启动（按顺序读取）
1. 读 `parts/quickstart.md` — 速查卡（**首先读**）
2. 读 `parts/pitfalls.md` — 硬规则+爆款原则（**必读**）
3. 读 `parts/workflow.md` — 七阶段工作流
4. 读 `parts/architecture.md` — 架构和目录结构
5. 按阶段推进，每阶段开始前读对应文件（见上表）

### 单集创作
1. 读 `parts/continuity.md` → 读 `parts/templates.md` → 写剧本 → 读 `parts/reviewers-agents.md` + `parts/reviewers-aligners.md` 跑**轻量审核**
2. 写分镜 → 跑审核 → 写Prompts → 读 `parts/reference-system.md` 注入视觉资产 → 跑审核
3. 更新 continuity（增量delta或批量）

### 批量任务（分镜/Prompts）
1. 读 `parts/pitfalls.md` 的批量执行纪律
2. 读 `parts/ai-tools.md` 确认工具限制
3. 输出执行计划 → 确认 → 执行

### 全剧审查
1. 读 `parts/reviewers-agents.md` + `parts/reviewers-aligners.md` + `parts/reviewers-patterns.md` 跑**全量审核**（10 Agent）
2. 读 `parts/continuity.md` 的回退机制处理问题

---

## 七阶段工作流概览

```
阶段1: 大纲 → 阶段2: 人物 → 阶段3: 视觉资产（全局，只跑一次）
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
| **叙事层/制作层分离** | 剧本串行（叙事连续性），分镜/Prompts批量（无叙事依赖） | `parts/workflow.md` |
| **visual_continuity.md** | 每集分镜完成后记录视觉状态快照，下集分镜/Prompts生成前必读 | `parts/continuity.md` |
| **类型DNA** | 项目类型核心套路+冲突升级模式+钩子偏好+禁忌模式，大纲阶段提取 | `parts/reference-system.md` |
| **集定位** | 每集战略定位（铺垫/转折/高潮/过渡/收束），大纲阶段规划 | `parts/reference-system.md` |
| **关系动力学** | 关系转折点+权力动态+张力曲线，人物阶段建模 | `parts/reference-system.md` |
| **AI炫技防控** | 爆款第一原则：每秒都有情绪；合规但无聊=不及格 | `parts/pitfalls.md` |
| **核心冲击力** | Script/Storyboard-Aligner最高权重维度(12分)：有让人"哇"的瞬间吗？ | `parts/reviewers.md` |
| **Lighting分层精度** | 按集类型分层：氛围一层/标准两层/高潮三层，不过度工程化 | `parts/reviewers.md` |
| **🟡运镜收紧** | 🟡≤2个/集+必须写理由，无理由=炫技扣分 | `parts/reviewers.md` |
| **钩子简单性** | 能用单一的不用复合，能用低级的不用高级，复合是高潮集特权 | `parts/reviewers.md` |
| **continuity精简** | 生成时只读3项核心（Last Cliffhanger+到期伏笔+角色状态） | `parts/workflow.md` |
| **continuity.md** | 伏笔状态机+角色状态+冲突模式+Last Cliffhanger+叙事预算 | `parts/continuity.md` |
| **付费墙建模** | 首集免费+付费墙位置+免费/付费集策略差异+沉没成本曲线 | `parts/continuity.md` |
| **Reference体系** | [ref: C-XX/S-XX/P-XX] 三重引用，改一处全局生效 | `parts/reference-system.md` |
| **类型参数化** | Aligner权重按项目类型动态调整（甜宠/复仇/悬疑/玛丽苏/强制爱） | `parts/reviewers.md` |
| **导演覆盖** | Green/Yellow/Red三色判定+导演override机制 | `parts/reviewers.md` |
| **十视角+三Aligner** | 按剧类型动态选3人逐集审核(08付费墙固定)+全剧完成跑全量10人；Agent01-10 × Script/Storyboard/Prompt-Aligner | `parts/reviewers-scoring.md` + `parts/reviewers-workflow.md` |
| **运镜可执行性分级** | 🟢可靠/🟡有限/🔴赌博三级，AI遵循率实测 | `parts/reviewers.md` |
| **竖屏视觉语法** | 纵向视线引导+画外空间叙事+文字叠加叙事+竖屏亲密空间 | `parts/architecture.md` |
| **Beat Engine** | 每集按Hook→Friction→Spike→Button四段写，先写timestamp skeleton再写对白 | `parts/pitfalls.md` |
| **Premise-Driven Conflict** | 冲突内建于设定（Enemies-to-lovers/Forbidden proximity/Power imbalance/Arranged circumstance） | `parts/pitfalls.md` |
| **Dramatic Irony** | EP2-3建立观众信息优势，维持差距到付费墙后，比cliffhanger更强留存 | `parts/pitfalls.md` |
| **对白=行动** | 每句对白推进冲突或压力下揭示角色，Subtext>Text，角色不解释感受 | `parts/pitfalls.md` |
| **竖屏特写优先** | vertical drama lives in faces, not locations。特写/近景≥50% | `parts/reviewers.md` |
| **声音/BGM** | 声音是海外用户付费第一驱动因素，BGM随Beat Engine节奏变化 | `parts/reviewers.md` |

---

## 项目目录结构

```
project/
├── TASK.md                      # 任务进度跟踪
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

| 版本 | 核心变更 | 验证项目 |
|------|---------|---------|
| v2.4 | 串行生成 + continuity.md | Lady Audley's Secret |
| v2.5 | 上下文管理 + 质量回退 + 文件依赖 | 系统性补全 |
| v3.0 | 三视角 + 三Aligner 审核系统 | — |
| v4.2 | 十视角MFLIX Agent评审团(10个具象化人格) + Agent激活策略 + 商业变现维度(付费墙精算师/UA总监) + 亚文化考据维度 | 欧美出海短剧多Agent对抗模拟需求驱动 |
| v3.5 | 主模型直接写硬规则 + 叙事钩子10级 | Carmilla v2 |
| v3.6 | 叙事层/制作层分离 + 伏笔状态机 + AI瑕疵2026 + 文化雷区具体化 | 架构评估 |
| v3.7 | 类型参数化 + 付费墙建模 + 导演覆盖 + 编剧视角 + Director's Treatment + 运镜分级 + 竖屏语法 | 好莱坞评估 |
| v3.8 | 模块化拆分（SKILL.md→入口索引+9个parts子文件） | 生产部署 |
| v3.9 | visual_continuity.md + 链式批量分镜 + 跨集视觉承接(10分) + 类型DNA + 集定位/大纲承诺/叙事预算 + 关系动力学 + 骨架串行生成 + 大纲承诺兑现(5分) + continuity每3集批量更新 | 创作者反馈"分镜连续性有问题"+"生成慢"驱动 |
| v4.0 | AI炫技防控+爆款核心原则+核心冲击力(12分)+Lighting分层精度+🟡运镜收紧(≤2+理由)+钩子简单性(防通胀)+continuity精简运行时(3项核心) | "合规但平庸"问题驱动——专业度和短剧节奏的张力 |
| v4.1 | Beat Engine(Hook→Friction→Spike→Button四段结构)+Premise-Driven Conflict(4种爆款Premise)+Dramatic Irony(观众知道角色不知道)+对白=行动(Subtext>Text)+付费墙3-7-21 Block分层 | 欧美爆款行业验证——Filmustage/ReelShort/DramaBox收敛结论 |
