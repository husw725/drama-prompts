---
name: drama-team
description: 短剧编剧全流程系统 — 叙事层串行+制作层批量分离+类型参数化+付费墙建模+模块化拆分，含剧集连续性追踪、伏笔管理、视觉一致性管控与独立审核机制
version: 3.8
author: Hermes Agent + User
license: MIT
metadata:
  hermes:
    tags: [Short-Drama, Scriptwriting, Creative-AI, Visual-Consistency, Continuity, Foreshadowing, Sequential-Generation]
    related_skills: [hermes-agent, writing-plans, novel-to-short-drama-adaptation, short-drama-production-index]
---

# Hermes Agent 短剧编剧团队 v3.8

> 短剧编剧全流程系统：从小说/Idea到剧本、分镜、AI生图Prompt。
> **v3.0**: 审核员已内置（三视角定性 + 三Aligner定量），本技能是唯一来源。

### 🔥 批量任务执行纪律（v3.1 ⭐ 2026-05-15 Carmilla v2 教训）

> **用户原话**："升级前你先计划一下会怎么用技能进行生成分镜等信息"
> **教训**：不要接到"生成分镜"就立刻开进程跑。必须先停下来规划：用什么方式（主模型逐集/本地API/子代理）、预计耗时、质量预期，然后告诉用户确认后再执行。
> **强制规则**：涉及 10+ 集的批量生成分镜/Prompts 时，先输出执行计划（方式+预估时间+分批策略），等用户确认后再动手。

### 🔥 阶段 5-6 批量执行纪律（v3.8 ⭐ 新增）

> 剧本定稿后，分镜和Prompts可批量生成，但仍需遵守执行纪律。

**阶段5（批量分镜）**：前置检查(TASK.md确认定稿) → 2-3集合并写入 → 批量审核 → FAIL集统一修改(patch模式)
**阶段6（批量Prompts）**：同上，额外检查风格词一致性（每集第一个Prompt风格词不应漂移）
**执行计划模板**：总集数/分批策略/预估耗时/审核策略 → 确认后执行

### 🔥 数据提取策略（v3.1 ⭐ 2026-05-15 Carmilla v2 教训）

> **用户原话**："提取数据或者什么转化过程出现问题，让大模型帮忙提取转化，准确性更高"
> **教训**：当正则/脚本解析好莱坞剧本出问题（角色名混入集标题、对白混入动作描述），不要反复调正则。直接让大模型（主模型）逐集读取剧本，输出结构化 JSON——它理解上下文，能区分"角色名"和"集标题"、"对白"和"动作描述"。
> **适用场景**：剧本 → 结构化 JSON 提取（角色、对白、场景）、复杂格式转换、跨版本 diff 分析。
> **硬编码正则的坑**（v3.1 实测 3 轮才调通）：
> 1. 角色名正则 `^[A-Z][A-Z0-9\s\.\'\-()]*$` 会捕获集标题（THE CURSE REVEALED、AFTERMATH）
> 2. 对白收集需要分离角色名后的"对白行"vs"动作描述行"（动作通常以人名+动词开头如 "Irina slams"）
> 3. 场景头正则 `INT.|EXT.` 需要 `$` 锚点否则匹配到中间行
> 4. `normalize_char` 需要处理 `(CONT'D)` 和 `(V.O.)` 后缀
> 5. 对白中的剧本术语（INSERT、SUPERIMPOSE、MATCH CUT TO）需要后处理清理

### 🔥 剧本提取：质量优先（v3.3 ⭐ 2026-05-15 Carmilla v2 教训）

> **用户原话**："就你自己一集一集分析提取，我们要高质量"
> **教训**：正则提取对白持续失败（动作描述混入对白、V.O.混淆、CONT'D归并失败、多行拼接断裂）。主模型逐集精读，对白/VO/Cliffhanger 准确无误，每集 30 秒，33 集一次完成。
> **强制规则**：剧本对白、V.O.、Cliffhanger 提取 **只用主模型逐集精读**，不调正则脚本，不让子代理跑。

