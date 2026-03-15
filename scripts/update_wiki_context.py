#!/usr/bin/env python3
"""
Update HeroAgent wiki files in a target project.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from common import ensure_wiki_section_path
from common import init_workspace
from common import refresh_wiki_registry


WIKI_FILES = {"overview", "arch", "api", "data"}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Update HeroAgent wiki files in a target project.",
    )
    parser.add_argument(
        "--section",
        choices=sorted(WIKI_FILES),
        help="Core wiki section to update.",
    )
    parser.add_argument(
        "--module",
        help="Module wiki to update under .heroagent/wiki/modules/<module>.md.",
    )
    parser.add_argument(
        "--content",
        required=True,
        help="Markdown content appended to the selected wiki file.",
    )
    parser.add_argument(
        "target",
        nargs="?",
        default=".",
        help="Target project directory. Defaults to the current directory.",
    )
    args = parser.parse_args()

    if not args.section and not args.module:
        parser.error("one of --section or --module is required")
    if args.section and args.module:
        parser.error("--section and --module cannot be used together")

    target = Path(args.target).resolve()
    target.mkdir(parents=True, exist_ok=True)
    workspace = init_workspace(target, with_readme=True, with_current_focus=True)

    path = ensure_wiki_section_path(
        workspace=workspace,
        section=args.section,
        module_name=args.module,
    )
    existing = path.read_text(encoding="utf-8").rstrip()
    appended = f"{existing}\n\n{args.content.strip()}\n"
    path.write_text(appended, encoding="utf-8")
    refresh_wiki_registry(workspace)

    print(f"Updated HeroAgent wiki: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
