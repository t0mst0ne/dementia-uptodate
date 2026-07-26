# CLAUDE.md — Dementia & Alzheimer's Weekly Report

## Project Purpose

Auto-generate weekly Markdown reports on dementia and Alzheimer's disease trends from:
- OpenEvidence MCP (`mcp__openevidence__oe_ask`)
- UpToDate MCP (`mcp__uptodate__uptodate_search`)
- CrossRef API — neurology/dementia journals (via `uv run python main.py journals`)
- Web news — Alzforum, NeurologyToday, Alzheimer's Association, CTAD/AAIC, and
  NEJM/JAMA Neurology via Google News RSS (via `uv run python main.py scrape`)

---

## Before Writing a New Report

**MANDATORY — do this BEFORE writing a single word of content:**

```bash
# 1. Find the latest report
PREV=$(ls reports/ -t | head -1)
echo "Previous report: $PREV"

# 2. Read it fully — note every trial, drug approval, and section topic covered
# 3. Grep key trial names to see what's already documented
grep -E "CLARITY AD|TRAILBLAZER|AHEAD|DIAN-TU|GRADUATE|evoke|SKYLINE|PrevenTRON|LiBBY|PROTECT-Cog" reports/$PREV
```

After reading the previous report, answer these before writing:
- Which trials were already covered with final/mature data? → **skip entirely**
- Which trials had interim data last week? → include only if new follow-up published
- Which drug approvals were already documented? → **skip unless label expanded**

**Do NOT repeat** any finding with identical numbers. Mark new follow-up data explicitly: `[更新]` before the subsection heading, and state what changed vs last week.

If a section has no genuinely new data this week: write `_本週無新訊號_` and move on.

---

## Report File Naming

```
reports/YYYY-WNN.md
```

Use ISO week number: `python3 -c "from datetime import date; d=date.today(); print(f'{d.year}-W{d.isocalendar()[1]:02d}')"`.

The GitHub Action runs on UTC. Triggering it manually while UTC is still Sunday
produces a file for the *previous* ISO week that duplicates the current one — only
the Monday 00:00 UTC schedule lands on the intended week.

---

## Report Structure

### Required Sections (繁體中文)

```
# 失智症治療趨勢週報 — YYYY-WNN

> 生成日期：YYYY-MM-DD｜資料來源：...
> 涵蓋期間：...

---

## 摘要
（本週五大訊號 — bullet points, concrete numbers）

## 一、抗類澱粉單株抗體（lecanemab / donanemab / trontinemab）
## 二、血液生物標記（p-tau217、p-tau181、GFAP、NfL）
## 三、影像與 CSF 診斷（amyloid PET、tau PET、CSF）
## 四、新機轉與非類澱粉標靶（tau、neuroinflammation、GLP-1）
## 五、症狀治療與 BPSD（膽鹼酯酶抑制劑、memantine、agitation）
## 六、風險因子與預防（血壓、聽力、運動、疫苗）
## 七、非阿茲海默型失智症（LBD、FTD、血管性、混合型）
## 八、照護體系與流行病學
## 九、進行中高優先試驗追蹤
## 十、台灣臨床情境備註
## 十一、本週 Key Takeaways

## 十二、蜥蜴LLM 點評
（OpenEvidence分類：practice-changing vs hypothesis-generating）

## 十三、媒體動態
（Alzforum / NeurologyToday / Alzheimer's Association / CTAD-AAIC news table）

## 文獻速報 — CrossRef 期刊
（LLM-filtered neurology journal articles）
```

Sections without new data this week should say: `_本週無新訊號_`

---

## Writing Style

- Language: **繁體中文**，英文術語保留原文（amyloid, tau, ARIA-E, CDR-SB, MMSE 等）
- Every clinical claim must cite trial name + author + journal + DOI
- Tables: use Markdown tables for comparative data (treatment vs placebo arm)
- Numbers: always include HR, CI, p-value when available. For cognitive endpoints
  report the between-group difference on CDR-SB / ADAS-Cog / ADCS-ADL, not just
  "slowed decline". For anti-amyloid agents always state ARIA-E and ARIA-H rates.
- Avoid vague superlatives; every "significant" needs a number

---

## Data Pipeline

Run in order before writing:

```bash
uv run python main.py scrape          # web news, last 7 days
uv run python main.py journals        # CrossRef neurology journals, last 14 days
```

Full pipeline (scrape + journals + write the source report):

```bash
uv run python main.py run
```

Notify Telegram about the latest report (needs `TELEGRAM_BOT_TOKEN` /
`TELEGRAM_CHAT_ID`; silently skipped when unset):

```bash
uv run python main.py notify
```

Cached data locations:
- `data/webscrape_cache.json` — web news articles
- `data/journals_cache.json` — CrossRef journal articles (pre-screened, not yet final-filtered)

### Filtering gotchas (learned the hard way)

**Keyword matching is word-boundary anchored, not substring.** Short abbreviations
in `source/keywords.yml` (`AD`, `tau`, `MCI`, `NIA`) would otherwise match inside
unrelated words — `AD` hits "r*ad*iotherapy", `tau` hits "pla*tau*". Use
`config.match_keywords()` / `config.keyword_pattern()`; never write `kw in text`.

**The CrossRef pre-screen is a two-tier filter** (`src/crossref_fetcher.py`).
Tier 1 terms (`dementia`, `Alzheimer`, `lecanemab`, `p-tau217`, …) pass on their
own; Tier 2 terms (`amyloid`, `tau`, `biomarker`, `cognition`) never do, because
they also appear in cardiac amyloidosis and oncology papers.

**Still filter in-session.** The Python pre-screen is a broad net. When writing the
report, read `data/journals_cache.json` and discard any article whose primary topic
is not dementia. Only include confirmed-relevant articles in `## 文獻速報`.

---

## 蜥蜴LLM 點評 Section

Use `mcp__openevidence__oe_ask` with a prompt like:

```
Based on the following dementia findings from this week, classify each as:
- Practice-changing (changes standard of care NOW)
- Hypothesis-generating (promising but needs confirmation)
- Context-dependent (changes practice for specific subgroup only)

[list findings with trial names and key numbers]
```

Extract result with: `result.extracted_answer_raw`

---

## After Writing

1. Check word count: report should be 3000–8000 words
2. Verify every table has header separators (`|---|---|`)
3. Commit: `git add reports/YYYY-WNN.md && git commit -m "report: YYYY-WNN"`
4. Push → GitHub Action auto-publishes to Wiki and notifies Telegram

---

## Duplicate-Avoidance Checklist

Before finalising, cross-check against the previous report:

```bash
PREV=$(ls reports/ -t | head -2 | tail -1)
# Check trial names
grep -E "CLARITY AD|TRAILBLAZER|AHEAD|DIAN-TU|GRADUATE|evoke|SKYLINE|PrevenTRON" reports/$PREV
# Check effect sizes — if same numbers appear, it's a repeat
grep -E "HR [0-9]|CDR-SB [0-9]|ADAS-Cog [0-9]|ARIA-E [0-9]" reports/$PREV | head -20
```

Rules:
- Same trial + same numbers → **delete the section**
- Same trial + new data (updated follow-up, subgroup, approval) → keep with `[更新]` tag
- Brand new trial → include normally

---

## Switching to Another Topic

Sources live in `source/` (`keywords.yml`, `web_sources.yml`, `journals.yml`) and
need no code changes. The Tier-1/Tier-2 term lists in `src/crossref_fetcher.py` are
topic-specific and **must** be updated too — a stale list silently passes the wrong
specialty's papers. See `README.md` for the step-by-step walkthrough.
