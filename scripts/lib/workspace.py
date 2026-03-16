from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime
from pathlib import Path

from .shared_data import README_CONTENT
from .shared_data import REQUIRED_DIRS
from .shared_data import TEMPLATES_DIR
from .shared_data import WIKI_API_CONTENT
from .shared_data import WIKI_ARCH_CONTENT
from .shared_data import WIKI_CORE_FILES
from .shared_data import WIKI_DATA_CONTENT
from .shared_data import WIKI_OVERVIEW_CONTENT
from .shared_data import WORKFLOW_STATE_CONTENT
from .shared_data import WORKSPACE_DIRNAME


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
    path.parent.mkdir(parents=True, exist_ok=True)
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


def blank_workflow_state() -> dict[str, object]:
    return {
        "current_goal": "",
        "goal_definition": "",
        "active_plan_path": "",
        "plan_summary": "",
        "plan_confirmed": False,
        "current_object": "",
        "current_stage": "",
        "workflow_mode": "",
        "complexity_level": "",
        "stage_status": "",
        "next_action": "",
        "pending_choice": [],
        "latest_score": 0,
        "current_question": "",
        "goal_confirmed": False,
        "reflect_status": "",
        "pending_reflect_reason": "",
        "pending_realize": False,
        "last_reflect_at": "",
        "last_realize_at": "",
        "wiki_status": "fresh",
        "pending_wiki_targets": [],
        "last_wiki_detected_at": "",
        "last_wiki_detected_paths": [],
        "last_wiki_sync_at": "",
        "last_wiki_sync_strategy": "",
        "last_wiki_sync_paths": [],
        "updated_at": "",
    }


def load_workflow_state(workspace: Path) -> dict[str, object]:
    path = workspace / "progress" / "workflow-state.json"
    if not path.exists():
        path.write_text(WORKFLOW_STATE_CONTENT, encoding="utf-8")
        return blank_workflow_state()
    state = blank_workflow_state()
    state.update(json.loads(path.read_text(encoding="utf-8")))
    return state


def save_workflow_state(workspace: Path, state: dict[str, object]) -> Path:
    path = workspace / "progress" / "workflow-state.json"
    state = dict(state)
    state["updated_at"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def init_workspace(target: Path, with_readme: bool, with_current_focus: bool) -> Path:
    from .wiki_ops import refresh_wiki_registry

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
    write_if_missing(root / "progress" / "workflow-state.json", WORKFLOW_STATE_CONTENT)

    write_if_missing(root / "wiki" / WIKI_CORE_FILES["overview"], WIKI_OVERVIEW_CONTENT)
    write_if_missing(root / "wiki" / WIKI_CORE_FILES["arch"], WIKI_ARCH_CONTENT)
    write_if_missing(root / "wiki" / WIKI_CORE_FILES["api"], WIKI_API_CONTENT)
    write_if_missing(root / "wiki" / WIKI_CORE_FILES["data"], WIKI_DATA_CONTENT)

    index_path = root / "wiki" / "index.md"
    registry_path = root / "wiki" / "registry.json"
    if not index_path.exists() or not registry_path.exists():
        refresh_wiki_registry(root)

    return root
