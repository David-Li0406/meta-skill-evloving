---
name: retrospect
description: Reflect on a completed workflow to identify improvements and capture changes
triggers:
  - retrospect
  - reflect on workflow
  - workflow feedback
  - what went well
  - workflow retro
---

<objective>
Guide structured reflection on a workflow that was just executed, identify what worked and what didn't, and optionally capture improvements to the workflow file.
</objective>

<prerequisites>
A workflow should have been recently completed in this session.
</prerequisites>

<process>

## Step 1: Identify the Workflow

Ask the user:

> "What workflow did we just complete? (e.g., 'setup', 'morning-briefing', or describe what we did)"

Accept either:

- Workflow name (e.g., "setup")
- Description (e.g., "the morning status check")

## Step 2: Evaluate Goal Achievement

Ask:

> "Did the workflow achieve its goal?"
>
> - **Yes**: It accomplished what it was supposed to
> - **Partial**: It helped but something was missing
> - **No**: It didn't really work

For "Partial" or "No", follow up:

> "What was missing or didn't work as expected?"

## Step 3: Identify Friction Points

Ask:

> "What felt awkward, slow, or confusing during the workflow?"
>
> Examples:
>
> - Steps that took too long
> - Information that was hard to find
> - Unclear instructions
> - Missing context

Capture specific pain points with quotes or examples when possible.

## Step 4: Suggest Improvements

Based on the feedback, brainstorm improvements:

> "Based on your feedback, here are some potential improvements:
>
> 1. {Improvement suggestion}
> 2. {Improvement suggestion}
> 3. {Improvement suggestion}
>
> Would you add anything else?"

Types of improvements to consider:

- Adding missing steps
- Removing unnecessary steps
- Clarifying instructions
- Adding context or examples
- Changing the order of operations
- Adding conditional paths ("if X, then Y")

## Step 5: Offer to Capture Changes

If the user identified actionable improvements:

> "Would you like me to draft edits to the workflow file based on this feedback?
>
> I won't make changes automatically—I'll show you the proposed edits first."

**If user says yes:**

- Read the workflow file
- Draft specific edits
- Show the proposed changes
- Ask for confirmation before applying

**If user says no:**

> "No problem! Your feedback is noted. You can always update the workflow later or run this retrospect again."

## Step 6: Summarize

Provide a brief summary:

```markdown
## Retrospect Summary

**Workflow:** {workflow name}
**Goal achieved:** {Yes/Partial/No}

**Key feedback:**
- {Point 1}
- {Point 2}

**Improvements identified:**
- {Improvement 1}
- {Improvement 2}

**Changes applied:** {Yes/No/Deferred}
```

</process>

<context_adaptation>

- **If workflow was successful**: Keep it brief, ask if there's anything to improve anyway
- **If workflow had issues**: Dig deeper into specifics, offer to fix
- **If user is frustrated**: Acknowledge the frustration, focus on constructive improvements
- **If it's a new workflow**: Feedback is especially valuable—suggest capturing learnings
</context_adaptation>

<success_criteria>

- Workflow identified
- Goal achievement evaluated
- Friction points captured (if any)
- Improvements discussed
- User offered chance to capture changes
- Summary provided
</success_criteria>
