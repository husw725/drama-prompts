---
name: short-drama-production-index
description: 为短剧项目生成 JSON 数据和交互式 HTML 工作台（固定模板 + JSON 注入单文件架构）
version: 4.0
author: Hermes Agent
metadata:
  hermes:
    tags: [Short-Drama, Production-Workflow, HTML-Workbench, Project-Index]
    related_skills: [drama-team, seedance-prompt-optimizer, screenplay-hollywood-format]
---

# Short Drama Production Index

**v4.0 架构：固定 HTML 模板 + JSON 分块注入（每块 ~30KB）+ 全量可编辑 + 自动保存 + 导出 JSON**

HTML 是固定"应用"（`template.html`），JSON 是数据（`project_data.json`），`build_html.py` 分块注入生成单文件 `index.html`。

## 触发条件

短剧项目已完成剧本/分镜/Prompts 文件，需要生成结构化 JSON 和交互式工作台。

## 核心架构

| 组件 | 说明 | 更新频率 |
|------|------|---------|
| `template.html` | 固定 SPA 应用（~31KB），含 9 Tab + 附件预览 + JSON 分块数据标签 + 全量可编辑 + 保存 JSON | 极少改动 |
| `project_data.json` | 项目数据（JSON），符合固定格式 | 每次更新 |
| `build_html.py` | 注入脚本：读取 JSON → 分块成 ~30KB chunks → 每个注入 `<script type="application/json" class="__data_chunk__">` → 输出 index.html | 极少改动 |
| `index.html` | 生成结果（~635KB），单文件自包含，双击直接打开使用 | 每次构建 |

## 工作流

### Step 1: 生成 `project_data.json`

**数据提取原则（用户偏好）**：
- **剧本数据**（角色/对白/场景/动作）→ **主模型直接提取**，不用正则（见下方坑点）
- **规则格式**（分镜 Markdown 表格、manifest 表格、Prompts 固定结构）→ 正则脚本
- **❌ 不用本地 LLM 批量提取** — 串行太慢且超时

### Step 2: JSON 格式规范

```json
{
  "project": "Carmilla",
  "total_episodes": 33,
  "manifest": {
    "aspect_ratio": "9:16",
    "scenes": [{"name": "...", "attrs": {"------": "------", "风格": "...", "色调": "..."}}],
    "props": [{"name": "...", "description": "...", "episodes": "EP-01, EP-02"}],
    "effects": [{"name": "...", "description": "...", "episodes": "..."}]
  },
  "characters": [{"name": "...", "desc": "...", "attrs": {"年龄": "...", "性格": "..."}}],
  "episodes": [{
    "id": "EP-01",
    "number": 1,
    "title": "THE CURSE REVEALED",
    "shot_count": 22,
    "duration": "70s",
    "script": "# EP-01: THE CURSE REVEALED\n\n## Source Screenplay\nCARMILLA\n...",
    "storyboard": {
      "shots": [{"#": "1", "time": "0-1s", "scene": "S-01 Laura卧室", "shot": "极端特写", "camera": "微距", "duration": "1s", "description": "...", "characters": "Laura", "atmosphere": "...", "lighting": "...", "sfx": "...", "bgm": "...", "num": 1}]
    },
    "review": {"score": 88, "criteria": [{"name": "...", "score": 9, "max_score": 10, "pass": true}]},
    "prompts": {
      "imagePrompts": [{"frame": 1, "time": "0-1s", "prompt": "Gothic style...", "attachments": ["/mnt/d/output/img1.jpg", "/mnt/d/output/img2.jpg"]}],
      "videoPrompts": [{"shot": 1, "timeRange": "0-26s", "duration": "26s", "prompt": "Cinematic...", "attachments": ["/mnt/d/output/vid1.mp4"]}]
    }
  }]
}
```

**关键字段说明**：
- `project` = 项目名（**不是** `manifest.title`，HTML 标题从此读取）
- `total_episodes` = 总集数，显示在标题旁
- `manifest.scenes.attrs["------"]` = "------" 是分隔线，前端渲染时跳过
- `prompts[].attachments` = **字符串数组**，可空/单条/多条，存图片/视频地址
- `episodes[].script` = **完整 markdown 剧本内容**（从 `script/EP-XX.md` 读取全文），前端做基本 markdown→HTML 转换
- **包含 `images` 字段**（可选），`attachments` 是字符串数组
- 编辑保存：所有内容 `contenteditable`，失焦自动存 localStorage
- **💾 保存 JSON**：头部按钮，合并 edits 到 D 后下载 `project_data.json`
- **📂 加载 JSON**：头部按钮，选择本地 JSON 文件 → FileReader → 替换 D → 重渲染

