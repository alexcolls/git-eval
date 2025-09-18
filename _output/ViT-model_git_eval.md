# Git Evaluation — ViT-model

Repo: `/home/quantium/labs/oriane/_deprecated/ViT-model`

## Summary

| Metric | Value |
|---|---:|
| Current tracked files | 6 |
| Current lines of code (tracked) | 29284 |
| Commits (total) | 6 |
| Commits (merges) | 0 |
| Commits (non-merges) | 6 |
| Unique authors | 1 |
| First commit | 2025-04-05T13:09:07+02:00 |
| Last commit | 2025-04-06T23:36:53+02:00 |
| Active days | 2 |
| Span days | 2 |
| Avg commits/day | 3.0 |
| Lines added (sum) | 29351 |
| Lines deleted (sum) | 2 |
| Files touched (sum of numstat rows) | 10 |
| Estimated hours (session-based) | 6.93 |

## Schedule footprint

| Metric | Count |
|---|---:|
| Weekend days active (Sat/Sun) | 2 |
| Weekday days active | 0 |
| Night days active | 1 |
| Daytime days active | 1 |
| Days with both day & night activity | 0 |
| Day-only days | 1 |
| Night-only days | 1 |

## Developer leaderboard

| Developer | Commits | Hours | Wknd days | Night days | Day days | Both | Added | Deleted | Files | Active days | First | Last | Avg size | Median size | Stars |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---:|---:|:--:
| quantium-rock <alexcollsoutumuro@gmail.com> | 5 | 6.18 | 2 | 1 | 1 | 0 | 29176 | 2 | 8 | 2 | 2025-04-05T13:35:52+02:00 | 2025-04-06T23:36:53+02:00 | 5835.6 | 66.0 | ★★★★★ |
| Alex Colls Outumuro <alexcollsoutumuro@gmail.com> | 1 | 0.75 | 1 | 0 | 1 | 0 | 175 | 0 | 2 | 1 | 2025-04-05T13:09:07+02:00 | 2025-04-05T13:09:07+02:00 | 175.0 | 175.0 | ★☆☆☆☆ |

## Commits by author

```mermaid
pie title Commits by author
    "quantium-rock <alexcollsoutumuro@gmail.com>" : 5
    "Alex Colls Outumuro <alexcollsoutumuro@gmail.com>" : 1
```

## Lines added by author

```mermaid
pie title Lines added by author
    "quantium-rock <alexcollsoutumuro@gmail.com>" : 29176
    "Alex Colls Outumuro <alexcollsoutumuro@gmail.com>" : 175
```

## Effort estimation model

This report estimates effort using a session + commit-weighted heuristic:
- Split commits per author into sessions where the gap > SESSION_GAP_MINUTES.
- Per session, sum per-commit minutes: base + sqrt(lines)/10 * MINUTES_PER_100_LINES + files * MINUTES_PER_FILE.
- Enforce MIN_SESSION_MINUTES minimum per session.
- Sum per day with MAX_HOURS_PER_DAY cap; multiply by CALIBRATION_FACTOR.

Parameters:

| Param | Value |
|---|---:|
| SESSION_GAP_MINUTES | 90 |
| MAX_HOURS_PER_DAY | 10.0 |
| MIN_SESSION_MINUTES | 30.0 |
| MINUTES_PER_COMMIT_BASE | 12.0 |
| MINUTES_PER_100_LINES | 8.0 |
| MINUTES_PER_FILE | 2.0 |
| CALIBRATION_FACTOR | 1.5 |

## Monthly activity

| Month | Commits | Added | Deleted | Files | Chart |
|---|---:|---:|---:|---:|:---|
| 2025-04 | 6 | 29351 | 2 | 10 | ######################################## |

## Author activity timeline

```mermaid
gantt
    title Active months per author
    dateFormat  YYYY-MM-DD
    section Alex Colls Outumuro <alexcollsoutumuro@gmail.com>
    Alex Colls Outumuro <alexcollsoutumuro@gmail.com> 1 : 2025-04-01, 2025-05-01
    section quantium-rock <alexcollsoutumuro@gmail.com>
    quantium-rock <alexcollsoutumuro@gmail.com> 1 : 2025-04-01, 2025-05-01
```

## Highlights

- Longest active streak: 2 days (2025-04-05 to 2025-04-06)
- Best day by commits: 2025-04-05 — 5 commits
- Best day by lines added: 2025-04-06 — 28947 lines

