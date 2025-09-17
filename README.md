# Git Eval

Small CLI to analyze a single Git repository’s full history and output metrics and reports.

Configuration
- Copy .env.sample to .env and set:
  - GIT_EVAL_GIT_DIR: absolute path to a .git directory or to the repo work tree root
  - OUTPUT_DIR: directory for output files (default ./outputs)
  - SESSION_GAP_MINUTES: gap to split sessions for hour estimation (default 90)
  - MAX_HOURS_PER_DAY: per-day cap when summing sessions (default 10)
  - INCLUDE_MERGES: 1 to include merge commits in stats (default 1)

Usage
- With Poetry (recommended):
  poetry install
  poetry run git-eval

- With Python directly (if Poetry not installed):
  python3 -m giteval

Outputs
- <repo_name>_git_eval.json: metrics plus per-commit numstat list
- <repo_name>_git_eval.csv: one-row summary of metrics
- <repo_name>_git_eval.txt: human-readable summary
- <repo_name>_git_eval.md: Markdown report with a summary table, Mermaid pie chart (commits by author), and monthly activity table with ASCII bars

Notes
- Lines of code refer to cumulative added/deleted lines from git numstat over full history (not current LOC snapshot).
- Estimated hours are a heuristic from commit sessions per author; treat as an approximation.
- Mermaid charts render in viewers that support Mermaid (e.g., GitHub).

