# 图片与图床（强制裁剪版）

目标：插入到文章里的图片必须是论文中对应的 Figure/Table 的裁剪图，不允许直接插入整页 PDF 渲染图。

## 1) 选图来源（优先级）

1. `paper/front_matter/page1_header.png`：封面信息图（通常作为图 1）。
2. `paper/figures/`：论文 Figure/Table 的裁剪图（默认 220 dpi），文件名通常形如 `fig_01_*`、`tbl_01_*`。
3. 只要 `paper/figures/` 存在，就不要用 `paper/pages/`。

判定标准：
- 文章中出现的图片链接应来自 `paper/figures/` 或 `paper/front_matter/`。
- 若你发现自己需要用 `paper/pages/page_00X.png`，说明没有按 Figure 裁剪。优先回到 `paper/figures_manifest.json` 找对应 `file`，不要把整页塞进正文。

## 2) 图注与编号

- 图号按文章出现顺序从 1 递增，不需要严格对齐论文里的 Figure 编号。
- 图注建议从 `paper/figures_manifest.json` 的 `caption_text` 提取要点后，用中文重写一版。
- 表格同理，用 `【表X：...】`。

## 3) 上传并自动替换为 URL（推荐做法）

写作时正文里可以先用本地相对路径，例如：

`【图2：...】![](paper/figures/fig_01_p002_dpi220.png)`

完稿后在项目工作区执行（需要已安装 `lsky-uploader`，并设置 `LSKY_TOKEN`）：

`python C:\\Users\\ciheb\\.codex\\skills\\dl-paper-code-blog\\scripts\\sync_lsky_images.py --workspace <你的项目目录> --markdown <blog.md>`

脚本会做三件事：
1. 读取 Markdown 中所有本地图片引用（排除 http/https）。
2. 通过 `lsky-uploader` 上传缺失图片（用 `.lsky_upload_cache.json` 的 SHA256 去重）。
3. 把 Markdown 里的 `![](本地路径)` 原地替换成 `![](https://...)`。

可选：
- `LSKY_BASE_URL`：如果你的 API 地址不是默认值，可通过环境变量覆盖。
- `--album-id/--strategy-id/--permission`：需要把图片归档到特定相册或策略时使用。

## 4) 可选：本地打包图集

如果下游平台需要本地 PNG：

1. 创建/更新 `salad_blog_assets/images/`。
2. 把文章实际引用的裁剪图复制进来并顺序命名：`fig1.png`, `fig2.png`, ...
3. 不要二次压缩或缩放，避免糊图。
