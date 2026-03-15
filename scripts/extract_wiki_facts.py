#!/usr/bin/env python3
"""
Extract stable wiki facts from changed source paths and write them into drafts.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from common import draft_filename_for_target
from common import extract_source_facts
from common import init_workspace
from common import refresh_wiki_registry
from common import render_extracted_facts


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Extract stable wiki facts from changed source paths and write them into drafts.",
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
        help="Changed source path used to infer stable wiki facts. Can be passed multiple times.",
    )
    args = parser.parse_args()

    target = Path(args.target).resolve()
    target.mkdir(parents=True, exist_ok=True)
    workspace = init_workspace(target, with_readme=True, with_current_focus=True)
    extracted = extract_source_facts(target, args.changed_paths)

    drafts_dir = workspace / "wiki" / "drafts"
    drafts_dir.mkdir(parents=True, exist_ok=True)

    written: list[Path] = []
    for target_doc, facts in extracted.items():
        draft_path = drafts_dir / f"facts__{draft_filename_for_target(target_doc)}"
        draft_path.write_text(render_extracted_facts(target_doc, facts), encoding="utf-8")
        written.append(draft_path)

    refresh_wiki_registry(workspace, changed_paths=args.changed_paths)

    if written:
        print("Extracted HeroAgent wiki facts:")
        for path in written:
            print(path)
    else:
        print("No extractable wiki facts found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
