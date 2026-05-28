---
name: clean-interviews
description: Clean up user interviews in Research/User interviews/, add frontmatter tags, standardize structure, and aggregate insights into the research dashboard.
allowed-tools: Read, Bash, Edit, Glob, Grep
---

# Clean Interviews

Processes user interviews in `~/obsidian/Research/User interviews/`, standardizes their format, adds tags, and aggregates insights into the research dashboard.

## When to Use

- After conducting user interviews
- When interview files need standardization
- To aggregate interview insights across projects
- When preparing interview data for analysis

## Workflow

### 1. Scan Interview Files

Find all interview files:

```bash
find ~/obsidian/Research/User\ interviews -name "*.md" -type f
```

Note the directory structure - interviews are organized by project (e.g., `Project-A/`, `Project-B/`).

### 2. Read Current Dashboard

```bash
cat ~/obsidian/research-dashboard.md
```

Check if "User Interview Insights" section exists.

### 3. Process Each Interview File

For each interview file:

a) **Read the file** to understand current content
b) **Add YAML frontmatter** if missing:

```yaml
---
tags:
  - interview
  - [project-name]
interviewee: Name
date: YYYY-MM-DD
project: Project Name
signal: strong | moderate | weak
action-items:
  - "Intro to [Contact] at [Company]"
  - "Follow up on [specific topic]"
---
```

**Note:** `action-items` is optional - only include if there are genuinely important actions from this interview. See "Action Item Criteria" section below.

c) **Restructure content** into standard sections:

```markdown
## Summary
One-paragraph synthesis of the interview

## Key Insights
- Bullet points of main takeaways

## Pain Points
- Problems the interviewee faces

## Quotes
> Direct quotes worth preserving

## Follow-ups
- Action items or questions for next time
```

d) **Preserve original content** - reorganize, don't delete

### 4. Determine Signal Strength

Apply these criteria:

**Strong Signal:**
- Explicit willingness/commitment ("I would definitely use this")
- Quantified usage metrics specific to their domain
- Current paid solution they would switch from
- Specific problems that match our solution

**Moderate Signal:**
- Interest expressed but conditional
- Some relevant problems, some not
- Unclear on willingness to pay or switch
- General positive sentiment without commitment

**Weak Signal:**
- Polite interest but no clear need
- Problems do not align with our solution
- Low usage/engagement in relevant areas
- Blockers (jurisdiction, technical, organizational)

### 5. Archive Dashboard (if updating)

If dashboard will be updated, run archive first:

```bash
bash ~/.claude/scripts/archive-dashboard.sh
```

### 6. Aggregate Interview Insights

Count interviews by:
- Project (directory name)
- Signal strength

Summarize key takeaways per project.

### 7. Update Research Dashboard

Add or update "User Interview Insights" section after "Latest Research Documents":

```markdown
## User Interview Insights
**Total Interviews:** X | **Strong:** Y | **Moderate:** Z | **Weak:** W

### By Project
- **Project-A:** X interviews - [key aggregated takeaway]
- **Project-B:** X interviews - [key aggregated takeaway]

### Recent Interviews
- [[Research/User interviews/Project-A/Jane Doe|Jane Doe]] - Strong, target user interested in product
```

### 8. Verify

- All interview files have YAML frontmatter
- All files have standard sections
- Dashboard has interview insights section
- Tags work in Obsidian (#interview)

## Interview Template

When processing interviews, structure them as:

```markdown
---
tags:
  - interview
  - project-a
interviewee: Jane Doe
date: 2026-01-15
project: Project-A
signal: strong
---

## Summary
One-paragraph synthesis capturing who they are, what they need, and key signals.

## Key Insights
- Insight 1
- Insight 2

## Pain Points
- Pain point 1
- Pain point 2

## Quotes
> "Direct quote that captures something important"

## Follow-ups
- Action item or question
```

## Action Item Criteria

Action items in frontmatter are for **genuinely important tasks** that should surface on the daily dashboard. Most interviews won't have any.

### Include (Important - Surface to Dashboard)

- **Introductions**: "Can intro to [Person] at [Company]" - warm intros are high-value
- **Follow-up calls/meetings**: Scheduled or promised follow-ups with the interviewee
- **Partner/vendor investigation**: Specific companies or tools mentioned worth investigating
- **Critical product decisions**: Feature requests that came with strong signal and affect architecture
- **Urgent blockers**: Regulatory, legal, or technical issues that need immediate attention

### Exclude (Keep in Follow-ups Section Only)

- General "look into X" observations
- Minor UX suggestions
- Feature ideas without strong signal
- Vague "might be interesting" items
- Things already on the roadmap
- Research that's nice-to-have, not blocking

### Examples

**Include:**
```yaml
action-items:
  - "Intro to [Partner] (via [Contact]) - partner opportunity"
  - "Investigate [Vendor] integration for risk management"
  - "Follow-up call with [Contact] re: [Feature] threshold feature"
```

**Don't Include:**
- "Think about rewards structure" (too vague)
- "Consider better FX handling" (product backlog, not action item)
- "Research stETH safety" (general research, not urgent)

### Rule of Thumb

Ask: "Would I forget this and regret it?" If yes, it's an action item. If it's just useful context, leave it in the Follow-ups section only.

## Signal Tagging Guidelines

### Strong
- Explicit "I would use this" or "I would pay for this"
- Currently using competitors and unhappy
- Quantified spending patterns (monthly card spend, holdings)
- Clear problem-solution fit

### Moderate
- "This sounds interesting" without commitment
- Some problems align, others don't
- Unclear on pricing sensitivity
- Would need to see it working first

### Weak
- Polite but non-committal
- Problems don't match solution
- Jurisdiction/regulatory blockers
- Low target market fit (small spender, no crypto holdings)

## Important Notes

- **Preserve original content** - restructure, don't delete information
- **Be conservative with signal strength** - default to moderate if unclear
- **Use project directory name** as the project tag (lowercase)
- **Date format:** YYYY-MM-DD (ISO 8601)
- **Link format:** Obsidian wikilinks with display text

## Paths Reference

- Interview root: `~/obsidian/Research/User interviews/`
- Dashboard: `~/obsidian/research-dashboard.md`
- Archive script: `~/.claude/scripts/archive-dashboard.sh`

**Note:** Paths can be customized in `~/.claude/config/paths.env`
