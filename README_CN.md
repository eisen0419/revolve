# Revolve

**Claude Code 自进化 AI 研究架构**

每次研究会话都会反哺你的 AI——让下一次会话更智能。

---

## 工作原理

```
采集                 分析               存储              进化
────────────         ──────────         ───────           ──────────────
YouTube / Web   →    NotebookLM    →    Obsidian    →    CLAUDE.md    →  更智能的 AI
PDF / 文本           (免费 Google AI)   （你的 vault）    （仅追加）      │
                                                                          └── 循环
```

---

## 前置依赖

| 依赖 | 是否必需 | 安装方式 |
|------|----------|---------|
| [Claude Code](https://claude.ai/code) | 必需 | — |
| [Obsidian](https://obsidian.md) vault | 必需 | — |
| NotebookLM MCP server | 必需 | `pipx install notebooklm-mcp-cli` 然后 `nlm login` |
| yt-dlp | 必需（YouTube 功能） | `brew install yt-dlp` 或 `pip install yt-dlp` |
| defuddle | 可选 | `npm install -g @nicekate/defuddle` |
| Python 3.8+ | 必需（同步脚本） | macOS 预装 |
| fswatch | 可选（自动同步） | `brew install fswatch` |

---

## 安装

在 Revolve 上架官方市场之前，请直接安装：

```bash
claude plugin marketplace add https://github.com/nicekate/revolve
claude plugin install revolve
```

---

## 快速开始

```bash
# 1. 配置 vault 路径并检查依赖
/revolve-setup

# 2. 搜索 YouTube 相关内容
/yt-search "Claude Code tips"

# 3. 运行完整研究流水线
/research-pipeline youtube "AI productivity"

# 4. 从积累的经验中进化 CLAUDE.md
/evolve-claude-md
```

**时间估算：** 前置依赖已安装时不超过 10 分钟；从零开始不超过 60 分钟。

---

## Skill 参考

| Skill | 说明 | 示例 |
|-------|------|------|
| `/revolve-setup` | 交互式向导——配置 vault、检查依赖 | `/revolve-setup` |
| `/yt-search` | 通过 yt-dlp 搜索 YouTube，返回结构化结果 | `/yt-search "Claude Code skills"` |
| `/research-pipeline` | 完整流水线：采集 → NotebookLM 分析 → 写入 Obsidian | `/research-pipeline youtube "AI agents"` |
| `/evolve-claude-md` | 扫描对话和 vault 笔记，将发现追加至 CLAUDE.md | `/evolve-claude-md --days 7` |

---

## 同步脚本

将多个 AI 提供商的对话文件（Claude、Codex、OpenCode、Gemini）转换为 Obsidian Markdown 笔记。支持单次同步和通过 launchd 自动同步。

详见 [`scripts/README.md`](scripts/README.md)。

---

## 模板

将 `templates/` 目录下的 Obsidian 模板复制到你 vault 的模板文件夹：

- `research-note.md` — 研究流水线输出的结构化笔记
- `research-index.md` — 跨所有研究笔记的 dataview 索引

---

## 配置

将 `config.md.example` 复制到 `~/.config/revolve/config.md` 并填写你的 vault 路径，或运行 `/revolve-setup` 自动生成。

字段说明与 schema：[`docs/config-contract.md`](docs/config-contract.md)。

---

## 演示

即将推出——完整飞轮流程视频演示。

---

## 许可证

MIT
