# Azure DevOps Field Reference

Required and optional fields for each work item type.

## Epic Fields

### Required
- `System.Title` - Title of the epic
- `System.WorkItemType` - "Epic"

### Standard
- `System.Description` - HTML formatted description
- `Microsoft.VSTS.Common.Priority` - 1, 2, 3, or 4
- `Microsoft.VSTS.Common.ValueArea` - "Business" or "Architectural"
- `System.State` - "New", "Active", "Resolved", "Closed"
- `System.AreaPath` - Team area path
- `System.IterationPath` - Iteration path

### Custom (Onshore)
- `Custom.ObjectiveUCP` - Calculated UCP value
- `System.Tags` - Semicolon-separated tags

## Feature Fields

### Required
- `System.Title` - Title of the feature
- `System.WorkItemType` - "Feature"
- `System.Parent` - ID of parent Epic (link)

### Standard
- `System.Description` - HTML formatted description
- `Microsoft.VSTS.Common.Priority` - 1, 2, 3, or 4
- `Microsoft.VSTS.Common.ValueArea` - "Business" or "Architectural"
- `System.State` - "New", "Active", "Resolved", "Closed"
- `System.AreaPath` - Team area path
- `System.IterationPath` - Target iteration

### Custom (Onshore)
- `Custom.ObjectiveUCP` - Calculated UCP value
- `System.Tags` - Semicolon-separated tags

## User Story Fields

### Required
- `System.Title` - Title of the user story
- `System.WorkItemType` - "User Story"
- `System.Parent` - ID of parent Feature (link)

### Standard
- `System.Description` - HTML formatted description
- `Microsoft.VSTS.Common.Priority` - 1, 2, 3, or 4
- `Microsoft.VSTS.Common.ValueArea` - "Business" or "Architectural"
- `Microsoft.VSTS.Scheduling.Effort` - Story points or hours
- `System.State` - "New", "Active", "Resolved", "Closed"
- `System.AreaPath` - Team area path
- `System.IterationPath` - Sprint iteration path

### Custom (Onshore)
- `Custom.ObjectiveUCP` - Calculated UCP value from tasks
- `System.Tags` - Semicolon-separated tags

## Parent-Child Linking

Parent-child relationships must be established AFTER work item creation:

```
Use mcp__azure-devops__wit_work_items_link with:
- id: Child work item ID
- linkToId: Parent work item ID
- type: "parent"
```

Example hierarchy:
```
Epic 1
├─ Feature 1.1 (parent: Epic 1)
│  ├─ Sprint 1.1.1 (parent: Feature 1.1)
│  └─ Sprint 1.1.2 (parent: Feature 1.1)
└─ Feature 1.2 (parent: Epic 1)
```

## Field Format Notes

- **Description**: Must be HTML format. Use `"format": "Html"` parameter.
- **Priority**: String value "1", "2", "3", or "4"
- **Effort**: String value of numeric hours
- **Tags**: Semicolon-separated, e.g., "Tag1; Tag2; Tag3"
- **State**: Must match valid state for work item type
