# OpenCode Zen GPT-5.6 Tier Selection

Select the least expensive tier that resolves the decision. Do not substitute a model, variant, or agent.

This profile is identical in tier mapping to `openai-gpt-5.6` but uses the OpenCode Zen provider (`opencode/`) so no ChatGPT Plus/Pro OAuth is required. One Zen API key covers all models.

| Advisor | Use when | Model and variant |
| --- | --- | --- |
| `advisor-terra-high` | The evidence is compact, the constraints are few, and the consequence is limited. | `opencode/gpt-5.6-terra`, `high` |
| `advisor-terra-xhigh` | The evidence spans several paths and needs careful synthesis, but little novel inference. | `opencode/gpt-5.6-terra`, `xhigh` |
| `advisor-terra-max` | The decision is difficult and bounded, risk is lower, and complete evidence should resolve it. | `opencode/gpt-5.6-terra`, `max` |
| `advisor-sol-medium` | The decision is ambiguous or high leverage and requires difficult inference or trade-offs. | `opencode/gpt-5.6-sol`, `medium` |
| `advisor-sol-high` | Several explanations are plausible, interactions are subtle, or security, concurrency, data integrity, public API, compatibility, migration, or irreversible-state risk is material. | `opencode/gpt-5.6-sol`, `high` |
| `advisor-sol-xhigh` | Constraints interact, evidence is incomplete or contradictory, or a lower tier left the central uncertainty unresolved. | `opencode/gpt-5.6-sol`, `xhigh` |
| `advisor-sol-max` | Difficulty and cost of error are exceptional, or conflicting evidence defeated a lower tier. | `opencode/gpt-5.6-sol`, `max` |

Breadth favours Terra. Ambiguity, novel inference, and high consequences favour Sol. Do not use Luna, `low`, Terra `medium`, Sol `low`, or `ultra`. Skip consultation when those depths would suffice.

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
