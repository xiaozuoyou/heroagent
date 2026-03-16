#!/usr/bin/env python3
"""
Update HeroAgent want-stage workflow state for clarification or plan handoff.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from common import init_workspace
from common import load_workflow_state
from common import save_workflow_state


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Update HeroAgent want-stage workflow state for clarification or plan handoff.",
    )
    parser.add_argument("--goal", default="", help="Current goal title or draft goal.")
    parser.add_argument(
        "--status",
        required=True,
        choices=["clarifying", "awaiting_goal_confirmation", "ready_for_plan", "paused"],
        help="Want-stage status.",
    )
    parser.add_argument(
        "--score",
        type=int,
        default=0,
        help="Latest want-stage requirement score.",
    )
    parser.add_argument(
        "--question",
        default="",
        help="Current Socratic question when status is clarifying.",
    )
    parser.add_argument(
        "--goal-definition",
        default="",
        help="Current synthesized goal definition for user confirmation.",
    )
    parser.add_argument(
        "--goal-confirmed",
        action="store_true",
        help="Whether the user has explicitly confirmed the current goal definition.",
    )
    parser.add_argument(
        "target",
        nargs="?",
        default=".",
        help="Target project directory. Defaults to the current directory.",
    )
    args = parser.parse_args()

    if args.status == "ready_for_plan" and not args.goal_confirmed:
        parser.error("--status ready_for_plan requires --goal-confirmed")

    target = Path(args.target).resolve()
    target.mkdir(parents=True, exist_ok=True)
    workspace = init_workspace(target, with_readme=True, with_current_focus=True)
    state = load_workflow_state(workspace)

    pending_choice: list[str]
    next_action: str
    if args.status == "clarifying":
        pending_choice = []
        next_action = "answer_current_question"
    elif args.status == "awaiting_goal_confirmation":
        pending_choice = ["confirm_goal_definition", "continue_want", "defer"]
        next_action = "confirm_goal_definition"
    elif args.status == "ready_for_plan":
        pending_choice = ["~plan", "continue_want", "defer"]
        next_action = "confirm_plan_handoff"
    else:
        pending_choice = ["defer"]
        next_action = "defer"

    state.update(
        {
            "current_goal": args.goal,
            "goal_definition": args.goal_definition,
            "current_object": "goal",
            "current_stage": "clarify",
            "workflow_mode": "interactive",
            "complexity_level": "standard",
            "stage_status": args.status,
            "next_action": next_action,
            "pending_choice": pending_choice,
            "latest_score": args.score,
            "current_question": args.question,
            "goal_confirmed": args.goal_confirmed,
        }
    )

    path = save_workflow_state(workspace, state)
    print(f"Updated HeroAgent want state: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
