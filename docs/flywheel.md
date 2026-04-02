# How the Flywheel Works

## The Problem

Every AI session starts with a blank slate. Claude Code has no memory of what you researched last week, which approaches worked, or what patterns you discovered in your domain. Knowledge accumulates in your head, not in the system.

This means the AI gives you the same generic answers every time — unable to build on prior context, prior errors, or prior expertise.

---

## The Flywheel Concept

Revolve introduces a self-reinforcing loop: each research session produces structured knowledge that is stored, and that stored knowledge is periodically fed back into CLAUDE.md — the persistent instruction layer that shapes every future Claude Code session.

```
Research input
      │
      ▼
  Collect raw sources          (YouTube, web pages, PDFs, text)
      │
      ▼
  Analyze with NotebookLM      (free Google AI — no Claude token cost)
      │
      ▼
  Store in Obsidian            (structured Markdown, queryable via dataview)
      │
      ▼
  Evolve CLAUDE.md             (append-only, preserves existing instructions)
      │
      ▼
  Better AI next session       ──────────────────────────────────┐
                                                                  │
      ┌───────────────────────────────────────────────────────────┘
      │
      ▼
  Research input  (loop)
```

Each turn of the loop makes the next one more productive. The flywheel accelerates over time.

---

## Component Roles

### Collect — `/yt-search`, `/research-pipeline`

The entry point. You provide a topic or URL; the skill fetches raw content from YouTube, web pages, PDFs, or pasted text. yt-dlp handles YouTube metadata; defuddle strips web pages to clean article text.

No analysis happens here — collection is intentionally dumb and fast.

### Analyze — NotebookLM

Raw content is sent to NotebookLM (via the MCP server) for deep analysis. NotebookLM runs on Google's infrastructure at no token cost to you. It returns structured summaries, key findings, actionable insights, and — optionally — artifacts like audio overviews or slide decks.

The `/research-pipeline` skill orchestrates this: create notebook → add sources → query → extract results.

### Store — Obsidian

Analysis results are written as structured Markdown notes to your Obsidian vault using the `research-note.md` template. Each note carries YAML frontmatter (date, source, tags, topic) so you can query across your entire research corpus with a single dataview block.

The `research-index.md` template provides a ready-made index view.

### Evolve — `/evolve-claude-md`

This is the flywheel's closing link. The skill performs a dual-layer scan:

1. **AI conversation layer** — scans `~/.claude/projects/**/*.jsonl` for tool call patterns, error/retry sequences, and skill effectiveness signals.
2. **Human reading layer** — scans your Obsidian vault for research notes, project docs, and work logs.

It extracts actionable findings (patterns, corrections, domain knowledge) and appends them to CLAUDE.md in an append-only fashion. Existing instructions are never modified — only new knowledge is added at the end.

On the next Claude Code session, these additions are active immediately.

---

## How They Chain Together

Each component hands off a clean artifact to the next:

| Step | Input | Output |
|------|-------|--------|
| Collect | Topic / URL | Raw content (video metadata, article text, PDF) |
| Analyze | Raw content | Structured findings (summary, key points, insights) |
| Store | Structured findings | Obsidian note with frontmatter + body |
| Evolve | Vault notes + conversation history | CLAUDE.md append block |
| Next session | Updated CLAUDE.md | AI with domain awareness |

The sync script adds a background dimension: AI conversations from Claude, Codex, OpenCode, and Gemini are continuously converted to Obsidian notes, feeding the Evolve step with cross-provider patterns you did not manually capture.

---

## Example Workflow

**Scenario:** You want to get better at using Claude Code for frontend development.

1. Run `/yt-search "Claude Code frontend workflow"` to find relevant videos.
2. Run `/research-pipeline youtube "Claude Code frontend workflow"` — Revolve fetches the video, sends it to NotebookLM, and writes a structured note to `Research/` in your vault.
3. Repeat for a few web articles: `/research-pipeline web "https://example.com/ai-frontend"`.
4. After a week of accumulation, run `/evolve-claude-md --days 7`. The skill scans your vault and recent conversations, extracts patterns (e.g., "component decomposition before implementation reduces back-and-forth"), and appends them to CLAUDE.md.
5. The next Claude Code session opens with those patterns already active in the AI's context — no manual copy-paste required.

Over time, CLAUDE.md grows into a high-fidelity model of your workflows, preferences, and hard-won domain knowledge.
