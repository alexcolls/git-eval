# Git Evaluation — OrianeCoreAI-mojo

Repo: `/home/quantium/labs/oriane/_deprecated/OrianeCoreAI-mojo`

## Summary

| Metric | Value |
|---|---:|
| Current tracked files | 838 |
| Current lines of code (tracked) | 318129 |
| Commits (total) | 6 |
| Commits (merges) | 1 |
| Commits (non-merges) | 5 |
| Unique authors | 1 |
| First commit | 2025-03-04T23:11:23+01:00 |
| Last commit | 2025-03-05T00:18:00+01:00 |
| Active days | 2 |
| Span days | 2 |
| Avg commits/day | 3.0 |
| Lines added (sum) | 301105 |
| Lines deleted (sum) | 1 |
| Files touched (sum of numstat rows) | 842 |
| Estimated hours (session-based) | 21.5 |

## Developer leaderboard

| Developer | Commits | Hours | Added | Deleted | Files | Active days | First | Last | Avg size | Median size | Stars |
|---|---:|---:|---:|---:|---:|---:|---|---|---:|---:|:--:
| quantium-rock <alexcollsoutumuro@gmail.com> | 4 | 20.0 | 301102 | 1 | 840 | 2 | 2025-03-04T23:58:27+01:00 | 2025-03-05T00:18:00+01:00 | 75275.75 | 2.5 | ★★★★★ |
| Alex Colls Outumuro <alexcollsoutumuro@gmail.com> | 2 | 1.5 | 3 | 0 | 2 | 2 | 2025-03-04T23:11:23+01:00 | 2025-03-05T00:01:08+01:00 | 1.5 | 1.5 | ☆☆☆☆☆ |

## Commits by author

```mermaid
pie title Commits by author
    "quantium-rock <alexcollsoutumuro@gmail.com>" : 4
    "Alex Colls Outumuro <alexcollsoutumuro@gmail.com>" : 2
```

## Lines added by author

```mermaid
pie title Lines added by author
    "quantium-rock <alexcollsoutumuro@gmail.com>" : 301102
    "Alex Colls Outumuro <alexcollsoutumuro@gmail.com>" : 3
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
| MIN_SESSION_MINUTES | 45.0 |
| MINUTES_PER_COMMIT_BASE | 15.0 |
| MINUTES_PER_100_LINES | 12.0 |
| MINUTES_PER_FILE | 3.0 |
| CALIBRATION_FACTOR | 2.0 |

## Monthly activity

| Month | Commits | Added | Deleted | Files | Chart |
|---|---:|---:|---:|---:|:---|
| 2025-03 | 6 | 301105 | 1 | 842 | ######################################## |

## Author activity timeline

```mermaid
gantt
    title Active months per author
    dateFormat  YYYY-MM-DD
    section Alex Colls Outumuro <alexcollsoutumuro@gmail.com>
    Alex Colls Outumuro <alexcollsoutumuro@gmail.com> 1 : 2025-03-01, 2025-04-01
    section quantium-rock <alexcollsoutumuro@gmail.com>
    quantium-rock <alexcollsoutumuro@gmail.com> 1 : 2025-03-01, 2025-04-01
```

## Highlights

- Longest active streak: 2 days (2025-03-04 to 2025-03-05)
- Best day by commits: 2025-03-05 — 4 commits
- Best day by lines added: 2025-03-04 — 301098 lines

