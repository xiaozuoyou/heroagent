#!/usr/bin/env python3
"""
Suggest HeroAgent wiki files to refresh based on changed paths.
"""

from __future__ import annotations

import argparse

from common import suggest_wiki_targets


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Suggest HeroAgent wiki files to refresh based on changed paths.",
    )
    parser.add_argument(
        "paths",
        nargs="+",
        help="Changed file paths used to infer which wiki files should be updated.",
    )
    args = parser.parse_args()

    suggestions = suggest_wiki_targets(args.paths)
    if not suggestions:
        print("No wiki updates suggested.")
        return 0

    print("Suggested wiki updates:")
    for item in suggestions:
        print(f"- {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
