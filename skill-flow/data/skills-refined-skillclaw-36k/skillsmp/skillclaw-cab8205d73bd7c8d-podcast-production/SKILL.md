---
name: podcast-production
description: Use this skill when you want to transform a raw podcast transcript into polished, multi-platform content assets through a structured workflow with strategic checkpoints.
---

# Podcast Production Skill

## Overview

Transform a raw podcast transcript into polished, multi-platform content assets through a four-checkpoint system. Each checkpoint delivers decision-ready analysis in a markdown file for your feedback before proceeding. Final outputs include publication-ready YouTube strategy and a narrative-driven blog post.

**Workflow Structure:**
1. Start with `[Guest]_Source_Material.md` (raw transcript + notes).
2. Create `Checkpoint_1_Comprehensive_Analysis.md` (your feedback here).
3. Create `Checkpoint_2_Cold_Opens_and_Clips.md` (your feedback here).
4. Create `Checkpoint_3_YouTube_Strategy.md` (your feedback here).
5. Create `Checkpoint_4_Polished_Transcript_and_Blog.md` (final deliverable).

## Execution Model: Subagents for Context Preservation

**CRITICAL**: Each checkpoint should be executed by a dedicated subagent (using the Task tool) to preserve context. The workflow is as follows:

1. **Main agent** reads source material and confirms approach with the user.
2. **Subagent 1** executes Checkpoint 1, writes the file, and reports back with a summary.
3. **User reviews** and provides feedback on the Big Idea selection.
4. **Subagent 2** executes Checkpoint 2 (reads Checkpoint 1 + source), writes the file, and reports back.
5. **User reviews** and approves cold open and clips.
6. **Subagent 3** executes Checkpoint 3 (reads prior checkpoints), writes the file, and reports back.
7. **User reviews** and approves YouTube strategy.
8. **Subagent 4** executes Checkpoint 4 (reads all prior work), writes final deliverables.

**Subagent prompt template:**
```
You are executing [Checkpoint N] of the podcast production workflow.

Episode: [Guest Name]
Working directory: [path to episode folder]

Read the following files:
- SOURCE.MD (raw transcript)
- [Any prior checkpoint files]

Create: Checkpoint_[N]_[Name].md following the podcast-production skill format.

[Specific checkpoint instructions from skill]

Write the checkpoint file and report back with:
1. Key decisions/recommendations
2. Questions for user feedback
```

This structure preserves context by having each subagent start fresh with only the necessary files.