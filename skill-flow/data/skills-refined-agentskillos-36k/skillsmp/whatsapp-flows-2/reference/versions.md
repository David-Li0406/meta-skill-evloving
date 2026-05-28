# Version Reference (v4.0 - v7.1)

Feature availability matrix across WhatsApp Flow JSON versions.

## Version History

| Version | Released | Status | Key Features |
|---------|----------|--------|--------------|
| 4.0 | 2021 | Stable | Core flows, basic components |
| 4.1 | 2021 | Stable | Enhanced validation |
| 5.0 | 2022 | Stable | RichText, better markdown |
| 5.1 | 2022 | Stable | Full markdown support in RichText |
| 6.0 | 2023 | Stable | Nested expressions, update_data, open_url |
| 6.1 | 2023 | Stable | Performance improvements |
| 6.2 | 2023 | Stable | NavigationList, advanced routing |
| 6.3 | 2024 | Current | ChipsSelector, enhanced ImageCarousel |
| 7.0 | 2024 | Current | Performance optimizations |
| 7.1 | 2024 | Current | Latest features and fixes |

---

## Component Availability

### Text Components

| Component | 4.0 | 5.0 | 6.0 | 6.2 | 6.3 | 7.0 | 7.1 | Note |
|-----------|-----|-----|-----|-----|-----|-----|-----|------|
| TextHeading | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | - |
| TextSubheading | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | - |
| TextBody | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | - |
| TextCaption | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | - |
| RichText | - | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | Basic markdown v5.0, full v5.1+ |

### Input Components

| Component | 4.0 | 5.0 | 6.0 | 6.2 | 6.3 | 7.0 | 7.1 | Note |
|-----------|-----|-----|-----|-----|-----|-----|-----|------|
| TextInput | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | - |
| TextArea | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | - |
| DatePicker | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | - |
| TimePicker | - | - | - | - | - | - | - | Not yet available |
| Dropdown | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | - |
| MultiSelect | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | - |

### Selection Components

| Component | 4.0 | 5.0 | 6.0 | 6.2 | 6.3 | 7.0 | 7.1 | Note |
|-----------|-----|-----|-----|-----|-----|-----|-----|------|
| RadioButtonsGroup | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | - |
| CheckboxGroup | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | - |
| OptIn | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | - |
| ChipsSelector | - | - | - | - | ✓ | ✓ | ✓ | Button-style selection v6.3+ |
| NavigationList | - | - | - | ✓ | ✓ | ✓ | ✓ | Rich navigation v6.2+ |

### Media Components

| Component | 4.0 | 5.0 | 6.0 | 6.2 | 6.3 | 7.0 | 7.1 | Note |
|-----------|-----|-----|-----|-----|-----|-----|-----|------|
| Image | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | - |
| ImageCarousel | - | - | - | - | ✓ | ✓ | ✓ | Slide galleries v7.1+ |

### Action Components

| Component | 4.0 | 5.0 | 6.0 | 6.2 | 6.3 | 7.0 | 7.1 | Note |
|-----------|-----|-----|-----|-----|-----|-----|-----|------|
| Footer | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | - |
| EmbeddedLink | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | - |

### Logic Components

| Component | 4.0 | 5.0 | 6.0 | 6.2 | 6.3 | 7.0 | 7.1 | Note |
|-----------|-----|-----|-----|-----|-----|-----|-----|------|
| If | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | - |
| Switch | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | - |

---

## Feature Availability

### Core Features

| Feature | 4.0 | 5.0 | 6.0 | 6.2 | 6.3 | 7.0 | 7.1 | Note |
|---------|-----|-----|-----|-----|-----|-----|-----|------|
| Basic flows | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | - |
| Form validation | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | - |
| Server integration | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | Via data_api_version |
| Conditional logic (If/Switch) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | - |
| Global references | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | `${screen.X.form.field}` |
| Navigation actions | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | - |
| Complete actions | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | - |
| Data exchange | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | - |

### Advanced Features

| Feature | 4.0 | 5.0 | 6.0 | 6.2 | 6.3 | 7.0 | 7.1 | Note |
|---------|-----|-----|-----|-----|-----|-----|-----|------|
| Nested expressions | - | - | ✓ | ✓ | ✓ | ✓ | ✓ | `${`expression`}` v6.0+ |
| Update data action | - | - | ✓ | ✓ | ✓ | ✓ | ✓ | v6.0+ |
| Open URL action | - | - | ✓ | ✓ | ✓ | ✓ | ✓ | v6.0+ |
| RichText component | - | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | Basic v5.0, full v5.1+ |
| NavigationList | - | - | - | ✓ | ✓ | ✓ | ✓ | v6.2+ |
| ChipsSelector | - | - | - | - | ✓ | ✓ | ✓ | v6.3+ |
| ImageCarousel | - | - | - | - | ✓ | ✓ | ✓ | v6.3+ |

### Data API Versions

| `data_api_version` | Introduced | Status | Features |
|--------------------|------------|--------|----------|
| 1.0 | v4.0 | Deprecated | Basic server integration |
| 2.0 | v5.0 | Stable | Enhanced request format |
| 3.0 | v6.0 | Current | Full validation, error handling |

---

## Breaking Changes & Migration Guide

### v5.1 → v6.0

**Breaking Changes:**
- None - fully backward compatible

**New Features to Adopt:**
```json
// New: Nested expressions
{"condition": "${`${form.age} >= 18`}"}

// New: update_data action
{"action": "update_data", "payload": {...}}

// New: open_url action
{"action": "open_url", "url": "https://..."}
```

**Migration Path:** No action required, but update to benefit from new features.

### v6.2 → v6.3

**Breaking Changes:**
- None - fully backward compatible

