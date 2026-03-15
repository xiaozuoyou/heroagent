#!/usr/bin/env python3
"""
Refresh HeroAgent wiki index and registry for AI-first consumption.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from common import init_workspace
from common import refresh_wiki_registry


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Refresh HeroAgent wiki index and registry for AI-first consumption.",
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
        help="Changed file path used to infer wiki freshness. Can be passed multiple times.",
    )
    parser.add_argument(
        "--materialize-suggestions",
        action="store_true",
        help="Create missing suggested wiki files before refreshing the registry.",
    )
    args = parser.parse_args()

    target = Path(args.target).resolve()
    target.mkdir(parents=True, exist_ok=True)
    workspace = init_workspace(target, with_readme=True, with_current_focus=True)
    index_path, registry_path, suggestions = refresh_wiki_registry(
        workspace=workspace,
        changed_paths=args.changed_paths,
        materialize_suggestions=args.materialize_suggestions,
    )

    print(f"Refreshed HeroAgent wiki index: {index_path}")
    print(f"Refreshed HeroAgent wiki registry: {registry_path}")
    if suggestions:
        print("Suggested wiki updates:")
        for item in suggestions:
            print(f"- {item}")
    else:
        print("Suggested wiki updates: none")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
