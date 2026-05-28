---
name: cook
description: Activates the Shopify Developer to immediately start coding, refactoring, or building features. Use when ready to implement code changes.
argument-hint: "[feature or task to implement]"
disable-model-invocation: true
---

# Cook - Start Coding

Immediately begin active development work.

1. **Assess Context**: Review the latest user request and the `task.md` file to determine the immediate coding objective.

2. **Act as Shopify Developer**:
   - Load the `shopify-developer` agent persona.
   - Leverage skills like `shopify-remix-template`, `shopify-api`, and `typescript`.

3. **Enter Execution Mode**: Call the `task_boundary` tool with `Mode="EXECUTION"` to signal the start of active development. Set a descriptive `TaskName` (e.g., "Implementing [Feature]", "Refactoring [Component]").

4. **Execute Changes**:
   - Inspect necessary files using `view_file` or `view_file_outline`.
   - Apply code changes using `replace_file_content`, `multi_replace_file_content`, or `write_to_file`.
   - Focus on producing working, high-quality code that meets the design aesthetics (if UI) and functional requirements.

5. **Verify**: Run relevant tests or build steps to ensure the code works as expected.
