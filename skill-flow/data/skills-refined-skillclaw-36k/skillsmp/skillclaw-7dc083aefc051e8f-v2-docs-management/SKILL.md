---
name: v2-docs-management
description: Use this skill to manage and review V2 transaction MDX documentation for coverage, accuracy, and quality.
---

# Skill body

## Introduction
This skill orchestrates the management and review of V2 transaction MDX documentation files located in `content/docs/protocol/v2/transactions/`. It tracks documentation coverage, identifies gaps, and facilitates the review process to ensure accuracy and completeness.

## When Invoked

1. **Scan Documentation Directory**
   - List all MDX files in `content/docs/protocol/v2/transactions/`
   - Compare against expected transactions from `v2-transaction-tracker.json`
   - Identify missing, outdated, or misaligned documentation

2. **Display Coverage Dashboard**
   - Show summary: X documented, Y missing, Z needs update
   - List transactions by system (global, instance, course, project)
   - Highlight path misalignments between current and expected paths

3. **Identify Work Needed**
   - List transactions with no MDX file
   - List transactions with path misalignment (legacy paths)
   - List transactions that need content review (outdated info)

4. **Prompt for Action**
   - Offer to run `/v2-docs-review` for specific transactions
   - Offer to migrate files to correct paths
   - Offer to create missing documentation stubs

## Review Individual Documentation

1. **Identify Transaction**
   - User specifies transaction ID (e.g., `course.student.enroll`)
   - Look up in `v2-docs-tracker.json` for current state

2. **Gather Sources**
   - Read the YAML source file (if exists)
   - Read the current MDX file (if exists)
   - Read `address-registry.json` for validator names

3. **Perform Review**
   - Compare MDX content against YAML
   - Check all required sections are present
   - Verify accuracy of costs, endpoints, schemas
   - Note any discrepancies

4. **Generate Report**
   - List what's correct
   - List what's missing
   - List what's incorrect
   - Provide specific fixes needed

5. **Offer Actions**
   - Create new MDX if missing
   - Update existing MDX with fixes
   - Migrate file to correct path if needed

## Commands

| Command | Description |
|---------|-------------|
| `/v2-docs-audit` | Show dashboard and coverage status |
| `/v2-docs-audit scan` | Rescan documentation directory |
| `/v2-docs-audit status` | Show summary counts only |
| `/v2-docs-audit next` | Suggest next documentation task |
| `/v2-docs-review <id>` | Run review for specific transaction |
| `/v2-docs-review <id> --fix` | Update existing MDX with fixes |
| `/v2-docs-review <id> --create` | Create new MDX if missing |
| `/v2-docs-review <id> --migrate` | Migrate file to correct path if needed |

## Documentation Statuses

| Status | Meaning |
|--------|---------|
| `missing` | No MDX file exists for this transaction |
| `path-mismatch` | MDX exists but at wrong path (needs migration) |
| `needs-review` | MDX exists but content may be outdated |
| `reviewed` | MDX reviewed and content is current |
| `verified` | MDX verified against live API documentation |

## Status Flow

```
missing → created → needs-review → reviewed → verified
                         ↑              ↓
path-mismatch → m
```