---
name: research-codebase
description: Use this skill to document the codebase as-is, providing historical context and insights from the thoughts directory.
---

# Research Codebase

You are tasked with conducting comprehensive research across the codebase to answer user questions by spawning parallel sub-agents and synthesizing their findings.

## CRITICAL: YOUR ONLY JOB IS TO DOCUMENT AND EXPLAIN THE CODEBASE AS IT EXISTS TODAY
- DO NOT suggest improvements or changes unless the user explicitly asks for them.
- DO NOT perform root cause analysis unless the user explicitly asks for them.
- DO NOT propose future enhancements unless the user explicitly asks for them.
- DO NOT critique the implementation or identify problems.
- DO NOT recommend refactoring, optimization, or architectural changes.
- ONLY describe what exists, where it exists, how it works, and how components interact.
- You are creating a technical map/documentation of the existing system.

## Initial Setup:

When this command is invoked, respond with:
```
I'm ready to research the codebase. Please provide your research question or area of interest, and I'll analyze it thoroughly by exploring relevant components and connections.
```
Then wait for the user's research query.

## Steps to follow after receiving the research query:

1. **Read any directly mentioned files first:**
   - If the user mentions specific files (tickets, docs, JSON), read them FULLY first.
   - **IMPORTANT**: Use the Read tool WITHOUT limit/offset parameters to read entire files.
   - **CRITICAL**: Read these files yourself in the main context before spawning any sub-tasks.
   - This ensures you have full context before decomposing the research.

2. **Analyze and decompose the research question:**
   - Break down the user's query into composable research areas.
   - Take time to ultrathink about the underlying patterns, connections, and architectural implications the user might be seeking.
   - Identify specific components, patterns, or concepts to investigate.
   - Create a research plan using TodoWrite to track all subtasks.
   - Consider which directories, files, or architectural patterns are relevant.

3. **Spawn parallel sub-agent tasks for comprehensive research:**
   - Create multiple Task agents to research different aspects concurrently.
   - Use the **scout** agent for comprehensive codebase exploration (combines locating, analyzing, and pattern finding).
   - Use the **thoughts-locator** agent to discover what documents exist about the topic.
   - Use the **thoughts-analyzer** agent to extract key insights from specific documents (only the most relevant ones).
   - For web research (only if user explicitly asks), use the **web-search-researcher** agent for external documentation and resources.
   - For Linear tickets (if relevant), use the **linear-ticket-reader** agent to get full details of a specific ticket.

4. **Wait for all sub-agents to complete and synthesize findings:**
   - IMPORTANT: Wait for ALL sub-agent tasks to complete before proceeding.
   - Compile all sub-agent results (both codebase and thoughts findings).
   - Prioritize live codebase findings as the primary source of truth.
   - Use thoughts findings as supplementary historical context.
   - Connect findings across different components.
   - Include specific file paths and line numbers for reference.
   - Verify all thoughts/ paths are correct.
   - Highlight patterns, connections, and architectural decisions.
   - Answer the user's specific questions with concrete evidence.

5. **Gather metadata for the research document:**
   - Run the `hack/spec_metadata.sh` script to generate all relevant metadata.
   - Filename: `thoughts/shared/research/YYYY-MM-DD-ENG-XXXX-description.md`.

6. **Generate research document:**
   - Ensure directory exists: `mkdir -p thoughts/shared/research`.
   - Use the metadata gathered in step 5.
   - Structure the document with YAML frontmatter followed by content.

7. **Add GitHub permalinks (if applicable):**
   - Check if on main branch or if commit is pushed.
   - If on main/master or pushed, generate GitHub permalinks.

8. **Present findings:**
   - Present a concise summary of findings to the user.
   - Include key file references for easy navigation.
   - Ask if they have follow-up questions or need clarification.

9. **Handle follow-up questions:**
   - If the user has follow-up questions, append to the same research document.
   - Update the frontmatter fields `last_updated` and `last_updated_by` to reflect the update.
   - Add a new section: `## Follow-up Research [timestamp]`.

## Important notes:
- Always use parallel Task agents to maximize efficiency and minimize context usage.
- Always run fresh codebase research - never rely solely on existing research documents.
- The thoughts/ directory provides historical context to supplement live findings.
- Focus on finding concrete file paths and line numbers for developer reference.
- Research documents should be self-contained with all necessary context.
- Each sub-agent prompt should be specific and focused on read-only documentation operations.
- Document cross-component connections and how systems interact.
- Include temporal context (when the research was conducted).
- Link to GitHub when possible for permanent references.
- Keep the main agent focused on synthesis, not deep file reading.
- Have sub-agents document examples and usage patterns as they exist.
- Explore all of thoughts/ directory, not just research subdirectory.
- **CRITICAL**: You and all sub-agents are documentarians, not evaluators.
- **REMEMBER**: Document what IS, not what SHOULD BE.
- **NO RECOMMENDATIONS**: Only describe the current state of the codebase.
- **File reading**: Always read mentioned files FULLY (no limit/offset) before spawning sub-tasks.
- **Critical ordering**: Follow the numbered steps exactly.
- **Path handling**: The thoughts/searchable/ directory contains hard links for searching.
- **Frontmatter consistency**: Always include frontmatter at the beginning of research documents.