# 生产与交付

> 阶段7（工作台生成）与交付时读取。

---

## 大规模批量生成检查清单

> 一次性生成 10+ 集后、进入工作台阶段前必须执行，否则会出现文件缺失（如 EP-20 prompts 漏写）。

**生成后必做验证：**

```python
import os
base = "/path/to/project"
for i in range(1, TOTAL_EPS + 1):
    ep = f"EP-{i:02d}"
    for subdir in ["script", "storyboard", "prompts"]:
        fp = f"{base}/{subdir}/{ep}.md"
        if not os.path.exists(fp):
            print(f"MISSING: {subdir}/{ep}.md")
        elif os.path.getsize(fp) < 500:
            print(f"SUSPECT: {subdir}/{ep}.md（<500 bytes，可能为空）")
```

**缺失处理流程：**
1. 运行验证脚本（见上）
2. 发现缺失 → 立即读取对应 script/EP-XX.md
3. 主模型直接手写补齐 storyboard 和 prompts（不派子代理，速度更快）
4. 重新验证确认全部存在 → 才能进入工作台阶段

**TASK.md 更新（每次批量生成后必做）：**
- ✅ 标记完成的集 + 更新项目状态（如 "Phase 2 全部完成"）+ 添加更新日志条目
- 不更新会导致下次续做时无法判断真实进度

---

## 工作台生成（三步）

```bash
# 1. 解析 MD → JSON
python3 generate_index.py    # → project_data.json

# 2. 生成 SPA 工作台
python3 build_html.py        # → index.html

# 3. 打开
open index.html
```

### Step 1: `generate_index.py` — MD → JSON 解析器

> 模板文件在同仓库 `short-drama-production-index/` 目录（或技能 `short-drama-production-index`），复制到项目根目录运行。

**核心结构**（关键陷阱已内联）：

```python
#!/usr/bin/env python3
import json, os, re

BASE = os.path.dirname(os.path.abspath(__file__))

def read(path):
    with open(os.path.join(BASE, path), 'r', encoding='utf-8') as f:
        return f.read()

# 解析函数：parse_script, parse_storyboard, parse_prompts, parse_characters, parse_manifest
# 关键修复点：
# 1. 正则用 (?=\n## [^#]|\Z) 而非 (?=##|$)，否则 ### 会被误匹配
# 2. Scene Breakdown 列数 >= 2（不是5），Key Dialogue >= 2（不是 ==2）
# 3. Cliffhanger 兼容 "## Cliffhanger / 终局" 后缀格式
# 4. Voiceovers 初始化空列表，VO-only 集不会 KeyError

def main():
    data = {'project': 'ProjectName', 'total_episodes': N, 'episodes': [],
            'characters': [], 'manifest': {}, 'scenes': [], 'props': []}
    # 加载 manifest.md、scene_prop_data.json
    # 遍历 script/ 目录，按 EP 解析三件套 → data['episodes']
    with open('project_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
```

**正则解析模式速查表**（与 `parts/templates.md` 的 ⚓ 锚点逐一对应）：

| 解析目标 | 正则锚点 |
|----------|---------|
| 场景分解 | `## Scene Breakdown\n(.+?)(?=\n## [^#]|\Z)` |
| Key Dialogue | `## Key Dialogue\n(.+?)(?=\n## [^#]|\Z)` |
| 分镜表 (Key Frames) | `## Key Frames\n(.+?)(?=\n## [^#]|\Z)` |
| Image Prompts | `### Frame (\d+): (.+?)\n\*\*Prompt:\*\*(.*?)` |
| Video Prompts | `### Shot (\d+): (.+?)\n\*\*Prompt:\*\*(.*?)` |

> ⭐ **数据提取原则**：剧本对白/VO/Cliffhanger 等复杂结构化数据 → **主模型逐集精读提取**，不用正则。规则格式（分镜 Markdown 表格、manifest 表格）→ 正则脚本。

### Step 2-3: 构建工作台

| 文件 | 角色 | 大小 |
|------|------|------|
| `template.html` | 固定 SPA 应用模板，9 Tab + 附件预览 + 全量可编辑 + 导入/导出 | ~32KB |
| `build_html.py` | 构建脚本：读取 JSON → 分块（~30KB/块）→ 注入 → 输出 index.html | ~2KB |
| `project_data.json` | 数据源（`generate_index.py` 生成） | 项目相关 |
| `index.html` | 最终产物，单文件自包含，双击即用 | ~635KB |

**9 个 Tab**：📊 仪表盘 / 🎬 分镜 / 📝 剧本 / 👤 角色 / 🏰 场景 / 🧰 道具 / 🖼️ 图片Prompt / 🎞️ 视频Prompt / 📁 素材库

**核心特性**：全量可编辑（contenteditable + localStorage）、保存/加载 JSON、数据分块注入、移动端适配。

---

## 常见陷阱

**解析器**：
- 正则截断：用 `(?=\n## [^#]|\Z)` 而非 `(?=##|$)`
- 列数动态检测：用 `>= 2` 不是 `==`；分镜表头动态解析，不硬编码列数
- manifest.md 按 `##` 大标题切分区段独立解析

**工作台**：
- JSON 必须含 `project` 和 `total_episodes`
- 修改 JSON 后必须重新运行 `build_html.py`

---

## 打包交付

```bash
tar --exclude='__pycache__' -czf /path/to/desktop/project-name.tar.gz -C /path/to project-name/
```

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
