# Priority and State Mapping

Quick reference for mapping markdown metadata to Azure DevOps fields.

## Priority Mapping

| Markdown Priority | DevOps Priority | Notes |
|------------------|-----------------|-------|
| CRITICAL | 1 | Highest priority |
| HIGH | 1 | Same as critical |
| MEDIUM | 2 | Default priority |
| NORMAL | 2 | Same as medium |
| LOW | 3 | Lowest priority |

**Usage**: `Microsoft.VSTS.Common.Priority` field takes integer 1-4.

## State Mapping

| Markdown Status | DevOps State | Work Item Types |
|----------------|--------------|-----------------|
| Planning | New | All |
| In Planning | New | All |
| Ready for Implementation | New | All |
| In Progress | Active | All |
| Active | Active | All |
| Completed | Resolved | All |
| Done | Resolved | All |
| Closed | Closed | All |

**Default**: If status not recognized, use "New".

## Value Area

| Work Item Type | Default Value Area |
|----------------|-------------------|
| Epic | Business |
| Feature | Business |
| User Story | Business |

**Field**: `Microsoft.VSTS.Common.ValueArea`

## Work Item Type Naming

| Markdown Type | DevOps Type | Title Format |
|--------------|-------------|--------------|
| Epic | Epic | "Epic X: Name" |
| Feature | Feature | "Feature X.Y: Name" |
| Sprint | User Story | "Sprint X.Y.Z: Name" |
