# Revolve Configuration Contract

This document defines the configuration field schema for `~/.config/revolve/config.md`. All Revolve skills and the sync script must follow this contract.

## Config File Location

```
~/.config/revolve/config.md
```

Created by `/revolve-setup`. Template at `config.md.example` in the repo root.

## Format

Markdown file with YAML frontmatter. All values are simple unquoted strings — no YAML quoting, no multi-line values, no list syntax. This enables reliable regex parsing by the sync script (which has no pyyaml dependency).

## Field Schema

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `vault_path` | string (absolute path) | Absolute path to Obsidian vault root |
| `output_dir` | string (relative path) | Relative path within vault for research notes. Must be under `vault_path` |

### Optional Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `screenshots_dir` | string (relative path) | `attachments/screenshots` | Relative path within vault for screenshot attachments |
| `sync_providers` | string (comma-separated) | `claude,codex,opencode,gemini` | Comma-separated list of enabled providers: `claude`, `gemini`, `chatgpt`, `codex` |
| `default_language` | string | `en` | Output language for generated content: `en` or `cn` |
| `notebooklm_enabled` | bool | `true` | Enable automatic NotebookLM import for research notes |

## Consumers

| Field | Consumers |
|-------|-----------|
| `vault_path` | all skills, sync script |
| `output_dir` | research-pipeline, evolve-claude-md |
| `screenshots_dir` | research-pipeline |
| `sync_providers` | sync script |
| `default_language` | research-pipeline, research-note template |
| `notebooklm_enabled` | research-pipeline |

## Constraints

- `output_dir` must be a subdirectory of `vault_path` (evolve-claude-md scans `vault_path`, research-pipeline writes to `output_dir` — containment relationship required)
- `/revolve-setup` validates this constraint when writing config
- Field names are exact — no aliases (e.g., `vault_path` not `obsidian_vault`)

## Reading Convention

**Skills (inside Claude Code):** Read at execution time via `Read ~/.config/revolve/config.md`. Parse frontmatter values from the YAML block between `---` markers. No Claude Code restart needed after config changes.

**Sync script (Python):** Parse with regex — split lines on first `: `, strip whitespace. For `sync_providers`, split on `,` to get a list.

## Skill Responsibilities

- Every skill MUST check for `~/.config/revolve/config.md` existence at startup
- If config.md is missing, skills MUST prompt user to run `/revolve-setup`
- Skills MUST NOT hardcode any user-specific paths

## Missing Config Behavior

If `~/.config/revolve/config.md` does not exist:
- Skills: display a clear message suggesting the user run `/revolve-setup`
- Sync script: exit with error code 1 and message pointing to setup instructions
