# 连续性追踪系统

> 每集开始前/结束后读取；回退时读取。工作流见 `parts/workflow.md`。

---

## continuity.md — 叙事连续性

> 连接集与集之间的"叙事记忆"。每集更新（前3集逐集，第4集起每3集批量）。下一集编剧开始前必须读取。

### 文件格式

```markdown
# 剧集连续性追踪

## 当前进度
- **已完成**: EP-01, EP-02
- **进行中**: EP-03
- **总集数**: 12 集

## 付费墙规划（3-7-21 Block 分层）

| Block | 集数 | 目标 | 策略 | Beat Engine 重点 |
|-------|------|------|------|-----------------|
| **Block 1** | EP 1-3 | 拉新+留存 | 免费，最强钩子，建立premise+DI信息优势 | Hook引爆(3秒定帧)，Button制造"不看不行" |
| **Block 2** | EP 4-7 | 转化 | 首次付费，沉没成本建立，DI差距拉大 | Friction加重，Spike重新定价 |
| **Block 3** | EP 8-21 | 深度绑定 | 付费集，DI维持，关系深化 | Spike密度可降，每集必须有Button |
| **Block 4** | EP 22+ | 续费 | 沉没成本锁住，揭秘区 | DI揭秘=最大付费驱动力 |

**硬规则**：
- Block 1 EP-01 = 广告，Hook全季最炸
- Block 2 EP-04 Spike = "不看会亏"的信息重新定价
- Block 3 DI差距不能缩小
- Block 4 DI收窄→真相揭示→新Irony建立

## 伏笔管理

| ID | 描述 | 埋入集 | 计划回收集 | 状态 | 备注 |
|----|------|--------|-----------|------|------|
| F-01 | [描述] | EP-XX | EP-XX | 🟡待回收 | |
| F-02 | [描述] | EP-XX | EP-XX | 🔵已埋 | |
| F-03 | [描述] | EP-XX | EP-XX | ✅已回收 | |
| F-04 | [描述] | EP-XX | EP-XX | ⏳逾期 | 需紧急处理 |
| F-05 | [描述] | EP-XX | EP-XX | ❌废弃 | [废弃原因] |

## Dramatic Irony 追踪

| ID | 观众知道 | 角色不知道 | 建立集 | 揭秘集 | 差距 | 备注 |
|----|---------|-----------|--------|--------|------|------|
| DI-01 | [信息] | [角色] | EP-XX | EP-XX | 🔴大/🟡缩小 | |

## 上一集结尾 (Last Cliffhanger)

### EP-XX 结尾
- **Hook**: [类型+等级]
- **描述**: [具体描述]
- **下一集必须**: 1.承接 2.推进 3.新悬念

## 角色当前状态

| 角色 | 当前状态 | 变化时间 |
|------|---------|---------|
| [角色名] | [状态描述] | EP-XX |

## 角色互动记录

| 集数 | 互动角色 | 互动类型 | 情感基调 |
|------|---------|---------|---------|

> 用途：Aligner检查"原谅/和解是否有前置互动铺垫"

## 感官刺激记录

| 集数 | 视觉动作 | 物理亲密 | 超自然现象 | 危险场景 | 感官得分(0-4) |
|------|---------|---------|-----------|---------|--------------|

> 用途：Aligner检查"连续低密度集"

## 冲突模式记录

| 集数 | 冲突类型 | 具体表现 |
|------|---------|---------|

⚠️ 下集避免重复以上冲突类型

## 叙事预算状态
- **活跃伏笔数**: N个（🟡待回收X + 🔵已埋Y）— 本集允许新埋≤1
- **逾期伏笔**: [必须本集或下集处理]
- **已出场角色数**: N个 — 本集允许新角色≤1
- **近3集冲突类型**: [列表] — 本集避免
- **近3集感官得分**: [列表] — 低集必须补偿
- **付费墙状态**: [当前Block+策略]
```

---

### 逾期伏笔自动检查（每集生成后必跑 ⭐）

> 每集剧本/分镜生成后，自动扫描 continuity.md 中 ⏳逾期 和 🟡待回收 项，输出告警。

