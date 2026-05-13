# Drama Prompts & Reviewers

短剧 AI 制作工具集 — Prompt 优化器 + 多维度评审系统。

## 给 Agent 的使用方式

将对应目录的 `SKILL.md` 作为技能加载，Agent 即可自动执行。

### Hermes Agent

```bash
git clone https://github.com/husw725/drama-prompts.git
# 在 ~/.hermes/skills/ 下创建软链接或直接复制 SKILL.md
ln -s ~/.hermes/tasks/drama-prompts/prompt-optimizer/SKILL.md ~/.hermes/skills/drama-prompt-optimizer/SKILL.md
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

### 评审团 — 单人角色

三个独立评审角色，可根据目标市场自动切换文化视角。

| 角色 | 文件 | 视角 | 关注点 |
|------|------|------|--------|
| **急躁哥** | `reviewer-impatient-bro/` | 下沉市场用户 | 节奏、爽点、反转、冲动点击欲 |
| **逻辑控** | `reviewer-logic-master/` | 高线城市用户 | 类型定位、信息密度、差异化、平台适配 |
| **视听专家** | `reviewer-visual-expert/` | 资深制片人 | 视觉品牌、商业潜力、IP 延展、竞品对标 |

每个角色支持 **四个目标市场**：

| 市场 | 急躁哥 | 逻辑控 | 视听专家 |
|------|--------|--------|----------|
| **欧美** | 28 岁仓库工人/网约车 | 32 岁 SF/纽约 Tech PM | 45 岁 ReelShort 制片人 |
| **日韩** | 25 岁便利店店员/职员 | 30 岁内容编辑 | 40 岁日/韩 PD |
| **国内** | 28 岁外卖骑手 | 32 岁互联网 PM | 45 岁资深制片人 |
| **东南亚** | 26 岁工厂职员 | 29 岁数字营销 | 38 岁区域发行 |

### 评审团 — 综合评审

同时调用三个角色进行综合评审，输出排名和优化建议。

```
reviewer-combo/
├── SKILL.md              # 综合评审技能
└── prompt_template.txt   # 系统级 prompt
```

**触发条件：** 用户需要多维度评审短剧标题、剧本或视频。

## 文件结构

```
drama-prompts/
├── prompt-optimizer/           # Seedance 2.0 Prompt 优化器
│   ├── SKILL.md
│   └── prompt_template.txt
├── reviewer-impatient-bro/     # 急躁哥（下沉用户视角）
│   ├── SKILL.md
│   └── prompt_template.txt
├── reviewer-logic-master/      # 逻辑控（高线用户视角）
│   ├── SKILL.md
│   └── prompt_template.txt
├── reviewer-visual-expert/     # 视听专家（制片人视角）
│   ├── SKILL.md
│   └── prompt_template.txt
├── reviewer-combo/             # 综合评审（三角色合一）
│   ├── SKILL.md
│   └── prompt_template.txt
└── README.md                   # 本文件
```

## License

MIT
