| 角色 (H2 + attrs) | `## (.+?)\n(.+?)(?=## |\Z)` |

### 打包交付

```bash
tar --exclude='__pycache__' -czf /path/to/desktop/project-name.tar.gz -C /path/to project-name/
```

### 常见陷阱

**解析器陷阱（⭐ 必须遵守）**：
1. **正则截断** — 所有 `parse_script` / `parse_storyboard` 正则必须用 `(?=\n## [^#]|\Z)` 而非 `(?=##|$)`，否则 `###` 会被误匹配截断
2. **列数动态检测** — Scene Breakdown/Key Dialogue/分镜表列数必须用 `>= 2`（不是 `==` 或 `>= 5`），动态映射 headers
3. **Cliffhanger 后缀** — 正则 `## Cliffhanger[^\n]*\n` 兼容 `/ 终局` 等后缀
4. **Voiceovers 初始化** — result 字典必须包含 `'voiceovers': []`，VO-only 集不会 KeyError
5. **manifest.md 分区段解析** — 按 `##` 大标题切分区段独立解析，避免全局扫描导致的跨区污染

**工作台 v4.0 陷阱**：
- **JSON 格式必须含 `project` 和 `total_episodes`** — 标题从 `data['project']` 读取（不是 `manifest.title`）
- **不要硬编码列数** — 分镜表头动态解析（8列/12列变化频繁）
- **修改 JSON 后必须重新运行 `build_html.py`** — 工作台渲染的是嵌入的 JSON 快照
- **`generate_index.py` 提取剧本对白用主模型** — 正则解析容易把动作描述混入对白（v3.1 实测 3 轮才调通）

## 注意事项

### 1. AI 审核的局限性
- Aligner 本身是 AI，可能僵化执行规则
- 可能对"格式正确但创意平庸"的剧本给 PASS
- **必须人工最终把关**

### 2. 昂贵的审核循环
- FAIL → 修改 → 再 FAIL 消耗大量 Token
- 同一问题反复 FAIL 超过 2-3 次时立即人工介入

### 3. 记忆污染风险
- 手动修改文档会导致 Recorder 记录过时
- **修改文档后需要手动更新 script.progress.md**

### 4. 风格漂移
- 长时间对话后可能忘记上下文
- 需要定期在 context 中重申创作法则

### 5. 视觉资产管理（三文件架构）
- **三文件各司其职** — `characters.md`（角色身份）、`scene_prop_data.json`（场景/道具 Reference）、`manifest.md`（视觉规则）
- **manifest.md 只保留不可替代内容**：服装场景映射、表情关键词、色调/光影/构图规则
- **角色外观改 → 只改 `characters.md`**
- **场景/道具改 → 只改 `scene_prop_data.json`**
- **服装/情绪/色调改 → 只改 `manifest.md`**
- 新角色首次出场时，同时更新三文件（characters.md 身份 + manifest.md 服装/表情 + scene_prop_data.json 如需要新场景）

---

## Drama Studio 集成参考

> Drama Studio 是 drama-team 的 Web UI 扩展（11 阶段流水线），项目位于 `~/.hermes/tasks/drama-studio/`。
> 启动：后端 `server/index.ts`（端口 3000），TapNow 前端端口 5176。
> AI 模型默认 qwen27b-awq（本地）。详见 `DESIGN.md`。

**核心架构**：
- 编剧层 7 阶段（输入处理 + 标准 6 阶段）→ 制作层 4 阶段（生图/生视频/配音/合成）→ 交付
- MCP 集成（`services/mcp.ts`，并发 3），全局资源一次生成全剧复用
- TapNow 为 state-based 无 React Router，四级下钻有返回导航，新建必须输入入口
- 工作流：全局资源(角色/场景/道具图)生一次 → 每集独立：剧本→分镜→Prompt→优化→生图→生视频→单集合成
- 端口：后端 3000，经典前端 5174，Luma 5175，TapNow 5176

## GitHub 同步

- 技能库仓库：`https://github.com/husw725/drama-prompts/`
- 同步：`git add -A && git commit -m "update" && git push`
- 读者人设更新参考：本技能 `## 审核员系统` 章节的国际化人设切换表

## 相关技能

- `hermes-agent` — Hermes Agent 配置与调试
- `writing-plans` — 实施规划与任务分解
- `novel-to-short-drama-adaptation` — 小说改编短剧流程
- `short-drama-production-index` — 短剧工作台 JSON/HTML 生成
- `drama-studio` — 11 阶段 Web UI 短剧制作系统
- `seedance-prompt-optimizer` — Seedance 2.0 Prompt 优化器
- `video-dubbing-indextts2` — IndexTTS 2.0 翻译配音工作流
