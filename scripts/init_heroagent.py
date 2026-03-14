#!/usr/bin/env python3
"""
Initialize a .heroagent workspace in a target project.
"""

from __future__ import annotations

import argparse
from pathlib import Path


DIRS = [
    "goals",
    "plans",
    "tasks",
    "progress",
    "retros",
    "principles",
    "processes",
    "archive",
]

README_CONTENT = """# .heroagent

This workspace stores goal execution artifacts for HeroAgent.

## Directories

- goals: goal cards
- plans: milestone plans
- tasks: executable task lists
- progress: progress snapshots and current focus
- retros: retrospectives
- principles: reusable principles
- processes: reusable workflows
- archive: closed or abandoned work
"""

CURRENT_FOCUS_CONTENT = """## 进度快照

- 当前目标：
- 当前阶段：
- 已完成：
- 进行中：
- 阻塞：
- 下一步：
"""


def write_if_missing(path: Path, content: str) -> None:
    if not path.exists():
        path.write_text(content, encoding="utf-8")


def touch_if_missing(path: Path) -> None:
    if not path.exists():
        path.touch()


def init_workspace(target: Path, with_readme: bool, with_current_focus: bool) -> Path:
    root = target / ".heroagent"
    root.mkdir(parents=True, exist_ok=True)

    for name in DIRS:
        directory = root / name
        directory.mkdir(exist_ok=True)
        touch_if_missing(directory / ".gitkeep")

    if with_readme:
        write_if_missing(root / "README.md", README_CONTENT)

    if with_current_focus:
        write_if_missing(root / "progress" / "current-focus.md", CURRENT_FOCUS_CONTENT)

    return root


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
