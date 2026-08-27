# OpenCode Provider Profile Template

Copy this directory into `integrations/opencode/profiles/<profile-name>/`. Replace every placeholder in `profile.json`. Add one Markdown agent file for each `agents` entry.

Copy a reviewed advisor agent file from `profiles/openai-gpt-5.6/agents/`. Keep the default-deny permission policy. Change only the model, variant, description, and any provider-specific selection guidance that the profile can support with evidence.

Do not add a profile to the supported `profiles/` directory until it passes repository validation, installation validation, capability probes, and behavioural evaluations.
