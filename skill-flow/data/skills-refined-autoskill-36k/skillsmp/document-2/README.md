# Document Skill

Create and improve product documentation for Viya TMS with consistent style and structure.

## Features

- User guide templates
- API reference templates
- Release notes templates
- Viya-specific terminology and style
- Metadata for documentation management

## Quick Start

No additional setup required - this skill works out of the box with OpenCode.

```bash
# Optional: Run setup to verify configuration
./tools/setup-skills.sh document
```

## Usage

```
/document <description of what to document>
```

### Examples

```
/document the carrier integration feature in the Shipping module
/document API endpoint for creating shipments
/document release notes for version 2.5
/document how to configure rate shopping in Planning
```

## Supported Documentation Types

### 1. User Guides

Step-by-step instructions for end users.

```
/document user guide for bulk shipment import
```

**Output includes:**
- Overview and prerequisites
- Numbered step-by-step instructions
- Configuration options table
- Tips and troubleshooting

### 2. API References

Technical documentation for developers.

```
/document API endpoint POST /api/v1/shipments
```

**Output includes:**
- Endpoint and method
- Request/response examples
- Parameter tables
- Error codes
- cURL examples

### 3. Release Notes

Version changelog for product updates.

```
/document release notes for version 2.5 with new tracking dashboard
```

**Output includes:**
- Highlights summary
- New features by module
- Improvements and bug fixes
- Breaking changes and migrations
- Known issues

## Style Guidelines

The skill enforces consistent Viya documentation style:

| Element | Format | Example |
|---------|--------|---------|
| UI buttons | **Bold** | Click **Save** |
| Menu paths | **Bold** with > | **Settings > Carriers** |
| API fields | `code` | The `carrier_id` field |
| Keyboard | kbd tags | <kbd>Ctrl</kbd>+<kbd>S</kbd> |

### Terminology

| Use | Don't Use |
|-----|-----------|
| Shipment | Order, Package |
| Carrier | Courier, Transporter |
| Consignment | Grouped shipment |
| Booking | Order, Request |
| Track & Trace | Tracking |

### Voice & Tone

- Active voice: "Click the button" not "The button should be clicked"
- Address user as "you"
- Be direct and concise
- Present tense

## Output Metadata

All documentation includes frontmatter:

```yaml
---
title: Feature Name
module: planning | shipping | tracking | improving
audience: users | admins | developers
last_updated: 2026-01-13
version: 1.0
status: draft | review | published
---
```

## Viya Context

The skill understands Viya's four core modules:

| Module | Purpose |
|--------|---------|
| **Planning** | Carrier selection, rate shopping, route optimization |
| **Shipping** | Multi-carrier booking, labels, documentation |
| **Tracking** | Real-time visibility, alerts, notifications |
| **Improving** | Analytics, reporting, performance dashboards |

## Best Practices

### Structure
- Start with what, then why, then how
- Use numbered lists for sequential steps
- Use bullet lists for non-sequential items
- Keep paragraphs short (2-4 sentences)

### Completeness
- Include prerequisites
- Add configuration options
- Provide troubleshooting section
- Link to related documentation

### Maintainability
- Use metadata for tracking
- Mark TODOs clearly: `[TODO: description]`
- Include last_updated date
- Set appropriate status
