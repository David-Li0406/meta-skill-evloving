---
name: project-workflow
description: Use this skill when you need to manage a project from planning through to archiving, ensuring all tasks are documented and skills are updated.
---

# Skill body

## Instructions

1. **Requirement Understanding and Decomposition**:
    * Read and interpret chat requests or provided plans (Markdown), breaking them down into specific work steps.
    * Identify classes, methods, and test items that require implementation.

2. **AI Assistant Strategy Formulation**:
    * Call the following skills in order to analyze task characteristics:
        * `suggest_model`: Propose the optimal LLM based on task difficulty.
        * `suggest_skill`: Propose auxiliary skills to be used during development.
        * `estimate_effort`: Predict the required time and quota consumption.

3. **Creation of Work Plan**:
    * Create or update a timestamped detailed plan (`.md`) in the `docs/developers/plans/` directory.
    * Include the following sections:
        * **Objectives & Goals**
        * **Detailed Roadmap (by Phase)**
        * **Testing & Verification Plan**
        * **Models, Recommended Skills, and Effort Estimates**

4. **Execution of Tasks**:
    * Implement the tasks as per the created plan, documenting progress and any changes made.

5. **Create Work Report**:
    * After completing the tasks, provide a detailed summary of what was implemented, including modified/added files, executed tests, resolved bugs, and performance improvements.
    * Include metadata such as the LLM model(s) used and the actual time taken.

6. **Save the Report**:
    * Save to the `docs/developers/reports/` directory with a timestamped filename (e.g., `report_TaskName_YYYYMMDD_HHMMSS.md`).
    * Notify the user of the saved path.

7. **Knowledge Extraction and Skillification**:
    * Reflect on any "reusable patterns," "unique design philosophies," or "pitfalls to watch out for" discovered during the work.
    * Add new skills to `.agent/skills/` and categorize them.
    * Update existing skills if they require additional notes.

8. **Suggest Continuation or Conclusion**:
    * Report the completion of archiving to the user and suggest whether to proceed to the next task or terminate the current session.