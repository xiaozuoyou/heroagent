#!/usr/bin/env python3
"""
Check whether a HeroAgent workspace is present and minimally healthy.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from common import REQUIRED_DIRS
from common import WORKSPACE_DIRNAME


REQUIRED_WIKI_FILES = [
    "index.md",
    "registry.json",
    "overview.md",
    "arch.md",
    "api.md",
    "data.md",
]

OPTIONAL_WIKI_DIRS = [
    "drafts",
    "modules",
]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check whether a HeroAgent workspace is present and minimally healthy.",
    )
    parser.add_argument(
        "target",
        nargs="?",
        default=".",
        help="Target project directory. Defaults to the current directory.",
    )
    args = parser.parse_args()

    target = Path(args.target).resolve()
    root = target / WORKSPACE_DIRNAME

    print(f"HeroAgent doctor target: {target}")

    if not root.exists():
        print("[FAIL] Missing .heroagent/")
        print("Suggested fix: run scripts/init_heroagent.py")
        return 1

    missing = []
    for name in REQUIRED_DIRS:
        path = root / name
        if path.exists() and path.is_dir():
            print(f"[OK] {path}")
        else:
            missing.append(path)
            print(f"[MISS] {path}")

    focus = root / "progress" / "current-focus.md"
    if focus.exists():
        print(f"[OK] {focus}")
    else:
        print(f"[MISS] {focus}")
        missing.append(focus)

    for filename in REQUIRED_WIKI_FILES:
        path = root / "wiki" / filename
        if path.exists():
            print(f"[OK] {path}")
        else:
            print(f"[MISS] {path}")
            missing.append(path)

    for dirname in OPTIONAL_WIKI_DIRS:
        path = root / "wiki" / dirname
        if path.exists() and path.is_dir():
            print(f"[OK] {path}")
        else:
            print(f"[WARN] Optional directory missing: {path}")

    readme = root / "README.md"
    if readme.exists():
        print(f"[OK] {readme}")
    else:
        print(f"[WARN] Optional file missing: {readme}")

    if missing:
        print("HeroAgent workspace check: INCOMPLETE")
        print("Suggested fix: run scripts/init_heroagent.py or补齐缺失文件")
        return 1

    print("HeroAgent workspace check: HEALTHY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
