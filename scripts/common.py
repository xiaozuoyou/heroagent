#!/usr/bin/env python3
"""
Shared helpers for HeroAgent scripts.
"""

from __future__ import annotations

from datetime import datetime
import hashlib
from pathlib import Path
import re


WORKSPACE_DIRNAME = ".heroagent"
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

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
TEMPLATES_DIR = REPO_ROOT / "assets" / "templates"

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


def timestamp_now() -> str:
    return datetime.now().strftime("%Y%m%d%H%M")


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", text.strip().lower()).strip("-")
    if slug:
        return slug

    digest = hashlib.sha1(text.strip().encode("utf-8")).hexdigest()[:8]
    return f"goal-{digest}"


def write_if_missing(path: Path, content: str) -> None:
    if not path.exists():
        path.write_text(content, encoding="utf-8")


def touch_if_missing(path: Path) -> None:
    if not path.exists():
        path.touch()


def safe_write(path: Path, content: str) -> Path:
    if not path.exists():
        path.write_text(content, encoding="utf-8")
        return path

    stem = path.stem
    suffix = path.suffix
    index = 1
    while True:
        candidate = path.parent / f"{stem}-{index}{suffix}"
        if not candidate.exists():
            candidate.write_text(content, encoding="utf-8")
            return candidate
        index += 1


def read_template(name: str) -> str:
    return (TEMPLATES_DIR / name).read_text(encoding="utf-8")


def fill_named_fields(template: str, fields: dict[str, str]) -> str:
    result = template
    for label, value in fields.items():
        pattern = rf"(^-\s+{re.escape(label)}[：:].*)$"
        replacement = f"- {label}：{value}"
        result = re.sub(pattern, replacement, result, count=1, flags=re.MULTILINE)
    return result


def fill_next_step(template: str, value: str) -> str:
    result = fill_named_fields(template, {"下一步": value})
    if result != template:
        return result

    lines = result.splitlines()
    for index, line in enumerate(lines):
        if line.strip() == "## 下一步":
            for bullet_index in range(index + 1, len(lines)):
                if lines[bullet_index].startswith("- "):
                    lines[bullet_index] = f"- {value}"
                    return "\n".join(lines) + ("\n" if result.endswith("\n") else "")
    return result


def render_template(
    template_name: str,
    fields: dict[str, str] | None = None,
    next_step: str | None = None,
) -> str:
    result = read_template(template_name)
    if fields:
        result = fill_named_fields(result, fields)
    if next_step is not None:
        result = fill_next_step(result, next_step)
    return result


def render_blank_focus() -> str:
    return render_template(
        "progress-snapshot.md",
        fields={
            "当前目标": "",
            "当前阶段": "",
            "已完成": "",
            "进行中": "",
            "阻塞": "",
            "下一步": "",
        },
    )


def init_workspace(target: Path, with_readme: bool, with_current_focus: bool) -> Path:
    root = target / WORKSPACE_DIRNAME
    root.mkdir(parents=True, exist_ok=True)

    for name in REQUIRED_DIRS:
        directory = root / name
        directory.mkdir(exist_ok=True)
        touch_if_missing(directory / ".gitkeep")

    if with_readme:
        write_if_missing(root / "README.md", README_CONTENT)

    if with_current_focus:
        write_if_missing(root / "progress" / "current-focus.md", render_blank_focus())

    return root
