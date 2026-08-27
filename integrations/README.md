# Integration Contract

This document is for integration maintainers. It is not part of the agent runtime instructions.

An integration makes the portable consultation workflow operational in one harness. Each integration must define:

1. The exact invocation method for one advisor.
2. The configured advisor names and model-selection policy.
3. The advisor tool permissions.
4. The response contract.
5. The handling for an unavailable agent, model, or variant.
6. The installation and validation steps.

An integration must not make the executor discover or rank available models. It must use an explicit provider profile or an explicit per-consultation configuration.

An advice-only advisor must not edit files, execute state-changing commands, or delegate work. A prompt instruction alone is not a capability boundary. Where the harness supports permissions, the integration must deny those capabilities explicitly.

The advisor response must contain:

1. Recommendation.
2. Why this is the best option.
3. Assumptions that must be verified.
4. Main failure modes and edge cases.
5. Relevant files, symbols, or execution paths.
6. Concrete validation criteria.
7. Whether the executor should proceed, investigate further, or change course.
