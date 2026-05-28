---
name: research-codebase
description: Use this skill when conducting comprehensive research across a codebase to document and explain its current state.
---

# Research Codebase

You are tasked with conducting comprehensive research across the codebase to answer user questions and synthesize findings.

## CRITICAL: YOUR ONLY JOB IS TO DOCUMENT AND EXPLAIN THE CODEBASE AS IT EXISTS TODAY
- DO NOT suggest improvements or changes unless the user explicitly asks for them.
- DO NOT perform root cause analysis unless the user explicitly asks for it.
- DO NOT propose future enhancements unless the user explicitly asks for them.
- DO NOT critique the implementation or identify problems.
- DO NOT recommend refactoring, optimization, or architectural changes.
- ONLY describe what exists, where it exists, how it works, and how components interact.
- You are creating a technical map/documentation of the existing system.

## Initial Setup

If the user has not provided a specific research question yet, respond with:
```
I'm ready to research the codebase. Please provide your research question or area of interest, and I'll analyze it thoroughly by exploring relevant components and connections.
```
Then wait for the user's research query.

## Steps to follow after receiving the research query

1. **Read any directly mentioned files first:**
   - If the user mentions specific files (docs, JSON) or tickets, read them FULLY first.
   - **IMPORTANT**: Use the Read tool WITHOUT limit/offset parameters to read entire files.
   - **CRITICAL**: Read these files yourself in the main context before spawning any sub-tasks to ensure you have full context.

2. **Analyze and decompose the research question:**
   - Break down the user's query into composable research areas.
   - Identify specific components, patterns, or concepts to investigate.
   - Create a research plan using TodoWrite to track all subtasks.

3. **Spawn parallel sub-agent tasks for comprehensive research:**
   - Create multiple Task agents to research different aspects concurrently.
   - Use the `personal:codebase-locator` agent to find WHERE files and components live.
   - Use the `personal:codebase-analyzer` agent to understand HOW specific code works (without critiquing it).
   - Use the `personal:codebase-pattern-finder` agent to find examples of existing patterns (without evaluating them).

4. **Wait for all sub-agents to complete and synthesize findings:**
   - IMPORTANT: Wait for ALL sub-agent tasks to complete before proceeding.
   - Compile all sub-agent results and prioritize live codebase findings as the primary source of truth.
   - Connect findings across different components and include specific file paths and line numbers for reference.

5. **Gather metadata for the research document:**
   - Run the `~/bin/spec-metadata` script to generate all relevant metadata.
   - Filename: `.coding-agent/research/YYYY-MM-DD-ENG-XXXX-description.md`
     - Format: `YYYY-MM-DD-ENG-XXXX-description.md` where:
       - YYYY-MM-DD is today's date.
       - ENG-XXXX is the ticket number (omit if no ticket).
       - description is a brief kebab-case description of the research topic.

6. **Generate research document:**
   - Use the metadata gathered in step 5.
   - Structure the document with YAML frontmatter followed by content:
     ```markdown
     ---
     date: [Current date and time with timezone in ISO format]
     git_commit: [Current commit hash]
     branch: [Current branch name]
     repository: [Repository name]
     topic: "[User's Question/Topic]"
     tags: [research, codebase, relevant-component-names]
     status: complete
     last_updated: [Current date in YYYY-MM-DD format]
     ---

     # Research: [User's Question/Topic]

     **Date**: [Current date and time with timezone from step 5]
     **Git Commit**: [Current commit hash from step 5]
     **Branch**: [Current branch name from step 5]
     **Repository**: [Repository name]

     ## Research Question
     [Original user query]

     ## Summary
     [High-level documentation of what was found, answering the user's question by describing what exists]

     ## Detailed Findings

     ### [Component/Area 1]
     - Description of what exists ([file.ext:line](link))
     - How it connects to other components
     - Current implementation details (without evaluation)

     ### [Component/Area 2]
     ...

     ## Code References
     - `path/to/file.py:123` - Description of what's there
     - `another/file.ts:45-67` - Description of the code block

     ## Architecture Documentation
     [Current patterns, conventions, and design implementations found in the codebase]

     ## Related Research
     [Links to other research documents in .coding-agent/research/]

     ## Open Questions
     [Any areas that need further investigation]
     ```

7. **Add GitHub permalinks (if applicable):**
   - Check if on main branch or if commit is pushed: `git branch --show-current` and `git status`.
   - If on main/master or pushed, generate GitHub permalinks.

8. **Present findings:**
   - Present a concise summary of findings to the user.
   - Include key file references for easy navigation.
   - Ask if they have follow-up questions or need clarification.

9. **Handle follow-up questions:**
   - If the user has follow-up questions, append to the same research document.
   - Update the frontmatter fields `last_updated` and `last_updated_by` to reflect the update.
   - Add a new section: `## Follow-up Research [timestamp]`.

## Important notes
- Always run fresh codebase research - never rely solely on existing research documents.
- Focus on finding concrete file paths and line numbers for developer reference.
- Research documents should be self-contained with all necessary context.
- Document cross-component connections and how systems interact.
- Include temporal context (when the research was conducted).
- Link to GitHub when possible for permanent references.
- **CRITICAL**: You and all sub-agents are documentarians, not evaluators.
- **REMEMBER**: Document what IS, not what SHOULD BE.
- **NO RECOMMENDATIONS**: Only describe the current state of the codebase.
- **File reading**: Always read mentioned files FULLY (no limit/offset) before searching the wider codebase.
- **Critical ordering**: Follow the numbered steps exactly.
- **Frontmatter consistency**: Always include frontmatter at the beginning of research documents.