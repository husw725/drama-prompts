
**批量分镜最佳实践（v3.4 ⭐ 2026-05-15 Carmilla v2 验证）**：
- **2-3 集合并生成**：用户确认"后面可以尝试2集或3集合一起去生成"。主模型单次输出 20-30K chars 不中断，是最佳批量粒度。
- **写前必做**：先读剧本 → 分析集类型(恐怖/对峙/亲密/揭示/调查) → 确定节奏/运镜/灯光策略 → 再生成。
- **写后必做**：每集内联 Storyboard-Aligner 自审（6维度评分），≥80 分 PASS。
- **详细实战模式**：见 `references/storyboard-bulk-generation-patterns.md`（集类型分类、运镜策略、节奏模式、常见扣分项）

**v4.1 模板增强（Beat Engine + Premise + DI + 对白=行动）**：
- **剧本模板**：每集开头必须写 Beat Engine Timestamp Skeleton（Hook/Friction/Spike/Button 四段时间+锚点）
- **Premise 自检**：大纲阶段必须执行，确认冲突内建于设定而非场景制造
- **Dramatic Irony 状态**：每集剧本标注观众信息优势（观众知道/角色不知道/差距维持）
- **对白=行动**：每集剧本标注解释性对白数量（目标0），冲突前2行进入
- **付费墙 Block**：每集标注当前 Block 策略（免费/付费/DI维持/揭秘）
- **竖屏特写优先**：分镜/Prompts中特写/近景≥50%，核心情绪在面部微表情传达
- **声音/BGM节奏**：BGM随Beat Engine变化（Hook引爆/Friction动作/Spike静音/Button骤停），SFX强化可拍摄动作

**批量模式 vs 多 Agent 模式的选择：**
| 场景 | 推荐方式 |
|------|---------|
| 多集快速出稿 | execute_code 批量生成 |
| 单集精雕细琢 | delegate_task 独立审核员 |
| **最佳实践** | 批量生成初稿 + 独立审核员逐集审 + 不通过就重写 |

## 大规模批量生成检查清单 (v2.4 ⭐ 2026-04-30 Count of Monte Cristo 验证)

> 当一次性生成 10+ 集时，必须执行以下步骤，否则会出现文件缺失（如 EP-20 prompts 漏写）。

**生成后必做验证（在继续工作台之前）：**

```python
import os
base = "/path/to/project"
for i in range(1, 37):
    ep = f"EP-{i:02d}"
    for subdir in ["script", "storyboard", "prompts"]:
        fp = f"{base}/{subdir}/{ep}.md"
        if not os.path.exists(fp):
            print(f"MISSING: {subdir}/{ep}.md")
```

**分镜批量生成标准化参数（36集验证）：**
| 参数 | 标准 | 范围 |
|------|------|------|
| 镜头数 | 18 | 16-20（氛围16-18 / 标准18-20 / 高潮20-24） |
| 总时长 | 70s | 固定 |
| 正面镜头比例 | 80-94% | 表情特写为主时偏高可接受 |
| 运镜种类 | ≥5种 | 推/拉/跟拍/俯拍/俯拍/过肩/固定 |
| 时长校验 | 必须等于70s | 每集 Shot Notes 末尾必须有校验行 |

**Prompts 批量生成标准化结构（每集必含）：**
1. `## Visual Asset References` — 本集角色外观 + 场景列表
2. `### Frame N: time Shot` — 每张图的完整 Prompt（18-20帧）
3. `## Shot Notes` — 场景/色调/情感弧线/关键道具/服装注意/对白

**批量生成后缺失处理流程：**
1. 运行验证脚本（见上）
2. 发现缺失 → 立即读取对应 script/EP-XX.md
3. 手写补齐 storyboard 和 prompts（不走 delegate_task，速度更快）
4. 重新验证确认全部存在 → 才能进入工作台阶段

## 生产工作台页面 (Index Page) — v4.0

> 将三件套 MD 文件转换为交互式 SPA（单 HTML 文件），用于管理 AI 生图/视频流程、追踪进度、一键复制 Prompt。
> **三文件架构 v4.0**：`generate_index.py`（MD → JSON） + `short-drama-production-index/`（固定模板 + 构建脚本）
> 详细规范见：同仓库 `short-drama-production-index/` 目录或技能 `short-drama-production-index`

### Step 1: `generate_index.py` — MD → JSON 解析器

