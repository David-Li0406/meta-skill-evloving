---
name: groom
description: Groom GitHub issues from needs-details to ready
argument-hint: [issue-number] (optional)
allowed-tools: Bash, Task, AskUserQuestion, Read, Grep, Glob
disable-model-invocation: true
agent: groom-agent
---

# Issue Grooming Command

This command helps transform draft issues (labeled `needs-details`) into implementation-ready issues (labeled `ready`).

## Dynamic Context

**Current issues needing grooming:**
!`gh issue list --label needs-details --json number,title --limit 10 2>/dev/null || echo "Could not fetch issues"`

## Templates Reference

**Draft issues** (`.github/ISSUE_TEMPLATE/draft.yml`):

- Minimal: just a Description field
- Auto-labeled: `needs-details`

**Ready issues** (`.github/ISSUE_TEMPLATE/task.yml`):

- Description: What needs to be done and why
- Acceptance Criteria: Testable checkboxes
- Out of Scope: What this task explicitly does NOT include

## Arguments

**Issue number:** $ARGUMENTS

## Instructions

### Step 1: Determine Mode

If an issue number was provided above (not empty):

- Skip to Step 3 with that issue number

If no issue number was provided:

1. Fetch issues with `needs-details` label:

    ```bash
    gh issue list --label needs-details --json number,title,labels,milestone --limit 20
    ```

2. If no issues found, inform the user and exit.

3. Use AskUserQuestion for mode selection with these options:
    - **Single**: "I'll pick one issue to work on" - Ask which issue number
    - **Multiple**: "Let me select specific issues" - Ask for comma-separated issue numbers
    - **Auto-select**: "You pick the highest priority issues (max 3)" - Claude selects based on labels/milestones
    - **Preview & Pick**: "Rank all issues by priority, then I'll choose" - Claude analyzes and ranks all issues, shows rankings with reasoning, user picks which to groom

### Step 2: Execute Based on Mode

**For Single mode:**

- Proceed to Step 3 with the selected issue

**For Preview & Pick mode:**

1. Analyze all issues considering:
    - Labels (priority, type, area)
    - Milestone assignment
    - Dependencies on other issues
    - Complexity vs value
    - Blocking status (does this unblock other work?)

2. Present a ranked list to the user showing:

    ```
    PRIORITY RANKING:

    1. #42 - User authentication flow
       Priority: HIGH | Reason: Blocks #43, #44; milestone: MVP

    2. #38 - File upload validation
       Priority: HIGH | Reason: Security-critical; no dependencies

    3. #35 - Dashboard layout
       Priority: MEDIUM | Reason: User-facing; straightforward scope

    ... (show all issues with rankings)
    ```

3. Use AskUserQuestion to let the user select which issues to groom (set multiSelect: true):
    - Each option should be an issue (e.g., label: "#42 - User authentication", description: "HIGH - Blocks #43, #44")
    - User can select multiple issues from the ranked list
    - Show all issues as options, if needed, you can show them in groups (each group as a question) of 5 options each.
    - Sort the issues options by highest-priority

4. Proceed to Multiple mode with selected issues

**For Multiple/Auto-select mode:**

- Spawn parallel Task agents (subagent_type: "general-purpose") for each issue
- Each agent uses the `groom-research` agent to run the **Research & Discovery** phase
- Agents return research findings and key decisions - NOT final drafts
- Main agent presents decisions to user for input
- THEN drafts are created incorporating user decisions

### Step 3: Groom Issue (per issue)

This is a TWO-PHASE process. Do NOT skip the first phase.

#### Phase 1: Research & Discovery (REQUIRED)

1. **Fetch issue details:**

    ```bash
    gh issue view <number> --json number,title,body,labels
    ```

2. **Research codebase context** using the `groom-research` agent:
    - Find related files using Grep and Glob
    - Read relevant code to understand the feature area
    - Look for similar patterns or existing implementations
    - Identify architectural implications

3. **Identify decisions and alternatives:**
    - What architectural choices exist?
    - Are there multiple valid approaches?
    - What trade-offs should the user consider?
    - What assumptions are you making that the user should validate?
    - What scope boundaries are ambiguous?

4. **Use AskUserQuestion** to gather user input on findings:
    - Show what you learned from the codebase
    - Present key decisions that need user input
    - Offer alternatives where they exist
    - Ask clarifying questions about ambiguous requirements

    Example questions to surface:
    - "Should this use the existing X pattern or introduce Y?"
    - "The scope could include A or exclude it - which do you prefer?"
    - "I found two approaches: [approach 1] vs [approach 2]. Which fits better?"
    - "This might affect [related feature]. Should we account for that?"

#### Phase 2: Draft & Finalize

Only proceed here AFTER getting user input on key decisions.

1. **Draft improved body** incorporating user decisions:

    ```markdown
    ## Description

    [Expanded description based on research AND user decisions]

    ## Acceptance Criteria

    - [ ] [Specific, testable criterion reflecting agreed approach]
    - [ ] [More criteria based on user input]

    ## Out of Scope

    - [Items explicitly excluded based on user decision]
    - [Scope boundaries the user confirmed]
    ```

2. **Present draft to user:**
    - Show the original issue content
    - Show the proposed new body
    - Highlight how user decisions were incorporated
    - Ask for final approval or modifications

