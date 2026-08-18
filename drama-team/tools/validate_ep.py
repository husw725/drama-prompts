#!/usr/bin/env python3
"""drama-team 单集验证器 — 宿主无关(仅依赖 python3 stdlib)。

把散落在技能文档里的机械检查收敛为一条命令:
    python3 tools/validate_ep.py EP-05 [--project /path/to/project]

全项目文件完整性(批量生成后/工作台前):
    python3 tools/validate_ep.py --all [--project /path/to/project]

检查项(机器可测的全部硬规则):
  script/     ⚓锚点完整 | 时长≈ep_duration±5 | 对白10-20句且英文且≤12词/句 | Cliffhanger钩子等级标注
  storyboard/ ⚓锚点 | 单镜≤5s | 总时长 | 特写/近景≥50%,全景/中景≤30% | 🟢≥60%,🟡≤2须有理由,🔴≤1 | 视觉衔接声明
  prompts/    ⚓锚点 | 帧数=分镜镜头数 | 每帧含[ref:] | 风格词漂移
  continuity  伏笔状态机(到期/逾期告警) | 本集已登记 | visual_continuity 快照已更新
  评分趋势     连续3集总分≥90 → 膨胀告警(读各集内联审核报告的"总分: XX/100"行)

退出码: 0=无FAIL, 1=有FAIL(不得进入下一集)。创意维度不在此审——那是 Aligner 的事。
"""
import argparse, glob, os, re, sys

FAIL, WARN, OK = "🔴 FAIL", "🟡 WARN", "🟢 OK"
results = []

def report(level, check, msg):
    results.append((level, check, msg))

