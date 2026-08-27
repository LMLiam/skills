#!/usr/bin/env python3
"""Install one reviewed OpenCode advisor profile without changing opencode.json."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

from opencode_profile import (
    POLICY_SOURCE,
    REPOSITORY_ROOT,
    SKILL_ROOT,
    Profile,
    available_profiles,
    load_profile,
)


def parse_arguments() -> argparse.Namespace:
    """Parse installation controls."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", choices=available_profiles())
    parser.add_argument("--scope", choices=("user", "project"))
    parser.add_argument("--project", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


def select_value(label: str, values: tuple[str, ...], default: str | None = None) -> str:
    """Prompt for one value from a small, fixed list."""
    prompt = f"{label} ({'/'.join(values)})"
    if default:
        prompt = f"{prompt} [{default}]"
    value = input(f"{prompt}: ").strip() or default
    if value not in values:
        raise ValueError(f"Invalid {label.lower()}: {value}")
    return value


def select_options(arguments: argparse.Namespace) -> tuple[Profile, str]:
    """Resolve command-line options, prompting only when necessary."""
    profile_name = arguments.profile or select_value("Profile", available_profiles())
    scope = arguments.scope or select_value("Scope", ("user", "project"), "user")
    return load_profile(profile_name), scope


def opencode_version() -> str:
    """Return the installed OpenCode version."""
    result = subprocess.run(
        ["opencode", "--version"],
        check=True,
        capture_output=True,
        cwd=REPOSITORY_ROOT,
        text=True,
    )
    return result.stdout.strip()


def version_tuple(version: str) -> tuple[int, int, int]:
    """Convert a release version to a comparable three-part tuple."""
    try:
        parts = tuple(int(part) for part in version.split(".", maxsplit=2))
    except ValueError as error:
        raise ValueError(f"Unsupported OpenCode version: {version}") from error
    if len(parts) != 3:
        raise ValueError(f"Unsupported OpenCode version: {version}")
    return parts


def verify_opencode(profile: Profile, project: Path) -> None:
    """Confirm the installed OpenCode version and configured models are visible."""
    installed = opencode_version()
    if version_tuple(installed) < version_tuple(profile.minimum_opencode_version):
        raise ValueError(
            f"OpenCode {profile.minimum_opencode_version} or later is required; found {installed}"
        )

    result = subprocess.run(
        ["opencode", "--pure", "models", profile.provider],
        check=True,
        capture_output=True,
        cwd=project,
        text=True,
    )
    visible_models = set(result.stdout.splitlines())
    missing = sorted({agent.model for agent in profile.agents} - visible_models)
    if missing:
        raise ValueError(f"Configured models are unavailable: {', '.join(missing)}")


def project_root(project: Path | None) -> Path:
    """Return the selected project directory or the current directory."""
    return (project or Path.cwd()).resolve()


def destination_root(scope: str, project: Path) -> Path:
    """Return the OpenCode configuration directory for the requested scope."""
    if scope == "user":
        return Path.home() / ".config" / "opencode"
    return project / ".opencode"


def installation_files(profile: Profile, destination: Path) -> tuple[tuple[Path, Path], ...]:
    """Map each source file to its exact destination."""
    skill_files = tuple(
        (source, destination / "skills" / source.relative_to(SKILL_ROOT))
        for source in SKILL_ROOT.rglob("*")
    )
    agent_root = profile.directory / "agents"
    agent_files = tuple((source, destination / "agents" / source.name) for source in agent_root.glob("*.md"))
    selected_files = tuple(
        (source, target)
        for source, target in (*skill_files, *agent_files)
        if source.is_file()
    )
    selection_target = (
        destination
        / "skills"
        / "consulting-senior-advisor"
        / "references"
        / "active-integration.md"
    )
    return selected_files + (
        (POLICY_SOURCE, destination / "advisor-policy.md"),
        (profile.directory / "selection.md", selection_target),
    )


def changed_targets(files: tuple[tuple[Path, Path], ...]) -> tuple[Path, ...]:
    """Return existing targets that are not identical to their source."""
    return tuple(target for source, target in files if target.exists() and source.read_bytes() != target.read_bytes())


def unsafe_paths(files: tuple[tuple[Path, Path], ...], destination: Path) -> tuple[Path, ...]:
    """Return unsafe target files and parent directories before installation."""
    paths: set[Path] = set()
    for _, target in files:
        if target.is_symlink() or (target.exists() and not target.is_file()):
            paths.add(target)
        parent = target.parent
        while parent != destination.parent:
            if parent.is_symlink() or (parent.exists() and not parent.is_dir()):
                paths.add(parent)
            parent = parent.parent
    return tuple(sorted(paths))


def install(files: tuple[tuple[Path, Path], ...]) -> None:
    """Copy reviewed assets after conflict checks have completed."""
    for source, target in files:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def report_files(heading: str, files: tuple[Path, ...]) -> None:
    """Print one labelled line per path."""
    for path in files:
        print(f"{heading}: {path}")


def main() -> int:
    """Run the installation, check, or dry-run command."""
    try:
        arguments = parse_arguments()
        profile, scope = select_options(arguments)
        project = project_root(arguments.project)
        if arguments.project and scope != "project":
            raise ValueError("--project requires --scope project")
        verify_opencode(profile, project)
        destination = destination_root(scope, project)
        files = installation_files(profile, destination)
        unsafe = unsafe_paths(files, destination)
        if unsafe:
            report_files("refusing unsafe destination", unsafe)
            return 1
        changed = changed_targets(files)
        if arguments.check:
            missing = tuple(target for _, target in files if not target.exists())
            report_files("missing", missing)
            report_files("modified", changed)
            return int(bool(missing or changed))
        if changed and not arguments.force:
            report_files("refusing to replace modified file", changed)
            return 1
        if arguments.dry_run:
            report_files("would install", tuple(target for _, target in files))
            return 0
        install(files)
        print(f"Installed profile {profile.name} in {destination}")
        print("Add advisor-policy.md to the instructions array in opencode.json.")
        return 0
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
