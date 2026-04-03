---
name: revolve-setup
description: "This skill should be used when the user asks to 'set up Revolve', 'configure Revolve', or 'run revolve setup'. Interactive wizard that detects Obsidian vault, checks dependencies, and writes config.md."
argument-hint: (no arguments)
---

# /revolve-setup

Interactive environment detection and configuration wizard for Revolve.

## Trigger

User runs `/revolve-setup` or asks to set up / configure Revolve.

## Instructions

### Step 1: Welcome

Greet the user and explain what this wizard does:

```
Welcome to Revolve Setup!

This wizard will:
  1. Detect your environment (Obsidian vault, Python, system tools)
  2. Collect required paths
  3. Generate config.md

Let's get started.
```

### Step 2: Dependency Check

Check the following dependencies and report status:

```bash
python3 --version 2>/dev/null && echo "PYTHON_OK" || echo "PYTHON_MISSING"
which fswatch 2>/dev/null && echo "FSWATCH_OK" || echo "FSWATCH_MISSING"
which yt-dlp 2>/dev/null && echo "YTDLP_OK" || echo "YTDLP_MISSING"
```

Show a summary table:

```
Dependency Check:
  ✅ Python 3.x.x   OK
  ❌ fswatch        MISSING — Install via: brew install fswatch
  ✅ yt-dlp         OK
```

Installation hints for missing deps:

- **Python 3.8+**: Install from https://python.org (or `brew install python`)
- **fswatch**: `brew install fswatch`
- **yt-dlp**: `pip install yt-dlp` or `brew install yt-dlp`

Non-fatal: warn about missing deps but continue. Do NOT abort.

### Step 3: Detect Obsidian Vault

Search common locations for Obsidian vault by looking for directories containing `.obsidian/`:

```bash
find ~/Documents -maxdepth 3 -name ".obsidian" -type d 2>/dev/null | sed 's|/.obsidian$||'
find ~/Desktop -maxdepth 2 -name ".obsidian" -type d 2>/dev/null | sed 's|/.obsidian$||'
find ~ -maxdepth 2 -name ".obsidian" -type d 2>/dev/null | sed 's|/.obsidian$||'
```

Deduplicate results, then:

- If **1 vault** found: via AskUserQuestion, confirm with user:
  > Detected Obsidian vault: `<path>`. Use this path? (press Enter to confirm, or type a new path)

- If **multiple vaults** found: via AskUserQuestion, present numbered options:
  > Detected Obsidian vaults:
  > 1. `/path/a`
  > 2. `/path/b`
  > Enter number or type a custom path:

- If **no vault** found: via AskUserQuestion, ask for manual entry:
  > No Obsidian vault detected. Please enter your vault path:

Store final path as `VAULT_PATH`.

### Step 4: Collect Paths

Ask the user (via AskUserQuestion) for:

1. **vault_path** — already confirmed in Step 3, display for final confirmation.

2. **output_dir** — Ask:
   > Output directory for research notes (relative to vault root):
   > Default: `Research` — press Enter to accept.

   Validate: must not start with `/` and must not contain `..`. Re-ask if invalid.
   Store as `OUTPUT_DIR` (default: `Research`).

3. **screenshots_dir** — Ask:
   > Screenshots directory (relative to vault root):
   > Default: `<OUTPUT_DIR>/screenshots` — press Enter to accept.

   Store as `SCREENSHOTS_DIR`.

### Step 5: Select Sync Providers

Via AskUserQuestion, present supported providers and ask which to enable:

```
Which providers would you like to sync conversations from?
(Enter comma-separated list, or press Enter for all)

  [ ] claude
  [ ] gemini
  [ ] chatgpt
  [ ] codex

Default: claude,gemini,chatgpt,codex
```

Store selection as `SYNC_PROVIDERS` (comma-separated, e.g. `claude,codex`).

### Step 6: Write config.md

First, check if config.md already exists at the plugin root:

```bash
[ -f "config.md" ] && echo "EXISTS" || echo "NOT_FOUND"
```

- If **exists**: via AskUserQuestion, ask:
  > `config.md` already exists. Overwrite? (y/n)
  - If user answers `n`: print `Setup cancelled. Existing config preserved.` and stop.
  - If user answers `y`: proceed to write.

- If **not found**: proceed to write.

Write `config.md` using the template from `config.md.example` with user-provided values:

```
---
vault_path: <VAULT_PATH>
output_dir: <OUTPUT_DIR>
screenshots_dir: <SCREENSHOTS_DIR>
sync_providers: <SYNC_PROVIDERS>
---

# Revolve Configuration

This file is the configuration for the Revolve plugin. Copy it to `~/.config/revolve/config.md` and update the values.

Quick setup: run `/revolve-setup` to generate this file automatically.

## Field Reference

- **vault_path** (required): Absolute path to your Obsidian vault root
- **output_dir** (required): Relative path within vault for research notes (must be under vault_path)
- **screenshots_dir** (optional): Relative path within vault for screenshot attachments
- **sync_providers** (optional): Comma-separated list of providers to sync. Options: claude, codex, opencode, gemini. Default: all

## Format Rules

- All values are simple unquoted strings (no YAML quoting)
- Lists use comma-separated format (e.g., `claude,codex,gemini`)
- Paths with spaces are fine — parser splits on first `: ` only
- Do not use multi-line values
```

Also create the config directory and copy to the canonical location:

```bash
mkdir -p ~/.config/revolve/
cp config.md ~/.config/revolve/config.md
```

### Step 7: Confirm & Next Steps

Show a summary of the written config:

```
Setup complete!

Config written to:
  ./config.md
  ~/.config/revolve/config.md

Configuration summary:
  vault_path:      <VAULT_PATH>
  output_dir:      <OUTPUT_DIR>
  screenshots_dir: <SCREENSHOTS_DIR>
  sync_providers:  <SYNC_PROVIDERS>

Next steps:
  1. Run /research-pipeline to start a research session
  2. Run /evolve-claude-md to evolve your CLAUDE.md
  3. Run /yt-search to search YouTube videos
```

If any deps were missing in Step 2, append:

```
Note: <N> dependencies are not installed. See the warnings above for installation instructions.
```
