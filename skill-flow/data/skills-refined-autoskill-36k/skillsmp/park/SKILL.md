---
name: park
description: Park an idea or task in the parking lot for future elaboration. Use when encountering scope creep, interesting tangents, or features to explore later.
allowed-tools: Read, Edit
---

# Park an Idea

Add an idea to the parking lot (`PARKING_LOT.md`) without derailing current work.

## Usage

Invoke with: `/park <idea description>`

Examples:
- `/park Multi-repo support for agent coordination`
- `/park Prometheus metrics for agent pool monitoring`
- `/park E2B sandbox integration for production`

## What to Capture

When parking an idea, include:

1. **Title** - Brief descriptive name
2. **Category** - Architecture, Feature, Integration, Performance, DevOps, etc.
3. **Phase** - Which roadmap phase this belongs to (2, 3, or 4)
4. **Concept** - 2-3 sentence summary of what it is
5. **Use Cases** - Why it matters, what it enables
6. **Open Questions** - What needs to be explored

## Template

Append this to PARKING_LOT.md:

```markdown
---

## [Idea Title]

**Added:** [Today's date]
**Status:** Parked
**Category:** [Category]
**Phase:** [2/3/4]

### Concept

[2-3 sentence description of the idea]

### Use Cases

- [Use case 1]
- [Use case 2]

### Open Questions

- [ ] [Question to explore]
- [ ] [Another question]

---
```

## When to Park

- Feature requests that don't fit Phase 1
- Interesting tangents discovered during research
- Ideas from architecture discussions
- "Nice to have" improvements
- Technical debt worth tracking

## After Parking

Confirm the idea was added and summarize briefly. Don't elaborate further - the point is to capture and move on.