> **实测数据**：本地 qwen27b-awq（port 8000）串行 16 批（每批 2 集）LLM 分镜生成，300 秒超时后才完成 0 集。
> **根因**：每集需要 1 次 HTTP 请求 + 模型推理 30-60 秒 + 上下文传输。32 集 × 30 秒 = 16 分钟，超时。
> **强制规则**：32 集以上的批量分镜/Prompts 生成，**不要用本地模型 API 循环调用**。改用主模型逐集直接写（write_file 模式），主模型已加载上下文，无需 HTTP 开销。
> **例外**：单集精修（1-2 集）可以用子代理或本地 API，但超过 5 集必须切主模型。

### 子 Agent 委托策略（v2.6 ⭐ 2026-05-12 Lady Audley's Secret 验证）

> **核心缺陷修复**：一次性委托 24+ 集给子 Agent 导致 token 耗尽/中断/跳过审核。
> **v3.5 升级（2026-05-15 Carmilla 验证）**：用户明确纠正"不要开子任务去做，你就主任务做完它"——子代理用于纯文本写作（剧本/分镜/Prompts/Review）必断。

### 🔥 硬规则：剧本/分镜/Prompts/Review 生成策略（v3.8 ⭐ 叙事层与制作层分离）

> **v3.8 关键变更**：剧本必须逐集串行（叙事连续性不可妥协），但分镜和 Prompts 在剧本定稿后可批量生成。实际工作流中剧本通常需要反复修改调整，不应锁死在一个循环里。

| 任务类型 | 策略 | 理由 |
|----------|------|------|
| **剧本生成** | 主模型逐集 write_file（串行） | 上下文连贯，叙事连续性是底线 |
| **分镜生成** | 主模型批量 write_file（剧本定稿后） | 剧本已定，分镜间无叙事依赖，2-3集合并最佳 |
| **Prompts 生成** | 主模型批量 write_file（分镜定稿后） | 分镜已定，可批量；纯文本写入 |
| **Review 审核** | 主模型直接做 | 多集审查子代理必超时 |
| **单集精修补遗** | 主模型 write_file | 1 集也要主模型做，子代理不值得启动开销 |
| **读者评审** | 主模型内联审查 | 多集采样+内联报告 |



### v3.6 说明（2026-05-16）

> **叙事层与制作层分离**：v3.6 将阶段4-6拆为叙事层（逐集剧本串行）和制作层（批量分镜+批量Prompts），实测提速37%。
> - **叙事层**（阶段4）：逐集串行写剧本，每集必须读 continuity.md + 上一集 Cliffhanger → Aligner 审核 → 更新连续性
> - **制作层**（阶段5-6）：剧本全部 PASS 后，批量写分镜（2-3集/次），批量写 Prompts（逐集 write_file）
> - **3个✅人工确认节点**：大纲确认 → 人物确认 → 视觉资产确认 → 叙事层全部剧本确认 → 制作层开始

### 子代理唯一适用场景
- **代码脚本编写**（generate_index.py, build_html.py, fix_prompts.py）
- **视频生成任务**（Dreamina/Seedance API 调用，可异步+notify）
- **独立推理任务**（单集质量分析、竞品对标）

### 🔥 批量 Prompts/Review 生成模式（v3.5 ⭐ 2026-05-15 Carmilla EP-10~30 验证）

**Prompts 批量写入**：主模型逐集 write_file，每集 1 次调用。EP-24~30（7集 Prompts）7 次 write_file 完成，每次 5-7K chars。
**Review 批量写入**：主模型用 `execute_code` 构造 Python 字典（所有集 Review 内容），一次性 write_file 全部。EP-10/13~30（19集 Review）单次 execute_code 完成，总耗时 12 秒 vs 逐集 write_file 预计 20+ 秒。

