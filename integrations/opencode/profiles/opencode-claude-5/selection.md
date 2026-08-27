# OpenCode Zen Claude 5 Tier Selection

Select the least expensive tier that resolves the decision. Do not substitute a model, variant, or agent.

This profile uses the Anthropic Claude 5 family through the OpenCode Zen provider (`opencode/`). No ChatGPT Plus/Pro OAuth and no separate Anthropic API key are required. One Zen API key covers all models.

The profile arranges three models as a cost-and-power escalation ladder. Sonnet 5 is the workhorse, Opus 5 is the escalation, and Fable 5 is the exceptional ceiling.

| Advisor | Model and variant | Use when |
| --- | --- | --- |
| `advisor-sonnet-medium` | `opencode/claude-sonnet-5`, `medium` | A lifecycle check-in where no binding recommendation is needed. |
| `advisor-sonnet-high` | `opencode/claude-sonnet-5`, `high` | A bounded decision with moderate consequence and clear evidence. |
| `advisor-sonnet-xhigh` | `opencode/claude-sonnet-5`, `xhigh` | A difficult but bounded decision that needs careful synthesis. |
| `advisor-sonnet-max` | `opencode/claude-sonnet-5`, `max` | An ambiguous or high-leverage decision at Sonnet's capacity ceiling. |
| `advisor-opus-medium` | `opencode/claude-opus-5`, `medium` | Material risk and clear evidence, where Opus grade is wanted but full effort is not yet needed. |
| `advisor-opus-high` | `opencode/claude-opus-5`, `high` | Security, concurrency, data integrity, public API, compatibility, migration, or irreversible-state risk is material, with several plausible explanations. |
| `advisor-opus-xhigh` | `opencode/claude-opus-5`, `xhigh` | Constraints interact, or evidence is incomplete or contradictory. |
| `advisor-opus-max` | `opencode/claude-opus-5`, `max` | Opus's capacity ceiling, with exceptional difficulty and cost of error. |
| `advisor-fable-xhigh` | `opencode/claude-fable-5`, `xhigh` | Opus-max is insufficient, or a very large decision packet needs the full 1M-token context. |
| `advisor-fable-max` | `opencode/claude-fable-5`, `max` | The highest-leverage, highest-cost-of-error judgement in the profile. |

Direction of reasoning: Sonnet for day-to-day work, Opus for material risk and conflicting evidence, Fable for the exceptional ceiling. Within a model, spend more reasoning effort (`variant`) only when the cheaper variant does not resolve the decision. Do not use `low`. Do not substitute a model, variant, or agent. If a configured model or variant is unavailable, do not substitute another advisor; ask the human whether to retry the same tier or continue without advice when that decision is material.

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
