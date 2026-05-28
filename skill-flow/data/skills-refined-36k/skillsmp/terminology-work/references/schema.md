# Vocabulary Package Schema

This document describes how to represent a concept system in a format that machines can read and humans can maintain.

The schema is not arbitrary. Each entity exists because it captures something that matters when terminology goes wrong. If you understand why each piece exists, you'll know when you need it and when you don't.

## The Core Entities

### Axis

An axis is a dimension along which you can divide a concept into kinds.

"Computer mouse" can be divided by tracking mechanism (optical vs. mechanical) or by connection type (wired vs. wireless). These are different axes. They're independent—knowing a mouse is optical tells you nothing about whether it's wired. They produce different sibling sets—optical and mechanical are siblings on the tracking axis; wired and wireless are siblings on the connection axis.

**Why axes exist in the schema:** Without explicit axes, people conflate them. The classic failure is an enum like `{optical, mechanical, wired, wireless}`. This looks like four options, but it's actually two independent binary choices incorrectly flattened into a list. A wireless optical mouse can't be represented. The data model encodes a false constraint.

When you define an axis, you're saying: "Here is one dimension of variation. Concepts that differ on this axis are siblings. Concepts that differ on other axes are not comparable on this one."

```json
{
  "id": "axis.tracking",
  "label": "Tracking mechanism",
  "description": "How the device detects movement"
}
```

### Characteristic

A characteristic is a property that can distinguish one concept from another.

"Movement detected by light sensors" is a characteristic. It belongs to the tracking axis. It distinguishes optical mice from mechanical mice (which detect movement by a rolling ball).

**Why characteristics exist in the schema:** Definitions are made of characteristics. If characteristics are just free text inside definitions, you can't check whether a definition uses characteristics from the wrong axis. By making characteristics explicit entities with axis assignments, cross-axis contamination becomes mechanically detectable.

A characteristic is not the same as a property. Properties are what individual objects have. Characteristics are what concepts are made of. "This particular mouse has a scratch on it" is a property. "Movement detected by light sensors" is a characteristic.

```json
{
  "id": "ch.tracking.light_sensors",
  "axisId": "axis.tracking",
  "label": "movement detected by light sensors"
}
```

### Concept

A concept is a unit of meaning. It's what a term points to.

The word "optical mouse" points to the concept of optical-mouse-ness. The concept is the idea; the word is the label. Multiple words can point to the same concept (synonyms). The same word can point to different concepts in different contexts (homonyms).

**Atomic vs. compound:** Most concepts are atomic—they're positioned on a single axis relative to their parent. An optical mouse is a kind of computer mouse, distinguished by its tracking mechanism. A compound concept sits at the intersection of multiple axes. A "wireless optical mouse" is both optical (tracking axis) and wireless (connection axis). Compounds inherit from their components.

**Status:** Concepts have confidence levels. A draft concept is captured but not yet positioned. A provisional concept has a definition but the definition might change. A stable concept has a definition that's been validated and won't change without a major version bump. Status protects downstream systems from building on sand.

```json
{
  "id": "c.mouse.optical",
  "kind": "atomic",
  "status": "stable",
  "prefLabel": "optical mouse",
  "altLabels": ["LED mouse"],
  "definitions": [...]
}
```

### Definition

A definition states what a concept is and what it's not.

The form that works: immediate parent plus distinguishing characteristics. "Optical mouse: computer mouse [parent] whose movement is detected by light sensors [distinguishing characteristic]."

The parent places the concept in the hierarchy. The distinguishing characteristic separates it from siblings on the same axis. Together, they encode position in the system.

**Why definitions have structure in the schema:** Free-text definitions drift. They accumulate qualifications. They include characteristics from other axes. They become self-contradictory. By making definitions structured—explicit parent, explicit axis, explicit characteristics—you can validate that definitions actually encode what they claim to encode.