3. **If approved, update the issue:**
    ```bash
    gh issue edit <number> --body "<new body>"
    gh issue edit <number> --remove-label needs-details --add-label ready
    ```

### Step 4: Summary

After all issues are processed, provide a summary:

- Number of issues groomed
- Key decisions made (for reference)
- Links to updated issues
- Any issues that were skipped or need follow-up

## After Subagents Return

When subagents return their research:

1. **Compile all decisions and questions** from all issues
2. **Use AskUserQuestion** for each decision point, grouped by issue
3. **Collect user decisions** before proceeding to draft
4. **Draft issues** incorporating the decisions
5. **Proceed to Self-Review**

## Self-Review (REQUIRED)

Before presenting drafts to the user, review them for quality and codebase alignment using parallel subagents.

### For Each Draft:

1. **Spawn three review agents in parallel:**

    **Issue Quality Review** (subagent_type: "general-purpose"):
    - Review the draft against `.claude/skills/groom/templates/review-criteria.md`
    - Check description clarity, acceptance criteria specificity, scope boundaries
    - Identify ambiguous language or undefined terms
    - Verify appropriate labels are set (type, area)
    - Return list of issues found, suggested fixes, and missing labels

    **Codebase Alignment Review** (subagent_type: "Explore"):
    - Confirm referenced files/patterns actually exist
    - Check that the approach matches codebase conventions
    - Identify any conflicts with existing features
    - Return list of alignment issues and concerns

    **Related Issues Review** (subagent_type: "general-purpose"):
    - Fetch open issues: `gh issue list --state open --json number,title,body,labels --limit 50`
    - Identify issues that should be updated as a result of this draft:
        - Issues that block or are blocked by this one
        - Issues that reference the same files/features
        - Issues that overlap in scope (potential duplicates or related work)
    - Return list of suggested relationship updates (blocked-by, blocks, references)

2. **Collect results from all three agents**

3. **Process findings:**
    - Fix obvious issues (unclear wording, missing criteria, non-existent references)
    - Note concerns to raise with user during Final Review

4. **Proceed to Final Review** with any flagged concerns

### What to Fix vs. Flag

**Fix directly:**

- Vague or untestable acceptance criteria
- Missing out of scope items
- Ambiguous language
- References to non-existent files/patterns

**Flag for user discussion:**

- Potential conflicts with existing features
- Architectural trade-offs
- Discovered complexity that may affect scope
- Suggested issue relationships (blocked-by, blocks)
- Related issues that may need updates
- Missing or suggested labels (type, area)

## Final Review (REQUIRED)

After all drafts are ready, you MUST review each issue individually with the user.

1. **Present all drafts** with a summary showing each issue's title and key changes

2. **Use AskUserQuestion for each issue** (up to 4 at a time). Each question should have these options (in this order):
    - **Approve as AI-drafted** (default): Issue content is good but mark as `ai-drafted` for later human review
    - **Approve as ready**: Issue is fully reviewed and ready for implementation
    - **Request changes**: User provides feedback, you revise the draft
    - **Skip**: Leave issue as `needs-details` for now

3. **Apply updates based on responses:**
    - "Approve as ready": `--remove-label needs-details --add-label ready`
    - "Approve as AI-drafted": `--remove-label needs-details --add-label ready --add-label ai-drafted`
    - "Request changes": Revise draft based on feedback, then ask again
    - "Skip": No changes, remains `needs-details`

4. **Handle "Request changes"** responses:
    - Show the specific feedback
    - Revise the draft accordingly
    - Present the revised version
    - Ask for approval again (same options)

## Labels Reference

| Label           | Meaning                                               |
| --------------- | ----------------------------------------------------- |
| `needs-details` | Draft issue, not ready for implementation             |
| `ready`         | Fully detailed, ready for implementation              |
| `ai-drafted`    | Content generated/groomed by AI, pending human review |

Note: `ai-drafted` is used WITH `ready` - the issue is detailed enough to work on, but a human hasn't verified the AI's decisions yet.

### Priority Labels

Issues should have a priority label for triage and backlog prioritization:

| Label                | Color  | When to Use                             |
| -------------------- | ------ | --------------------------------------- |
| `priority: critical` | Red    | Must be addressed immediately           |
| `priority: high`     | Orange | Important, should be addressed soon     |
| `priority: medium`   | Yellow | Normal priority                         |
| `priority: low`      | Green  | Nice to have, address when time permits |

During grooming, suggest an appropriate priority label based on:

- Business impact and user-facing visibility
- Blocking status (does this unblock other work?)
- Security or stability implications
- Milestone deadlines

## Creating Follow-up Issues

During grooming, you may identify work that should be separate issues (prerequisites, follow-ups, discovered scope). When creating these:

1. **Get user approval** before creating any new issues
2. **Create as draft** with `needs-details` label
3. **Link related issues** using GitHub's native relationships

**For issue relationships (sub-issues, blocking):** Read `docs/ai/github-workflow.md` for the GraphQL commands and decision guide on when to use parent/child vs blocking relationships.

## Notes

- NEVER skip the Research & Discovery phase
- ALWAYS surface architectural decisions to the user
- Subagents research and identify - they don't decide
- Present alternatives, don't just pick one
- User decisions should be reflected in the final draft
- Preserve existing context from the original issue
- Make acceptance criteria specific and testable based on agreed approach
- Link related issues using GitHub's relationship APIs (see `docs/ai/github-workflow.md`)
