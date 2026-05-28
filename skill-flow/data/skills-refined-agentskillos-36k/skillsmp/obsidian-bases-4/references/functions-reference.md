# Functions Reference

Quick reference for Obsidian Bases functions. For complete documentation, see: https://help.obsidian.md/bases/functions

## Global Functions

Used without a type qualifier.

| Function | Syntax | Description |
|----------|--------|-------------|
| `date()` | `date("2025-05-27")` | Parse string as date object |
| `today()` | `today()` | Current date (time = 00:00) |
| `now()` | `now()` | Current date and time |
| `duration()` | `duration("1d")`, `duration("2h")` | Parse duration string |
| `link()` | `link("path")`, `link("path", "display")` | Create link object |
| `if()` | `if(condition, trueResult, falseResult)` | Conditional expression |
| `max()` | `max(value1, value2, ...)` | Largest of values |
| `min()` | `min(value1, value2, ...)` | Smallest of values |
| `number()` | `number("3.14")` | Parse as number |
| `list()` | `list(value)` | Wrap in list (or return if already list) |
| `icon()` | `icon("arrow-right")` | Create icon (Lucide names) |
| `image()` | `image(path)` | Create image object |
| `file()` | `file("path")` | Get file object |
| `html()` | `html("<div>...</div>")` | Render HTML |
| `escapeHTML()` | `escapeHTML(string)` | Escape HTML characters |

## Date Functions

Called on date objects.

### Fields

```yaml
date.year          # Year (2026)
date.month         # Month (1-12)
date.day           # Day of month
date.hour          # Hour (0-23)
date.minute        # Minute (0-59)
date.second        # Second (0-59)
date.millisecond   # Millisecond (0-999)
```

### Methods

| Function | Syntax | Description |
|----------|--------|-------------|
| `format()` | `date.format("YYYY-MM-DD")` | Format using Moment.js format string |
| `date()` | `datetime.date()` | Remove time component |
| `time()` | `datetime.time()` | Get time as string |
| `relative()` | `date.relative()` | Human-readable relative time ("3 days ago") |
| `isEmpty()` | `date.isEmpty()` | Always false |

### Date Arithmetic

```yaml
today() + "1d"              # Add 1 day
now() - "2h"                # Subtract 2 hours
due + "1w"                  # Add 1 week
meeting_date - "30m"        # Subtract 30 minutes
(date1 - date2)             # Milliseconds between dates
```

Duration units: `y|year|years`, `M|month|months`, `w|week|weeks`, `d|day|days`, `h|hour|hours`, `m|minute|minutes`, `s|second|seconds`

## String Functions

Called on text values.

### Fields

```yaml
string.length      # Character count
```

### Methods

| Function | Syntax | Description |
|----------|--------|-------------|
| `contains()` | `string.contains("text")` | Check if contains substring |
| `containsAll()` | `string.containsAll("a", "b")` | Contains all substrings |
| `containsAny()` | `string.containsAny("a", "b")` | Contains any substring |
| `startsWith()` | `string.startsWith("prefix")` | Starts with string |
| `endsWith()` | `string.endsWith("suffix")` | Ends with string |
| `lower()` | `string.lower()` | Convert to lowercase |
| `upper()` | `string.upper()` | Convert to uppercase |
| `title()` | `string.title()` | Title Case Each Word |
| `trim()` | `string.trim()` | Remove leading/trailing whitespace |
| `split()` | `string.split(",")`, `string.split(",", 3)` | Split into list |
| `replace()` | `string.replace("old", "new")` | Replace occurrences |
| `repeat()` | `string.repeat(3)` | Repeat string N times |
| `reverse()` | `string.reverse()` | Reverse string |
| `slice()` | `string.slice(1, 4)` | Extract substring |
| `isEmpty()` | `string.isEmpty()` | Check if empty |

## Number Functions

Called on numeric values.

| Function | Syntax | Description |
|----------|--------|-------------|
| `abs()` | `number.abs()` | Absolute value |
| `ceil()` | `number.ceil()` | Round up |
| `floor()` | `number.floor()` | Round down |
| `round()` | `number.round()`, `number.round(2)` | Round to integer or N decimals |
| `toFixed()` | `number.toFixed(2)` | Format with N decimal places (returns string) |
| `isEmpty()` | `number.isEmpty()` | Check if null/undefined |

## List Functions

Called on array values.

### Fields

```yaml
list.length        # Number of elements
```

### Methods