**检查逻辑（伪代码）**：
```
for each foreshadow in continuity.md:
  if status == ⏳逾期:
    WARN: "F-{id} 已逾期{current_ep - due_ep}集，必须本集或下集回收"
    if current_ep - due_ep >= 3:
      ERROR: "F-{id} 逾期≥3集，Aligner将扣5分"
  if status == 🟡待回收 and due_episode == current_ep:
    WARN: "F-{id} 本集到期，必须回收"
  if status == 🟡待回收 and due_episode == current_ep + 1:
    INFO: "F-{id} 下集到期，提前提醒"
```

**集成方式**：
- 阶段4 Step 3（更新continuity后）自动执行检查
- 检查结果追加到 TASK.md 的「伏笔告警」章节
- ⏳逾期项在下一集编剧 Step 0 时强制读取（加入上下文）
- 如逾期≥3集，Aligner自动扣5分（无需人工触发）

**Python 检查脚本（可独立运行）**：
```python
import re, sys

def check_foreshadow(continuity_path, current_ep):
    with open(continuity_path) as f:
        content = f.read()
    warnings = []
    # 匹配伏笔表行：| F-XX | 描述 | EP-XX | EP-XX | 状态 |
    pattern = r'\|\s*(F-\d+)\s*\|\s*([^|]+)\s*\|\s*EP-(\d+)\s*\|\s*EP-(\d+)\s*\|\s*(🟡|🔵|✅|⏳|❌)'
    for m in re.finditer(pattern, content):
        fid, desc, planted, due, status = m.groups()
        due_ep = int(due)
        if status == '⏳':
            overdue = current_ep - due_ep
            warnings.append(f"⚠️ {fid} 已逾期{overdue}集: {desc.strip()}")
            if overdue >= 3:
                warnings.append(f"🔴 {fid} 逾期≥3集，Aligner扣5分")
        elif status == '🟡' and due_ep == current_ep:
            warnings.append(f"⏰ {fid} 本集到期，必须回收: {desc.strip()}")
        elif status == '🟡' and due_ep == current_ep + 1:
            warnings.append(f"💡 {fid} 下集到期: {desc.strip()}")
    return warnings

if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else 'continuity.md'
    ep = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    for w in check_foreshadow(path, ep):
        print(w)
```

---

### 伏笔状态机

```
状态转换：
 🔵 已埋 → 🟡 待回收 （current_episode ≥ due_episode - 1）
 🟡 待回收 → ✅ 已回收 （本集处理）
 🟡 待回收 → ⏳ 逾期 （current_episode > due_episode 且未回收）
 ⏳ 逾期 → ✅ 已回收 （后续集补回收）
 ⏳ 逾期 → ❌ 废弃 （编剧决定放弃，需记录原因）
 🔵 已埋 → ❌ 废弃 （剧情调整导致线索不再需要）

Aligner 检查规则：
 1. 每集：⏳逾期伏笔？→ 必须本集或下集处理
 2. 每集：🟡待回收且due_episode=当前集？→ 必须本集回收
 3. ❌废弃：需写明原因，且无后续集依赖
 4. 逾期超过3集未处理 → 扣5分
```

---

### continuity.md 更新规则（每集完成后）

1. 伏笔管理表 — 新增本集埋下的，标记本集回收的
2. Last Cliffhanger — 记录本集结尾悬念
3. 角色状态 — 更新因本集剧情变化的角色
4. 角色物理状态 — 服装/受伤/物理位置变化（仅标注变化）
5. 冲突模式 — 记录本集冲突类型
6. Beat Engine状态 — 四段实际时间分布
7. Premise验证 — 冲突是否Premise驱动
8. DI状态 — 观众信息优势+差距维持
9. 对白=行动 — 解释性对白数量（目标0），冲突前2行进入
10. 竖屏特写占比 — 目标≥50%
11. 声音/BGM节奏 — 是否随Beat Engine变化
12. 未解决问题 — 更新问题列表

---

### 上下文长度管理

**截断策略（continuity.md > 6000字符时触发）**：

| 优先级 | 保留内容 |
|--------|---------|
| **必须保留** | 当前进度、Last Cliffhanger完整、活跃伏笔(🟡+🔵)、角色状态、角色物理状态 |
| **精简保留** | 冲突模式最近3集、未解决问题各一句话 |
| **可截断** | 已回收伏笔(✅→ID+一句话)、5集前冲突模式 |

**EP-10后**：优先读 `continuity_summary.md`（如存在），否则读截断后版本。无论哪种，都必须读上集script的Cliffhanger部分。

---

## visual_continuity.md — 视觉连续性

