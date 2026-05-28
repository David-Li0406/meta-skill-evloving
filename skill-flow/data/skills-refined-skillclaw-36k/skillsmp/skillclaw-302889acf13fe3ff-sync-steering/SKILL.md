---
name: sync-steering
description: Use this skill to sync existing steering documents from the local workspace to the knowledge base, ensuring they include updated Context sections for searchability and session recovery.
---

# Sync Steering Documents to Knowledge Base

## Overview
This skill syncs existing steering documents from the local workspace to the knowledge base, adding Context sections for searchability and session recovery. Use this when steering documents already exist in the designated steering directory and need to be synced to the knowledge base.

## ⚠️ CRITICAL REQUIREMENT: Context Section

**ALL synced files MUST:**
1. Include a Context section at the end (in knowledge base copy only).
2. Have this Context section updated AUTOMATICALLY after EVERY significant interaction.
3. Updates happen WITHOUT asking for permission - just do it automatically.
4. This enables session recovery if the conversation dies.

**Update Context section automatically when:**
- Files are initially synced.
- User provides feedback or requests changes.
- Documents are updated or regenerated.
- User asks questions or provides clarifications.
- Any modifications are made to the documents.

## What This Syncs
Any steering documents from the local workspace:
- **product.md** - Your app's features and business logic.
- **tech.md** - Your technology stack and conventions.
- **structure.md** - How your codebase is organized.
- **Any other .md files** in the steering directory.

## File Locations
Documents are synced FROM and TO:
- **Source (Workspace)**: `.kiro/steering/` or `.gemini/steering/` (local to current project).
- **Destination (Knowledge Base)**: `~/.kiro/knowledge/steering/{workspace-name}/` or `~/.gemini/knowledge/steering/{workspace-name}/`.

Format:
- `{workspace-name}` = name of the current workspace (e.g., my-api-service, user-dashboard).

## Workflow

### Step 1: Identify Workspace
Gather information about the current workspace:
- Identify workspace root and name.
- Locate the steering directory.
- List all steering documents present.

### Step 2: Check Existing Steering Documents
Scan the steering directory for existing documents:
- List all `.md` files.
- Verify content is present.
- Identify which files need syncing.

### Step 3: Automatic Sync to Knowledge Base
**CRITICAL**: This happens AUTOMATICALLY without asking for permission.

For each steering file found:
1. **Read content** from the local workspace file.
2. **Add Context section** at the end (if not already present).
3. **Save to knowledge base**: `~/.kiro/knowledge/steering/{workspace-name}/` or `~/.gemini/knowledge/steering/{workspace-name}/`.