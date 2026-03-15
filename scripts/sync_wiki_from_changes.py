#!/usr/bin/env python3
"""
Create HeroAgent wiki draft updates from changed paths and refresh registry.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from common import create_wiki_sync_drafts
from common import init_workspace
from common import refresh_wiki_registry


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create HeroAgent wiki draft updates from changed paths and refresh registry.",
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
        help="Changed file path used to infer wiki draft updates. Can be passed multiple times.",
    )
    parser.add_argument(
        "--materialize-suggestions",
        action="store_true",
        help="Create missing suggested wiki files before generating drafts.",
    )
    args = parser.parse_args()

    target = Path(args.target).resolve()
    target.mkdir(parents=True, exist_ok=True)
    workspace = init_workspace(target, with_readme=True, with_current_focus=True)

    drafts, suggestions = create_wiki_sync_drafts(
        workspace=workspace,
        changed_paths=args.changed_paths,
        materialize_suggestions=args.materialize_suggestions,
    )
    index_path, registry_path, _ = refresh_wiki_registry(
        workspace=workspace,
        changed_paths=args.changed_paths,
        materialize_suggestions=args.materialize_suggestions,
    )

    if not suggestions:
        print("No wiki sync drafts created.")
        print(f"Refreshed HeroAgent wiki index: {index_path}")
        print(f"Refreshed HeroAgent wiki registry: {registry_path}")
        return 0

    print("Created HeroAgent wiki sync drafts:")
    for path in drafts:
        print(path)
    print(f"Refreshed HeroAgent wiki index: {index_path}")
    print(f"Refreshed HeroAgent wiki registry: {registry_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
