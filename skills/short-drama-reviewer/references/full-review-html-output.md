# Full Review HTML Output — Interactive Multi-Reporter Format

> **Trigger**: User asks for a screenplay/script review and wants results delivered as a self-contained HTML file (not Markdown or plain text).

## Why HTML over Markdown

- User explicitly requested HTML output for Carmilla review (2026-05-14)
- Interactive tab navigation for 4+ reviewers is impractical in plain Markdown
- Dark theme matches Drama Studio aesthetic
- Single file, zero dependencies, opens in any browser
- User requested both Chinese and English versions of the same report

## Structure

```
HTML Report (single file, ~60KB)
├── Sticky nav bar with tab buttons
├── Tab 1: Overview (scores at a glance, per-episode timeline, core issues table)
├── Tab 2: Impatient Bro (pacing, retention, per-episode diagnosis)
├── Tab 3: Logic Master (rule consistency, plot holes, continuity check)
├── Tab 4: Visual Expert (production feasibility, commercial analysis)
├── Tab 5: Aligner (130-point quantitative scoring, PASS/FAIL)
└── Tab 6: Action Items (🔴🟡🟢 prioritized combined recommendations)
```

## Key Design Decisions

1. **Sticky nav bar** with `position: sticky; top: 0` — stays visible when scrolling
2. **Tab switching via vanilla JS** — no framework, single-file
3. **Color-coded timeline** — green/yellow/red per-episode rating bars
4. **Diagnosis cards** with `.diagnosis` class: time/location → emotion → quote → problem → suggestion
5. **Continuity breaks** highlighted with `.continuity-break` gradient background
6. **Priority items** numbered/lettered with consensus attribution (which reviewers flagged it)
7. **Score bars** with percentage-based width for Aligner scoring
8. **Consensus matrix table** at the end — which reviewer flagged which issue

## Reviewer Combination (4-reviewer model)

| Reviewer | Source | Focus |
|----------|--------|-------|
| Impatient Bro | short-drama-reviewer skill | Pacing, retention, hooks, swipe-away points |
| Logic Master | short-drama-reviewer skill | Rule consistency, timeline, plot holes |
| Visual Expert | short-drama-reviewer skill | Production feasibility, AI video risks, commercial value |
| Aligner v5.1 | drama-team skill (hermes-short-drama-team) | 130-point quantitative scoring, PASS/FAIL gate |

## Output Convention

- Save to `/home/husw/.hermes/cache/review-<PROJECT-NAME>.html`
- Copy to desktop: `/mnt/c/Users/melot/Desktop/<PROJECT_NAME>_Review.html`
- English version suffix: `_<PROJECT_NAME>_Review_EN.html`
- Send via Feishu + desktop copy

## CSS Variables (dark theme)

```css
--bg: #0d0d12;
--card: #16161e;
--card2: #1c1c26;
--border: #2a2a3a;
--text: #d4d4dc;
--text-dim: #8888a0;
--accent-red: #ff4d6a;
--accent-yellow: #ffb84d;
--accent-green: #4dff91;
--impatient: #ff6b6b;
--logic: #60a5fa;
--visual: #a78bfa;
--aligner: #34d399;
```

## When to Use

- Full screenplay review (10+ episodes)
- User explicitly asks for HTML format
- Multi-reviewer reports where tab navigation improves readability

## When NOT to Use

- Single-episode quick review → plain Markdown is sufficient
- User asks for specific format (PDF, Markdown, etc.)
- Review is purely Aligner quantitative (no multi-perspective needed)
