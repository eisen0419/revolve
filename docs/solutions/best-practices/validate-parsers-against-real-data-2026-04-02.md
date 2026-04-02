---
title: Third-Party Parser Format Assumptions Always Wrong — Examine Real Files First
date: 2026-04-02
category: best-practices
module: sync-script / data-parsing
problem_type: best_practice
component: tooling
severity: high
applies_when:
  - Writing parsers for undocumented or third-party data formats
  - Multi-provider integrations where each provider has a different schema
  - Any code that reads files written by tools you don't control
  - Plan says "format is uncertain" or "best-effort"
symptoms:
  - Parser silently produces empty or incomplete output
  - Duplicate notes created on repeated sync runs
  - Bootstrap/metadata messages leak into exported conversation content
  - Date fields show 'unknown' due to missing timestamp fields
tags:
  - parser
  - data-format
  - sync-script
  - silent-corruption
  - codex-review
  - multi-provider
---

# Third-Party Parser Format Assumptions Always Wrong — Examine Real Files First

## Context

When writing parsers for third-party data formats (AI conversation logs, API responses, undocumented file formats), plan-time format assumptions are almost always wrong. Even when the plan explicitly acknowledges format uncertainty, implementation tends to code against the assumed format rather than examining real data first.

In the Revolve sync script, all 4 provider parsers (Claude, Codex, OpenCode, Gemini) had format errors. The plan documented the risk ("3 of 4 provider formats are undocumented and unstable") but the mitigation was "best-effort with graceful degradation" — which meant silent wrong output, not crashes. Only an external code review (Codex reviewer independently examining real files on disk) caught all 6 issues across 3 review rounds.

## Guidance

1. **Examine real files before writing any parser.** Run `head -20 <file>` or `python3 -c "import json; ..."` on 2–3 actual data files before touching implementation. Do this before the plan is finalized, not after.

2. **Document the REAL schema as a comment block at the top of each parser function.** Include actual field names, nesting structure, and discriminator values. This forces the schema to be verified and makes format drift visible.

3. **For append-only logs, track file offset — not mtime.** Re-reading the entire file on mtime change duplicates all previously processed entries. Store the byte offset and seek to it on subsequent reads.

4. **For formats with metadata/bootstrap events mixed with real content, use an allowlist of content event types — not a blocklist.** Blocking known metadata types is whack-a-mole. Allowlisting known content types is stable.

5. **Include an external reviewer as a quality gate for parsers.** The implementer has format blindness from reading the plan. A reviewer who independently examines the real files catches what the implementer cannot see.

## Why This Matters

All 6 bugs produced **silent wrong output, not crashes**:
- Wrong content (empty `role` fields → messages attributed to nobody)
- Wrong roles (all Gemini turns mislabeled)
- Wrong dates (all OpenCode entries showing "unknown")
- Polluted titles (synthetic bootstrap messages rendered as note sections)
- Duplicated content (entire OpenCode log replayed on every file change)
- Metadata noise (Claude `queue-operation` events rendered as conversation)

Users would see "working" sync producing garbage Obsidian notes. **Silent corruption is worse than crashes** — a crash surfaces the bug immediately; silent corruption may go undetected for weeks.

## When to Apply

- Writing parsers for any undocumented or third-party data format
- Multi-provider integrations where each provider has a different schema
- Any code that reads files written by tools you don't control
- Any plan that says "format is uncertain" or "best-effort" — treat that phrase as a trigger to examine real files immediately

## Examples

### Codex JSONL — payload wrapper

```python
# Before: assumes role/content at top level
role = item.get("role", "")           # always "" — field lives under payload

# After: unwrap payload first
payload = item.get("payload", item)
role = payload.get("role", "")        # correct
```

### Gemini JSON — type field, not role

```python
# Before: assumes OpenAI-style role field
role = msg.get("role", "")            # never "user" — Gemini uses "type"

# After: check type first
msg_type = msg.get("type", msg.get("role", ""))   # "user" / "gemini"
```

### OpenCode — offset tracking, not mtime

```python
# Before: re-read entire file on mtime change → duplicates everything
entries = read_all_entries(path)

# After: seek to last known offset → only new entries
with open(path) as f:
    f.seek(last_offset)
    new_entries = [json.loads(line) for line in f]
```

### Claude — metadata event filtering

```python
# Before: only skip "system" and "summary"
if msg_type in ("system", "summary"): continue   # misses queue-operation, last-prompt

# After: explicit metadata blocklist
if msg_type in ("system", "summary", "queue-operation", "last-prompt",
                "session-start", "session-end", "progress", "result", "error"):
    continue
```

## Related

- `docs/config-contract.md` — an example of format validation applied proactively (simple unquoted strings to enable reliable regex parsing)
- Codex review (3 rounds): the external quality gate that caught all 6 parser bugs
