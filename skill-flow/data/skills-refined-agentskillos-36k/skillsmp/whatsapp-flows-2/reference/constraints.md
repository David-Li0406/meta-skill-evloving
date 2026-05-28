# Constraints & Validation Rules

All character limits, component counts, and validation rules for WhatsApp Flows.

## Character Limits

| Component | Limit | Notes |
|-----------|-------|-------|
| TextHeading | 80 chars | Concise titles |
| TextSubheading | 80 chars | Section labels |
| TextBody | 4096 chars | Supports markdown v5.1+ |
| TextCaption | 409 chars | Small text |
| RichText | 4096 chars | Full markdown, v5.1+ |
| TextInput | 80 chars (default) | Configurable via max-length |
| TextArea | 600 chars (default) | Configurable via max-length |
| Footer label | 30 chars | Button text |
| Footer label | 30 chars | Button text |
| EmbeddedLink text | 25 chars | Link text |
| OptIn label | 80 chars | Checkbox label |
| OptIn description | 200 chars | Additional text |

## Component Limits Per Screen

| Component | Max | Notes |
|-----------|-----|-------|
| Total components | 50 | All types combined |
| Image | 3 | Media display |
| ImageCarousel | 2 | Slide galleries, v7.1+ |
| EmbeddedLink | 2 | Secondary actions |
| OptIn | 5 | Checkboxes |
| Footer | 1 | Primary button |
| RichText | 1 (v5.1-v6.2), unlimited (v6.3+) | Standalone or combined |
| NavigationList | 2 | Rich navigation, v6.2+ |

## Option Limits

| Component | Min | Max | Notes |
|-----------|-----|-----|-------|
| CheckboxGroup | 1 | 20 | Multiple selection |
| RadioButtonsGroup | 1 | 20 | Single selection |
| Dropdown (static) | 1 | 200 | Hard-coded options |
| Dropdown (dynamic, no images) | 1 | 200 | From server |
| Dropdown (dynamic, with images) | 1 | 100 | Images add overhead |
| ChipsSelector | 2 | 20 | v6.3+, button-style |
| NavigationList | 1 | 20 | Rich items, v6.2+ |

## Screen & Flow Limits

| Item | Limit | Notes |
|------|-------|-------|
| Screens per flow | Unlimited | Practical: 50-100 |
| Components per screen | 50 | All types combined |
| Flow JSON size | 10MB | Hard limit |
| Nesting depth (If/Switch) | 3 levels | Max nesting |
| Branches per screen (routing) | 10 | Max in routing_model |
| Sensitive fields | Unlimited | Marked for masking |

## Validation Rules

### Required Properties

- **Flow level (Business 3.0 API):**
  - `version` - Flow JSON version (recommend 7.1)
  - `screens` - Array of screens
  - `data_api_version` (recommended) - Set to "3.0" for server integration

- **Screen level (REQUIRED):**
  - `id` - Unique screen identifier (alphanumeric + underscore)
  - `title` - Screen title for navigation and context (MUST be present)
  - `layout` - UI layout definition

- **Layout level:**
  - `type` - Must be "SingleColumnLayout"
  - `children` - Array of components

**Important:** Every screen MUST have a `title` property. This is a Business 3.0 API requirement.

### Screen ID Rules

- Must be unique across flow
- Alphanumeric and underscore: `[a-zA-Z0-9_]`
- Cannot be `SUCCESS` (reserved but allowed)
- Case-sensitive
- Max 100 characters

### Field Name Rules

- Must match component `name` property
- Alphanumeric and underscore: `[a-zA-Z0-9_]`
- Case-sensitive
- Unique per screen
- Recommended: snake_case (field_name)

### Data Schema Rules

- All dynamic fields must have `__example__`
- `__example__` should represent actual data
- Used for preview mode validation
- Type must match property type

### Terminal Screen Rules

- Must have `terminal: true` property
- Must contain Footer component
- Footer must use `complete` action
- May have `success: true/false`
- Cannot use `navigate` action

### Component Rules

- Max 50 components per screen
- Component types must be recognized
- Required properties must be present
- Limits per screen must be respected
- If Footer in If: must be in both branches

### Image URL Rules

- Must be HTTPS (no HTTP)
- Publicly accessible
- Recommended: 600x400px minimum
- Max 300KB
- Formats: JPEG, PNG, WebP

### Routing Model Rules

- `routing_model` paired with `data_api_version`
- All referenced screens must exist
- Entry screen has no inbound edges
- Terminal screens have no outbound
- Max 10 destinations per screen
- Cannot self-reference

## Markdown Configuration

