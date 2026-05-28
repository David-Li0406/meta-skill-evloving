---
name: developer-growth-analysis
description: Analyzes recent Claude Code chat history to identify knowledge gaps, searches for resources to fill them, and generates a report. Use when the user asks about learning gaps, skill assessment, areas for improvement, or wants to review recent coding sessions for growth opportunities.
---

# Developer Growth Analysis

Triangulates knowledge gaps from your recent Claude Code sessions, searches for resources to fill them, reports back.

## Instructions

1. **Read Chat History**

   Read `~/.claude/history.jsonl` (JSONL format):
   - `display`: User's message
   - `project`: Project path
   - `timestamp`: Unix ms
   - `pastedContents`: Pasted code/content

   Filter to past 24-48 hours.

2. **Triangulate Knowledge Gaps**

   Look for signals of incomplete understanding:
   - **Repeated questions** on same topic (didn't stick)
   - **Multiple attempts** to solve one problem (missing mental model)
   - **Clarifying questions** that reveal conceptual gaps
   - **Workarounds** instead of idiomatic solutions
   - **Copy-paste patterns** without adaptation (cargo culting)
   - **Architectural uncertainty** (flip-flopping on approach)

   Cross-reference these signals. A single instance isn't a gap—look for convergence across multiple interactions.

3. **Identify 2-4 Gaps**

   Each gap must be:
   - **Specific**: "React useEffect cleanup" not "React hooks"
   - **Evidence-based**: Quote the chat history
   - **Addressable**: Something docs/articles can fix (not "needs experience")

4. **Search for Resources**

   For each gap, use web search to find:
   - Official documentation (primary source)
   - Well-regarded tutorials/articles
   - Relevant discussions with depth

   Prioritize:
   - Authoritative sources over blog spam
   - Recent content for fast-moving tech
   - Content that addresses the specific gap, not adjacent topics

5. **Report**

   Format:

   ```markdown
   ## Knowledge Gaps

   ### 1. [Gap Name]

   **Evidence**: [Quote from chat history showing the gap]

   **What's Missing**: [The specific concept/pattern not understood]

   **Resources**:
   - [Title](url) — [One line on why this helps]
   - [Title](url) — [One line on why this helps]

   ---

   [Repeat for each gap]

   ## What You're Solid On

   - [Thing you demonstrated competence in]
   - [Another thing]
   ```

   Keep it tight. No fluff, no "great job" padding.
