#!/usr/bin/env python3
"""Validate the published skill and OpenCode advisor profile invariants."""

from __future__ import annotations

import re
import sys
from pathlib import Path

from opencode_profile import (
    POLICY_SOURCE,
    REQUIRED_PERMISSIONS,
    SKILL_ROOT,
    available_profiles,
    load_profile,
)


FIELD_PATTERN = re.compile(r"^(model|variant):\s*(.+)$", re.MULTILINE)
PERMISSION_ENTRY = re.compile(r'^  ("\*"|[a-z_]+): (allow|ask|deny)$')
REQUIRED_ADVISOR_TEXT = (
    "You provide advice. You do not implement changes.",
    "Do not force a recommendation when evidence is insufficient.",
    "1. Recommendation",
    "7. Whether the executor should proceed, investigate further, or change course",
)


def frontmatter(path: Path) -> str:
    """Return YAML frontmatter from a Markdown file."""
    parts = path.read_text().split("---", maxsplit=2)
    if len(parts) != 3 or parts[0] != "":
        raise ValueError(f"Missing frontmatter: {path}")
    return parts[1]


def validate_skill(errors: list[str]) -> None:
    """Check the required Agent Skills identity fields."""
    skill = SKILL_ROOT / "SKILL.md"
    try:
        data = frontmatter(skill)
    except (OSError, ValueError) as error:
        errors.append(str(error))
        return
    if "name: consulting-senior-advisor" not in data:
        errors.append(f"Skill name does not match its directory: {skill}")
    if "description:" not in data:
        errors.append(f"Skill has no description: {skill}")


def flat_permissions(data: str) -> dict[str, str]:
    """Parse the approved flat permission mapping and reject all other YAML forms."""
    lines = data.splitlines()
    try:
        start = lines.index("permission:") + 1
    except ValueError as error:
        raise ValueError("Missing advisor permission mapping") from error

    permissions: dict[str, str] = {}
    for line in lines[start:]:
        if not line:
            continue
        if not line.startswith(" "):
            break
        match = PERMISSION_ENTRY.fullmatch(line)
        if not match:
            raise ValueError("Advisor permission mapping must contain flat allow or deny entries")
        name, action = match.groups()
        name = name.strip('"')
        if name in permissions:
            raise ValueError(f"Duplicate advisor permission entry: {name}")
        permissions[name] = action
    return permissions


def agent_metadata(path: Path) -> tuple[dict[str, str], dict[str, str]]:
    """Parse the fixed scalar metadata and flat permissions used by advisor agents."""
    data = frontmatter(path)
    metadata = {name: value for name, value in FIELD_PATTERN.findall(data)}
    return metadata, flat_permissions(data)


def validate_profile(name: str, errors: list[str]) -> None:
    """Check profile metadata, agent mapping, and capability restrictions."""
    try:
        profile = load_profile(name)
    except ValueError as error:
        errors.append(str(error))
        return

    agent_root = profile.directory / "agents"
    actual_agents = {path.stem for path in agent_root.glob("*.md")}
    expected_agents = {agent.name for agent in profile.agents}
    if actual_agents != expected_agents:
        errors.append(f"Profile agent files do not match profile metadata: {profile.name}")
    selection = profile.directory / "selection.md"
    if not selection.is_file():
        errors.append(f"Profile selection guide is missing: {selection}")
    elif any(agent.name not in selection.read_text() for agent in profile.agents):
        errors.append(f"Profile selection guide does not map every advisor: {selection}")

    for agent in profile.agents:
        path = agent_root / f"{agent.name}.md"
        try:
            metadata, permissions = agent_metadata(path)
        except (OSError, ValueError) as error:
            errors.append(str(error))
            continue
        if metadata != {"model": agent.model, "variant": agent.variant}:
            errors.append(f"Model or variant differs from profile: {path}")
        if permissions != REQUIRED_PERMISSIONS:
            errors.append(
                f"Advisor permissions are not the required default-deny allow-list: {path}"
            )
        content = path.read_text()
        if any(text not in content for text in REQUIRED_ADVISOR_TEXT):
            errors.append(f"Advisor response contract is incomplete: {path}")


def main() -> int:
    """Print all validation failures and return a shell status."""
    errors: list[str] = []
    validate_skill(errors)
    if not POLICY_SOURCE.is_file():
        errors.append(f"Missing OpenCode policy: {POLICY_SOURCE}")
    for profile in available_profiles():
        validate_profile(profile, errors)
    if errors:
        print("\n".join(f"error: {error}" for error in errors), file=sys.stderr)
        return 1
    print("Skill and OpenCode profiles are valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
