---
name: recover_quota
description: LLMのクオータ（利用制限）を管理・節約し、効率的に回復・継続するための戦略を実行する
---

# Recover Quota

This skill is used when LLM usage limits (quota) become tight or when you want to manage quota efficiently to continue work. While it cannot physically reset the quota, it supports "recovery" and "continuity" by optimizing token consumption and adjusting work strategies.

## Instructions

1. **Context Analysis**:
    * Check current token consumption and context bloat.
    * Evaluate if large-scale searches or reading long files are occurring frequently.

2. **Efficiency Strategies**:
    * **Switch Models**: Use `suggest_model` to consider switching to a lower-cost model.
    * **Compress Context**: Organize and remove unnecessary history or logs to include only essential information in the prompt.
    * **Consolidate Requests**: Avoid fragmented commands; group multiple related tasks into a single prompt.

3. **Cooldown Procedures**:
    * **Wait**: Pause low-priority tasks to wait for natural quota recovery over time.
    * **Local Execution**: Prioritize tasks that don't rely on the LLM, such as running local tests or checking documentation.

4. **Optimization**:
    * Use the `wrap_up` skill to clean up the session so the next session can resume with minimal context.
