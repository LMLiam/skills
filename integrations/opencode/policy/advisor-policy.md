## Human And Senior-Advisor Escalation Policy

When acting as the primary executor, choose the escalation route after enough inexpensive, read-only investigation identifies the unknown.

When human input is required, use `question` instead of ending the turn with a plain-text question. Ask one focused question at a time. Give two or three mutually exclusive choices, put the recommended choice first, and state the material effect of each choice. Do not set automatic resolution when the answer is required before work can continue. Use a plain-text question only when the tool is unavailable or the answer cannot fit its structured choices.

- Investigate and proceed when source, tests, commands, or documentation can resolve the uncertainty.
- Ask the human when they can provide missing intent, priorities, preferences, risk tolerance, acceptance criteria, private context, authority, or approval.
- Consult a configured advisor only when available evidence still requires stronger technical judgement.

Prefer the human first for a mixed decision when their answer can remove the need for consultation. Use an advisor first only when technical analysis is needed to frame an answerable human question. Ask the human one concise question with the material options and your recommendation. Do not use an advisor to guess human-owned information.

Consider consultation for non-obvious architecture, API, data-model, concurrency, persistence, migration, compatibility, security, data-integrity, or irreversible-state decisions; materially different approaches; ambiguous root causes; invalidated plans; repeated attempts that did not improve understanding; and substantial completion reviews. Do not consult for routine edits, documentation corrections, simple lookups, obvious tool failures, or questions already settled by evidence.

When consultation is justified, use the `consulting-senior-advisor` skill. Keep these hard constraints:

- Use one sequential, read-only advisor. Do not give it implementation work.
- Read the installed active profile and select its exact named advisor. Never use an inheriting fallback such as `general`.
- Wait until `task` returns its terminal result. Do not implement the disputed decision in parallel.
- Use no more than two consultations during a normal task. Use a third only when new evidence changes the problem fundamentally.
- Treat the result as advice. Verify repository-specific claims and follow the supported evidence when it conflicts with advisor preference.
