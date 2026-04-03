<div align="center" id="readme-top">

![Revolve Banner][banner]

[![License][license-badge]][license]
[![Claude Code][claude-badge]][claude-code]
[![Plugin][plugin-badge]][install-url]

**Self-Evolving AI Research Architecture for Claude Code**

Research any topic through YouTube, web articles, PDFs, or raw text. NotebookLM analyzes the sources for free. Results land in your Obsidian vault as structured notes. Over time, Revolve scans your accumulated research and conversations to evolve CLAUDE.md -- so your AI gets smarter with every session.

[Quick Start][quick-start] •
[Skills Reference][skills-ref] •
[Sync Script][sync-section] •
[Configuration][config-section]

Sister project: **[Forge][forge-repo]** -- CLAUDE.md workflow starter kit

[![English][lang-en-badge]][lang-en]
[![简体中文][lang-zh-badge]][lang-zh]

</div>

<br>

<details open>
<summary><kbd>Table of Contents</kbd></summary>

- [How It Works][how-it-works]
- [What You Get][what-you-get]
- [Prerequisites][prerequisites]
- [Installation][installation]
- [Quick Start][quick-start]
- [Skills Reference][skills-ref]
- [Sync Script][sync-section]
- [Templates][templates-section]
- [Configuration][config-section]
- [Built With][built-with]
- [Acknowledgments][acknowledgments]
- [Contributing][contributing]
- [License][license-section]

</details>

<br>

## How It Works

![Flywheel Diagram][flywheel-diagram]

```
Collect              Analyze            Store             Evolve
────────────         ──────────         ───────           ──────────────
YouTube / Web   →    NotebookLM    →    Obsidian    →    CLAUDE.md    →  Better AI
PDF / Text           (free Google AI)   (your vault)     (append-only)    └── loop
```

Each research session feeds back into your AI -- making the next session smarter. Here is a concrete walkthrough:

Say you want to research "AI agent architectures". Here is what happens:

1. **Collect** -- `/research-pipeline youtube "AI agent architectures"` searches YouTube via yt-dlp. You see a ranked table of results and pick the 3 most relevant videos.
2. **Analyze** -- Revolve sends the selected videos to NotebookLM, which processes them and produces structured analysis: key concepts, comparisons across sources, and practical takeaways. This runs on Google's infrastructure, not your Claude tokens.
3. **Store** -- Results are written as a formatted Obsidian note with YAML frontmatter, tags, source links, and a full analysis section -- ready for your knowledge base.
4. **Evolve** -- `/evolve-claude-md` scans your recent research notes and raw conversation logs (.jsonl), extracts patterns like "user prefers agent-first architecture" or "NotebookLM auth expires weekly -- run `nlm login` to fix", and appends them to CLAUDE.md.

Next time you ask Claude about architecture, it already knows your preferences and past research. The flywheel closes automatically.

<div align="right">

[![][back-to-top]][readme-top]

</div>

## What You Get

Each research session produces an Obsidian note like this:

```markdown
---
date: 2026-04-02
topic: AI Agent Architectures
source_type: youtube
notebook_id: nbl_a7x9k2m
tags:
  - research
  - ai-agents
  - architecture
status: complete
---

# AI Agent Architectures

> Sources: 3 YouTube videos | Analysis engine: NotebookLM

## Summary

Multi-agent systems outperform single-agent setups for complex tasks.
The key tradeoff is between orchestrator control and agent autonomy...

## Key Findings

- ReAct-style agents work best for tool-heavy tasks with clear APIs
- Hierarchical delegation (planner → executor → reviewer) reduces error
  propagation by 40% compared to flat agent pools
- Memory systems (vector DB + structured logs) are more important than
  model choice for long-running agent workflows

## Analysis

### Agent Communication Patterns
...

## Sources

- "Building Multi-Agent Systems" by AI Engineering (12:34)
- "ReAct vs Plan-and-Execute" by Tech Frontiers (18:02)
- "Production Agent Architectures" by ML Ops Community (24:15)

## Links

- NotebookLM notebook: https://notebooklm.google.com/notebook/nbl_a7x9k2m
```

