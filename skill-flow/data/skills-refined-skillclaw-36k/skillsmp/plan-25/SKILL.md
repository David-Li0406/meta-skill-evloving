---
name: plan
description: Activates the Project Manager to break down a feature request into tasks. Use when planning new features or organizing work.
argument-hint: "[feature request or project to plan]"
---

# Plan Feature

Break down a feature request into actionable tasks.

1. **Analyze Request**: Read the user's feature request provided in the argument.

2. **Act as Project Manager**:
    * Load the `project-manager` agent persona.
    * Analyze the request to identify the prompt purpose, scope, and key components.
    * Create a plan structure:
        * Create an Epic task for the feature.
        * Create subtasks for Design, Implementation, and Testing.
        * Identify dependencies between tasks.

3. **Report**: List the created tasks and the next actionable item.
