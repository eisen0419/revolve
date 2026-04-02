---
name: research-pipeline
description: "This skill should be used when the user asks to 'research a topic', 'analyze a video', or 'run the research pipeline'. Runs a multi-source research pipeline via NotebookLM to create Obsidian notes."
argument-hint: "<mode> <query> [--deep] [--deliverable <type>]"
---

# Research Pipeline

一条命令完成：数据源采集 → NotebookLM 深度分析 → 结构化结果写入 Obsidian。

分析工作由 NotebookLM 承担（免费 Google AI 算力），不消耗 Claude token。

## 用法 / Usage

```
/research-pipeline youtube "claude code skills"
/research-pipeline web "https://example.com/article"
/research-pipeline text "粘贴的文本内容"
/research-pipeline file "/path/to/document.pdf"
```

可选参数 / Optional flags:
- `--deep` — 启用深度研究模式（使用 `research_start`，约 5 分钟；默认使用 `notebook_query` 快速模式）
- `--deliverable <type>` — 请求 NotebookLM 生成交付物（infographic / audio / slide_deck / report / quiz）
- `--query "<自定义分析问题>"` — 自定义分析角度（默认：全面总结核心内容、关键发现和实用建议）
- `--notebook <id>` — 复用已有 notebook（默认：以主题创建新 notebook）

---

## Pipeline 执行流程

### 阶段 0：读取配置 / Read Config

```bash
cat ~/.config/revolve/config.md 2>/dev/null
```

从 frontmatter 解析：
- `vault_path` — Obsidian vault 根目录（必填）
- `output_dir` — vault 内研究笔记目录（必填）

若文件缺失或 `vault_path` / `output_dir` 为空，输出：

```
❌ Revolve 配置未找到。请先运行 /revolve-setup 完成初始配置。
```

然后**立即停止**，不执行后续步骤。

目标输出路径：`<vault_path>/<output_dir>/`

---

### 阶段 1：前置检查 / Dependency Checks

根据 mode 进行检查：

**YouTube 模式：**
```bash
which yt-dlp || echo "MISSING"
```
若缺失 → 提示并停止：
```
❌ yt-dlp 未安装。请运行：brew install yt-dlp
```

**Web 模式：**
```bash
which defuddle || echo "MISSING"
```
若缺失 → 不停止，仅记录降级：将跳过 defuddle 解析，直接用 URL 让 NotebookLM 处理。

**NotebookLM MCP：**
在继续之前确认 NotebookLM MCP 工具可用（`notebook_list` 测试调用）。若失败，提示：
```
❌ NotebookLM MCP 不可用。请确认 MCP 服务已启动，或运行 nlm login 重新认证。
```

---

### 阶段 2：数据采集 / Source Ingestion

根据 mode 分发：

**YouTube 模式：**
1. 使用 yt-dlp 搜索视频：
   ```bash
   yt-dlp "ytsearch10:<关键词>" --flat-playlist --dump-json 2>/dev/null
   ```
2. 展示搜索结果表格（标题、频道、时长、观看数、URL）
3. 通过 AskUserQuestion 让用户选择要分析的视频（可多选）
4. 将选中的视频 URL 通过 `source_add(source_type=youtube, url=...)` 添加到 NotebookLM

**Web 模式：**
1. 若 defuddle 可用，先提取内容：`defuddle parse <url> --md`
2. 通过 `source_add(source_type=url, url=...)` 添加到 NotebookLM
3. 若 defuddle 失败或不可用，降级为 `source_add(source_type=url, url=<url>)` 让 NotebookLM 直接处理

**Text 模式：**
1. 直接通过 `source_add(source_type=text, text=...)` 添加到 NotebookLM

**File 模式：**
1. 通过 `source_add(source_type=file, file_path=...)` 添加到 NotebookLM

---

### 阶段 3：NotebookLM 分析 / Analysis

1. 若未指定 `--notebook`，创建新 notebook：
   ```
   notebook_create(title="Research: <主题> - <YYYY-MM-DD>")
   ```
2. 添加来源后执行分析：

   **默认（快速）模式：**
   ```
   notebook_query(notebook_id, query="<分析问题>")
   ```
   默认分析问题："请全面总结这些内容的核心观点、关键发现和实用建议。按主题组织，提供具体的要点和例子。"

   **深度模式（`--deep` 标志）：**
   ```
   research_start(notebook_id, topic="<主题>", mode="deep")
   ```
   然后轮询 `research_status(notebook_id)` 直到完成（约 5 分钟）。每次轮询间隔 30 秒，持续报告进度。

---

### 阶段 4：交付物生成（可选）/ Deliverable

若用户指定了 `--deliverable`：
1. 调用 `studio_create(notebook_id, artifact_type=<type>)`
2. 轮询 `studio_status(notebook_id)` 直到完成
3. 使用 `download_artifact(notebook_id, artifact_type=<type>)` 下载结果

---

### 阶段 5：写入 Obsidian / Write to Obsidian

**目标目录：** `<vault_path>/<output_dir>/`

**文件名：** `YYYY-MM-DD <主题>.md`

**冲突处理（Append-on-conflict）：**
若同名文件已存在（同一天、同一主题），不覆盖，改为在文件末尾追加：
```markdown
---

<!-- appended: YYYY-MM-DD HH:MM -->

## 补充分析 / Supplementary Analysis

<新的 NotebookLM 分析内容>
```

**新文件内容格式：**
```markdown
---
date: YYYY-MM-DD
topic: <主题>
source_type: youtube|web|pdf|text
notebook_id: <notebook_id>
tags:
  - research
  - <相关标签>
status: complete
---

# <主题>

> 来源：<来源描述> | 分析引擎：NotebookLM

## 摘要 / Summary

<一段话概括>

## 关键发现 / Key Findings

- 发现 1
- 发现 2
- ...

## 深入分析 / Analysis

<NotebookLM 的详细分析内容>

## 来源列表 / Sources

- <来源1>
- <来源2>

## 相关链接 / Links

- NotebookLM notebook: <notebook_url>
```

---

### 阶段 6：完成提示 / Completion

Pipeline 完成后输出：

```
✅ 研究完成！结果已保存到：
   <vault_path>/<output_dir>/YYYY-MM-DD <主题>.md

💡 建议：运行 /evolve-claude-md 基于近期研究更新 CLAUDE.md，闭合飞轮循环。
```

---

## 错误处理 / Error Handling

| 错误 | 处理方式 |
|------|---------|
| `yt-dlp` 未安装 | 停止并提示 `brew install yt-dlp` |
| `defuddle` 未安装 | 降级，直接传 URL 给 NotebookLM |
| NotebookLM 认证过期 | 提示运行 `nlm login` |
| Notebook 来源超过 50 | 提示创建新 notebook 或清理旧来源 |
| 配置文件缺失 | 停止并提示运行 `/revolve-setup` |
| 目标文件已存在 | 追加新分析，不覆盖 |

---

## 参考 / References

- [NotebookLM MCP 工具速查](references/notebooklm-tools.md)
- `/yt-search` — YouTube 搜索
- `/revolve-setup` — 初始化配置向导
- `/evolve-claude-md` — 基于研究更新 CLAUDE.md（飞轮 R11）
