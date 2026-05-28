---
name: manage-pr-comments
description: Use this skill when you need to handle unresolved comments on GitHub pull requests, either by retrieving them for planning fixes or resolving them automatically.
---

# Skill body

## Instructions

Follow these steps to manage unresolved comments on GitHub pull requests.

### Step 1: Retrieve Unresolved PR Comments

To get unresolved review comments from a pull request, run the following command:

```
bash /プラグインルートパス/skills/manage-pr-comments/scripts/read-unresolved-pr-comments.sh
```

### Step 2: Create a Fix Plan

Based on the retrieved unresolved comments, create a fix plan by following these steps:

- Use the Explore sub-agent to analyze the content of the unresolved comments.
- Use the Plan sub-agent to formulate a specific fix plan.

### Step 3: Resolve PR Comments

To automatically resolve unresolved review threads, execute the following command:

```
bash /プラグインルートパス/skills/manage-pr-comments/scripts/resolve-pr-comments.sh
```

This command will resolve all unresolved review threads using the GraphQL API and display the results of each resolution. Note that issue comments (from the conversation tab) are not included in this process.