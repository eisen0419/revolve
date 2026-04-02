#!/usr/bin/env python3
"""Revolve Conversation Sync — convert AI conversation files to Obsidian notes.

Supports: Claude, Codex, OpenCode, Gemini.
Dependencies: Python 3.8+ stdlib only (Pillow optional for image optimization).
"""

import argparse
import base64
import json
import logging
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

CONFIG_PATH = Path.home() / ".config" / "revolve" / "config.md"
STATE_PATH = Path.home() / ".config" / "revolve" / ".sync_state.json"

PROVIDER_ROOTS = {
    "claude": Path.home() / ".claude" / "projects",
    "codex": Path.home() / ".codex" / "sessions",
    "opencode": Path.home() / ".local" / "state" / "opencode" / "prompt-history.jsonl",
    "gemini": Path.home() / ".gemini" / "tmp",
}

GEMINI_EXCLUDE = {"oauth_creds.json", "settings.json", "config.json"}

log = logging.getLogger("revolve-sync")

def parse_config() -> Dict[str, str]:
    """Parse YAML frontmatter from config.md."""
    if not CONFIG_PATH.exists():
        sys.exit(f"[ERROR] Config not found: {CONFIG_PATH}\n"
                 "Run /revolve-setup or copy config.md.example to create it.")
    text = CONFIG_PATH.read_text(encoding="utf-8")
    m = re.search(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not m:
        sys.exit(f"[ERROR] No YAML frontmatter in {CONFIG_PATH}")
    cfg: Dict[str, str] = {}
    for line in m.group(1).splitlines():
        if ": " in line:
            key, val = line.split(": ", 1)
            cfg[key.strip()] = val.strip()
    if "vault_path" not in cfg:
        sys.exit("[ERROR] vault_path not set in config")
    return cfg

def load_state() -> Dict[str, Any]:
    if STATE_PATH.exists():
        try:
            return json.loads(STATE_PATH.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            log.warning("Corrupted sync state — starting fresh")
    return {}

def save_state(state: Dict[str, Any]) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, indent=2, ensure_ascii=False),
                          encoding="utf-8")

def is_synced(state: Dict[str, Any], path: Path) -> bool:
    key = str(path)
    try:
        mtime = path.stat().st_mtime
    except OSError:
        return True
    entry = state.get(key)
    return entry is not None and entry.get("mtime") == mtime

def mark_synced(state: Dict[str, Any], path: Path) -> None:
    state[str(path)] = {"mtime": path.stat().st_mtime,
                        "synced_at": datetime.now(timezone.utc).isoformat()}

def sanitize_title(text: str, max_len: int = 50) -> str:
    """Generate safe filename title from user message."""
    title = text.strip().replace("\n", " ")[:max_len]
    title = re.sub(r'[\\/*?"<>|:#]', "", title)
    title = re.sub(r"\s+", " ", title).strip()
    return title or "untitled"

def write_obsidian_note(
    vault_path: str,
    provider: str,
    title: str,
    date_str: str,
    body: str,
    extra_frontmatter: Optional[Dict[str, str]] = None,
) -> Path:
    """Write an Obsidian Markdown note, return file path."""
    out_dir = Path(vault_path) / "AI Conversations" / provider
    out_dir.mkdir(parents=True, exist_ok=True)

    safe_title = sanitize_title(title)
    slug = f"{date_str} {safe_title}"
    out_file = out_dir / f"{slug}.md"
    counter = 1
    while out_file.exists():
        out_file = out_dir / f"{slug} ({counter}).md"
        counter += 1

    fm: Dict[str, str] = {
        "date": date_str,
        "provider": provider,
        "title": safe_title,
        "tags": f"ai-conversation, {provider}",
    }
    if extra_frontmatter:
        fm.update(extra_frontmatter)

    lines = ["---"]
    for k, v in fm.items():
        lines.append(f"{k}: {v}")
    lines.append("---")
    lines.append("")
    lines.append(body)

    try:
        out_file.write_text("\n".join(lines), encoding="utf-8")
    except OSError as exc:
        log.error("Failed to write note %s: %s", out_file, exc)
        body_no_img = re.sub(r"!\[\[.*?\]\]\n?", "", body)
        try:
            out_file.write_text("\n".join(lines[:len(fm)+2]) + "\n\n" + body_no_img,
                                encoding="utf-8")
        except OSError:
            log.error("Cannot write even stripped note — disk full?")
            raise
    log.info("Wrote %s", out_file)
    return out_file

