<div align="center" id="readme-top">

<!-- BANNER: 替换为你的 banner 图片 -->
![Revolve Banner][banner]

[![License][license-badge]][license]
[![Claude Code][claude-badge]][claude-code]
[![Plugin][plugin-badge]][install-url]

**Claude Code 自进化 AI 研究架构**

通过 NotebookLM 研究主题，存储到 Obsidian，从积累的经验中持续进化 CLAUDE.md。

[快速开始][quick-start] •
[Skill 参考][skills-ref] •
[同步脚本][sync-section] •
[配置][config-section]

[![English][lang-en-badge]][lang-en]
[![简体中文][lang-zh-badge]][lang-zh]

</div>

<br>

<details open>
<summary><kbd>目录</kbd></summary>

- [工作原理][how-it-works]
- [前置依赖][prerequisites]
- [安装][installation]
- [快速开始][quick-start]
- [Skill 参考][skills-ref]
- [同步脚本][sync-section]
- [模板][templates-section]
- [配置][config-section]
- [配套工具][built-with]
- [致谢][acknowledgments]
- [参与贡献][contributing]
- [许可证][license-section]

</details>

<br>

## 工作原理

<!-- DIAGRAM: 替换为你的飞轮架构图 -->
![飞轮架构图][flywheel-diagram]

```
采集                 分析               存储              进化
────────────         ──────────         ───────           ──────────────
YouTube / Web   →    NotebookLM    →    Obsidian    →    CLAUDE.md    →  更智能的 AI
PDF / 文本           (免费 Google AI)   （你的 vault）    （仅追加）        └── 循环
```

每次研究会话都会反哺你的 AI——让下一次会话更智能。飞轮可通过 Revolve 的进化 Skill 自动闭合，也可手动回顾笔记后更新 CLAUDE.md。

<div align="right">

[![][back-to-top]][readme-top]

</div>

## 前置依赖

| 依赖 | 是否必需 | 安装方式 |
|------|----------|---------|
| [Claude Code][claude-code] | 必需 | — |
| [Obsidian][obsidian] vault | 必需 | — |
| NotebookLM MCP server | 必需 | `pipx install notebooklm-mcp-cli` 然后 `nlm login` |
| yt-dlp | 必需（YouTube 功能） | `brew install yt-dlp` 或 `pip install yt-dlp` |
| defuddle | 可选 | `npm install -g @nicekate/defuddle` |
| Python 3.8+ | 必需（同步脚本） | macOS 预装 |
| fswatch | 可选（自动同步） | `brew install fswatch` |

<div align="right">

[![][back-to-top]][readme-top]

</div>

## 安装

```bash
claude plugin marketplace add https://github.com/eisen0419/revolve
claude plugin install revolve
```

<div align="right">

[![][back-to-top]][readme-top]

</div>

## 快速开始

```bash
# 1. 配置 vault 路径并检查依赖
/revolve-setup

# 2. 搜索 YouTube 相关内容
/yt-search "Claude Code tips"

# 3. 完整研究流水线 → NotebookLM 分析 → 写入 Obsidian 笔记
/research-pipeline youtube "AI productivity"

# 4. 从积累的经验中进化 CLAUDE.md
/evolve-claude-md
```

前置依赖已安装时不超过 10 分钟；从零开始不超过 60 分钟。

<div align="right">

[![][back-to-top]][readme-top]

</div>

## Skill 参考

| Skill | 说明 | 示例 |
|-------|------|------|
| `/revolve-setup` | 交互式向导——配置 vault、检查依赖 | `/revolve-setup` |
| `/yt-search` | 通过 yt-dlp 搜索 YouTube | `/yt-search "Claude Code skills"` |
| `/research-pipeline` | 采集 → NotebookLM 分析 → 写入 Obsidian 笔记 | `/research-pipeline youtube "AI agents"` |
| `/evolve-claude-md` | 扫描对话和笔记，将发现追加至 CLAUDE.md | `/evolve-claude-md --days 7` |

<div align="right">

[![][back-to-top]][readme-top]

</div>

## 同步脚本

独立 Python 脚本，将 AI 对话转换为带图片提取功能的 Obsidian Markdown 笔记。

| 提供商 | 格式 | 支持内容 |
|--------|------|---------|
| Claude | `.jsonl` | 完整对话 |
| Codex | sessions `.jsonl` | 完整对话 |
| OpenCode | `prompt-history.jsonl` | 仅提示词 |
| Gemini | `session-*.json` | 完整对话 |

支持单次同步和通过 launchd 自动同步。

详见 [`scripts/README.md`][sync-docs] 获取安装和使用说明。

<div align="right">

[![][back-to-top]][readme-top]

</div>

## 模板

将 `templates/` 目录下的模板复制到你 vault 的模板文件夹：

- **`research-note.md`** — 带 frontmatter 的结构化笔记（日期、主题、来源类型、标签）
- **`research-index.md`** — 基于 Dataview 的跨研究笔记动态索引

<div align="right">

[![][back-to-top]][readme-top]

</div>

## 配置

运行 `/revolve-setup` 自动生成配置，或将 `config.md.example` 复制到 `~/.config/revolve/config.md`。

| 字段 | 是否必需 | 说明 |
|------|----------|------|
| `vault_path` | 必需 | Obsidian vault 的绝对路径 |
| `output_dir` | 必需 | vault 内研究笔记的相对路径 |
| `screenshots_dir` | 可选 | 截图附件的相对路径 |
| `sync_providers` | 可选 | 逗号分隔：`claude,codex,opencode,gemini` |

完整 schema：[`docs/config-contract.md`][config-contract]

<div align="right">

[![][back-to-top]][readme-top]

</div>

