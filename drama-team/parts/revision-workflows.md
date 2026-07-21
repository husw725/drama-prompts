# 剧本导入与修订工作流

> 按需读取：用户直接提供好莱坞格式剧本时；收到导演/编剧修订版剧本时。

---

## 好莱坞剧本快速路径（跳过阶段1-2）

> 2026-04-30 Count of Monte Cristo 项目验证。当用户直接提供好莱坞格式剧本（非小说）：

1. 解析 screenplay → 提取 EP 分集 + 场景头(INT./EXT.) + 对白 + Voiceover
2. **从剧本反向初始化状态文件**：提取各集 Cliffhanger/伏笔/角色状态 → continuity.md；visual_continuity.md 从首集分镜起正常累积
3. 并行生成：人物设定 + 视觉资产清单
4. 写分镜（EP1-5 Demo 先做）
5. 写 Prompts（必须包含 Reference 体系）
6. 补 scene_prop_data.json + manifest.md Reference 章节
7. 改造 Prompts 用 `[ref: S-XX]`

**完整执行顺序**：人物 → 视觉资产 → 分镜 → Prompts → **Reference 体系**（场景图+道具图+引用标记）

---

## 导演修订剧本的更新路径

> 2026-04-30 Carmilla 项目验证。当用户发送导演优化后的新剧本，更新已有项目：

1. 读取新剧本（PDF → pymupdf 提取文本 → 保存 .txt，或 DOCX → python-docx 解析）
2. 按 `EPISODE \d+:` 切分 → 提取每集标题/场景/对白
3. **对比新旧**：集名变化？对白变化？新增角色？集数增减？
4. 更新 outline.md 分集梗概（集名映射）
5. 批量更新 script/EP-XX.md
6. 更新 characters.md（如有新角色）
7. 更新 outline.md 三幕结构（如结构变化）+ continuity.md（Cliffhanger/伏笔随剧本变化）
8. 更新 generate_index.py（episode range + 解析器兼容新格式）
9. 运行 generate_index.py + build_html.py 重新生成工作台

**⚠️ 先做 Demo（1-2集）确认风格再批量处理全部**

---

## 剧本修订闭环流程（v2.7+）

当收到编剧修订版时：

1. **版本对比**：按集切分两版，对比标题/字符数/行数/对白数
2. **质量审计**（5项必查）：角色名错误、过度删减(Δ>-20%)、结尾缺失(FADE OUT)、Epilogue独立、修订说明残留
3. **学习编剧修改逻辑**：句式简化方向(长→短)、对话风格一致性(古典vs口语)、格式标准化(CONT'D/FADE OUT)、节奏感知(从删减幅度反向推导)
4. **更新Prompt**：将学到的风格规则写入 TASK.md 的 Style Guide 章节
5. **提意见**：发现不理想修改要指出（关键情感过度简化、高潮戏压缩、角色独特性丢失）

---

## 版本差异量化（v3.1 关键教训，Carmilla v1→v2 踩坑）

- **永远确认"分镜基于哪个剧本版本"** — v1 和 v2 可能完全不同（Carmilla v1 改了 1207 行，v2 只改了 37 行）。分镜如果基于 v1 生成，v2 来了要全部重来。
- **新版本剧本 → 用 `difflib.SequenceMatcher` 自动量化差异量**：

```python
import re, difflib
# 新脚本按集拆分
ep_pattern = re.compile(r'^EPISODE (\d+):', re.MULTILINE)
ep_splits = list(ep_pattern.finditer(new_script))
for i, m in enumerate(ep_splits):
    ep_num = int(m.group(1))
    new_text = new_script[m.start():ep_splits[i+1].start() if i+1 < len(ep_splits) else len(new_script)]
    old_text = open(f'script/EP-{ep_num:02d}.md').read()
    ratio = difflib.SequenceMatcher(None, new_text, old_text).ratio()
    if ratio < 0.7: print(f"EP-{ep_num:02d}: {ratio:.0%} → 需全量重写")
    elif ratio < 0.95: print(f"EP-{ep_num:02d}: {ratio:.0%} → 增量修改")
    else: print(f"EP-{ep_num:02d}: {ratio:.0%} → 无需修改")
```

**经验值**：ratio < 70% → 全量重写分镜+Prompts；70-95% → 增量修改；>95% → 无需改动

- **保留原始剧本**：原始版、v1、v2 全部保留，版本清晰
- **Index 页面数据源跟着剧本版本走**：剧本换了，project_data.json 要重新生成，index.html 要重新 build
- **影响范围判定**：剧本全换 → 分镜全换 → Prompts 全换；角色人设/Manifest/已生成图片可保留
