---
name: consulting-senior-advisor
description: Use when a difficult architecture, diagnosis, concurrency, security, data-integrity, compatibility, migration, public-API, or completion-review decision remains unresolved after evidence gathering and requires stronger technical judgement.
---

# Consulting Senior Advisor

Use one sequential, read-only advisor call for a precise technical decision. The executor retains ownership and verifies the advice.

## Confirm that consultation is justified

Gather source, test, command, and documentation evidence first. Ask the human when the unknown concerns intent, priorities, acceptance criteria, private context, risk tolerance, authority, or approval. Use `request_user_input` when it is available and follow the global question policy. Consult only when material technical judgement remains. Do not give the advisor implementation ownership.

## Choose the least expensive sufficient tier

- **Terra high:** Focused check, compact evidence, few constraints, low ambiguity, and limited consequences.
- **Terra xhigh:** Evidence-rich question across several paths that needs careful synthesis but little novel inference.
- **Terra max:** Difficult, bounded, lower-risk question with mostly complete evidence where exhaustive checking should resolve it once.
- **Sol medium:** Default for ambiguous or high-leverage design, diagnosis, or completion review where inference and trade-offs are difficult.
- **Sol high:** Several plausible explanations, subtle interactions, or material security, concurrency, data-integrity, public-API, compatibility, migration, or irreversible-state risk.
- **Sol xhigh:** Many interacting constraints, incomplete or contradictory evidence, or a lower-tier call that left the central uncertainty unresolved.
- **Sol max:** Exceptional difficulty and cost of error, or conflicting evidence that defeated a lower tier.

Breadth favours Terra. Ambiguity, novel inference, and high consequences favour Sol. Do not use Luna, `low`, Terra `medium`, Sol `low`, or `ultra`. Skip consultation when those depths would suffice. Avoid a tier likely to cause a retry.

## Prepare the decision packet

Send a compact **Decision packet** with:

1. Objective.
2. Constraints.
3. Evidence gathered.
4. Relevant files and symbols.
5. Current hypothesis.
6. Options considered.
7. Unresolved uncertainty.
8. One precise question.

Tell the advisor to inspect cited paths first and expand only when necessary. Do not transfer the full transcript.

## Invoke and wait

Spawn the custom `advisor` with `fork_turns="none"`. Set both `model` and `reasoning_effort` explicitly from the chosen tier. Use one advisor at a time.

Wait until the advisor reaches a terminal state and returns its advice. Poll at reasonable intervals. Do not cancel it because it is slow or temporarily produces no output. Do not implement in parallel. Interrupt it only when the human changes direction or it reports an unrecoverable failure.

Treat a live child as active regardless of elapsed time or silence. Continue to poll it and give the human concise progress updates. Do not silently abandon it. Treat the consultation as stalled only when the tool reports that the child no longer exists, cannot be reached, or ended with an infrastructure failure. In that case, do not change the model or effort. Ask the human whether to retry the same tier or continue without advice.

If the spawn cannot apply both overrides, do not fall back to the global subagent model. Use `request_user_input` to ask whether advice is required to proceed when the tool is available, or continue without consultation only when safe.

Use no more than two consultations during a normal task: one decision review and one completion challenge. Use a third only when new evidence changes the problem fundamentally.

## Apply the advice

Treat the result as advice. Verify repository-specific claims against source, tests, commands, or documentation. Evidence overrides advisor preference. Extract supported corrections and continue from existing progress. Do not restart work merely because the advisor prefers another style.
