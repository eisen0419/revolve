---
name: evolve-claude-md
description: "This skill should be used when the user asks to 'evolve CLAUDE.md', 'update CLAUDE.md from experience', or 'self-evolve'. Scans conversations and notes to extract actionable findings and appends them to CLAUDE.md."
argument-hint: "[--days <N>]"
---

# CLAUDE.md 自进化（双层数据源）

从两个数据层提取进化信号，以仅追加模式更新 CLAUDE.md。

**核心原则：绝不修改 CLAUDE.md 中已有的任何内容——只在末尾追加。**

## 数据架构

```
进化层（AI 专用）                    阅读层（人类友好）
~/.claude/projects/**/*.jsonl        <vault_path>/**/*.md
├── 工具调用序列                      ├── 研究笔记
├── 错误 & 重试记录                   ├── 工作日志
├── Skill 调用 & 效果                 ├── 项目文档
├── 文件操作 patterns                 └── 对话摘要
└── 决策过程原始数据
         ↓                                    ↓
    ┌─────────────────────────────────────────────┐
    │        /evolve-claude-md                     │
    │   交叉分析 → 提取新发现 → 用户审批 → 追加    │
    └─────────────────────────────────────────────┘
```

## 用法

```
/evolve-claude-md              # 扫描最近 7 天
/evolve-claude-md --days 30    # 扫描最近 30 天
/evolve-claude-md --days 1     # 仅扫描今天
```

## 执行流程

### 阶段 0：读取配置

执行开始时，读取 `~/.config/revolve/config.md`，提取 frontmatter 中的配置值：

```bash
# 检查配置文件是否存在
test -f ~/.config/revolve/config.md
```

用 `Read ~/.config/revolve/config.md` 读取文件，从 `---` 之间的 YAML frontmatter 解析：

| 字段 | 用途 |
|------|------|
| `vault_path` | Obsidian vault 根目录（必需） |
| `output_dir` | vault 内的笔记目录（可选，用于过滤扫描范围） |

**如果配置文件不存在：** 输出以下提示并退出：

```
⚠️  Revolve config not found at ~/.config/revolve/config.md
Run /revolve-setup to configure your vault path and other settings.
```

将解析得到的 `vault_path` 用于后续阶段 1B 的扫描。

默认 `--days` 为 7，若用户传入参数则覆盖。

### 阶段 0.5：幂等性检查

读取目标 CLAUDE.md 文件（通常是 `~/.claude/CLAUDE.md` 或当前项目的 `CLAUDE.md`），检查是否已有今天日期的进化条目：

```python
import datetime
today = datetime.date.today().isoformat()  # e.g. "2026-04-02"
# 检查 CLAUDE.md 中是否包含 f"## {today} 进化"
```

**如果今天的条目已存在：** 用 AskUserQuestion 询问用户：

```
⚠️  今天（YYYY-MM-DD）的进化记录已存在于 CLAUDE.md 中。
是否继续并追加新条目？
- 继续追加
- 跳过（不做修改）
```

若用户选择跳过，直接退出。

### 阶段 1：双层扫描

**1A. 进化层：扫描原始 .jsonl**

获取最近 N 天修改的会话文件：

```bash
find ~/.claude/projects -name "*.jsonl" -mtime -<N> -type f 2>/dev/null
```

对每个 .jsonl 文件，**先估算大小再读取**：

```bash
# 先估行数，避免 token 超限
wc -l <file.jsonl>
```

逐行解析 JSON，**只提取以下行类型**，跳过 assistant 的长文本输出：

| 信号类型 | JSON 特征 | 提取什么 |
|---------|----------|---------|
| **工具调用** | `type: "tool_use"`, `name: "Bash"/"Read"/"Edit"/...` | 高频工具组合、常用命令 patterns |
| **工具结果** | `type: "tool_result"` | 成功/失败比、错误类型分布 |
| **错误 & 重试** | 连续相似的 tool_use（同名工具、相似参数） | 什么操作需要多次尝试、最终怎么解决的 |
| **Skill 调用** | user content 中包含 `Base directory for this skill:` | 哪些 skill 被频繁使用、哪些从不用 |
| **文件操作** | `name: "Edit"/"Write"`, `file_path` 参数 | 哪些目录/文件被频繁修改 |
| **MCP 调用** | `name` 以 `mcp__` 开头 | MCP 工具使用频率和 patterns |
| **用户纠正** | user message 紧跟在 assistant 之后，含否定词（"不对"、"别"、"不要"、"错了"、"no"、"don't"、"wrong"） | 什么情况下 AI 犯错、用户怎么纠正 |

**提取方式**（用 python3 内联脚本或 subagent 处理）：

```python
# 核心提取逻辑伪代码（只处理关键行类型）
KEEP_TYPES = {"tool_use", "tool_result", "user"}

for each jsonl:
    tool_calls = []       # (tool_name, key_params)
    errors = []           # (tool_name, error_text)
    retries = []          # (tool_name, attempt_count, final_outcome)
    skills_used = []      # skill_name
    corrections = []      # (user_correction_text, context)
    mcp_calls = []        # (mcp_tool, params_summary)

    for line in jsonl:
        d = json.loads(line)
        if d.get("type") not in KEEP_TYPES:
            continue       # 跳过 assistant 长文本，节省 token
        # ... 按上表分类提取
```

**1B. 阅读层：扫描 Obsidian 笔记**

使用阶段 0 读取的 `vault_path`，应用相同的 `--days N` 时间窗口扫描 .md 文件：

```bash
find "<vault_path>" -name "*.md" -mtime -<N> -type f \
  ! -path "*/.obsidian/*" \
  ! -path "*/.smart-env/*" \
  ! -path "*/Templates/*" \
  ! -path "*/.trash/*" \
  2>/dev/null
```

