---
name: conversation_report
description: 会話全体の作業レポートをタイムスタンプ付きで保存する
---

# Conversation Work Report

This skill creates a Markdown report summarizing all work done in the current conversation and saves it under `docs/developers/`.

## Instructions

1. **Collect Context**
   * Summarize all work performed in the conversation (reviews, fixes, tests, lint, docs, commits, cleanups).
   * Include major outcomes and any skipped/blocked items.

2. **Timestamp**
   * Generate a timestamp in local time using `date +%Y%m%d_%H%M%S`.
   * Include a human-readable timestamp in the report header.

3. **Save Location**
   * Save to `docs/developers/reviews/` with filename `conversation_work_report_<timestamp>.md`.

4. **Report Structure (Markdown)**
   * Title: `Conversation Work Report`
   * Timestamp line
   * Sections: `Accomplishments`, `Current Status`, `References`

5. **Confirm**
   * Tell the user the file path.