### Step 3: 构建单文件 `index.html`

技能侧生成 `project_data.json` 后，运行：

```bash
python3 build_html.py
# → 生成 index.html（~635KB，单文件，内含所有数据分块）
```

**build_html.py 原理（JSON 分块方案 v4.0）**：
- 读取 `project_data.json` → 验证格式
- `json.dumps(data, ensure_ascii=False)` 生成 UTF-8 JSON 字符串
- 按 ~30KB 切分成 N 个 chunk（如 21 块）
- 每个 chunk 注入一个 `<script type="application/json" class="__data_chunk__">` 标签
- 替换 template.html 中的 `<!--DATA_CHUNKS-->` 占位符
- 输出 `index.html`

**HTML 端数据加载（分块拼接）**：
```javascript
var chunks = document.querySelectorAll('script.__data_chunk__');
var jsonStr = '';
for(var i = 0; i < chunks.length; i++) jsonStr += chunks[i].textContent;
D = JSON.parse(jsonStr);
```
如果分块加载失败，fallback 尝试 XHR 加载同目录 `project_data.json`（HTTP 模式）。

**为什么用分块方案（不是单一大块/base64/字符串嵌入）：**

| 方案 | 问题 |
|------|------|
| base64 数组 + atob 循环解码 | 900KB+ 时 atob 超时，JS 异常（v3.4） |
| base64 字符串拼接（4924行 `+`） | JS 引擎解析超时/失败 |
| 单行 base64 字符串 | 浏览器可能缓存旧版 |
| `json.dumps(json.dumps())` 嵌套字符串 | 引号冲突，需要额外解码层 |
| `<script type="application/json">` 单一大块（920KB） | **浏览器解析超大 script 标签后，后面的 JS 脚本根本不执行！** |
| `<div>` + base64 | atob() 982KB 超时，2个 JS 异常 |
| **✅ JSON 分块（~30KB/块）** | 每块浏览器轻松解析，JS 拼接后 JSON.parse，零错误 |

**用户打开 index.html** → 分块脚本自动加载数据，打开即工作台。

## 9 个 Tab

| Tab | 内容 |
|-----|------|
| 📊 仪表盘 | 全局统计（总集/图片Prompt/视频Prompt/平均分/角色/场景/道具）、制作进度分布（6 阶段进度条）、各集概览表 |
| 🎬 分镜 | 每集分镜表格（**所有列可编辑**）、审核详情 |
| 📝 剧本 | Markdown 全文（**可编辑**，渲染后直接修改） |
| 👤 角色 | 角色详情 + 属性表（**所有字段可编辑**） |
| 🏰 场景 | 场景详情 + 属性表（跳过 "------" 键，**所有字段可编辑**） |
| 🧰 道具 | 名称/描述/出现集数（**所有字段可编辑**） |
| 🖼️ 图片 Prompt | 可编辑 + **附件缩略图**（可多张，点击放大） |
| 🎞️ 视频 Prompt | 可编辑 + **附件**（图片/视频，点击播放） |
| 📁 素材库 | 全局/分集图片缩略图 |

## 功能特性

- **全量可编辑**：所有 Tab 中所有文本字段均 `contenteditable`，失焦自动存 localStorage
- **刷新不丢**：渲染用 `gVal(key, default)` 优先读取 localStorage 编辑值（不是原始数据）
- **💾 保存 JSON**：头部按钮，点击后 `mergeEditsIntoD()` 将 edits 合并回 JSON → 下载 `project_data.json` → 替换后 `python3 build_html.py` 重新生成
- **📂 加载 JSON**：头部按钮，点击后 `FileReader.readAsText` → `JSON.parse` → 替换全局 `D` → 清空 edits/statuses → 清除 localStorage → `initApp()` 重渲染
- **附件预览**：图片显示缩略图（点击放大），视频显示播放器（点击播放）
- **集数切换**：右上角下拉 + 左侧栏点击
- **状态管理**：每集 6 阶段（草稿→分镜完成→生图中→生图完成→生视频中→成片完成），状态颜色侧栏显示
- **移动端适配**：侧栏隐藏、Tab 横滑、附件缩略图缩小

## JSON 格式验证

```python
import json

def validate_project_data(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Required top-level keys
    assert 'project' in data, "Missing 'project' (title)"
    assert 'episodes' in data and len(data['episodes']), "Missing or empty 'episodes'"
    
    # Each episode must have
    for ep in data['episodes']:
        assert 'id' in ep, "Episode missing 'id'"
        assert 'number' in ep, "Episode missing 'number'"
        assert 'title' in ep, "Episode missing 'title'"
    
    print(f"OK: {data['project']}, {len(data['episodes'])} episodes")
    return True
```

