"""Black-box checks for the OpenCode advisor integration commands."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
INSTALLER = REPOSITORY_ROOT / "scripts" / "install-opencode.py"
VALIDATOR = REPOSITORY_ROOT / "scripts" / "validate.py"
sys.path.insert(0, str(REPOSITORY_ROOT / "scripts"))

from validate import flat_permissions


def run_command(
    *arguments: str,
    directory: Path = REPOSITORY_ROOT,
    input_text: str | None = None,
) -> subprocess.CompletedProcess[str]:
    """Run one public repository command and capture its result."""
    return subprocess.run(arguments, cwd=directory, capture_output=True, input=input_text, text=True)


class OpenCodeIntegrationTests(unittest.TestCase):
    """Verify installation and validation as users invoke them."""

    def test_validator_accepts_published_profile(self) -> None:
        result = run_command("python3", str(VALIDATOR))

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Skill and OpenCode profiles are valid.", result.stdout)

    def test_permission_parser_rejects_nested_and_duplicate_rules(self) -> None:
        with self.assertRaisesRegex(ValueError, "flat allow or deny"):
            flat_permissions('permission:\n  bash:\n    "*": allow')
        with self.assertRaisesRegex(ValueError, "Duplicate advisor permission entry"):
            flat_permissions('permission:\n  read: allow\n  read: deny')

    def test_project_install_detects_and_replaces_modified_file(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            project = Path(temporary_directory)
            command = (
                "python3",
                str(INSTALLER),
                "--profile",
                "openai-gpt-5.6",
                "--scope",
                "project",
            )
            installed = run_command(*command, directory=project)

            self.assertEqual(installed.returncode, 0, installed.stderr)
            agent = project / ".opencode" / "agents" / "advisor-sol-medium.md"
            self.assertTrue(agent.is_file())
            reference = project / ".opencode" / "skills" / "consulting-senior-advisor" / "references"
            self.assertTrue((reference / "active-integration.md").is_file())
            self.assertFalse((project / ".opencode" / "skills" / "consulting-senior-advisor" / "evals").exists())
            self.assertFalse((reference / "adapter-contract.md").exists())
            checked = run_command(*command, "--check", directory=project)

            self.assertEqual(checked.returncode, 0, checked.stderr)
            agent.write_text("changed")

            protected = run_command(*command, directory=project)

            self.assertNotEqual(protected.returncode, 0)
            self.assertIn("refusing to replace modified file", protected.stdout)
            restored = run_command(*command, "--force", directory=project)

            self.assertEqual(restored.returncode, 0, restored.stderr)
            self.assertIn("model: openai/gpt-5.6-sol", agent.read_text())

    def test_project_install_refuses_symbolic_link_target(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            project = Path(temporary_directory)
            agent = project / ".opencode" / "agents" / "advisor-sol-medium.md"
            agent.parent.mkdir(parents=True)
            agent.symlink_to(project / "outside.md")
            result = run_command(
                "python3",
                str(INSTALLER),
                "--profile",
                "openai-gpt-5.6",
                "--scope",
                "project",
                "--force",
                directory=project,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("refusing unsafe destination", result.stdout)

    def test_project_install_refuses_symbolic_link_parent_before_copying(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            project = Path(temporary_directory)
            config = project / ".opencode"
            outside = project / "outside"
            config.mkdir()
            outside.mkdir()
            (config / "agents").symlink_to(outside, target_is_directory=True)
            result = run_command(
                "python3",
                str(INSTALLER),
                "--profile",
                "openai-gpt-5.6",
                "--scope",
                "project",
                "--force",
                directory=project,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("refusing unsafe destination", result.stdout)
            self.assertFalse((config / "skills").exists())

    def test_project_option_installs_in_the_requested_project(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_root = Path(temporary_directory)
            project = temporary_root / "project"
            project.mkdir()
            result = run_command(
                "python3",
                str(INSTALLER),
                "--profile",
                "openai-gpt-5.6",
                "--scope",
                "project",
                "--project",
                str(project),
                "--dry-run",
                directory=temporary_root,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn(str(project / ".opencode"), result.stdout)
            self.assertFalse((project / ".opencode").exists())

    def test_dry_run_does_not_create_project_configuration(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            project = Path(temporary_directory)
            result = run_command(
                "python3",
                str(INSTALLER),
                "--profile",
                "openai-gpt-5.6",
                "--scope",
                "project",
                "--dry-run",
                directory=project,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("would install", result.stdout)
            self.assertFalse((project / ".opencode").exists())

    def test_interactive_selection_accepts_profile_and_scope(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            project = Path(temporary_directory)
            result = run_command(
                "python3",
                str(INSTALLER),
                "--dry-run",
                directory=project,
                input_text="openai-gpt-5.6\nproject\n",
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Profile (", result.stdout)
            self.assertIn("openai-gpt-5.6", result.stdout)
            self.assertIn("Scope (user/project) [user]:", result.stdout)


if __name__ == "__main__":
    unittest.main()