Over time, `/evolve-claude-md` appends findings like these to your CLAUDE.md:

```markdown
# Evolution Log

## 2026-04-02 Evolution

Based on 328 sessions (.jsonl) + 94 notes analyzed over 7 days.

New findings:
- [Tool Pattern] yt-dlp search with `--flat-playlist --dump-json` is the most reliable method
- [Error Recovery] NotebookLM auth expires weekly -- `nlm login` restores it instantly
- [User Correction] Never auto-commit without explicit user confirmation
- [Work Preference] User prefers table comparisons over prose for architecture decisions
- [New Knowledge] Hierarchical agent delegation reduces error propagation significantly
```

<div align="right">

[![][back-to-top]][readme-top]

</div>

## Prerequisites

| Dependency | Required | Install |
|------------|----------|---------|
| [Claude Code][claude-code] | Yes | -- |
| [Obsidian][obsidian] vault | Yes | -- |
| NotebookLM MCP server | Yes | See [NotebookLM MCP Setup][nlm-setup] below |
| yt-dlp | Yes (YouTube) | `brew install yt-dlp` or `pip install yt-dlp` |
| defuddle | Optional | `npm install -g defuddle-cli` |
| Python 3.8+ | Yes (sync script) | Pre-installed on macOS |
| fswatch | Optional (auto-sync) | `brew install fswatch` |

<div align="right">

[![][back-to-top]][readme-top]

</div>

## Installation

```bash
claude plugin marketplace add https://github.com/eisen0419/revolve
claude plugin install revolve
```

### NotebookLM MCP Setup (Required)

NotebookLM is the analysis engine that powers the research pipeline. Setting it up takes about 5 minutes:

```bash
# 1. Install the NotebookLM CLI
npm install -g notebooklm-mcp

# 2. Authenticate with your Google account (opens browser for OAuth)
nlm login

# 3. Verify the connection works
nlm notebook_list
```

Step 3 should return a JSON list of your notebooks (empty list `[]` is fine for new accounts). If you get an authentication error, re-run `nlm login`.

Then add the MCP server to Claude Code so skills can call NotebookLM programmatically:

```bash
claude mcp add notebooklm-mcp
```

<div align="right">

[![][back-to-top]][readme-top]

</div>

## Demo

> Coming soon — a video walkthrough showing the full research-to-evolution flywheel in action.

## Quick Start

**Step 1: Configure vault path and check dependencies**

```
> /revolve-setup

Detected Obsidian vault: /Users/you/Documents/Obsidian Vault
Use this path? (Enter to confirm, or type a different path)
> [Enter]

Research notes output directory (relative to vault, default: Research):
> [Enter]

Dependency check:
  yt-dlp       installed
  python3      installed
  defuddle     not installed (optional -- web mode will fall back to NotebookLM direct fetch)
  NotebookLM   connected

Config written to ~/.config/revolve/config.md
```

**Step 2: Search YouTube**

```
> /yt-search "Claude Code productivity"

| # | Title                                   | Channel          | Duration | Views   | URL                                    |
|---|-----------------------------------------|------------------|----------|---------|----------------------------------------|
| 1 | Claude Code: 10x Your Workflow          | AI Explained     | 12:34    | 45,000  | https://youtube.com/watch?v=abc123     |
| 2 | Building Claude Code Plugins from Scratch| Tech Weekly      | 08:21    | 23,000  | https://youtube.com/watch?v=def456     |
| 3 | Advanced Claude Code Skills Nobody Uses  | Dev Mastery      | 15:47    | 67,000  | https://youtube.com/watch?v=ghi789     |
| 4 | Claude Code vs Cursor: Honest Comparison | Code Review      | 20:12    | 112,000 | https://youtube.com/watch?v=jkl012     |
| 5 | My Claude Code Setup for Research        | Knowledge Worker | 09:55    | 18,000  | https://youtube.com/watch?v=mno345     |
```

**Step 3: Run the full research pipeline**

