# 写作规格速览（对标最初 SML 提示）

以下约束来自你最初的 SML 提示（`deep_learning_paper_and_code_blog_generic`），并结合当前 workflow 做了两点增强：
1) 插图必须使用裁剪后的 Figure/Table（不允许整页 PDF）。  
2) 期刊指标（JCR IF/分区 + 中科院分区）优先从本地表格库查询。

## 目标读者
- 有深度学习常识，但不熟悉该垂直领域与这篇工作。
- 希望通过一篇中文博客搞清楚：做什么、为什么这样做、如何落地到训练/推理/评估。
- 喜欢聊天式讲清楚，而不是学术报告式复述。

## 输入信号
- `paper_text`: 论文正文文本（来自 `paper/paper_text.txt`）。
- `code_analysis_text`: 代码解读/仓库上下文（来自 `code/repo_context.md` 等）。
- `paper_images`: 论文图片（在本工作流中对应 `paper/front_matter/` 与 `paper/figures/`）。

## 输出要求
- 语言：中文（简体）。
- 标题：首行单独成行，格式固定为 `【文献阅读】| {模型/方法名}：一句话主线总结`。
- 字数：建议 5000-7000 字，默认 6000 左右。完稿后可用 `scripts/check_article_length.py` 做字数校验。
- 交付前：用 `scripts/check_article_requirements.py` 卡住硬性约束，并按 `references/self_review.md` 做一轮“讲明白/讲清楚”的润色。
- 允许少量代码片段或公式，但要克制：能用自然语言解释就不要堆符号。

## 结构与语气
- 全文以自然段为主，列表只在需要强调要点时使用。
- 章节层级建议不超过二级标题；避免“输入阶段/编码阶段/投影阶段”这类机械分段。
- 技术术语可保留英文（Transformer/diffusion/domain adaptation），并紧跟一句中文解释。
- 严禁无依据猜测（尤其是作者动机、未来工作）。

## 图片规则（强制）
- 插图必须是裁剪后的 Figure/Table：只允许引用 `paper/figures/` 与 `paper/front_matter/`。
- 禁止把整页渲染图（`paper/pages/page_00X.png`）插入正文。
- 写作时可以先用本地相对路径，完稿后运行：
  - `scripts/sync_lsky_images.py` 自动上传到 Lsky 并把链接替换成 URL。
- 若图片信息不足以支撑结论，必须明确写“仅从图中无法确定/论文未说明”，不要脑补。

## 期刊指标（JCR + 中科院分区）
- 影响因子/分区/Top/Open Access 等字段，优先从本地 DB 查询：
  - DB 文件：`references/journal_metrics_2025.sqlite3`
  - 查询脚本：`scripts/query_journal_metrics.py`
- 第一原则：只写能从输入/本地表格库中查到且可核验的信息。

## 参考文献
- 末尾必须有“参考文献”小节，按 `[1]`, `[2]` 编号。
- 第 1 条必须是本次论文（从 `paper_text`/`paper_meta` 抽取），不要凭空补全作者或年份。
- 其他引用只收录“输入中明确出现且可定位”的 DOI/arXiv/URL。
