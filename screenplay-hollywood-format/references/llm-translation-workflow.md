# LLM 翻译法：中文剧本 → 纯英文好莱坞剧本

> 2026-05-14 在 Christ of Monte Cristo (25集) 项目中验证。替代词表映射法，从根本上消除中文残留。

## 为什么不用词表法

词表映射法（ACTION_PHRASES / LOCATION_MAP）无论怎么扩充，总有长尾问题：
- 音效 `(咚……咚……咚……)`、`(SFX - tapping sound)`
- 闪回标记 `(EP-03酒馆写诬告信画面)`
- 复合动作 `(喘息，无法言语)`、`(沉默回望)`
- `—` 破折号角色行的 EN 列也塞了中文

25 集最终总有 10-15 行中文残留，需要人工修补。

## LLM 翻译法

**核心思路**：对每集调用 LLM，用 system prompt 包含完整好莱坞格式规范 + 角色名映射，直接输出纯英文 screenplay 文本。

### Prompt 结构

```
[Role + Rules]
- 11 条格式规范（场景标题、角色名、动作、对白、转场等）
- 角色名中英映射表
- 输出格式示例（含缩进）

[Source Script]
- 原始 EP-XX.md 内容
```

### API 参数

- `temperature: 0.3` — 保持一致性，不要过度发挥
- `max_tokens: 8000` — 每集约 2-3k tokens 输出
- `top_p: 0.9`
- `timeout: 300` — **重要**：本地 LLM 处理长 prompt（中文剧本 + 翻译指令）需要 60-180s，120s 会超时

> ⚠️ timeout/串行策略是**本地单机 LLM**（qwen 系列 sGLang/vLLM 单实例）的环境经验；云 API 可正常并发，无需 300s timeout。

### Prompt 优化

**Prompt 要精简** — 不要堆叠 11 条规则 + 完整示例。经验：精简到 8 条规则 + 一行式角色映射 + 最小示例，能将每集翻译时间从 120s 降到 60s。

```
Convert [script] into English Hollywood screenplay format.

RULES: (8条核心规则)
NAMES: 角色名=DANTE, 角色名=MERCEDES, ...（一行式）
OUTPUT: 最小格式示例（含 EPISODE/FADE IN/角色/对白/FADE OUT）
Translate:
```

### 执行策略

- **后台运行 + `notify_on_complete`** — 不要开子代理，纯脚本执行直接用后台
- **串行** — 本地 LLM 不支持并发，`MAX_CONCURRENT = 1`
- 25 集预计 15-30 分钟（每集 30-60s）
- 每集翻译完立即检查中文残留率（应 <1%）

### 解析 .txt → DOCX

从 LLM 输出的纯文本解析格式：
- `0` 缩进 → Action（普通段落）
- `≥6 空格` + ALL CAPS → Character Name（加粗，居中缩进）
- `≥6 空格` + `(xxx)` → Parenthetical（缩进括号）
- `≥6 空格` + 普通文本 → Dialogue（左右缩进）
- `INT./EXT.` 前缀 → Scene Heading（大写加粗）
- `FADE/CUT/DISSOLVE` → Transition（右对齐加粗）

### python-docx 排版通用代码

东亚字体设置必须通过 `run._element` 操作 rPr（`p.element.rPr.rFonts.set(...)` 是错误 API，会报 `AttributeError`）：

```python
from docx.shared import Pt
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

def add_run_with_font(p, text, font_name='Courier New', font_size=12, bold=False):
    run = p.add_run(text)
    run.font.name = font_name
    run.font.size = Pt(font_size)
    run.bold = bold
    # 正确设置东亚字体（避免 .element.rPr 报错）
    r = run._element
    rFonts = r.find(qn('w:rPr'))
    if rFonts is None:
        rFonts = OxmlElement('w:rPr')
        r.insert(0, rFonts)
    rFonts.set(qn('w:eastAsia'), font_name)
    return run
```

### 质量指标

| 方法 | 中文残留 | 翻译质量 | 维护成本 |
|---|---|---|---|
| 词表法 | 5-10% | 中等（逐句匹配） | 高（每遇新 case 补词表） |
| LLM 翻译法 | <1% | 高（上下文理解） | 低（只需一次 prompt） |

### 执行方式

1. 主模型写 `translate_to_screenplay.py` 脚本
2. 后台执行 `python3 translate_to_screenplay.py`
3. `notify_on_complete` 完成后检查
4. 串行运行（本地 LLM 不支持并发）
