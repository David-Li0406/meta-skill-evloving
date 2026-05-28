---
name: jira-daily-update
description: Generate structured daily progress update comments for Jira tasks, ensuring consistent status tracking and timeline estimates. Use when providing daily updates on Jira task progress.
---

# Jira Daily Progress Update Generator

Generates structured daily progress update comments for Jira tasks with comprehensive status tracking and timeline estimates. Provides consistent reporting of daily accomplishments and next steps in a clean format ready to copy to Jira.

---

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
        - Must be specific about what's preventing progress if present
    ETA:
      required: true
      min_length: 20
      validation_rules:
        - Must include realistic and justifiable timeline
```

---

## The Job

1. **Receive Jira task ID from user**
2. **Validate Jira task ID format (PROJECT-123)**
3. **Auto-detect current date in YYYY-MM-DD format**
4. **Gather data from multiple sources**:
   - JIRA MCP server for ticket details, recent activity, and context
   - Git commit history for today's work and current branch status
   - GitHub CLI for related PR status and activity
   - Previous comments for context and continuity
5. **Generate structured daily update comment with 5 required fields**
6. **Ensure all content follows exact format: `Field: Content`**
7. **Preview**: Show formatted output ready for Jira
8. **User Confirmation**: Require explicit approval
9. **Posting**: Use `jira_add_comment` to add comment if confirmed

---

## Error Handling

### Jira Server Errors
- **Ticket not found**: "Jira ticket $1 does not exist. Please create the ticket first before generating updates."
- **Access denied**: "Unable to access Jira ticket $1. Check your Jira permissions and ensure the ticket exists."

### Validation Errors
- **Date too far in future**: "Date is more than 2 days ahead. Consider splitting deliverables into separate tasks for better timeline management."
- **Insufficient content**: "Field content below minimum character requirements. Please provide more specific details and measurable outcomes."

### System Errors
- **MCP server unavailable**: "Jira MCP server is currently unavailable. Please try again later."
- **Git history limited**: "No recent commits found. Please provide manual input for completed work."
- **Date validation failed**: "Unable to validate date format. Please use YYYY-MM-DD format."

---

## Best Practices

- Run this command at the end of each workday for consistent updates.
- Ensure git repository is clean and commits are properly pushed.
- Have related PRs created and linked to Jira ticket.
- Review the generated content for accuracy before approval.
- Use specific commit hashes and PR numbers when possible.
- Maintain consistency with previous daily updates.
- Keep ETA realistic based on actual progress and remaining complexity.

---

## Output Format

The generated daily update comment must follow this exact format:

```
Date: Current Date
What I completed: What was completed today
What's next: What is next on TODOs
Blockers: What blockers exist from continuing work
ETA: Time to complete remaining tasks
```

### **Key Requirements:**
- Each line follows the exact pattern: `Field: Content`
- Date must be in YYYY-MM-DD format
- Content should be specific and actionable
- All five fields must be present

### **Field-Specific Requirements:**

**Date:**
- Auto-populated with current date (YYYY-MM-DD format)
- Cannot be future date unless specified

**What I completed:**
- Minimum 30 characters
- Specific accomplishments from today with technical details
- Include commit hashes, PR numbers, or ticket references where possible

**What's next:**
- Minimum 30 characters
- Clear next tasks and TODOs based on remaining work
- Prioritized and actionable with implementation complexity considered

**Blockers:**
- Can be empty (minimum 0 characters)
- Clear description of blockers if present

**ETA:**
- Minimum 20 characters
- Specific time estimate based on actual work remaining
- Realistic and justifiable timeline

---

## Auto-Detection Features

- **Current Date**: Automatically uses today's date in YYYY-MM-DD format.
- **Git Context**: Analyzes current branch status and recent commits.
- **PR Activity**: Checks GitHub for related pull requests and their status.
- **Previous Updates**: Reviews existing comments to avoid repetition.
- **Timeline Calculation**: Adjusts ETA based on daily progress.