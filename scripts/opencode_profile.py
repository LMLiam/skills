"""Load and validate OpenCode advisor profile metadata."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
PROFILE_ROOT = REPOSITORY_ROOT / "integrations" / "opencode" / "profiles"
SKILL_ROOT = REPOSITORY_ROOT / "skills" / "consulting-senior-advisor"
POLICY_SOURCE = (
    REPOSITORY_ROOT / "integrations" / "opencode" / "policy" / "advisor-policy.md"
)
REQUIRED_PERMISSIONS = {
    "*": "deny",
    "read": "allow",
    "glob": "allow",
    "grep": "allow",
    "list": "allow",
    "lsp": "allow",
}


@dataclass(frozen=True)
class AdvisorAgent:
    """One named OpenCode advisor agent."""

    name: str
    model: str
    variant: str


@dataclass(frozen=True)
class Profile:
    """A reviewed mapping from advisor names to a provider model."""

    name: str
    minimum_opencode_version: str
    provider: str
    agents: tuple[AdvisorAgent, ...]

    @property
    def directory(self) -> Path:
        return PROFILE_ROOT / self.name


def available_profiles() -> tuple[str, ...]:
    """Return sorted profile names that have profile metadata."""
    return tuple(sorted(path.parent.name for path in PROFILE_ROOT.glob("*/profile.json")))


def load_profile(name: str) -> Profile:
    """Load one profile after checking its required JSON fields."""
    path = PROFILE_ROOT / name / "profile.json"
    try:
        data = json.loads(path.read_text())
    except FileNotFoundError as error:
        raise ValueError(f"Unknown profile: {name}") from error
    except json.JSONDecodeError as error:
        raise ValueError(f"Invalid JSON in {path}: {error.msg}") from error

    if not isinstance(data, dict):
        raise ValueError(f"Profile must be a JSON object: {path}")
    if data.get("name") != name:
        raise ValueError(f"Profile name does not match directory: {path}")

    fields = ("minimum_opencode_version", "provider", "agents")
    if any(not data.get(field) for field in fields):
        raise ValueError(f"Profile is missing a required field: {path}")
    if not all(isinstance(data[field], str) for field in fields[:2]):
        raise ValueError(f"Profile version and provider must be strings: {path}")

    agent_data = data["agents"]
    if not isinstance(agent_data, dict) or not agent_data:
        raise ValueError(f"Profile agents must be a non-empty object: {path}")

    agents = tuple(
        AdvisorAgent(agent_name, details.get("model", ""), details.get("variant", ""))
        for agent_name, details in sorted(agent_data.items())
        if isinstance(agent_name, str) and isinstance(details, dict)
    )
    if len(agents) != len(agent_data) or any(
        not isinstance(agent.model, str)
        or not isinstance(agent.variant, str)
        or not agent.model
        or not agent.variant
        for agent in agents
    ):
        raise ValueError(f"Every profile agent requires a model and variant: {path}")

    return Profile(name, data["minimum_opencode_version"], data["provider"], agents)
