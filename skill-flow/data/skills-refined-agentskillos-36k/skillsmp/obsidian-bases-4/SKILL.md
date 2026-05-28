---
name: obsidian-bases
description: "Work with Obsidian Bases - a native database system for creating dynamic views of notes using properties, filters, formulas, and multiple view layouts (table, cards, list, map). Use when creating or editing .base files, writing Base queries in code blocks, working with Database/ folder schemas (Tasks, Projects, People, Companies, Meetings, Bookmarks), defining formulas or filters, setting up views and relationships, or answering questions about Bases syntax and features."
---

# Obsidian Bases

Create and manage database-like views of notes using Obsidian Bases, including the standardized Database/ folder schemas.

## Quick Start

### Create a base file

Use Command Palette → "Bases: Create new base" or right-click folder → "New base".

Basic structure:
```yaml
filters:
  and:
    - file.inFolder("Database/Tasks")
    - status == "active"
views:
  - type: table
    name: Active Tasks
    order:
      - priority
      - due
```

### Embed a base

Use `![[File.base]]` or `![[File.base#ViewName]]` in any note.

### Inline base queries

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

Three types of properties:

1. **Note properties** - Frontmatter YAML (access as `property` or `note.property`)
2. **File properties** - Built-in fields (`file.name`, `file.mtime`, `file.size`, etc.)
3. **Formula properties** - Calculated fields (`formula.formula_name`)

### Filters

Apply to all views or specific views. Use boolean logic (`and`, `or`, `not`):

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

Use in filters: `formula.is_overdue`

### Views

Multiple views per base with different layouts:

- **table** - Rows and columns (default)
- **cards** - Gallery grid with optional images
- **list** - Bulleted or numbered lists
- **map** - Interactive map with pins (requires Maps plugin)

## Database/ Folder Schemas

See [references/database-schemas.md](references/database-schemas.md) for complete property definitions and relationship patterns for:

- **Tasks** - Task management (`status`, `priority`, `assignee`, `project`, `due`)
- **Projects** - Project tracking (`lead`, `team`, `target_date`, completion metrics)
- **People** - CRM contacts (`company`, `role`, `email`, contact tracking)
- **Companies** - Organizations (`industry`, `stage`, `relationship`)
- **Meetings** - Meeting notes (`attendees`, `meeting_date`, `project`, `company`)
- **Bookmarks** - URL management (`url`, `category`, `saved`, `rating`)

## Common Patterns

### Filter by folder and type

```yaml
filters:
  and:
    - file.inFolder("Database/Tasks")
    - type == "task"
```

### Group by property

```yaml
views:
  - type: table
    name: Tasks by Priority
    groupBy:
      property: priority
      direction: DESC
```

### Reference current file with `this`

```yaml
filters:
  and:
    - project == link(this.file)  # Tasks for current project
    - file.hasLink(this.file)     # Files linking here
```

### Create relationships

```yaml
# In task frontmatter
assignee: "[[Database/People/Team-Member]]"
project: "[[Database/Projects/AGI-Assistant]]"
```

Query related data:
```yaml
filters:
  and:
    - file.inFolder("Database/Tasks")
    - project == link("Database/Projects/AGI-Assistant")
```

### Date arithmetic

```yaml
formulas:
  deadline: start_date + "2w"
  is_overdue: due_date < now() && status != "Done"
  days_ago: '(today() - file.ctime).format("days")'
```

### Conditional display

```yaml
formulas:
  status_indicator: 'if(completed, "✅", "⏳")'
  formatted_price: 'if(price, "$" + price.toFixed(2), "")'
```

### List operations

```yaml
formulas:
  tag_count: tags.length
  first_tag: tags[0]
  has_urgent: tags.contains("urgent")
```

## View Configuration

### Table view

```yaml
views:
  - type: table
    name: My View
    limit: 50
    order:
      - priority
      - due
    groupBy:
      property: status
      direction: ASC
    summaries:
      file.name: Count
      price: Sum
```

### Cards view

```yaml
views:
  - type: cards
    name: Gallery
    cardSize: medium
    imageProperty: cover
    imageFit: cover
    imageAspectRatio: "16:9"
```

### List view

```yaml
views:
  - type: list
    name: Task List
    markers: bullets  # bullets, numbers, or none
    indentProperties: true
    separator: ", "
```

