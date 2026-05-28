---
name: codebase-audit
description: Use this skill when you need to analyze a codebase for architectural complexity and identify areas of technical debt based on Ousterhout's principles.
---

# Skill body

1. **Spawn the Analysis Agent**:
   - Use the Task tool to create an `ousterhout-codebase-review` agent with the subagent type set to "ousterhout-codebase-review".

2. **Specify the Scope**:
   - Pass any specific directories or portions of the codebase that the user mentions for targeted analysis.

3. **Analysis Focus Areas**:
   The agent will evaluate the codebase for the following systemic complexity issues:
   - **Module Depth Assessment**: Determine if modules genuinely hide complexity or merely relocate it.
   - **Leaky Abstractions**: Identify any implementation details that are exposed to callers.
   - **Consistency Issues**: Look for complexity hotspots and areas where changes require modifications across multiple files.
   - **Layer Quality and Abstraction Boundaries**: Assess if the abstraction boundaries are well-defined and if complexity is appropriately managed.
   - **Signs of Tactical vs Strategic Programming**: Evaluate if the code reflects short-term fixes rather than long-term architectural planning.

4. **Output**:
   - The agent will provide a summary of findings, a module depth assessment table, and a prioritized list of issues to address.

5. **Review Ousterhout's Principles**:
   - Familiarize yourself with John Ousterhout's principles from "A Philosophy of Software Design" to better understand the evaluation criteria:
     - Module Depth
     - Information Hiding
     - Pull Complexity Downward
     - Change Amplification
     - Cognitive Load
     - Interface Design

By following these steps, you can effectively audit a codebase and identify areas for improvement based on established software design principles.