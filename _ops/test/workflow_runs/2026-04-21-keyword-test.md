# Keyword Researcher — Test Run 2026-04-21

## Verification Checklist

- [x] Step 1: reads `D:/ai-verse/_ops/data/keyword_matrix.json` via `read_file`
- [x] Step 1: selects topic with lowest coverage count (AI Model Releases — 0 history entries, priority 1 tier 1)
- [ ] Step 1: if AI in Verticals selected, picks least-covered vertical — not triggered this run
- [x] Step 2: uses `keywords[]` from matrix as seed starting point (4 matrix seeds + 6 self-generated)
- [x] Step 7: reads then writes `D:/ai-verse/_ops/data/keyword_history.json`
- [x] Output contains `KEYWORD_RESEARCH_JSON` marker
- [ ] `target_audience` uses new values: watcher / investor / professional / all — **ISSUE: output used `"all"` as a string, not an array `["all"]`**
- [ ] `suggested_angles` keys match `target_audience` entries — **ISSUE: `suggested_angles` field missing from output entirely**

## Issues Found

1. `target_audience` should be an array `["all"]`, output was `"all"` (string)
2. `suggested_angles` field missing — skill should always output this
3. Output JSON uses non-standard fields (`lsi_keywords`, `content_angle`, `content_gaps`, `suggested_title`, `suggested_slug`, `word_count_target`, `serp_sources_observed`) not defined in the schema — downstream agents may not parse correctly
4. `long_tail_keywords` field missing — required by schema

## Raw Output

### Step 1: Topic Selection

Reviewed keyword_matrix.json (13 topics) against keyword_history.json (15 entries) and published articles (22 slugs).

Most covered in history: AI startups/investment (6 entries), AI agents/automation (4), AI industry trends (3).

Zero history entries for: AI Model Releases (priority 1, tier 1), AI Market Dynamics (priority 3), AI Enterprise Adoption (priority 4), AI Infrastructure, AI Geopolitics, AI Business Models, AI Consumer Products, AI Open Source Ecosystem, AI in Verticals.

Selected: **AI Model Releases** — highest priority (1), tier 1, high opportunity, zero history coverage, no published articles in this space.

### Step 2: Seed Keywords

From matrix + topic context:
1. best AI models benchmark comparison 2026
2. best new AI models released 2026
3. AI model capability breakthroughs 2026
4. latest LLM releases ranked 2026
5. top AI models 2026
6. best AI model per task 2026
7. GPT-5 vs Claude vs Gemini 2026
8. which AI model should I use 2026
9. AI model pricing comparison 2026
10. LLM benchmark comparison April 2026

### Steps 3-6: SERP Validation & Selection

6 searches run. 0 authority sites on SERP for all candidates → HIGH opportunity confirmed.

Primary: `best AI models 2026 ranked`
Secondary: which AI model should I use 2026, GPT-5 vs Claude vs Gemini 2026, best AI model per task 2026, LLM benchmark comparison 2026, AI model pricing comparison 2026

### Final Output

```json
KEYWORD_RESEARCH_JSON
{
  "date": "2026-04-21",
  "topic": "AI Model Releases",
  "primary_keyword": "best AI models 2026 ranked",
  "secondary_keywords": [
    "which AI model should I use 2026",
    "GPT-5 vs Claude vs Gemini 2026",
    "best AI model per task 2026",
    "LLM benchmark comparison 2026",
    "AI model pricing comparison 2026"
  ],
  "lsi_keywords": [
    "Claude Opus 4.6 benchmark",
    "GPT-5.4 performance",
    "Gemini 3.1 Pro comparison",
    "Grok 4 SWE-bench",
    "DeepSeek V4 2026",
    "LLM leaderboard 2026",
    "AI model context window comparison",
    "best LLM for coding 2026",
    "AI model market share 2026"
  ],
  "opportunity": "high",
  "content_type": "listicle + comparison",
  "target_audience": "all",
  "intent": "comparison + informational",
  "competition": "low-medium",
  "authority_sites_on_serp": 0,
  "content_angle": "Task-by-task model decision matrix covering 8+ models with April 2026 benchmark data, pricing tiers, and market share shift analysis.",
  "content_gaps": [
    "No single article combines task-by-task decision matrix + pricing TCO + market share shifts",
    "Grok 4 inclusion missing from most April 2026 comparisons",
    "Investor angle on market share concentration underserved",
    "Free tier comparison not covered comprehensively"
  ],
  "suggested_title": "Best AI Models in 2026: Ranked by Task, Benchmark, and Price",
  "suggested_slug": "best-ai-models-2026-ranked",
  "word_count_target": 2800
}
```
