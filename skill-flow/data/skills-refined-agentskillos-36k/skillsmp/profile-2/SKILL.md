---
name: profile
description: 指定したコードの実行速度をプロファイリングし、ボトルネックを特定する
---

# Profile Code

This skill helps find performance bottlenecks in the code.

## Instructions

1.  **Identify Target**:
    *   Ask user for the script or function call to profile.

2.  **Run Profiler**:
    *   **Simple Timer**: For quick checks, wrap code in `time.perf_counter()`.
    *   **cProfile**: Run `python -m cProfile -s cumulative <script_name.py>`.
    *   **Line Profiler**: If detailed line-by-line analysis is needed, suggesting adding `@profile` decorator and running `kernprof -l -v <script_name.py>` (requires `line_profiler` installed).

3.  **Analyze Output**:
    *   Look for functions with high `cumtime` (cumulative time).
    *   Look for functions with high call counts (`ncalls`).

4.  **Report**:
    *   Summarize which parts of the code are consuming the most time.
    *   Suggest potential optimizations (vectorization, caching, algorithm change).