def read(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except OSError:
        return None

def parse_ts(tok):
    """'0:03'→3, '1:25'→85, '3s'/'3'→3"""
    tok = tok.strip().rstrip("s")
    if ":" in tok:
        m, s = tok.split(":", 1)
        return int(m) * 60 + int(s)
    return float(tok)

def parse_range(cell):
    """'0:00-0:03' / '0-3s' / '3-7s' → (start, end);解析失败返回 None"""
    m = re.match(r"^\s*([\d:.]+s?)\s*[-–~]\s*([\d:.]+s?)\s*$", cell.strip())
    if not m:
        return None
    try:
        a, b = parse_ts(m.group(1)), parse_ts(m.group(2))
        return (a, b) if b >= a else None
    except ValueError:
        return None

def table_rows(section):
    """markdown 表格数据行(首列为数字的行)→ [cells...]"""
    rows = []
    for line in section.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells and re.match(r"^\d+$", cells[0]):
            rows.append(cells)
    return rows

def section_of(text, header):
    m = re.search(rf"^##\s*{re.escape(header)}.*?$(.*?)(?=^##\s|\Z)", text, re.M | re.S)
    return m.group(1) if m else None

def cjk_ratio(s):
    cjk = len(re.findall(r"[一-鿿]", s))
    letters = len(re.findall(r"[A-Za-z一-鿿]", s))
    return cjk / letters if letters else 0.0


def check_script(path, ep_duration):
    text = read(path)
    if text is None:
        report(FAIL, "script", f"{path} 不存在")
        return
    for anchor in ["Scene Breakdown", "Key Dialogue", "Cliffhanger"]:
        if f"## {anchor}" not in text:
            report(FAIL, "script/锚点", f"缺 ⚓ `## {anchor}`(工作台解析将静默丢数据)")
    # 时长
    sb = section_of(text, "Scene Breakdown")
    if sb:
        total, bad = 0.0, 0
        for cells in table_rows(sb):
            r = parse_range(cells[1]) if len(cells) > 1 else None
            if r:
                total += r[1] - r[0]
            else:
                bad += 1
        if bad:
            report(WARN, "script/时长", f"{bad} 行时间列无法解析,时长合计不完整")
        if total and abs(total - ep_duration) > 5:
            report(FAIL, "script/时长", f"合计 {total:.0f}s vs ep_duration {ep_duration}s(容差±5)")
        elif total:
            report(OK, "script/时长", f"{total:.0f}s ≈ {ep_duration}s")
    # 对白
    kd = section_of(text, "Key Dialogue")
    if kd:
        rows = table_rows(kd)
        n = len(rows)
        if not 10 <= n <= 20:
            report(WARN, "script/对白", f"{n} 句(软区间 10-20,按集类型浮动)")
        else:
            report(OK, "script/对白", f"{n} 句")
        zh = [r for r in rows if len(r) > 2 and cjk_ratio(r[2]) > 0.3]
        if zh:
            report(FAIL, "script/对白英文", f"{len(zh)} 句台词为中文——对白必须英文直写(禁止中文→翻译)")
        long_lines = [r[0] for r in rows if len(r) > 2 and len(re.findall(r"[A-Za-z']+", r[2])) > 12]
        if long_lines:
            report(WARN, "script/对白长度", f"{len(long_lines)} 句 >12 words(#{','.join(long_lines)})——竖屏对白短促")
    # Cliffhanger 钩子等级标注
    cf = section_of(text, "Cliffhanger")
    if cf and not re.search(r"[（(]\s*\d+\s*[)）]", cf):
        report(FAIL, "script/钩子标注", "Cliffhanger 无钩子类型+等级标注,如 `不可逆(7)`(Aligner 扣3分项)")


def check_storyboard(path, ep_duration):
    text = read(path)
    if text is None:
        report(WARN, "storyboard", f"{path} 不存在(尚未到阶段5则忽略)")
        return False
    if "## Key Frames" not in text:
        report(FAIL, "storyboard/锚点", "缺 ⚓ `## Key Frames`")
    if "## 视觉衔接" not in text:
        report(FAIL, "storyboard/视觉衔接", "缺 `## 视觉衔接` 声明(承接上集结尾)")
    kf = section_of(text, "Key Frames")
    if not kf:
        return True
    rows = table_rows(kf)
    total, over5, closeup, wide, unknown_shot = 0.0, 0, 0, 0, 0
    tiers = {"🟢": 0, "🟡": 0, "🔴": 0, "none": 0}
    for cells in rows:
        r = parse_range(cells[1]) if len(cells) > 1 else None
        if r:
            dur = r[1] - r[0]
            total += dur
            if dur > 5:
                over5 += 1
        shot = cells[2] if len(cells) > 2 else ""
        if re.search(r"特写|近景", shot):
            closeup += 1
        elif re.search(r"全景|中景|远景", shot):
            wide += 1
        else:
            unknown_shot += 1
        cam = cells[3] if len(cells) > 3 else ""
        for t in ("🟢", "🟡", "🔴"):
            if t in cam:
                tiers[t] += 1
                break
        else:
            tiers["none"] += 1
    n = len(rows)
    if not n:
        report(FAIL, "storyboard/表格", "Key Frames 无有效数据行")
        return True
    if over5:
        report(FAIL, "storyboard/单镜", f"{over5} 个镜头 >5s(单镜≤5s 无例外)")
    if total and abs(total - ep_duration) > 5:
        report(FAIL, "storyboard/时长", f"合计 {total:.0f}s vs {ep_duration}s")
    if closeup / n < 0.5:
        report(FAIL, "storyboard/景别", f"特写/近景 {closeup}/{n}={closeup/n:.0%} <50%(竖屏铁律)")
    if wide / n > 0.3:
        report(FAIL, "storyboard/景别", f"全景/中景 {wide}/{n}={wide/n:.0%} >30%")
    if unknown_shot:
        report(WARN, "storyboard/景别", f"{unknown_shot} 行 Shot 列无法归类")
    if tiers["none"]:
        report(FAIL, "storyboard/运镜分级", f"{tiers['none']} 个镜头 Camera 列无 🟢/🟡/🔴 标注")
    if tiers["🟡"] > 2:
        report(FAIL, "storyboard/运镜", f"🟡 运镜 {tiers['🟡']} 个 >2(炫技防控)")
    if tiers["🔴"] > 1:
        report(FAIL, "storyboard/运镜", f"🔴 运镜 {tiers['🔴']} 个 >1")
    graded = n - tiers["none"]
    if graded and tiers["🟢"] / graded < 0.6:
        report(WARN, "storyboard/运镜", f"🟢 占比 {tiers['🟢']}/{graded}={tiers['🟢']/graded:.0%} <60%")
    if tiers["🟡"] and "🟡运镜理由" not in text:
        report(FAIL, "storyboard/运镜理由", "有 🟡 运镜但 Shot Notes 无「🟡运镜理由」——无理由=炫技")
    report(OK, "storyboard", f"{n} 镜 / {total:.0f}s / 特写近景 {closeup/n:.0%} / 🟢{tiers['🟢']} 🟡{tiers['🟡']} 🔴{tiers['🔴']}")
    return True


def check_prompts(path, storyboard_exists, sb_path):
    text = read(path)
    if text is None:
        report(WARN, "prompts", f"{path} 不存在(尚未到阶段6则忽略)")
        return
    if "## Visual Asset References" not in text:
        report(FAIL, "prompts/锚点", "缺 ⚓ `## Visual Asset References`")
    frames = re.findall(r"^### Frame \d+:.*?\n\*\*Prompt:\*\*\s*(.+?)(?=^###|\Z)", text, re.M | re.S)
    if not frames:
        report(FAIL, "prompts/帧", "未找到 `### Frame N:` + `**Prompt:**` 结构")
        return
    if storyboard_exists:
        sb_text = read(sb_path) or ""
        kf = section_of(sb_text, "Key Frames")
        n_shots = len(table_rows(kf)) if kf else 0
        if n_shots and len(frames) != n_shots:
            report(WARN, "prompts/帧数", f"帧数 {len(frames)} ≠ 分镜镜头数 {n_shots}(应一一对应)")
    noref = sum(1 for f in frames if "[ref:" not in f)
    if noref:
        report(FAIL, "prompts/ref注入", f"{noref}/{len(frames)} 帧缺 [ref: C-XX/S-XX] 引用")
    styles = {f.strip().split(",")[0].strip() for f in frames if f.strip()}
    if len(styles) > 1:
        report(FAIL, "prompts/风格漂移", f"帧首风格词不一致: {sorted(styles)[:4]}")
    else:
        report(OK, "prompts", f"{len(frames)} 帧 / 风格词统一 / ref 注入完整")


def check_continuity(project, ep_num, storyboard_exists):
    text = read(os.path.join(project, "continuity.md"))
    if text is None:
        report(WARN, "continuity", "continuity.md 不存在(阶段1前可忽略)")
        return
    pattern = r"\|\s*(F-\d+)\s*\|\s*([^|]+)\|\s*EP-(\d+)\s*\|\s*EP-(\d+)\s*\|\s*(🟡|🔵|✅|⏳|❌)"
    for fid, desc, _, due, status in re.findall(pattern, text):
        due = int(due)
        desc = desc.strip()
        if status == "⏳":
            overdue = ep_num - due
            level = FAIL if overdue >= 3 else WARN
            report(level, "continuity/伏笔", f"{fid} 已逾期{overdue}集: {desc}" + ("(逾期≥3集,Aligner扣5分)" if overdue >= 3 else ""))
        elif status == "🟡" and due == ep_num:
            report(WARN, "continuity/伏笔", f"{fid} 本集到期,必须回收: {desc}")
        elif status == "🟡" and due == ep_num + 1:
            report(WARN, "continuity/伏笔", f"{fid} 下集到期: {desc}")
    ep_tag = f"EP-{ep_num:02d}"
    progress = section_of(text, "当前进度") or ""
    has_cliff = re.search(rf"###\s*{ep_tag}\s*结尾", text)
    if ep_tag not in progress and not has_cliff:
        report(FAIL, "continuity/更新", f"continuity.md 的「当前进度」与「Last Cliffhanger」均无 {ep_tag}——核心三项每集必更(伏笔表里预登记的集数不算)")
    if storyboard_exists:
        vc = read(os.path.join(project, "visual_continuity.md"))
        if vc is None or f"EP-{ep_num:02d}" not in vc:
            report(FAIL, "visual_continuity", f"分镜已存在但 visual_continuity.md 无 EP-{ep_num:02d} 结尾快照——每集分镜完成后必须立即更新")


def check_score_trend(project):
    scores = []
    files = sorted(glob.glob(os.path.join(project, "script", "EP-*.md")))
    for f in files:
        text = read(f) or ""
        m = re.findall(r"总分[:：]\s*\**\s*(\d+)\s*/\s*100", text)
        if m:
            scores.append((os.path.basename(f), int(m[-1])))
    if len(files) >= 3 and not scores:
        report(WARN, "评分趋势", f"{len(files)} 集剧本均无「总分: XX/100」行——膨胀趋势检测失效,审核报告请内联总分行")
    if len(scores) >= 3 and all(s >= 90 for _, s in scores[-3:]):
        report(WARN, "评分膨胀", f"连续3集总分≥90({scores[-3:]})——按 reviewers-scoring 自检规则,人工抽检最近一集")


def check_all(project):
    """全项目三件套完整性(批量生成后必跑)。以 script/ 集数为基准。"""
    script_eps = [int(m.group(1)) for f in glob.glob(os.path.join(project, "script", "EP-*.md"))
                  if (m := re.search(r"EP-(\d+)", os.path.basename(f)))]
    if not script_eps:
        report(FAIL, "all/script", "script/ 下没有任何 EP-*.md")
        return
    total = max(script_eps)
    for sub in ("script", "storyboard", "prompts"):
        if sub != "script" and not glob.glob(os.path.join(project, sub, "EP-*.md")):
            report(WARN, f"all/{sub}", "目录为空(未到该阶段则忽略)")
            continue
        for i in range(1, total + 1):
            fp = os.path.join(project, sub, f"EP-{i:02d}.md")
            if not os.path.exists(fp):
                report(FAIL, "all/缺失", f"{sub}/EP-{i:02d}.md 不存在")
            elif os.path.getsize(fp) < 500:
                report(WARN, "all/疑似空文件", f"{sub}/EP-{i:02d}.md <500 bytes")
    report(OK, "all", f"以 script/ 最大集 EP-{total:02d} 为基准查完三件套")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ep", nargs="?", help="EP-05 或 5")
    ap.add_argument("--all", action="store_true", help="全项目三件套完整性检查(批量生成后)")
    ap.add_argument("--project", default=".", help="项目根目录(默认当前目录)")
    args = ap.parse_args()
    if args.all:
        check_all(args.project)
        print(f"\n=== 全项目完整性报告 ===")
        for level, check, msg in results:
            print(f"{level} [{check}] {msg}")
        fails = sum(1 for l, _, _ in results if l == FAIL)
        print(f"\n结果: {fails} FAIL → {'❌ 补齐后重跑' if fails else '✅ 三件套完整'}")
        sys.exit(1 if fails else 0)
    if not args.ep:
        ap.error("需要 EP 参数或 --all")
    ep_num = int(re.sub(r"\D", "", args.ep))
    ep = f"EP-{ep_num:02d}"
    project = args.project

    outline = read(os.path.join(project, "outline.md")) or ""
    m = re.search(r"ep_duration[^\d]*(\d+)", outline)
    ep_duration = int(m.group(1)) if m else 90

    sb_path = os.path.join(project, "storyboard", f"{ep}.md")
    check_script(os.path.join(project, "script", f"{ep}.md"), ep_duration)
    sb_exists = check_storyboard(sb_path, ep_duration)
    check_prompts(os.path.join(project, "prompts", f"{ep}.md"), sb_exists, sb_path)
    check_continuity(project, ep_num, sb_exists)
    check_score_trend(project)

    print(f"\n=== {ep} 验证报告(ep_duration={ep_duration}s)===")
    for level, check, msg in results:
        print(f"{level} [{check}] {msg}")
    fails = sum(1 for l, _, _ in results if l == FAIL)
    warns = sum(1 for l, _, _ in results if l == WARN)
    print(f"\n结果: {fails} FAIL / {warns} WARN → {'❌ 不得进入下一集' if fails else '✅ 可进入下一集'}")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
