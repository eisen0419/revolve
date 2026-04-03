# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-04-02

### Added

**Skills**
- `/revolve-setup` skill: interactive wizard that detects Obsidian vault, checks dependencies (yt-dlp, python3), and writes `~/.config/revolve/config.md`
- `/research-pipeline` skill: multi-source research via NotebookLM → Obsidian; supports youtube, web, text, file, and screenshot modes with deep-dive and deliverable options
- `/evolve-claude-md` skill: dual-layer scan of Claude conversation history and Obsidian notes; appends actionable findings to CLAUDE.md in append-only mode
- `/yt-search` skill: YouTube search via yt-dlp with transcript extraction for research purposes

**Sync Script**
- `scripts/sync_conversations.py`: exports AI conversations from 4 providers (Claude, Codex, OpenCode, Gemini) to Obsidian markdown notes with incremental sync state to prevent re-processing
- `scripts/com.revolve.sync.plist`: macOS launchd agent template for automatic sync every 5 minutes (no fswatch dependency)

**Templates**
- `templates/research-note.md`: Obsidian research note template with required frontmatter fields (topic, date, type, sources, tags, status)
- `templates/research-index.md`: Obsidian dataview index template listing all research notes sorted by date

**Configuration**
- `config.md.example`: template configuration file with all supported fields
- `docs/config-contract.md`: schema reference defining all config fields, consumers, and reading conventions

**Documentation**
- `README.md`: comprehensive English documentation with usage examples, skill reference, and flywheel diagram
- `README_CN.md`: full Chinese translation of README
- `docs/flywheel.md`: architecture description of the self-reinforcing research and evolution flywheel
- `CONTRIBUTING.md`: contribution guidelines for skill and script development

**Plugin Manifest**
- `.claude-plugin/plugin.json`: Claude Code plugin manifest declaring 4 skills at version 0.1.0
