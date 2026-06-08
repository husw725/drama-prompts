# 生产与交付

---

## 工作台生成

```bash
# 1. 解析 MD → JSON
python generate_index.py

# 2. 生成 SPA 工作台
python build_html.py

# 3. 打开
open index.html
```

## 打包交付

```bash
tar --exclude='__pycache__' -czf /path/to/desktop/project-name.tar.gz -C /path/to project-name/
```

---

## 常见陷阱

**解析器**：
- 正则截断：用 `(?=\n## [^#]|\Z)` 而非 `(?=##|$)`
- 列数动态检测：用 `>= 2` 不是 `==`
- manifest.md 按 `##` 大标题切分区段独立解析

**工作台**：
- JSON 必须含 `project` 和 `total_episodes`
- 不要硬编码列数，分镜表头动态解析
- 修改 JSON 后必须重新运行 `build_html.py`
- `generate_index.py` 提取对白用主模型

---

## 注意事项

1. **AI 审核局限** — Aligner 可能对"格式正确但创意平庸"给 PASS，必须人工最终把关
2. **昂贵审核循环** — 同一问题反复 FAIL 超过2-3次时立即人工介入
3. **记忆污染** — 手动修改文档后需更新 `script.progress.md`
4. **风格漂移** — 长对话后定期重申创作法则

---

## 三文件架构（视觉资产）

- `characters.md`（角色身份）— 角色外观改只改这里
- `scene_prop_data.json`（场景/道具 Reference）— 场景/道具改只改这里
- `manifest.md`（视觉规则）— 服装/情绪/色调改只改这里

---

## GitHub 同步

- 仓库：`https://github.com/husw725/drama-prompts/`
- 同步：`git add -A && git commit -m "update" && git push`