**Scope:** A definition's scope says what kind of position it encodes:
- `root`: This concept has no parent. It's the top of its hierarchy.
- `axis`: This concept is positioned on a single axis relative to its parent.
- `multi`: This concept is a compound, positioned on multiple axes.

```json
{
  "scope": "axis",
  "axisId": "axis.tracking",
  "parentId": "c.mouse",
  "delimitingCharacteristicIds": ["ch.tracking.light_sensors"],
  "text": "computer mouse whose movement is detected by light sensors"
}
```

### Relation

A relation connects two concepts.

**Generic (kind-of):** The source is a kind of the target. Optical mouse is a kind of computer mouse. Generic relations have an axis—they say which axis the kind-of relationship is on.

**Partitive (part-of):** The source is part of the target. A button is part of a mouse. Partitive relations don't have axes—parts aren't positioned on subdivision dimensions.

**Associative:** The source and target are related but neither is a kind of or part of the other. A mouse controls a cursor. These relations need labels to say what the relationship is: `controls`, `produces`, `causes`, `uses`.

**Why relations exist as explicit entities:** The concept system is a graph. Concepts are nodes; relations are edges. Without explicit edges, the graph is implicit—you have to infer it from definitions. Explicit relations make the graph queryable, visualizable, and validatable.

```json
{
  "type": "generic",
  "sourceId": "c.mouse.optical",
  "targetId": "c.mouse",
  "axisId": "axis.tracking"
}
```

### Mapping

A mapping connects a concept to its implementation.

Concepts live in the world of meaning. Implementation lives in the world of databases, APIs, enums, fields. The gap between them is permanent. Mappings make the gap explicit.

**Mapping types:**
- `exact`: 1:1 correspondence. The concept and the implementation represent the same thing.
- `partial`: The concept maps to part of the implementation, or the implementation contains more than this concept.
- `composite`: Multiple concepts combine into one implementation artifact.
- `derived`: The implementation is computed from the concept rather than stored directly.
- `lossy`: Information is lost in the mapping. You can't recover the concept from the implementation alone.

**Why mappings exist in the schema:** Implementation compromises meaning. A database field can't store nuance. An enum can't represent a continuous spectrum. A boolean can't represent three states. Every time you implement a concept, you lose something.

If the loss is invisible, bugs hide. Data means something in the concept system but something else in the database. Code written against the database diverges from the intended meaning. The mapping ledger makes the loss visible—you can see exactly where meaning is compromised and what the compromise costs.

```json
{
  "conceptId": "c.mouse.optical",
  "artifact": "products.tracking_type='optical'",
  "mappingType": "exact",
  "notes": null,
  "sinceVersion": "2.0.0",
  "owner": "inventory-team"
}
```

