---
name: update-project-brief
description: This skill should be used when the user wants to update the project brief with current high-level strategic project information. It maintains the overview, tech stack, architectural decisions, and key commands documentation.
allowed-tools: Bash(bun:*), Read(**/package.json), Edit(memory-bank/project-brief.md), Write(memory-bank/project-brief.md)
---

# Project Brief Updater

Your task is to update the project brief with current high-level strategic information.

## Reference Documents

Review these files to understand the expected format and current state:

1. **Current project brief**: @memory-bank/project-brief.md
2. **Document map** (for reference only - do NOT duplicate its content): @document-map.md

## Project Brief Structure

The project brief should be concise (~60-120 lines) with four sections:

### 1. Overview

- What this project is and its purpose
- Who uses it and how
- Core use cases (2-4 sentences)

### 2. Tech Stack

- Programming languages
- Runtime environment
- Key libraries and frameworks
- Build tools

### 3. Key Architectural Decisions

- 0-10 most important architectural choices
- Each decision should explain WHAT and WHY
- Focus on non-obvious decisions that shape the codebase
- Avoid implementation details

### 4. Key Commands

- Most important commands for working with the project
- Group by category: Installation, Build, Test, Deploy, Utilities, etc.
- Only include commands an AI would actually run
- Brief descriptions for each command

## Instructions

1. Read the existing project brief at @memory-bank/project-brief.md
2. **Optional**: Review project configuration files to identify tech stack changes
3. **Optional**: Review build scripts to identify key commands
4. Update the project brief, maintaining the four-section structure
5. Keep it strategic and high-level - do NOT include:
   - Directory trees or file paths (that's in document-map.md)
   - Line counts or file sizes
   - Detailed installation procedures
   - Implementation details of specific components

## Important Distinctions

**Project Brief** (this file):

- Strategic overview
- High-level architecture
- Tech stack and key decisions
- Important commands

**Document Map** (document-map.md):

- Tactical navigation
- File locations and purposes
- When to read specific files
- Code structure details

Do NOT duplicate information from the document map. Keep the project brief focused on WHY and HOW the project is architected, not WHERE things are located.
