---
name: archive_work
description: 作業完了後にタイムスタンプをつけて報告書を作成・保存し、必要に応じてエージェントスキルを追加・更新する
---

# Archive Work Workflow

This skill ensures that once a series of tasks are completed, the results are recorded (report creation) and knowledge is solidified (skill updates) simultaneously.

## Instructions

1. **Create Work Report**:
    * Provide a detailed summary of what was implemented during this conversation (or series of tasks).
    * Include modified/added files, executed tests, resolved bugs, and performance improvements.
    * Include metadata such as the LLM model(s) used and the actual time taken.

2. **Save the Report**:
    * Save to the `docs/developers/reports/` directory with a timestamped filename (e.g., `report_TaskName_YYYYMMDD_HHMMSS.md`).
    * Notify the user of the saved path.

3. **Knowledge Extraction and Skillification (`learn_skill` / `refactor_skills`)**:
    * Reflect on whether any "reusable patterns," "unique design philosophies," or "pitfalls to watch out for" were discovered during the work.
    * Add new skills to `.agent/skills/` and categorize them (refer to `index.md`).
    * Update existing skills if they require additional notes.

4. **Suggest Continuation or Conclusion**:
    * Report the completion of archiving to the user and suggest whether to proceed to the next task (e.g., `setup_plan` / `collaborative_design`) or terminate the current session (e.g., `git_commit` / `wrap_up`).
