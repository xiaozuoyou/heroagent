#!/usr/bin/env python3
"""
Inspect HeroAgent wiki freshness and draft coverage, then write a maintenance report.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from common import draft_filename_for_target
from common import draft_target_from_text
from common import init_workspace
from common import is_stale_file
from common import load_wiki_registry
from common import refresh_wiki_registry
from common import render_wiki_maintenance_report


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Inspect HeroAgent wiki freshness and draft coverage, then write a maintenance report.",
    )
    parser.add_argument(
        "target",
        nargs="?",
        default=".",
        help="Target project directory. Defaults to the current directory.",
    )
    parser.add_argument(
        "--changed-path",
        dest="changed_paths",
        action="append",
        default=[],
        help="Changed file path used to infer pending wiki maintenance. Can be passed multiple times.",
    )
    parser.add_argument(
        "--stale-days",
        type=int,
        default=7,
        help="Draft files older than this number of days are treated as stale. Defaults to 7.",
    )
    args = parser.parse_args()

    target = Path(args.target).resolve()
    target.mkdir(parents=True, exist_ok=True)
    workspace = init_workspace(target, with_readme=True, with_current_focus=True)
    refresh_wiki_registry(workspace, changed_paths=args.changed_paths)
    registry = load_wiki_registry(workspace)

    drafts_dir = workspace / "wiki" / "drafts"
    drafts_dir.mkdir(parents=True, exist_ok=True)

    suggested_updates = registry.get("suggested_updates", [])
    missing_drafts: list[str] = []
    for item in suggested_updates:
        draft_path = drafts_dir / draft_filename_for_target(item)
        if not draft_path.exists():
            missing_drafts.append(item)

    stale_drafts: list[str] = []
    ready_drafts: list[str] = []
    for path in sorted(drafts_dir.glob("*")):
        if not path.is_file():
            continue
        if path.name == ".gitkeep":
            continue

        rel = path.relative_to(workspace / "wiki").as_posix()
        draft_text = path.read_text(encoding="utf-8")
        draft_target = draft_target_from_text(draft_text, draft_name=path.name)
        display_name = f"{rel} -> {draft_target}"
        if is_stale_file(path, args.stale_days):
            stale_drafts.append(display_name)
        else:
            ready_drafts.append(display_name)

    report = render_wiki_maintenance_report(
        stale_days=args.stale_days,
        changed_paths=args.changed_paths,
        missing_drafts=missing_drafts,
        stale_drafts=stale_drafts,
        ready_drafts=ready_drafts,
    )
    report_path = drafts_dir / "maintenance-report.md"
    report_path.write_text(report, encoding="utf-8")
    refresh_wiki_registry(workspace, changed_paths=args.changed_paths)

    print(f"Wrote HeroAgent wiki maintenance report: {report_path}")
    if missing_drafts:
        print("Missing drafts:")
        for item in missing_drafts:
            print(f"- {item}")
    if stale_drafts:
        print("Stale drafts:")
        for item in stale_drafts:
            print(f"- {item}")
    if ready_drafts:
        print("Ready drafts:")
        for item in ready_drafts:
            print(f"- {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
