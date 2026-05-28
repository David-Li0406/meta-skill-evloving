---
name: azure-pipelines-tasks
description: Finds Azure Pipelines task implementation source code. Use when investigating task behavior, debugging pipeline issues, or understanding how built-in tasks work.
---

# Azure Pipelines Tasks Source Code

The source code for Azure DevOps built-in pipeline tasks lives in `microsoft/azure-pipelines-tasks`.

## Finding Task Source Code

Tasks are in `Tasks/<TaskName>V<Version>/` directories. The naming convention is:
- `Tasks/AzureCLIV2/` → AzureCLI@2
- `Tasks/DotNetCoreCLIV2/` → DotNetCoreCLI@2
- `Tasks/PublishBuildArtifactsV1/` → PublishBuildArtifacts@1

## Key Files in Each Task

| File | Purpose |
|------|---------|
| `task.json` | Task definition: inputs, outputs, execution entry point |
| `*.ts` or `*.ps1` | Main implementation (check `task.json` for entry point) |
| `Strings/resources.resjson/en-US/resources.resjson` | User-facing strings and error messages |
| `Tests/` | Unit tests showing expected behavior |

## Workflow

1. **Identify the task name and version** from the pipeline YAML (e.g., `AzureCLI@2`)
2. **Search the repo** for the task directory:
   ```
   gh api repos/microsoft/azure-pipelines-tasks/contents/Tasks/<TaskName>V<Version>
   ```
3. **Read `task.json`** to find the execution entry point
4. **Read the implementation file** to understand behavior

## Example: Finding AzureCLI@2 Implementation

```bash
# Get task definition
gh api repos/microsoft/azure-pipelines-tasks/contents/Tasks/AzureCLIV2/task.json

# Get main implementation
gh api repos/microsoft/azure-pipelines-tasks/contents/Tasks/AzureCLIV2/azureclitask.ts
```

## Searching for Specific Behavior

Use GitHub code search to find where specific logic is implemented:

```
repo:microsoft/azure-pipelines-tasks path:Tasks/<TaskName> <search_term>
```
