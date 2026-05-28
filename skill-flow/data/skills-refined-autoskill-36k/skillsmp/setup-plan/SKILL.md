---
name: setup_plan
description: ユーザーの要求から具体的な作業計画を作成し、モデル・スキル・工数を提案して計画書を保存・更新する
---

# Setup Plan Workflow

This skill initiates a workflow that consistently handles understanding requirements, model selection, and creating/updating plans at the start of a new task.

## Instructions

1. **Requirement Understanding and Decomposition**:
    * Read and interpret chat requests or provided plans (Markdown), decomposing them into specific work steps.
    * Identify classes, methods, and test items that require implementation.

2. **AI Assistant Strategy Formulation**:
    * Call the following skills in order to analyze task characteristics:
        * `suggest_model`: Propose the optimal LLM based on task difficulty.
        * `suggest_skill`: Propose auxiliary skills to be used during development.
        * `estimate_effort`: Predict the required time and quota consumption.

3. **Creation or Update of Plan**:
    * Create or update a timestamped detailed plan (`.md`) in the `docs/developers/plans/` directory.
    * Include the following sections:
        * **Objectives & Goals**
        * **Detailed Roadmap (by Phase)**
        * **Testing & Verification Plan**
        * **Models, Recommended Skills, and Effort Estimates** (reflecting results of step 2)

4. **Await Model Selection**:
    * Present the analysis results to the user and **wait for user approval** (selection of LLM model or plan approval) before proceeding to the next step.

5. **Confirmation for Continuation**:
    * Upon obtaining approval, proceed to execute the first phase or ask for further instructions.
