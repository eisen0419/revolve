# NotebookLM MCP 工具速查 / Tool Reference

## 笔记本管理 / Notebook Management

- `notebook_create(title)` — 创建笔记本
- `notebook_list()` — 列出所有笔记本
- `notebook_get(notebook_id)` — 获取笔记本详情
- `notebook_rename(notebook_id, title)` — 重命名笔记本
- `notebook_delete(notebook_id)` — 删除笔记本（需 confirm=True）
- `notebook_describe(notebook_id)` — 获取笔记本描述与摘要

## 来源管理 / Source Management

- `source_add(notebook_id, source_type, ...)` — 添加来源
  - `source_type=youtube, url=<视频URL>`
  - `source_type=url, url=<网页URL>`
  - `source_type=text, text=<文本内容>`
  - `source_type=file, file_path=<文件路径>`
- `source_describe(notebook_id, source_id)` — 获取来源摘要
- `source_get_content(notebook_id, source_id)` — 获取来源全文
- `source_rename(notebook_id, source_id, title)` — 重命名来源
- `source_delete(notebook_id, source_id)` — 删除来源（需 confirm=True）

## 查询与分析 / Query & Analysis

- `notebook_query(notebook_id, query)` — 快速查询已有来源（推荐，秒级响应）
- `notebook_query(notebook_id, query, conversation_id)` — 多轮对话
- `research_start(notebook_id, topic, mode="deep")` — 深度研究（约 5 分钟，需 `--deep` 标志）
- `research_status(notebook_id)` — 深度研究进度（轮询间隔 30 秒）
- `research_import(notebook_id, research_id)` — 将深度研究结果导入笔记本
- `cross_notebook_query(notebook_ids, query)` — 跨笔记本查询

## 批处理 / Batch Operations

- `batch(operations)` — 批量执行多个操作（合并 API 调用）

## 交付物 / Studio Artifacts

- `studio_create(notebook_id, artifact_type)` — 创建交付物（异步）
  - artifact_type: `audio` / `video` / `infographic` / `slide_deck` / `report` / `quiz`
- `studio_status(notebook_id)` — 轮询生成进度
- `studio_revise(notebook_id, instructions)` — 修改已有交付物
- `studio_delete(notebook_id, artifact_type)` — 删除交付物
- `download_artifact(notebook_id, artifact_type)` — 下载交付物
- `export_artifact(notebook_id, artifact_type, path)` — 导出交付物到本地

## 笔记 / Notes

- `note(notebook_id, content, action)` — 创建/列出/更新/删除笔记
  - action: `create` / `list` / `update` / `delete`

## 共享 / Sharing

- `notebook_share_public(notebook_id)` — 设为公开
- `notebook_share_invite(notebook_id, emails)` — 邀请协作
- `notebook_share_batch(notebook_id, invites)` — 批量邀请
- `notebook_share_status(notebook_id)` — 查看共享状态

## 认证 / Auth

- `refresh_auth()` — 刷新认证 token
- `save_auth_tokens(tokens)` — 手动保存 token（CLI 失败时备用）
- `server_info()` — 查看服务器状态与认证信息

## 注意事项 / Notes

- 认证过期时运行 `nlm login`（推荐）或 `nlm login switch <profile>` 切换账号
- 每个 notebook 最多 50 个来源
- `studio_create` 是异步的，需用 `studio_status` 轮询，完成后再调用 `download_artifact`
- `confirm` 参数：先设 `false` 预览效果，用户确认后设 `true` 执行
- 深度研究（`research_start`）约需 5 分钟，适合复杂主题；简单查询用 `notebook_query` 更快