```python
# Review 批量模式（推荐 ⭐ — 19集 12秒完成）
from hermes_tools import write_file

reviews = {
    '10': '# EP-10 Review: ...\n## Episode Review — Score: 93/100 ✅\n...',
    '13': '# EP-13 Review: ...\n## Episode Review — Score: 92/100 ✅\n...',
    # ... 所有集
}

for ep, content in reviews.items():
    write_file(f"review/EP-{ep}.md", content)

# Prompts 批量模式 — 逐集 write_file（每集需要独立上下文推理）
# for ep in ['24','25','26','27','28','29','30']:
#     read_file(f"storyboard/EP-{ep}.md")  # 先读分镜
#     write_file(f"prompts/EP-{ep}.md", generated_content)  # 再写 Prompt
```

**选择依据**：
| 任务 | 推荐模式 | 理由 |
|------|---------|------|
| Prompts | 逐集 write_file | 需要逐集读分镜+独立推理，不适合字典构造 |
| Review | execute_code 字典批量 | 可先全部读取分镜到内存，再批量生成+写入 |

### 失败模式（Lady Audley's Secret 实测）

| 方案 | 结果 | 根因 |
|------|------|------|
| 一次委托 EP-06→30（24集） | EP-06 Prompts 就断 | 输入 152K tokens，输出预算只剩 ~6K，跑不完 |
| 一次委托 EP-07+08（2集） | 读了文件就断 | 上下文文件过多（6个文件 30K+），输出预算不够 |
| **主 Agent 自己逐集跑（推荐）** | ✅ EP-07 完整通过 | 主 Agent 已在上下文中，无需额外加载文件，输出空间充足 |

### 推荐策略

| 场景 | 策略 | 理由 |
|------|------|------|
| **单集精修**（推荐 ⭐） | 主 Agent 自己执行 | 上下文已加载，输出空间大，审核可控 |
| **补遗/补文件** | 子 Agent 委托（1集） | 如补 EP-06 Prompts（其他集已存在） |
| **读者评审** | 子 Agent 委托（1次/3-5集） | 独立视角，不影响主流程 |
| **批量初稿** | 子 Agent 可试（最多3集） | 接受质量较低，后续逐集精修 |

### 子 Agent 委托时上下文压缩

如果必须用子 Agent，压缩上下文：
```
# 坏（30K+ tokens）
- 读 outline.md 全文
- 读 characters.md 全文
- 读 manifest.md 全文
- 读 scene_prop_data.json 全文
- 读 script/EP-06.md 全文
- 读 storyboard/EP-06.md 全文
- 读 continuity.md 全文

# 好（~5K tokens）
- 读 continuity.md（核心，含进度+伏笔+角色状态）
- 读 outline.md 中对应集梗概（只读相关段落）
- 读 characters.md 中本集出场角色的 base_prompt（只读相关角色）
- 读 manifest.md 中的色调规则（当前集所在幕）
```

### 硬性规则（v2.6 新增）

1. **审核不可跳过** — 每集三件套完成后必须跑 Aligner 审核，≥80分才过。子 Agent 跳过审核 = 重来。质量基线稳定后（3+集通过）可接受1轮快速审核。
2. **每集输出预算** — 一集完整三件套 + 审核 ≈ 15-17K tokens 输出（含 continuity 更新）。子 Agent 总输出预算通常 20-30K，最多跑 1-2 集。
3. **主 Agent 逐集是默认方案** — 除非有明确理由（并行读者评审、补遗），否则主 Agent 自己跑质量更高。实测 20+集无问题。
4. **中断恢复** — 子 Agent 中断后，用 `ls script/ storyboard/ prompts/` + `stat` 时间戳确认实际完成到哪，不要假设。
5. **连续性文件批量更新** — continuity.md 不必每集更新，每 3-5 集批量更新一次即可。EP-20+ 后只保留活跃伏笔（已回收的压缩为一句话），避免上下文膨胀。
6. **Review 可内联** — 审核结果可内联到 Script 文件末尾（不单独写 review 文件），节省 1 个 write_file 调用。

## 核心问题

传统 AI 短剧创作存在五大问题：
1. **节奏/爽点/付费转化** — 缺乏对短剧特有规律的理解
2. **跨集叙事断裂** — 多子Agent并行生成时，EP-03不知道EP-02的悬念、角色状态、伏笔，导致剧情不连贯