---
name: revolve-setup
description: This skill should be used when the user asks to "set up Revolve", "configure Revolve", or "revolve setup". Interactive wizard that detects Obsidian vault, checks dependencies, and writes configuration.
argument-hint: (no arguments)
---

# Revolve Setup Wizard

交互式配置向导，自动检测 Obsidian vault、核查依赖、写入配置文件。

---

## Step 1: 检查现有配置

```bash
cat ~/.config/revolve/config.md 2>/dev/null && echo "CONFIG_EXISTS" || echo "CONFIG_MISSING"
```

若输出 `CONFIG_EXISTS`，通过 AskUserQuestion 询问：

> 检测到 `~/.config/revolve/config.md` 已存在。是否要重新配置？(y/N)

- 回答 `n` 或直接回车 → 显示当前配置内容后退出，提示可运行 `/research-pipeline` 或 `/yt-search`
- 回答 `y` → 继续后续步骤

---

## Step 2: 检测 Obsidian Vault

依次搜索以下位置，查找包含 `.obsidian/` 子目录的文件夹：

```bash
# 搜索常见 vault 位置（深度限制为 3 层）
find ~/Documents ~/Library/Mobile\ Documents -maxdepth 3 -name ".obsidian" -type d 2>/dev/null | sed 's|/.obsidian$||'
find ~ -maxdepth 2 -name ".obsidian" -type d 2>/dev/null | sed 's|/.obsidian$||'
```

收集所有找到的路径（去重），然后：

- 若找到 **1 个**：通过 AskUserQuestion 确认：
  > 检测到 Obsidian vault：`<path>`
  > 直接使用此路径，还是输入其他路径？（直接回车确认，或输入新路径）
  
- 若找到 **多个**：通过 AskUserQuestion 列出编号让用户选择：
  > 检测到以下 Obsidian vault，请输入编号或直接输入自定义路径：
  > 1. `/path/a`
  > 2. `/path/b`
  > (输入编号 1-N 或完整路径)

- 若**未找到**：通过 AskUserQuestion 要求用户手动输入：
  > 未检测到 Obsidian vault。请输入 vault 的完整路径：

将最终路径存为 `VAULT_PATH`。

---

## Step 3: 确认 output_dir

通过 AskUserQuestion 询问：

> 请输入研究笔记的输出目录（相对于 vault 根目录，默认：`Research`）：
> 直接回车使用默认值。

将答案存为 `OUTPUT_DIR`（默认 `Research`）。

**验证**：`OUTPUT_DIR` 不得为绝对路径（不以 `/` 开头），且不得包含 `..`。若验证失败，重新询问。

---

## Step 4: 核查依赖

逐一检查以下依赖，汇总结果：

```bash
which yt-dlp 2>/dev/null && echo "OK" || echo "MISSING"
which defuddle 2>/dev/null && echo "OK" || echo "MISSING"
which python3 2>/dev/null && echo "OK" || echo "MISSING"
which fswatch 2>/dev/null && echo "OK" || echo "MISSING"
```

**输出格式示例：**

```
依赖检查结果：
  ✅ yt-dlp       已安装
  ✅ python3      已安装
  ❌ defuddle     未安装
  ❌ fswatch      未安装
```

**缺失依赖的安装指引：**

- **yt-dlp**
  - macOS: `brew install yt-dlp`
  - Linux: `pip install yt-dlp`

- **defuddle**
  - macOS/Linux: `npm install -g defuddle-cli`

- **python3**
  - macOS: `brew install python`
  - Linux: `sudo apt install python3`

- **fswatch**
  - macOS: `brew install fswatch`
  - Linux: `sudo apt install inotify-tools`（或使用 fswatch 源码编译）

---

## Step 5: 检查 NotebookLM MCP

```bash
nlm notebook_list 2>/dev/null && echo "NLM_OK" || echo "NLM_MISSING"
```

若输出 `NLM_OK`：显示 `✅ NotebookLM MCP 已连接`

若输出 `NLM_MISSING`，显示以下指引：

```
❌ NotebookLM MCP 未就绪

安装步骤：
1. 安装 nlm CLI：npm install -g notebooklm-mcp
2. 登录：nlm login
   （会打开浏览器，用 Google 账号授权）
3. 验证连接：nlm notebook_list
   （应返回你的 notebook 列表）
4. 在 Claude Code 中启用 MCP server（claude mcp add）
```

---

## Step 6: 写入配置

```bash
mkdir -p ~/.config/revolve/
```

写入 `~/.config/revolve/config.md`，内容格式如下（参照 `config.md.example`）：

```
---
vault_path: <VAULT_PATH>
output_dir: <OUTPUT_DIR>
screenshots_dir: attachments/screenshots
sync_providers: claude,codex,opencode,gemini
---

# Revolve Configuration

This file is the configuration for the Revolve plugin.

## Field Reference

- **vault_path** (required): Absolute path to your Obsidian vault root
- **output_dir** (required): Relative path within vault for research notes (must be under vault_path)
- **screenshots_dir** (optional): Relative path within vault for screenshot attachments
- **sync_providers** (optional): Comma-separated list of providers to sync. Options: claude, codex, opencode, gemini. Default: all
```

注意：
- 所有值为无引号的纯字符串（no YAML quoting）
- `sync_providers` 使用逗号分隔

---

## Step 7: 验证 output_dir 在 vault_path 下

检查 `<VAULT_PATH>/<OUTPUT_DIR>` 路径合法性：

```bash
# output_dir 不应以 / 开头（已在 Step 3 检查）
# 验证拼接后的路径逻辑上在 vault_path 内
echo "<VAULT_PATH>/<OUTPUT_DIR>" | grep -q "^<VAULT_PATH>" && echo "PATH_OK" || echo "PATH_ERROR"
```

若验证失败，提示用户检查配置并重新运行 `/revolve-setup`。

---

## Step 8: 完成

```
✅ Revolve 配置完成！

配置文件已写入：~/.config/revolve/config.md
  vault_path:  <VAULT_PATH>
  output_dir:  <OUTPUT_DIR>

后续步骤：
  • 运行 /research-pipeline 开始研究工作流
  • 运行 /yt-search 搜索并处理 YouTube 内容
```

若有缺失依赖，末尾追加提示：

```
⚠️  有 <N> 个依赖未安装，请参照上方指引完成安装后再使用相关功能。
```
