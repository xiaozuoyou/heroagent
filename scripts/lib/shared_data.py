from __future__ import annotations

from pathlib import Path


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

SCRIPT_DIR = Path(__file__).resolve().parents[1]
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
  "goal_definition": "",
  "current_object": "",
  "current_stage": "",
  "workflow_mode": "",
  "complexity_level": "",
  "stage_status": "",
  "next_action": "",
  "pending_choice": [],
  "latest_score": 0,
  "current_question": "",
  "goal_confirmed": false,
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
