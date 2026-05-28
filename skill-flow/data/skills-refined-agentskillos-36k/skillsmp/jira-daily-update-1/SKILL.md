---
name: jira-daily-update
description: "Generate daily progress update comment for Jira tasks with structured status tracking. Use when providing daily updates on Jira task progress. Triggers on: jira daily, jira-update, daily update, progress update."
agent: project-manager
tools: read, glob, grep, bash, jira_search_issues, jira_get_issue, jira_add_comment, jira_list_projects, jira_get_project, task
---

# Jira Daily Progress Update Generator

Generates comprehensive daily progress update comments for Jira tasks with structured status tracking and timeline estimates. Provides consistent reporting of daily accomplishments and next steps.

---

## Validation Schema

```yaml
validation_schema:
  required_fields: [Date, What_I_completed, What_s_next, Blockers, ETA]
  format_requirements:
    format_pattern: "Field: Content"
    no_markdown: true
    date_format: "YYYY-MM-DD"
  field_validations:
    Date:
      required: true
      format: "YYYY-MM-DD"
      auto_populate: true
      validation_rules:
        - Must be current date or reasonable business day context
        - Cannot be future date unless specified
        - Must follow YYYY-MM-DD format strictly
    What_I_completed:
      required: true
      min_length: 30
      validation_rules:
        - Must include specific accomplishments from today
        - Should reference commits, PRs, or tickets where possible
        - Must be actionable and measurable items
        - Avoid vague statements like "worked on stuff"
    What_s_next:
      required: true
      min_length: 30
      validation_rules:
        - Must include clear next tasks and TODOs
        - Should be prioritized and actionable
        - Include immediate tasks (today/tomorrow) and upcoming milestones
        - Avoid generic statements like "continue work"
    Blockers:
      required: true
      min_length: 0
      allow_empty: true
      validation_rules:
        - Can be empty (0 characters minimum)
        - Must be specific about what's preventing progress if present
        - Should include impact assessment and resolution timeline
        - Categorize: technical, resource, dependency, decision, external
    ETA:
      required: true
      min_length: 20
      validation_rules:
        - Must include realistic and justifiable timeline
        - Should include protective language: "contingent on", "assuming", "pending"
        - Include confidence level and influencing factors
        - Must mention key milestones with individual ETAs
        - Avoid overly optimistic estimates without justification
```

---

## The Job

1. **Receive Jira task ID from user**
2. **Validate Jira task ID format (PROJECT-123)**
3. **Auto-detect current date in YYYY-MM-DD format**
4. **Gather data from multiple sources**:
   - JIRA MCP server for ticket details, recent activity, and context
   - Coordinate with fullstack-developer subagent for technical code analysis
   - Fullstack-developer analysis includes:
     - Actual code changes made and their complexity
     - Technical implementation quality assessment
     - Integration points and dependencies affected
     - Remaining work estimation based on code state
     - Technical blockers discovered during implementation
   - Git commit history for today's work and current branch status
   - GitHub CLI for related PR status and activity
   - Previous comments for context and continuity
5. **Generate structured daily update with 5 required fields**
6. **Ensure all content follows exact format: `Field: Content`**
7. **Enhanced Validation**: Applies enhanced validation rules for content quality and compliance
8. **Preview**: Shows formatted output ready for Jira
9. **User Confirmation**: Requires explicit approval
10. **Posting**: Uses `jira_add_comment` to add comment if confirmed

---

## Technical Error Handling

### Jira Server Errors
- **Ticket not found**: "Jira ticket $1 does not exist. Please create the ticket first before generating comments."
- **Access denied**: "Unable to access Jira ticket $1. Check your Jira permissions and ensure the ticket exists."

### Enhanced Validation Errors
- **Date too far in future**: "Date is more than 2 days ahead. Consider splitting deliverables into separate tasks for better timeline management."
- **ETA unrealistic**: "ETA should include protective language (approximately, estimated, contingent on) to protect against deadline uncertainties."
- **Insufficient content**: "Field content below minimum character requirements. Please provide more specific details and measurable outcomes."

### System Errors
- **MCP server unavailable**: "Jira MCP server is currently unavailable. Please try again later."
- **Git history limited**: "No recent commits found. Please provide manual input for completed work."
- **Date validation failed**: "Unable to validate date format. Please use YYYY-MM-DD format."

---

## Best Practices

- Run this command at the end of each workday for consistent updates
- Ensure git repository is clean and commits are properly pushed
- Have related PRs created and linked to Jira ticket
- Review the generated content for accuracy before approval
- Use specific commit hashes and PR numbers when possible
- Maintain consistency with previous daily updates
- Keep ETA realistic based on actual progress and remaining complexity

1. Receive Jira task ID from user
2. Validate Jira task ID format (PROJECT-123)
3. Auto-detect current date in YYYY-MM-DD format
4. Gather data from multiple sources:
   - JIRA MCP server for ticket details and recent activity
   - Git commit history for today's work
   - GitHub CLI for related PR status and activity
   - Previous comments for context and continuity
5. Generate structured daily update with 5 required fields
6. Ensure all content follows exact format: `Field: Content`
7. Validate content quality and completeness
8. Return formatted comment ready for posting to Jira

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

