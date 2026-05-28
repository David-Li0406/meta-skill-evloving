---
name: codebase-investigation
description: Use this skill when planning or designing features to understand the current state of a codebase, verify assumptions, and find existing patterns, ensuring decisions are grounded in reality.
---

# Codebase Investigation

## Overview

This skill provides a systematic approach to investigating a codebase, helping to verify assumptions and understand existing patterns before making design decisions. It prevents missteps by grounding plans in the actual structure and content of the codebase.

## When to Use

**Use for:**
- Verifying design assumptions before implementation (e.g., "Does auth.ts exist?")
- Understanding current architecture and patterns (e.g., "How do we handle API errors?")
- Locating features or code (e.g., "Where is user authentication implemented?")
- Confirming the existence of components or functions (e.g., "Does feature X exist?")
- Preventing hallucination about file paths and structure

**Don't use for:**
- Information available in external documentation (use internet research)
- Questions answered by reading specific known files (use Read directly)
- General programming questions not specific to this codebase

## Core Investigation Workflow

1. **State the Investigation Goal**
   - Clearly define the question or assumption you are investigating.
   - Explain why you need this information and what you expect to find.

2. **Fingerprint the Project**
   - Identify the project type by checking key files (e.g., `package.json` for Node.js, `pyproject.toml` for Python).

3. **Map the Structure**
   - Scan the directory layout to understand the architecture and purpose of different folders (e.g., `src/` for source code, `tests/` for test files).

4. **Find Entry Points**
   - Locate where execution begins to clarify how different components connect.

5. **Use Multiple Search Strategies**
   - Employ various methods such as glob patterns, grep keywords, and reading files to gather information.

6. **Follow Traces**
   - Investigate imports, references, and component relationships to understand how the codebase operates.

7. **Verify Assumptions**
   - For each assumption, search for supporting and contradicting evidence, then weigh the findings to render a verdict.

8. **Report Findings**
   - Clearly communicate your findings, indicating confirmed assumptions, discrepancies, additions, or missing elements.

## Quick Reference

| Task | Strategy |
|------|----------|
| **Where is X?** | Use glob patterns or search tools |
| **How is Y done?** | Investigate related components and patterns |

**Why this matters:** This structured approach ensures that implementation plans are based on accurate understanding of the codebase, reducing the risk of errors and misalignment with existing code.