def extract_images(
    blocks: List[Dict[str, Any]],
    vault_path: str,
    conv_id: str,
) -> Dict[str, str]:
    """Extract base64 images from tool_result blocks and save to vault."""
    img_dir = Path(vault_path) / "attachments" / "ai-conversations"
    img_dir.mkdir(parents=True, exist_ok=True)
    result: Dict[str, str] = {}
    idx = 0
    for block in blocks:
        if not isinstance(block, dict):
            continue
        contents = block.get("content", [])
        if isinstance(contents, str):
            continue
        for item in contents if isinstance(contents, list) else []:
            if not isinstance(item, dict):
                continue
            if item.get("type") == "image":
                source = item.get("source", {})
                data = source.get("data", "")
                media_type = source.get("media_type", "image/png")
                if not data:
                    continue
                ext = media_type.split("/")[-1].split(";")[0]
                if ext not in ("png", "jpeg", "jpg", "gif", "webp"):
                    ext = "png"
                fname = f"{conv_id}_{idx}.{ext}"
                fpath = img_dir / fname
                try:
                    fpath.write_bytes(base64.b64decode(data))
                    result[str(idx)] = f"![[ai-conversations/{fname}]]"
                    idx += 1
                except Exception as exc:
                    log.warning("Image decode failed: %s", exc)
    return result

def _date_from_mtime(path: Path) -> str:
    try:
        return datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d")
    except OSError:
        return "unknown"

def _is_skill_injection(text: str) -> bool:
    """Detect skill injection blocks (long system prompts) for folding."""
    markers = ["<command-name>", "IMPORTANT: These instructions OVERRIDE",
               "system-reminder", "# MCP Server Instructions"]
    return any(m in text[:500] for m in markers)

def _read_jsonl(path: Path) -> List[Dict[str, Any]]:
    """Read JSONL file, skip corrupt lines."""
    items: List[Dict[str, Any]] = []
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            for lineno, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    items.append(json.loads(line))
                except json.JSONDecodeError:
                    log.debug("Skipping corrupt line %d in %s", lineno, path)
    except OSError as exc:
        log.warning("Cannot read %s: %s", path, exc)
    return items

def sync_claude(vault_path: str, state: Dict[str, Any]) -> int:
    """Sync Claude conversations. Return count of newly synced."""
    root = PROVIDER_ROOTS["claude"]
    if not root.exists():
        log.debug("Claude root not found: %s", root)
        return 0
    count = 0
    for jsonl in sorted(root.rglob("*.jsonl")):
        if is_synced(state, jsonl):
            continue
        items = _read_jsonl(jsonl)
        if not items:
            mark_synced(state, jsonl)
            continue

        parts: List[str] = []
        first_user_msg = ""
        model = ""
        date_str = ""
        tool_result_blocks: List[Dict[str, Any]] = []

        for item in items:
            ts = item.get("timestamp")
            if ts and not date_str:
                date_str = ts[:10]
            msg_type = item.get("type", "")
            # Skip non-message metadata events
            if msg_type in ("system", "summary", "queue-operation", "last-prompt",
                            "login", "logout", "session-start", "session-end",
                            "progress", "result", "error"):
                continue

            role = item.get("role", msg_type)
            message = item.get("message", {})
            if isinstance(message, dict):
                role = message.get("role", role)
                model = message.get("model", model)

            content = message.get("content", "") if isinstance(message, dict) else item.get("content", "")
            if isinstance(content, list):
                text_parts = []
                for c in content:
                    if isinstance(c, dict):
                        if c.get("type") == "text":
                            text_parts.append(c.get("text", ""))
                        elif c.get("type") == "tool_use":
                            text_parts.append(f"\n`{c.get('name', 'tool')}()`\n")
                        elif c.get("type") == "tool_result":
                            tool_result_blocks.append(c)
                content = "\n".join(text_parts)
            if not isinstance(content, str):
                continue

            if _is_skill_injection(content):
                parts.append(f"\n> [!abstract]- System prompt (folded)\n> ...\n")
                continue

            if role in ("human", "user") and not first_user_msg:
                first_user_msg = content

            label = {"human": "User", "user": "User", "assistant": "Assistant"}.get(role, role.title())
            parts.append(f"## {label}\n\n{content}\n")

        if not parts:
            mark_synced(state, jsonl)
            continue

        if not date_str:
            date_str = _date_from_mtime(jsonl)
        conv_id = jsonl.stem
        images = extract_images(tool_result_blocks, vault_path, conv_id)
        body = "\n".join(parts)
        for img_key, embed in images.items():
            body += f"\n{embed}\n"

        extra: Dict[str, str] = {}
        if model:
            extra["model"] = model

        write_obsidian_note(vault_path, "claude", first_user_msg or conv_id,
                            date_str, body, extra)
        mark_synced(state, jsonl)
        count += 1
    return count