> ⭐ **推荐使用模板**：`templates/generate_index.py`（已包含双格式解析 + VO-only 支持）
> 复制到项目根目录即可运行：`cp templates/generate_index.py /path/to/project/ && python3 generate_index.py`

**核心结构**（关键陷阱已内联到解析器中）：

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
    data = {'project': 'ProjectName', 'total_episodes': 33, 'episodes': [], 'characters': [], 'manifest': {}, 'scenes': [], 'props': []}
    
    # 加载 manifest, scene_prop_data.json
    if os.path.exists('visual_assets/manifest.md'):
        data['manifest'] = parse_manifest(read('visual_assets/manifest.md'))
    if os.path.exists('scene_prop_data.json'):
        with open('scene_prop_data.json', 'r', encoding='utf-8') as f:
            sp_data = json.load(f)
        data['scenes'] = sp_data.get('scenes', [])
        data['props'] = sp_data.get('props', [])
    
    # 遍历 script/ 目录，按 EP 解析三件套
    script_dir = os.path.join(BASE, 'script')
    for fname in sorted(os.listdir(script_dir)):
        if not fname.endswith('.md'): continue
        ep_id = fname.replace('.md', '')
        episodes.append({
            'id': ep_id, 'title': title,
            'script': parse_script(read(f'script/{fname}')),
            'storyboard': parse_storyboard(sb_md),
            'prompts': parse_prompts(pr_md),
        })
    
    # 输出 JSON
    with open('project_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
```

**完整代码见模板**：`templates/generate_index.py`（含全部解析器实现 + 正则模式速查表）

> ⭐ **数据提取原则（用户偏好）**：剧本对白/VO/Cliffhanger 等复杂结构化数据 → **主模型直接提取**，不用正则。规则格式（分镜 Markdown 表格、manifest 表格）→ 正则脚本。

### Step 2: 运行解析

```bash
cd /path/to/project
python3 generate_index.py
# → 生成 project_data.json
```

### Step 3: 复制工作台风架 + 构建

```bash
# 从 drama-prompts 复制 short-drama-production-index 到项目
cp -r ~/.hermes/tasks/drama-prompts/short-drama-production-index/* /path/to/project/  # 同仓库下

# 构建
cd /path/to/project
python3 build_html.py
# → 生成 index.html（~635KB，单文件自包含，内含所有数据分块）
```

**v4.0 工作台架构**：

| 文件 | 角色 | 大小 |
|------|------|------|
| `template.html` | 固定 SPA 应用模板，含 9 Tab + 附件预览 + 全量可编辑 + 导入/导出 | ~32KB |
| `build_html.py` | 构建脚本：读取 JSON → 分块（~30KB/块）→ 注入 → 输出 index.html | ~2KB |
| `project_data.json` | 数据源（`generate_index.py` 生成） | 项目相关 |
| `index.html` | 最终产物，单文件自包含，双击即用 | ~635KB |

**9 个 Tab**：📊 仪表盘 / 🎬 分镜 / 📝 剧本 / 👤 角色 / 🏰 场景 / 🧰 道具 / 🖼️ 图片Prompt / 🎞️ 视频Prompt / 📁 素材库

**核心特性**：
- **全量可编辑**：所有文本字段 `contenteditable`，失焦自动存 localStorage，刷新不丢
- **💾 保存 JSON**：合并编辑回 JSON 后下载，替换后 `python3 build_html.py` 重新生成
- **📂 加载 JSON**：选择本地 JSON 文件导入替换
- **数据分块注入**：JSON 按 ~30KB 分块存入 `<script type="application/json" class="__data_chunk__">` 标签，JS 收集拼接后解析
- **移动端适配**：侧栏隐藏、Tab 横滑、附件缩略图缩小

### 正则解析模式速查表

| 解析目标 | 正则锚点 |
|----------|---------|
| 场景分解 | `## Scene Breakdown\n(.+?)(?=\n## [^#]|\Z)` |
| Key Dialogue | `## Key Dialogue\n(.+?)(?=\n## [^#]|\Z)` |
| 分镜表 (Key Frames) | `## Key Frames\n(.+?)(?=\n## [^#]|\Z)` |
| Image Prompts | `### Frame (\d+): (.+?)\n\*\*Prompt:\*\*(.*?)` |
| Video Prompts | `### Shot (\d+): (.+?)\n\*\*Prompt:\*\*(.*?)` |