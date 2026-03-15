#!/usr/bin/env python3
"""
Run a named HeroAgent wiki maintenance strategy.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from common import compact_wiki_content
from common import create_wiki_sync_drafts
from common import draft_filename_for_target
from common import draft_target_from_text
from common import ensure_wiki_section_path
from common import extract_draft_merge_content
from common import extract_source_facts
from common import init_workspace
from common import is_stale_file
from common import refresh_wiki_registry
from common import render_extracted_facts
from common import render_wiki_maintenance_report
from common import resolve_wiki_strategy
from common import suggest_wiki_targets
from common import append_wiki_sync_content


def resolve_target_path(workspace: Path, target: str) -> Path:
    if target.startswith("modules/"):
        return ensure_wiki_section_path(workspace=workspace, module_name=Path(target).stem)
    return ensure_wiki_section_path(workspace=workspace, section=Path(target).stem)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run a named HeroAgent wiki maintenance strategy.",
    )
    parser.add_argument(
        "strategy",
        choices=["conservative", "balanced", "aggressive"],
        help="Named wiki maintenance strategy.",
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
        help="Changed path used to drive wiki maintenance. Can be passed multiple times.",
    )
    parser.add_argument(
        "--stale-days",
        type=int,
        default=7,
        help="Draft files older than this number of days are treated as stale. Defaults to 7.",
    )
    args = parser.parse_args()

    strategy = resolve_wiki_strategy(args.strategy)
    target = Path(args.target).resolve()
    target.mkdir(parents=True, exist_ok=True)
    workspace = init_workspace(target, with_readme=True, with_current_focus=True)
    drafts_dir = workspace / "wiki" / "drafts"
    drafts_dir.mkdir(parents=True, exist_ok=True)

    created_drafts: list[str] = []
    applied_drafts: list[str] = []
    marked_stale: list[str] = []
    extracted_fact_drafts: list[str] = []
    compacted_files: list[str] = []

    refresh_wiki_registry(workspace, changed_paths=args.changed_paths)
    suggestions = suggest_wiki_targets(args.changed_paths)

    if strategy["materialize_missing"]:
        drafts, _ = create_wiki_sync_drafts(
            workspace=workspace,
            changed_paths=args.changed_paths,
            materialize_suggestions=True,
        )
        created_drafts.extend(path.relative_to(workspace).as_posix() for path in drafts)

    if strategy["extract_facts"]:
        extracted = extract_source_facts(target, args.changed_paths)
        for target_doc, facts in extracted.items():
            draft_path = drafts_dir / f"facts__{draft_filename_for_target(target_doc)}"
            draft_path.write_text(render_extracted_facts(target_doc, facts), encoding="utf-8")
            extracted_fact_drafts.append(draft_path.relative_to(workspace).as_posix())

    refresh_wiki_registry(workspace, changed_paths=args.changed_paths)

    stale_drafts: list[Path] = []
    ready_drafts: list[Path] = []
    for path in sorted(drafts_dir.glob("*")):
        if not path.is_file() or path.name in {".gitkeep", "maintenance-report.md"}:
            continue
        if is_stale_file(path, args.stale_days):
            stale_drafts.append(path)
        else:
            ready_drafts.append(path)

    if strategy["apply_ready"]:
        for draft_path in ready_drafts:
            draft_text = draft_path.read_text(encoding="utf-8")
            target_name = draft_target_from_text(draft_text, draft_name=draft_path.name)
            content = extract_draft_merge_content(draft_text)
            if not content and "## 建议写回" in draft_text:
                content = draft_text.split("## 建议写回", 1)[1].strip()
            if not content:
                continue
            wiki_path = resolve_target_path(workspace, target_name)
            append_wiki_sync_content(wiki_path, content)
            draft_path.unlink()
            applied_drafts.append(target_name)

    if strategy["mark_stale"]:
        for draft_path in stale_drafts:
            text = draft_path.read_text(encoding="utf-8")
            if "## 陈旧标记" not in text:
                draft_path.write_text(
                    text.rstrip()
                    + "\n\n## 陈旧标记\n- 该草稿已超过维护阈值，建议复核或重生成。\n",
                    encoding="utf-8",
                )
            marked_stale.append(draft_path.relative_to(workspace).as_posix())

    if strategy["compact_memory"]:
        wiki_root = workspace / "wiki"
        for path in list((wiki_root / "modules").glob("*.md")) + [
            wiki_root / "overview.md",
            wiki_root / "arch.md",
            wiki_root / "api.md",
            wiki_root / "data.md",
        ]:
            if not path.exists():
                continue
            original = path.read_text(encoding="utf-8")
            updated = compact_wiki_content(original)
            if updated != original:
                path.write_text(updated, encoding="utf-8")
                compacted_files.append(path.relative_to(workspace).as_posix())

    missing_drafts = []
    for item in suggestions:
        draft_path = drafts_dir / draft_filename_for_target(item)
        if not draft_path.exists():
            missing_drafts.append(item)

    report = render_wiki_maintenance_report(
        stale_days=args.stale_days,
        changed_paths=args.changed_paths,
        missing_drafts=missing_drafts,
        stale_drafts=marked_stale,
        ready_drafts=applied_drafts,
    )
    report_path = drafts_dir / "maintenance-report.md"
    report_path.write_text(report, encoding="utf-8")

    refresh_wiki_registry(workspace, changed_paths=args.changed_paths)

    print(f"Ran HeroAgent wiki strategy: {args.strategy}")
    if created_drafts:
        print("Created drafts:")
        for item in created_drafts:
            print(f"- {item}")
    if extracted_fact_drafts:
        print("Extracted fact drafts:")
        for item in extracted_fact_drafts:
            print(f"- {item}")
    if applied_drafts:
        print("Applied drafts:")
        for item in applied_drafts:
            print(f"- {item}")
    if marked_stale:
        print("Marked stale drafts:")
        for item in marked_stale:
            print(f"- {item}")
    if compacted_files:
        print("Compacted wiki files:")
        for item in compacted_files:
            print(f"- {item}")
    print(f"Updated maintenance report: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