## The Full Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "VocabularyPackage",
  "type": "object",
  "required": ["vocab", "concepts"],
  "properties": {
    "vocab": {
      "type": "object",
      "required": ["id", "version"],
      "properties": {
        "id": { 
          "type": "string",
          "description": "Stable identifier for this vocabulary"
        },
        "version": { 
          "type": "string", 
          "pattern": "^\\d+\\.\\d+\\.\\d+$",
          "description": "Semver version"
        },
        "releasedAt": { 
          "type": "string", 
          "format": "date" 
        },
        "status": { 
          "enum": ["draft", "internal", "published"],
          "description": "Whether this vocabulary is ready for external use"
        },
        "purpose": { 
          "type": "string",
          "description": "What problem this vocabulary solves"
        },
        "domain": { 
          "type": "string",
          "description": "Subject area covered"
        }
      }
    },
    "axes": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "label"],
        "properties": {
          "id": { "type": "string", "pattern": "^axis\\." },
          "label": { "type": "string" },
          "description": { "type": "string" }
        }
      }
    },
    "characteristics": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "axisId", "label"],
        "properties": {
          "id": { "type": "string", "pattern": "^ch\\." },
          "axisId": { "type": "string" },
          "label": { "type": "string" }
        }
      }
    },
    "concepts": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "status", "prefLabel"],
        "properties": {
          "id": { "type": "string", "pattern": "^c\\." },
          "kind": { "enum": ["atomic", "compound"], "default": "atomic" },
          "status": { "enum": ["draft", "provisional", "stable"] },
          "prefLabel": { "type": "string" },
          "altLabels": { "type": "array", "items": { "type": "string" } },
          "deprecatedLabels": { "type": "array", "items": { "type": "string" } },
          "components": {
            "type": "array",
            "description": "For compound concepts: which atomic concepts this intersects",
            "items": {
              "type": "object",
              "required": ["axisId", "conceptId"],
              "properties": {
                "axisId": { "type": "string" },
                "conceptId": { "type": "string" }
              }
            }
          },
          "definitions": {
            "type": "array",
            "items": {
              "type": "object",
              "required": ["text"],
              "properties": {
                "scope": { "enum": ["axis", "multi", "root"], "default": "axis" },
                "axisId": { "type": ["string", "null"] },
                "parentId": { "type": ["string", "null"] },
                "delimitingCharacteristicIds": {
                  "type": "array",
                  "items": { "type": "string" }
                },
                "text": { "type": "string" }
              }
            }
          },
          "notes": {
            "type": "object",
            "properties": {
              "scope": { "type": "string", "description": "What this concept includes/excludes" },
              "history": { "type": "string", "description": "How this concept has evolved" },
              "editorial": { "type": "string", "description": "Internal notes for maintainers" }
            }
          }
        }
      }
    },
    "relations": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["type", "sourceId", "targetId"],
        "properties": {
          "type": { "enum": ["generic", "partitive", "associative"] },
          "sourceId": { "type": "string" },
          "targetId": { "type": "string" },
          "axisId": { "type": ["string", "null"] },
          "label": { "type": "string", "description": "For associative: what kind of relationship" }
        }
      }
    },
    "mappings": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["conceptId", "artifact", "mappingType"],
        "properties": {
          "conceptId": { "type": "string" },
          "artifact": { "type": "string", "description": "What this maps to: table.column, endpoint.field, enum value" },
          "mappingType": { "enum": ["exact", "partial", "composite", "derived", "lossy"] },
          "notes": { "type": "string", "description": "What's lost or compromised" },
          "sinceVersion": { "type": "string" },
          "plannedMigration": { "type": "boolean" },
          "owner": { "type": "string" }
        }
      }
    }
  }
}
```

## When You Need Each Piece

**You always need:**
- `vocab`: Identification and version
- `concepts`: The things you're defining
- At least one `definition` per concept with `status: stable`

**You need `axes` when:**
- The same parent concept can be subdivided multiple ways
- You want to prevent cross-axis contamination in definitions
- You want to validate that siblings are actually comparable

**You need `characteristics` when:**
- You want to mechanically validate that definitions don't mix axes
- Multiple concepts share the same distinguishing feature
- You want to track which features are definitional vs. incidental

**You need `relations` when:**
- You want to visualize the concept system as a graph
- You want to query ancestors, descendants, or related concepts
- You have associative relationships (cause-effect, tool-action) that matter

**You need `mappings` when:**
- Concepts are implemented in databases, APIs, or code
- The implementation doesn't perfectly match the concept
- You need to track where meaning is compromised
- You need to plan migrations

## Export Formats

The JSON schema above is the canonical format. Generate other formats as needed:

**SKOS (RDF):** For publishing to semantic web infrastructure. Use `skos:Concept`, `skos:broader`, `skos:narrower`, `skos:related`. Axes don't have a direct SKOS equivalent; use `skos:inScheme` with multiple scheme URIs or a custom property.

**CSV:** For spreadsheet consumers. Flatten to one row per concept. Loses structure but gains accessibility.

**SQL:** For seeding reference tables. Generate INSERT statements or COPY data.

**OpenAPI:** For API contracts. Generate enum schemas from concepts that share a parent and axis.

The vocabulary package is the source of truth. Exports are derived. When the package changes, regenerate exports.
