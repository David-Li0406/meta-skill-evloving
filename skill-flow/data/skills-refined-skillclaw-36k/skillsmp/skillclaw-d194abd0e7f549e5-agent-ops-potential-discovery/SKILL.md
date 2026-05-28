---
name: agent-ops-potential-discovery
description: Use this skill when you need to analyze incoming content (text, files, folders, URLs) to extract its purpose, create summaries, and identify potential value for your current project.
---

# Potential Discovery Workflow

## Purpose

Perform deep analysis of incoming content to:
1. Extract and understand its core purpose.
2. Create extensive, structured summaries.
3. Identify potential value and applications for the current project.
4. Suggest concrete integration opportunities or inspired improvements.

## When to Use

- Evaluating a new library, tool, or framework.
- Reviewing incoming code contributions or PRs.
- Analyzing competitor products or similar solutions.
- Assessing documentation, specs, or RFCs.
- Exploring repositories for reusable patterns.
- Reviewing articles, blog posts, or research papers.

## Input Types

| Type   | Description                                   | Example                               |
|--------|-----------------------------------------------|---------------------------------------|
| **Text** | Raw text, markdown, documentation            | Pasted README, spec doc               |
| **File** | Single file analysis                          | `analyze: ./incoming/proposal.md`     |
| **Folder** | Directory tree analysis                     | `analyze: ./incoming/new-library/`    |
| **URL** | Web content (requires fetch capability)      | `analyze: https://github.com/user/repo` |

## Procedure

### Phase 1: Content Ingestion

1. **Identify content type** (text/file/folder/URL).
2. **Load content**:
   - Text: Use directly.
   - File: Read file contents.
   - Folder: Scan structure, read key files (README, package.json, etc.).
   - URL: Fetch content (if MCP fetch available) or note for manual review.
3. **Assess scope**: Estimate content size and complexity.

### Phase 2: Purpose Extraction

Analyze content to identify:

| Aspect            | Questions to Answer                                           |
|-------------------|-------------------------------------------------------------|
| **Core Purpose**  | What problem does this solve? What is its primary function? |
| **Target Audience** | Who is this for? What skill level?                       |
| **Key Features**  | What are the main capabilities?                             |
| **Architecture**  | How is it structured? What patterns does it use?          |
| **Dependencies**  | What does it rely on? What ecosystem?                     |
| **Maturity**      | How stable/complete is it? Active development?             |

**Output format:**
```markdown
### Purpose Analysis

**Core Purpose:** {one-sentence summary}

**Problem Solved:** {what pain point it addresses}

**Target Audience:** {who would use this}

**Key Features:** {list of key features}
```