---
date: 2026-04-02
topic: forge-starter-kit
---

# Forge — AI-Assisted Development Workflow Starter Kit

## Problem Frame

Claude Code users build their CLAUDE.md incrementally through trial and error. Most never discover patterns like task routing, error recovery circuit breaker, quality gates, or structured knowledge compounding. The result: scattered ad-hoc rules instead of a coherent workflow that gets smarter over time.

Forge packages a battle-tested workflow methodology as a reusable starter kit — a verified structural starting point that avoids reinventing workflow patterns from scratch. It is not a "production-grade CLAUDE.md from day one" — real production quality comes from accumulated personal experience. Forge gives you the skeleton; you grow the muscle.

## Flywheel Concept

```
┌─────────────────────────────────────────────────────────┐
│                    FORGE FLYWHEEL                        │
│                                                          │
│   Install Forge → Configure tools → Work on tasks        │
│        ↑                                    ↓            │
│   Better AI ← Update CLAUDE.md ← Compound knowledge     │
│               (manual or Revolve)                        │
│                                                          │
│   Each session makes the next one smarter                │
└─────────────────────────────────────────────────────────┘
```

Note: The "Update CLAUDE.md" step is manual by default. Install Revolve (`/evolve-claude-md`) to automate it.

## Requirements

**Core Framework (CLAUDE.md Template)**

- R1. Provide a CLAUDE.md template with the workflow methodology extracted as reusable rules — task routing, error recovery circuit breaker, quality gates, subagent strategy, and self-improvement loop. Template is a single file with clearly marked sections (no multi-file includes — CLAUDE.md has no import syntax)
- R2. All personal preferences (language, tools, paths, plugins) are fill-in-the-blank variables, not hardcoded
- R3. Each section has inline comments explaining what it does, why it exists, and how to customize it (this replaces the need for a separate philosophy guide)
- R4. Template works standalone without any plugins — the methodology is CLAUDE.md instructions that Claude follows at inference time, not plugin-system features

**Role System**

- R5. Define the abstract role system (designer, inspiration, reviewer, executor) as a CLAUDE.md instruction convention — a markdown mapping table that Claude reads and follows. Explicitly note this is not a Claude Code API feature
- R6. Include the Peer Review Framework (plan review + code review checkpoints) as a configurable pattern
- R7. Role assignments default to Claude-only. Show alternative provider examples as commented-out rows (e.g., `<!-- reviewer | codex | Scored quality gate -->`) so users see the multi-provider pattern without a confusing all-Claude table

**Task Routing & Error Recovery**

- R8. Include the decision-three-questions framework (real problem? simpler approach? what breaks?)
- R9. Include the task routing table (read-only / investigate / lightweight / medium-large) with customizable thresholds
- R10. Include the error recovery circuit breaker (2 failures → re-plan → 3 rounds → escalate to user)
- R11. Include the compact recovery discipline (re-read todo + plan after context compression)

**Quality Gates**

- R12. Include the tiered testing strategy (Level 0-4) as a customizable framework
- R13. Include verification discipline rules (independent verification, no fabricated results)
- R14. Include the blast radius protocol (grep callers before modifying exports)

**Knowledge Compounding**

- R15. Include compound discipline rules (when to compound, judgment criteria, minimum content)
- R16. Include the `docs/solutions/` knowledge store pattern with category structure
- R17. Document Revolve (`/evolve-claude-md`) as the recommended automation for CLAUDE.md evolution, with a fallback description of manual update workflow for users without Revolve

**Tiered Templates**

- R18. Provide two template tiers based on experience level:
  - **Essential** (newcomers): core rules only — task routing, basic quality gates, git conventions. No circuit breaker, no subagent strategy, no compound discipline
  - **Full** (power users): complete methodology including circuit breaker, subagent strategy, role system, compound discipline, blast radius protocol
- R19. `/forge-setup` asks experience level as the first question and generates the appropriate tier

**Setup Plugin (`/forge-setup`)**

