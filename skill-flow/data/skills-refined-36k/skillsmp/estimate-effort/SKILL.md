---
name: estimate_effort
description: 作業計画から必要な時間とLLMクオータ（トークン消費量）の見積もりを算出し、コストパフォーマンスを評価する
---

# Estimate Effort

This skill analyzes a proposed implementation plan or task description to estimate the time required for completion and the approximate LLM quota consumption.

## Instructions

1. **Task Decomposition**:
    * Break down the task into phases such as "Research", "Implementation", "Testing", and "Refactoring".
    * Assess the difficulty of each phase (Low / Medium / High).

2. **Time Estimation**:
    * Estimate the total time (in minutes) required for the assistant.
    * **LLM-Native Benchmarks**:
        * **Detailed Plan Boost**: If the input Markdown plan specifies method names, logic, and tests, assume implementation is 10-20x faster than human equivalent (e.g., 4 hours -> 15 mins).
        * **Ambiguity Penalty**: Clear requirements = 10-20 mins. Vague research tasks = 30-60 mins.
        * **Test Loop**: Assume pytest-driven debugging is near-instantaneous.
    * Use "Wall-clock time" (actual AI thinking/execution time) for the estimate.

3. **Quota Estimation**:
    * Predict token consumption based on the following criteria:
        * **High**: Large-scale file edits, many tool calls (`run_command`, `replace_file_content`), or long context reads. Note: High Quota != Long Time.
        * **Medium**: Targeted fixes, standard unit tests.
        * **Low**: Information retrieval only, simple renaming.
    * Account for model-specific behavior (e.g., Claude Opus is "Heavy", Gemini Flash is "Light").

4. **Efficiency Evaluation**:
    * Evaluate the Return on Investment (ROI) by comparing predicted results with costs (time/quota).
    * Propose "lower-cost alternative approaches" if necessary.

5. **Reporting**:
    * Generate an estimation report in the following format:
        * **Estimated Total Time**: XX minutes
        * **Estimated Quota Consumption**: [Low / Medium / High]
        * **Breakdown**: Estimates per step
        * **Concerns**: Uncertain elements that could cause significant time/quota overruns.
