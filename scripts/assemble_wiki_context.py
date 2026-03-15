#!/usr/bin/env python3
"""
Assemble the most relevant HeroAgent wiki context bundle for a given action.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from common import assemble_wiki_context
from common import init_workspace
from common import refresh_wiki_registry


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Assemble the most relevant HeroAgent wiki context bundle for a given action.",
    )
    parser.add_argument(
        "action",
        choices=["wiki", "want", "plan", "todo", "focus", "reflect"],
        help="HeroAgent action used to choose the wiki context bundle.",
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
        help="Changed file path used to refresh wiki signals before assembling context.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=5,
        help="Maximum number of wiki docs to include. Defaults to 5.",
    )
    args = parser.parse_args()

    target = Path(args.target).resolve()
    target.mkdir(parents=True, exist_ok=True)
    workspace = init_workspace(target, with_readme=True, with_current_focus=True)
    refresh_wiki_registry(workspace, changed_paths=args.changed_paths)

    bundle = assemble_wiki_context(workspace, action=args.action, limit=args.limit)
    print(f"HeroAgent wiki context bundle for {args.action}:")
    for doc in bundle:
        signals = doc["signals"]
        print(
            f"- {doc['path']} | kind={doc['kind']} | status={doc['status']} | "
            f"priority={signals['priority_score']} | summary={doc['summary']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