```
> /research-pipeline youtube "AI productivity"

Searching YouTube for "AI productivity"...
[results table shown, you pick videos 1 and 3]

Creating NotebookLM notebook: "Research: AI Productivity - 2026-04-02"
Adding 2 video sources...
Analyzing with NotebookLM (quick mode)...

Research complete! Results saved to:
   /Users/you/Documents/Obsidian Vault/Research/2026-04-02 AI Productivity.md

Tip: Run /evolve-claude-md to update CLAUDE.md from your recent research.
```

**Step 4: Evolve CLAUDE.md from accumulated experience**

```
> /evolve-claude-md

Scanning evolution layer: 42 sessions (.jsonl) from last 7 days
Scanning reading layer: 12 notes (.md) from vault

New findings (5):
- [Error Recovery] Read large files with offset+limit to avoid token overflow
- [Tool Pattern] ssh used 499 times -- dual-machine workflow is core pattern
- [User Correction] Design tasks must not modify content text -- separate content from styling
- [Skill Usage] /research-pipeline followed by /evolve-claude-md is the standard loop
- [Work Preference] User prefers concise Chinese with mixed English technical terms

Append these to CLAUDE.md? (confirm / edit / cancel)
> confirm

CLAUDE.md evolution complete! 5 findings appended.
```

Under 10 minutes if prerequisites are installed. Under 60 minutes from scratch.

<div align="right">

[![][back-to-top]][readme-top]

</div>

## Skills Reference

### `/revolve-setup`

Interactive configuration wizard. Detects your Obsidian vault location, checks all dependencies (yt-dlp, defuddle, python3, fswatch, NotebookLM MCP), and writes `~/.config/revolve/config.md`. Run this once before using any other skill.

```
/revolve-setup
```

No arguments. The wizard walks you through each step interactively.

---

### `/yt-search`

Search YouTube via yt-dlp and return a structured results table. Does not download videos -- only retrieves metadata (title, channel, duration, view count, upload date, URL). Results default to 10; pass a number to change.

```
/yt-search "Claude Code skills"          # 10 results (default)
/yt-search "machine learning papers" 20  # 20 results
```

Useful on its own for quick video discovery, or as a precursor to `/research-pipeline youtube`.

---

### `/research-pipeline`

The core skill. Collects source material, sends it to NotebookLM for analysis, and writes a structured Obsidian note. Supports four input modes:

```
/research-pipeline youtube "query"                 # Search YouTube, pick videos, analyze
/research-pipeline web https://example.com/article # Extract article via defuddle, analyze
/research-pipeline text "paste any content here"   # Analyze raw text directly
/research-pipeline file /path/to/document.pdf      # Analyze a local PDF or document
```

**Optional flags:**

| Flag | Effect |
|------|--------|
| `--deep` | Use NotebookLM deep research mode instead of quick query. Takes ~5 minutes but produces significantly more thorough analysis. |
| `--deliverable <type>` | Generate a NotebookLM deliverable after analysis. Types: `infographic`, `audio`, `slide_deck`, `report`, `quiz`. |
| `--query "<custom question>"` | Override the default analysis prompt with your own question. Default: comprehensive summary of core concepts, key findings, and practical advice. |
| `--notebook <id>` | Reuse an existing NotebookLM notebook instead of creating a new one. Useful for building up a multi-session research corpus. |

**Full example with flags:**

```
/research-pipeline youtube "transformer architecture" --deep --deliverable slide_deck
```

This searches YouTube, analyzes selected videos in deep mode (~5 min), generates a slide deck, and saves everything to Obsidian.

**Pipeline stages:**

The research pipeline executes in 6 stages. Each stage is self-contained — if a stage fails, the error is reported immediately with a recovery suggestion.

