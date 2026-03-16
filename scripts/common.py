#!/usr/bin/env python3
"""
Shared helpers for HeroAgent scripts.
"""

from __future__ import annotations

import json
from datetime import datetime
from datetime import timedelta
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
    "archive",
    "wiki",
    "wiki/drafts",
    "wiki/modules",
]

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
TEMPLATES_DIR = REPO_ROOT / "assets" / "templates"

README_CONTENT = """# .heroagent

这个工作区用于维护目标推进、问题复盘和项目知识。

## 公开动作

- `want -> plan -> todo -> achieve | abandon`：目标推进主流程
- `focus`：当前态势观察动作
- `wiki`：知识维护与知识消费入口
- `reflect`：问题复盘入口

执行规则：

- `plan`：负责继续沟通并写出可确认的本地计划文档
- `todo`：基于已确认计划文档开始执行
- `focus`：处理当前态势，不改变推进决定

## 内部方法

- `realize`：复盘结论确认后，沉淀到 `principles/`
- `synthesize`：压缩长记录、提炼一句话经验
- `forget`：淘汰旧知识、旧需求结论和失效约束
- `master`：沉淀项目级或 HeroAgent 级执行标准

## 目录说明

- `goals/`：目标卡
- `plans/`：已确认的计划文档
- `tasks/`：执行留痕，可选
- `progress/`：当前焦点与状态
- `retros/`：复盘记录
- `principles/`：已确认的稳定经验
- `archive/`：已完成或已放弃目标的归档
- `wiki/`：项目知识与上下文
"""

WORKFLOW_STATE_CONTENT = """{
  "current_goal": "",
  "current_object": "",
  "current_stage": "",
  "workflow_mode": "",
  "complexity_level": "",
  "stage_status": "",
  "next_action": "",
  "pending_choice": [],
  "latest_score": 0,
  "current_question": "",
  "reflect_status": "",
  "pending_reflect_reason": "",
  "pending_realize": false,
  "last_reflect_at": "",
  "last_realize_at": "",
  "wiki_status": "fresh",
  "pending_wiki_targets": [],
  "last_wiki_detected_at": "",
  "last_wiki_detected_paths": [],
  "last_wiki_sync_at": "",
  "last_wiki_sync_strategy": "",
  "last_wiki_sync_paths": [],
  "updated_at": ""
}
"""

WIKI_OVERVIEW_CONTENT = """# 项目概览

## 目标

- 

## 模块总览

- 

## 当前重点

- 
"""

WIKI_ARCH_CONTENT = """# 架构设计

## 核心结构

- 

## 关键模块关系

- 

## 架构约束

- 
"""

WIKI_API_CONTENT = """# API 手册

## 对外接口

- 

## 关键约定

- 
"""

WIKI_DATA_CONTENT = """# 数据模型

## 核心实体

- 

## 关键字段约束

- 
"""

WIKI_MODULE_TEMPLATE = """# 模块说明

## 模块职责

- 

## 对外接口

- 

## 关键依赖

- 

## 约束与注意事项

- 
"""

WIKI_CORE_FILES = {
    "overview": "overview.md",
    "arch": "arch.md",
    "api": "api.md",
    "data": "data.md",
}

WIKI_CORE_SUMMARIES = {
    "overview.md": "项目目标、模块总览与当前重点。",
    "arch.md": "架构关系、技术边界与关键约束。",
    "api.md": "对外接口、调用约定与集成边界。",
    "data.md": "核心实体、字段约束与数据流。",
}

OVERVIEW_FILENAMES = {
    "readme.md",
    "package.json",
    "pyproject.toml",
    "cargo.toml",
    "go.mod",
    "pom.xml",
    "build.gradle",
    "build.gradle.kts",
    "makefile",
}

API_HINTS = {
    "api",
    "apis",
    "route",
    "routes",
    "router",
    "routers",
    "controller",
    "controllers",
    "endpoint",
    "endpoints",
    "openapi",
    "graphql",
    "rpc",
}

DATA_HINTS = {
    "db",
    "database",
    "data",
    "schema",
    "schemas",
    "migration",
    "migrations",
    "model",
    "models",
    "entity",
    "entities",
    "prisma",
    "sql",
}

