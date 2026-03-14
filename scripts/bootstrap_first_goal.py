#!/usr/bin/env python3
"""
Bootstrap the first HeroAgent goal artifacts in a target project.
"""

from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
from pathlib import Path
import re

from init_heroagent import init_workspace


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", text.strip().lower()).strip("-")
    if slug:
        return slug

    digest = hashlib.sha1(text.strip().encode("utf-8")).hexdigest()[:8]
    return f"goal-{digest}"


def timestamp_now() -> str:
    return datetime.now().strftime("%Y%m%d%H%M")


def safe_write(path: Path, content: str) -> Path:
    if not path.exists():
        path.write_text(content, encoding="utf-8")
        return path

    stem = path.stem
    suffix = path.suffix
    parent = path.parent
    index = 1
    while True:
        candidate = parent / f"{stem}-{index}{suffix}"
        if not candidate.exists():
            candidate.write_text(content, encoding="utf-8")
            return candidate
        index += 1


def goal_card(goal_title: str) -> str:
    return f"""## 目标卡片

- 目标：{goal_title}
- 背景：
- 价值：
- 范围：
- 不做什么：
- 成功标准：
- 约束：
- 下一步：补全目标边界与成功标准
"""


def milestone_plan() -> str:
    return """## 里程碑计划

1. 阶段：
   产出：
   风险：
   完成标志：

2. 阶段：
   产出：
   风险：
   完成标志：

3. 阶段：
   产出：
   风险：
   完成标志：

## 下一步

- 根据目标卡片补齐阶段路径
"""


def todo_list() -> str:
    return """## 任务列表

- [ ] 任务名
  完成定义：
  依赖：
  优先级：

- [ ] 任务名
  完成定义：
  依赖：
  优先级：

## 下一步

- 根据里程碑计划拆解第一批可执行任务
"""


def current_focus(goal_title: str, stage: str) -> str:
    return f"""## 进度快照

- 当前目标：{goal_title}
- 当前阶段：{stage}
- 已完成：已初始化 HeroAgent 工作区与首批草稿文件
- 进行中：补全目标与计划
- 阻塞：
- 下一步：先完善目标卡片，再细化里程碑计划
"""


def bootstrap(target: Path, goal_title: str, stage: str, refresh_focus: bool) -> list[Path]:
    workspace = init_workspace(target, with_readme=True, with_current_focus=True)
    ts = timestamp_now()
    slug = slugify(goal_title)

    created = []
    created.append(
        safe_write(workspace / "goals" / f"{ts}_{slug}.md", goal_card(goal_title))
    )
    created.append(
        safe_write(workspace / "plans" / f"{ts}_{slug}.md", milestone_plan())
    )
    created.append(
        safe_write(workspace / "tasks" / f"{ts}_{slug}.md", todo_list())
    )

    focus_path = workspace / "progress" / "current-focus.md"
    if refresh_focus or not focus_path.exists():
        focus_path.write_text(current_focus(goal_title, stage), encoding="utf-8")
        created.append(focus_path)

    return created


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Bootstrap the first HeroAgent goal artifacts in a target project.",
    )
    parser.add_argument("goal_title", help="Goal title used to seed the first files.")
    parser.add_argument(
        "target",
        nargs="?",
        default=".",
        help="Target project directory. Defaults to the current directory.",
    )
    parser.add_argument(
        "--stage",
        default="want",
        help="Initial stage written to progress/current-focus.md. Defaults to want.",
    )
    parser.add_argument(
        "--refresh-focus",
        action="store_true",
        help="Overwrite progress/current-focus.md with the new goal focus.",
    )
    args = parser.parse_args()

    target = Path(args.target).resolve()
    target.mkdir(parents=True, exist_ok=True)

    created = bootstrap(
        target=target,
        goal_title=args.goal_title,
        stage=args.stage,
        refresh_focus=args.refresh_focus,
    )

    print("Bootstrapped HeroAgent artifacts:")
    for path in created:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
