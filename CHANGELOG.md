# Changelog

All notable changes to this repository are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Releases use semantic versioning.

## Unreleased

### Changed

- The Claude Code `implementer` defaults to Haiku at medium effort, with standing rules for Haiku: edit rather than suggest, read before editing, stay in scope, no hard-coding for tests, verify with a real run, stop and report when a step is impossible.
- The Claude Code `reviewer` runs at medium effort, stays within the diff and the brief, lists out-of-scope ideas under Suggestions, and starts no extra review rounds or subagents.
- The `implementer` no longer stops shared build daemons unless the brief says to.

### Added

- Added per-model briefing guidance for Haiku, Sonnet and the Opus advisor to the Claude Code integration, based on Anthropic's prompting guides.

## [0.2.0] - 2026-11-13

### Added

- Added Claude Code integration with `scout`, `verifier`, `implementer`, and `reviewer` subagents and an orchestration guide.

## [0.1.0] - 2026-08-28

### Changed

- Restructured `consulting-senior-advisor` as a standard Agent Skill with an OpenCode integration.
- Added an explicit OpenCode GPT-5.6 provider profile with capability-restricted advisor agents.
- Separated agent runtime instructions from human installation and integration-maintainer documentation.

### Added

- Added `opencode-gpt-5.6` provider profile mirroring `openai-gpt-5.6` via OpenCode Zen (`opencode/gpt-5.6-*`) so no ChatGPT Plus/Pro OAuth is required.
- Added `opencode-claude-5` provider profile using Claude Sonnet 5, Opus 5, and Fable 5 via OpenCode Zen (`opencode/claude-*-5`) so no ChatGPT Plus/Pro or Anthropic subscription is required.
- Added `opencode-gemini-3` provider profile using Gemini 3.7 Flash and 3.1 Pro via OpenCode Zen (`opencode/gemini-*`) so no ChatGPT Plus/Pro, Anthropic, or Google subscription is required.
- Added `opencode-mixed` provider profile: a flat, index-ordered ladder of twelve advisor tiers spanning model families (GPT-5.6, Gemini, Claude, Grok) via OpenCode Zen, ordered by the Artificial Analysis Intelligence Index with price as the tiebreak.
- Added evaluation cases and repository validation for the portable core and integrations.
