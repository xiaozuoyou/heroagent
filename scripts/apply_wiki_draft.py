#!/usr/bin/env python3
"""
Apply a HeroAgent wiki draft into the target wiki document and refresh registry.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from common import append_wiki_sync_content
from common import draft_target_from_text
from common import ensure_wiki_section_path
from common import extract_draft_merge_content
from common import init_workspace
from common import refresh_wiki_registry


def resolve_target_path(workspace: Path, target: str) -> Path:
    if target.startswith("modules/"):
        module_name = Path(target).stem
        return ensure_wiki_section_path(workspace=workspace, module_name=module_name)

    section_name = Path(target).stem
    return ensure_wiki_section_path(workspace=workspace, section=section_name)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Apply a HeroAgent wiki draft into the target wiki document and refresh registry.",
    )
    parser.add_argument(
        "draft",
        help="Draft file path relative to .heroagent/wiki/drafts/ or an absolute path.",
    )
    parser.add_argument(
        "target",
        nargs="?",
        default=".",
        help="Target project directory. Defaults to the current directory.",
    )
    parser.add_argument(
        "--keep-draft",
        action="store_true",
        help="Keep the draft file after applying it.",
    )
    args = parser.parse_args()

    target = Path(args.target).resolve()
    target.mkdir(parents=True, exist_ok=True)
    workspace = init_workspace(target, with_readme=True, with_current_focus=True)

    draft_path = Path(args.draft)
    if not draft_path.is_absolute():
        draft_path = workspace / "wiki" / "drafts" / draft_path
    draft_path = draft_path.resolve()

    if not draft_path.exists():
        raise SystemExit(f"Draft not found: {draft_path}")

    draft_text = draft_path.read_text(encoding="utf-8")
    merge_content = extract_draft_merge_content(draft_text)
    if not merge_content:
        raise SystemExit(f"Draft has no mergeable content: {draft_path}")

    draft_target = draft_target_from_text(draft_text, draft_name=draft_path.name)
    wiki_path = resolve_target_path(workspace, draft_target)
    append_wiki_sync_content(wiki_path, merge_content)

    if not args.keep_draft:
        draft_path.unlink()

    refresh_wiki_registry(workspace)

    print(f"Applied HeroAgent wiki draft: {draft_path}")
    print(f"Updated HeroAgent wiki: {wiki_path}")
    if args.keep_draft:
        print("Draft retained.")
    else:
        print("Draft removed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
