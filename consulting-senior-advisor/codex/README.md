# Consulting Senior Advisor: Codex

This directory contains the Codex files for the `consulting-senior-advisor` skill.

The skill routes difficult or high-risk decisions to a read-only advisor. The advisor provides judgement and does not implement changes.

## Contents

| Path | Purpose |
| --- | --- |
| `AGENTS.md` | Related escalation policy. |
| `agents/advisor.toml` | Definition of the custom `advisor` agent. |
| `skills/consulting-senior-advisor/` | Consultation workflow skill. |

## Install

Copy `agents/advisor.toml` to `~/.codex/agents/advisor.toml`.

Copy `skills/consulting-senior-advisor/` to
`~/.codex/skills/consulting-senior-advisor/`.

Add the policy in `AGENTS.md` to `~/.codex/AGENTS.md`.
