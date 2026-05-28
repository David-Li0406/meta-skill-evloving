# Appearances Reference

The `appearance` column customizes how questions are displayed on mobile/web. Each question type supports different appearance options.

## Text Input Appearances

### text type

| Appearance | Effect | Use Case |
|-----------|--------|----------|
| `multiline` | Large text box (multiple lines) | Long descriptions, feedback |
| `url` | Validate as URL | Website input |
| `email` | Validate as email | Email addresses |
| `default` | Single-line text box | Normal text |

**Example:**
```
| type | name | label | appearance |
| text | name | Full name | |
| text | feedback | Feedback | multiline |
| text | website | Website | url |
| text | email | Email | email |
```

### integer/decimal type

| Appearance | Effect |
|-----------|--------|
| `thousands-sep` | Format with thousand separators: 1,000,000 |
| `default` | Plain number |

**Example:**
```
| type | name | label | appearance |
| integer | sales | Total sales | thousands-sep |
| decimal | price | Unit price | thousands-sep |
```

---

## Selection Appearances

### select_one type

| Appearance | Effect | Use When |
|-----------|--------|----------|
| `vertical` | Radio buttons stacked | Default, many options |
| `horizontal` | Radio buttons side-by-side | Few options (2-3) |
| `likert` | Likert scale styling | Survey ratings |
| `label` | Show labels only | Minimal display |
| `list-nolabel` | List without labels | Simple lists |
| `spinner` | Dropdown menu | Many options |
| `compact` | Compact display | Limited space |
| `search` | Searchable dropdown | Large choice lists |

**Example:**
```
| type | name | label | appearance |
| select_one yes_no | q1 | Do you agree? | horizontal |
| select_one satisfaction | satisfaction | Satisfaction | likert |
| select_one country | country | Country | search |
```

### select_multiple type

| Appearance | Effect |
|-----------|--------|
| `vertical` | Checkboxes stacked (default) |
| `horizontal` | Checkboxes side-by-side |
| `compact` | Compact multi-select |
| `search` | Searchable multi-select |

**Example:**
```
| type | name | label | appearance |
| select_multiple services | services | Available services | horizontal |
| select_multiple languages | languages | Languages | vertical |
```

---

## Date/Time Appearances

### date type

| Appearance | Effect |
|-----------|--------|
| `default` | Date picker (default) |
| `gregorian` | Gregorian calendar |
| `ethiopic` | Ethiopian calendar |
| `coptic` | Coptic calendar |
| `islamic` | Islamic calendar |

**Example:**
```
| type | name | label | appearance |
| date | visit_date | Date of visit | default |
| date | birth_date | Birth date | gregorian |
```

### time type

| Appearance | Effect |
|-----------|--------|
| `default` | Time picker (default) |

### dateTime type

| Appearance | Effect |
|-----------|--------|
| `default` | Date + time picker |

---

## Location Appearances

### geopoint type

| Appearance | Effect | Requires |
|-----------|--------|----------|
| `maps` | Interactive map for marking | GPS + map data |
| `default` | GPS capture mode | GPS hardware |
| `placement-map` | Map-based placement | GPS + map |

**Example:**
```
| type | name | label | appearance |
| geopoint | site | Mark site location | maps |
| geopoint | home | Home location | default |
```

### geotrace type

| Appearance | Effect |
|-----------|--------|
| `maps` | Map-based path drawing |
| `default` | GPS path recording |

**Example:**
```
| type | name | label | appearance |
| geotrace | boundary | Trace boundary | maps |
```

### geoshape type

| Appearance | Effect |
|-----------|--------|
| `maps` | Map-based polygon drawing |
| `default` | GPS polygon recording |

---

## Media Appearances

### image type

| Appearance | Effect |
|-----------|--------|
| `default` | Camera or gallery |
| `new` | Camera only (no gallery) |
| `new-front` | Front-facing camera only |
| `new-rear` | Rear-facing camera only |
| `annotate` | Draw on image after capture |
| `signature` | Signature pad |

**Example:**
```
| type | name | label | appearance |
| image | photo | Take photo | new |
| image | evidence | Evidence photo | annotate |
| image | signature | Signature | signature |
```

### audio type

| Appearance | Effect |
|-----------|--------|
| `default` | Audio recorder |
| `placement-box` | Placement box recorder |

**Example:**
```
| type | name | label | appearance |
| audio | notes | Field notes | default |
```

### video type

| Appearance | Effect |
|-----------|--------|
| `default` | Video recorder |
| `selfie` | Front-facing video |
| `new` | Recording only (no gallery) |

**Example:**
```
| type | name | label | appearance |
| video | incident | Video of incident | default |
| video | selfie_proof | Selfie proof | selfie |
```

---

## Special Appearances

### note type

| Appearance | Effect |
|-----------|--------|
| `default` | Static text message |
| `hint` | Display as hint text |

### rank type

| Appearance | Effect |
|-----------|--------|
| `default` | Drag-and-drop ranking |
| `vertical` | Vertical ranking list |

**Example:**
```
| type | name | label | appearance |
| rank | priorities | Rank by priority | vertical |
```

---

## Multiple Appearances

You can combine multiple appearances separated by spaces:

```
| type | name | label | appearance |
| text | feedback | Feedback | multiline |
| select_one country | country | Country | search |
| image | photo | Photo | new-rear annotate |
```

---

## Platform Support

Not all appearances work on all platforms:

| Appearance | ODK Collect | KoBoToolbox | SurveyCTO | Enketo |
|-----------|---|---|---|---|
| multiline | ✓ | ✓ | ✓ | ✓ |
| search | ✓ | ✓ | ✓ | ✓ |
| maps | ✓ | ✓ | ✓ | ✓ |
| annotate | ✓ | ✓ | ✓ | (limited) |
| likert | ✓ | ✓ | ✓ | ✓ |
| signature | ✓ | ✓ | ✓ | ✓ |
| spinner | ✓ | ✓ | ✓ | ✓ |

Check platform documentation for latest support.

---

## Best Practices

### Text
- Use `multiline` for descriptions > 50 chars
- Use `url` or `email` with constraint validation

### Selection
- Use `horizontal` for yes/no and small lists
- Use `search` for lists > 20 items
- Use `likert` for satisfaction/rating scales

### Location
- Always use `maps` appearance if available
- Falls back to GPS if maps not supported

### Media
- Use `new` for photo capture (security)
- Use `annotate` for damage documentation
- Use `signature` for consent/acknowledgment

### Date
- Gregorian calendar is default, change only if needed
- Multiple calendars support international use

---

## Testing Appearances

1. Test on actual mobile device
2. Verify appearance renders correctly
3. Check text wrapping on small screens
4. Verify functionality (maps load, camera works)
5. Test fallback if appearance not supported

---

## See Also

- [question-types.md](question-types.md) - Detailed type documentation
- [examples.md](../examples.md) - Working form examples
