---
name: yt-search
description: This skill should be used when the user asks to 'search YouTube', 'find YouTube videos', 'yt-search', or 'find video transcripts'. Searches YouTube videos via yt-dlp and extracts transcripts for research purposes.
argument-hint: "<search-query>"
---

# /yt-search

Search YouTube videos and extract transcripts for research purposes.

## Trigger

User runs `/yt-search <query>` or asks to search YouTube / find video transcripts.

## Instructions

### Step 0: Dependency Check

Verify yt-dlp is available:

```bash
which yt-dlp
```

- If missing: inform the user "yt-dlp is required. Install via `pip install yt-dlp` or `brew install yt-dlp`"
- Abort if dependency is missing — do not proceed.

### Step 1: Read Config

Read `config.md` in the plugin root to get `output_dir`.

- If config.md is missing: inform the user "Run /revolve-setup first to configure Revolve."
- Default output_dir fallback: `~/Downloads/revolve-research`

Extract the `output_dir` value from the YAML frontmatter in config.md.

### Step 2: Search YouTube

Use yt-dlp to search YouTube for the query and parse results:

```bash
yt-dlp "ytsearch5:<query>" --flat-playlist --dump-json 2>/dev/null | python3 -c "
import json, sys
results = []
for line in sys.stdin:
    d = json.loads(line)
    results.append({
        'title': d.get('title', ''),
        'url': d.get('url', ''),
        'duration': d.get('duration_string', ''),
        'views': d.get('view_count', 0),
        'date': d.get('upload_date', ''),
        'channel': d.get('channel', '')
    })
print('| # | Title | Channel | Duration | Views | URL |')
print('|---|-------|---------|----------|-------|-----|')
for i, r in enumerate(results, 1):
    print(f\"| {i} | {r['title'][:50]} | {r['channel'][:20]} | {r['duration']} | {r['views']:,} | {r['url']} |\")
"
```

Present results as a numbered table with title, channel, duration, and URL.

### Step 3: Select Video

Ask user to select a video number from the results, or enter a YouTube URL directly.

### Step 4: Extract Transcript

Extract transcript/subtitles using yt-dlp with the output_dir from config:

```bash
yt-dlp --write-auto-sub --sub-lang en --skip-download \
  --output "<output_dir>/%(title)s.%(ext)s" <url>
```

If no English subtitles are available, try other available languages:

```bash
yt-dlp --write-auto-sub --skip-download \
  --output "<output_dir>/%(title)s.%(ext)s" <url>
```

### Step 5: Format and Save

Parse the subtitle file (vtt/srt) and format as clean text, stripping timestamps and duplicate lines.

Save to `<output_dir>/yt-<video-id>-transcript.md` with frontmatter:

```markdown
---
source: youtube
url: <video_url>
title: <video_title>
date: <today>
---

<transcript text>
```

Report the saved file path to the user.

## Notes

- Search results come from yt-dlp's `ytsearch` prefix; adjust N in `ytsearchN` for more results
- Can be used with `/research-pipeline` — pass the saved transcript file path for further analysis
- Only downloads subtitles, never full video files
