#!/usr/bin/env python3
"""
Refresh HeroAgent wiki registry and print the highest-priority wiki documents.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from common import init_workspace
from common import load_wiki_registry
from common import refresh_wiki_registry


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Refresh HeroAgent wiki registry and print the highest-priority wiki documents.",
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
        help="Changed file path used to refresh wiki signals. Can be passed multiple times.",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=5,
        help="How many top wiki documents to print. Defaults to 5.",
    )
    args = parser.parse_args()

    target = Path(args.target).resolve()
    target.mkdir(parents=True, exist_ok=True)
    workspace = init_workspace(target, with_readme=True, with_current_focus=True)
    refresh_wiki_registry(workspace, changed_paths=args.changed_paths)
    registry = load_wiki_registry(workspace)

    documents = registry.get("documents", [])[: args.top]
    print("Top HeroAgent wiki signals:")
    for doc in documents:
        signals = doc["signals"]
        print(
            f"- {doc['path']} | priority={signals['priority_score']} | "
            f"freshness={signals['freshness_score']} | density={signals['density_score']} | "
            f"draft_dependency={signals['draft_dependency_score']} | status={doc['status']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
