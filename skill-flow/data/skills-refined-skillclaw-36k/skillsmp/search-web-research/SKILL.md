---
name: search_web_research
description: Webからの情報収集、最新の技術トレンド調査、および公開ドキュメントの分析を行う
---

# Search & Web Research

Collect and analyze information through web search, URL content reading, and browser interaction.

## Guidelines and Workflow

### 1. Web Search (`search_web`)
*   **Query Optimization**: Combine specific and English searches to obtain the latest and most comprehensive information.
*   **Source Evaluation**: Prioritize official documentation (GitHub, PyPI, official wikis).

### 2. Content Examination (`read_url_content` / `browser_subagent`)
*   **Static Analysis**: Rapidly read Markdown-converted text using `read_url_content`.
*   **Dynamic Analysis**: Utilize `browser_subagent` for sites with CSR (Client Side Rendering) or those requiring interactive operation.

### 3. Summarization and Integration of Information
*   Instead of outputting collected information as-is, provide a summary tailored to the current project context on "how it can be applied."
*   Clarify citations so that users can perform follow-up verification.

## Precautions
*   Do not collect private information requiring authentication (browser tools do not share authenticated sessions).
*   Always check the freshness of information (Date) and be careful not to recommend outdated APIs or deprecated libraries.
