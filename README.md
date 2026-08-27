# Skills

Shareable Agent Skills with harness-specific integration assets.

## Available Skills

| Skill | Purpose | Integrations |
| --- | --- | --- |
| [`consulting-senior-advisor`](skills/consulting-senior-advisor/) | Routes difficult technical decisions to an advice-only senior advisor. | [OpenCode](integrations/opencode/) |

## Architecture

Each skill under `skills/` follows the [Agent Skills specification](https://agentskills.io/specification). It contains portable workflow rules and does not select a model provider.

An integration configures one harness. It owns harness tools, permissions, installation, and failure handling. Each integration follows the [integration contract](integrations/README.md). An OpenCode provider profile maps a consultation tier to an explicit agent, model, and variant. The workflow never discovers, ranks, or selects models at runtime.

```text
skills/                         # Portable, standard Agent Skills
integrations/                   # Harness configuration and provider profiles
scripts/                        # Repository validation
```

## Install

Install the portable skill with a compatible Agent Skills installer, or place `skills/<name>/` in your harness skill directory. Then install the OpenCode integration before you use the skill.

Use the [OpenCode integration guide](integrations/opencode/README.md).

The integrations are not installed by a skill installer. They contain harness configuration that needs local review before installation.

## Validate

Run the repository validator before a change:

```sh
python3 scripts/validate.py
npx --yes skills-ref@0.1.5 validate skills/consulting-senior-advisor
```

The validator checks the published structure, profile-to-agent mapping, and OpenCode read-only permissions. It does not prove a provider will accept a model or variant. Run the integration checks in its guide before use.

## Versioning

This repository uses semantic versioning for released skills. Record user-visible changes in [CHANGELOG.md](CHANGELOG.md). Create a release tag after the pull request has merged and the published artefacts have passed validation.
