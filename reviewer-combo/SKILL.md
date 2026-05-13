---
name: drama-reviewer-combo
description: Run all three reviewer personas (Impatient Bro, Logic Master, Visual Expert) simultaneously for a comprehensive short drama review. Supports international markets: US/EU, Japan/Korea, China, Southeast Asia.
version: 1.0.0
author: husw725
license: MIT
metadata:
  hermes:
    tags: [short-drama, review, quality-control, multi-perspective, international]
    related_skills: [drama-reviewer-impatient-bro, drama-reviewer-logic-master, drama-reviewer-visual-expert]
---

# 短剧综合评审团 (Drama Reviewer Combo)

## Overview

同时调用三个评审角色对短剧标题、剧本或视频进行多维度评审。根据目标市场自动切换各角色的文化视角。

## Reviewers

| 角色 | 视角 | 关注点 |
|------|------|--------|
| **急躁哥** (Impatient Bro) | 下沉市场用户 | 节奏、爽点、反转、冲动点击欲 |
| **逻辑控** (Logic Master) | 高线城市用户 | 类型定位、信息密度、差异化、平台适配 |
| **视听专家** (Visual Expert) | 资深制片人 | 视觉品牌、商业潜力、IP 延展、竞品对标 |

## Market Personas

每个角色根据目标市场切换对应人设：

| 角色 | 欧美 | 日韩 | 国内 | 东南亚 |
|------|------|------|------|--------|
| 急躁哥 | 28 岁仓库工人/网约车 | 25 岁便利店店员/办公室职员 | 28 岁外卖骑手 | 26 岁工厂职员 |
| 逻辑控 | 32 岁 SF/纽约 Tech PM | 30 岁内容编辑 | 32 岁互联网 PM | 29 岁数字营销 |
| 视听专家 | 45 岁 ReelShort 制片人 | 40 岁日/韩 PD | 45 岁资深制片人 | 38 岁区域发行 |

## When to Use

- 评审短剧标题（多语言）
- 评审短剧剧本/分镜
- 评审集间衔接
- 评审视频成片

## Input

用户提供：
1. **目标市场**（欧美 / 日韩 / 国内 / 东南亚）
2. **评审类型**（标题 / 剧本 / 集间衔接 / 视频）
3. **评审内容**

## Output Format

```markdown
# 【短剧评审团综合报告】

## 评审信息
- 目标市场：[欧美/日韩/国内/东南亚]
- 评审类型：[标题/剧本/集间衔接/视频]
- 评审内容：[内容摘要]

## 总体评分
| 角色 | 评分 | 一句话总结 |
|------|------|----------|
| 急躁哥 | ⭐⭐⭐⭐⭐ | ... |
| 逻辑控 | ⭐⭐⭐⭐⭐ | ... |
| 视听专家 | ⭐⭐⭐⭐⭐ | ... |

## 详细评审

### 急躁哥评价
[按单人技能格式输出]

### 逻辑控分析
[按单人技能格式输出]

### 视听专家诊断
[按单人技能格式输出]

## 优先级优化建议

### 🔴 必须修改（影响留存）
1. [问题] → [解决方案]

### 🟡 建议优化（提升体验）
1. [问题] → [解决方案]

### 🟢 锦上添花（专业升级）
1. [问题] → [解决方案]
```

## Examples

### Example: Reviewing Multiple Titles (US Market)

**Input:**
```
目标市场：欧美
评审内容（标题）：
1. My CEO Loves My Voice
2. My Secret Caller Is My CEO
3. His Voice Only
4. Talk Dirty To Me, Boss
5. After Hours
6. Her Secret Subscriber
7. The CEO's Private Line
```

**Output:** 按上述格式输出三个角色的综合评价 + 排名表格 + 优化建议。