> 每集分镜完成后更新。下一集分镜/Prompts生成前必须读取。与continuity.md职责分离——叙事连续性 vs 视觉连续性。

### 文件格式

```markdown
# 视觉连续性追踪

## EP-XX 结尾视觉快照
- **画面状态**：[角色位置/景别/朝向/动作]
- **场景物理**：[门/窗/物品状态]
- **色调**：[主色调+辅色调]，与上集差异
- **运镜风格**：[景别偏好+运镜类型]，节奏特征
- **服装状态**：[各角色当前服装]，仅标注变化
- **光源方向**：[主光源方向+色温]
- **与上集视觉差异**：[色调/运镜/服装变化]
```

### 读取规则

| 阶段 | 读取内容 |
|------|---------|
| 分镜生成（阶段5） | 上集结尾快照 |
| Prompts生成（阶段6） | 上集结尾快照 |
| Storyboard-Aligner | 上集结尾快照（跨集视觉承接检查） |
| 批量分镜 | 上一批尾集的结尾快照 |

### 截断/维护策略

| 集数范围 | 策略 |
|---------|------|
| ≤12集 | 全量保留 |
| 13-24集 | 最近3集完整 + 更早集1行摘要 |
| 25集+ | 最近3集完整 + 最近5-10集1行摘要 + 更早集删除 |

触发条件：visual_continuity.md > 4000字符

---

## 质量控制与回退机制

### 质量门禁

| 阶段 | 质量门 | 未通过处理 |
|------|--------|-----------|
| 大纲/人物/视觉资产 | 人工确认 | 重写/调整 |
| 剧本/分镜/Prompts | Aligner ≥ 80 | 重写（最多3轮） |

### 回退链机制

发现前集有重大逻辑错误时：
1. 修复问题集 → 重新Aligner
2. 更新continuity.md（Cliffhanger+角色状态+伏笔）
3. 级联检查后续集（差异检测：只回退真正受影响的集）
4. TASK.md标记回退完成

**触发条件**：人工发现逻辑错误 / 读者评审发现硬伤 / 后续集无法衔接

---

## 读者反馈模拟

> 主Agent内联审查（子Agent必超时）。采样关键集→三视角报告→优先级分级→逐集修改。

**三视角**：
- **急躁哥**：节奏/留存（前5秒hook、爽点密度、拖沓集）
- **逻辑控**：时间线/动机链/道具回收/时代错误
- **视听专家**：多人同镜风险、文字道具、AI生成可行性

**重点关注（US/EU市场）**：
- 前5秒hook：纯风景>5秒=必改
- 拖沓集检测：连续3集"主角倒霉"→至少隔1集有冲突升级
- 时间跳跃>3年→加标题卡
- 时代错误/地理跳跃→加过渡

**审查报告**：REVIEW-IMPATIENT-BRO.md + REVIEW-LOGIC-MASTER.md + REVIEW-VISUAL-EXPERT.md + REVIEW-SUMMARY.md

---

## 增量 Continuity 方案（长剧推荐 ⭐）

> 每集只写 diff，运行时由脚本合并为完整状态。避免每集重写大文件。

### 格式：continuity-delta/EP-XX.yaml

```yaml
ep: 03
cliffhanger: "密室入口暴露，钟声响起"
foreshadow:
 resolve: [F-01] # 本集回收
 plant: [F-07] # 本集新埋
 due_next: [F-02] # 下集到期
chars:
 Laura: {state: "调查咬痕", outfit: white_nightgown}
 Carmilla: {state: "部分揭示身份", outfit: black_dress}
conflict: 信息争夺 # 本集类型，下集避免
beat: {hook: 3, friction: 45, spike: 30, button: 7} # 秒
di:
 DI-01: {gap: "维持", note: "Laura仍不知道"}
sensory: 3 # 感官得分
closeup_pct: 55 # 特写占比
```

### 运行时合并

```python
# continuity_runtime = merge(continuity_base.yaml, delta/EP-01.yaml, ..., delta/EP-N.yaml)
# 每集开始前：合并到当前集 → 传给编剧
# 每集结束后：写 delta/EP-XX.yaml（只写变化量）
```

**优势**：
- 每集更新从~2000字符→~200字符（-90%）
- 不重写大文件，无截断风险
- 可程序化校验（YAML schema）
- 长剧（30+集）无膨胀问题
