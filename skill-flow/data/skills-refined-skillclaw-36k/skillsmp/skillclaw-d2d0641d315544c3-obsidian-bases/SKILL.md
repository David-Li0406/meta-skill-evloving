---
name: obsidian-bases
description: Use this skill when creating or editing Obsidian Bases (.base files) to manage dynamic views of notes with properties, filters, formulas, and multiple layouts.
---

# Obsidian Bases Skill

This skill enables users to create and edit valid Obsidian Bases (`.base` files) that define dynamic views of notes in an Obsidian vault. A Base file can contain multiple views, global filters, formulas, property configurations, and custom summaries.

## Overview

Obsidian Bases are YAML-based files that allow users to create database-like views of notes. They can be embedded in Markdown code blocks and support various configurations.

## File Format

Base files use the `.base` extension and contain valid YAML. The basic structure includes:

```yaml
filters:
  and: []
views:
  - type: table | cards | list | map
    name: "View Name"
    limit: 10                    # Optional: limit results
    groupBy:                     # Optional: group results
      property: property_name
      direction: ASC | DESC
    filters:                     # View-specific filters
      and: []
    order:                       # Properties to display in order
      - file.name
      - property_name
      - formula.formula_name
    summaries:                   # Map properties to summary formulas
      property_name: Average
```

## Quick Start

### Create a Base File

Use Command Palette → "Bases: Create new base" or right-click a folder → "New base".

### Embed a Base

Use `![[File.base]]` or `![[File.base#ViewName]]` in any note.

### Inline Base Queries

You can write inline queries in code blocks:

````markdown
```base
filters:
  and:
    - file.hasTag("example")
views:
  - type: table
    name: Results
```
````

## Core Concepts

### Properties

1. **Note Properties** - Accessed via frontmatter YAML (e.g., `property` or `note.property`).
2. **File Properties** - Built-in fields (e.g., `file.name`, `file.mtime`).
3. **Formula Properties** - Calculated fields (e.g., `formula.formula_name`).

### Filters

Filters can be applied globally or per view using boolean logic:

```yaml
filters:
  and:
    - file.inFolder("Database/Tasks")
    - status == "active"
  or:
    - priority == "urgent"
    - due < today()
  not:
    - assignee == null
```

### Formulas

Define calculated properties:

```yaml
formulas:
  is_overdue: due && due < today() && status == "active"
  days_until: 'due ? (due - today()).format("days") : ""'
  price_total: "price * quantity"
```

### Views

Multiple views can be defined per base with different layouts:

- **Table** - Rows and columns (default).
- **Cards** - Gallery grid with optional images.
- **List** - Bulleted or numbered lists.
- **Map** - Interactive map with pins (requires Maps plugin).

## Conclusion

Use this skill to effectively manage and visualize your notes in Obsidian using Bases, enhancing your productivity and organization.