- R20. Lightweight Claude Code plugin with a single `/forge-setup` skill that guides users through template configuration
- R21. Setup wizard asks: experience level (essential/full), preferred language, primary tools/plugins, role assignments (full tier only), git workflow preferences
- R22. Generates a customized CLAUDE.md and outputs it to a user-confirmed path. If writing to the active CLAUDE.md path fails or is unsupported, save to `./CLAUDE.md.forge` with instructions to copy manually
- R23. After setup, print install commands for recommended plugins (CE, Revolve) — do not attempt to install them programmatically

**Documentation**

- R24. English README with quickstart, inline philosophy (not a separate guide), and customization reference
- R25. "Works with" section in README showing plugin compatibility (CE, gstack, Revolve, standalone) — a simple table, not a separate matrix document

**Distribution**

- R26. GitHub repo `eisen0419/forge`
- R27. Claude Code plugin on marketplace (self-hosted initially, like Revolve)
- R28. Template files also usable without installing the plugin (just copy the CLAUDE.md template from the repo)
- R29. MIT license

## Success Criteria

- User can go from zero to a working CLAUDE.md in under 15 minutes using `/forge-setup`
- User can copy the template manually from the repo and get full structural value without installing any plugin
- Power users can customize every section without breaking the framework
- `/forge-setup` generates meaningfully different output for Essential vs Full tiers

## Scope Boundaries

- Not reimplementing CE, gstack, or Revolve — Forge references them as recommended tools
- Not building a web UI or dashboard — terminal-native
- Not enforcing a specific plugin stack — the methodology works with any combination
- Not auto-evolving CLAUDE.md — Revolve handles that, and Forge documents the manual alternative
- Not including personal configurations (SSH setup, specific vault paths, provider API keys)
- Not a "production-grade CLAUDE.md from day one" — it's a verified structural starting point

## Key Decisions

- **Name: Forge** — "锻造" metaphor, forging tools into workflows
- **CLAUDE.md template as core** — the methodology lives in the template, not in plugin code. Works even without the plugin
- **Methodology framework, not opinionated config** — extract universal rules, let users fill in their tools/preferences
- **Single skill plugin** — one `/forge-setup` skill only. No `/forge-check` in v1.0 — users can diff against the template to audit drift
- **Tiered templates** — Essential for newcomers (won't overwhelm), Full for power users (complete methodology). `/forge-setup` selects tier based on experience level
- **Revolve as documented recommendation, not integration** — the flywheel's evolution step is manual by default, automated via Revolve for those who install it
- **Separate repo from Revolve** — different concerns (Forge = workflow methodology, Revolve = research + evolution tools)
- **Print, don't install** — `/forge-setup` prints plugin install commands; it does not programmatically install other plugins
- **Inline philosophy** — R3's inline comments replace the need for a separate Workflow Philosophy guide. README covers the high-level "why"
- **Role system is a CLAUDE.md convention** — not a Claude Code API feature. Template includes a mapping table that Claude reads as instructions at inference time

## Differentiation

Why Forge vs. copying someone's CLAUDE.md from GitHub:
1. **Structured methodology, not personal config** — Forge extracts universal workflow patterns; random CLAUDE.md files mix methodology with personal tools/paths
2. **Tiered onboarding** — newcomers get a digestible subset; power users get the full framework
3. **Interactive setup** — `/forge-setup` asks questions and generates a customized template, not a one-size-fits-all copy
4. **Documented rationale** — every rule has an inline comment explaining why it exists, turning the template into a learning artifact

## Dependencies / Assumptions

- Claude Code must be the runtime (CLAUDE.md is Claude-specific)
- Role system works because Claude follows markdown table instructions at inference time (verified in production)
- Plugin installation requires Claude Code plugin system
- Revolve integration is optional — Forge works without it

## Outstanding Questions

### Deferred to Planning

- [Affects R22][Needs research] Can a Claude Code plugin skill write to the user's CLAUDE.md? Test with the Write tool targeting the project CLAUDE.md path. If blocked, fallback to `./CLAUDE.md.forge` is already specified in R22
- [Affects R18][Technical] Exact content split between Essential and Full tiers — which sections go in which tier?
- [Affects R25][Needs research] Which specific CE/gstack skills correspond to which Forge methodology sections?

## Next Steps

→ `/ce:plan` for structured implementation planning
