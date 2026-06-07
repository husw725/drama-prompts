- 角色外观只定义一次 → 全剧一致性
- 每张 frame prompt 省 ~50% token（去掉 80-120 词的角色重复描述）
- 改角色外观只需改一处（`characters.md` 的 `base_prompt`）

**数据模型（`characters.md` 扩展）：**

```markdown
## Carmilla
- **base_prompt**: Gothic Korean manga style, 175cm tall vampire woman, pale skin, shoulder-length black wavy hair, amber eyes, fangs
- **outfits**:
 - **black_dress**: black Victorian gown with silver necklace
 - **white_dress**: white silk evening gown
 - **casual**: dark coat with leather boots
- **expressions**:
 - **fear**: dilated pupils, trembling lips, retreating
 - **seductive**: half-lidded eyes, slight smirk, leaning forward
 - **angry**: narrowed eyes, clenched jaw, glowing amber eyes
```

**Image Prompt 改造（角色部分）：**

```
改前（内嵌完整角色描述）：
Gothic Korean manga style, 9:16 vertical, close-up,
[Carmilla: pale skin, shoulder-length black wavy hair, amber eyes, fangs, black Victorian gown with silver necklace],
scene: [Gothic Victorian bedroom...],
a vampire woman looking in terror...

改后（角色 ref + 服装 + 表情）：
Gothic Korean manga style, 9:16 vertical, close-up,
[ref: C-01], black_dress, fear,
[ref: S-01],
a vampire woman looking in terror...
```

**Image Prompt 新增字段：**

```json
{
 "frame": 1,
 "time": "0-2s 特写",
 "char_refs": ["C-01"],
 "char_outfits": ["C-01:black_dress"],
 "char_expressions": ["C-01:fear"],
 "scene_ref": "S-01",
 "prop_refs": ["P-01"],
 "prompt": "Gothic Korean manga style, 9:16 vertical, close-up, [ref: C-01], black_dress, fear, [ref: S-01], ..."
}
```

**角色 Reference Prompt 写法规则：**
- `base_prompt`：风格 + 体型 + 肤色 + 发型发色 + 瞳色 + 标志性特征（尖牙、疤痕等）
- `outfits`：按剧情阶段命名（如 `prison_uniform`、`evening_gown`），不含角色基本信息
- `expressions`：情绪关键词组合（瞳孔 + 嘴唇 + 姿态）

**执行流程：**
1. 为每个角色写 `base_prompt`（从现有 characters.md 外观描述精简）
2. 梳理全剧服装，按角色归纳为 `outfits` 字典
3. 梳理表情关键词为 `expressions` 字典
4. 批量改造 prompts：`完整角色描述` → `[ref: C-XX], outfit_key, expression_key`
5. 多角色同框：每个角色都用 `[ref: C-XX]` 格式
6. 更新 `build_html.py` 角色 Tab：显示 reference 视图 + 一键复制

> **完整 v2.3 检查清单（扩展）**：
> 6. Prompts 中的角色描述是否已替换为 `[ref: C-XX]` 引用标记？
> 7. 改造后每集的 `[ref: C-XX]` 标记数是否 ≥ 出场角色数 × 帧数？
> 8. `characters.md` 是否含 `base_prompt` / `outfits` / `expressions` 三个字段？

> 💡 **从 Hollywood Screenplay 入手的快速路径**（2026-04-30 Count of Monte Cristo 项目验证）：
> 当用户直接提供好莱坞格式剧本（非小说），跳过阶段1-2，直接：
> 1. 解析 screenplay → 提取 EP 分集 + 场景头(INT./EXT.) + 对白 + Voiceover
> 2. 并行生成：人物设定 + 视觉资产清单（用 delegate_task 各派一个Agent）
> 3. 写分镜（EP1-5 Demo 先做）
> 4. 写 Prompts（必须包含 v2.2 Reference 体系！）
> 5. 补 scene_prop_data.json + manifest.md Reference 章节
> 6. 改造 Prompts 用 `[ref: S-XX]`
> **完整执行顺序**：人物 → 视觉资产 → 分镜 → Prompts → **Reference 体系**（场景图+道具图+引用标记）

