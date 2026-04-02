# Revolve

**Self-Evolving AI Research Architecture for Claude Code**

Each research session feeds back into your AI — making the next session smarter.

---

## How It Works

```
Collect              Analyze            Store             Evolve
────────────         ──────────         ───────           ──────────────
YouTube / Web   →    NotebookLM    →    Obsidian    →    CLAUDE.md    →  Better AI
PDF / Text           (free Google AI)   (your vault)     (append-only)    │
                                                                           └── loop
```

---

## Prerequisites

| Dependency | Required | Install |
|------------|----------|---------|
| [Claude Code](https://claude.ai/code) | yes | — |
| [Obsidian](https://obsidian.md) vault | yes | — |
| NotebookLM MCP server | yes | `pipx install notebooklm-mcp-cli` then `nlm login` |
| yt-dlp | yes (for YouTube) | `brew install yt-dlp` or `pip install yt-dlp` |
| defuddle | optional | `npm install -g @eisen0419/defuddle` |
| Python 3.8+ | yes (sync script) | pre-installed on macOS |
| fswatch | optional (auto-sync) | `brew install fswatch` |

---

## Installation

Until Revolve is available in the official marketplace, install directly:

```bash
claude plugin marketplace add https://github.com/eisen0419/revolve
claude plugin install revolve
```

---

## Quick Start

```bash
# 1. Configure vault path and check dependencies
/revolve-setup

# 2. Search YouTube for relevant content
/yt-search "Claude Code tips"

# 3. Run the full research pipeline
/research-pipeline youtube "AI productivity"

# 4. Evolve CLAUDE.md from accumulated experience
/evolve-claude-md
```

**Time estimates:** under 10 minutes if prerequisites are already installed; under 60 minutes from scratch.

---

## Skills Reference

| Skill | Description | Example |
|-------|-------------|---------|
| `/revolve-setup` | Interactive wizard — configure vault, check dependencies | `/revolve-setup` |
| `/yt-search` | Search YouTube via yt-dlp, return structured results | `/yt-search "Claude Code skills"` |
| `/research-pipeline` | Full pipeline: collect → NotebookLM analysis → Obsidian note | `/research-pipeline youtube "AI agents"` |
| `/evolve-claude-md` | Scan conversations and vault notes, append findings to CLAUDE.md | `/evolve-claude-md --days 7` |

---

## Sync Script

Converts AI conversation files (Claude, Codex, OpenCode, Gemini) into Obsidian Markdown notes. Supports one-shot sync and automatic sync via launchd.

See [`scripts/README.md`](scripts/README.md) for full usage.

---

## Templates

Copy the Obsidian templates from `templates/` to your vault's template folder:

- `research-note.md` — structured note for research pipeline output
- `research-index.md` — dataview index across all research notes

---

## Configuration

Copy `config.md.example` to `~/.config/revolve/config.md` and set your vault path, or run `/revolve-setup` to generate it automatically.

Field reference and schema: [`docs/config-contract.md`](docs/config-contract.md).

---

## Demo

Coming soon — video walkthrough of the complete flywheel.

---

## License

MIT
