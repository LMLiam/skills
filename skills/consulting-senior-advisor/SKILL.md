---
name: consulting-senior-advisor
description: Use when a difficult architecture, diagnosis, concurrency, security, data integrity, compatibility, migration, public API, or completion-review decision remains unresolved after evidence gathering and needs stronger technical judgement.
license: MIT
compatibility: Requires a configured integration with named advisor agents.
metadata:
  author: LMLiam
  version: "1.0.0"
---

# Consulting Senior Advisor

Use one sequential, advice-only advisor consultation for a precise technical decision. The executor retains ownership and verifies all advice.

This skill does not select a model. Install an explicit integration before use. The active integration owns model selection, tools, permissions, invocation, and failure handling.

## Confirm Consultation Is Justified

Gather source, test, command, and documentation evidence first. Ask the human when the unknown concerns intent, priorities, acceptance criteria, private context, risk tolerance, authority, or approval. Consult only when material technical judgement remains. Do not give the advisor implementation ownership.

Do not consult for routine edits, documentation corrections, simple lookups, obvious tool failures, or questions that available evidence already resolves.

## Select a Consultation Tier

Read [the active integration](references/active-integration.md) before you select an advisor. If it is unavailable, stop and ask the human to install an integration.

Use the least expensive sufficient tier from the active provider profile.

- Select a focused tier for a compact evidence check with limited ambiguity and consequences.
- Select a review tier for an ambiguous or high-leverage design, diagnosis, or completion decision.
- Select a challenge tier for conflicting evidence, several interacting constraints, or material security, concurrency, data-integrity, compatibility, migration, public-API, or irreversible-state risk.

The active integration maps each category to an exact named advisor. Follow that mapping. Do not infer equivalence between providers. Do not discover, rank, or select models at runtime.

## Prepare the Decision Packet

Send a compact decision packet. Use [the packet template](references/decision-packet.md).

Tell the advisor to inspect cited paths first and expand only when necessary. Do not transfer the full transcript. Do not include secrets.

## Invoke and Wait

Follow the active integration invocation contract. Invoke exactly one configured advisor. Do not use a primary-agent, global-agent, or inheriting fallback. Do not implement the disputed decision while the consultation is active.

Wait for a terminal result. Do not cancel a consultation because it is slow or temporarily silent. If the integration reports a failure or an unavailable configured advisor, do not change the model or tier automatically. Ask the human whether to retry the same tier or continue without advice when that decision is material.

Use no more than two consultations in a normal task: one decision review and one completion challenge. Use a third only when new evidence changes the problem fundamentally.

## Apply the Advice

Treat the result as advice. Verify repository-specific claims against source, tests, commands, or documentation. Evidence overrides advisor preference. Extract supported corrections and continue from existing progress.

Do not restart work merely because the advisor prefers another style. If advice conflicts with a human decision or repository rule, follow the higher-authority constraint and report the conflict.
