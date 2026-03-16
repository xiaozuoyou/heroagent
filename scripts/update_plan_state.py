#!/usr/bin/env python3
"""
Update HeroAgent plan-stage workflow state for planning or plan confirmation.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from common import init_workspace
from common import load_workflow_state
from common import save_workflow_state


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Update HeroAgent plan-stage workflow state for planning or plan confirmation.",
    )
    parser.add_argument("--goal", default="", help="Current goal title.")
    parser.add_argument(
        "--status",
        required=True,
        choices=["planning", "plan_ready_for_confirm", "paused"],
        help="Plan-stage status.",
    )
    parser.add_argument(
        "--plan-path",
        default="",
        help="Current active plan document path.",
    )
    parser.add_argument(
        "--plan-summary",
        default="",
        help="Current synthesized plan summary.",
    )
    parser.add_argument(
        "--plan-confirmed",
        action="store_true",
        help="Whether the user has explicitly confirmed the current plan.",
    )
    parser.add_argument(
        "target",
        nargs="?",
        default=".",
        help="Target project directory. Defaults to the current directory.",
    )
    args = parser.parse_args()

    if args.plan_confirmed and not args.plan_path:
        parser.error("--plan-confirmed requires --plan-path")

    target = Path(args.target).resolve()
    target.mkdir(parents=True, exist_ok=True)
    workspace = init_workspace(target, with_readme=True, with_current_focus=True)
    state = load_workflow_state(workspace)

    pending_choice: list[str]
    next_action: str
    if args.status == "planning":
        pending_choice = []
        next_action = "continue_plan_alignment"
    elif args.status == "plan_ready_for_confirm":
        pending_choice = ["confirm_plan", "continue_plan", "defer"]
        next_action = "confirm_plan"
    else:
        pending_choice = ["defer"]
        next_action = "defer"

    state.update(
        {
            "current_goal": args.goal,
            "current_object": "plan",
            "current_stage": "planning",
            "workflow_mode": "interactive",
            "complexity_level": "standard",
            "stage_status": args.status,
            "next_action": next_action,
            "pending_choice": pending_choice,
            "active_plan_path": args.plan_path,
            "plan_summary": args.plan_summary,
            "plan_confirmed": args.plan_confirmed,
        }
    )

    path = save_workflow_state(workspace, state)
    print(f"Updated HeroAgent plan state: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