> 💡 **导演修订剧本的更新路径**（2026-04-30 Carmilla 项目验证）：
> 当用户发送导演优化后的新剧本，更新已有项目：
> 1. 读取新剧本（PDF → pymupdf 提取文本 → 保存 .txt，或 DOCX → python-docx 解析）
> 2. 按 `EPISODE \d+:` 切分 → 提取每集标题/场景/对白
> 3. **对比新旧**：集名变化？对白变化？新增角色？集数增减？
> 4. 更新 INDEX.md（集名映射）
> 5. 批量更新 script/EP-XX.md
> 6. 更新 characters.md（如有新角色）
> 7. 更新 MASTER.md（如三幕结构变化）
> 8. 更新 generate_index.py（episode range + 解析器兼容新格式）
> 9. 运行 generate_index.py + build_html.py 重新生成工作台
> **⚠️ 先做 Demo（1-2集）确认风格再批量处理全部**
>
> 💡 **剧本修订闭环流程**（v2.7+）：当收到编剧修订版时：
> 1. **版本对比**：按集切分两版，对比标题/字符数/行数/对白数
> 2. **质量审计**（5项必查）：角色名错误、过度删减(Δ>-20%)、结尾缺失(FADE OUT)、Epilogue独立、修订说明残留
> 3. **学习编剧修改逻辑**：句式简化方向(长→短)、对话风格一致性(古典vs口语)、格式标准化(CONT'D/FADE OUT)、节奏感知(从删减幅度反向推导)
> 4. **更新Prompt**：将学到的风格规则写入 TASK.md 的 Style Guide 章节
> 5. **提意见**：发现不理想修改要指出（关键情感过度简化、高潮戏压缩、角色独特性丢失）
>
> ⚠️ **v3.1 关键教训（Carmilla v1→v2 踩坑）**：
> - **永远确认"分镜基于哪个剧本版本"** — v1 和 v2 可能完全不同（Carmilla v1 改了 1207 行，v2 只改了 37 行）。分镜如果基于 v1 生成，v2 来了要全部重来。
> - **新版本剧本 → 用 `difflib.SequenceMatcher` 自动量化差异量**：
> ```python
> import re, difflib
> # 新脚本按集拆分
> ep_pattern = re.compile(r'^EPISODE (\d+):', re.MULTILINE)
> ep_splits = list(ep_pattern.finditer(new_script))
> for i, m in enumerate(ep_splits):
> ep_num = int(m.group(1))
> new_text = new_script[m.start():ep_splits[i+1].start() if i+1 < len(ep_splits) else len(new_script)]
> old_text = open(f'script/EP-{ep_num:02d}.md').read()
> ratio = difflib.SequenceMatcher(None, new_text, old_text).ratio()
> if ratio < 0.7: print(f"EP-{ep_num:02d}: {ratio:.0%} → 需全量重写")
> elif ratio < 0.95: print(f"EP-{ep_num:02d}: {ratio:.0%} → 增量修改")
> else: print(f"EP-{ep_num:02d}: {ratio:.0%} → 无需修改")
> ```
> **经验值**：ratio < 70% → 全量重写分镜+Prompts；70-95% → 增量修改；>95% → 无需改动
> - **保留原始剧本**：`carmilla_full_text.txt`（原始）、`carmilla_modified.txt`（v1）、`carmilla_revised_v2.txt`（v2）都要保留，版本清晰。
> - **Index 页面数据源跟着剧本版本走**：剧本换了，project_data.json 要重新生成，index.html 要重新 build。
> - **影响范围判定**：剧本全换 → 分镜全换 → Prompts 全换；角色人设/Manifest/已生成图片可保留。

## 审核员系统（三视角定性 + 三Aligner定量）