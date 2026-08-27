# OpenCode Permission Probes

Run these probes in a fresh temporary project after you install a profile with `--scope project`.

```sh
opencode agent list
```

For every `advisor-*` agent, confirm that the final agent-specific rules are:

```text
*     deny
read  allow
glob  allow
grep  allow
list  allow
lsp   allow
```

In a primary-agent session, ask the agent to invoke `task` with `subagent_type` set to `advisor-terra-high`. Confirm that the advisor starts. This step is required because `hidden: true` omits advisors from `@` autocomplete.

Then ask the advisor to inspect a known source file. Confirm that it can read and search the project.

In separate sessions, ask the advisor to run a shell command, edit a file, and start a nested task. OpenCode must deny each action. Do not use `--auto`, because it changes approvals that are not explicitly denied.

Record the OpenCode version, selected profile, and results. Run these probes again after an OpenCode upgrade or a permission change.
