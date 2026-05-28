# Migration Templates

Terminology changes break things. When you change what a concept means, code that depended on the old meaning does the wrong thing. When you split one concept into two, code that expected one value gets two. When you merge two concepts into one, code that distinguished them loses a distinction it needed.

Migration templates exist to communicate changes to downstream systems in a form they can act on. The human notes explain what changed and why. The machine manifest provides a structured record that tooling can process.

## What Counts as a Breaking Change

Not all changes break things. The question is: does the change invalidate assumptions that downstream code might reasonably hold?

### Breaking changes

**Splitting a concept:** One concept becomes two or more. Code that stored, queried, or compared the single value must now handle multiple values. If a database column held "mouse_type" and you split it into "tracking_mechanism" and "connection_type," every query against that column breaks.

**Merging concepts:** Two or more concepts become one. Code that distinguished them loses a distinction. If you merge "trial_user" and "free_user" into "unpaid_user," code that behaved differently for trials and free users can no longer tell them apart.

**Changing intension:** A concept's definition changes. Code that assumed the old meaning now has a false assumption. If "customer" used to mean "anyone who purchased" and now means "anyone who has an active subscription," code that treated past purchasers as customers is wrong.

**Changing hierarchy:** A concept moves to a different parent. Code that traversed ancestors or filtered by hierarchy gets different results. If "trackball" moves from being a sibling of "mouse" to being a kind of "mouse," hierarchical queries behave differently.

**Removing a concept:** A concept is deleted without replacement. Code that references it breaks. This is obviously breaking, but often handled poorly because the temptation is to remove the concept from the vocabulary without checking what depends on it.

### Non-breaking changes

**Adding a concept:** New concepts don't break existing code because nothing depends on them yet. Consumers can ignore new concepts until they're ready to use them.

**Adding a synonym:** A new label for an existing concept. The concept's meaning doesn't change, so code based on the meaning still works.

**Fixing a typo:** Label corrections don't change meaning. Code shouldn't depend on exact spelling anyway.

**Adding notes or examples:** Documentation improvements don't affect programmatic use.

**Adding relations:** New relations between existing concepts. These enrich the graph but don't change what individual concepts mean.

The distinction matters because breaking changes require migration support. Non-breaking changes require communication but not action.

## Human Migration Notes

Human notes explain changes to people who need to understand and respond. They should answer:

- What changed?
- Why?
- Who's affected?
- What do they need to do?
- When?

### Template

```markdown
# [Vocabulary Name] v[Version] Migration Guide

Released: [Date]
Previous version: [Previous Version]

## Summary

[One paragraph explaining the overall nature of this release. Is it routine maintenance? A significant restructuring? A response to discovered problems?]

## Breaking Changes

[For each breaking change, include:]

### [Short title describing the change]

**What changed:** [Concrete description of the structural change]

**Why:** [The problem this change solves or the reason it's necessary]

**Impact:** [Which systems, teams, or workflows are affected]

**Migration steps:**

1. [Specific action]
2. [Specific action]
3. [Verification step]

**Deadline:** [If there's a date by which migration must complete]

**Fallback:** [What to do if migration can't complete in time]

---

## Deprecations

[For items that are deprecated but not yet removed:]

### [Deprecated item]

**Deprecated:** [What's being deprecated]
**Replacement:** [What to use instead]
**Removal planned:** [Version when it will be removed]
**Migration:** [How to move to the replacement]

---

## Additions

[Brief list of new concepts, axes, or relations. These don't require migration but consumers may want to use them.]

- [New item]: [One-line description]

---

## Notes

[Any additional context, caveats, or explanations that didn't fit above]

---

## Support

[Who to contact with questions]
```

### Example

```markdown
# Pointing Devices Vocabulary v2.0.0 Migration Guide

Released: 2026-02-05
Previous version: 1.3.0

## Summary

This release fixes a structural problem in how mouse types were classified. The previous `mouse_type` concept conflated two independent dimensions: how a mouse detects movement (tracking mechanism) and how it connects to a computer (connection type). A wireless optical mouse couldn't be represented because the data model only allowed one value.

Version 2.0.0 introduces explicit axes for tracking mechanism and connection type. This is a breaking change for all systems that store or query `mouse_type`.

## Breaking Changes

### mouse_type split into tracking_mechanism and connection_type

**What changed:** The single `mouse_type` concept (with values: optical, mechanical, wireless, wired) has been replaced by two concepts: `tracking_mechanism` (optical, mechanical, laser) and `connection_type` (wired, wireless).

**Why:** The previous structure conflated orthogonal dimensions. A wireless optical mouse couldn't be represented—the enum forced a choice between "optical" and "wireless" when both are true.

**Impact:** 
- Database: `products.mouse_type` column
- API: `/products` response `type` field
- Reports: Any report grouping by mouse type

**Migration steps:**

1. Add new columns: `tracking_mechanism VARCHAR, connection_type VARCHAR`
2. Backfill using this logic:
   ```sql
   UPDATE products SET
     tracking_mechanism = CASE 
       WHEN mouse_type IN ('optical', 'mechanical') THEN mouse_type
       ELSE NULL END,
     connection_type = CASE
       WHEN mouse_type IN ('wireless', 'wired') THEN mouse_type
       ELSE NULL END;
   ```
3. Update API responses to include both fields
4. Update reports to group by the appropriate axis
5. Verify data integrity: no product should have both columns NULL (unless it's not a mouse)
6. Deprecate the `mouse_type` field in API v1; remove in v3

**Deadline:** API consumers must migrate by 2026-04-01 when v1 API is deprecated.

**Fallback:** Legacy API endpoint will continue returning `mouse_type` for v1 consumers. Contact the platform team if you can't migrate by deadline.

---

## Deprecations

### mouse_type

**Deprecated:** `c.mouse.type` concept and all implementations
**Replacement:** `c.mouse.tracking.*` and `c.mouse.connection.*` concepts
**Removal planned:** v3.0.0 (estimated Q3 2026)
**Migration:** See breaking change above

---

## Additions

- `axis.tracking`: Tracking mechanism axis (optical, mechanical, laser)
- `axis.connection`: Connection type axis (wired, wireless)
- `c.mouse.laser`: Laser mouse (tracking axis)
- `c.mouse.wireless_optical`: Compound concept for wireless optical mice

---

## Support

Questions: #terminology-help Slack channel
Migration assistance: platform-team@company.com
```

