---
name: document
description: Create and improve product documentation for Viya TMS. Supports user guides, feature docs, API references, and release notes with consistent style and structure.
---

# Documentation Skill

Create and improve product documentation for Viya TMS (Transport Management System). Ensures consistent style, structure, and terminology across all documentation.

## Trigger

When user asks to:
- Write documentation for a feature
- Create a user guide
- Document an API endpoint
- Write release notes
- Improve existing documentation

## Context: Viya TMS

Viya is a Transport Management System (TMS) with four core modules:
- **Planning**: Carrier selection, rate shopping, route optimization
- **Shipping**: Multi-carrier booking, label generation, documentation
- **Tracking**: Real-time visibility, exception alerts, notifications
- **Improving**: Analytics, reporting, performance dashboards

Target audience: B2B logistics teams, shipping managers, IT integrators.

## Process

### Step 1: Understand the Documentation Need

Clarify with user:
1. **Type**: User guide | Feature doc | API reference | Release notes | FAQ
2. **Audience**: End users | Administrators | Developers | All
3. **Module**: Planning | Shipping | Tracking | Improving | Platform-wide
4. **Scope**: New doc | Update existing | Improve/rewrite

### Step 2: Check Existing Documentation

Search for related documentation:
```javascript
memory({ mode: "search", query: "<feature/topic>", tags: ["documentation", "viya"] })
```

Check if there's existing content to build upon or maintain consistency with.

### Step 3: Gather Feature Information

For new features, gather:
- Feature name and module
- User problem it solves
- How it works (workflow/steps)
- Configuration options
- Related features
- Screenshots/diagrams needed

Ask clarifying questions if information is incomplete.

### Step 4: Select Template

Choose the appropriate template based on documentation type:

#### User Guide Template
```markdown
# [Feature Name]

Brief description of what this feature does and why it matters.

## Overview

Explain the feature's purpose and benefits in 2-3 sentences.

## Prerequisites

- Required permissions
- Required configuration
- Related features that should be set up first

## How to [Action]

### Step 1: [Action verb]

Description of what to do.

1. Navigate to **Module > Section**
2. Click **Button Name**
3. Fill in the required fields:
   - **Field Name**: Description of what to enter
   - **Field Name**: Description of what to enter

### Step 2: [Action verb]

Continue with next steps...

## Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| Option name | What it controls | Default value |

## Tips

- Tip for better usage
- Common best practice

## Troubleshooting

### Issue: [Common problem]

**Solution**: How to resolve it.

## Related Features

- [Related Feature 1](./related-feature-1.md)
- [Related Feature 2](./related-feature-2.md)
```

#### API Reference Template
```markdown
# [Endpoint Name]

Brief description of what this endpoint does.

## Endpoint

```
METHOD /api/v1/resource
```

## Authentication

Required authentication method and permissions.

## Request

### Headers

| Header | Required | Description |
|--------|----------|-------------|
| Authorization | Yes | Bearer token |
| Content-Type | Yes | application/json |

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | string | Yes | Resource identifier |

### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| limit | integer | No | Maximum results (default: 50) |

### Request Body

```json
{
  "field": "value",
  "nested": {
    "field": "value"
  }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| field | string | Yes | Description |

## Response

### Success (200 OK)

```json
{
  "id": "abc123",
  "status": "success",
  "data": {}
}
```

### Error Responses

| Code | Description |
|------|-------------|
| 400 | Bad request - invalid parameters |
| 401 | Unauthorized - invalid or missing token |
| 404 | Resource not found |

## Example

```bash
curl -X POST https://api.viya.me/v1/resource \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"field": "value"}'
```

## Related Endpoints

- [GET /api/v1/resource](./get-resource.md)
- [DELETE /api/v1/resource](./delete-resource.md)
```

#### Release Notes Template
```markdown
# Release Notes - [Version]

**Release Date**: YYYY-MM-DD

## Highlights

Brief summary of the most important changes in 2-3 sentences.

## New Features

### [Feature Name]

Description of the new feature and its benefits.

**Module**: Planning | Shipping | Tracking | Improving

**How to use**: Brief instructions or link to documentation.

## Improvements

- **[Area]**: Description of improvement
- **[Area]**: Description of improvement

## Bug Fixes

- Fixed issue where [description of bug and fix]
- Resolved problem with [description]

## Breaking Changes

### [Change Name]

**What changed**: Description of the breaking change.

**Migration**: Steps to update.

## Deprecations

- **[Feature/API]**: Will be removed in version X. Use [alternative] instead.

## Known Issues

- [Issue description] - Workaround: [workaround]
```

### Step 5: Write Documentation

Follow these style guidelines:

**Voice & Tone**
- Use active voice: "Click the button" not "The button should be clicked"
- Be direct and concise
- Address user as "you"
- Use present tense

**Formatting**
- Use **bold** for UI elements: **Save**, **Settings**, **Planning**
- Use `code` for technical values: `shipment_id`, `POST`, `null`
- Use > blockquotes for important notes or warnings
- Keep paragraphs short (2-4 sentences)

**Terminology**
- Shipment (not order/package)
- Carrier (not courier/transporter)
- Consignment (for grouped shipments)
- Booking (not order/request)
- Track & Trace (for tracking feature)

**Structure**
- Start with what, then why, then how
- Use numbered lists for sequential steps
- Use bullet lists for non-sequential items
- Include examples for complex concepts

### Step 6: Add Metadata

Include frontmatter for documentation management:

```yaml
---
title: Feature Name
module: planning | shipping | tracking | improving
audience: users | admins | developers
last_updated: YYYY-MM-DD
version: 1.0
status: draft | review | published
---
```

### Step 7: Review Checklist

Before finishing, verify:
- [ ] Clear title and introduction
- [ ] All steps are numbered and actionable
- [ ] Screenshots/diagrams are referenced (if needed)
- [ ] Terminology is consistent with Viya standards
- [ ] Links to related documentation included
- [ ] Metadata is complete

### Step 8: Store in Memory

After creating documentation, store reference:
```javascript
memory({
  mode: "add",
  content: "Documentation: [title] - [brief description]",
  scope: "project",
  tags: ["documentation", "viya", "<module>"]
})
```

## Output to User

Provide:
1. The complete documentation content
2. Suggested file location (if applicable)
3. Any missing information that should be added
4. Related documentation that may need updates

## Style Quick Reference

| Element | Example |
|---------|---------|
| UI button | **Save Changes** |
| Menu path | **Settings > Carriers > Add New** |
| API field | `carrier_id` |
| Keyboard | <kbd>Ctrl</kbd>+<kbd>S</kbd> |
| Warning | > **Warning**: This action cannot be undone. |
| Tip | > **Tip**: You can also use keyboard shortcuts. |

## Error Handling

If information is incomplete:
- Ask specific clarifying questions
- Provide placeholder text marked with `[TODO: description]`
- Note what's missing in the output

If conflicting information exists:
- Note the conflict
- Ask user to clarify
- Document the decision made