## 已知 Pitfalls

### 剧本解析：用主模型提取，不用正则

正则解析剧本对白时持续失败：
- 动作描述混入对白（`Carmilla touches the mother's face` 被捕获为对白）
- V.O. vs 普通对白、CONT'D 后缀、多行对白、动作/对白边界

**正确做法**：主模型逐集精读 → 输出结构化 JSON。33 集一次完成。

### 分镜表头必须动态解析

不要硬编码表头列数（8 列/12 列变化频繁）：
```python
lines = [l for l in text.split('\n') if l.strip().startswith('|') and not all(c in '-_' for c in l.split('|')[1])]
headers = [h.strip() for h in lines[0].split('|')[1:-1]]
```

### 正则注意事项
- `## Scene Breakdown\n(.+?)(?=##|$)` — 用 `\n` 不是 `\\n`（在 `r''` 字符串中）
- `parse_table` 最小列数用 `< 2` 不是 `< 3`（Key Dialogue 只有 2 列）
- `## Cliffhanger` 可能带后缀（`## Cliffhanger / 终局`），用 `## Cliffhanger[^\n]*\n`
- Manifest section 正则用精确匹配（`## Scene Visuals`、`## Prop Reference Prompts`），避免误吸脚本标题

### localStorage 编辑 Key 格式

前端 `saveCell(el, key)` 用统一 key 格式：
- `EP-01_sb_0_description` → split('_') → `['EP','01','sb','0','description']` → shot index=`parts[3]`, column=`parts[4]`
- `EP-01_ip_0` → split('_') → image index=`parts[3]`
- `EP-01_vp_0` → split('_') → video index=`parts[3]`
- `char_0_name`, `char_0_desc`, `char_0_<attr>` → 角色编辑
- `scene_0_name`, `scene_0_<attr>` → 场景编辑
- `prop_0_name`, `prop_0_desc`, `prop_0_eps` → 道具编辑
- `EP-01_script` → 剧本全文编辑
- **不要写成 `parts[2]`** — 那是 `sb/ip/vp` 标记，不是索引

### 数据注入方式（v4.0 — JSON 分块）

**已验证方案：JSON 字符串按 ~30KB 分块，每块塞进 `<script type="application/json" class="__data_chunk__">` 标签。**
- template.html 放 `<!--DATA_CHUNKS-->` 占位符
- build_html.py：`json.dumps(data, ensure_ascii=False)` → 按 30KB 切分 → 每个 chunk 注入 `<script type="application/json" class="__data_chunk__">chunk内容</script>` → 替换占位符
- HTML 启动 IIFE：收集所有 `script.__data_chunk__` 的 textContent → 拼接 → JSON.parse
- Chunk 内如有 `</script>` 需转义为 `<\\/script>`
- **有 XHR fallback**：分块失败则尝试 `XMLHttpRequest('project_data.json')`（HTTP 模式）

**❌ 不要用的方案（全部已在 v3.4-v3.9 中验证失败）：**

| 方案 | 失败原因 |
|------|---------|
| base64 数组 + atob 循环 | 900KB+ 时 atob 超时，JS 异常 |
| base64 字符串拼接（4924行 `+`） | JS 引擎解析超时 |
| `json.dumps(json.dumps(data))` 嵌套字符串 | 引号冲突，需要额外解码层 |
| `<script type="application/json">` **单一大块**（920KB） | **浏览器解析超大 script 标签后，后面的 JS 脚本根本不执行！IIFE 不跑，D 永远是 null** |
| `<div>` + base64 | atob() 982KB 超时，2 个 JS 异常 |
| 单行 JS 对象字面量 `D = {...}` | JSON 里含大量 `"` 直接破坏 JS 语法 |

### 编辑值渲染（gVal 模式）

**关键修复**：渲染时**必须用 `gVal(key, default)`** 读取值，不能直接用原始数据。否则刷新后编辑值丢失。
```javascript
// 正确：优先返回 localStorage 中的编辑值
function gVal(key, def) { return edits[key] !== undefined ? edits[key] : def }
// 渲染时：var dv = gVal(key, shot[k] || '');
```
**失焦清除样式**：`saveCell` 中必须 `el.classList.remove('cell-edited')`，否则高亮不消失。

### initApp 执行时机

`initApp()` 必须在脚本末尾调用，确保 `TABS`、`esc()` 等所有变量和函数已定义。不能放在 IIFE 解码后立即执行。

## 相关技能

- `drama-team` — 短剧编剧系统
- `seedance2-short-drama-workflow` — Seedance 2.0 工作流
