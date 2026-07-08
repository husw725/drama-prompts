---
name: seedance-prompt-optimizer
description: Use when optimizing draft prompts for Seedance 2.0 multimodal2video short drama generation. Transforms raw prompts into ByteDance official-compliant format with @image reference syntax, emotional body-signaling, and quality constraints.
version: 1.1.0
author: husw725
license: MIT
metadata:
  hermes:
    tags: [seedance, short-drama, prompt-optimization, video-generation, dreamina]
    related_skills: [drama-team, short-drama-production-index]
---

# Seedance Prompt Optimizer

## Overview

将 draft prompt 优化为符合字节官方《Seedance 2.0 影视场景提示词指南》规范的 multimodal2video 提示词。确保角色一致性、动作合理性和画面质量。

## When to Use

- 用户提供了 draft prompt 需要优化为官方合规版本
- 短剧视频生成前的 prompt 审核与重写
- 需要按 11 步标准化流程转换 prompt

## Input

用户提供：
1. 一个 draft prompt（可能中英文混杂，结构不完整）
2. 传入的参考图列表（如：@图片1=Carmilla角色图, @图片2=Laura角色图, @图片3=场景图等）

**批量模式**：输入是整集 prompts 文件（如 drama-team 的 `prompts/EP-XX.md`）时，对文件内每条 prompt 逐一应用 11 步，输出保持原文件的分节结构。

## 输入来自 drama-team 时

drama-team 的 `prompts/EP-XX.md` 用 `[ref: C-XX]` / `[ref: S-XX]` 引用体系 + 英文 `Shot [N]: [time_range]` 格式，需先做一次映射再走 11 步：

1. **建立 ref → 参考图编号表**：对照项目 `manifest.md`，为本条 prompt 实际用到的每个 `[ref: C-XX]`（角色）和 `[ref: S-XX]`（场景）分配 `@图片N` 编号，角色图在前、场景图在后。
2. **替换引用**：正文中 `[ref: C-01]` + 角色名 → `@图片N的角色名`；`[ref: S-XX]` → 对应场景图声明。
3. **时序格式**：`Shot [N]: [X-Ys]` → `镜头N（X-Y秒）`（即 Step 3 的规则）。
4. **外观描述**：drama-team prompt 中逐字复制的角色外观描述按 Step 2 删除——参考图已锁定外观，只保留 characters.md 之外的剧情新增特征。

## Optimization Steps (11 步逐一执行)

### Step 1: 加 @ 语法声明

开头加 N 行声明（N=参考图数量），格式：

```
@图片1 为角色 Carmilla 外观参考（金色头发、苍白皮肤、暗色维多利亚长裙）
@图片2 为角色 Laura 外观参考（棕色头发、白色睡裙）
@图片3 为卧室场景参考
```

每个声明括号内加 2-3 个关键静态特征。正文中所有角色名替换为 `@图片N的角色名`（如 `@图片1的Carmilla`）。

**原因：** 帮助模型将 prompt 文本与参考图对齐，确保外观一致性。

### Step 2: 删除外观冗余

参考图已锁定外观，删除所有角色外观描述。

- ❌ `Laura (young woman with brown wavy hair and green eyes)`
- ✅ `@图片2的Laura`

只保留：动作、位置、情绪、台词、参考图没有的新增特征（如脖子印记、紫光等剧情元素）。

### Step 3: 分镜时序标准化

- `[0-3s]` → `镜头1（0-3秒）`
- `[3-6s]` → `镜头2（3-6秒）`
- 时长用中文"秒"，不用英文"s"
- **时间缺口补镜头**：draft 时间段之间有缺口时（如 `[0-4s]` 直接跳 `[8-12s]`），按前后镜头的动作逻辑补一个过渡镜头填满缺口（如角色从门口走到床边的移动过程），保证时间轴连续、每个时间段都有明确的人物动作

### Step 4: 情绪外化为身体信号

用具体身体动作替代抽象情绪词：

| 抽象情绪 | 身体信号 |
|---------|---------|
| `frozen with terror` | `双手紧抓床单，双眼因恐惧睁大` |
| `desperate` | `眼泪从脸颊滑落，拼命摇头` |
| `panicked whisper` | `（惊恐低语）` |
| `elegant` | `步伐缓慢优雅` |
| `cold stare` | `目光冰冷，嘴角不自然地微扬` |

### Step 5: 动作慢化

加入"缓慢""缓缓""逐渐"等慢动作修饰词。避免"狂奔""大跳""剧烈翻滚"等大幅度动作。

**原因：** Seedance 2.0 对慢动作的还原度远高于快速动作。

### Step 6: 运镜约束

每个镜头只指定 1 种运镜方式。如需固定镜头，加 `单一固定中景机位`。不要同时推拉摇移。

### Step 7: 约束词结尾

每段 prompt 末尾加固定约束词：

