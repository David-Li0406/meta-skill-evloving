---
name: jira-daily-update
description: "Generate daily progress update string for Jira tasks with structured status tracking. Use when providing daily updates on Jira task progress. Triggers on: jira daily, jira-update, daily update, progress update."
agent: project-manager
tools: read, glob, grep, bash, jira_search_issues, jira_get_issue, jira_list_projects, jira_get_project, task
---

# Jira Daily Progress Update Generator

Generates daily progress update strings for Jira tasks with structured status tracking and timeline estimates. Provides consistent reporting of daily accomplishments and next steps in a clean format ready to copy to Jira.

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
    What_I_completed:
      required: true
      allow_empty: false
    What_s_next:
      required: true
      allow_empty: false
    Blockers:
      required: true
      allow_empty: true
    ETA:
      required: true
      allow_empty: false
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
5. **Generate structured daily update string with 5 required fields**
6. **Ensure all content follows exact format: `Field: Content`**
7. **Return formatted update string ready to copy to Jira**

---

## Error Handling

### Jira Server Errors
- **Ticket not found**: "Jira ticket $1 does not exist. Please create the ticket first before generating updates."
- **Access denied**: "Unable to access Jira ticket $1. Check your Jira permissions and ensure the ticket exists."

### System Errors
- **MCP server unavailable**: "Jira MCP server is currently unavailable. Please try again later."
- **Git history limited**: "No recent commits found. Please provide manual input for completed work."
- **Date validation failed**: "Unable to validate date format. Please use YYYY-MM-DD format."

---

## Best Practices

- Run this command at the end of each workday for consistent updates
- Ensure git repository is clean and commits are properly pushed
- Have related PRs created and linked to Jira ticket
- Review the generated content for accuracy before copying to Jira
- Use specific commit hashes and PR numbers when possible
- Maintain consistency with previous daily updates
- Keep ETA realistic based on actual progress and remaining complexity

---

## Data Gathering Phase

### 1. JIRA Analysis
Use JIRA MCP server to retrieve:
- **Current Status**: Ticket status, assignee, priority
- **Recent Activity**: Comments since last update, status changes
- **Previous Updates**: Last daily comment for context
- **Blocking Issues**: Any new blockers or dependencies
- **Timeline Context**: Due dates, sprint timelines

### 2. Git Activity Analysis
Use git commands to understand today's work:
- **Today's Commits**: `git log --since="1 day ago" --author="$(git config user.name)"`
- **Current Changes**: `git status --porcelain` for staged/unstaged changes
- **Branch Activity**: Recent branch switches or merges
- **Diff Analysis**: `git diff --stat` for scope of changes

### 3. GitHub Integration
Use `gh` CLI commands to identify:
- **Recent PR Activity**: `gh pr list --state updated --search "<ticket keywords>"`
- **PR Status Changes**: Reviews, approvals, merge status updates
- **CI/CD Status**: Build results, test outcomes
- **Code Review Comments**: New feedback or requested changes

### 4. Context Continuity
Review previous daily updates to:
- **Maintain Continuity**: Reference previous blockers and their status
- **Track Progress**: Compare planned vs actual completion
- **Update ETA**: Refine estimates based on new information
- **Avoid Repetition**: Don't repeat same information daily

---

## Output Format

The generated daily update string must follow this structured format using the provided template:

## Output Template

```markdown
Date: YYYY-MM-DD

## What I completed:
- **Task description**  
  [PR #1234](link) - Brief outcome
  - Specific subtask completed
  - Another specific achievement

## What's next:
- **Next task** - Priority: High
- Another task - Priority: Medium

## Blockers:
- *No blockers* OR **Blocker description** with potential impact

## ETA: X hours/days
```

### **Key Requirements:**
- Each section follows the pattern: `Field: Content`
- Date must be in YYYY-MM-DD format
- Use Markdown formatting for better readability
- Include blank lines between sections
- All five fields must be present: Date, What I completed, What's next, Blockers, ETA

### **Markdown Formatting Support:**
- Headers: `##` for section titles
- Bold text: `**text**` for emphasis
- Italic text: `*text*` for "No blockers"
- Links: `[PR #1234](url)` format
- Bullet points: `-` for list items
- Optional emojis: 📋 📝 ✅ ⏱️

### **Field-Specific Requirements:**

**Date:**
- Auto-populated with current date (YYYY-MM-DD format)

**What I completed:**
- Use bullet points with bold task names
- Include PR links when available: `[PR #1234](url)`
- Add sub-bullets for specific achievements
- Keep descriptions concise but informative

**What's next:**
- Use bullet points with bold task names
- Add priority indicators: `- Priority: High/Medium/Low`
- Focus on immediate and upcoming tasks
- Include reference links when helpful

**Blockers:**
- Use italic for no blockers: `- *No blockers*`
- Use bold for actual blockers: `- **Blocker description**`
- Explain potential impact when applicable
- Be specific about what's preventing progress

**ETA:**
- Use only `hours` or `days` (NEVER weeks)
- Example: `2 hours`, `1 day`, `3 days`
- **Important**: If ETA is 2+ days, include task splitting recommendation:
  ```
  ## ETA: 3 days
  *Recommendation: Consider splitting into smaller tasks*
  ```

---

## Error Handling

If any data source is unavailable:
- Note the missing data source clearly
- Proceed with available information
- Indicate which sections may have incomplete information
- Suggest manual verification steps

If JIRA task ID format is invalid:
- Provide clear error message with correct format example (PROJECT-123)
- Suggest verifying task ID before proceeding

If ticket existence verification fails:
- Clearly indicate ticket not found or access denied
- Suggest verifying ticket ID and permissions

If git history is limited:
- Provide template for manual completed work input
- Focus on user-provided information
- Suggest manual verification of recent activities

If date detection fails:
- Provide manual date entry option with validation
- Auto-populate with reasonable default
- Validate format correctness before proceeding

---

## Best Practices

- Run this command at the end of each workday for consistent updates
- Ensure git repository is clean and commits are properly pushed
- Have related PRs created and linked to Jira ticket
- Review the generated content for accuracy before copying to Jira
- Use specific commit hashes and PR numbers when possible
- Maintain consistency with previous daily updates
- Keep ETA realistic based on actual progress and remaining complexity