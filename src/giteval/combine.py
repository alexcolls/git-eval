#!/usr/bin/env python3
import os
import sys
from pathlib import Path
from typing import List, Dict, Tuple
from dataclasses import asdict
import json

from giteval.main import (
    parse_git_log_with_numstat,
    compute_metrics,
    write_reports,
    _aggregate_monthly,
    _author_details,
    _current_loc_snapshot,
)

BASE = Path("/home/quantium/labs/oriane").resolve()
OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", "./_output")).resolve()


def discover_repos(base: Path) -> List[Path]:
    repos: List[Path] = []
    for d in sorted(base.iterdir()):
        if not d.is_dir():
            continue
        if d.name in {"git-eval", "_deprecated"}:
            continue
        # check git repo
        ok = os.system(f"git -C {d.as_posix()} rev-parse --is-inside-work-tree >/dev/null 2>&1") == 0
        if ok:
            repos.append(d)
    dep = base / "_deprecated"
    if dep.is_dir():
        for d in sorted(dep.iterdir()):
            if d.is_dir():
                ok = os.system(f"git -C {d.as_posix()} rev-parse --is-inside-work-tree >/dev/null 2>&1") == 0
                if ok:
                    repos.append(d)
    return repos


def build_dashboard(per_repo: List[Dict]) -> Tuple[str, Dict]:
    # Sort repos by estimated_hours_total desc
    per_repo_sorted = sorted(per_repo, key=lambda r: r["metrics"]["estimated_hours_total"], reverse=True)
    # Aggregate authors across repos
    author_agg: Dict[str, Dict[str, float]] = {}
    for r in per_repo:
        authors = r.get("breakdowns", {}).get("authors", [])
        for a in authors:
            key = a["author"]
            agg = author_agg.setdefault(key, {
                "author": key,
                "repos": set(),
                "commits_total": 0,
                "estimated_hours": 0.0,
                "added_total": 0,
                "deleted_total": 0,
                "files_changed_total": 0,
                "active_days": 0,
            })
            agg["repos"].add(r["repo"])  # type: ignore
            agg["commits_total"] += int(a.get("commits_total", 0))
            agg["estimated_hours"] += float(a.get("estimated_hours", 0.0))
            agg["added_total"] += int(a.get("added_total", 0))
            agg["deleted_total"] += int(a.get("deleted_total", 0))
            agg["files_changed_total"] += int(a.get("files_changed_total", 0))
            agg["active_days"] += int(a.get("active_days", 0))
    author_list = list(author_agg.values())
    for a in author_list:
        a["repos"] = sorted(list(a["repos"]))  # type: ignore
    author_sorted = sorted(author_list, key=lambda x: (x["estimated_hours"], x["commits_total"]), reverse=True)

    # Markdown
    lines: List[str] = []
    lines.append("# Oriane — Git evaluation dashboard")
    lines.append("")
    lines.append(f"Repos analyzed: {len(per_repo)}")
    lines.append("")

    # Repo ranking
    lines.append("## Repositories by estimated hours")
    lines.append("")
    lines.append("| Rank | Repository | Hours | Commits | Authors | First | Last | Added | Deleted | Files | Avg commits/day |")
    lines.append("|---:|---|---:|---:|---:|---|---|---:|---:|---:|---:|")
    for i, r in enumerate(per_repo_sorted, 1):
        m = r["metrics"]
        repo = r["repo"]
        lines.append(
            f"| {i} | `{repo}` | {m['estimated_hours_total']} | {m['commits_total']} | {m['unique_authors']} | {m['first_commit']} | {m['last_commit']} | {m['added_lines_total']} | {m['deleted_lines_total']} | {m['files_changed_total']} | {m['avg_commits_per_day']} |"
        )
    lines.append("")

    # Author leaderboard
    if author_sorted:
        lines.append("## Developers by estimated hours (across repos)")
        lines.append("")
        lines.append("| Rank | Developer | Hours | Commits | Repos | Added | Deleted | Files | Active days |")
        lines.append("|---:|---|---:|---:|---|---:|---:|---:|---:|")
        top_hours = author_sorted[0]["estimated_hours"] if author_sorted else 0
        for i, a in enumerate(author_sorted, 1):
            stars = int(round((a["estimated_hours"] / top_hours) * 5)) if top_hours > 0 else 0
            star_bar = "★" * stars + "☆" * (5 - stars)
            lines.append(
                f"| {i} | {a['author']} | {a['estimated_hours']:.2f} {star_bar} | {a['commits_total']} | {', '.join(a['repos'])} | {a['added_total']} | {a['deleted_total']} | {a['files_changed_total']} | {a['active_days']} |"
            )
        lines.append("")

    md = "\n".join(lines) + "\n"
    payload = {
        "repos": per_repo_sorted,
        "authors": author_sorted,
    }
    return md, payload


def main(argv: List[str] = None) -> int:
    argv = argv or sys.argv[1:]
    if argv:
        repo_paths = [Path(a).resolve() for a in argv]
    else:
        repo_paths = discover_repos(BASE)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    all_payloads = []
    for path in repo_paths:
        try:
            commits = parse_git_log_with_numstat(path, include_merges=(os.getenv("INCLUDE_MERGES", "1") not in {"0", "false", "False"}))
        except Exception:
            continue
        metrics = compute_metrics(commits)
        metrics.repo_path = path.as_posix()
        write_reports(OUTPUT_DIR, path, metrics, commits)
        curr_loc = _current_loc_snapshot(path)
        data = {
            "repo": path.as_posix(),
            "metrics": asdict(metrics),
            "current_loc": {"lines": curr_loc[0], "files": curr_loc[1]},
            "breakdowns": {
                "authors": _author_details(commits),
                "monthly": [
                    {"month": m, "commits": c, "added": a, "deleted": d, "files": f}
                    for (m, c, a, d, f) in _aggregate_monthly(commits)
                ],
            },
        }
        all_payloads.append(data)

    md, combined = build_dashboard(all_payloads)
    (OUTPUT_DIR / "_git_eval_dashboard.md").write_text(md)
    (OUTPUT_DIR / "_git_eval_dashboard.json").write_text(json.dumps(combined, indent=2))
    print(f"Wrote combined dashboard for {len(all_payloads)} repos to {OUTPUT_DIR.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
