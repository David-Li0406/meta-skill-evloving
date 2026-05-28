---
name: generate-steering
description: Use this skill to generate foundational steering documents (product.md, tech.md, structure.md) for the current workspace by analyzing the codebase, ideal for starting new projects or documenting existing ones.
---

# Generate Project Steering Documents

## Overview
This skill generates foundational steering documents for the current workspace and saves them to both local and knowledge base locations for searchability.

## ⚠️ CRITICAL REQUIREMENT: Context Section

**ALL three generated files (product.md, tech.md, structure.md) MUST:**
1. Include a Context section at the end with Timeline and Conversation Summary.
2. Have this Context section updated AUTOMATICALLY after EVERY significant interaction.
3. Updates happen WITHOUT asking for permission - just do it automatically.
4. This enables session recovery if the conversation dies.

**Update Context section automatically when:**
- Files are initially generated.
- User provides feedback or requests changes.
- Documents are updated or regenerated.
- User asks questions or provides clarifications.
- Any modifications are made to the documents.

## What This Generates
Three foundational documents:
1. **product.md** - Your app's features and business logic.
2. **structure.md** - How your codebase is organized.
3. **tech.md** - Your technology stack and conventions.

## File Locations
Documents are saved to TWO locations:
- **Workspace**: `.kiro/steering/` or `.gemini/steering/` (local to current project).
- **Knowledge Base**: `~/.kiro/knowledge/steering/{workspace-name}/` or `~/.gemini/knowledge/steering/{workspace-name}/`.

Format:
- `{workspace-name}` = name of the current workspace (e.g., my-api-service, user-dashboard).

## Workflow

### Step 1: Analyze Workspace
Gather information about the current workspace:
- Identify workspace root and name.
- Examine README files, package.json, pom.xml, build files.
- Review directory structure.
- Understand project purpose and architecture.
- Identify key technologies and dependencies.

### Step 2: Generate product.md
Create a comprehensive product document WITHOUT Context section (for local workspace):

```markdown
# Product: {Project Name}

## Purpose
[What problem does this project solve?]

## Features and Business Logic
- [Feature 1]: [Description and business value]
- [Feature 2]: [Description and business value]
- [Feature 3]: [Description and business value]

## Goals
- [Primary goal 1]
- [Primary goal 2]
- [Primary goal 3]

## Target Users
[Who uses this project?]

## Business Value
[Why does this project matter?]
```