## Common Formulas

See [references/formula-examples.md](references/formula-examples.md) for extensive examples.

Quick reference:

```yaml
# Date calculations
due_in_days: '(due - today()).format("days")'
overdue: due < today() && status == "active"
age_in_days: '(today() - file.ctime).format("days")'

# Text formatting
full_name: first_name + " " + last_name
display_title: file.name.title()
domain: 'url.split("/")[2]'

# Number calculations
total: price * quantity
percent: '(part / whole * 100).toFixed(1) + "%"'

# Conditional logic
priority_score: '(impact * urgency) / effort'
status_emoji: 'status == "done" ? "✅" : "⏳"'
```

## Functions Reference

See [references/functions-reference.md](references/functions-reference.md) for complete function list.

Common functions:

**Global**: `if()`, `now()`, `today()`, `date()`, `link()`, `max()`, `min()`

**String**: `contains()`, `replace()`, `split()`, `lower()`, `title()`, `trim()`

**Number**: `round()`, `ceil()`, `floor()`, `abs()`, `toFixed()`

**Date**: `format()`, `relative()`, `date()`, `time()`

**List**: `filter()`, `map()`, `sort()`, `join()`, `unique()`, `contains()`

**File**: `hasTag()`, `hasLink()`, `inFolder()`, `hasProperty()`

## Best Practices

### File organization

- Keep .base files in the folder they query
- Use `Database/` folder for centralized data
- Name files descriptively: `Tasks.base`, `Active-Projects.base`

### Property naming

- Use lowercase with underscores: `due_date`, `last_contact`
- Reserve `type` for entity classification
- Prefix formulas: `formula.is_overdue`

### Filter optimization

- Apply folder filters at global level (applies to all views)
- Apply specific filters at view level
- Use file properties before note properties (faster)

### Formula design

- Keep formulas simple and readable
- Use meaningful names: `days_until_due` not `calc1`
- Handle null values: `if(price, price.toFixed(2), "")`
- Avoid circular references

### View structure

- First view is default when embedding
- Name views descriptively: "Active Tasks by Priority"
- Use grouping for categorical data
- Add summaries for numeric columns

## Syntax Reference

### Operators

**Arithmetic**: `+`, `-`, `*`, `/`, `%`, `( )`

**Comparison**: `==`, `!=`, `>`, `<`, `>=`, `<=`

**Boolean**: `!`, `&&`, `||`

### Property access

```yaml
property          # Note property (shorthand)
note.property     # Note property (explicit)
file.name         # File property
formula.calc      # Formula property
property.subprop  # Object property (dot notation)
property[0]       # List element
```

### Links

```yaml
link("path")                    # Create link
link("path", "display")         # Link with display text
link("path", icon("plus"))      # Link with icon
assignee == link(this.file)     # Compare link to current file
authors.contains(this)          # Check if list contains link
```

## Troubleshooting

**Base not showing data**
- Check filter logic (use advanced editor to debug)
- Verify folder paths are correct
- Ensure property names match frontmatter

**Formula not calculating**
- Check for circular references
- Verify property types match operators
- Use `if()` to handle null values

**View not updating**
- File properties auto-refresh
- Note properties require file save
- Backlinks may need manual refresh

**Performance issues**
- Avoid `file.backlinks` in formulas (expensive)
- Use `file.hasLink()` instead of checking backlinks
- Limit results with `limit` property
- Filter at folder level first

## Migration from Dataview

Dataview query:
```js
TABLE status, priority, due
FROM "Tasks"
WHERE status = "active"
SORT priority DESC
```

Equivalent Base:
```yaml
filters:
  and:
    - file.inFolder("Tasks")
    - status == "active"
views:
  - type: table
    name: Active Tasks
    order:
      - priority
```

Key differences:
- No `FROM` - use `file.inFolder()` filter
- No `TABLE` - properties selected in UI
- `WHERE` → `filters`
- `SORT` → `order`
- `=` → `==`
- Function syntax: `contains()` not `contains`

## Additional Resources

- Official Docs: https://help.obsidian.md/bases
- [Database Schemas](references/database-schemas.md) - Complete property definitions
- [Formula Examples](references/formula-examples.md) - Real-world formula patterns
- [Functions Reference](references/functions-reference.md) - Complete function list
