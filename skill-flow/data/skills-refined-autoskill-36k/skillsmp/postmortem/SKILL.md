---
name: postmortem
description: Write incident postmortems for homelab infrastructure. Proactively invoke when you notice the user has been debugging a significant issue and finally resolves it, when troubleshooting reveals a surprising root cause or wrong assumption, or when an incident is mentioned in passing that sounds worth documenting. Suggest writing a postmortem rather than waiting to be asked.
---

# Postmortem Skill

Create blameless, learning-focused incident documentation for homelab infrastructure.

## Core Principles

1. **Construction, not purification** - Build knowledge, don't flagellate
2. **Blameless means systems-focused** - "How did the system allow this?" not "Who did this?"
3. **Contributing factors, not root cause** - Complex failures have multiple causes
4. **Be concrete** - Specific times, commands, errors
5. **Name the mental model** - What assumption was wrong?
6. **Action items must be actionable** - Specific, bounded, completable
7. **Surface what helped and where you got lucky** - Mitigators and near-misses reveal future risks
8. **Keep it simple enough to actually write** - A short postmortem is better than none

## When to Write a Postmortem

Write postmortems for principled matters - issues that reveal something about process, architecture, or mental models. Skip for trivial one-off errors that were immediately caught.

Good candidates:
- Outages or service degradation
- Incidents that took significant time to debug
- Near-misses that could have been worse
- Recurring issues (even if individually minor)
- Situations where assumptions proved wrong

## File Naming Convention

Use the format: `YYYY-MM-DD-HHMM-slug.md`

- **YYYY-MM-DD**: Date of the incident
- **HHMM**: Time (24h format) when the postmortem was written
- **slug**: Brief kebab-case description

Examples:
- `2026-01-25-1923-metallb-hairpin-nat.md`
- `2026-01-25-1745-sops-flux-decryption-failure.md`

This enables automatic sorting by date/time in the mkdocs nav (newest first).

## Template Usage

Copy the template from `template.md` to the user's postmortem location. The template includes:

- **Frontmatter**: Metadata for searchability (date, systems, tags, severity, commit link)
- **Timeline**: Concrete sequence of events with timestamps
- **What Happened**: Narrative description respecting decision context at the time
- **Contributing Factors**: Multiple causes (never singular "root cause")
- **What I Was Wrong About**: Mental models and assumptions that failed
- **What Helped / What Could Have Been Worse**: Mitigators and near-misses
- **Is This a Pattern?**: Distinguishes one-off errors from systemic issues
- **Action Items**: Specific, bounded, completable tasks
- **Lessons**: Key takeaways for future reference

## Writing Guidelines

### Timeline
Use consistent timezone (CST recommended). Include:
- First indication of problem
- When investigation began
- Key discoveries or decision points
- Resolution applied
- Confirmed resolved

### What Happened
Write narrative prose, not bullet points. Describe what the situation looked like at each stage - what information was available, what decisions were made based on that information. Avoid hindsight bias.

### Contributing Factors
List all conditions that combined to cause the incident. Resist the urge to pick a single "root cause." Ask: "If this factor had been different, would the incident still have happened?"

### What I Was Wrong About
This section is often the most valuable. Name specific assumptions or mental models that proved incorrect. Examples:
- "I assumed the config would reload automatically"
- "I thought opt1 mapped to the IoT VLAN"
- "I expected the rollback to be instant"

### Is This a Pattern?
Ask: Is this a one-off mistake within a sound approach, or does the approach itself need to change?
- One-off: Fix and move on
- Pattern: Document what needs to change at a higher level

### Action Items
Each item should be:
- Specific (not "be more careful")
- Bounded (clear scope and completion criteria)
- Actionable (something that can actually be done)

## Example

See `example.md` for a filled-in postmortem demonstrating these principles.
