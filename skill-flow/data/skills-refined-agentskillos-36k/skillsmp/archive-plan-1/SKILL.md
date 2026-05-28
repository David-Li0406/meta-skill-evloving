---
name: archive_plan
description: 実装計画（implementation_plan.md）を日本語に翻訳し、モデル選定・リソース管理戦略を含めた正式な計画書として docs/developers/plans/ に保存する
---

# Archive Plan

This skill takes the current `implementation_plan.md` (English), translates it into Japanese, and saves it as a formalized plan in `docs/developers/plans/` with a timestamp and additional metadata (recommended model and quota strategy).

## Instructions

1. **Read Implementation Plan**:
    * Locate and read the current `implementation_plan.md` from the artifact directory.

2. **Collect Metadata**:
    * Ensure `suggest_model` and `recover_quota` have been performed.
    * Summarize the recommended model and its rationale.
    * Summarize the quota management strategy (context compression, batching, etc.).

3. **Translate and Format**:
    * Translate the content of `implementation_plan.md` into Japanese.
    * Include a new section `使用モデルとリソース最適化` with the metadata collected above.
    * Add a timestamped title like `# [Goal] 計画書 (YYYY-MM-DD HH:MM:SS)`.

4. **Determine Save Path**:
    * Generate a timestamp string (e.g., `20260121_093243`).
    * Set the save path to `docs/developers/plans/<description>_plan_<timestamp>.md`.

5. **Save and Notify**:
    * Write the content to the file.
    * Inform the user of the saved path.
