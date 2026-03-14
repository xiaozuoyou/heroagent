#!/usr/bin/env python3
"""
Bootstrap the first HeroAgent goal artifacts in a target project.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from common import init_workspace
from common import render_template
from common import safe_write
from common import slugify
from common import timestamp_now


def goal_card(goal_title: str) -> str:
    return render_template(
        "goal-card.md",
        fields={"目标": goal_title},
        next_step="补全目标边界与成功标准",
    )


def milestone_plan() -> str:
    return render_template(
        "milestone-plan.md",
        next_step="根据目标卡片补齐阶段路径",
    )


def todo_list() -> str:
    return render_template(
        "todo-list.md",
        next_step="根据里程碑计划拆解第一批可执行任务",
    )


def current_focus(goal_title: str, stage: str) -> str:
    return render_template(
        "progress-snapshot.md",
        fields={
            "当前目标": goal_title,
            "当前阶段": stage,
            "已完成": "已初始化 HeroAgent 工作区与首批草稿文件",
            "进行中": "补全目标与计划",
            "阻塞": "",
            "下一步": "先完善目标卡片，再细化里程碑计划",
        },
    )


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
