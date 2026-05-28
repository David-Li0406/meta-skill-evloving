---
name: create-summary
description: Use this skill to generate comprehensive work summaries from daily notes or conversation context for performance reviews, project retrospectives, or documenting completed work with timeline and impact.
---

# Generate Work Summary

## Overview
Creates a comprehensive summary of work completed on a plan or project, including timeline, accomplishments, and impact. Summaries can be generated from daily notes or conversation context.

## ⚠️ CRITICAL REQUIREMENT: Preserve Existing Content

**When working with summary files:**
1. ALWAYS read the existing file first before making changes.
2. NEVER overwrite unrelated content.
3. APPEND new summaries if the file already contains other data.
4. Preserve all existing sections and metadata.
5. Add clear separators between different summaries.

## What This Generates
A structured work summary document with:
- Project overview and context
- Timeline of key milestones
- Detailed accomplishments
- Business and technical impact
- Challenges and solutions
- Links to related resources

## File Locations
Summaries are saved to:
- **Knowledge Base**: `~/.{cli}/knowledge/summary/{YYYY}/`
- **Year Index**: `~/.{cli}/knowledge/summary/{YYYY}/index.md`

## Parameters
- **project** (required): Project or feature name (e.g., "user-authentication", "api-optimization").
- **date** (optional): Date or date range for this work (defaults to today).
- **from_notes** (optional): Set to "true" to generate summary from daily notes instead of conversation context.

## Workflow

### Step 1: Gather Context
Collect information about the work completed.

**From Notes (when from_notes=true):**
- Search for notes in `~/workplace/LimonoctNvim/src/LimonoctNvim/notes/journal`.
- Filter notes by date range (if provided) or search for project mentions.
- Extract relevant work items, accomplishments, and decisions.
- Keep track of note file paths for linking.
- Look for patterns: completed tasks, decisions made, problems solved.

**From Conversation Context (when from_notes=false):**
- Review current conversation context.
- Identify key accomplishments and deliverables.
- Note any code reviews, deployments, or milestones.
- Capture technical decisions and their rationale.
- Look for references to plans, tickets, MCMs.

### Step 2: Check for Existing Summary File
**CRITICAL**: Before creating or updating a summary:
1. **Check if the file exists** and read its content.
2. If it exists, follow the preservation guidelines outlined above.