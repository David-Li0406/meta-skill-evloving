---
name: linked-spaces
description: Use when configuring cross-space access, sharing context between spaces, delegating tasks to other agents, or setting up agent-to-agent communication
---

# Linked Spaces

Connect spaces to share context and delegate tasks between agents.

## When to Use

- Accessing files or context from another space
- Delegating tasks to a specialized agent in another space
- Building workflows that span multiple spaces
- Sharing knowledge across related projects

## Link Configuration

Add to `.manifest/app.json`:

```json
{
  "links": [
    {
      "space": "Research",
      "access": "readonly",
      "reason": "Access research findings"
    },
    {
      "space": "DevOps",
      "access": "a2a",
      "reason": "Delegate deployment tasks"
    }
  ]
}
```

## Access Levels

| Level | Description |
|-------|-------------|
| `readonly` | Read files and context from linked space |
| `a2a` | Agent-to-agent delegation (can send tasks) |

### Readonly Access

Agent can:
- Read files from linked space
- Access guidelines and knowledge
- Include linked context in system prompt

Agent cannot:
- Write to linked space
- Send messages to linked agent
- Modify linked space configuration

### A2A Access

Agent can:
- Everything in readonly, plus:
- Delegate tasks to linked space's agent
- Receive results from delegated tasks
- Coordinate multi-space workflows

## Link Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `space` | string | Yes | Space name or ID |
| `access` | string | Yes | `readonly` or `a2a` |
| `reason` | string | Yes | Why this link exists |

## Context Aggregation

Linked spaces automatically contribute to agent context:

1. **Guidelines**: Merged into system prompt
2. **Files**: Available via LinkedSpacesService
3. **Knowledge**: Searchable across linked spaces

## Example: Multi-Space Workflow

**Career space** links to Research for company intel:

```json
{
  "space": { "name": "Career", "icon": "briefcase.fill" },
  "links": [
    {
      "space": "Research",
      "access": "readonly",
      "reason": "Access company research for interview prep"
    }
  ]
}
```

**Project space** links to DevOps for deployments:

```json
{
  "space": { "name": "WebApp", "icon": "globe" },
  "links": [
    {
      "space": "DevOps",
      "access": "a2a",
      "reason": "Delegate deployments and infrastructure"
    },
    {
      "space": "Design",
      "access": "readonly",
      "reason": "Access design system and assets"
    }
  ]
}
```

## File Access from Linked Spaces

Via LinkedSpacesService:

```swift
// Get files from linked space
let files = try await linkedSpaces.files(
    from: "Research",
    sourceSpace: currentSpace,
    path: "companies"
)

// Read specific file
let content = try await linkedSpaces.readFile(
    from: "Research",
    sourceSpace: currentSpace,
    path: "companies/acme-notes.md"
)
```

## System Prompt Integration

Linked context appears in agent's system prompt:

```
## Linked Spaces

You have access to context from the following linked spaces:
- Research
- Design

### Guidelines from Linked Spaces

# From: Research

Focus on actionable insights...

---

# From: Design

Follow the design system tokens...
```

## Delegation (A2A)

For spaces with `a2a` access:

```swift
// Check if delegation allowed
let canDelegate = try await linkedSpaces.canDelegate(
    from: sourceSpace,
    to: "DevOps"
)

// Get delegatable spaces
let targets = try await linkedSpaces.delegatableSpaces(from: sourceSpace)
```

## Best Practices

| Practice | Reason |
|----------|--------|
| Always include `reason` | Documents why link exists |
| Use `readonly` by default | Principle of least privilege |
| Only use `a2a` when needed | Delegation has overhead |
| Link bidirectionally if needed | Links are one-way |

## Security

- Path traversal prevented (stays within linked space)
- Access verified on every operation
- Links cached but validated against manifest
- A2A requires explicit delegation capability

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Link not found | Verify space name matches exactly |
| Access denied | Check access level in link config |
| Missing context | Ensure guidelines.md exists in linked space |
| Can't delegate | Upgrade to `a2a` access level |
