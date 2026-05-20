# Drama Prompts & Reviewers

短剧 AI 制作工具集 — Prompt 优化器 + 剧本格式化 + 制作工作台。

## 给 Agent 的使用方式

将对应目录的 `SKILL.md` 作为技能加载，Agent 即可自动执行。

### OpenClaw / 其他 Agent

将对应目录的 `SKILL.md` 作为技能加载，或将 `prompt_template.txt` 内容作为 system prompt 传入。

## 工具集

### Seedance Prompt Optimizer

将 draft prompt 优化为字节官方合规的 Seedance 2.0 multimodal2video 提示词，11 步标准化流程。

```
seedance-prompt-optimizer/
├── SKILL.md              # 完整优化技能（11步流程 + 示例）
└── prompt_template.txt   # 系统级 prompt（给任何 LLM 用）
```

**触发条件：** 用户提供 draft prompt 需要优化为 Seedance 2.0 格式。

### Screenplay Hollywood Format

将短剧分镜脚本转换为好莱坞标准格式剧本（DOCX）— 移除镜头指示、添加角色介绍、修复场景标题、自然化对白、python-docx 排版输出。

```
screenplay-hollywood-format/
├── SKILL.md              # 格式化技能（含转换规则 + 示例）
└── references/
    └── llm-translation-workflow.md
```

**触发条件：** 用户需要将分镜脚本转为好莱坞标准剧本格式。

### Short Drama Production Index

为短剧项目生成 JSON 数据和交互式 HTML 工作台（固定模板 + JSON 注入单文件架构）。

```
short-drama-production-index/
├── SKILL.md              # 工作台技能（含生成流程 + 配置说明）
├── build_html.py         # HTML 构建脚本
└── template.html         # 工作台 HTML 模板
```

**触发条件：** 用户需要为短剧项目生成交互式制作工作台 / 项目索引。

## 文件结构

```
drama-prompts/
├── seedance-prompt-optimizer/     # Seedance Prompt 优化器
│   ├── SKILL.md
│   └── prompt_template.txt
├── screenplay-hollywood-format/   # 剧本好莱坞格式化
│   ├── SKILL.md
│   └── references/
├── short-drama-production-index/  # 短剧制作工作台
│   ├── SKILL.md
│   ├── build_html.py
│   └── template.html
└── README.md                      # 本文件
```

## License

MIT
