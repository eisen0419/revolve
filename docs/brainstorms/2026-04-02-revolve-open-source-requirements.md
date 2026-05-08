---
date: 2026-04-02
topic: revolve-open-source
---

# Revolve — Self-Evolving AI Research Architecture

## Problem Frame

AI coding assistants like Claude Code lack a feedback loop: each session starts fresh, knowledge is scattered, and the AI never learns from accumulated experience. Users manually repeat research workflows, and their CLAUDE.md stays static despite growing expertise.

Revolve solves this by creating a **self-reinforcing flywheel**: research → analyze → store → evolve → better AI → better research → loop.

## Flywheel Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                     REVOLVE FLYWHEEL                          │
│                                                               │
│   ┌─────────┐    ┌─────────────┐    ┌──────────┐            │
│   │ Collect  │───▶│  Analyze    │───▶│  Store   │            │
│   │ YouTube  │    │  NotebookLM │    │ Obsidian │            │
│   │ Web/PDF  │    │  (Free AI)  │    │  Vault   │            │
│   └─────────┘    └─────────────┘    └────┬─────┘            │
│                                          │                    │
│   ┌─────────┐    ┌─────────────┐         │                   │
│   │ Better  │◀───│  Evolve     │◀────────┘                   │
│   │ AI      │    │  CLAUDE.md  │  dual-layer scan            │
│   │ Output  │    │  (append)   │  .jsonl + .md               │
│   └────┬────┘    └─────────────┘                             │
│        │                                                      │
│        └──────────── feeds back into ────────────────▶ ↑     │
└──────────────────────────────────────────────────────────────┘
```

## Requirements

**Plugin Package**

- R1. Publish as a Claude Code plugin named `revolve` on the plugin marketplace
- R2. Plugin installs 3 skills: `/research-pipeline`, `/evolve-claude-md`, `/yt-search`
- R3. One-command install: `claude plugin install revolve`
- R4. Skills work independently (each can be used without the others) but are designed to chain

**Research Pipeline Skill (`/research-pipeline`)**

- R5. Accept multiple data source types: YouTube URL/search, web URL, text, file (PDF)
- R6. YouTube mode: search via yt-dlp, present results, user selects, send to NotebookLM
- R7. Web mode: extract via defuddle, send to NotebookLM
- R8. Query NotebookLM for deep analysis, return structured findings
- R9. Optionally generate deliverables (infographic, audio, slides) via NotebookLM Studio
- R10. Write results as Obsidian-formatted Markdown (frontmatter, wikilinks, tags) to a configurable output directory
- R11. After completion, suggest running `/evolve-claude-md` to close the loop

**Evolution Skill (`/evolve-claude-md`)**

- R12. Dual-layer scanning: raw .jsonl conversation files (tool calls, errors, retries, corrections) + Obsidian .md notes
- R13. Extract 6 signal categories: tool patterns, error recovery, skill usage, user corrections, work preferences, new knowledge
- R14. Append-only mode: never modify existing CLAUDE.md content, only append to a dedicated `# Evolution Log` section
- R15. Show diff preview and require user approval before writing
- R16. Configurable scan window (default 7 days)

**YouTube Search Skill (`/yt-search`)**

- R17. Search YouTube via yt-dlp, return structured table (title, channel, duration, views, URL)
- R18. Configurable result count
- R19. Prerequisite check: prompt to install yt-dlp if not found

**AI Conversation Sync (companion tool, not a skill)**

- R20. Python script that converts Claude Code / Codex / OpenCode / Gemini conversation .jsonl/.db/.json into Obsidian Markdown
- R21. Extract base64 images from conversations (including tool_result-nested images) and save as attachments
- R22. Embed images in notes using Obsidian `![[filename]]` syntax
- R23. Filter system messages, fold skill injections, clean titles
- R24. fswatch + launchd auto-sync with 30-second debounce
- R25. Distributed as a standalone script in the GitHub repo (not part of the plugin)

**Obsidian Templates**

- R26. Research note template with frontmatter (date, topic, source_type, notebook_id, tags)
- R27. Dataview-powered research index
- R28. Distributed as part of the GitHub repo with setup instructions

**Documentation**

- R29. English README with architecture diagram, quickstart, and configuration guide
- R30. Chinese README (README_CN.md) with same content
- R31. "How the Flywheel Works" conceptual guide explaining the self-reinforcing loop
- R32. Video/GIF demo of the complete flywheel in action

**Configuration & Portability**

- R33. All file paths must be configurable (Obsidian vault path, output directory, screenshots directory) — no hardcoded paths in distributed code
- R34. First-run setup wizard or `/revolve-setup` skill that detects Obsidian vault location and configures paths

## Success Criteria

- User can install the plugin and run the full flywheel (research → store → evolve) within 30 minutes
- Research pipeline produces a well-formatted Obsidian note from a YouTube URL in under 5 minutes
- Evolution skill surfaces at least 3 actionable findings from 7 days of activity
- GitHub repo gets meaningful engagement (stars, forks, issues) from AI productivity community
- Works on macOS out of the box; Linux with minimal adaptation

## Scope Boundaries

- Not a general-purpose Obsidian plugin — requires Claude Code as the runtime
- Not a replacement for CE / claude-mem / Prismer — complements them
- Not supporting non-Claude AI assistants in v1.0 (sync script supports Codex/OpenCode/Gemini for reading, but evolution only targets CLAUDE.md)
- Not building a web UI or dashboard — terminal + Obsidian is the interface
- Not auto-evolving without user approval — human-in-the-loop always

## Key Decisions

- **Name: Revolve** — re-evolve double meaning, matches self-evolution core concept
- **Primary distribution: Claude Code plugin marketplace** — one-command install for skills; GitHub for sync script, templates, and docs
- **Target audience: AI efficiency enthusiasts** — core features need Claude Code, but architecture/concepts are portable to any AI tool chain
- **Language: English-first** — all code, skills, and primary docs in English; README_CN.md for Chinese audience
- **MVP = complete flywheel** — all 5 components ship in v1.0, no phased release
- **License: MIT** — maximally permissive for adoption
- **Hardcoded paths removed** — all paths configurable via setup wizard or config file

## Dependencies / Assumptions

- NotebookLM MCP server must be configured separately (not bundled — it's a third-party tool)
- yt-dlp must be installed separately (brew/pip)
- defuddle must be installed separately (npm)
- Obsidian must be installed with a vault already set up
- Python 3 required for sync script

## Outstanding Questions

### Deferred to Planning
- [Affects R33][Technical] Configuration storage: use a `revolve.config.json` in the vault root, or leverage Claude Code's settings.json?
- [Affects R34][Technical] Setup wizard implementation: interactive skill vs. CLI script?
- [Affects R1][Needs research] Claude Code plugin marketplace publishing process and requirements
- [Affects R25][Technical] Sync script packaging: standalone .py or pip-installable package?
- [Affects R20][Technical] Should sync script support Codex/OpenCode/Gemini in v1.0, or start Claude-only?

## Next Steps

→ `/ce:plan` for structured implementation planning
