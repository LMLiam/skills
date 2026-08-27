# Changelog

All notable changes to this repository are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Releases use semantic versioning.

## Unreleased

### Changed

- Restructured `consulting-senior-advisor` as a standard Agent Skill with an OpenCode integration.
- Added an explicit OpenCode GPT-5.6 provider profile with capability-restricted advisor agents.
- Separated agent runtime instructions from human installation and integration-maintainer documentation.

### Added

- Added `opencode-gpt-5.6` provider profile mirroring `openai-gpt-5.6` via OpenCode Zen (`opencode/gpt-5.6-*`) so no ChatGPT Plus/Pro OAuth is required.
- Added evaluation cases and repository validation for the portable core and integrations.
