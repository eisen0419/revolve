# Revolve Conversation Sync

Convert AI conversation files from multiple providers into Obsidian Markdown notes.

## Prerequisites

- Python 3.8+ (macOS system Python works)
- Revolve config at `~/.config/revolve/config.md` (run `/revolve-setup` to generate)
- An Obsidian vault with write access

## Usage

### One-shot sync

```bash
# Sync all configured providers
python3 scripts/sync_conversations.py --verbose

# Sync a single provider
python3 scripts/sync_conversations.py --provider claude --verbose
```

### Automatic sync (launchd)

```bash
# 1. Review and customize the plist (update script path if needed)
vim scripts/com.revolve.sync.plist

# 2. Install the launch agent
cp scripts/com.revolve.sync.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.revolve.sync.plist

# 3. Check logs
tail -f ~/.config/revolve/sync.log
```

The agent runs every 5 minutes and on login.

To uninstall:

```bash
launchctl unload ~/Library/LaunchAgents/com.revolve.sync.plist
rm ~/Library/LaunchAgents/com.revolve.sync.plist
```

## Provider Support

| Provider | Source | Content | Notes |
|----------|--------|---------|-------|
| **Claude** | `~/.claude/projects/**/*.jsonl` | Full conversations (user + assistant + tool use) | Extracts base64 images from tool results |
| **Codex** | `~/.codex/sessions/**/*.jsonl` | Full conversations (`response_item`, `event_msg` events) | |
| **OpenCode** | `~/.local/state/opencode/prompt-history.jsonl` | User prompts only | Tagged `sync_mode: prompt-only` in frontmatter |
| **Gemini** | `~/.gemini/tmp/**/chats/session-*.json` | Full conversations | Excludes non-chat JSON (oauth, settings) |

## Output

Notes are written to `<vault_path>/AI Conversations/<provider>/` with:

- YAML frontmatter (date, provider, model, tags)
- Clean Markdown with `## User` / `## Assistant` sections
- Extracted images embedded via `![[filename]]` syntax
- System prompts and skill injections folded or skipped

## Configuration

Edit `~/.config/revolve/config.md`:

```yaml
---
vault_path: /path/to/your/Obsidian/Vault
sync_providers: claude,codex,opencode,gemini
---
```

Set `sync_providers` to a comma-separated subset to limit which providers are synced.

## Idempotency

Sync state is tracked in `~/.config/revolve/.sync_state.json` (file path + mtime). Re-running the script only processes new or modified conversations. Delete the state file to force a full re-sync.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `Config not found` | Run `/revolve-setup` or copy `config.md.example` to `~/.config/revolve/config.md` |
| No conversations synced | Check `sync_providers` in config; run with `--verbose` |
| Corrupt JSONL errors | Corrupt lines are skipped automatically; check `--verbose` output |
| Launchd not running | `launchctl list | grep revolve` to check status; review `sync.log` |
| Images missing | Verify `attachments/ai-conversations/` exists in vault; check file permissions |
| Disk full | Script attempts to write notes without images as fallback |