```
Stage 0  Read config         → Load vault_path and output_dir from ~/.config/revolve/config.md
Stage 1  Dependency check    → Verify yt-dlp (YouTube), defuddle (web, optional), NotebookLM MCP
Stage 2  Source ingestion    → Collect data via yt-dlp / defuddle / direct text / file upload
Stage 3  NotebookLM analysis → notebook_create → source_add → notebook_query or research_start
Stage 4  Deliverable (opt)   → studio_create → poll studio_status → download_artifact
Stage 5  Write to Obsidian   → Format as Markdown with frontmatter → write to vault output_dir
Stage 6  Completion          → Report file path, suggest /evolve-claude-md to close the flywheel
```

**Error handling:**

| Error | What happens | Recovery |
|-------|-------------|----------|
| Config file missing | Pipeline stops at Stage 0 | Run `/revolve-setup` to generate config |
| `yt-dlp` not installed | Pipeline stops at Stage 1 (YouTube mode) | `brew install yt-dlp` or `pip install yt-dlp` |
| `defuddle` not installed | Pipeline continues with degraded web mode — URL passed directly to NotebookLM | `npm install -g defuddle-cli` (optional) |
| NotebookLM MCP unavailable | Pipeline stops at Stage 1 | Check MCP server is running; run `nlm login` if auth expired |
| NotebookLM auth expired | API calls fail with auth error | Run `nlm login` to re-authenticate (opens browser) |
| Notebook source limit (50) reached | Cannot add more sources to current notebook | Create a new notebook with `--notebook` flag or let pipeline auto-create |
| `vault_path` directory doesn't exist | Pipeline stops at Stage 5 | Check path in `~/.config/revolve/config.md` |
| Target note file already exists | Pipeline appends new analysis with `---` separator and timestamp — never overwrites | By design — preserves iteration history |
| `research_start` timeout | Deep research takes longer than expected | Wait and retry; NotebookLM processing is asynchronous |

**NotebookLM MCP tools used:**

The research pipeline calls these NotebookLM tools through the MCP bridge. You don't need to call them directly — the skill orchestrates them automatically — but understanding the flow helps with debugging.

| Stage | Tool | What it does |
|-------|------|-------------|
| 3 | `notebook_create(title)` | Creates a new NotebookLM notebook for this research session |
| 2-3 | `source_add(source_type, ...)` | Adds a source to the notebook. Types: `youtube` (video URL), `url` (web page), `text` (raw content), `file` (local document) |
| 3 | `notebook_query(notebook_id, query)` | Quick analysis — asks NotebookLM a question about the sources. Returns in seconds |
| 3 | `research_start(notebook_id, topic)` | Deep analysis — triggers NotebookLM's thorough research mode. Takes ~5 minutes |
| 3 | `research_status(notebook_id)` | Polls the status of a deep research job (pending/processing/complete) |
| 4 | `studio_create(notebook_id, artifact_type)` | Requests a deliverable: `infographic`, `audio`, `slide_deck`, `report`, or `quiz` |
| 4 | `studio_status(notebook_id)` | Polls deliverable generation progress |
| 4 | `download_artifact(notebook_id, artifact_type)` | Downloads the completed deliverable |

All tools require the NotebookLM MCP server to be running and authenticated. If any call fails with an auth error, run `nlm login` to refresh credentials.

---

### `/evolve-claude-md`

Scans two data layers -- raw conversation logs (.jsonl files) and Obsidian notes -- to extract patterns that improve future AI sessions. Findings are appended to CLAUDE.md (never modifies existing content). Extracts six categories: tool patterns, error recovery strategies, skill usage, work preferences, user corrections, and new knowledge.

```
/evolve-claude-md              # Scan last 7 days (default)
/evolve-claude-md --days 30    # Scan last 30 days
/evolve-claude-md --days 1     # Scan today only
```

Always shows a preview and asks for confirmation before writing. Recommended frequency: weekly or after a productive research session.

<div align="right">

[![][back-to-top]][readme-top]

</div>

## Sync Script

Standalone Python script that converts AI conversation files into Obsidian Markdown notes with automatic image extraction. Turns your scattered `.jsonl` and `.json` conversation logs into browsable, searchable notes in your vault.

