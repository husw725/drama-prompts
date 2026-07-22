#!/usr/bin/env python3
"""validate_ep.py 冒烟测试:合规集应 exit 0,违规集应抓到全部埋点。
运行: python3 tools/test_validate_ep.py
"""
import os, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
NL = "\n"


def write(root, rel, content):
    path = os.path.join(root, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def build_project(root):
    write(root, "outline.md", "## 类型DNA\n- **单集时长 (ep_duration)**: 90s\n")
    write(root, "continuity.md", """## 当前进度
- **已完成**: EP-01
## 伏笔管理
| ID | 描述 | 埋入集 | 计划回收集 | 状态 | 备注 |
|----|------|--------|-----------|------|------|
| F-01 | 咬痕 | EP-01 | EP-02 | 🟡待回收 | |
| F-09 | 旧账 | EP-01 | EP-01 | ⏳逾期 | |
### EP-01 结尾
- **Hook**: 不可逆(7)
""")
    write(root, "visual_continuity.md", "## EP-01 结尾视觉快照\n- 色调: 冷蓝\n")
    # EP-01 合规:18镜×5s,12句英文对白,特写≥50%,🟡1个有理由
    sc, sb, t = [], [], 0
    for i in range(18):
        shot = "特写" if i % 10 < 6 else ("近景" if i % 10 < 7 else "中景")
        cam = "handheld 🟡" if i == 5 else "static 🟢"
        sb.append(f"| {i+1} | {t}-{t+5}s | {shot} | {cam} | a | 深夜 | 冷白 | 雷 |")
        sc.append(f"| {i+1} | {t}-{t+5}s | 老宅 | a | — |")
        t += 5
    kd = NL.join(f'| {i+1} | Laura | "You lied to me, Damien." | 指控 |' for i in range(12))
    write(root, "script/EP-01.md", f"""# EP-01
## Scene Breakdown ⚓
| # | 时间 | 场景 | 画面/动作 | 对白/VO |
|---|---|---|---|---|
{NL.join(sc)}
## Key Dialogue ⚓
| # | 角色 | 台词 | 潜台词 |
|---|---|---|---|
{kd}
## Cliffhanger ⚓
- **Hook**: 不可逆(7)
**总分: 85/100**
""")
    write(root, "storyboard/EP-01.md", f"""# EP-01
## 视觉衔接
无——首集
## Key Frames ⚓
| # | Time | Shot | Camera | D | A | L | S |
|---|---|---|---|---|---|---|---|
{NL.join(sb)}
## Shot Notes
- **🟡运镜理由**: #6 追逐需不稳定感
""")
    frames = NL.join(
        f"### Frame {i+1}: {i*5}-{i*5+5}s 特写{NL}**Prompt:** Gothic style, 9:16, [ref: C-01]{NL}"
        for i in range(18))
    write(root, "prompts/EP-01.md", f"# EP-01\n## Visual Asset References\n**L**: x\n{frames}")
    # EP-02 违规:超时长/中文对白/无钩子标注/🟡x3无理由/全景超标/快照未更新/风格漂移/缺ref
    rows = NL.join(f"| {i+1} | {i*10}-{i*10+10}s | 老宅 | a | 台词 |" for i in range(10))
    kd2 = NL.join(f'| {i+1} | L | "你骗了我这么多年" | x |' for i in range(8))
    write(root, "script/EP-02.md", f"""# EP-02
## Scene Breakdown ⚓
| # | 时间 | 场景 | 画面/动作 | 对白/VO |
|---|---|---|---|---|
{rows}
## Key Dialogue ⚓
| # | 角色 | 台词 | 潜台词 |
|---|---|---|---|
{kd2}
## Cliffhanger ⚓
- 没标类型等级
""")
    sb2 = NL.join(
        f"| {i+1} | {i*10}-{i*10+10}s | {'全景' if i < 5 else '特写'} | {'orbit 🟡' if i < 3 else 'static 🟢'} | a | 夜 | 冷 | 雷 |"
        for i in range(10))
    write(root, "storyboard/EP-02.md", f"""# EP-02
## Key Frames ⚓
| # | Time | Shot | Camera | D | A | L | S |
|---|---|---|---|---|---|---|---|
{sb2}
## Shot Notes
- 没写理由
""")
    write(root, "prompts/EP-02.md", """# EP-02
### Frame 1: 0-10s 全景
**Prompt:** Gothic style, no ref
### Frame 2: 10-20s 全景
**Prompt:** Bright anime style, [ref: C-01]
""")


def run(root, ep):
    p = subprocess.run([sys.executable, os.path.join(HERE, "validate_ep.py"), ep, "--project", root],
                       capture_output=True, text=True)
    return p.returncode, p.stdout


def main():
    with tempfile.TemporaryDirectory() as root:
        build_project(root)
        code, out = run(root, "EP-01")
        assert code == 0, f"合规集应通过:\n{out}"
        assert "F-01 下集到期" in out, out
        code, out = run(root, "EP-02")
        assert code == 1, "违规集应 FAIL"
        for expected in ["script/时长", "对白英文", "钩子标注", "视觉衔接", "单镜",
                         "storyboard/景别", "运镜理由", "ref注入", "风格漂移",
                         "visual_continuity", "continuity/更新", "F-09 已逾期"]:
            assert expected in out, f"漏检 [{expected}]:\n{out}"
        n_yellow = out.count("🟡 运镜 3 个")
        assert n_yellow == 1, out
    print("validate_ep 冒烟测试: PASS(合规集放行,违规集12类埋点全部抓到)")


if __name__ == "__main__":
    main()