def sync_codex(vault_path: str, state: Dict[str, Any]) -> int:
    """Sync Codex conversations."""
    root = PROVIDER_ROOTS["codex"]
    if not root.exists():
        log.debug("Codex root not found: %s", root)
        return 0
    count = 0
    for jsonl in sorted(root.rglob("*.jsonl")):
        if is_synced(state, jsonl):
            continue
        items = _read_jsonl(jsonl)
        if not items:
            mark_synced(state, jsonl)
            continue

        parts: List[str] = []
        first_user_msg = ""
        date_str = ""
        model = ""

        for item in items:
            event_type = item.get("type", "")
            if event_type not in ("response_item", "event_msg"):
                continue

            ts = item.get("timestamp", item.get("created_at", ""))
            if ts and not date_str:
                date_str = str(ts)[:10]

            # Codex stores actual data under "payload"
            payload = item.get("payload", item)
            if not isinstance(payload, dict):
                continue

            # For event_msg, skip non-message payloads
            if event_type == "event_msg" and payload.get("type") not in ("message",):
                continue

            role = payload.get("role", "")
            model = payload.get("model", item.get("model", model))

            # Skip developer/system messages
            if role in ("developer", "system"):
                continue

            content_parts = payload.get("content", [])
            if isinstance(content_parts, str):
                text = content_parts
            elif isinstance(content_parts, list):
                text = "\n".join(
                    c.get("text", "") for c in content_parts
                    if isinstance(c, dict) and c.get("type") in ("text", "output_text", "input_text")
                )
            else:
                continue

            if not text.strip():
                continue
            if _is_skill_injection(text):
                continue

            # Skip Codex bootstrap user messages (environment_context, AGENTS.md, permissions, etc.)
            if role == "user" and (
                text.lstrip().startswith("<environment_context>")
                or text.lstrip().startswith("<permissions")
                or text.lstrip().startswith("# AGENTS.md")
                or text.lstrip().startswith("# CLAUDE.md")
            ):
                continue

            if role == "user" and not first_user_msg:
                first_user_msg = text

            label = "User" if role == "user" else "Assistant"
            parts.append(f"## {label}\n\n{text}\n")

        if not parts:
            mark_synced(state, jsonl)
            continue

        if not date_str:
            date_str = _date_from_mtime(jsonl)
        extra: Dict[str, str] = {}
        if model:
            extra["model"] = model
        write_obsidian_note(vault_path, "codex", first_user_msg or jsonl.stem,
                            date_str, "\n".join(parts), extra)
        mark_synced(state, jsonl)
        count += 1
    return count

def sync_opencode(vault_path: str, state: Dict[str, Any]) -> int:
    """Sync OpenCode prompt history (prompts only, no responses).

    Tracks the last synced line offset to avoid re-exporting the entire
    append-only history file on every run.
    """
    src = PROVIDER_ROOTS["opencode"]
    if not src.exists():
        log.debug("OpenCode history not found: %s", src)
        return 0

    # Track offset: only read new lines since last sync
    state_key = str(src) + ":offset"
    last_offset = state.get(state_key, 0)

    try:
        with open(src, "r", encoding="utf-8", errors="replace") as fh:
            fh.seek(last_offset)
            new_lines = fh.readlines()
            new_offset = fh.tell()
    except OSError as exc:
        log.warning("Cannot read OpenCode history: %s", exc)
        return 0

    if not new_lines:
        return 0

    grouped: Dict[str, List[str]] = {}
    for line in new_lines:
        line = line.strip()
        if not line:
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            continue
        ts = item.get("timestamp", item.get("created_at", ""))
        # OpenCode entries often lack timestamps — fall back to today's date
        date_str = str(ts)[:10] if ts else datetime.now().strftime("%Y-%m-%d")
        prompt = item.get("input", item.get("prompt", item.get("content", "")))
        if isinstance(prompt, dict):
            prompt = prompt.get("text", str(prompt))
        if not prompt or not isinstance(prompt, str):
            continue
        grouped.setdefault(date_str, []).append(prompt.strip())

    count = 0
    for date_str, prompts in grouped.items():
        body_parts = []
        for i, p in enumerate(prompts, 1):
            body_parts.append(f"## Prompt {i}\n\n{p}\n")
        first = prompts[0] if prompts else "opencode prompts"
        extra = {"sync_mode": "prompt-only"}
        write_obsidian_note(vault_path, "opencode", first,
                            date_str, "\n".join(body_parts), extra)
        count += 1

    # Save new offset so next run only reads appended lines
    state[state_key] = new_offset
    return count

