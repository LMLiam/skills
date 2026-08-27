# OpenCode Zen Gemini 3 Tier Selection

Select the least expensive tier that resolves the decision. Do not substitute a model, variant, or agent.

This profile uses the Google Gemini 3 family through the OpenCode Zen provider (`opencode/`). No ChatGPT Plus/Pro OAuth, no Anthropic subscription, and no separate Google account are required beyond one Zen API key.

The profile arranges two models as a cost-and-power escalation ladder. Flash 3.7 is the workhorse and Pro 3.1 is the escalation.

| Advisor | Model and variant | Use when |
| --- | --- | --- |
| `advisor-flash-medium` | `opencode/gemini-3.7-flash`, `medium` | A lifecycle check-in where no binding recommendation is needed. |
| `advisor-flash-high` | `opencode/gemini-3.7-flash`, `high` | A bounded decision with moderate consequence, or an ambiguous decision that needs careful synthesis. |
| `advisor-pro-medium` | `opencode/gemini-3.1-pro`, `medium` | Material risk with clear evidence, where Pro grade is wanted but full effort is not yet needed. |
| `advisor-pro-high` | `opencode/gemini-3.1-pro`, `high` | Security, concurrency, data integrity, public API, compatibility, migration, or irreversible-state risk is material, or evidence is incomplete or contradictory. |

Direction of reasoning: Flash for day-to-day work, Pro for material risk and conflicting evidence. Within a model, spend more reasoning effort (`variant`) only when the cheaper variant does not resolve the decision. Do not use `minimal` or `low`. Do not substitute a model, variant, or agent. If a configured model or variant is unavailable, do not substitute another advisor; ask the human whether to retry the same tier or continue without advice when that decision is material.

## Invoke And Wait

In OpenCode, invoke the selected advisor in the foreground:

```text
task({
  description: "Review technical decision",
  subagent_type: "<exact advisor name from this table>",
  prompt: "<decision packet>"
})
```

Do not use background mode. Wait for a terminal result before implementation. If the advisor, model, or variant is unavailable, do not substitute another advisor. Ask the human whether to retry the same tier or continue without advice when that decision is material.
