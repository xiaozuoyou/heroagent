#!/usr/bin/env python3
"""
Promote HeroAgent wiki maintenance by creating missing drafts, applying ready drafts,
and marking stale drafts.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from common import append_wiki_sync_content
from common import create_wiki_sync_drafts
from common import draft_target_from_text
from common import ensure_wiki_section_path
from common import extract_draft_merge_content
from common import init_workspace
from common import parse_draft_mapping
from common import parse_maintenance_report
from common import refresh_wiki_registry
from common import render_wiki_maintenance_report
from common import is_stale_file
from common import draft_filename_for_target


def resolve_target_path(workspace: Path, target: str) -> Path:
    if target.startswith("modules/"):
        return ensure_wiki_section_path(workspace=workspace, module_name=Path(target).stem)
    return ensure_wiki_section_path(workspace=workspace, section=Path(target).stem)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Promote HeroAgent wiki maintenance by creating missing drafts, applying ready drafts, and marking stale drafts.",
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
        help="Changed file path used to infer wiki maintenance. Can be passed multiple times.",
    )
    parser.add_argument(
        "--stale-days",
        type=int,
        default=7,
        help="Draft files older than this number of days are treated as stale. Defaults to 7.",
    )
    parser.add_argument(
        "--apply-ready",
        action="store_true",
        help="Apply non-stale drafts back into formal wiki files.",
    )
    parser.add_argument(
        "--materialize-missing",
        action="store_true",
        help="Create missing suggested drafts before refreshing maintenance state.",
    )
    parser.add_argument(
        "--mark-stale",
        action="store_true",
        help="Append a stale marker to stale draft files instead of leaving them untouched.",
    )
    args = parser.parse_args()

    target = Path(args.target).resolve()
    target.mkdir(parents=True, exist_ok=True)
    workspace = init_workspace(target, with_readme=True, with_current_focus=True)
    drafts_dir = workspace / "wiki" / "drafts"
    drafts_dir.mkdir(parents=True, exist_ok=True)

    if args.materialize_missing:
        create_wiki_sync_drafts(
            workspace=workspace,
            changed_paths=args.changed_paths,
            materialize_suggestions=True,
        )

    refresh_wiki_registry(workspace, changed_paths=args.changed_paths)

    suggested = set(refresh_wiki_registry(workspace, changed_paths=args.changed_paths)[2])

    missing_drafts = []
    for item in suggested:
        draft_path = drafts_dir / draft_filename_for_target(item)
        if not draft_path.exists():
            missing_drafts.append(item)

    stale_drafts = []
    ready_drafts = []
    for path in sorted(drafts_dir.glob("*")):
        if not path.is_file() or path.name in {".gitkeep", "maintenance-report.md"}:
            continue
        draft_text = path.read_text(encoding="utf-8")
        target_name = draft_target_from_text(draft_text, draft_name=path.name)
        display = f"{path.relative_to(workspace / 'wiki').as_posix()} -> {target_name}"
        if is_stale_file(path, args.stale_days):
            stale_drafts.append(display)
        else:
            ready_drafts.append(display)

    report_text = render_wiki_maintenance_report(
        stale_days=args.stale_days,
        changed_paths=args.changed_paths,
        missing_drafts=missing_drafts,
        stale_drafts=stale_drafts,
        ready_drafts=ready_drafts,
    )
    report_path = drafts_dir / "maintenance-report.md"
    report_path.write_text(report_text, encoding="utf-8")

    parsed = parse_maintenance_report(report_text)
    created_drafts: list[str] = []
    applied_drafts: list[str] = []
    marked_stale: list[str] = []

    if args.materialize_missing and parsed["missing_drafts"]:
        drafts, _ = create_wiki_sync_drafts(
            workspace=workspace,
            changed_paths=args.changed_paths,
            materialize_suggestions=True,
        )
        created_drafts = [path.relative_to(workspace).as_posix() for path in drafts]

    if args.apply_ready:
        for item in parsed["ready_drafts"]:
            draft_rel, target_name = parse_draft_mapping(item)
            draft_path = workspace / "wiki" / draft_rel
            draft_text = draft_path.read_text(encoding="utf-8")
            content = extract_draft_merge_content(draft_text)
            if not content:
                continue
            wiki_path = resolve_target_path(workspace, target_name)
            append_wiki_sync_content(wiki_path, content)
            draft_path.unlink()
            applied_drafts.append(target_name)

    if args.mark_stale:
        for item in parsed["stale_drafts"]:
            draft_rel, _ = parse_draft_mapping(item)
            draft_path = workspace / "wiki" / draft_rel
            text = draft_path.read_text(encoding="utf-8")
            if "## 陈旧标记" not in text:
                draft_path.write_text(
                    text.rstrip()
                    + "\n\n## 陈旧标记\n- 该草稿已超过维护阈值，建议复核或重生成。\n",
                    encoding="utf-8",
                )
            marked_stale.append(draft_path.relative_to(workspace / "wiki").as_posix())

    refresh_wiki_registry(workspace, changed_paths=args.changed_paths)

    print(f"Promoted HeroAgent wiki maintenance: {report_path}")
    if created_drafts:
        print("Created drafts:")
        for item in created_drafts:
            print(f"- {item}")
    if applied_drafts:
        print("Applied drafts:")
        for item in applied_drafts:
            print(f"- {item}")
    if marked_stale:
        print("Marked stale drafts:")
        for item in marked_stale:
            print(f"- {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