TextBody and TextCaption components support markdown formatting (v5.1+).

**Important:** Markdown is disabled by default. To enable it:

```json
{
  "type": "TextBody",
  "text": "**Bold** and *italic* text",
  "markdown": true
}
```

**Supported markdown in TextBody/TextCaption:**
- Bold: `**text**`
- Italic: `*text*`
- Line breaks: `\n`
- Bullet lists: `• item`
- Numbered lists: `1. item`

**Key Rules:**
- Only TextBody and TextCaption support markdown property
- TextHeading DOES NOT support markdown (error if included)
- RichText always supports full markdown without needing property
- Default is `markdown: false` if property omitted
- When false, markdown syntax displays as plain text

---

## Validation Checklist

### Before Deploying

- [ ] Valid JSON syntax
- [ ] All required properties present
- [ ] Version specified (4.0-7.1, recommend 7.1)
- [ ] **ALL screens have `title` property** (Business 3.0 requirement)
- [ ] All screen IDs unique
- [ ] All field names unique per screen
- [ ] Character limits respected
- [ ] Component counts within limits
- [ ] Terminal screens properly configured
- [ ] All navigation targets exist
- [ ] All data schema fields have `__example__`
- [ ] Image URLs are HTTPS
- [ ] Routing model consistent (if used)
- [ ] No undefined component types
- [ ] Markdown only on TextBody/TextCaption, not TextHeading
- [ ] `markdown: true` explicitly set where needed

### Testing

- [ ] All screens accessible
- [ ] All navigation paths work
- [ ] Conditional logic triggers correctly
- [ ] Form validation works
- [ ] Data binding displays correctly
- [ ] Global references resolve
- [ ] Server integration working (if used)
- [ ] Error handling works
- [ ] Terminal screens display correctly

## Common Validation Errors

### Missing `__example__`

**Error:** Screen has dynamic data fields without examples

**Fix:** Add `__example__` to every property in data schema:
```json
"data": {
  "products": {
    "type": "array",
    "__example__": ["Product A"]  // Add this
  }
}
```

### Missing Screen Title

**Error:** Screen missing required `title` property

**Fix:** Add `title` to every screen:
```json
{
  "id": "SCREEN_NAME",
  "title": "User-Facing Screen Title",
  "layout": { ... }
}
```

### Duplicate Screen IDs

**Error:** Two screens with same ID

**Fix:** Make each screen ID unique

### Footer in If without else

**Error:** Footer only in then branch, not else

**Fix:** Add Footer to both branches:
```json
{
  "type": "If",
  "then": [{ "type": "Footer", ... }],
  "else": [{ "type": "Footer", ... }]
}
```

### Non-existent screen in routing

**Error:** Routing references screen that doesn't exist

**Fix:** Create the screen or remove from routing_model

### Exceeded character limits

**Error:** TextHeading exceeds 80 characters

**Fix:** Shorten text:
```json
// Wrong:
{ "type": "TextHeading", "text": "This is a very long heading that exceeds the maximum character limit" }

// Right:
{ "type": "TextHeading", "text": "Short heading" }
```

### Image URL not HTTPS

**Error:** Image URL uses HTTP

**Fix:** Use HTTPS URL:
```json
// Wrong:
{ "type": "Image", "src": "http://example.com/image.jpg" }

// Right:
{ "type": "Image", "src": "https://example.com/image.jpg" }
```

### Too many components per screen

**Error:** Screen has 51+ components

**Fix:** Move components to separate screen

### Exceeded option limits

**Error:** Dropdown has 250 static options

**Fix:** Reduce to max 200, or use dynamic data

### Markdown property on TextHeading

**Error:** Property 'markdown' is not allowed in 'TextHeading' component

**Fix:** Move markdown to TextBody instead, or use RichText:
```json
// Wrong:
{
  "type": "TextHeading",
  "text": "**Bold Heading**",
  "markdown": true
}

// Correct - use TextBody for formatted content:
{
  "type": "TextHeading",
  "text": "Heading"
},
{
  "type": "TextBody",
  "text": "**Bold text** here",
  "markdown": true
}

// Or use RichText for full markdown:
{
  "type": "RichText",
  "text": "# Heading\n**Bold text** here"
}
```

**Important:** Only TextBody and TextCaption support the markdown property. TextHeading does not.

## Validation Tools

Use provided validators:

```bash
# Full validation
python scripts/validate_flow.py your-flow.json

# Component-specific validation
python scripts/validate_components.py your-flow.json
```

Output includes:
- Error details with line references
- Warning about missing examples
- Constraint violation reports
- Character count issues
