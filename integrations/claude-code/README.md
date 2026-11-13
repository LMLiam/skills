# Orchestration Agents: Claude Code

This integration provides four Claude Code subagents and a working pattern for using them. The main session plans, delegates, spot-checks, and reports. Cheaper models do the searching, building, and implementing.

## Agents

| Agent | Model | Tools | Use for |
| --- | --- | --- | --- |
| [`scout`](agents/scout.md) | Haiku | Read, Bash, WebFetch, WebSearch | Read-only search, code reading, and research that returns a short, cited conclusion. |
| [`verifier`](agents/verifier.md) | Haiku | Read, Bash | Running builds, tests, and linters, or reading CI logs, and reporting the failing step. It does not fix code. |
| [`implementer`](agents/implementer.md) | Sonnet | All | One coherent unit of code work, about one commit, in a named worktree and branch. It commits locally and never pushes. |
| [`reviewer`](agents/reviewer.md) | Sonnet | All | Skeptical code-quality review of a branch against a base. It folds fixes into the right commits as fixups. |

Each agent reports in a fixed, short format. This keeps long output out of the main session.

## Install

Copy the agent files to one of these locations:

```sh
cp integrations/claude-code/agents/*.md ~/.claude/agents/     # all projects
cp integrations/claude-code/agents/*.md .claude/agents/       # one project
```

Restart Claude Code, or run `/agents`, to load them. Review the files before you install them. Each `description` tells the main session when to delegate, and `model` sets the default model.

## The Pattern

The main session does not do the bulk work. It decides what to do, writes a brief, and checks the result.

| Work | Agent |
| --- | --- |
| Search, summarising, reading logs or pages | `scout` (Haiku) |
| Running builds, tests, reading CI | `verifier` (Haiku) |
| Mechanical, fully specified edits | Haiku with an exact brief |
| Code that needs judgement or design | `implementer` (Sonnet) |
| Code-quality review | `reviewer` (Sonnet) |

Rules that make the pattern work:

- **Narrow briefs.** State the exact goal, files, constraints, verification, and report format. Pass only what the step needs. A cold agent has none of the session context.
- **One unit per agent.** Give each agent about one commit of work. Split larger work into sequential agents that each start from the previous reviewed commit. Run agents in parallel only when they do not touch the same files.
- **One worktree per agent.** Each implementer works in its own git worktree on a local branch, commits locally, and never pushes.
- **Review before handover.** Run `reviewer` on every change and fix real issues before a person sees it.
- **Verify against the brief.** Check that every item was delivered, nothing was quietly narrowed, and no test was weakened. Sample diffs and re-run the tests. Do not re-read everything.
- **Escalate on poor work.** Move from Haiku to Sonnet. If that fails, ask a read-only advisor how to approach the task. Then give the weak part to a fresh agent with a narrow brief.
- **Override the model sparingly.** Raise it on the call only when the task needs it: Haiku to Sonnet for judgement, Opus only for subtle or high-risk work such as invariants, concurrency, or public API shape.
- **The main session edits only small changes.** It edits code itself only for a change of a few lines whose context it already holds, because a cold agent would cost more.

### Optional Read-Only Advisor

When a decision stays open after reading the source, tests, and docs, consult an advisor on a stronger model. Do not consult it for routine edits or for decisions that belong to a person. The advisor starts cold, so give it the decision, the options, the evidence, and the constraints. Ask for a recommendation with its reasons in under 200 words. It does not edit code.

The [`consulting-senior-advisor`](../../skills/consulting-senior-advisor/) skill in this repository implements this workflow.

## Suggested CLAUDE.md Snippet

Add this to your user or project `CLAUDE.md` so the main session follows the pattern. Adjust the wording to your own process.

````markdown
## Orchestration

The main session plans, delegates, spot-checks, and reports. Builds, debugging, research, and implementation go to subagents on cheaper models. Edit code in the main session only for a change of a few lines whose context you already hold.

Each agent's frontmatter sets its default model. Override it on the call only when the task needs it: Haiku to Sonnet for judgement, Opus only for subtle or high-risk work.

| Work | Agent |
|---|---|
| Search, summarising, reading logs or pages | `scout` |
| Running builds, tests, reading CI | `verifier` |
| Mechanical, fully specified edits | Haiku with an exact brief |
| Code that needs judgement or design | `implementer` |
| Code-quality review | `reviewer` |

- One coherent unit per agent, about one commit's worth. Split larger work into sequential agents. Parallelise only when the pieces do not touch the same files.
- Briefs are explicit and narrow: exact goal, files, constraints, verification, report format.
- Escalate when an agent does a poor job: Haiku to Sonnet, then ask a read-only advisor. Give the weak part to a fresh agent with a narrow brief.
- Verify against the brief, not the agent's report: every item delivered, nothing quietly narrowed, no weakened tests.

## Delivering code

1. Agents work in a separate worktree on a local branch and commit locally.
2. Every change gets a code-quality review, and real issues are fixed before handover.
3. Remove the worktree to free the branch, then report the branch and what to compare it with.
4. Push and open a PR only after approval.
5. After opening or pushing to a PR, watch CI. On failure, diagnose it, then re-run if it is transient or fix it.
````

## Customise

- Add project rules to your `AGENTS.md` or `CLAUDE.md`. The `implementer` and `reviewer` read it first and follow it.
- Set `tools` in the frontmatter to restrict an agent. `scout` and `verifier` have no edit tools, and that is the capability boundary. A prompt instruction alone is not one.
- Change `model` to suit your plan and the models you have access to.
