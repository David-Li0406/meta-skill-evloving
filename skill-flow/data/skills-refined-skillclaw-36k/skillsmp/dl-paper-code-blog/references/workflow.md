# 从论文+代码到博客文章：端到端流程

这套流程面向你当前的标准化素材包（`paper/` + `code/` + `materials_manifest.json`），目标是产出一篇可发布的中文长文博客，并把插图上传到 Lsky 后自动回填 URL。

## Phase 0：入场检查（先确认素材齐全）

1. 打开 `materials_manifest.json`，记录：
   - 论文信息：venue、published_date、doi（以及 ISSN/eISSN 如果有）。
   - repo 快照：commit hash（用于在文中注明版本）。
2. 确认目录是否存在：
   - `paper/`（含 `paper_text.txt`, `figures/`, `figures_manifest.json`, `front_matter/` 等）
   - `code/`（含 `repo_context.md`）
   - `article_scaffold.md`
   - `.lsky_upload_cache.json`（没有也没关系，后续脚本会创建）
3. 把 `assets/article_scaffold_template.md` 复制到项目根目录（或覆盖已有 `article_scaffold.md`），作为“读论文时的工作笔记”。

## Phase 0.5：补全期刊指标（JCR + 中科院分区）

文章元信息里的影响因子、分区、Top 等字段，优先用本地表格查询，而不是凭记忆或网上检索。

1. 确认 skill 内的指标库存在：
   - `references/journal_metrics_2025.sqlite3`
2. 若需要更新（例如 Excel 表更新了），在任意目录运行：
   - `python C:\\Users\\ciheb\\.codex\\skills\\dl-paper-code-blog\\scripts\\build_journal_metrics_db.py --overwrite`
3. 查询并把结果填进元信息块：
   - `python C:\\Users\\ciheb\\.codex\\skills\\dl-paper-code-blog\\scripts\\query_journal_metrics.py --journal \"Advanced Science\"`
   - 取返回 JSON 的 `best.jcr`（JIF/Quartile）和 `best.cas`（分区/Top/Open Access）。

## Phase 1：读论文（抓主线 + 证据点）

1. 用 `paper/paper_text.txt` 快速扫一遍，锚定：
   - 问题定义：输入/输出/约束/成功标准。
   - 方法主线：3-4 个关键设计转折。
   - 实验：数据集、指标、关键结果、消融/边界。
2. 用 `paper/figures_manifest.json` 挑图：
   - 优先选择 method overview + 关键实验结果（4-6 张图足够）。
   - 不要用 `paper/pages/` 整页图来当插图（见 Phase 3 的强制规则）。
3. 把证据写进 `article_scaffold.md`，每条都标注来源（论文哪一节/哪张图）。

## Phase 1.5：读代码（抓可复现路径 + 关键默认值）

1. 打开 `code/repo_context.md`，整理：
   - 训练/推理/评估的入口脚本与配置文件（描述即可，不必贴满路径清单）。
   - 数据下载、环境依赖、常见坑（对读者更有价值）。
2. 明确“论文写的” vs “代码实现”的差异点，把它们提前记入 `article_scaffold.md` 的差异清单。

## Phase 2：填满脚手架（把 TODO 全部替换掉）

你应该在写正文前，把 `article_scaffold.md` 的每个 TODO 都填成：
- 一两句话结论 + 证据来源（paper_text/figure/README/代码模块）。

这一阶段做得扎实，后面写稿会非常快。

## Phase 3：写正文（先本地路径，后自动回填 URL）

强制要求：
- 正文里插入的图片必须来自 `paper/figures/` 或 `paper/front_matter/`，不允许直接插入 `paper/pages/` 整页图。

写作建议：
1. 按 `references/blog_outline.md` 的结构写 `*_blog.md`/`blog.md`。
2. 插图先用本地相对路径写入，例如：
   - `【图1：论文封面】![](paper/front_matter/page1_header.png)`
   - `【图2：方法总览】![](paper/figures/fig_01_p002_dpi220.png)`
3. 完稿后运行自动上传与替换脚本：
   - `python C:\\Users\\ciheb\\.codex\\skills\\dl-paper-code-blog\\scripts\\sync_lsky_images.py --workspace <项目目录> --markdown <blog.md>`
   - 脚本会使用 `lsky-uploader` 上传缺失图片，并把 Markdown 中的本地路径替换成 Lsky URL，同时更新 `.lsky_upload_cache.json`。

## Phase 3.5：自检与润色（讲明白 / 讲清楚）

建议把这一阶段当成“发布前 QA 的第一部分”：先用脚本把硬性约束卡住，再做一轮面向读者的润色。

推荐顺序：
1. 结构/禁忌项先查一遍（不强制 URL，便于先改结构）：
   - `python C:\\Users\\ciheb\\.codex\\skills\\dl-paper-code-blog\\scripts\\check_article_requirements.py <blog.md>`
2. 如果图片仍是本地路径，先上传并回填 URL：
   - `python C:\\Users\\ciheb\\.codex\\skills\\dl-paper-code-blog\\scripts\\sync_lsky_images.py --workspace <项目目录> --markdown <blog.md>`
3. 再跑一次硬性检查（要求全部 https URL）：
   - `python C:\\Users\\ciheb\\.codex\\skills\\dl-paper-code-blog\\scripts\\check_article_requirements.py <blog.md> --require-urls`
4. 字数守护（目标 5000-7000 非空白字符）：
   - `python C:\\Users\\ciheb\\.codex\\skills\\dl-paper-code-blog\\scripts\\check_article_length.py <blog.md> --min 5000 --max 7000`
5. 对照清单做“讲明白/讲清楚”润色：
   - `C:\\Users\\ciheb\\.codex\\skills\\dl-paper-code-blog\\references\\self_review.md`

## Phase 4：交付前 QA

- 图像：Markdown 中不应再出现 `paper/pages/`，并且所有插图都应是可访问的 https URL。
- 指标：影响因子与中科院分区来自本地 DB 查询结果（可在正文里注明来源为 JCR/CAS 2025 表）。
- 结构：运行 `python C:\\Users\\ciheb\\.codex\\skills\\dl-paper-code-blog\\scripts\\check_article_requirements.py <blog.md> --require-urls`，确保标题/元信息/参考文献齐全、无整页图、图片均为 URL。
- 字数：运行 `python C:\\Users\\ciheb\\.codex\\skills\\dl-paper-code-blog\\scripts\\check_article_length.py <blog.md> --min 5000 --max 7000`，确保非空白字符数在 5000-7000 之间；超出范围则回到正文做一次增补/压缩。
- 可复现性：至少给出一条“最短复现路径”和 5-10 个关键开关（配置/阈值/步数/采样策略等）。
- 交付文件（项目根目录）：
  - `article_scaffold.md`（已填满）
  - `*_blog.md` 或 `blog.md`（最终稿）
  - `.lsky_upload_cache.json`（如有上传）
  - 可选：`salad_blog_assets/images/`（本地图包）

如果遇到素材缺失（repo 不全、PDF 无法解析、图没裁出来等），把阻塞写在文章开头并明确“无法从当前输入确认”。
