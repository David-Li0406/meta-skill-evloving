---
name: azure-devops
description: Use this skill when you need to automate tasks in Azure DevOps, including managing boards, repositories, pipelines, and artifacts.
---

# Skill body

This skill provides comprehensive guidance for Azure DevOps automation through purpose-built Python CLI tools that handle:

### Work Items (Boards)
- Create work items with HTML-formatted descriptions.
- Update work items (state, assignments, fields).
- Delete work items with confirmation.
- Link parent-child relationships between work items.
- Execute WIQL queries to retrieve work items.

### Repositories
- List repositories.
- Create pull requests.

### Pipelines
- Manage Azure pipelines.

### Artifacts
- Handle Azure artifacts.

**Auto-activates when:** User mentions Azure DevOps, ADO, work items, boards, repos, pipelines, artifacts, or Azure DevOps URLs.

## Tools Required
- `.claude/scenarios/az-devops-tools/auth_check.py`
- `.claude/scenarios/az-devops-tools/create_work_item.py`
- `.claude/scenarios/az-devops-tools/update_work_item.py`
- `.claude/scenarios/az-devops-tools/delete_work_item.py`
- `.claude/scenarios/az-devops-tools/get_work_item.py`
- `.claude/scenarios/az-devops-tools/list_work_items.py`
- `.claude/scenarios/az-devops-tools/link_parent.py`
- `.claude/scenarios/az-devops-tools/query_wiql.py`
- `.claude/scenarios/az-devops-tools/format_html.py`
- `.claude/scenarios/az-devops-tools/list_types.py`
- `.claude/scenarios/az-devops-tools/list_repos.py`
- `.claude/scenarios/az-devops-tools/create_pr.py`

## References
- [Azure DevOps CLI Documentation](https://learn.microsoft.com/en-us/cli/azure/devops)
- [az boards work-item Commands](https://learn.microsoft.com/en-us/cli/azure/boards/work-item)
- [Work Items REST API](https://learn.microsoft.com/en-us/rest/api/azure/devops/wit/work-items)
- [WIQL Syntax Reference](https://learn.microsoft.com/en-us/azure/devops/boards/queries/wiql-syntax)
- [Work Item Fields](https://learn.microsoft.com/en-us/azure/devops/boards/work-items/work-item-fields)
- [Link Types Reference](https://learn.microsoft.com/en-us/azure/devops/boards/queries/link-type-reference)

## Supporting Documents
- authentication.md
- work-items.md
- queries.md
- html-formatting.md
- repos.md
- pipelines.md
- artifacts.md
- HOW_TO_CREATE_YOUR_OWN.md