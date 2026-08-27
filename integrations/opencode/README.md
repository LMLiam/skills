# Consulting Senior Advisor: OpenCode

This integration configures the `consulting-senior-advisor` skill for OpenCode 1.18.23 or later. It installs one explicit provider profile with seven named, read-only advisor agents.

The profile does not discover, rank, or substitute models. If a configured model is unavailable, installation stops.

## Install

Run the installer from the target project, or use its absolute path with `--project`. Without `--profile` or `--scope`, it asks which profile and installation scope to use.

```sh
python3 /path/to/skills/scripts/install-opencode.py --profile openai-gpt-5.6
```

Use `--dry-run` to inspect the files before installation.

```sh
python3 /path/to/skills/scripts/install-opencode.py --profile openai-gpt-5.6 --scope user --dry-run
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

## Profile

`openai-gpt-5.6` maps each tier to a fixed OpenAI model and variant. Do not treat its tier names as equivalent to another provider profile. Add another profile only after it has a reviewed mapping and passes the same installation, safety, and behavioural checks.
