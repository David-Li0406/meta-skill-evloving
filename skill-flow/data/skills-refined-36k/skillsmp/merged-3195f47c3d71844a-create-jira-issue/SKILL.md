---
name: create-jira-issue
description: Use this skill to create well-structured Jira bug reports and generate release notes from Jira and GitHub PRs.
---

# Create Jira Issue and Release Note

This skill provides implementation guidance for creating well-structured Jira bug reports and generating bug fix release notes by analyzing Jira bug tickets and their linked GitHub pull requests.

## When to Use This Skill

This skill is automatically invoked by the `/jira:create bug` and `/jira:create-release-note` commands to guide the bug creation and release note generation processes.

## Prerequisites

- MCP Jira server configured and accessible
- GitHub CLI (`gh`) installed and authenticated
- User has permissions to create issues in the target project
- User has read access to the Jira bug and write access to Release Note fields in Jira
- User has read access to linked GitHub repositories
- Bug information available (problem description, steps to reproduce, etc.)

## Bug Report Best Practices

### Complete Information

A good bug report contains:
1. **Clear summary** - Brief description that identifies the problem.
2. **Detailed description** - Complete context and background.
3. **Reproducibility** - How often the bug occurs.
4. **Steps to reproduce** - Exact sequence to trigger the bug.
5. **Actual vs expected results** - What happens vs what should happen.
6. **Environment details** - Version, platform, configuration.
7. **Additional context** - Logs, screenshots, error messages.

### Summary Guidelines

The summary should:
- Be concise (one sentence).
- Identify the problem clearly.
- Include key context when helpful.
- Avoid vague terms like "broken" or "doesn't work".

## Bug Description Template

Use this template structure for consistency:

```
Description of problem:
<Clear, detailed description of the issue>

Version-Release number of selected component (if applicable):
<e.g., 4.21.0, openshift-client-4.20.5>

How reproducible:
<Always | Sometimes | Rarely>

Steps to Reproduce:
1. <First step - be specific>
2. <Second step>
3. <Third step>

Actual results:
<What actually happens - include error messages>

Expected results:
<What should happen instead>

Additional info:
<Logs, screenshots, stack traces, related issues, workarounds>
```

## Implementation Steps for Creating a Bug

### Step 1: Collect Bug Information

Interactively guide the user through each section of the bug report:
1. **Problem Description**: Prompt for a clear and detailed description.
2. **Version Information**: Ask for the version exhibiting the issue.
3. **Reproducibility**: Inquire how reproducible the issue is.
4. **Steps to Reproduce**: Collect the exact steps to reproduce the issue.
5. **Actual Results**: Gather information on what actually happens.
6. **Expected Results**: Clarify what should happen instead.
7. **Additional Information**: Request any extra context or logs.

### Step 2: Validate Required Fields

Before submission, ensure:
- Summary is not empty and is clear.
- Description contains a problem description.
- Affects version is specified (if required by the project).
- Steps to reproduce are provided.

### Step 3: Create the Bug in Jira

Use the MCP tool to create the bug:
```python
mcp__atlassian__jira_create_issue(
    project_key="<PROJECT_KEY>",
    summary="<bug summary>",
    issue_type="Bug",
    description="<formatted bug template>",
    additional_fields={
        "versions": [{"name": "<version>"}],
        # Add other project-specific fields as needed
    }
)
```

### Step 4: Generate Release Note

If the bug is linked to GitHub PRs, follow these steps:
1. **Fetch and Validate Jira Bug**: Retrieve the bug ticket and validate it.
2. **Parse Bug Description**: Extract Cause and Consequence sections.
3. **Extract Linked GitHub PRs**: Find all GitHub PR URLs associated with the bug.
4. **Analyze Each GitHub PR**: Extract Fix, Result, and Workaround information.
5. **Format Release Note**: Create the final release note text following the standard template.

### Step 5: Update Jira Ticket with Release Note

Use the MCP tool to write the release note to the Jira ticket:
```python
mcp__atlassian__jira_update_issue(
  issue_key=<issue-key>,
  fields={
    "customfield_12320850": {"value": "<selected_type>"},
    "customfield_12317313": "<formatted_release_note_text>"
  }
)
```

### Step 6: Display Results

Show the user what was created and provide next steps.

## Error Handling

### Missing Required Information

If required fields are missing, prompt the user for each missing field and provide context/examples to help.

### Security Validation

Always validate the content for sensitive data before updating Jira. If sensitive data is detected, inform the user and request a sanitized version.

## Best Practices Summary

1. **Clear summaries**: One sentence, specific problem.
2. **Complete steps**: Exact sequence to reproduce.
3. **Specific results**: Include error messages and symptoms.
4. **Sanitize content**: Remove all credentials and secrets.
5. **Add context**: Logs, environment details, workarounds.
6. **Use template**: Follow standard bug template structure.
7. **Validate before submit**: Check all required fields populated.

## See Also

- `/jira:create` - Main command that invokes this skill.
- `/jira:create-release-note` - Command for generating release notes.
- Jira documentation on bug workflows.