def sync_gemini(vault_path: str, state: Dict[str, Any]) -> int:
    """Sync Gemini conversations, excluding non-chat JSON files."""
    root = PROVIDER_ROOTS["gemini"]
    if not root.exists():
        log.debug("Gemini root not found: %s", root)
        return 0
    count = 0
    for jf in sorted(root.rglob("chats/session-*.json")):
        if jf.name in GEMINI_EXCLUDE:
            continue
        if is_synced(state, jf):
            continue

        try:
            data = json.loads(jf.read_text(encoding="utf-8", errors="replace"))
        except (json.JSONDecodeError, OSError) as exc:
            log.warning("Skipping corrupt Gemini file %s: %s", jf, exc)
            continue

        if not isinstance(data, (dict, list)):
            mark_synced(state, jf)
            continue

        messages = data if isinstance(data, list) else data.get("messages", data.get("conversation", []))
        if not isinstance(messages, list):
            mark_synced(state, jf)
            continue

        parts: List[str] = []
        first_user_msg = ""
        date_str = ""
        model = ""

        if isinstance(data, dict):
            model = data.get("model", "")
            ts = data.get("created_at", data.get("timestamp", ""))
            if ts:
                date_str = str(ts)[:10]

        for msg in messages:
            if not isinstance(msg, dict):
                continue
            # Gemini uses "type" field: "user" or "gemini"
            msg_type = msg.get("type", msg.get("role", ""))
            if msg_type in ("system",):
                continue
            # Per-message model (Gemini stores model on each message)
            msg_model = msg.get("model", "")
            if msg_model and not model:
                model = msg_model
            content = msg.get("content", msg.get("text", msg.get("parts", "")))
            if isinstance(content, list):
                content = "\n".join(
                    p.get("text", str(p)) if isinstance(p, dict) else str(p)
                    for p in content
                )
            if not isinstance(content, str) or not content.strip():
                continue
            if _is_skill_injection(content):
                continue

            is_user = msg_type == "user"
            if is_user and not first_user_msg:
                first_user_msg = content

            ts = msg.get("timestamp", msg.get("created_at", ""))
            if ts and not date_str:
                date_str = str(ts)[:10]

            label = "User" if is_user else "Assistant"
            parts.append(f"## {label}\n\n{content}\n")

        if not parts:
            mark_synced(state, jf)
            continue

        if not date_str:
            date_str = _date_from_mtime(jf)
        extra: Dict[str, str] = {}
        if model:
            extra["model"] = model
        write_obsidian_note(vault_path, "gemini", first_user_msg or jf.stem,
                            date_str, "\n".join(parts), extra)
        mark_synced(state, jf)
        count += 1
    return count

SYNC_FUNCS = {
    "claude": sync_claude,
    "codex": sync_codex,
    "opencode": sync_opencode,
    "gemini": sync_gemini,
}

def main() -> None:
    parser = argparse.ArgumentParser(description="Revolve Conversation Sync")
    parser.add_argument("--once", action="store_true", default=True,
                        help="Process all new conversations and exit (default)")
    parser.add_argument("--provider", choices=list(SYNC_FUNCS.keys()),
                        help="Sync only one provider")
    parser.add_argument("--verbose", action="store_true",
                        help="Print progress")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
    )

    cfg = parse_config()
    vault_path = cfg["vault_path"]
    allowed = set(cfg.get("sync_providers", "claude,codex,opencode,gemini").split(","))
    state = load_state()

    providers = [args.provider] if args.provider else list(SYNC_FUNCS.keys())
    total = 0

    for prov in providers:
        if prov not in allowed:
            log.debug("Provider %s not in sync_providers — skipping", prov)
            continue
        fn = SYNC_FUNCS[prov]
        try:
            n = fn(vault_path, state)
            if n:
                log.info("[%s] Synced %d conversation(s)", prov, n)
            total += n
        except Exception:
            log.exception("Provider %s failed — continuing with others", prov)

    save_state(state)
    log.info("Done. Total synced: %d", total)

if __name__ == "__main__":
    main()
