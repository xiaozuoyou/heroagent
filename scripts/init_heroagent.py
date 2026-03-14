#!/usr/bin/env python3
"""
Initialize a .heroagent workspace in a target project.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from common import init_workspace


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Initialize a .heroagent workspace in a target project.",
    )
    parser.add_argument(
        "target",
        nargs="?",
        default=".",
        help="Target project directory. Defaults to the current directory.",
    )
    parser.add_argument(
        "--no-readme",
        action="store_true",
        help="Do not create .heroagent/README.md",
    )
    parser.add_argument(
        "--no-current-focus",
        action="store_true",
        help="Do not create .heroagent/progress/current-focus.md",
    )
    args = parser.parse_args()

    target = Path(args.target).resolve()
    target.mkdir(parents=True, exist_ok=True)

    root = init_workspace(
        target=target,
        with_readme=not args.no_readme,
        with_current_focus=not args.no_current_focus,
    )

    print(f"Initialized HeroAgent workspace at: {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