| Provider | Source Path | Content |
|----------|-------------|---------|
| Claude | `~/.claude/projects/**/*.jsonl` | Full conversations with tool use and images |
| Codex | `~/.codex/sessions/**/*.jsonl` | Full conversations |
| OpenCode | `~/.local/state/opencode/prompt-history.jsonl` | User prompts only |
| Gemini | `~/.gemini/tmp/**/chats/session-*.json` | Full conversations |

### Usage

```bash
# One-shot sync all configured providers
python3 scripts/sync_conversations.py --verbose

# Sync only Claude conversations
python3 scripts/sync_conversations.py --provider claude --verbose

# Sync Claude and Codex only
python3 scripts/sync_conversations.py --provider claude --provider codex --verbose
```

### Automatic sync (macOS launchd)

```bash
# Install the launch agent (runs every 5 minutes and on login)
cp scripts/com.revolve.sync.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.revolve.sync.plist

# Check logs
tail -f ~/.config/revolve/sync.log
```

### Output format

Each synced conversation becomes a note in `<vault_path>/AI Conversations/<provider>/`:

```markdown
---
date: 2026-04-02
provider: claude
model: claude-opus-4
tags:
  - ai-conversation
  - claude
sync_mode: full
---

# Claude Session - 2026-04-02 14:30

## User
How do I set up NotebookLM MCP?

## Assistant
Here are the steps to set up NotebookLM MCP...
```

Sync state is tracked in `~/.config/revolve/.sync_state.json` so re-running only processes new or modified conversations. Delete the state file to force a full re-sync.

See [`scripts/README.md`][sync-docs] for launchd setup, troubleshooting, and advanced options.

<div align="right">

[![][back-to-top]][readme-top]

</div>

## Templates

Copy from `templates/` to your vault's template folder:

- **`research-note.md`** -- Structured note with frontmatter (date, topic, source type, tags). Works with Obsidian Templater for variable substitution.
- **`research-index.md`** -- Dataview-powered index that dynamically lists and filters all research notes by date, topic, source type, or tag.

<div align="right">

[![][back-to-top]][readme-top]

</div>

## Configuration

Run `/revolve-setup` to generate config automatically, or copy `config.md.example` to `~/.config/revolve/config.md`.

| Field | Required | Description |
|-------|----------|-------------|
| `vault_path` | Yes | Absolute path to your Obsidian vault |
| `output_dir` | Yes | Relative path within vault for research notes |
| `screenshots_dir` | No | Relative path for screenshot attachments |
| `sync_providers` | No | Comma-separated: `claude,codex,opencode,gemini` |

Full schema: [`docs/config-contract.md`][config-contract]

<div align="right">

[![][back-to-top]][readme-top]

</div>

## Works With

| Tool | Status | What it adds |
|------|--------|-------------|
| Standalone | Works | All skills functional without other plugins |
| [Compound Engineering][ce-plugin] | Enhanced | `/ce:plan`, `/ce:work`, `/ce:review`, `/ce:compound` |
| [Forge][forge-repo] | Enhanced | CLAUDE.md workflow methodology templates |

<div align="right">

[![][back-to-top]][readme-top]

</div>

## Built With

Revolve stands on the shoulders of these projects:

| Project | Description | Role in Revolve |
|---------|-------------|-----------------|
| [Claude Code][claude-code] | Anthropic's AI coding CLI | Runtime -- all skills execute inside Claude Code sessions |
| [NotebookLM][notebooklm] | Google's free AI research and analysis tool | Analysis engine -- processes YouTube, web, PDF sources into structured findings |
| [notebooklm-mcp][nlm-mcp] | MCP server bridging Claude Code to NotebookLM | Integration layer -- enables skills to call NotebookLM programmatically |
| [Obsidian][obsidian] | Local-first Markdown knowledge base | Storage layer -- research notes and synced conversations live here |
| [yt-dlp][ytdlp] | YouTube metadata extractor CLI | Data collection -- searches YouTube and retrieves video metadata |
| [defuddle][defuddle] | Web page to clean Markdown extractor | Data collection -- strips web pages to clean article text |
| [Compound Engineering][ce-plugin] | AI-powered development workflow plugin by Kieran Klaassen / Every | Workflow enhancement -- provides `/ce:plan`, `/ce:work`, `/ce:review` |
| [Dataview][dataview] | Obsidian plugin for SQL-like note queries | Used in research index template for dynamic note listing |
| [Templater][templater] | Obsidian template engine | Used in research note template for variable substitution |

