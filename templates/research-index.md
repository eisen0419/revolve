---
date: 2026-04-02
tags:
  - index
  - research
---

# Research Index

## All Research Notes

```dataview
TABLE date, source_type, status, tags
FROM "" 
WHERE contains(tags, "research") AND !contains(file.name, "index")
SORT date DESC
```

## By Source Type

### YouTube
```dataview
TABLE date, topic, status
FROM ""
WHERE source_type = "youtube"
SORT date DESC
```

### Web
```dataview
TABLE date, topic, status
FROM ""
WHERE source_type = "web"
SORT date DESC
```

### PDF
```dataview
TABLE date, topic, status
FROM ""
WHERE source_type = "pdf"
SORT date DESC
```

## Recent (Last 30 Days)

```dataview
TABLE date, source_type, topic
FROM ""
WHERE contains(tags, "research") AND date >= date(today) - dur(30 days)
SORT date DESC
```
