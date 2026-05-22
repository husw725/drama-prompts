3. **跨集视觉不一致** — 角色服装、道具、场景在AI生图时漂移
4. **编剧自批** — 缺乏独立审核，质量问题到生图阶段才发现
5. **伏笔无追踪** — 埋下的线索无人回收，"紫色咬痕"在EP-03出现，EP-10还是没解释

## 解决方案架构

### Agent 角色分工

| Agent | 职责 |
|-------|------|
| **主编剧** (主 Agent) | 严格按集串行创作剧本、分镜、AI Prompts |
| **视觉导演** (Visual Director) | 创建视觉资产清单，定义角色外观、服装、道具、场景的统一视觉规范 |
| **Aligner 系统** | 按内容类型路由到专用审核员：Script-Aligner（剧本）、Storyboard-Aligner（分镜）、Prompt-Aligner（Prompts），返回 PASS/FAIL。详见本技能 `## 审核员系统（三视角定性 + 三Aligner定量）
### 导演覆盖机制（v3.7 ⭐ 新增）

> 当导演（用户）对 Aligner 评分有异议时，可启动覆盖机制。

| 信号 | 含义 | 操作 |
|------|------|------|
| 🟢 Green | 导演同意 Aligner 判定 | 无需操作，正常流程 |
| 🟡 Yellow | 导演认为某项扣分过严 | 标记该项为 `director_review`，Aligner 报告中注明，不阻塞流程 |
| 🔴 Red | 导演认为 Aligner 判定完全错误 | 标记该项为 `director_override`，用导演评分替代，记录覆盖理由 |

**覆盖限制**：
- 每集最多覆盖 2 项（防止全面绕过审核）
- 覆盖项必须在审核报告中注明 `Director Override: [理由]`
- 被覆盖的项不参与后续集的"模式学习"（避免污染 Aligner 判断基准）

` 章节 |

### 核心机制

1. **🔥 严格按集串行生成（v2.4 重大变更）** — 不使用多子Agent并行。主Agent逐集完成：EP-01剧本→审核→分镜→Prompts→提取连续性信息→EP-02...。避免会话隔离导致的叙事断裂。
2. **🔥 连续性追踪文件 `continuity.md`（v2.4 新增）** — 每集完成后自动更新，记录伏笔、悬念、角色状态变化，下一集开始前强制读取。
3. **六阶段创作流程** — 大纲 → 人物 → **视觉资产清单** → **按集循环（剧本→分镜→Prompts）**
4. **视觉资产驱动** — 所有 Prompts 强制注入视觉资产清单中的角色描述，确保跨集一致性
5. **ReAct 循环优化** — 按内容路由到对应 Aligner 审核（剧本→Script-Aligner，分镜→Storyboard-Aligner，含跨集连续性），不达标返回修改建议，循环直到通过
6. **文档驱动架构** — 所有内容分文件存储，支持断点续写



### 竖屏视觉语法（v3.8 ⭐ 新增）

> 竖屏不是"横屏裁剪"，它有独特的视觉语法和叙事逻辑。

**1. 纵向视线引导** — 竖屏天然视线流：上→下；上方=权威/未来/希望，下方=压迫/过去/恐惧
**2. 画外空间叙事** — 竖屏左右画外空间巨大，角色看向画外→观众看不到→紧张感倍增
**3. 文字叠加叙事** — 倒计时叠加、内心OS文字、消息弹窗（⚠️ AI生图中文字必崩，需后期合成）
**4. 竖屏亲密空间** — 竖屏天然适合单人/双人近景，双人近景是杀手锏（拆分生成后合成）

## 项目目录结构

```
project/
├── TASK.md                      # 任务进度跟踪
├── outline.md                   # 故事大纲
├── continuity.md                # 🔥 v2.4 剧集连续性追踪（伏笔/悬念/角色状态/交接记录）
├── characters/
│   └── characters.md            # 人物设定（性格、关系、动机、弧光）
├── visual_assets/
│   └── manifest.md              # 视觉规则（服装指南、表情库、色调/光影/构图）
├── scene_prop_data.json         # 场景/道具 Reference Prompts（AI生图参考图）
├── script/
│   └── EP-XX.md                 # 各集剧本
├── treatment/
│   └── EP-XX.md                 # 各集 Director's Treatment（v3.8 新增）
├── storyboard/
│   └── EP-XX.md                 # 各集分镜
├── prompts/
│   └── EP-XX.md                 # 各集 AI Prompts（含视觉资产注入）
├── generate_index.py            # MD → JSON 解析脚本
├── build_html.py                # JSON → SPA 工作台
├── project_data.json            # 结构化数据（工作台数据源）
├── index.html                   # 离线工作台页面
└── script.progress.md           # 创作进度记录
```