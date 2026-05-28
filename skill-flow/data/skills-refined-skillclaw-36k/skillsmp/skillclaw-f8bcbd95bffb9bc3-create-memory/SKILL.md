---
name: create-memory
description: Use this skill to store important information, decisions, implementations, or learnings to the knowledge base during active work sessions for future reference.
---

# Store to Knowledge Base Memory

## Overview
Quickly stores important information, decisions, implementations, or learnings to the knowledge base during active work sessions. Use this when you want to preserve context, decisions, or outputs for future reference.

## ⚠️ CRITICAL: Knowledge Base Integration

**This uses the native knowledge base:**
- Files are stored as markdown in `~/.{platform}/knowledge/memory/`
- **Global knowledge base**: Accessible across ALL workspaces and projects
- Automatically indexed and searchable via `/search` from any workspace
- No manual indexing needed - the system handles it automatically
- Search and list functionality comes from core features

## What This Does
Stores knowledge entries during active sessions:
- Implementation details and approaches
- Technical decisions and rationale
- Debugging solutions and findings
- Architecture choices
- Code patterns and conventions
- Lessons learned
- Important outputs or results

## File Locations
Knowledge is stored in:
- **Knowledge Base**: `~/.{platform}/knowledge/memory/{project}/{YYYY}/{MM}/{topic}.md`
- **Index**: `~/.{platform}/knowledge/memory/index.md`

## Parameters
- **topic** (required): Topic name (e.g., "architecture", "debugging", "api-design", "implementation")
- **project** (optional): Project name (defaults to current workspace name)

**Note**: Content can come from:
- Direct user input (what they want to store)
- Open/referenced documents (agent extracts automatically)
- URLs mentioned in the request (agent fetches and extracts)

## Workflow

### Step 1: Determine Context and Source
Identify what needs to be stored and where it comes from:
- Current project/workspace
- Topic category
- Content source (direct input, document, or URL)

**Content Sources:**
1. **Direct input**: User provides content directly
2. **Document**: User references a file path (e.g., "look at design.md")
3. **URL**: User provides a link (e.g., "store info from https://...")

**If source is provided:**
- Read the document or fetch the URL
- Extract relevant information
- Summarize key points
- Include source reference in the entry

**If not specified:**
- Project defaults to current workspace name
- Topic can be identified based on context