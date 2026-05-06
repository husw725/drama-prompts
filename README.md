# Seedance 2.0 短剧 Prompt 优化器

将 draft prompt 优化为字节官方合规的 multimodal2video 提示词。

## 给 Agent 的使用方式

将此仓库的 `SKILL.md` 作为技能加载，Agent 即可自动执行 11 步优化流程。

### Hermes Agent

```bash
git clone https://github.com/husw725/drama-prompts.git
# 在 ~/.hermes/skills/ 下创建软链接或直接复制 SKILL.md
```

### OpenClaw / 其他 Agent

将 `prompt_template.txt` 的内容作为 system prompt 或 instruction 传入，Agent 即可按 11 步流程优化用户提供的 draft prompt。

## 文件结构

```
drama-prompts/
├── SKILL.md              # 完整优化技能（11步流程 + 示例）
├── prompt_template.txt   # 系统级 prompt（给任何 LLM 用）
└── README.md             # 本文件
```

## License

MIT
