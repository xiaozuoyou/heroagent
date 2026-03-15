#!/usr/bin/env python3
"""
Update HeroAgent workflow wiki sync state based on changed paths.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from common import init_workspace
from common import refresh_workflow_wiki_state


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Update HeroAgent workflow wiki sync state based on changed paths.",
    )
    parser.add_argument(
        "--changed-path",
        dest="changed_paths",
        action="append",
        default=[],
        help="Changed file path used to infer whether wiki needs syncing. Can be passed multiple times.",
    )
    parser.add_argument(
        "--mark-synced",
        action="store_true",
        help="Mark the current changed paths as already synced into formal wiki files.",
    )
    parser.add_argument(
        "--strategy",
        default="",
        help="Wiki sync strategy used when marking synced, such as balanced or aggressive.",
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
    path, state = refresh_workflow_wiki_state(
        workspace,
        changed_paths=args.changed_paths,
        mark_synced=args.mark_synced,
        strategy=args.strategy,
    )

    print(f"Updated HeroAgent wiki signal state: {path}")
    print(f"Wiki status: {state['wiki_status']}")
    pending = state.get("pending_wiki_targets", [])
    if pending:
        print("Pending wiki targets:")
        for item in pending:
            print(f"- {item}")
    else:
        print("Pending wiki targets: none")

    if args.mark_synced:
        strategy = args.strategy or "manual"
        print(f"Recorded wiki sync strategy: {strategy}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