**New Components:**
```json
// New: ChipsSelector (button-style selection)
{
  "type": "ChipsSelector",
  "name": "tags",
  "options": ["Tag1", "Tag2", "Tag3"]
}

// New: ImageCarousel (slide galleries)
{
  "type": "ImageCarousel",
  "images": [...]
}
```

**Migration Path:** No action required. Optional adoption of new components.

### v7.0 → v7.1

**Breaking Changes:**
- None - fully backward compatible

**Enhancements:**
- Performance improvements
- Better error handling
- Enhanced ImageCarousel with more options

**Migration Path:** No migration needed, update recommended for performance.

---

## Version-Specific Syntax

### Nested Expressions (v6.0+)

Only available in v6.0 and later:

```json
{
  "version": "6.0",
  "screens": [
    {
      "id": "CHECK_AGE",
      "layout": {
        "type": "SingleColumnLayout",
        "children": [
          {
            "type": "If",
            // Nested expressions work here
            "condition": "${`${form.age} >= 18`}"
          }
        ]
      }
    }
  ]
}
```

Use for earlier versions:
```json
{
  "version": "5.1",
  "screens": [
    {
      "id": "CHECK_AGE",
      "layout": {
        "type": "SingleColumnLayout",
        "children": [
          {
            "type": "If",
            // Simple conditions only (no expressions)
            "condition": "${form.is_adult}"
          }
        ]
      }
    }
  ]
}
```

### ChipsSelector (v6.3+)

Only available in v6.3+:

```json
{
  "version": "6.3",
  "screens": [
    {
      "id": "TAGS",
      "layout": {
        "type": "SingleColumnLayout",
        "children": [
          {
            "type": "ChipsSelector",
            "name": "interests",
            "label": "Select interests",
            "options": ["Sports", "Music", "Art"],
            "multiple": true
          }
        ]
      }
    }
  ]
}
```

### ImageCarousel (v7.1+)

Enhanced version in v7.1:

```json
{
  "version": "7.1",
  "screens": [
    {
      "id": "GALLERY",
      "layout": {
        "type": "SingleColumnLayout",
        "children": [
          {
            "type": "ImageCarousel",
            "images": [
              {
                "src": "https://...",
                "alt": "Image 1",
                "title": "Title 1"
              },
              {
                "src": "https://...",
                "alt": "Image 2",
                "title": "Title 2"
              }
            ]
          }
        ]
      }
    }
  ]
}
```

---

## API Version Matrix

### Server Integration by Flow Version

| Flow Version | `data_api_version` | Features |
|--------------|-------------------|----------|
| 4.0 - 4.1 | 1.0 | Basic routing, simple responses |
| 5.0 - 5.1 | 2.0 | Enhanced format, better errors |
| 6.0 - 6.3 | 3.0 | Full validation, rich error messages |
| 7.0 - 7.1 | 3.0 | Maintained, no changes |

**Current Recommendation:** Use `data_api_version: "3.0"` with `version: "7.1"`

---

## Deprecation Timeline

### Deprecated Features

| Feature | Deprecated | Status | Alternative |
|---------|-----------|--------|-------------|
| data_api_version 1.0 | v5.0 | Don't use | Use 2.0 or 3.0 |
| data_api_version 2.0 | v6.0 | Avoid | Use 3.0 |

### Sunset Dates

No components or major features have been sunset yet. All v4.0+ features still supported in v7.1.

---

## Recommended Versions

### For New Flows

**Use v7.1** with all latest features:

```json
{
  "version": "7.1",
  "data_api_version": "3.0",
  "screens": [...]
}
```

### For Legacy Flows

If maintaining older flows, upgrade to at least v6.0 to access:
- Nested expressions (validation logic)
- update_data (dynamic updates)
- open_url (external links)

```json
{
  "version": "6.0",
  "data_api_version": "3.0",
  "screens": [...]
}
```

### Minimum Version for Features

| If you need... | Use version... |
|---|---|
| Basic flows | 4.0+ |
| RichText | 5.0+ |
| Nested expressions | 6.0+ |
| update_data, open_url | 6.0+ |
| NavigationList | 6.2+ |
| ChipsSelector | 6.3+ |
| ImageCarousel | 6.3+ |
| Latest features | 7.1 |

---

## Validation by Version

### v4.0 Validation Rules

- Simple field references only: `${form.field}`
- No nested expressions
- Basic component support

```json
{
  "type": "TextBody",
  "text": "Hello ${form.name}"
}
```

### v6.0+ Validation Rules

- Full expressions: `${`expression`}`
- Complex conditions
- All component types

```json
{
  "type": "If",
  "condition": "${`${form.age} >= 18 && ${form.country} == 'USA'`}",
  "then": [...]
}
```

---

## Compatibility Notes

### Browser Support

All versions work on:
- WhatsApp Web
- WhatsApp Business app
- WhatsApp Desktop
- Mobile platforms

### Device Support

Tested on:
- iOS 11+
- Android 6.0+
- Desktop browsers (modern versions)

### Network Conditions

Flows handle:
- Slow connections (optimized for 2G/3G)
- Offline scenarios (graceful degradation)
- Reconnection after interruption

---

## Version-Specific Best Practices

### v4.0 - v5.1

- Keep flows simple
- Validate server-side extensively
- Avoid complex conditionals
- Use static data when possible

### v6.0+

- Leverage nested expressions
- Use update_data for interactive flows
- Implement dynamic features
- Build rich components

### v7.0+

- Use latest components (ChipsSelector, ImageCarousel)
- Optimize for performance
- Use all security features
- Build modern experiences

---

## Future Roadmap

Planned features (subject to change):

- [ ] TimePicker component
- [ ] File upload support
- [ ] Video components
- [ ] Payment integration
- [ ] Geolocation features
- [ ] Native app integration