> **注意：** `-mtime -N` 时间窗口同样应用于 vault 扫描，防止大型 vault 导致 context window 耗尽。

如果两层都没有新数据，输出"近 N 天无新活动，无需进化。"并退出。

### 阶段 2：交叉分析与提取

将两层数据交叉分析，提取以下 6 个类别的新发现：

| 类别 | 数据来源 | 寻找什么 | 示例 |
|------|---------|---------|------|
| **工具 Patterns** | .jsonl 工具调用 | 高频工具组合、偏好的命令写法 | "用户习惯用 `yt-dlp --flat-playlist --dump-json` 搜索 YouTube" |
| **错误 & 恢复** | .jsonl 错误+重试 | 反复出现的错误类型、有效的恢复策略 | "NotebookLM 认证过期时 `nlm login` 即可恢复" |
| **Skill 使用** | .jsonl skill 调用 | 高频 skill、从不使用的 skill、skill 组合 | "`/research-pipeline` 后通常跟 `/evolve-claude-md`" |
| **工作偏好** | Obsidian 笔记 | 输出格式、分析方法、交互风格 | "用户偏好用表格对比方案而非纯文本" |
| **用户纠正** | .jsonl 纠正信号 | AI 犯错的 pattern、用户期望的正确行为 | "用户纠正：不要在没有用户确认的情况下自动 commit" |
| **新知识** | Obsidian 研究笔记 | 新工具、新概念、新工作流 | "Chase AI 的内容瀑布流 skill 可以一鱼多吃" |

**分析策略：**

- 用 subagent 并行处理：一个扫描 .jsonl（进化层），一个扫描 Obsidian（阅读层）
- 对 .jsonl 的大文件，只读取 tool_use/tool_result/user 类型的行，跳过 assistant 的长文本输出
- 交叉验证：如果 .jsonl 显示某个操作被反复重试，检查 Obsidian 中是否已有相关教训

**过滤规则：**
- 只提取有**跨 session 复用价值**的发现
- 如果发现已存在于 CLAUDE.md 中（包括进化日志），跳过
- 如果发现只在特定项目有意义（如某个 API key 格式），跳过
- 如果纠正是一次性的误解而非系统性问题，跳过
- 每次进化最多提取 5-10 条发现，保持精简
- 优先级：用户纠正 > 错误恢复 > 工具 patterns > 工作偏好 > 新知识

### 阶段 3：生成 Diff 预览

将提取的发现格式化为 CLAUDE.md 追加内容，展示给用户：

```markdown
# 进化日志

## YYYY-MM-DD 进化

基于近 N 天的 X 个会话（.jsonl）+ Y 篇笔记分析。

**新发现：**
- [错误恢复] Obsidian MCP patch_content 只能定位一级标题，子标题用 Edit 工具直接编辑
- [工具 Pattern] yt-dlp 搜索用 `ytsearch<N>:<query> --flat-playlist --dump-json` 最高效
- [用户纠正] 不要在没有用户确认的情况下自动 commit
- [Skill 使用] /research-pipeline 完成后建议 /evolve-claude-md 形成闭环
- [工作偏好] 分析对比类问题优先用 Markdown 表格呈现
```

使用 AskUserQuestion 展示预览并请求确认：
- **确认追加** — 将内容追加到 CLAUDE.md 末尾
- **编辑后追加** — 让用户修改后再追加
- **放弃** — 不做任何修改

### 阶段 4：安全追加

确认后，将内容追加到 CLAUDE.md 文件末尾。

**安全规则（Append-Only Invariant）：**
1. 读取当前 CLAUDE.md 完整内容，记录总行数 L
2. 检查是否已有 `# 进化日志` 章节
   - 已有：在该章节末尾追加新的日期条目
   - 没有：在文件末尾新增 `# 进化日志` 章节
3. 使用 Edit 工具追加，确保不修改任何已有内容
4. 追加完成后验证：前 L 行内容不变

**绝不修改 `# 进化日志` 以上的任何内容。**

### 阶段 5：完成报告

```
✅ CLAUDE.md 进化完成！

数据源：
  进化层：X 个会话 (.jsonl)，提取 A 次工具调用 / B 个错误 / C 次纠正
  阅读层：Y 篇笔记 (.md)，来自 vault: <vault_path>

新增发现：K 条
  - 错误恢复: n1 条
  - 工具 Pattern: n2 条
  - 用户纠正: n3 条
  - Skill 使用: n4 条
  - 工作偏好: n5 条
  - 新知识: n6 条

追加位置：CLAUDE.md # 进化日志 > YYYY-MM-DD 进化
原有内容（L 行）未修改 ✅
```

## 与 /research-pipeline 的协作

当 `/research-pipeline` 完成后会建议运行本 skill。推荐工作流：

```
1. /research-pipeline youtube "某个话题"     # 研究并存储到 Obsidian
2. ... 继续日常工作，积累更多笔记 ...
3. /evolve-claude-md                         # 定期进化（双层扫描）
```

## 注意事项

- 绝不修改 `# 进化日志` 以上的任何内容
- 每条进化记录带日期戳和数据源统计，便于追溯
- 建议频率：每周或每月运行一次
- .jsonl 文件可能很大（几 MB）——先用 `wc -l` 估算行数，再分段处理；只读取 tool_use/tool_result/user 类型的行，跳过 assistant 长文本
- vault 扫描同样受 `--days N` 限制，防止大型 vault 撑爆 context window
- 如果近期无有价值的新 patterns，提示"已扫描但未发现新的进化信号"
- 用户纠正类发现优先级最高——这是最直接的改进信号
- 配置从 `~/.config/revolve/config.md` 运行时读取，修改配置后无需重启 Claude Code