## Machine Migration Manifest

The machine manifest provides the same information in a structured format that tooling can process. Automated migration scripts can read the manifest to know what changes to make. Validation tools can check whether migrations have been applied.

### Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "MigrationManifest",
  "type": "object",
  "required": ["fromVersion", "toVersion", "releasedAt"],
  "properties": {
    "fromVersion": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$",
      "description": "Version this manifest migrates from"
    },
    "toVersion": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$",
      "description": "Version this manifest migrates to"
    },
    "releasedAt": {
      "type": "string",
      "format": "date"
    },
    "breaking": {
      "type": "array",
      "description": "Changes that require consumer action",
      "items": { "$ref": "#/definitions/BreakingChange" }
    },
    "deprecated": {
      "type": "array",
      "description": "Items deprecated in this version",
      "items": { "$ref": "#/definitions/Deprecation" }
    },
    "added": {
      "type": "object",
      "description": "New items in this version",
      "properties": {
        "concepts": { "type": "array", "items": { "type": "string" } },
        "axes": { "type": "array", "items": { "type": "string" } }
      }
    }
  },
  "definitions": {
    "BreakingChange": {
      "type": "object",
      "required": ["type", "description", "action"],
      "properties": {
        "type": {
          "enum": ["split", "merge", "redefine", "reparent", "remove"],
          "description": "Category of breaking change"
        },
        "from": {
          "description": "Concept(s) being changed",
          "oneOf": [
            { "type": "string" },
            { "type": "array", "items": { "type": "string" } }
          ]
        },
        "to": {
          "description": "Concept(s) resulting from change",
          "oneOf": [
            { "type": "string" },
            { "type": "array", "items": { "type": "string" } }
          ]
        },
        "description": {
          "type": "string",
          "description": "What changed and why"
        },
        "action": {
          "type": "string",
          "description": "What consumers must do"
        },
        "dataMigration": {
          "type": "string",
          "description": "SQL or pseudocode for data transformation"
        },
        "deadline": {
          "type": "string",
          "format": "date",
          "description": "When migration must complete"
        }
      }
    },
    "Deprecation": {
      "type": "object",
      "required": ["item", "replacement", "removeIn"],
      "properties": {
        "item": { "type": "string", "description": "What's deprecated" },
        "replacement": {
          "description": "What to use instead",
          "oneOf": [
            { "type": "string" },
            { "type": "array", "items": { "type": "string" } }
          ]
        },
        "removeIn": { "type": "string", "description": "Version when item will be removed" }
      }
    }
  }
}
```

### Example

```json
{
  "fromVersion": "1.3.0",
  "toVersion": "2.0.0",
  "releasedAt": "2026-02-05",
  "breaking": [
    {
      "type": "split",
      "from": "c.mouse.type",
      "to": ["axis.tracking", "axis.connection"],
      "description": "mouse_type conflated tracking mechanism and connection type; split into independent axes",
      "action": "Replace mouse_type with tracking_mechanism and connection_type fields",
      "dataMigration": "tracking_mechanism = CASE WHEN mouse_type IN ('optical','mechanical') THEN mouse_type END; connection_type = CASE WHEN mouse_type IN ('wireless','wired') THEN mouse_type END",
      "deadline": "2026-04-01"
    }
  ],
  "deprecated": [
    {
      "item": "c.mouse.type",
      "replacement": ["axis.tracking", "axis.connection"],
      "removeIn": "3.0.0"
    }
  ],
  "added": {
    "concepts": [
      "c.mouse.optical",
      "c.mouse.mechanical", 
      "c.mouse.laser",
      "c.mouse.wired",
      "c.mouse.wireless",
      "c.mouse.wireless_optical"
    ],
    "axes": [
      "axis.tracking",
      "axis.connection"
    ]
  }
}
```

## Version Numbering

Use semantic versioning. The version number communicates the nature of changes:

**Major (X.0.0):** Breaking changes. Consumers must take action.

**Minor (x.Y.0):** Additions and deprecations. Consumers can benefit from new features but aren't forced to change.

**Patch (x.y.Z):** Fixes that don't change meaning. Label corrections, documentation improvements.

The version number is a promise. A minor bump promises that existing consumers won't break. A major bump warns that they might. Don't lie—if a change is breaking, it's a major bump even if the change seems small.

## Process

When preparing a release:

1. **Identify all changes since last release.** Use diff against previous vocabulary package.

2. **Classify each change.** Breaking, deprecation, or addition? Use the criteria above.

3. **If any breaking changes exist, bump major version.** Otherwise, bump minor or patch as appropriate.

4. **Write human migration notes.** For each breaking change, document impact and migration steps.

5. **Generate machine manifest.** Include all breaking changes and deprecations.

6. **Communicate.** Notify affected teams. Give them time to migrate before deadline.

7. **Support.** Be available to help with migration questions.

The goal is not to minimize change. Terminology needs to evolve as understanding deepens. The goal is to make change safe by making it predictable, documented, and supported.
