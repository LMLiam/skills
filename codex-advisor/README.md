# Codex Advisor

This repository contains the Codex Advisor configuration.

The Advisor provides read-only technical judgement for difficult or high-risk
decisions. It does not implement changes.

## Contents

- `AGENTS.md` contains the related escalation policy.
- `agents/advisor.toml` defines the custom `advisor` agent.
- `skills/consulting-senior-advisor/` defines the consultation workflow.

## Install

Copy `agents/advisor.toml` to `~/.codex/agents/advisor.toml`.

Copy `skills/consulting-senior-advisor/` to
`~/.codex/skills/consulting-senior-advisor/`.

Add the policy in `AGENTS.md` to `~/.codex/AGENTS.md`.
