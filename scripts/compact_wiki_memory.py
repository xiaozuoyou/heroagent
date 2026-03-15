#!/usr/bin/env python3
"""
Compact HeroAgent wiki files by merging repeated auto-sync blocks into a summary.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from common import compact_wiki_content
from common import init_workspace
from common import refresh_wiki_registry


def iter_target_files(workspace: Path, scope: str) -> list[Path]:
    wiki_root = workspace / "wiki"
    files: list[Path] = []

    if scope in {"all", "core"}:
        for name in ("overview.md", "arch.md", "api.md", "data.md"):
            path = wiki_root / name
            if path.exists():
                files.append(path)

    if scope in {"all", "modules"}:
        files.extend(sorted((wiki_root / "modules").glob("*.md")))

    return files


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Compact HeroAgent wiki files by merging repeated auto-sync blocks into a summary.",
    )
    parser.add_argument(
        "target",
        nargs="?",
        default=".",
        help="Target project directory. Defaults to the current directory.",
    )
    parser.add_argument(
        "--scope",
        choices=["all", "core", "modules"],
        default="all",
        help="Which wiki files to compact. Defaults to all.",
    )
    args = parser.parse_args()

    target = Path(args.target).resolve()
    target.mkdir(parents=True, exist_ok=True)
    workspace = init_workspace(target, with_readme=True, with_current_focus=True)

    compacted: list[Path] = []
    for path in iter_target_files(workspace, args.scope):
        original = path.read_text(encoding="utf-8")
        updated = compact_wiki_content(original)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            compacted.append(path)

    refresh_wiki_registry(workspace)

    if compacted:
        print("Compacted HeroAgent wiki files:")
        for path in compacted:
            print(path)
    else:
        print("No wiki compaction needed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
