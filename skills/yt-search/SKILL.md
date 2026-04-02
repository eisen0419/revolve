---
name: yt-search
description: This skill should be used when the user asks to 'search YouTube', 'find YouTube videos', or 'yt-search'. Searches YouTube videos via yt-dlp and returns structured results.
argument-hint: "<search-query> [result-count]"
---

# YouTube 搜索

使用 yt-dlp 搜索 YouTube 视频，返回结构化的视频信息。

## 用法

```bash
# 搜索并返回 10 条结果（默认）
yt-dlp "ytsearch10:<关键词>" --flat-playlist --dump-json 2>/dev/null

# 自定义数量（例如 5 条）
yt-dlp "ytsearch5:<关键词>" --flat-playlist --dump-json 2>/dev/null
```

## 输出格式

将 JSON 结果解析为 Markdown 表格：

| 标题 | URL | 时长 | 观看数 | 上传日期 |
|------|-----|------|--------|----------|
| 视频标题 | https://youtube.com/watch?v=xxx | 10:30 | 50000 | 20260401 |

关键 JSON 字段：`title`、`url`、`duration_string`、`view_count`、`upload_date`、`channel`、`description`

## 完整解析命令

```bash
yt-dlp "ytsearch10:<关键词>" --flat-playlist --dump-json 2>/dev/null | python3 -c "
import json, sys
results = []
for line in sys.stdin:
    d = json.loads(line)
    results.append({
        'title': d.get('title',''),
        'url': d.get('url',''),
        'duration': d.get('duration_string',''),
        'views': d.get('view_count',0),
        'date': d.get('upload_date',''),
        'channel': d.get('channel','')
    })
print('| # | 标题 | 频道 | 时长 | 观看数 | URL |')
print('|---|------|------|------|--------|-----|')
for i, r in enumerate(results, 1):
    print(f\"| {i} | {r['title'][:50]} | {r['channel'][:20]} | {r['duration']} | {r['views']:,} | {r['url']} |\")
"
```

## 前置检查

如果 `yt-dlp` 未安装，根据系统提示用户安装：

```bash
# macOS
brew install yt-dlp

# Linux (pip)
pip install yt-dlp

# Linux (apt)
sudo apt install yt-dlp
```

## 注意事项

- 仅做搜索和元数据提取，不下载视频
- 搜索结果数量通过 `ytsearchN` 的 N 控制
- 可与 `/research-pipeline` 配合使用，将视频 URL 发送到 NotebookLM 进行深度分析
