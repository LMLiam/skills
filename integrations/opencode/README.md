# Consulting Senior Advisor: OpenCode

This integration configures the `consulting-senior-advisor` skill for OpenCode 1.18.23 or later. It installs one explicit provider profile at a time with a set of named, read-only advisor agents.

The profile does not discover, rank, or substitute models. If a configured model is unavailable, installation stops.

## Install

Run the installer from the target project, or use its absolute path with `--project`. Without `--profile` or `--scope`, it asks which profile and installation scope to use.

```sh
python3 /path/to/skills/scripts/install-opencode.py --profile openai-gpt-5.6
python3 /path/to/skills/scripts/install-opencode.py --profile opencode-gpt-5.6
```

Use `--dry-run` to inspect the files before installation.

```sh
python3 /path/to/skills/scripts/install-opencode.py --profile openai-gpt-5.6 --scope user --dry-run
python3 /path/to/skills/scripts/install-opencode.py --profile opencode-gpt-5.6 --scope user --dry-run
```

Use `--scope project` to install under `.opencode/` in the current project. Add `--project /path/to/project` to install in another project. Use `--scope user` to install under `~/.config/opencode/`.

The installer refuses to replace a changed installed file. Use `--force` only after you review the replacement.

## Enable The Policy

The installer copies `advisor-policy.md` but does not modify `opencode.json`. Add its installed path to the `instructions` array yourself.

For a user installation, use:

```json
{
  "instructions": [
    "~/.config/opencode/advisor-policy.md"
  ]
}
```

For a project installation, use:

```json
{
  "instructions": [
    ".opencode/advisor-policy.md"
  ]
}
```

Preserve your existing instruction paths.

## Validate

Run these commands from the repository root:

```sh
python3 scripts/validate.py
python3 scripts/install-opencode.py --profile openai-gpt-5.6 --scope project --dry-run
```

Run `opencode agent list` after installation. Confirm that every `advisor-*` agent has the configured model and a default-deny permission policy with inspection tools only.

Use [the permission probes](tests/permission-probes.md) to verify enforcement after an OpenCode upgrade or a profile change.

## Profiles

| Profile | Provider | Models | Auth |
| --- | --- | --- | --- |
| `openai-gpt-5.6` | `openai` | `openai/gpt-5.6-terra`, `openai/gpt-5.6-sol` | ChatGPT Plus/Pro OAuth or `OPENAI_API_KEY` |
| `opencode-gpt-5.6` | `opencode` | `opencode/gpt-5.6-terra`, `opencode/gpt-5.6-sol` | OpenCode Zen API key (`/connect` → `opencode`) — no ChatGPT subscription required |
| `opencode-claude-5` | `opencode` | `opencode/claude-sonnet-5`, `opencode/claude-opus-5`, `opencode/claude-fable-5` | OpenCode Zen API key (`/connect` → `opencode`) — no ChatGPT or Anthropic subscription required |
| `opencode-gemini-3` | `opencode` | `opencode/gemini-3.7-flash`, `opencode/gemini-3.1-pro` | OpenCode Zen API key (`/connect` → `opencode`) — no ChatGPT, Anthropic, or Google subscription required |
| `opencode-mixed` | `opencode` | `opencode/gpt-5.6-sol`, `opencode/gpt-5.6-luna`, `opencode/gemini-3.7-flash`, `opencode/gemini-3.1-pro`, `opencode/claude-sonnet-5`, `opencode/claude-opus-5`, `opencode/claude-fable-5`, `opencode/grok-4.6` | OpenCode Zen API key (`/connect` → `opencode`) — no ChatGPT, Anthropic, Google, or xAI subscription required |

`openai-gpt-5.6` and `opencode-gpt-5.6` share identical tier mappings (Terra for breadth, Sol for ambiguity and high consequence). Each other profile is native to its model family and defines its own agent surface: `opencode-claude-5` uses ten tiers across Sonnet 5, Opus 5, and Fable 5; `opencode-gemini-3` uses four tiers across Flash 3.7 and Pro 3.1. The `opencode-mixed` profile is different: it is a flat ladder of twelve tiers that spans model families, ordered by the Artificial Analysis Intelligence Index with price as the tiebreak, and each tier is named by its model and variant. Do not treat tier names as equivalent to another provider profile. Add another profile only after it has a reviewed mapping and passes the same installation, safety, and behavioural checks.
