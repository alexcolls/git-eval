# Git Eval

Small CLI to analyze a single Git repository’s full history and output metrics and reports.

Configuration

- Copy .env.sample to .env and set:
- GIT_EVAL_GIT_DIR: absolute path to a .git directory or to the repo work tree root
- OUTPUT_DIR: directory for output files (default ./\_output)
- GIT_EVAL_EXCLUDE_EXTS: comma-separated extensions to skip writing (default .csv,.txt,.json)
- SESSION_GAP_MINUTES: gap to split sessions for hour estimation (default 90)
- MAX_HOURS_PER_DAY: per-day cap when summing sessions (default 10)
- TIMEZONE: optional IANA timezone name to normalize commit times (default: use commit timezones). Default in sample: Europe/Madrid.
- DAY_START_HOUR, DAY_END_HOUR: daytime window (default 8–20)
- NIGHTS_START_HOUR, NIGHTS_END_HOUR: nighttime window (default 22–6, wrapping midnight)
- INCLUDE_MERGES: 1 to include merge commits in stats (default 1)

Usage

- With Poetry (recommended):
  poetry install
  poetry run git-eval

- With Python directly (if Poetry not installed):
  python3 -m giteval

Multi-repo dashboard

- Run across all top-level repos under /home/quantium/labs/oriane (and _deprecated/*):
  python3 -m giteval.combine
- Outputs in OUTPUT_DIR (default ./_output):
  - _git_eval_dashboard.md (detailed Markdown with charts and tables)
  - _git_eval_dashboard.json (data backing the dashboard)
  - _git_eval_monthly_totals.csv (global month aggregates: hours, commits, added, deleted)
  - _git_eval_authors_schedule.csv (per-author: hours, commits, weekend/weekday, day/night, repos_count)

Outputs

- <repo_name>\_git_eval.md: Markdown report with summary, charts, tables, and schedule footprint (default)
- <repo_name>\_git_eval.json: metrics plus per-commit list (omit by adding .json to GIT_EVAL_EXCLUDE_EXTS)
- <repo_name>\_git_eval.csv: one-row summary (omit with .csv in GIT_EVAL_EXCLUDE_EXTS)
- <repo_name>\_git_eval.txt: human-readable summary (omit with .txt in GIT_EVAL_EXCLUDE_EXTS)
- Dashboard extras in OUTPUT_DIR: `_git_eval_dashboard.md`, `_git_eval_dashboard.json`, `_git_eval_monthly_totals.csv`, `_git_eval_authors_schedule.csv`

Notes

- Lines of code refer to cumulative added/deleted lines from git numstat over full history (not current LOC snapshot).
- Estimated hours are a heuristic from commit sessions per author; treat as an approximation.
- Mermaid charts render in viewers that support Mermaid (e.g., GitHub). Some charts use xychart-beta and sankey-beta features.

## Examples

```bash
git-eval
```

or

```bash
OUTPUT_DIR=./_output
GIT_EVAL_EXCLUDE_EXTS=.csv,.txt,.json
SESSION_GAP_MINUTES=90
MIN_SESSION_MINUTES=45
MINUTES_PER_COMMIT_BASE=15
MINUTES_PER_100_LINES=12
MINUTES_PER_FILE=3
CALIBRATION_FACTOR=2.0
PYTHONPATH=./src python3 -m giteval.combine
```
