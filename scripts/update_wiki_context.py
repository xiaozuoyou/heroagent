#!/usr/bin/env python3
"""
Update HeroAgent wiki files in a target project.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from common import init_workspace


WIKI_FILES = {"overview", "arch", "api", "data"}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Update HeroAgent wiki files in a target project.",
    )
    parser.add_argument(
        "--section",
        required=True,
        choices=sorted(WIKI_FILES),
        help="Wiki section to update.",
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

    target = Path(args.target).resolve()
    target.mkdir(parents=True, exist_ok=True)
    workspace = init_workspace(target, with_readme=True, with_current_focus=True)

    path = workspace / "wiki" / f"{args.section}.md"
    existing = path.read_text(encoding="utf-8").rstrip()
    appended = f"{existing}\n\n{args.content.strip()}\n"
    path.write_text(appended, encoding="utf-8")

    print(f"Updated HeroAgent wiki: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