```
面部稳定不变形、五官清晰、人体结构正常、动作自然流畅、画面无卡顿、无闪烁、不生成字幕、角色外观与参考图一致
```

### Step 8: 清理模糊词

删除以下无效描述：
- `Cinematic shot`、`movie scene`、`电影感`
- `mysterious atmosphere`、`氛围感`、`好看点`
- `4K`、`60fps`、`HDR` 等画质参数（这些是接口参数，不是 prompt 内容）

### Step 9: 台词语言统一

- 描述全部用中文
- 台词保留英文（引号标注），情绪标注用中文如 `（惊恐低语）`
- 不要中英混杂

### Step 10: 避免 `--` 截断

搜索全文中的 `--`，替换为 `——`（中文破折号）或文字描述。`--` 后的内容会被模型忽略！

### Step 11: 参考图分工检查

确保每张图只承担一种职责（人物外观/场景空间/特殊特征），不要混用。

## Output Format

只输出优化后的完整 prompt，不解释、不附加说明。结构：

```
@图片1 为角色 XXX 外观参考（特征1、特征2、特征3）
@图片2 为角色 XXX 外观参考（特征1、特征2）
@图片3 为场景描述参考
（空一行）
镜头1（0-X秒）：@图片N的角色在...做...动作...
角色（情绪标注）："台词"
镜头2（X-Y秒）：@图片N的角色...
（空一行）
风格描述，9:16竖屏，运镜描述
面部稳定不变形、五官清晰、人体结构正常、动作自然流畅、画面无卡顿、无闪烁、不生成字幕、角色外观与参考图一致
```

## Verification Checklist

输出前逐项自检：

- [ ] 每张图片有开头声明 + 括注特征
- [ ] 正文中角色都用 `@图片N的角色名` 指代
- [ ] 无外观冗余描述
- [ ] 分镜用 `镜头N（X-Y秒）` 格式
- [ ] 情绪用身体信号表达
- [ ] 无模糊词（Cinematic/atmosphere/4K 等）
- [ ] 无 `--` 符号
- [ ] 结尾有完整约束词
- [ ] 描述全中文，台词英文引号
- [ ] 每个时间段至少有一个明确的人物动作/位置描述

## Common Pitfalls

1. **忘记加 @ 语法声明** — 模型不知道参考图与角色的对应关系，导致外观不一致
2. **保留外观描述** — 参考图已锁定外观，重复描述反而干扰模型
3. **用 `--` 而非 `——`** — `--` 后的内容被模型截断忽略
4. **情绪用抽象词** — "恐惧""悲伤"不如"双手颤抖""眼泪滑落"具体
5. **一个镜头多种运镜** — 同时指定推拉摇移会导致模型无法执行
6. **参考图混用** — 角色图+场景图混在一起，模型分不清职责
7. **缺少约束词** — 结尾没有固定约束词，容易出现面部变形或闪烁
8. **无时间锚定** — 每个时间段必须有明确的人物在场，否则生成空镜头

## Examples

### Example: 角色对峙场景

**Input (draft):**
```
[0-4s] Laura frozen on bed, Carmilla approaches menacingly from doorway
Laura (terrified whisper): "I cannot move..."
Carmilla (soft voice): "Hush. I am here."
[8-12s] Laura desperately tries to shake her head, Carmilla stops her hand inches from Laura's face
Laura (desperate): "No... I beg you... no."
Cinematic, Gothic style, 9:16 vertical
```

**Reference images:** @图片1=Carmilla, @图片2=Laura, @图片3=卧室

**Output (optimized):**
```
@图片1 为角色 Carmilla 外观参考（金色头发、苍白皮肤、暗色维多利亚长裙）
@图片2 为角色 Laura 外观参考（棕色头发、白色睡裙）
@图片3 为卧室场景参考

镜头1（0-4秒）：@图片2的Laura僵硬坐在床上，双手紧抓床单，双眼因恐惧睁大。@图片1的Carmilla站在Laura床后的门口，注视着她。

Laura（恐惧颤抖）："I cannot move..."

镜头2（4-8秒）：@图片1的Carmilla从门口缓慢走向床边，长裙随步伐轻轻摆动。@图片2的Laura僵在床上注视她靠近。Carmilla到达床边，身体缓慢前倾，一只苍白的手缓缓伸向Laura的脸。烛光温暖地照亮两人的面容。

Carmilla（轻柔低语）："Hush. I am here."

镜头3（8-12秒）：@图片2的Laura拼命摇头，眼泪从脸颊滑落，试图向后缩进枕头。@图片1的Carmilla苍白的手停在Laura的脖子旁几英寸处。两人的面孔在画面中清晰可见。

Laura（绝望低语）："No... I beg you... no."

哥特式暗黑韩漫风格，9:16竖屏，烛光卧室
面部稳定不变形、五官清晰、人体结构正常、动作自然流畅、画面无卡顿、无闪烁、不生成字幕、角色外观与参考图一致
```