## 配套工具

| 工具 | 状态 | 额外能力 |
|------|------|---------|
| 独立使用 | 可用 | 所有 Skill 无需其他插件即可运行 |
| [Compound Engineering][ce-plugin] | 增强 | `/ce:plan`、`/ce:work`、`/ce:review`、`/ce:compound` |
| [Forge][forge-repo] | 增强 | CLAUDE.md 工作流方法论模板 |

<div align="right">

[![][back-to-top]][readme-top]

</div>

## Built With

Revolve 站在以下项目的肩膀上：

| 项目 | 说明 | 在 Revolve 中的角色 |
|------|------|-------------------|
| [Claude Code][claude-code] | Anthropic 的 AI 编程 CLI | 运行时——所有 Skill 在 Claude Code 会话中执行 |
| [NotebookLM][notebooklm] | Google 免费 AI 研究与分析工具 | 分析引擎——将 YouTube、网页、PDF 来源处理为结构化发现 |
| [notebooklm-mcp][nlm-mcp] | 连接 Claude Code 与 NotebookLM 的 MCP server | 集成层——让 Skill 能以编程方式调用 NotebookLM |
| [Obsidian][obsidian] | 本地优先的 Markdown 知识库 | 存储层——研究笔记和同步对话的归宿 |
| [yt-dlp][ytdlp] | YouTube 元数据提取 CLI | 数据采集——搜索 YouTube 并获取视频元数据 |
| [defuddle][defuddle] | 网页转干净 Markdown 提取器 | 数据采集——将网页剥离为干净的文章文本 |
| [Compound Engineering][ce-plugin] | Kieran Klaassen / Every 出品的 AI 驱动开发工作流插件 | 工作流增强——提供 `/ce:plan`、`/ce:work`、`/ce:review` |
| [Dataview][dataview] | 支持 SQL 式笔记查询的 Obsidian 插件 | 用于研究索引模板的动态笔记列表 |
| [Templater][templater] | Obsidian 模板引擎 | 用于研究笔记模板的变量替换 |

<div align="right">

[![][back-to-top]][readme-top]

</div>

## Acknowledgments

- [Kieran Klaassen](https://github.com/kieranklaassen) 和 [Every](https://every.to) — 感谢 [Compound Engineering][ce-plugin]，其插件框架和工作流方法论启发了 Revolve 的架构设计
- [Google NotebookLM](https://notebooklm.google.com) 团队 — 感谢提供免费且强大的 AI 研究工具，让飞轮成为可能
- [notebooklm-mcp](https://github.com/sinjab/notebooklm-mcp) 贡献者 — 感谢将 NotebookLM 桥接到 MCP 生态
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) 维护者 — 感谢提供最可靠的 YouTube 元数据提取工具
- [Obsidian](https://obsidian.md) 团队 — 感谢构建了串联整个飞轮的知识库
- [Anthropic](https://anthropic.com) — 感谢 Claude Code 和让这一切成为可能的插件系统
- [Best-README-Template](https://github.com/othneildrew/Best-README-Template) — README 结构灵感来源

<div align="right">

[![][back-to-top]][readme-top]

</div>

## 参与贡献

欢迎提交 Issue、功能请求和 PR。

<div align="right">

[![][back-to-top]][readme-top]

</div>

## 许可证

[MIT][license]

<!-- 导航 -->
[readme-top]: #readme-top
[how-it-works]: #工作原理
[prerequisites]: #前置依赖
[installation]: #安装
[quick-start]: #快速开始
[skills-ref]: #skill-参考
[sync-section]: #同步脚本
[templates-section]: #模板
[config-section]: #配置
[built-with]: #built-with
[acknowledgments]: #acknowledgments
[contributing]: #参与贡献
[license-section]: #许可证

<!-- 图片 — 替换为你的实际图片 URL -->
[banner]: images/banner.jpg
[flywheel-diagram]: images/flywheel.jpg
[back-to-top]: https://img.shields.io/badge/-回到顶部-gray?style=flat-square

<!-- Badges -->
[license-badge]: https://img.shields.io/badge/License-MIT-blue?style=flat-square
[claude-badge]: https://img.shields.io/badge/Claude_Code-Plugin-7C3AED?style=flat-square&logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cGF0aCBkPSJNMTIgMkM2LjQ4IDIgMiA2LjQ4IDIgMTJzNC40OCAxMCAxMCAxMCAxMC00LjQ4IDEwLTEwUzE3LjUyIDIgMTIgMnoiIGZpbGw9IndoaXRlIi8+PC9zdmc+
[plugin-badge]: https://img.shields.io/badge/Install-Plugin-14B8A6?style=flat-square
[lang-en-badge]: https://img.shields.io/badge/English-lightgrey?style=flat-square
[lang-zh-badge]: https://img.shields.io/badge/简体中文-lightgrey?style=flat-square

<!-- 链接 -->
[license]: LICENSE
[claude-code]: https://claude.ai/code
[notebooklm]: https://notebooklm.google.com
[nlm-mcp]: https://github.com/sinjab/notebooklm-mcp
[obsidian]: https://obsidian.md
[ytdlp]: https://github.com/yt-dlp/yt-dlp
[defuddle]: https://github.com/nicekate/defuddle
[install-url]: https://github.com/eisen0419/revolve
[lang-en]: README.md
[lang-zh]: README_CN.md
[sync-docs]: scripts/README.md
[config-contract]: docs/config-contract.md
[ce-plugin]: https://github.com/EveryInc/compound-engineering-plugin
[dataview]: https://github.com/blacksmithgu/obsidian-dataview
[templater]: https://github.com/SilentVoid13/Templater
[forge-repo]: https://github.com/eisen0419/forge
