# Web Clipper Template Troubleshooting

## "Error importing template"

This generic error appears when the Web Clipper parser can't understand the template JSON.

### Most Common Cause: URLs in Replace Filters

**Problem:**
```json
"{{schema:@Event:eventStatus|replace:\"https://schema.org/\":\"\"}}"
```

The `://` in URLs breaks the parser because `:` is used as a separator in filter syntax.

**Solution: Use regex syntax**
```json
"{{schema:@Event:eventStatus|replace:\"/https:\\/\\/schema\\.org\\//:\"\"}}\"
```

### Other Causes

1. **Invalid JSON syntax** - Use `jq` to validate:
   ```bash
   cat template.json | jq . > /dev/null && echo "Valid" || echo "Invalid"
   ```

2. **Unescaped special characters in replace filters**
   Characters that need escaping in search term: `: | { } ( ) ' "`

3. **Missing required fields** - Ensure you have:
   - `schemaVersion`
   - `name`
   - `noteNameFormat`
   - `noteContentFormat`

---

## Template imports but creates wrong filename

### Cause: Missing `|trim` filter

**Problem:**
```json
"noteNameFormat": "{{title|safe_name}}"
```

Trailing whitespace from the page title ends up in the filename.

**Solution:**
```json
"noteNameFormat": "{{title|safe_name|trim}}"
```

---

## Markdown tables are broken

### Cause: Aggressive pipe cleaning

If you have code that strips spaces around `|` characters, it will break markdown table syntax.

**Problem regex (DON'T USE):**
```javascript
content.replace(/\|\s+(\w)/g, '|$1')  // Breaks tables!
```

This turns `| Calories |` into `|Calories |`.

**Solution:** Don't strip spaces around pipes. Tables need the format:
```
| Header 1 | Header 2 |
|----------|----------|
| Value 1  | Value 2  |
```

---

## Dataview syntax appears in clipped notes

### Cause: Source templates have Dataview syntax

Web Clipper uses `{{variable}}` syntax. Dataview uses `` `= this.field` ``.

**Before (wrong for Web Clipper):**
```markdown
# `= this.file.name`

**Author:** `= this.author`
```

**After (correct for Web Clipper):**
```markdown
# {{title}}

**Author:** {{schema:@Article:author.name}}{{author}}
```

The export script handles this conversion automatically.

---

## Template triggers don't match

### Schema triggers
Use the `schema:@Type` format:
```json
"triggers": [
  "schema:@Article",
  "schema:@NewsArticle",
  "schema:@BlogPosting"
]
```

### URL triggers
Match URL prefixes:
```json
"triggers": [
  "https://www.goodreads.com/book/show",
  "https://www.amazon.com/dp/"
]
```

---

## Field values are empty

### Cause: Wrong variable syntax

**Schema data:**
```
{{schema:@Book:author.name}}      # Correct
{{schema:Book:author.name}}       # Wrong - missing @
{{schema:@Book.author.name}}      # Wrong - should be :author not .author
```

**Meta data:**
```
{{meta:property:og:title}}        # Correct
{{meta:og:title}}                 # Wrong - missing property:
```

---

## Dates show as raw ISO strings

### Solution: Add date filter

```
{{schema:@Article:datePublished|date:"YYYY-MM-DD"}}
{{date|date:"YYYY-MM-DD"}}
```

---

## Debug Workflow

1. **Test minimal template first:**
   ```json
   {
     "schemaVersion": "0.1.0",
     "name": "Test",
     "behavior": "create",
     "noteNameFormat": "{{title|safe_name}}",
     "path": "00 Inbox",
     "noteContentFormat": "# {{title}}",
     "properties": [],
     "triggers": []
   }
   ```

2. **Add fields one at a time** until you find the breaking change

3. **Check JSON validity:**
   ```bash
   cat template.json | jq .
   ```

4. **Look for special characters** in replace filters - especially `:` in URLs

5. **Compare with working template** to spot differences
