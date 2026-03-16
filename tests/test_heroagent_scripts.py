import subprocess
import sys
import tempfile
import unittest
import os
import json
import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
PYTHON = sys.executable
EXPECTED_ACTIONS = {
    "init",
    "wiki",
    "want",
    "plan",
    "todo",
    "focus",
    "achieve",
    "abandon",
    "reflect",
}
INTERNAL_ONLY_SCRIPTS = {"update_wiki_signal_state.py"}


def run_script(script_name: str, *args: str) -> subprocess.CompletedProcess[str]:
    script_path = SCRIPTS_DIR / script_name
    env = {"PYTHONPATH": str(SCRIPTS_DIR)}
    return subprocess.run(
        [PYTHON, str(script_path), *args],
        text=True,
        capture_output=True,
        env=env,
        check=False,
    )


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_backticked_values(text: str, pattern: str) -> set[str]:
    return set(re.findall(pattern, text))


class HeroAgentScriptsTest(unittest.TestCase):
    def test_init_creates_workspace_structure(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            result = run_script("init_heroagent.py", tmpdir)
            self.assertEqual(result.returncode, 0, result.stderr)

            root = Path(tmpdir) / ".heroagent"
            self.assertTrue((root / "goals").is_dir())
            self.assertTrue((root / "progress" / "current-focus.md").exists())
            self.assertTrue((root / "README.md").exists())
            self.assertFalse((root / "processes").exists())
            self.assertTrue((root / "wiki" / "index.md").exists())
            self.assertTrue((root / "wiki" / "registry.json").exists())
            self.assertTrue((root / "wiki" / "overview.md").exists())
            self.assertTrue((root / "wiki" / "arch.md").exists())
            self.assertTrue((root / "wiki" / "api.md").exists())
            self.assertTrue((root / "wiki" / "data.md").exists())

    def test_init_readme_uses_new_workflow_model(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            result = run_script("init_heroagent.py", tmpdir)
            self.assertEqual(result.returncode, 0, result.stderr)

            readme = (Path(tmpdir) / ".heroagent" / "README.md").read_text(encoding="utf-8")
            self.assertIn("公开动作", readme)
            self.assertIn("内部方法", readme)
            self.assertIn("want -> plan -> todo -> achieve | abandon", readme)
            self.assertIn("`focus`：当前态势观察动作", readme)
            self.assertIn("`todo`：基于已确认计划文档开始执行", readme)
            self.assertIn("`plan`：负责继续沟通并写出可确认的本地计划文档", readme)
            self.assertIn("`reflect`：问题复盘入口", readme)

    def test_init_workflow_state_includes_reflect_fields(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            result = run_script("init_heroagent.py", tmpdir)
            self.assertEqual(result.returncode, 0, result.stderr)

            state = json.loads(
                (Path(tmpdir) / ".heroagent" / "progress" / "workflow-state.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(state["reflect_status"], "")
            self.assertEqual(state["pending_reflect_reason"], "")
            self.assertFalse(state["pending_realize"])
            self.assertEqual(state["last_reflect_at"], "")
            self.assertEqual(state["last_realize_at"], "")
            self.assertEqual(state["current_object"], "")
            self.assertEqual(state["goal_definition"], "")
            self.assertFalse(state["goal_confirmed"])
            self.assertEqual(state["workflow_mode"], "")
            self.assertEqual(state["complexity_level"], "")

    def test_bootstrap_creates_seed_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            result = run_script(
                "bootstrap_first_goal.py",
                "规范团队周报流程",
                tmpdir,
                "--refresh-focus",
            )
            self.assertEqual(result.returncode, 0, result.stderr)

            root = Path(tmpdir) / ".heroagent"
            goals = list((root / "goals").glob("*.md"))
            plans = list((root / "plans").glob("*.md"))
            self.assertEqual(len(goals), 1)
            self.assertEqual(len(plans), 1)
            self.assertEqual(len(list((root / "tasks").glob("*.md"))), 0)
            self.assertIn("规范团队周报流程", goals[0].read_text(encoding="utf-8"))

    def test_update_current_focus_overwrites_focus_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            run_script("init_heroagent.py", tmpdir)
            result = run_script(
                "update_current_focus.py",
                "--goal",
                "规范团队周报流程",
                "--stage",
                "focus",
                "--completed",
                "已生成计划",
                "--in-progress",
                "补充任务",
                "--blockers",
                "无",
                "--next-step",
                "完成任务拆解",
                tmpdir,
            )
            self.assertEqual(result.returncode, 0, result.stderr)

            content = (Path(tmpdir) / ".heroagent" / "progress" / "current-focus.md").read_text(
                encoding="utf-8"
            )
            self.assertIn("当前目标：规范团队周报流程", content)
            self.assertIn("下一步：完成任务拆解", content)

    def test_update_want_state_clarifying(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            run_script("init_heroagent.py", tmpdir)
            result = run_script(
                "update_want_state.py",
                "--goal",
                "规范团队周报流程",
                "--status",
                "clarifying",
                "--score",
                "6",
                "--question",
                "你这次最想达成的结果是什么",
                tmpdir,
            )
            self.assertEqual(result.returncode, 0, result.stderr)

            state = json.loads(
                (Path(tmpdir) / ".heroagent" / "progress" / "workflow-state.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(state["current_object"], "goal")
            self.assertEqual(state["current_stage"], "clarify")
            self.assertEqual(state["workflow_mode"], "interactive")
            self.assertEqual(state["complexity_level"], "standard")
            self.assertEqual(state["stage_status"], "clarifying")
            self.assertEqual(state["next_action"], "answer_current_question")
            self.assertEqual(state["latest_score"], 6)
            self.assertEqual(state["current_question"], "你这次最想达成的结果是什么")
            self.assertEqual(state["goal_definition"], "")
            self.assertFalse(state["goal_confirmed"])

    def test_update_want_state_awaiting_goal_confirmation(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            run_script("init_heroagent.py", tmpdir)
            result = run_script(
                "update_want_state.py",
                "--goal",
                "规范团队周报流程",
                "--status",
                "awaiting_goal_confirmation",
                "--score",
                "8",
                "--goal-definition",
                "两周内明确周报模板、提交流程和负责人边界，不处理绩效考核。",
                tmpdir,
            )
            self.assertEqual(result.returncode, 0, result.stderr)

            state = json.loads(
                (Path(tmpdir) / ".heroagent" / "progress" / "workflow-state.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(state["stage_status"], "awaiting_goal_confirmation")
            self.assertEqual(state["next_action"], "confirm_goal_definition")
            self.assertEqual(
                state["pending_choice"],
                ["confirm_goal_definition", "continue_want", "defer"],
            )
            self.assertEqual(
                state["goal_definition"],
                "两周内明确周报模板、提交流程和负责人边界，不处理绩效考核。",
            )
            self.assertFalse(state["goal_confirmed"])

    def test_update_want_state_ready_for_plan(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            run_script("init_heroagent.py", tmpdir)
            result = run_script(
                "update_want_state.py",
                "--goal",
                "规范团队周报流程",
                "--status",
                "ready_for_plan",
                "--score",
                "8",
                "--goal-definition",
                "两周内明确周报模板、提交流程和负责人边界，不处理绩效考核。",
                "--goal-confirmed",
                tmpdir,
            )
            self.assertEqual(result.returncode, 0, result.stderr)

            state = json.loads(
                (Path(tmpdir) / ".heroagent" / "progress" / "workflow-state.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(state["stage_status"], "ready_for_plan")
            self.assertEqual(state["next_action"], "confirm_plan_handoff")
            self.assertEqual(state["pending_choice"], ["~plan", "continue_want", "defer"])
            self.assertEqual(state["current_stage"], "clarify")
            self.assertTrue(state["goal_confirmed"])
            self.assertEqual(
                state["goal_definition"],
                "两周内明确周报模板、提交流程和负责人边界，不处理绩效考核。",
            )

    def test_update_want_state_ready_for_plan_requires_goal_confirmed(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            run_script("init_heroagent.py", tmpdir)
            result = run_script(
                "update_want_state.py",
                "--goal",
                "规范团队周报流程",
                "--status",
                "ready_for_plan",
                "--score",
                "8",
                "--goal-definition",
                "两周内明确周报模板、提交流程和负责人边界，不处理绩效考核。",
                tmpdir,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("requires --goal-confirmed", result.stderr)

    def test_update_wiki_signal_state_marks_pending_targets(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            run_script("init_heroagent.py", tmpdir)
            result = run_script(
                "update_wiki_signal_state.py",
                "--changed-path",
                "src/payments/service.ts",
                "--changed-path",
                "src/api/routes/orders.ts",
                tmpdir,
            )
            self.assertEqual(result.returncode, 0, result.stderr)

            state = json.loads(
                (Path(tmpdir) / ".heroagent" / "progress" / "workflow-state.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(state["wiki_status"], "needs_sync")
            self.assertIn("modules/payments.md", state["pending_wiki_targets"])
            self.assertIn("api.md", state["pending_wiki_targets"])
            self.assertIn("Wiki status: needs_sync", result.stdout)

    def test_update_wiki_signal_state_can_mark_targets_synced(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            run_script("init_heroagent.py", tmpdir)
            run_script(
                "update_wiki_signal_state.py",
                "--changed-path",
                "src/payments/service.ts",
                "--changed-path",
                "src/api/routes/orders.ts",
                tmpdir,
            )
            result = run_script(
                "update_wiki_signal_state.py",
                "--mark-synced",
                "--strategy",
                "aggressive",
                "--changed-path",
                "src/payments/service.ts",
                "--changed-path",
                "src/api/routes/orders.ts",
                tmpdir,
            )
            self.assertEqual(result.returncode, 0, result.stderr)

            state = json.loads(
                (Path(tmpdir) / ".heroagent" / "progress" / "workflow-state.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(state["wiki_status"], "fresh")
            self.assertEqual(state["pending_wiki_targets"], [])
            self.assertEqual(state["last_wiki_sync_strategy"], "aggressive")
            self.assertIn("Recorded wiki sync strategy: aggressive", result.stdout)

    def test_archive_moves_goal_related_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            run_script("bootstrap_first_goal.py", "规范团队周报流程", tmpdir, "--refresh-focus")
            slug = "goal-d348d219"
            progress_note = Path(tmpdir) / ".heroagent" / "progress" / f"202603151200_{slug}.md"
            progress_note.write_text("# 验收结论\n\n- 已完成验收\n", encoding="utf-8")

            result = run_script("archive_goal.py", "--slug", slug, "--reset-focus", tmpdir)
            self.assertEqual(result.returncode, 0, result.stderr)

            archive_dirs = list((Path(tmpdir) / ".heroagent" / "archive").glob(f"*_{slug}"))
            self.assertEqual(len(archive_dirs), 1)
            archive_dir = archive_dirs[0]
            self.assertTrue((archive_dir / f"goals__{archive_dir.name}.md").exists())
            self.assertTrue((archive_dir / f"plans__{archive_dir.name}.md").exists())
            self.assertTrue((archive_dir / f"progress__{progress_note.name}").exists())
            self.assertFalse(progress_note.exists())

            focus = (Path(tmpdir) / ".heroagent" / "progress" / "current-focus.md").read_text(
                encoding="utf-8"
            )
            self.assertIn("当前目标：", focus)

    def test_doctor_reports_missing_workspace_then_healthy(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            missing = run_script("doctor_heroagent.py", tmpdir)
            self.assertNotEqual(missing.returncode, 0)
            self.assertIn("Missing .heroagent", missing.stdout)

            run_script("init_heroagent.py", tmpdir)
            healthy = run_script("doctor_heroagent.py", tmpdir)
            self.assertEqual(healthy.returncode, 0, healthy.stderr)
            self.assertIn("HEALTHY", healthy.stdout)

    def test_doctor_reports_missing_wiki_core_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            run_script("init_heroagent.py", tmpdir)
            api_doc = Path(tmpdir) / ".heroagent" / "wiki" / "api.md"
            api_doc.unlink()

            result = run_script("doctor_heroagent.py", tmpdir)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn(str(api_doc), result.stdout)

    def test_update_wiki_context_appends_content(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            run_script("init_heroagent.py", tmpdir)
            result = run_script(
                "update_wiki_context.py",
                "--section",
                "overview",
                "--content",
                "## 模块事实\n\n- 支付模块负责统一收单",
                tmpdir,
            )
            self.assertEqual(result.returncode, 0, result.stderr)

            content = (Path(tmpdir) / ".heroagent" / "wiki" / "overview.md").read_text(
                encoding="utf-8"
            )
            self.assertIn("支付模块负责统一收单", content)
            index_content = (Path(tmpdir) / ".heroagent" / "wiki" / "index.md").read_text(
                encoding="utf-8"
            )
            self.assertIn("overview.md", index_content)

    def test_init_creates_wiki_modules_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            run_script("init_heroagent.py", tmpdir)
            modules_dir = Path(tmpdir) / ".heroagent" / "wiki" / "modules"
            self.assertTrue(modules_dir.is_dir())

    def test_update_wiki_context_supports_module_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            run_script("init_heroagent.py", tmpdir)
            result = run_script(
                "update_wiki_context.py",
                "--module",
                "payments",
                "--content",
                "## 模块事实\n\n- 支付模块负责统一收单",
                tmpdir,
            )
            self.assertEqual(result.returncode, 0, result.stderr)

            module_doc = Path(tmpdir) / ".heroagent" / "wiki" / "modules" / "payments.md"
            self.assertTrue(module_doc.exists())
            self.assertIn("支付模块负责统一收单", module_doc.read_text(encoding="utf-8"))
            registry = (Path(tmpdir) / ".heroagent" / "wiki" / "registry.json").read_text(
                encoding="utf-8"
            )
            self.assertIn("modules/payments.md", registry)

    def test_suggest_wiki_updates_returns_expected_targets(self) -> None:
        result = run_script(
            "suggest_wiki_updates.py",
            "src/payments/service.ts",
            "src/api/routes/orders.ts",
            "prisma/schema.prisma",
            "README.md",
        )
        self.assertEqual(result.returncode, 0, result.stderr)

        self.assertIn("overview.md", result.stdout)
        self.assertIn("api.md", result.stdout)
        self.assertIn("data.md", result.stdout)
        self.assertIn("modules/payments.md", result.stdout)

    def test_suggest_wiki_updates_ignores_existing_wiki_paths(self) -> None:
        result = run_script(
            "suggest_wiki_updates.py",
            ".heroagent/wiki/overview.md",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("No wiki updates suggested.", result.stdout)

    def test_refresh_wiki_registry_marks_suggested_updates_and_materializes_module(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            run_script("init_heroagent.py", tmpdir)
            result = run_script(
                "refresh_wiki_registry.py",
                "--changed-path",
                "src/payments/service.ts",
                "--changed-path",
                "src/api/routes/orders.ts",
                "--materialize-suggestions",
                tmpdir,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("modules/payments.md", result.stdout)
            self.assertTrue(
                (Path(tmpdir) / ".heroagent" / "wiki" / "modules" / "payments.md").exists()
            )

            index_content = (Path(tmpdir) / ".heroagent" / "wiki" / "index.md").read_text(
                encoding="utf-8"
            )
            self.assertIn("needs_update", index_content)
            self.assertIn("api.md", index_content)

    def test_sync_wiki_from_changes_creates_drafts_and_refreshes_registry(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            run_script("init_heroagent.py", tmpdir)
            result = run_script(
                "sync_wiki_from_changes.py",
                "--changed-path",
                "src/payments/service.ts",
                "--changed-path",
                "prisma/schema.prisma",
                "--materialize-suggestions",
                tmpdir,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Created HeroAgent wiki sync drafts:", result.stdout)

            drafts_dir = Path(tmpdir) / ".heroagent" / "wiki" / "drafts"
            payment_draft = drafts_dir / "modules__payments.md"
            data_draft = drafts_dir / "data.md"
            self.assertTrue(payment_draft.exists())
            self.assertTrue(data_draft.exists())
            self.assertIn("payments", payment_draft.read_text(encoding="utf-8"))
            self.assertIn("schema.prisma", data_draft.read_text(encoding="utf-8"))

            registry = (Path(tmpdir) / ".heroagent" / "wiki" / "registry.json").read_text(
                encoding="utf-8"
            )
            self.assertIn("draft", registry)
            self.assertIn("drafts/modules__payments.md", registry)

    def test_apply_wiki_draft_merges_into_target_and_removes_draft(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            run_script("init_heroagent.py", tmpdir)
            run_script(
                "sync_wiki_from_changes.py",
                "--changed-path",
                "src/payments/service.ts",
                "--materialize-suggestions",
                tmpdir,
            )

            result = run_script(
                "apply_wiki_draft.py",
                "modules__payments.md",
                tmpdir,
            )
            self.assertEqual(result.returncode, 0, result.stderr)

            wiki_doc = Path(tmpdir) / ".heroagent" / "wiki" / "modules" / "payments.md"
            self.assertIn("自动同步补充", wiki_doc.read_text(encoding="utf-8"))

            draft_doc = Path(tmpdir) / ".heroagent" / "wiki" / "drafts" / "modules__payments.md"
            self.assertFalse(draft_doc.exists())

            registry = (Path(tmpdir) / ".heroagent" / "wiki" / "registry.json").read_text(
                encoding="utf-8"
            )
            self.assertNotIn("drafts/modules__payments.md", registry)

    def test_reconcile_wiki_state_writes_maintenance_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            run_script("init_heroagent.py", tmpdir)
            run_script(
                "sync_wiki_from_changes.py",
                "--changed-path",
                "src/payments/service.ts",
                tmpdir,
            )

            draft_doc = Path(tmpdir) / ".heroagent" / "wiki" / "drafts" / "modules__payments.md"
            stale_timestamp = 1
            os.utime(draft_doc, (stale_timestamp, stale_timestamp))

            result = run_script(
                "reconcile_wiki_state.py",
                "--changed-path",
                "src/payments/service.ts",
                "--changed-path",
                "src/api/routes/orders.ts",
                "--stale-days",
                "0",
                tmpdir,
            )
            self.assertEqual(result.returncode, 0, result.stderr)

            report = (
                Path(tmpdir) / ".heroagent" / "wiki" / "drafts" / "maintenance-report.md"
            ).read_text(encoding="utf-8")
            self.assertIn("api.md", report)
            self.assertIn("modules/payments.md", report)
            self.assertIn("陈旧草稿", report)

    def test_promote_wiki_maintenance_creates_missing_applies_ready_and_marks_stale(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            run_script("init_heroagent.py", tmpdir)
            run_script(
                "sync_wiki_from_changes.py",
                "--changed-path",
                "src/payments/service.ts",
                tmpdir,
            )

            stale_draft = Path(tmpdir) / ".heroagent" / "wiki" / "drafts" / "modules__payments.md"
            stale_timestamp = 1
            os.utime(stale_draft, (stale_timestamp, stale_timestamp))

            result = run_script(
                "promote_wiki_maintenance.py",
                "--changed-path",
                "src/payments/service.ts",
                "--changed-path",
                "src/api/routes/orders.ts",
                "--stale-days",
                "0",
                "--materialize-missing",
                "--apply-ready",
                "--mark-stale",
                tmpdir,
            )
            self.assertEqual(result.returncode, 0, result.stderr)

            api_draft = Path(tmpdir) / ".heroagent" / "wiki" / "drafts" / "api.md"
            self.assertTrue(api_draft.exists())

            stale_content = stale_draft.read_text(encoding="utf-8")
            self.assertIn("陈旧标记", stale_content)

            report = (
                Path(tmpdir) / ".heroagent" / "wiki" / "drafts" / "maintenance-report.md"
            ).read_text(encoding="utf-8")
            self.assertIn("api.md", report)

    def test_compact_wiki_memory_merges_multiple_auto_sync_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            run_script("init_heroagent.py", tmpdir)
            run_script(
                "update_wiki_context.py",
                "--module",
                "payments",
                "--content",
                "## 模块事实\n\n- 支付模块负责统一收单",
                tmpdir,
            )

            module_doc = Path(tmpdir) / ".heroagent" / "wiki" / "modules" / "payments.md"
            original = module_doc.read_text(encoding="utf-8")
            module_doc.write_text(
                original
                + "\n## 自动同步补充 2026-03-15 12:00:00\n\n- 第一条补充\n"
                + "\n## 自动同步补充 2026-03-15 12:05:00\n\n- 第二条补充\n",
                encoding="utf-8",
            )

            result = run_script(
                "compact_wiki_memory.py",
                "--scope",
                "modules",
                tmpdir,
            )
            self.assertEqual(result.returncode, 0, result.stderr)

            content = module_doc.read_text(encoding="utf-8")
            self.assertIn("## 自动同步摘要", content)
            self.assertIn("第一条补充", content)
            self.assertIn("第二条补充", content)
            self.assertNotIn("## 自动同步补充 2026-03-15 12:00:00", content)

    def test_score_wiki_signals_outputs_priority_order(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            run_script("init_heroagent.py", tmpdir)
            run_script(
                "sync_wiki_from_changes.py",
                "--changed-path",
                "src/payments/service.ts",
                "--changed-path",
                "src/api/routes/orders.ts",
                tmpdir,
            )

            result = run_script(
                "score_wiki_signals.py",
                "--changed-path",
                "src/payments/service.ts",
                "--changed-path",
                "src/api/routes/orders.ts",
                "--top",
                "3",
                tmpdir,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Top HeroAgent wiki signals:", result.stdout)
            self.assertIn("priority=", result.stdout)
            self.assertIn("freshness=", result.stdout)

            registry = (Path(tmpdir) / ".heroagent" / "wiki" / "registry.json").read_text(
                encoding="utf-8"
            )
            self.assertIn('"signals"', registry)
            self.assertIn('"priority_score"', registry)

    def test_assemble_wiki_context_returns_action_specific_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            run_script("init_heroagent.py", tmpdir)
            run_script(
                "update_wiki_context.py",
                "--module",
                "payments",
                "--content",
                "## 模块事实\n\n- 支付模块负责统一收单",
                tmpdir,
            )

            result = run_script(
                "assemble_wiki_context.py",
                "todo",
                "--changed-path",
                "src/payments/service.ts",
                "--changed-path",
                "src/api/routes/orders.ts",
                "--limit",
                "4",
                tmpdir,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("HeroAgent wiki context bundle for todo:", result.stdout)
            self.assertIn("modules/payments.md", result.stdout)
            self.assertIn("api.md", result.stdout)

    def test_extract_wiki_facts_generates_fact_drafts(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            run_script("init_heroagent.py", tmpdir)
            result = run_script(
                "extract_wiki_facts.py",
                "--changed-path",
                "src/payments/service.ts",
                "--changed-path",
                "src/api/routes/orders.ts",
                "--changed-path",
                "prisma/schema.prisma",
                tmpdir,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Extracted HeroAgent wiki facts:", result.stdout)

            drafts_dir = Path(tmpdir) / ".heroagent" / "wiki" / "drafts"
            self.assertTrue((drafts_dir / "facts__modules__payments.md").exists())
            self.assertTrue((drafts_dir / "facts__api.md").exists())
            self.assertTrue((drafts_dir / "facts__data.md").exists())

            content = (drafts_dir / "facts__api.md").read_text(encoding="utf-8")
            self.assertIn("接口相关文件", content)
            self.assertIn("src/api/routes/orders.ts", content)

    def test_run_wiki_strategy_balanced_extracts_facts_and_marks_stale(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            run_script("init_heroagent.py", tmpdir)
            run_script(
                "sync_wiki_from_changes.py",
                "--changed-path",
                "src/payments/service.ts",
                tmpdir,
            )

            stale_draft = Path(tmpdir) / ".heroagent" / "wiki" / "drafts" / "modules__payments.md"
            stale_timestamp = 1
            os.utime(stale_draft, (stale_timestamp, stale_timestamp))

            result = run_script(
                "run_wiki_strategy.py",
                "balanced",
                "--changed-path",
                "src/payments/service.ts",
                "--changed-path",
                "src/api/routes/orders.ts",
                "--stale-days",
                "0",
                tmpdir,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Ran HeroAgent wiki strategy: balanced", result.stdout)
            self.assertIn("Extracted fact drafts:", result.stdout)

            fact_draft = Path(tmpdir) / ".heroagent" / "wiki" / "drafts" / "facts__api.md"
            self.assertTrue(fact_draft.exists())
            self.assertIn("陈旧标记", stale_draft.read_text(encoding="utf-8"))

            state = json.loads(
                (Path(tmpdir) / ".heroagent" / "progress" / "workflow-state.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(state["wiki_status"], "needs_sync")
            self.assertIn("api.md", state["pending_wiki_targets"])

    def test_run_wiki_strategy_aggressive_marks_wiki_fresh(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            run_script("init_heroagent.py", tmpdir)
            result = run_script(
                "run_wiki_strategy.py",
                "aggressive",
                "--changed-path",
                "src/payments/service.ts",
                "--changed-path",
                "src/api/routes/orders.ts",
                tmpdir,
            )
            self.assertEqual(result.returncode, 0, result.stderr)

            state = json.loads(
                (Path(tmpdir) / ".heroagent" / "progress" / "workflow-state.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(state["wiki_status"], "fresh")
            self.assertEqual(state["pending_wiki_targets"], [])
            self.assertEqual(state["last_wiki_sync_strategy"], "aggressive")


class HeroAgentDocumentationTest(unittest.TestCase):
    def test_skill_declares_all_actions(self) -> None:
        skill_text = read_text(REPO_ROOT / "SKILL.md")
        actions = extract_backticked_values(skill_text, r"`~([a-z]+)`")
        self.assertEqual(actions, EXPECTED_ACTIONS)

    def test_skill_enforces_plan_then_confirm_then_todo(self) -> None:
        skill_text = read_text(REPO_ROOT / "SKILL.md")
        self.assertIn("收敛后，把计划写入 `.heroagent/plans/`", skill_text)
        self.assertIn("写完后等待用户确认", skill_text)
        self.assertIn("用户确认计划后，进入 `todo`", skill_text)

    def test_skill_enforces_todo_executes_from_confirmed_plan(self) -> None:
        skill_text = read_text(REPO_ROOT / "SKILL.md")
        self.assertIn("直接基于计划文档执行", skill_text)
        self.assertIn("需要留痕时，再补最小执行记录到 `tasks/`", skill_text)
        self.assertIn("不要把执行留痕当作进入 `todo` 的前置条件。", skill_text)

    def test_skill_references_existing_support_files(self) -> None:
        skill_text = read_text(REPO_ROOT / "SKILL.md")
        referenced_paths = extract_backticked_values(
            skill_text,
            r"`((?:references|assets/templates|scripts|examples)/[^`]+)`",
        )

        for relative_path in referenced_paths:
            with self.subTest(path=relative_path):
                self.assertTrue((REPO_ROOT / relative_path).exists(), relative_path)

    def test_readme_explicit_action_list_stays_complete(self) -> None:
        readme_text = read_text(REPO_ROOT / "README.md")
        match = re.search(
            r"推荐显式指令：\s*(.*?)\n### 初始化指令",
            readme_text,
            re.S,
        )
        self.assertIsNotNone(match)
        actions = extract_backticked_values(match.group(1), r"`~([a-z]+)`")
        self.assertEqual(actions, EXPECTED_ACTIONS)

    def test_readme_script_inventory_matches_repository(self) -> None:
        readme_text = read_text(REPO_ROOT / "README.md")
        match = re.search(
            r"仓库内已经提供一组可执行脚本，主要用于调试、批处理和验证公开能力：\s*(.*?)\n## ",
            readme_text,
            re.S,
        )
        self.assertIsNotNone(match)
        documented_scripts = extract_backticked_values(
            match.group(1),
            r"`scripts/([^`]+\.py)`",
        )

        actual_scripts = {
            path.name
            for path in SCRIPTS_DIR.glob("*.py")
            if path.name != "common.py" and path.name not in INTERNAL_ONLY_SCRIPTS
        }
        self.assertEqual(documented_scripts, actual_scripts)

    def test_readme_does_not_expose_internal_only_scripts(self) -> None:
        readme_text = read_text(REPO_ROOT / "README.md")
        for script_name in INTERNAL_ONLY_SCRIPTS:
            self.assertNotIn(f"`scripts/{script_name}`", readme_text)

    def test_agent_default_prompt_matches_plan_confirm_todo_flow(self) -> None:
        agent_config = read_text(REPO_ROOT / "agents" / "openai.yaml")
        self.assertIn("先收敛目标，再写入本地计划文档", agent_config)
        self.assertIn("计划确认后按计划执行", agent_config)

    def test_examples_capture_minimal_flows(self) -> None:
        examples_text = read_text(REPO_ROOT / "examples" / "minimal-flows.md")
        self.assertIn("## Want", examples_text)
        self.assertIn("## Plan", examples_text)
        self.assertIn("## Todo", examples_text)
        self.assertIn("## Focus", examples_text)
        self.assertIn("## Achieve", examples_text)
        self.assertIn("## Reflect", examples_text)

    def test_requirement_scoring_keeps_threshold_and_plan_handoff(self) -> None:
        scoring_text = read_text(REPO_ROOT / "references" / "core" / "requirement-scoring.md")
        self.assertIn("阈值 `8`", scoring_text)
        self.assertIn("评分达到 `>= 8` 后，不直接进入 `plan`", scoring_text)
        self.assertIn("`1. 继续下一步 ~plan`", scoring_text)

    def test_wiki_sync_rules_keep_detect_then_sync_model(self) -> None:
        wiki_sync_text = read_text(REPO_ROOT / "references" / "wiki" / "wiki-sync-rules.md")
        self.assertIn("1. `detect`：只判断本轮变更是否会让 wiki 失真，并记录待同步目标", wiki_sync_text)
        self.assertIn("2. `sync`：在关键节点再真正补写、生成草稿或合并正式 wiki", wiki_sync_text)
        self.assertIn("默认在执行 `todo` 之后、已经产生实际代码变更时，再做 `detect`", wiki_sync_text)
        self.assertIn("进入 `achieve` 或显式 `wiki` 请求前，优先补一次正式同步判断", wiki_sync_text)

    def test_wiki_generated_text_uses_action_or_state_wording(self) -> None:
        wiki_ops_text = read_text(REPO_ROOT / "scripts" / "lib" / "wiki_ops.py")
        self.assertIn("## 读取顺序", wiki_ops_text)
        self.assertIn("## 同步状态", wiki_ops_text)
        self.assertIn("## 状态定义", wiki_ops_text)
        self.assertIn("## 写回内容", wiki_ops_text)
        self.assertIn("priority=", wiki_ops_text)
        self.assertIn("updated_at=", wiki_ops_text)
        self.assertNotIn("## 建议写回", wiki_ops_text)


if __name__ == "__main__":
    unittest.main()
