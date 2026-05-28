---
tags: 30_Resources
---
# Instruction Authoring Guidelines

When populating the `Instructions` section of a new skill's `SKILL.md`, follow these guidelines to ensuring the skill is reliable and easy for Claude to use.

## Core Principles

1.  **Clear & Sequential**: Write instructions as a numbered list of steps.
    *   *Bad*: "Run the script and then maybe check the output."
    *   *Good*: 
        1. Run `python scripts/analyze.py input.txt`.
        2. Read the output file `results.json`.

2.  **Concrete Examples**: Always provide code blocks showing exact command usage.
    ```bash
    python scripts/my_script.py --verbose
    ```

3.  **Input/Output Specifications**: Clearly state what the script expects and what it produces.
    *   "The script takes a CSV file path as an argument."
    *   "It outputs a JSON summary to stdout."

4.  **Handling Edge Cases**: Briefly mention what to do if things go wrong, although the script itself should handle most errors (following "Solve, don't punt").
    *   "If the API is down, the script will return a 503 error code. Retry once after 5 seconds."

5.  **Distinguish Execution vs. Reference**:
    *   Use **Execute** for utility scripts (most common).
    *   Use **Read** only if Claude needs to understand the *logic* inside the file (rare).

## Formatting

*   Use Markdown headers (H3, H4) to structure long instructions.
*   Use `code blocks` for file paths, variable names, and commands.
*   Keep the main instruction body concise (< 500 lines). Move detailed reference tables or large examples to the `references/` directory.

## Example Structure

```markdown
## Instructions

To process a dataset:

1. **Prepare Data**: Ensure your data is in CSV format.
2. **Run Analysis**: 
   ```bash
   python scripts/analyze_data.py --input "data.csv" --output "summary.json"
   ```
3. **Interpret Results**:
   - The script outputs a JSON file.
   - Key fields: `total_revenue`, `growth_rate`.
```
