#!/usr/bin/env python3
"""
Check whether a HeroAgent workspace is present and minimally healthy.
"""

from __future__ import annotations

import argparse
from pathlib import Path


REQUIRED_DIRS = [
    "goals",
    "plans",
    "tasks",
    "progress",
    "retros",
    "principles",
    "processes",
    "archive",
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
    root = target / ".heroagent"

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
