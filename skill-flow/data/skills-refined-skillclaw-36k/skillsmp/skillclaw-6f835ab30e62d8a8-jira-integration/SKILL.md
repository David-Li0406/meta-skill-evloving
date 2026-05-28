---
name: jira-integration
description: Use this skill when you need to synchronize SpecWeave increments with JIRA epics and stories, including setup guidance and troubleshooting for the integration.
---

# Skill body

## Overview

This skill facilitates the mapping and synchronization of SpecWeave increments to JIRA, ensuring bidirectional sync of content and status while maintaining traceability across systems.

## Core Responsibilities

1. **Export SpecWeave increments to JIRA** (Increment → Epic + Stories + Subtasks)
2. **Import JIRA epics as SpecWeave increments** (Epic → Increment structure)
3. **Sync**: Content flows from SpecWeave to JIRA, and status flows from JIRA to SpecWeave.
4. **Maintain traceability** (store keys, URLs, timestamps).
5. **Validate mapping accuracy** using test cases.
6. **Handle edge cases** (missing fields, invalid statuses, API errors).
7. **Provide guidance** on JIRA sync setup and troubleshooting.

## Concept Mappings

### SpecWeave → JIRA

| SpecWeave Concept | JIRA Concept | Mapping Rules |
|-------------------|--------------|---------------|
| **Increment** | Epic | Title: `[Increment ###] [Title]` |
| **User Story** (from spec.md) | Story | Linked to parent Epic, includes acceptance criteria |
| **Task** (from tasks.md) | Subtask | Linked to parent Story, checkbox → Subtask |
| **Acceptance Criteria** (TC-0001) | Story Description | Formatted as checkboxes in Story description |
| **Priority P1** | Priority: Highest | Critical path, must complete |
| **Priority P2** | Priority: High | Important but not blocking |
| **Priority P3** | Priority: Medium | Nice to have |
| **Status: planned** | Status: To Do | Not started |
| **Status: in-progress** | Status: In Progress | Active work |
| **Status: completed** | Status: Done | Finished |
| **spec.md** | Epic Description | Summary + link to spec (if GitHub repo) |
| **context-manifest.yaml** | Custom Field: Context | Serialized YAML in custom field (optional) |

### JIRA → SpecWeave

| JIRA Concept | SpecWeave Concept | Import Rules |
|--------------|-------------------|--------------|
| **Epic** | Increment | Auto-number next available (e.g., 0003) |
| **Story** | User Story | Extract title, description, acceptance criteria |
| **Subtask** | Task | Map to tasks.md checklist |
| **Story Description** | Acceptance Criteria | Parse checkboxes as TC-0001, TC-0002 |
| **Epic Link** | Parent Increment | Maintain parent-child relationships |
| **Priority: Highest** | Priority P1 | Critical |

## Sync Guidance

### When to Activate

✅ **Do activate when**:
- User asks: "How do I set up JIRA sync?"
- User asks: "What JIRA credentials do I need?"
- User asks: "How does JIRA sync work?"
- User needs help configuring JIRA integration.

❌ **Do NOT activate when**:
- User invokes `/sw-jira:sync` command (command handles it).
- Command is already running (avoid duplicate invocation).
- Task completion hook is syncing (automatic process).

### Critical: Secrets Required (Mandatory Check)

**BEFORE attempting JIRA sync, CHECK for JIRA credentials.**

#### Step 1: Check If Credentials Exist

```bash
# Check .env file for both required credentials
if [ -f .env ] && grep -q "JIRA_API_TOKEN" .env && grep -q "JIRA_EMAIL" .env; then
  echo "✅ JIRA credentials found"
else
  # Credentials NOT found - STOP and prompt user
fi
```

#### Step 2: If Credentials Missing, STOP and Show This Message

```
🔐 **JIRA API Token and Email Required**

I need your JIRA API token and email to sync with JIRA.

**How to get it**:
1. Go to: https://id.atlassian.com/manage-profile/security/api-tokens
2. Log in with your Atlassian account.
3. Click "Create API token".
4. Give it a label (e.g., "specweave-sync").
5. Click "Create".
6. **Copy the token immediately** (you can't see it again!).

**Where I'll save it**:
- File: `.env` (gitignored, secure).
- Format:
  ```
  JIRA_API_TOKEN=your-jira-api-token-here
  JIRA_EMAIL=your-email@example.com
  JIRA_DOMAIN=your-domain.atlassian.net
  ```

**Security**:
✅ .env is in .gitignore.