ARCH_HINTS = {
    "infra",
    "infrastructure",
    "deploy",
    "deployment",
    "docker",
    "k8s",
    "helm",
    "terraform",
    "config",
    "configs",
    "nginx",
    "compose",
}

MODULE_ROOTS = {"src", "app", "apps", "services", "modules", "packages", "pkg"}
GENERIC_SEGMENTS = {
    "src",
    "app",
    "apps",
    "services",
    "modules",
    "packages",
    "pkg",
    "lib",
    "libs",
    "backend",
    "frontend",
    "client",
    "server",
    "internal",
    "core",
    "shared",
    "common",
    "components",
    "tests",
    "test",
    "spec",
    "specs",
    "scripts",
    "docs",
    "doc",
    ".github",
    ".heroagent",
    "wiki",
    "progress",
    "archive",
}
TOP_LEVEL_SKIP_SEGMENTS = GENERIC_SEGMENTS | {
    "dist",
    "build",
    "coverage",
    "public",
    "assets",
    "static",
    "vendor",
    "node_modules",
}

CORE_WIKI_ORDER = {
    "overview.md": 0,
    "arch.md": 1,
    "api.md": 2,
    "data.md": 3,
}

WIKI_DRAFT_FOCUSES = {
    "overview.md": [
        "本轮项目级变化是什么",
        "哪些模块或工作重点发生了变化",
        "这些变化为什么值得写入项目概览",
    ],
    "arch.md": [
        "本轮架构或部署结构发生了什么变化",
        "新增或调整了哪些依赖关系",
        "是否引入了新的约束、边界或技术决策",
    ],
    "api.md": [
        "新增、修改或删除了哪些接口",
        "接口契约、调用方式或返回结构有什么变化",
        "是否存在兼容性影响或调用约定变化",
    ],
    "data.md": [
        "哪些实体、字段或迁移发生了变化",
        "这些变化会影响哪些读写流程",
        "是否新增了数据约束或一致性要求",
    ],
}

ACTION_CONTEXT_HINTS = {
    "wiki": {"overview.md", "arch.md", "api.md", "data.md"},
    "want": {"overview.md", "arch.md"},
    "plan": {"overview.md", "arch.md"},
    "todo": {"api.md", "data.md"},
    "focus": {"overview.md", "arch.md"},
    "reflect": {"arch.md", "data.md"},
}

STATUS_BASE_SCORES = {
    "needs_update": 80,
    "seed": 65,
    "draft": 55,
    "report": 20,
    "active": 35,
}

WIKI_STRATEGIES = {
    "conservative": {
        "materialize_missing": False,
        "apply_ready": False,
        "mark_stale": False,
        "extract_facts": False,
        "compact_memory": False,
    },
    "balanced": {
        "materialize_missing": True,
        "apply_ready": False,
        "mark_stale": True,
        "extract_facts": True,
        "compact_memory": False,
    },
    "aggressive": {
        "materialize_missing": True,
        "apply_ready": True,
        "mark_stale": True,
        "extract_facts": True,
        "compact_memory": True,
    },
}


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
    write_if_missing(root / "progress" / "workflow-state.json", WORKFLOW_STATE_CONTENT)

    write_if_missing(root / "wiki" / "overview.md", WIKI_OVERVIEW_CONTENT)
    write_if_missing(root / "wiki" / "arch.md", WIKI_ARCH_CONTENT)
    write_if_missing(root / "wiki" / "api.md", WIKI_API_CONTENT)
    write_if_missing(root / "wiki" / "data.md", WIKI_DATA_CONTENT)

    index_path = root / "wiki" / "index.md"
    registry_path = root / "wiki" / "registry.json"
    if not index_path.exists() or not registry_path.exists():
        refresh_wiki_registry(root)

    return root


