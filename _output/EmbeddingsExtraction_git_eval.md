# Git Evaluation — EmbeddingsExtraction

Repo: `/home/quantium/labs/oriane/_deprecated/EmbeddingsExtraction`

## Summary

| Metric | Value |
|---|---:|
| Current tracked files | 224 |
| Current lines of code (tracked) | 45700 |
| Commits (total) | 10 |
| Commits (merges) | 0 |
| Commits (non-merges) | 10 |
| Unique authors | 1 |
| First commit | 2025-06-18T16:29:57+02:00 |
| Last commit | 2025-06-25T09:20:23+02:00 |
| Active days | 4 |
| Span days | 8 |
| Avg commits/day | 1.25 |
| Lines added (sum) | 18012 |
| Lines deleted (sum) | 12860 |
| Files touched (sum of numstat rows) | 495 |
| Estimated hours (session-based) | 59.53 |

## Developer leaderboard

| Developer | Commits | Hours | Added | Deleted | Files | Active days | First | Last | Avg size | Median size | Stars |
|---|---:|---:|---:|---:|---:|---:|---|---|---:|---:|:--:
| quantium-rock <alexcollsoutumuro@gmail.com> | 9 | 58.03 | 17817 | 12860 | 493 | 4 | 2025-06-18T18:16:41+02:00 | 2025-06-25T09:20:23+02:00 | 3408.56 | 107.0 | ★★★★★ |
| Alex Colls Outumuro <alexcollsoutumuro@gmail.com> | 1 | 1.5 | 195 | 0 | 2 | 1 | 2025-06-18T16:29:57+02:00 | 2025-06-18T16:29:57+02:00 | 195.0 | 195.0 | ☆☆☆☆☆ |

## Commits by author

```mermaid
pie title Commits by author
    "quantium-rock <alexcollsoutumuro@gmail.com>" : 9
    "Alex Colls Outumuro <alexcollsoutumuro@gmail.com>" : 1
```

## Lines added by author

```mermaid
pie title Lines added by author
    "quantium-rock <alexcollsoutumuro@gmail.com>" : 17817
    "Alex Colls Outumuro <alexcollsoutumuro@gmail.com>" : 195
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
| 2025-06 | 10 | 18012 | 12860 | 495 | ######################################## |

## Author activity timeline

```mermaid
gantt
    title Active months per author
    dateFormat  YYYY-MM-DD
    section Alex Colls Outumuro <alexcollsoutumuro@gmail.com>
    Alex Colls Outumuro <alexcollsoutumuro@gmail.com> 1 : 2025-06-01, 2025-07-01
    section quantium-rock <alexcollsoutumuro@gmail.com>
    quantium-rock <alexcollsoutumuro@gmail.com> 1 : 2025-06-01, 2025-07-01
```

## Highlights

- Longest active streak: 3 days (2025-06-18 to 2025-06-20)
- Best day by commits: 2025-06-18 — 4 commits
- Best day by lines added: 2025-06-19 — 10576 lines

