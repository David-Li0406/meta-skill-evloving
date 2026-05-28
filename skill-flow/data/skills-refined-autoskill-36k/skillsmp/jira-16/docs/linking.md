# Linking Jira Tickets

Complete guide to linking Jira tickets together using the `link_ticket.py` script.

## Overview

Issue links connect related Jira tickets, showing relationships like "blocks", "duplicates", or "relates to". This helps teams understand dependencies and track related work.

## Quick Start

```bash
# List available link types
python3 scripts/link_ticket.py --list-types

# View existing links on a ticket
python3 scripts/link_ticket.py PROJ-123 --list

# Create a link
python3 scripts/link_ticket.py PROJ-123 PROJ-456 "Blocks"
```

## Understanding Link Types

Each link type has two directions:

| Link Type | Outward (Source) | Inward (Target) |
|-----------|------------------|-----------------|
| Blocks | "blocks" | "is blocked by" |
| Duplicate | "duplicates" | "is duplicated by" |
| Relates | "relates to" | "relates to" |
| Cloners | "clones" | "is cloned by" |

When you run:
```bash
python3 scripts/link_ticket.py PROJ-123 PROJ-456 "Blocks"
```

The result is:
- PROJ-123 **blocks** PROJ-456
- PROJ-456 **is blocked by** PROJ-123

## Commands

### List Available Link Types

See all link types configured in your Jira instance:

```bash
python3 scripts/link_ticket.py --list-types
```

**Example Output:**
```
Available Link Types:
============================================================

  Blocks (ID: 10000)
    Outward: "blocks"
    Inward:  "is blocked by"

  Duplicate (ID: 10001)
    Outward: "duplicates"
    Inward:  "is duplicated by"

  Relates (ID: 10003)
    Outward: "relates to"
    Inward:  "relates to"
```

### View Existing Links

See all links on a specific ticket:

```bash
python3 scripts/link_ticket.py PROJ-123 --list
```

**Example Output:**
```
PROJ-123: Implement user authentication
============================================================

Links (2):

  [12345] blocks:
    PROJ-456: Add login form
    Status: In Progress

  [12346] relates to:
    PROJ-789: Security audit
    Status: Done
```

### Create a Link

Link two tickets together:

```bash
# Basic link
python3 scripts/link_ticket.py SOURCE TARGET "Link Type"

# Examples
python3 scripts/link_ticket.py PROJ-123 PROJ-456 "Blocks"
python3 scripts/link_ticket.py BUG-100 BUG-101 "Duplicate"
python3 scripts/link_ticket.py FEAT-50 FEAT-51 "Relates"
```

### Create Link with Comment

Add a comment explaining why tickets are linked:

```bash
python3 scripts/link_ticket.py PROJ-123 PROJ-456 "Blocks" --comment "Must complete auth before login form"
```

The comment is added to the **target** (inward) issue.

### Preview with Dry Run

See what would happen without making changes:

```bash
python3 scripts/link_ticket.py PROJ-123 PROJ-456 "Blocks" --dry-run
```

**Example Output:**
```
Source: PROJ-123: Implement user authentication
Target: PROJ-456: Add login form

Link Type: Blocks
  PROJ-123 blocks PROJ-456
  PROJ-456 is blocked by PROJ-123

Dry run: No changes made
```

### Remove a Link

Delete an existing link by its ID (found using `--list`):

```bash
# First, find the link ID
python3 scripts/link_ticket.py PROJ-123 --list

# Then remove it
python3 scripts/link_ticket.py PROJ-123 --remove 12345
```

## Natural Language Patterns

When using the Jira skill, these phrases trigger linking:

| User Says | Action |
|-----------|--------|
| "link PROJ-123 to PROJ-456" | Prompt for link type |
| "PROJ-123 blocks PROJ-456" | Create Blocks link |
| "PROJ-123 duplicates PROJ-456" | Create Duplicate link |
| "relate PROJ-123 and PROJ-456" | Create Relates link |
| "show links for PROJ-123" | List existing links |
| "what link types are available" | List link types |
| "remove link 12345 from PROJ-123" | Delete link |

## Common Workflows

### Blocking Dependency

When one ticket must be completed before another:

```bash
# PROJ-100 must be done before PROJ-101 can start
python3 scripts/link_ticket.py PROJ-100 PROJ-101 "Blocks"
```

### Mark Duplicate

When two tickets describe the same issue:

```bash
# BUG-200 is a duplicate of BUG-150
python3 scripts/link_ticket.py BUG-200 BUG-150 "Duplicate"
```

### Related Work

When tickets are related but not dependent:

```bash
python3 scripts/link_ticket.py FEAT-50 FEAT-51 "Relates"
```

## Error Handling

### Unknown Link Type

```
Error: Unknown link type 'Blockers'

Use --list-types to see available link types
```

**Solution:** Check spelling or use `--list-types` to see exact names.

### Link Not Found

```
Error: Link ID 99999 not found on PROJ-123

Use --list to see existing links and their IDs
```

**Solution:** Use `--list` to find the correct link ID.

### Ticket Not Found (404)

```
Error: HTTP 404: Issue does not exist or you do not have permission to see it.
```

**Solution:** Verify ticket key and your access permissions.

### Authentication Error (401)

```
Error: HTTP 401: Basic authentication with passwords is deprecated.
```

**Solution:** Regenerate your API token at:
https://id.atlassian.com/manage-profile/security/api-tokens

## Script Reference

**Location:** `scripts/link_ticket.py`

**Arguments:**

| Argument | Description |
|----------|-------------|
| `SOURCE` | Source issue key (outward direction) |
| `TARGET` | Target issue key (inward direction) |
| `LINK_TYPE` | Link type name (required for creating) |

**Options:**

| Option | Description |
|--------|-------------|
| `--list-types` | List available link types |
| `--list, -l` | List existing links on SOURCE |
| `--remove, -r ID` | Remove link by ID |
| `--comment, -c MSG` | Add comment when linking |
| `--dry-run, -n` | Preview without changes |
| `--site HOSTNAME` | Override Atlassian site |

## Environment Variables

```bash
ATLASSIAN_EMAIL="your.email@company.com"
ATLASSIAN_API_TOKEN="ATATT..."
ATLASSIAN_SITE="yoursite.atlassian.net"
```
