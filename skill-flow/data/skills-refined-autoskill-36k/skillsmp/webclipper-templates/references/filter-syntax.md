# Web Clipper Filter Syntax Reference

## Basic Syntax

```
{{variable|filter}}
{{variable|filter1|filter2}}           # Chained (applied left to right)
{{variable|filter:"argument"}}         # With argument
{{variable|filter:("arg1","arg2")}}    # Multiple arguments
```

---

## Date Filters

### `date`
Convert date to format. Uses [Day.js format tokens](https://day.js.org/docs/en/display/format).

```
{{date|date:"YYYY-MM-DD"}}              # 2025-01-12
{{date|date:"YYYY-MM-DD HH:mm"}}        # 2025-01-12 14:30
{{published|date:"YYYY"}}               # 2025
```

With input format:
```
"12/01/2024"|date:("YYYY-MM-DD", "MM/DD/YYYY")  # 2024-12-01
```

### `date_modify`
Add/subtract time from date.

```
"2024-12-01"|date_modify:"+1 year"      # 2025-12-01
"2024-12-01"|date_modify:"- 2 months"   # 2024-10-01
```

### `duration`
Convert ISO 8601 duration or seconds to formatted time.

```
"PT1H30M"|duration:"HH:mm:ss"           # 01:30:00
"3665"|duration:"H:mm:ss"               # 1:01:05
```

---

## Text Filters

### Case Conversion
```
{{title|lower}}                         # lowercase
{{title|upper}}                         # UPPERCASE
{{title|capitalize}}                    # Hello world
{{title|title}}                         # Hello World
{{title|camel}}                         # camelCase
{{title|pascal}}                        # PascalCase
{{title|kebab}}                         # kebab-case
{{title|snake}}                         # snake_case
```

### `trim`
Remove whitespace from both ends.
```
"  hello world  "|trim                  # "hello world"
```

### `safe_name`
Convert to safe filename. **Always pair with `|trim`**.
```
{{title|safe_name|trim}}
```

### `replace`
Replace text occurrences.

**Simple replacement:**
```
{{text|replace:",":""}}                 # Remove commas
{{text|replace:"old":"new"}}            # Replace old with new
```

**Multiple replacements:**
```
{{text|replace:("e":"a","o":"0")}}      # hall0 w0rld
```

**CRITICAL: Escaping special characters**

In the **search term**, escape these with `\`:
- `:` → `\:`
- `|` → `\|`
- `{` `}` → `\{` `\}`
- `(` `)` → `\(` `\)`
- `'` `"` → `\'` `\"`

**CRITICAL: URLs require regex syntax**

Plain URL replacement BREAKS because of `://`:
```
# WRONG - causes import failure
{{field|replace:"https://schema.org/":""}}
```

Use regex instead:
```
# CORRECT - regex avoids colon parsing
{{field|replace:"/https:\/\/schema\.org\//":""}}
```

**Regex syntax:**
```
{{text|replace:"/[aeiou]/g":"*"}}       # h*ll* w*rld (replace all vowels)
{{text|replace:"/hello/i":"hi"}}        # Case-insensitive
```

Regex flags: `g` (global), `i` (case-insensitive), `m` (multiline), `s` (dotAll), `u` (unicode), `y` (sticky)

---

## Array Filters

### `first` / `last`
```
["a","b","c"]|first                     # "a"
["a","b","c"]|last                      # "c"
```

### `join`
```
["a","b","c"]|join                      # "a,b,c"
["a","b","c"]|join:" "                  # "a b c"
["a","b","c"]|join:"\n"                 # Multi-line
```

### `split`
```
"a,b,c"|split:","                       # ["a","b","c"]
```

### `slice`
```
"hello"|slice:1,4                       # "ell"
["a","b","c","d"]|slice:1,3             # ["b","c"]
```

### `unique`
Remove duplicates from array.

### `map`
Transform array elements.
```
[{gem: "obsidian"}, {gem: "amethyst"}]|map:item => item.gem
# ["obsidian", "amethyst"]
```

---

## Formatting Filters

### `list`
Convert array to Markdown list.
```
{{items|list}}                          # Bullet list
{{items|list:task}}                     # Task list
{{items|list:numbered}}                 # Numbered list
```

### `table`
Convert to Markdown table.

### `link`
Create Markdown link.
```
{{url|link:"Click here"}}               # [Click here](url)
```

### `wikilink`
Create Obsidian wikilink.
```
{{page|wikilink}}                       # [[page]]
{{page|wikilink:"alias"}}               # [[page|alias]]
```

### `image`
Create Markdown image.
```
{{url|image:"alt text"}}                # ![alt text](url)
```

### `blockquote`
Add `>` prefix to each line.

### `callout`
Create Obsidian callout.
```
{{text|callout:("info", "Title", false)}}
```

---

## HTML Processing

### `markdown`
Convert HTML to Obsidian-flavored Markdown.
```
{{contentHtml|markdown}}
```

### `strip_tags`
Remove all HTML tags (keep content).
```
{{html|strip_tags}}
{{html|strip_tags:("p","strong")}}      # Keep specific tags
```

### `strip_md`
Remove all Markdown formatting.

---

## Number Filters

### `length`
```
"hello"|length                          # 5
["a","b","c"]|length                    # 3
```

### `round`
```
3.7|round                               # 4
3.14159|round:2                         # 3.14
```

### `calc`
```
5|calc:"+10"                            # 15
2|calc:"**3"                            # 8
```

---

## Schema Variables

Access structured data from web pages:
```
{{schema:@Article:author.name}}
{{schema:@Book:aggregateRating.ratingValue}}
{{schema:@Event:startDate|date:"YYYY-MM-DD"}}
{{schema:@JobPosting:hiringOrganization.name}}
{{schema:@Movie:duration|replace:"PT":""|replace:"H":"h "|replace:"M":"m"}}
```

## Meta Variables

Access page metadata:
```
{{meta:property:og:title}}
{{meta:property:og:image}}
{{meta:property:og:site_name}}
{{meta:property:article:published_time}}
```

## Built-in Variables

```
{{title}}                               # Page title
{{url}}                                 # Page URL
{{domain}}                              # Domain name
{{date}}                                # Current date
{{time}}                                # Current time
{{content}}                             # Page content (Markdown)
{{contentHtml}}                         # Page content (HTML)
{{author}}                              # Author if detected
{{published}}                           # Published date if detected
{{highlights}}                          # User highlights
{{words}}                               # Word count
```
