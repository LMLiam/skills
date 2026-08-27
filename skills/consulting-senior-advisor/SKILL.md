---
name: consulting-senior-advisor
description: Use for one advice-only consultation when evidence leaves a consequential technical decision unresolved, including ambiguous architecture, diagnosis, concurrency, security, data integrity, compatibility, migration, public API, or completion review. Do not use for routine work or human-owned product and priority decisions.
license: MIT
compatibility: Requires a configured integration with named advisor agents.
metadata:
  author: LMLiam
  version: "1.0.0"
---

# Consulting Senior Advisor

Resolve one precise technical uncertainty through a sequential, advice-only consultation. Retain execution ownership and verify the advice.

## Route The Uncertainty

1. Gather enough source, test, command, trace, and documentation evidence to identify the unresolved uncertainty.
2. If the uncertainty concerns intent, priorities, acceptance criteria, private context, risk tolerance, authority, or approval, ask the human. Do not ask an advisor to guess human-owned information.
3. If available evidence resolves the uncertainty, proceed without consultation.
4. Do not consult for routine edits, documentation corrections, simple lookups, or obvious tool failures.
5. Consult only when consequential technical judgement remains unresolved.

## Configure The Consultation

Read [the active integration](references/active-integration.md) only after consultation is justified. If the reference is unavailable, report that consultation is not configured. Do not use a primary agent, global agent, or inheriting fallback.

Select the least expensive sufficient tier from the active integration:

- Select a focused tier for a compact evidence check with limited ambiguity and consequences.
- Select a review tier for an ambiguous or high-leverage design, diagnosis, or completion decision.
- Select a challenge tier for conflicting evidence, several interacting constraints, or material security, concurrency, data-integrity, compatibility, migration, public-API, or irreversible-state risk.

Use the exact advisor named by the active integration. Do not infer equivalence between providers. Do not discover, rank, or select models at runtime.

## Prepare the Decision Packet

Build a compact prompt with [the decision-packet template](references/decision-packet.md). Give the advisor one precise question.

Tell the advisor to inspect cited paths first and expand only when necessary. Do not transfer the full transcript. Do not include secrets.

## Invoke And Wait

1. Follow the active integration invocation contract.
2. Invoke exactly one configured advisor. Give it advice ownership, not implementation ownership.
3. Wait for a terminal result. Do not implement the disputed decision in parallel.
4. If the advisor, model, or variant is unavailable, do not substitute another one. Ask whether to retry the same tier or continue without advice when that choice is material.

Use no more than two consultations in a normal task: one decision review and one completion challenge. Use a third only when new evidence changes the problem fundamentally.

## Evaluate The Advice

1. Treat the result as advice, not authority.
2. Verify repository-specific claims against source, tests, commands, traces, or documentation.
3. Follow verified evidence when it conflicts with advisor preference.
4. Extract supported corrections and continue from existing progress.

Do not restart work merely because the advisor prefers another style. If advice conflicts with a human decision or repository rule, follow the higher-authority constraint and report the conflict.
