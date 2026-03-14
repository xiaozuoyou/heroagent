#!/usr/bin/env python3
"""
Update .heroagent/progress/current-focus.md in a target project.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from init_heroagent import init_workspace


def render_focus(
    goal: str,
    stage: str,
    completed: str,
    in_progress: str,
    blockers: str,
    next_step: str,
) -> str:
    return f"""## 进度快照

- 当前目标：{goal}
- 当前阶段：{stage}
- 已完成：{completed}
- 进行中：{in_progress}
- 阻塞：{blockers}
- 下一步：{next_step}
"""


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Update .heroagent/progress/current-focus.md in a target project.",
    )
    parser.add_argument("--goal", default="", help="Current goal.")
    parser.add_argument("--stage", default="focus", help="Current stage.")
    parser.add_argument("--completed", default="", help="Completed facts.")
    parser.add_argument("--in-progress", default="", help="Current in-progress work.")
    parser.add_argument("--blockers", default="", help="Current blockers.")
    parser.add_argument("--next-step", default="", help="Next highest priority step.")
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

    focus_path = workspace / "progress" / "current-focus.md"
    focus_path.write_text(
        render_focus(
            goal=args.goal,
            stage=args.stage,
            completed=args.completed,
            in_progress=args.in_progress,
            blockers=args.blockers,
            next_step=args.next_step,
        ),
        encoding="utf-8",
    )

    print(f"Updated HeroAgent focus: {focus_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