| Function | Syntax | Description |
|----------|--------|-------------|
| `contains()` | `list.contains(value)` | Check if contains element |
| `containsAll()` | `list.containsAll(v1, v2)` | Contains all elements |
| `containsAny()` | `list.containsAny(v1, v2)` | Contains any element |
| `filter()` | `list.filter(value > 2)` | Filter elements (uses `value`, `index` vars) |
| `map()` | `list.map(value + 1)` | Transform elements (uses `value`, `index` vars) |
| `reduce()` | `list.reduce(acc + value, 0)` | Reduce to single value (uses `acc`, `value`, `index`) |
| `sort()` | `list.sort()` | Sort ascending |
| `reverse()` | `list.reverse()` | Reverse order |
| `unique()` | `list.unique()` | Remove duplicates |
| `flat()` | `list.flat()` | Flatten nested lists |
| `join()` | `list.join(", ")` | Join into string |
| `slice()` | `list.slice(1, 3)` | Extract portion |
| `isEmpty()` | `list.isEmpty()` | Check if empty |

## File Functions

Called on file objects.

### Fields

```yaml
file.name          # Filename with extension
file.basename      # Filename without extension
file.path          # Full path from vault root
file.folder        # Parent folder path
file.ext           # File extension
file.size          # Size in bytes
file.ctime         # Created time (date)
file.mtime         # Modified time (date)
file.properties    # Object of all properties
file.tags          # List of tags (includes inline)
file.links         # List of internal links
file.backlinks     # List of backlinks (expensive!)
```

### Methods

| Function | Syntax | Description |
|----------|--------|-------------|
| `asLink()` | `file.asLink()`, `file.asLink("display")` | Convert to link object |
| `hasLink()` | `file.hasLink(otherFile)` | Check if links to file/path |
| `hasTag()` | `file.hasTag("tag1", "tag2")` | Has any of these tags (includes nested) |
| `hasProperty()` | `file.hasProperty("name")` | Has property defined |
| `inFolder()` | `file.inFolder("folder/path")` | In folder or subfolder |

## Link Functions

Called on link objects.

| Function | Syntax | Description |
|----------|--------|-------------|
| `asFile()` | `link.asFile()` | Get file object (if valid local file) |
| `linksTo()` | `link.linksTo(file)` | Check if links to file |

## Object Functions

Called on objects.

| Function | Syntax | Description |
|----------|--------|-------------|
| `keys()` | `object.keys()` | List of keys |
| `values()` | `object.values()` | List of values |
| `isEmpty()` | `object.isEmpty()` | Check if empty |

## Regular Expression

| Function | Syntax | Description |
|----------|--------|-------------|
| `matches()` | `/pattern/.matches("text")` | Check if regex matches |

## Any Type Functions

Work on any value.

| Function | Syntax | Description |
|----------|--------|-------------|
| `toString()` | `any.toString()` | Convert to string |
| `isType()` | `any.isType("string")` | Check type |
| `isTruthy()` | `any.isTruthy()` | Convert to boolean |

## Operators

### Arithmetic

`+` (add), `-` (subtract), `*` (multiply), `/` (divide), `%` (modulo), `( )` (grouping)

### Comparison

`==` (equals), `!=` (not equal), `>` (greater), `<` (less), `>=` (greater or equal), `<=` (less or equal)

### Boolean

`!` (not), `&&` (and), `||` (or)

## Special Variables

### In filters and formulas

```yaml
this             # Current file (when base embedded)
this.file        # Current file object
file             # Note being evaluated
```

### In list.filter() and list.map()

```yaml
value            # Current element
index            # Current index (0-based)
```

### In list.reduce()

```yaml
acc              # Accumulator
value            # Current element
index            # Current index
```

### In summary formulas

```yaml
values           # List of all values for the property
```

## Common Patterns

### Null-safe access

```yaml
'property ? property.method() : ""'
'list ? list.length : 0'
'date ? date.format("YYYY-MM-DD") : "No date"'
```

### Type checking

```yaml
'value.isType("number")'
'value.isType("string")'
'value.isType("date")'
```

### List filtering

```yaml
list.filter(value > threshold)
list.filter(value.contains("text"))
file.backlinks.filter(x => x.type == "task")
```

### List mapping

```yaml
tags.map(t => t.replace("prefix/", ""))
list.map(x => x.toUpperCase())
```

### List reducing

```yaml
# Sum
list.reduce(acc + value, 0)

# Max
list.reduce(if(acc == null || value > acc, value, acc), null)

# Count matching
list.reduce(acc + (value.contains("text") ? 1 : 0), 0)
```

## Performance Considerations

**Expensive operations** (avoid in formulas):
- `file.backlinks` - Scans entire vault for links
- `file.properties` - Loads all properties

**Better alternatives**:
- Use `file.hasLink(target)` instead of checking backlinks
- Access specific properties directly instead of `file.properties`
- Filter at folder level before complex operations
- Use `limit` in views to reduce processing

**Caching**:
- File properties auto-refresh
- Note properties update on file save
- Backlinks may need manual refresh
