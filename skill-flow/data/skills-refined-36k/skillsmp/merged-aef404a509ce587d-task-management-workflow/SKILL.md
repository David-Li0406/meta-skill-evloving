---
name: task-management-workflow
description: Use this skill when you need to create a detailed work plan and archive completed tasks with reports and skill updates.
---

# Task Management Workflow

This skill combines the processes of setting up a work plan based on user requirements and archiving completed tasks with reports and skill updates.

## Instructions

### 1. Requirement Understanding and Decomposition
- Read and interpret chat requests or provided plans (Markdown), breaking them down into specific work steps.
- Identify classes, methods, and test items that require implementation.

### 2. AI Assistant Strategy Formulation
- Analyze task characteristics by calling the following skills in order:
    - `suggest_model`: Propose the optimal LLM based on task difficulty.
    - `suggest_skill`: Propose auxiliary skills to be used during development.
    - `estimate_effort`: Predict the required time and resource consumption.

### 3. Creation or Update of Plan
- Create or update a timestamped detailed plan (`.md`) in the `docs/developers/plans/` directory, including:
    - **Objectives & Goals**
    - **Detailed Roadmap (by Phase)**
    - **Testing & Verification Plan**
    - **Models, Recommended Skills, and Effort Estimates**

### 4. Create Work Report
- After completing tasks, provide a detailed summary of what was implemented, including modified/added files, executed tests, resolved bugs, and performance improvements.
- Include metadata such as the LLM model(s) used and the actual time taken.

### 5. Save the Report
- Save the report to the `docs/developers/reports/` directory with a timestamped filename (e.g., `report_TaskName_YYYYMMDD_HHMMSS.md`).
- Notify the user of the saved path.

### 6. Knowledge Extraction and Skillification
- Reflect on any "reusable patterns," "unique design philosophies," or "pitfalls to watch out for" discovered during the work.
- Add new skills to `.agent/skills/` and categorize them, updating existing skills as necessary.

### 7. Await Model Selection
- Present the analysis results to the user and wait for user approval (selection of LLM model or plan approval) before proceeding to the next step.

### 8. Confirmation for Continuation
- Upon obtaining approval, proceed to execute the first phase or ask for further instructions.
- Report the completion of archiving to the user and suggest whether to proceed to the next task or terminate the current session.