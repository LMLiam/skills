# OpenCode Zen Mixed Tier Selection

Select the least expensive tier that resolves the decision. Do not substitute a model, variant, or agent.

This profile uses the best available Zen model for each reasoning tier, chosen across model families. It runs through the OpenCode Zen provider (`opencode/`). No ChatGPT Plus/Pro OAuth, no Anthropic subscription, and no separate Google or xAI account are required beyond one Zen API key.

The profile is a flat ladder of thirteen tiers. Ability sets the order, from the Artificial Analysis Intelligence Index. Within one index value, the profile uses the cheapest model and variant. Each tier runs one model and one variant. The tiers intentionally mix model families (GPT-5.6, Gemini, Claude, Grok) inside one ladder.

Select the lowest tier whose ability resolves the decision. Do not use a higher tier when the current tier suffices; do not use a lower tier when evidence is incomplete or contradictory.

| Advisor | Model and variant | Intelligence Index | Use when |
| --- | --- | --- | --- |
| `advisor-luna-high` | `opencode/gpt-5.6-luna`, `high` | 47 | A lifecycle check-in where no binding recommendation is needed. |
| `advisor-pro3-medium` | `opencode/gemini-3.1-pro`, `medium` | 48 | A bounded low-risk decision with clear evidence. |
| `advisor-gem37-low` | `opencode/gemini-3.7-flash`, `low` | 51 | A routine decision that needs a careful but shallow pass. |
| `advisor-luna-max` | `opencode/gpt-5.6-luna`, `max` | 52 | A standard decision where cost matters and ability is ample. |
| `advisor-gem37-medium` | `opencode/gemini-3.7-flash`, `medium` | 53 | A bounded decision with moderate consequence. |
| `advisor-sonnet5-max` | `opencode/claude-sonnet-5`, `max` | 55 | An ambiguous or moderate-risk decision that needs careful synthesis. |
| `advisor-gem37-high` | `opencode/gemini-3.7-flash`, `high` | 56 | A decision that needs cross-model synthesis. |
| `advisor-sol-high` | `opencode/gpt-5.6-sol`, `high` | 57 | Material risk with clear evidence at strong reasoning. |
| `advisor-sol-xhigh` | `opencode/gpt-5.6-sol`, `xhigh` | 59 | Material risk with incomplete or partly conflicting evidence. |
| `advisor-grok46-xhigh` | `opencode/grok-4.6`, `xhigh` | 60 | Material risk where a strong reasoning ceiling is needed. |
| `advisor-sol-max` | `opencode/gpt-5.6-sol`, `max` | 61 | Security, concurrency, data integrity, public API, compatibility, migration, or irreversible-state risk is material, or evidence is conflicting. |
| `advisor-fable5-max` | `opencode/claude-fable-5`, `max` | 62 | The highest-ability Claude tier with Opus fallback, for the most consequential decisions. |
| `advisor-opus5-max` | `opencode/claude-opus-5`, `max` | 63 | The highest-ability tier available; use only for the most severe, irreversible decisions. |

Direction of reasoning: the ladder rises from cheap low-ability tiers to expensive high-ability tiers. Within one model family, spend more reasoning effort only when the cheaper effort tier does not resolve the decision.

Do not substitute a model, variant, or agent. If a configured model or variant is unavailable, do not substitute another advisor; ask the human whether to retry the same tier or continue without advice when that decision is material.

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
