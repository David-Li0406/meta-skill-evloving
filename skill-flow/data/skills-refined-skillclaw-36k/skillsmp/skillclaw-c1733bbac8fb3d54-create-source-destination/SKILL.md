---
name: create-source-destination
description: Use this skill when creating new walkerOS sources or destinations, following an example-driven workflow that includes research and implementation.
---

# Create a New Source or Destination

## Prerequisites

Before starting, read these skills:

- [understanding-flow](../understanding-flow/SKILL.md) - How sources and destinations fit in architecture
- [understanding-sources](../understanding-sources/SKILL.md) - Source interface
- [understanding-destinations](../understanding-destinations/SKILL.md) - Destination interface
- [understanding-transformers](../understanding-transformers/SKILL.md) - Transformer chaining from sources to destinations
- [understanding-events](../understanding-events/SKILL.md) - Event structure sources and destinations emit
- [understanding-mapping](../understanding-mapping/SKILL.md) - Transform raw input to events
- [testing-strategy](../testing-strategy/SKILL.md) - How to test
- [writing-documentation](../writing-documentation/SKILL.md) - Documentation standards (for Phase 7)

## Source and Destination Types

### Source Types

| Type   | Platform | Input                   | Example                             |
| ------ | -------- | ----------------------- | ----------------------------------- |
| Web    | Browser  | DOM events, dataLayer   | `browser`, `dataLayer`              |
| Server | Node.js  | HTTP requests, webhooks | `gcp`, `express`, `lambda`, `fetch` |

### Destination Types

| Complexity | Template     | When to Use                         |
| ---------- | ------------ | ----------------------------------- |
| Simple     | `plausible/` | Single SDK call, minimal config     |
| Complex    | `gtag/`      | Multiple services, sub-destinations |
| Server     | `gcp/`       | Server-side, batching, SDK init     |

## Process Overview

### For Sources

1. Research     → Understand how sources fit into the architecture and gather input examples.
2. Choose Your Template → Select a template based on the source type and complexity.
3. Implement    → Build the source using examples as test fixtures.
4. Test         → Verify against example variations.
5. Document     → Write README.

### For Destinations

1. Research     → Find SDK, understand vendor API.
2. Examples     → Create dev entry with real usage patterns.
3. Mapping      → Define walkerOS → vendor transformation.
4. Scaffold     → Copy template and configure.
5. Implement    → Build using examples as test fixtures.
6. Test         → Verify against example variations.
7. Document     → Write README.

## Source and Destination Categories

Sources and destinations can be categorized based on their primary function:

| Category           | Purpose                                   | Examples                | Key Concern          |
| ------------------ | ----------------------------------------- | ----------------------- | -------------------- |
| **Transformation** | Convert external format → walkerOS events | `dataLayer`, `fetch`    | Mapping accuracy     |
| **Transport**      | Receive events from specific platform     | `gcp`, `aws`, `express` | Platform integration |

Many sources and destinations are both - they handle platform transport AND transform data.