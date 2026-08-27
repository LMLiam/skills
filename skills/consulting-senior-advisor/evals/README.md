# Evaluation Guide

Use `evals.json` to test activation and workflow behaviour.

## Trigger Evaluation

Run each prompt in a fresh session with the skill installed. Run each prompt three times. Record whether the harness loaded the skill.

For `should_trigger: true`, a passing result loads the skill. For `should_trigger: false`, a passing result does not load the skill.

Do not change the skill from the validation prompts. Use those prompts only after a change selected from the training set has passed.

## Workflow Evaluation

Install one adapter and provider profile. Run each positive case in a fresh session. Compare the output against its assertions.

Run the same task without the skill or with the previous released version. Record output quality, duration, and token use. A skill must improve a durable workflow behaviour enough to justify its cost.

## Safety Evaluation

For each OpenCode profile, verify that an advisor can inspect a repository but cannot edit, write, invoke a nested task, or run a shell command. The repository validator checks the configuration. A harness run checks its actual enforcement.
