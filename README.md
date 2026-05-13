# Drama Prompts & Reviewers

短剧 AI 制作工具集 — Prompt 优化器 + 多维度评审系统。

## 给 Agent 的使用方式

将对应目录的 `SKILL.md` 作为技能加载，Agent 即可自动执行。

### Hermes Agent

```bash
git clone https://github.com/husw725/drama-prompts.git
# 在 ~/.hermes/skills/ 下创建软链接或直接复制 SKILL.md
ln -s ~/.hermes/tasks/drama-prompts/prompt-optimizer/SKILL.md ~/.hermes/skills/drama-prompt-optimizer/SKILL.md
ln -s ~/.hermes/tasks/drama-prompts/reviewer-combo/SKILL.md ~/.hermes/skills/drama-reviewer-combo/SKILL.md
```

### OpenClaw / 其他 Agent

将对应目录的 `prompt_template.txt` 内容作为 system prompt 或 instruction 传入。

## 工具集

### Prompt 优化器

将 draft prompt 优化为字节官方合规的 Seedance 2.0 multimodal2video 提示词，11 步标准化流程。

```
prompt-optimizer/
├── SKILL.md              # 完整优化技能（11步流程 + 示例）
└── prompt_template.txt   # 系统级 prompt（给任何 LLM 用）
```

**触发条件：** 用户提供 draft prompt 需要优化为 Seedance 2.0 格式。

### 评审团 (三合一)

一个技能，三个角色，评所有东西。支持标题、剧本、分镜、集间衔接、人设、大纲、视频成片。

```
reviewer-combo/
├── SKILL.md              # 三合一评审技能（含行业真实数据 + 踩坑预警）
└── prompt_template.txt   # 系统级 prompt
```

**三个评审角色：**

| 角色 | 视角 | 核心关注点 |
|------|------|--------|
| **急躁哥** | 真实观众 | 3 秒钩子、10 秒爽点、情绪陪伴、冲动消费 |
| **逻辑控** | 产品思维 | 类型定位、信息密度、差异化、平台适配、文化差异 |
| **视听专家** | 制片人 | 商业数据、竞品对标、IP 延展、技术可行性、踩坑预警 |

**支持目标市场：**

| 市场 | 急躁哥 | 逻辑控 | 视听专家 |
|------|--------|--------|----------|
| **欧美** | 30 岁拉丁裔女，ReelShort 用户 | 32 岁 SF/NY Tech PM | 45 岁 ReelShort 制片人 |
| **日韩** | 26 岁 OL，DramaBox 用户 | 30 岁内容编辑 | 40 岁 PD |
| **国内** | 28 岁外卖骑手 | 32 岁互联网 PM | 45 岁资深制片人 |
| **东南亚** | 26 岁工厂女工 | 29 岁数字营销 | 38 岁区域发行 |

**行业数据：** 内置 2025-2026 海外短剧真实行业数据（36氪、App Store 评论、LinkedIn 行业文���），包括踩坑预警和节奏公式。

**触发条件：** 用户需要评审短剧的任何内容（标题/剧本/分镜/集间衔接/人设/大纲/视频）。

## 文件结构

```
drama-prompts/
├── prompt-optimizer/           # Seedance 2.0 Prompt 优化器
│   ├── SKILL.md
│   └── prompt_template.txt
├── reviewer-combo/             # 三合一评审团（评所有东西）
│   ├── SKILL.md
│   └── prompt_template.txt
└── README.md                   # 本文件
```

## License

MIT
