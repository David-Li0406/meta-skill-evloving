---
name: power-automate-review
description: Validate Power Automate flow definitions against live Microsoft documentation. Use after creating or modifying flows to check connector schemas, parameters, and deprecation warnings.
---

# Power Automate Flow Review

Validate Power Automate flow definitions against live Microsoft documentation.

## Triggers

This skill activates when users:
- Run `/review` after creating or modifying a flow
- Say "review my flow", "validate flow", "check flow schema"
- Want to verify connector configurations are correct

## Purpose

After a flow is created using the power-automate skill, run `/review` to:
1. Identify all connectors used in the flow
2. Fetch live documentation from Microsoft Learn
3. Validate action schemas, parameters, and connection references
4. Report any issues or deprecation warnings

## Review Process

### Step 1: Identify Flow Files

Find the workflow JSON file(s) to review:
```
src/{Solution}/src/Workflows/*.json
```

### Step 2: Parse Connectors Used

Extract all connectors from `properties.connectionReferences` and identify action types in the flow.

### Step 3: Fetch Live Documentation

For each connector identified, fetch the latest documentation:

| Connector ID | Documentation URL |
|--------------|------------------|
| `shared_office365` | https://learn.microsoft.com/en-us/connectors/office365/ |
| `shared_sharepointonline` | https://learn.microsoft.com/en-us/connectors/sharepointonline/ |
| `shared_commondataserviceforapps` | https://learn.microsoft.com/en-us/connectors/commondataserviceforapps/ |
| `shared_visualstudioteamservices` | https://learn.microsoft.com/en-us/connectors/visualstudioteamservices/ |
| `shared_excelonlinebusiness` | https://learn.microsoft.com/en-us/connectors/excelonlinebusiness/ |
| `shared_teams` | https://learn.microsoft.com/en-us/connectors/teams/ |
| `shared_onedriveforbusiness` | https://learn.microsoft.com/en-us/connectors/onedriveforbusiness/ |
| `shared_approvals` | https://learn.microsoft.com/en-us/connectors/approvals/ |
| Other connectors | https://learn.microsoft.com/en-us/connectors/{connector-name}/ |

Use the WebFetch tool to retrieve documentation for validation.

### Step 4: Validate Each Action

For each action in the flow, verify:

1. **Action Type**: Is the action type valid for this connector?
2. **Required Parameters**: Are all required parameters present?
3. **Parameter Types**: Do parameter values match expected types?
4. **Path Format**: Is the API path correctly formatted with encodeURIComponent?
5. **Connection Reference**: Does the host.connection.name reference the correct connector?
6. **Deprecation**: Is this action deprecated? Suggest alternatives.
7. **Throttling**: Are there throttling limits to be aware of?

### Step 5: Report Findings

Generate a validation report:

```markdown
## Flow Review: {FlowName}

### Connectors Used
- ✅ SharePoint (shared_sharepointonline)
- ✅ Office 365 Outlook (shared_office365)

### Action Validation

| Action | Connector | Status | Notes |
|--------|-----------|--------|-------|
| When_item_created | SharePoint | ✅ Valid | - |
| Send_email | Outlook | ⚠️ Warning | Using deprecated V1 action, recommend V2 |
| Get_items | SharePoint | ❌ Error | Missing required 'siteAddress' parameter |

### Recommendations
1. Update Send_email to use SendEmailV2 action
2. Add siteAddress parameter to Get_items action

### Documentation References
- [SharePoint Connector](https://learn.microsoft.com/en-us/connectors/sharepointonline/)
- [Office 365 Outlook Connector](https://learn.microsoft.com/en-us/connectors/office365/)
```

## Common Validation Checks

### Connection Reference Pattern
Verify this pattern is used correctly:
```json
"host": {
  "connection": {
    "name": "@parameters('$connections')['CONNECTOR_ID']['connectionId']"
  }
}
```

### Required Schema Version
```json
{
  "schemaVersion": "1.0.0.0",
  ...
}
```

### Action runAfter Dependencies
Ensure all `runAfter` references point to existing actions.

### Expression Syntax
Verify expressions use correct syntax:
- `@{expression}` for inline expressions
- `@outputs('ActionName')` for action outputs
- `@triggerBody()` for trigger data

## Deprecation Warnings

### Office 365 Outlook
- V1 actions are deprecated, use V3/V4 versions
- Webhook triggers deprecated, use polling triggers

### SharePoint
- `OnNewFile`/`OnUpdatedFile` deprecated, use `GetOnNewFileItems`/`GetOnUpdatedFileItems`

### Azure DevOps
- V1 work item triggers deprecated, use V2 versions

## Quick Validation Commands

After review, if issues are found, suggest fixes:

```
I found {N} issues in your flow. Would you like me to:
1. Fix all issues automatically
2. Show detailed fix instructions
3. Skip and deploy anyway (not recommended)
```

## Attribution Rules

NEVER include AI attribution in commits, code, or PRs. All work is attributed to the user.