<div align="right">

[![][back-to-top]][readme-top]

</div>

## Acknowledgments

- [Kieran Klaassen](https://github.com/kieranklaassen) and [Every](https://every.to) -- for [Compound Engineering][ce-plugin], the plugin framework and workflow methodology that inspired Revolve's architecture
- [Google NotebookLM](https://notebooklm.google.com) team -- for providing a free, powerful AI research tool that makes the flywheel possible
- [notebooklm-mcp](https://github.com/sinjab/notebooklm-mcp) contributors -- for bridging NotebookLM to the MCP ecosystem
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) maintainers -- for the most reliable YouTube metadata extraction tool
- [Obsidian](https://obsidian.md) team -- for building the knowledge base that ties the flywheel together
- [Anthropic](https://anthropic.com) -- for Claude Code and the plugin system that makes this possible
- [Best-README-Template](https://github.com/othneildrew/Best-README-Template) -- README structure inspiration

<div align="right">

[![][back-to-top]][readme-top]

</div>

## Contributing

Issues, feature requests, and PRs welcome.

<div align="right">

[![][back-to-top]][readme-top]

</div>

## License

[MIT][license]

<!-- Navigation -->
[readme-top]: #readme-top
[how-it-works]: #how-it-works
[what-you-get]: #what-you-get
[prerequisites]: #prerequisites
[installation]: #installation
[quick-start]: #quick-start
[skills-ref]: #skills-reference
[sync-section]: #sync-script
[templates-section]: #templates
[config-section]: #configuration
[built-with]: #built-with
[acknowledgments]: #acknowledgments
[contributing]: #contributing
[license-section]: #license
[nlm-setup]: #notebooklm-mcp-setup-required

<!-- Images -->
[banner]: images/banner.jpg
[flywheel-diagram]: images/flywheel.gif
[back-to-top]: https://img.shields.io/badge/-Back_to_top-gray?style=flat-square

<!-- Badges -->
[license-badge]: https://img.shields.io/badge/License-MIT-blue?style=flat-square
[claude-badge]: https://img.shields.io/badge/Claude_Code-Plugin-7C3AED?style=flat-square&logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cGF0aCBkPSJNMTIgMkM2LjQ4IDIgMiA2LjQ4IDIgMTJzNC40OCAxMCAxMCAxMCAxMC00LjQ4IDEwLTEwUzE3LjUyIDIgMTIgMnoiIGZpbGw9IndoaXRlIi8+PC9zdmc+
[plugin-badge]: https://img.shields.io/badge/Install-Plugin-14B8A6?style=flat-square
[lang-en-badge]: https://img.shields.io/badge/English-lightgrey?style=flat-square
[lang-zh-badge]: https://img.shields.io/badge/简体中文-lightgrey?style=flat-square

<!-- Links -->
[license]: LICENSE
[claude-code]: https://claude.ai/code
[notebooklm]: https://notebooklm.google.com
[nlm-mcp]: https://github.com/sinjab/notebooklm-mcp
[obsidian]: https://obsidian.md
[ytdlp]: https://github.com/yt-dlp/yt-dlp
[defuddle]: https://github.com/nicekate/defuddle
[install-url]: https://github.com/eisen0419/revolve
[lang-en]: README.md
[lang-zh]: README_CN.md
[sync-docs]: scripts/README.md
[config-contract]: docs/config-contract.md
[ce-plugin]: https://github.com/EveryInc/compound-engineering-plugin
[dataview]: https://github.com/blacksmithgu/obsidian-dataview
[templater]: https://github.com/SilentVoid13/Templater
[forge-repo]: https://github.com/eisen0419/forge
