import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
PYTHON = sys.executable


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


class HeroAgentScriptsTest(unittest.TestCase):
    def test_init_creates_workspace_structure(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            result = run_script("init_heroagent.py", tmpdir)
            self.assertEqual(result.returncode, 0, result.stderr)

            root = Path(tmpdir) / ".heroagent"
            self.assertTrue((root / "goals").is_dir())
            self.assertTrue((root / "progress" / "current-focus.md").exists())
            self.assertTrue((root / "README.md").exists())

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
            tasks = list((root / "tasks").glob("*.md"))
            self.assertEqual(len(goals), 1)
            self.assertEqual(len(plans), 1)
            self.assertEqual(len(tasks), 1)
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

    def test_archive_moves_goal_related_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            run_script("bootstrap_first_goal.py", "规范团队周报流程", tmpdir, "--refresh-focus")
            slug = "goal-d348d219"

            result = run_script("archive_goal.py", "--slug", slug, "--reset-focus", tmpdir)
            self.assertEqual(result.returncode, 0, result.stderr)

            archive_dirs = list((Path(tmpdir) / ".heroagent" / "archive").glob(f"*_{slug}"))
            self.assertEqual(len(archive_dirs), 1)
            archive_dir = archive_dirs[0]
            self.assertTrue((archive_dir / f"goals__{archive_dir.name}.md").exists())
            self.assertTrue((archive_dir / f"plans__{archive_dir.name}.md").exists())
            self.assertTrue((archive_dir / f"tasks__{archive_dir.name}.md").exists())

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


if __name__ == "__main__":
    unittest.main()
