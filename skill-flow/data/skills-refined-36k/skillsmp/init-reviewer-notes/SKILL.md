---
name: init-reviewer-notes
description: Create a template file for human reviewers to write free-form feedback before AI code review.
---

# Initialize Reviewer Notes

Create a template file for human reviewers to capture their feedback in free-form format.

## Workflow

1. **Check for existing file**
   - If `.claude/reviewer-notes.md` exists, warn and ask to overwrite or abort

2. **Create template file**
   - Write the template below to `.claude/reviewer-notes.md`

3. **Inform the user**
   - Tell them to fill in their feedback
   - Remind them to run `/process-reviewer-feedback` when done

## Template Content

```markdown
# Reviewer Notes

Write your feedback in any format. AI will convert to structured review items.

## Concerns

- [Add your concerns here - reference files/lines if known]
- Example: "The retry logic in authentication_service.rb seems aggressive"
- Example: "app/models/user.rb:45 - missing validation for email format"

## Questions

- [Questions for the code author or for discussion]
- Example: "Why was the caching layer removed?"

## Context

- [Any background context that might help AI understand your feedback]
- Example: "This relates to the recent performance issues reported in #123"
```

## Output

After creating the file, display:

```
Created `.claude/reviewer-notes.md`

Next steps:
1. Fill in your feedback in the file
2. Run `/process-reviewer-feedback` to convert to structured format
3. Run `/code-review` to generate AI review and merge with your feedback
```
