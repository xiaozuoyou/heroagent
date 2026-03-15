#!/usr/bin/env python3
"""
Archive HeroAgent goal artifacts into .heroagent/archive/.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import shutil

from common import init_workspace
from common import render_blank_focus
from common import timestamp_now


def safe_archive_dir(base: Path, name: str) -> Path:
    candidate = base / name
    if not candidate.exists():
        candidate.mkdir(parents=True, exist_ok=True)
        return candidate

    index = 1
    while True:
        next_candidate = base / f"{name}-{index}"
        if not next_candidate.exists():
            next_candidate.mkdir(parents=True, exist_ok=True)
            return next_candidate
        index += 1


def maybe_move(path: Path, archive_dir: Path, folder: str, moved: list[Path]) -> None:
    if not path.exists():
        return
    destination = archive_dir / f"{folder}__{path.name}"
    if destination.exists():
        destination = archive_dir / f"{folder}__{path.stem}-archived{path.suffix}"
    shutil.move(str(path), str(destination))
    moved.append(destination)


def is_archivable_progress(path: Path, slug: str) -> bool:
    if path.name in {"current-focus.md", "workflow-state.json", ".gitkeep"}:
        return False
    if path.suffix != ".md":
        return False
    return slug in path.name


def reset_current_focus(path: Path) -> None:
    path.write_text(render_blank_focus(), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Archive HeroAgent goal artifacts into .heroagent/archive/.",
    )
    parser.add_argument("--slug", required=True, help="Goal slug used in related file names.")
    parser.add_argument(
        "--archive-name",
        default="",
        help="Optional archive directory name. Defaults to {timestamp}_{slug}.",
    )
    parser.add_argument(
        "--reset-focus",
        action="store_true",
        help="Reset progress/current-focus.md after archiving.",
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

    archive_root = workspace / "archive"
    archive_name = args.archive_name or f"{timestamp_now()}_{args.slug}"
    archive_dir = safe_archive_dir(archive_root, archive_name)

    moved: list[Path] = []
    for folder in ("goals", "plans", "tasks", "retros"):
        for path in (workspace / folder).glob(f"*{args.slug}*.md"):
            maybe_move(path, archive_dir, folder, moved)

    for path in sorted((workspace / "progress").glob("*.md")):
        if is_archivable_progress(path, args.slug):
            maybe_move(path, archive_dir, "progress", moved)

    focus_path = workspace / "progress" / "current-focus.md"
    if args.reset_focus:
        reset_current_focus(focus_path)

    print(f"Archived HeroAgent artifacts to: {archive_dir}")
    for path in moved:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
