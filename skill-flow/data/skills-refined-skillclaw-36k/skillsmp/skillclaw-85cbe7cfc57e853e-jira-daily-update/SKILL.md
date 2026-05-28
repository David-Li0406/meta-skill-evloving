---
name: jira-daily-update
description: Use this skill when providing daily updates on Jira task progress to ensure structured and comprehensive reporting of accomplishments and next steps.
---

# Jira Daily Progress Update Generator

Generates structured daily progress update comments for Jira tasks with status tracking and timeline estimates. This skill provides consistent reporting of daily accomplishments and next steps in a clean format ready to copy to Jira.

## Validation Schema

```yaml
validation_schema:
  required_fields: [Date, What_I_completed, What_s_next, Blockers, ETA]
  format_requirements:
    format_pattern: "Field: Content"
    date_format: "YYYY-MM-DD"
  field_validations:
    Date:
      required: true
      format: "YYYY-MM-DD"
      auto_populate: true
      validation_rules:
        - Must be current date or reasonable business day context
        - Cannot be future date unless specified
    What_I_completed:
      required: true
      min_length: 30
      validation_rules:
        - Must include specific accomplishments from today
        - Should reference commits, PRs, or tickets where possible
        - Must be actionable and measurable items
    What_s_next:
      required: true
      min_length: 30
      validation_rules:
        - Must include clear next tasks and TODOs
        - Should be prioritized and actionable
    Blockers:
      required: true
      min_length: 0
      allow_empty: true
      validation_rules:
        - Can be empty (0 characters minimum)
        - Must specify what's preventing progress if present
    ETA:
      required: true
      min_length: 20
      validation_rules:
        - Must include realistic and justifiable timeline
        - Should mention key milestones with individual timelines
```

## The Job

1. **Receive Jira task ID from user**
2. **Validate Jira task ID format (PROJECT-123)**
3. **Auto-detect current date in YYYY-MM-DD format**
4. **Gather data from multiple sources**:
   - JIRA MCP server for ticket details, recent activity, and context
   - Git commit history for today's work and current branch status
   - GitHub CLI for related PR status and activity
   - Previous comments for context and continuity
5. **Generate structured daily update string with 5 required fields**
6. **Ensure all content follows exact format: `Field: Content`**
7. **Return formatted update string ready to copy to Jira**

## Error Handling

### Jira Server Errors
- **Ticket not found**: "Jira ticket $1 does not exist. Please create the ticket first before generating updates."
- **Access denied**: "Unable to access Jira ticket $1. Check your Jira permissions and ensure the ticket exists."

### System Errors
- **MCP server unavailable**: "Jira MCP server is currently unavailable. Please try again later."
- **Git history limited**: "No recent commits found. Please provide manual input for completed work."
- **Date validation failed**: "Unable to validate date format. Please use YYYY-MM-DD format."

## Best Practices

- Run this command at the end of the workday to ensure timely updates.