def blank_workflow_state() -> dict[str, object]:
    return {
        "current_goal": "",
        "current_object": "",
        "current_stage": "",
        "workflow_mode": "",
        "complexity_level": "",
        "stage_status": "",
        "next_action": "",
        "pending_choice": [],
        "latest_score": 0,
        "current_question": "",
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


def refresh_workflow_wiki_state(
    workspace: Path,
    changed_paths: list[str] | None = None,
    *,
    mark_synced: bool = False,
    strategy: str = "",
) -> tuple[Path, dict[str, object]]:
    changed_paths = changed_paths or []
    state = load_workflow_state(workspace)
    current_pending = {
        str(item)
        for item in state.get("pending_wiki_targets", [])
        if isinstance(item, str) and item
    }
    suggested_targets = set(suggest_wiki_targets(changed_paths))
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    if changed_paths:
        state["last_wiki_detected_at"] = now
        state["last_wiki_detected_paths"] = changed_paths

    if mark_synced:
        resolved_targets = suggested_targets or current_pending
        pending_targets = sorted(current_pending - resolved_targets)
        state["last_wiki_sync_at"] = now
        state["last_wiki_sync_strategy"] = strategy
        state["last_wiki_sync_paths"] = changed_paths
    else:
        pending_targets = sorted(current_pending | suggested_targets)

    state["pending_wiki_targets"] = pending_targets
    state["wiki_status"] = "needs_sync" if pending_targets else "fresh"
    path = save_workflow_state(workspace, state)
    return path, state


def split_path_parts(raw_path: str) -> list[str]:
    return [part for part in raw_path.replace("\\", "/").split("/") if part not in {"", "."}]


def normalize_module_name(segment: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_-]+", "-", segment.strip().lower()).strip("-_")


def detect_module_target(parts: list[str]) -> str | None:
    if len(parts) < 2:
        return None

    lowered = [part.lower() for part in parts]
    stemmed = lowered[:-1]

    for index, segment in enumerate(stemmed):
        if segment not in MODULE_ROOTS:
            continue

        for candidate in parts[index + 1 : -1]:
            normalized = normalize_module_name(candidate)
            if (
                normalized
                and normalized not in GENERIC_SEGMENTS
                and normalized not in API_HINTS
                and normalized not in DATA_HINTS
                and normalized not in ARCH_HINTS
            ):
                return f"modules/{normalized}.md"

    top_level = normalize_module_name(parts[0])
    if top_level and top_level not in TOP_LEVEL_SKIP_SEGMENTS:
        return f"modules/{top_level}.md"

    return None


def suggest_wiki_targets(changed_paths: list[str]) -> list[str]:
    targets: set[str] = set()

    for raw_path in changed_paths:
        parts = split_path_parts(raw_path)
        if not parts:
            continue

        lowered = [part.lower() for part in parts]
        filename = lowered[-1]

        if lowered[:2] == [WORKSPACE_DIRNAME, "wiki"]:
            continue

        if filename in OVERVIEW_FILENAMES or lowered[0] in {"docs", ".github"}:
            targets.add("overview.md")

        if any(part in ARCH_HINTS for part in lowered) or filename in {
            "dockerfile",
            "docker-compose.yml",
            "docker-compose.yaml",
        }:
            targets.add("arch.md")

        if any(part in API_HINTS for part in lowered):
            targets.add("api.md")

        if any(part in DATA_HINTS for part in lowered) or filename.endswith((".sql", ".prisma")):
            targets.add("data.md")

        module_target = detect_module_target(parts)
        if module_target:
            targets.add(module_target)

    return sorted(
        targets,
        key=lambda item: (CORE_WIKI_ORDER.get(item, 99), item),
    )


def ensure_wiki_section_path(
    workspace: Path,
    section: str | None = None,
    module_name: str | None = None,
) -> Path:
    wiki_root = workspace / "wiki"

    if section:
        filename = WIKI_CORE_FILES[section]
        path = wiki_root / filename
        if section == "overview":
            write_if_missing(path, WIKI_OVERVIEW_CONTENT)
        elif section == "arch":
            write_if_missing(path, WIKI_ARCH_CONTENT)
        elif section == "api":
            write_if_missing(path, WIKI_API_CONTENT)
        elif section == "data":
            write_if_missing(path, WIKI_DATA_CONTENT)
        return path

    if not module_name:
        raise ValueError("module_name is required when section is not provided")

    normalized = normalize_module_name(module_name)
    if not normalized:
        raise ValueError("module_name must contain at least one alphanumeric character")

    modules_dir = wiki_root / "modules"
    modules_dir.mkdir(parents=True, exist_ok=True)
    path = modules_dir / f"{normalized}.md"
    write_if_missing(path, WIKI_MODULE_TEMPLATE)
    return path


def wiki_doc_status(path: Path, suggested_updates: set[str]) -> str:
    relative_path = path.as_posix()
    if relative_path in suggested_updates:
        return "needs_update"

    lines = [line.strip() for line in path.read_text(encoding="utf-8").splitlines()]
    meaningful_lines = [
        line
        for line in lines
        if line
        and not line.startswith("#")
        and line not in {"-"}
    ]
    if not meaningful_lines:
        return "seed"
    return "active"


def wiki_doc_summary(relative_path: str) -> str:
    if relative_path in WIKI_CORE_SUMMARIES:
        return WIKI_CORE_SUMMARIES[relative_path]

    module_name = Path(relative_path).stem
    return f"模块 {module_name} 的职责、接口、依赖与注意事项。"


def wiki_doc_kind(relative_path: str) -> str:
    if relative_path.startswith("modules/"):
        return "module"
    return "core"


def wiki_doc_topic(relative_path: str) -> str:
    if relative_path.startswith("modules/"):
        return Path(relative_path).stem
    return Path(relative_path).stem


def score_wiki_document(doc: dict[str, object]) -> dict[str, object]:
    status = str(doc["status"])
    related_changed_paths = list(doc.get("related_changed_paths", []))
    summary = str(doc.get("summary", ""))
    path = str(doc["path"])

    freshness_score = STATUS_BASE_SCORES.get(status, 30)
    if related_changed_paths:
        freshness_score += min(len(related_changed_paths) * 8, 16)

    density_score = 40
    if "自动同步摘要" in summary:
        density_score += 10
    if status == "seed":
        density_score = 20
    elif status == "report":
        density_score = 15
    elif status == "draft":
        density_score = 30

    draft_dependency_score = 0
    if status == "draft":
        draft_dependency_score = 75
    elif status == "needs_update":
        draft_dependency_score = 45
    elif path.startswith("modules/"):
        draft_dependency_score = 35
    else:
        draft_dependency_score = 20

    priority_score = min(
        100,
        round(freshness_score * 0.45 + density_score * 0.2 + draft_dependency_score * 0.35),
    )

    return {
        "freshness_score": freshness_score,
        "density_score": density_score,
        "draft_dependency_score": draft_dependency_score,
        "priority_score": priority_score,
    }


def build_wiki_registry(
    workspace: Path,
    changed_paths: list[str] | None = None,
) -> dict[str, object]:
    changed_paths = changed_paths or []
    suggestions = suggest_wiki_targets(changed_paths)
    suggested_updates = set(suggestions)
    wiki_root = workspace / "wiki"

    documents: list[dict[str, object]] = []

    for filename in ("overview.md", "arch.md", "api.md", "data.md"):
        path = wiki_root / filename
        if not path.exists():
            continue

        relative_path = filename
        related_changes = [
            raw_path
            for raw_path in changed_paths
            if relative_path in suggest_wiki_targets([raw_path])
        ]
        documents.append(
            {
                "path": relative_path,
                "kind": wiki_doc_kind(relative_path),
                "topic": wiki_doc_topic(relative_path),
                "status": wiki_doc_status(path, suggested_updates),
                "summary": wiki_doc_summary(relative_path),
                "last_modified": datetime.fromtimestamp(path.stat().st_mtime).strftime(
                    "%Y-%m-%dT%H:%M:%S"
                ),
                "related_changed_paths": related_changes,
            }
        )
        documents[-1]["signals"] = score_wiki_document(documents[-1])

    modules_dir = wiki_root / "modules"
    for path in sorted(modules_dir.glob("*.md")):
        relative_path = path.relative_to(wiki_root).as_posix()
        related_changes = [
            raw_path
            for raw_path in changed_paths
            if relative_path in suggest_wiki_targets([raw_path])
        ]
        documents.append(
            {
                "path": relative_path,
                "kind": wiki_doc_kind(relative_path),
                "topic": wiki_doc_topic(relative_path),
                "status": wiki_doc_status(path, suggested_updates),
                "summary": wiki_doc_summary(relative_path),
                "last_modified": datetime.fromtimestamp(path.stat().st_mtime).strftime(
                    "%Y-%m-%dT%H:%M:%S"
                ),
                "related_changed_paths": related_changes,
            }
        )
        documents[-1]["signals"] = score_wiki_document(documents[-1])

    drafts_dir = wiki_root / "drafts"
    for path in sorted(drafts_dir.glob("*")):
        if not path.is_file():
            continue

        relative_path = path.relative_to(wiki_root).as_posix()
        kind = "draft"
        status = "draft"
        summary = "基于代码变更自动生成的待补写草稿。"
        if path.name == "maintenance-report.md":
            kind = "report"
            status = "report"
            summary = "wiki 维护状态，列出缺失草稿、陈旧草稿与可合并草稿。"
        documents.append(
            {
                "path": relative_path,
                "kind": kind,
                "topic": path.stem.replace("__", " -> "),
                "status": status,
                "summary": summary,
                "last_modified": datetime.fromtimestamp(path.stat().st_mtime).strftime(
                    "%Y-%m-%dT%H:%M:%S"
                ),
                "related_changed_paths": [],
            }
        )
        documents[-1]["signals"] = score_wiki_document(documents[-1])

    documents.sort(
        key=lambda item: (
            -int(item.get("signals", {}).get("priority_score", 0)),
            item["path"],
        )
    )

    return {
        "generated_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "workspace": workspace.as_posix(),
        "changed_paths": changed_paths,
        "suggested_updates": suggestions,
        "documents": documents,
    }


def render_wiki_index(registry: dict[str, object]) -> str:
    suggested_updates = registry["suggested_updates"]
    documents = registry["documents"]

    lines = [
        "# Wiki 索引",
        "",
        "## 读取顺序",
        "1. 先读本索引，确定当前应读取哪些文档。",
        "2. 再读 `overview.md` 与 `arch.md` 获取项目级背景。",
        "3. 最后按任务需要补读模块、API、数据文档。",
        "",
        "## 同步状态",
        f"- 生成时间：{registry['generated_at']}",
        f"- 待同步：{', '.join(suggested_updates) if suggested_updates else '无'}",
        "",
        "## 状态定义",
        "- `active`：文档已有有效内容，当前未命中同步目标。",
        "- `seed`：文档仍是初始化骨架，信息不足。",
        "- `needs_update`：本轮代码变更提示该文档应复查。",
        "- `draft`：已生成待补写草稿，但尚未合并回正式 wiki。",
        "- `report`：维护巡检报告，不参与正式 wiki 合并。",
        "",
        "## 信号定义",
        "- `priority_score`：综合维护优先级，分数越高越应先处理。",
        "- `freshness_score`：文档新鲜度风险，越高表示越可能需要更新。",
        "- `density_score`：信息密度，越高表示越适合作为直接上下文。",
        "- `draft_dependency_score`：对草稿依赖程度，越高表示离稳定知识还更远。",
        "",
        "## 文档清单",
    ]

    for doc in documents:
        related = ", ".join(doc["related_changed_paths"]) if doc["related_changed_paths"] else "无"
        signals = doc["signals"]
        lines.append(
            "- "
            f"`{doc['path']}` | 类型：{doc['kind']} | 状态：{doc['status']} | "
            f"priority={signals['priority_score']} | freshness={signals['freshness_score']} | "
            f"density={signals['density_score']} | draft_dependency={signals['draft_dependency_score']} | "
            f"topic={doc['topic']} | updated_at={doc['last_modified']} | "
            f"summary={doc['summary']} | changed_paths={related}"
        )

    return "\n".join(lines) + "\n"


def refresh_wiki_registry(
    workspace: Path,
    changed_paths: list[str] | None = None,
    materialize_suggestions: bool = False,
) -> tuple[Path, Path, list[str]]:
    changed_paths = changed_paths or []
    suggestions = suggest_wiki_targets(changed_paths)

    if materialize_suggestions:
        for target in suggestions:
            if target.startswith("modules/"):
                ensure_wiki_section_path(workspace=workspace, module_name=Path(target).stem)
            else:
                ensure_wiki_section_path(workspace=workspace, section=Path(target).stem)

    registry = build_wiki_registry(workspace, changed_paths=changed_paths)
    wiki_root = workspace / "wiki"
    index_path = wiki_root / "index.md"
    registry_path = wiki_root / "registry.json"

    index_path.write_text(render_wiki_index(registry), encoding="utf-8")
    registry_path.write_text(
        json.dumps(registry, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return index_path, registry_path, suggestions


def draft_focus_points_for_target(target: str) -> list[str]:
    if target in WIKI_DRAFT_FOCUSES:
        return WIKI_DRAFT_FOCUSES[target]

    module_name = Path(target).stem
    return [
        f"模块 {module_name} 的职责是否发生变化",
        f"模块 {module_name} 暴露了哪些新接口或依赖",
        f"模块 {module_name} 的边界、限制或注意事项是否需要更新",
    ]


def draft_filename_for_target(target: str) -> str:
    return target.replace("/", "__")


def render_wiki_sync_draft(target: str, changed_paths: list[str]) -> str:
    focus_points = draft_focus_points_for_target(target)
    change_summary = ", ".join(f"`{path}`" for path in changed_paths) if changed_paths else "无"
    lines = [
        "# Wiki 待补写草稿",
        "",
        f"- 目标文件：{target}",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%dT%H:%M:%S')}",
        "",
        "## 变更线索",
    ]

    if changed_paths:
        for path in changed_paths:
            lines.append(f"- {path}")
    else:
        lines.append("- 无")

    lines.extend(
        [
            "",
            "## 待核对要点",
        ]
    )
    for point in focus_points:
        lines.append(f"- {point}")

    lines.extend(
        [
            "",
            "## 待补写草稿",
            f"- 本轮关联变更：{change_summary}",
            f"- 先核对：{focus_points[0]}",
            f"- 补充重点：{focus_points[1]}",
            "",
            "## 处理规则",
            "- 先核对代码事实，再把稳定信息写回目标 wiki 文件。",
            "- 若本轮仍不确定，保留在线索层，不要提前写成确定事实。",
        ]
    )
    return "\n".join(lines) + "\n"


def create_wiki_sync_drafts(
    workspace: Path,
    changed_paths: list[str] | None = None,
    materialize_suggestions: bool = False,
) -> tuple[list[Path], list[str]]:
    changed_paths = changed_paths or []
    suggestions = suggest_wiki_targets(changed_paths)

    if materialize_suggestions:
        for target in suggestions:
            if target.startswith("modules/"):
                ensure_wiki_section_path(workspace=workspace, module_name=Path(target).stem)
            else:
                ensure_wiki_section_path(workspace=workspace, section=Path(target).stem)

    drafts_dir = workspace / "wiki" / "drafts"
    drafts_dir.mkdir(parents=True, exist_ok=True)
    created: list[Path] = []

    for target in suggestions:
        matched_paths = [
            raw_path
            for raw_path in changed_paths
            if target in suggest_wiki_targets([raw_path])
        ]
        draft_path = drafts_dir / draft_filename_for_target(target)
        draft_path.write_text(render_wiki_sync_draft(target, matched_paths), encoding="utf-8")
        created.append(draft_path)

    return created, suggestions


def draft_target_from_text(draft_text: str, draft_name: str | None = None) -> str:
    match = re.search(r"^- 目标文件：(.+)$", draft_text, flags=re.MULTILINE)
    if match:
        return match.group(1).strip()

    if draft_name:
        return draft_name.replace("__", "/")

    raise ValueError("Unable to detect wiki draft target")


def extract_draft_merge_content(draft_text: str) -> str:
    match = re.search(
        r"^## 待补写草稿\s*(.*?)^\s*## ",
        draft_text + "\n## ",
        flags=re.MULTILINE | re.DOTALL,
    )
    if not match:
        return ""

    return match.group(1).strip()


def append_wiki_sync_content(target_path: Path, content: str) -> None:
    existing = target_path.read_text(encoding="utf-8").rstrip()
    block = "\n".join(
        [
            f"## 自动同步补充 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            content.strip(),
        ]
    )
    target_path.write_text(f"{existing}\n\n{block}\n", encoding="utf-8")


def compact_wiki_content(text: str) -> str:
    lines = text.splitlines()
    compacted: list[str] = []
    auto_blocks: list[list[str]] = []
    current_auto_block: list[str] | None = None

    for line in lines:
        if line.startswith("## 自动同步补充 "):
            if current_auto_block:
                auto_blocks.append(current_auto_block)
            current_auto_block = [line]
            continue

        if current_auto_block is not None:
            if line.startswith("## ") and not line.startswith("## 自动同步补充 "):
                auto_blocks.append(current_auto_block)
                current_auto_block = None
                compacted.append(line)
            else:
                current_auto_block.append(line)
            continue

        compacted.append(line)

    if current_auto_block:
        auto_blocks.append(current_auto_block)

    if len(auto_blocks) <= 1:
        return text if text.endswith("\n") else text + "\n"

    bullets: list[str] = []
    for block in auto_blocks:
        for line in block[1:]:
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.startswith("- "):
                bullet = stripped
            else:
                bullet = f"- {stripped}"
            if bullet not in bullets:
                bullets.append(bullet)

    summary_block = [
        "## 自动同步摘要",
        "",
        f"- 已合并补充块数：{len(auto_blocks)}",
    ]
    summary_block.extend(bullets or ["- 无有效补充内容"])

    result_lines: list[str] = []
    inserted_summary = False
    for line in compacted:
        result_lines.append(line)
        if not inserted_summary and line.startswith("# "):
            result_lines.extend([""] + summary_block + [""])
            inserted_summary = True

    if not inserted_summary:
        result_lines = summary_block + [""] + result_lines

    while result_lines and result_lines[-1] == "":
        result_lines.pop()
    return "\n".join(result_lines) + "\n"


def load_wiki_registry(workspace: Path) -> dict[str, object]:
    registry_path = workspace / "wiki" / "registry.json"
    if not registry_path.exists():
        refresh_wiki_registry(workspace)
    return json.loads(registry_path.read_text(encoding="utf-8"))


def is_stale_file(path: Path, stale_days: int) -> bool:
    cutoff = datetime.now() - timedelta(days=stale_days)
    modified_at = datetime.fromtimestamp(path.stat().st_mtime)
    return modified_at < cutoff


def render_wiki_maintenance_report(
    stale_days: int,
    changed_paths: list[str],
    missing_drafts: list[str],
    stale_drafts: list[str],
    ready_drafts: list[str],
) -> str:
    lines = [
        "# Wiki 维护报告",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%dT%H:%M:%S')}",
        f"- 草稿过期阈值：{stale_days} 天",
        "",
        "## 本轮变更线索",
    ]

    if changed_paths:
        for path in changed_paths:
            lines.append(f"- {path}")
    else:
        lines.append("- 无")

    lines.extend(
        [
            "",
            "## 待生成草稿",
        ]
    )
    if missing_drafts:
        for item in missing_drafts:
            lines.append(f"- {item}")
    else:
        lines.append("- 无")

    lines.extend(
        [
            "",
            "## 陈旧草稿",
        ]
    )
    if stale_drafts:
        for item in stale_drafts:
            lines.append(f"- {item}")
    else:
        lines.append("- 无")

    lines.extend(
        [
            "",
            "## 可合并草稿",
        ]
    )
    if ready_drafts:
        for item in ready_drafts:
            lines.append(f"- {item}")
    else:
        lines.append("- 无")

    lines.extend(
        [
            "",
            "## 后续动作",
        ]
    )

    if missing_drafts:
        lines.append("- 为缺失草稿的目标 wiki 生成待补写草稿。")
    if stale_drafts:
        lines.append("- 复查陈旧草稿，确认是否重生成、更新或删除。")
    if ready_drafts:
        lines.append("- 将已确认的草稿合并回正式 wiki。")
    if not missing_drafts and not stale_drafts and not ready_drafts:
        lines.append("- 当前无需额外维护。")

    return "\n".join(lines) + "\n"


def parse_maintenance_report(report_text: str) -> dict[str, list[str]]:
    sections = {
        "missing_drafts": "## 待生成草稿",
        "stale_drafts": "## 陈旧草稿",
        "ready_drafts": "## 可合并草稿",
    }
    parsed: dict[str, list[str]] = {}

    for key, header in sections.items():
        match = re.search(
            rf"^{re.escape(header)}\s*(.*?)^\s*## ",
            report_text + "\n## ",
            flags=re.MULTILINE | re.DOTALL,
        )
        if not match:
            parsed[key] = []
            continue

        items = []
        for line in match.group(1).splitlines():
            stripped = line.strip()
            if not stripped.startswith("- "):
                continue
            value = stripped[2:].strip()
            if value and value != "无":
                items.append(value)
        parsed[key] = items

    return parsed


def parse_draft_mapping(item: str) -> tuple[str, str]:
    if " -> " not in item:
        raise ValueError(f"Invalid draft mapping: {item}")
    left, right = item.split(" -> ", 1)
    return left.strip(), right.strip()


def extract_source_facts(project_root: Path, changed_paths: list[str]) -> dict[str, list[str]]:
    module_facts: dict[str, set[str]] = {}
    api_facts: set[str] = set()
    data_facts: set[str] = set()

    for raw_path in changed_paths:
        parts = split_path_parts(raw_path)
        if not parts:
            continue

        normalized_path = "/".join(parts)
        module_target = detect_module_target(parts)
        if module_target:
            module_name = Path(module_target).stem
            module_facts.setdefault(module_name, set()).add(f"变更文件：`{normalized_path}`")

        lowered = [part.lower() for part in parts]
        filename = parts[-1]

        if any(part in API_HINTS for part in lowered):
            api_facts.add(f"接口相关文件：`{normalized_path}`")

        if any(part in DATA_HINTS for part in lowered) or filename.endswith((".sql", ".prisma")):
            data_facts.add(f"数据相关文件：`{normalized_path}`")

    extracted: dict[str, list[str]] = {}
    for module_name, facts in module_facts.items():
        extracted[f"modules/{module_name}.md"] = sorted(facts)
    if api_facts:
        extracted["api.md"] = sorted(api_facts)
    if data_facts:
        extracted["data.md"] = sorted(data_facts)
    return extracted


def render_extracted_facts(target: str, facts: list[str]) -> str:
    lines = [
        "# 源码提炼草稿",
        "",
        f"- 目标文件：{target}",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%dT%H:%M:%S')}",
        "",
        "## 提炼事实",
    ]
    for fact in facts:
        lines.append(f"- {fact}")
    lines.extend(
        [
            "",
            "## 写回内容",
        ]
    )
    for fact in facts:
        lines.append(f"- {fact}")
    return "\n".join(lines) + "\n"


def assemble_wiki_context(
    workspace: Path,
    action: str,
    limit: int = 5,
) -> list[dict[str, object]]:
    registry = load_wiki_registry(workspace)
    hints = ACTION_CONTEXT_HINTS.get(action, set())
    documents = list(registry.get("documents", []))

    scored: list[tuple[tuple[int, int, int, str], dict[str, object]]] = []
    for doc in documents:
        path = str(doc["path"])
        kind = str(doc["kind"])
        status = str(doc["status"])
        signals = doc.get("signals", {})

        if kind == "report":
            continue
        if status == "draft" and action not in {"wiki", "reflect"}:
            continue

        hint_bonus = 1 if path in hints else 0
        module_bonus = 1 if action in {"plan", "todo", "reflect"} and path.startswith("modules/") else 0
        score = int(signals.get("priority_score", 0))
        scored.append(((-hint_bonus, -module_bonus, -score, path), doc))

    scored.sort(key=lambda item: item[0])
    return [doc for _, doc in scored[:limit]]


def resolve_wiki_strategy(name: str) -> dict[str, bool]:
    if name not in WIKI_STRATEGIES:
        raise ValueError(f"Unknown wiki strategy: {name}")
    return dict(WIKI_STRATEGIES[name])


def merge_fact_draft_into_target(workspace: Path, draft_path: Path) -> Path:
    draft_text = draft_path.read_text(encoding="utf-8")
    target = draft_target_from_text(draft_text, draft_name=draft_path.name)
    match = re.search(
        r"^## 写回内容\s*(.*)$",
        draft_text,
        flags=re.MULTILINE | re.DOTALL,
    )
    content = match.group(1).strip() if match else ""
    if not content:
        raise ValueError(f"No mergeable facts in draft: {draft_path}")

    if target.startswith("modules/"):
        wiki_path = ensure_wiki_section_path(workspace=workspace, module_name=Path(target).stem)
    else:
        wiki_path = ensure_wiki_section_path(workspace=workspace, section=Path(target).stem)
    append_wiki_sync_content(wiki_path, content)
    return wiki_path