## Enhanced Validation Rules

### **Date Threshold Validation:**
- ✅ Date must be within reasonable business day context (not too far in past)
- ✅ Current date auto-detected with timezone awareness
- ✅ Future dates only allowed with explicit justification
- ❌ Validation fails if date is invalid or unreasonable

### **ETA Realism Validation:**
- ✅ Must include protective language: "contingent on", "assuming", "pending"
- ✅ Estimates should be justified based on remaining complexity
- ✅ Include confidence level and potential blockers
- ✅ Reference key milestones with individual ETAs
- ❌ Validation fails if ETA is overly optimistic without justification

### **Cross-field Validation:**
- ✅ "What's next" should align with ETA timeline
- ✅ Blockers should be reflected in ETA estimates if present
- ✅ Completed work should align with previous updates when applicable
- ❌ Validation fails if fields conflict or are inconsistent

### **Quality Validation:**
- ✅ Content should avoid generic statements ("worked on stuff", "continue work")
- ✅ Include specific references (commit hashes, PR numbers, ticket IDs)
- ✅ Maintain consistency with previous daily updates
- ✅ Technical details should be accurate and relevant
- ❌ Validation fails if content is too vague or irrelevant

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
- No additional markdown formatting or bullet points
- All five fields must be present

### **Field-Specific Requirements:**

**Date:**
- Auto-populated with current date (YYYY-MM-DD format)
- Cannot be future date unless specified
- Must be valid business day context

**What I completed:**
   - Minimum 30 characters
   - Enhanced with technical analysis from fullstack-developer
   - Specific accomplishments from today with technical details
   - Include commit hashes, PR numbers, or ticket references where possible
   - Actionable and measurable items with code quality assessment
   - Clear completion status verified through code analysis

**What's next:**
   - Minimum 30 characters
   - Enhanced with technical roadmap from fullstack-developer analysis
   - Clear next tasks and TODOs based on remaining technical work
   - Prioritized and actionable with implementation complexity considered
   - Include immediate tasks (today/tomorrow) and upcoming milestones
   - Specific timelines and deliverables grounded in code analysis

**Blockers:**
- Can be empty (minimum 0 characters)
- Clear description of blockers if present
- Categorized (technical, resource, dependency, decision, external)
- Include impact assessment and resolution timeline
- Specific about what's preventing progress

**ETA:**
   - Minimum 20 characters
   - Enhanced with technical estimation from fullstack-developer
   - Specific time estimate based on actual code complexity analysis
   - Realistic and justifiable timeline with technical backing
   - Include confidence level and technical risk factors
   - Key milestones with individual ETAs grounded in implementation reality

---

## Auto-Detection Features

- **Current Date**: Automatically uses today's date in YYYY-MM-DD format
- **Git Context**: Analyzes current branch status and recent commits
- **PR Activity**: Checks GitHub for related pull requests and their status
- **Previous Updates**: Reviews existing comments to avoid repetition
- **Timeline Calculation**: Adjusts ETA based on daily progress

---

## Validation Rules

### **Format Validation:**
- ✅ Field name exactly as specified
- ✅ Colon followed by space
- ✅ No additional formatting or bullet points
- ✅ Date in YYYY-MM-DD format
- ❌ Validation fails if format deviates

### **Content Validation:**
- ✅ All fields meet minimum character requirements
- ✅ Completed work includes specific references (commits, PRs, tickets)
- ✅ Next steps are clear and prioritized
- ✅ Blockers are specific when present
- ✅ ETA includes specific time estimates
- ❌ Validation fails if content is vague or incomplete

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
- Provide option to proceed with manual input if appropriate

If git history is limited:
- Provide template for manual completed work input
- Focus on user-provided information
- Suggest manual verification of recent activities

If date detection fails:
- Provide manual date entry option with validation
- Auto-populate with reasonable default
- Validate format correctness before proceeding

### **Enhanced Validation Error Handling:**

**Date Validation Errors:**
- Invalid format: Provide correct YYYY-MM-DD format with examples
- Future date: Require justification or suggest current date
- Unreasonable date: Suggest verifying date context

**ETA Validation Errors:**
- Overly optimistic: Suggest including protective language and contingencies
- Missing justification: Request breakdown of remaining work and timeline
- Unrealistic timeline: Provide guidance on realistic time estimates

**Content Quality Errors:**
- Vague statements: Provide specific examples of detailed content
- Missing references: Suggest including commit hashes, PR numbers, or ticket IDs
- Generic language: Offer field-specific templates with concrete examples

**Cross-field Validation Errors:**
- ETA and blockers conflict: Suggest adjusting timeline based on blockers
- Next steps misaligned with ETA: Recommend timeline adjustment or task reordering
- Inconsistent with previous updates: Request clarification on changes

---

## Best Practices

- Run this command at the end of each workday for consistent updates
- Ensure git repository is clean and commits are properly pushed
- Have related PRs created and linked to Jira ticket
- Review the generated content for accuracy before approval
- Use specific commit hashes and PR numbers when possible
- Maintain consistency with previous daily updates
- Keep ETA realistic based on actual progress and remaining complexity