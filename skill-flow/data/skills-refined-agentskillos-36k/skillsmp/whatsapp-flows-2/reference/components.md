# Components Reference

Complete documentation of all 22 WhatsApp Flow components organized by category.

## Quick Component Summary

| Component | Type | Max | Required Props | v |
|-----------|------|-----|-----------------|---|
| TextHeading | Text | 80 chars | text | 4.0 |
| TextSubheading | Text | 80 chars | text | 4.0 |
| TextBody | Text | 4096 chars | text | 4.0 |
| TextCaption | Text | 409 chars | text | 4.0 |
| RichText | Text | 4096 chars | text | 5.1+ |
| TextInput | Input | 80 chars | name | 4.0 |
| TextArea | Input | 600 chars | name | 4.0 |
| DatePicker | Input | - | name | 5.0+ |
| CalendarPicker | Input | - | name | 6.1+ |
| PhotoPicker | Input | - | name | 5.0+ |
| DocumentPicker | Input | - | name | 5.0+ |
| CheckboxGroup | Select | 20 options | name | 4.0 |
| RadioButtonsGroup | Select | 20 options | name | 4.0 |
| Dropdown | Select | 200 options | name | 4.0 |
| OptIn | Select | 80 chars | name, label | 4.0 |
| ChipsSelector | Select | 20 options | name | 6.3+ |
| NavigationList | Select | 20 items | name | 6.2+ |
| Image | Media | 3/screen | src | 4.0 |
| ImageCarousel | Media | 3 images | images | 7.1+ |
| PhotoPicker | Media | - | name | 5.0+ |
| DocumentPicker | Media | - | name | 5.0+ |
| Footer | Action | 1/screen | label | 4.0 |
| EmbeddedLink | Action | 2/screen | text | 4.0 |
| If | Logic | 3 levels | condition, then | 4.0+ |
| Switch | Logic | 3 levels | value, cases | 4.0+ |

---

## Text Components

Display information to users.

### TextHeading

Large title text at the top of a screen.

**Properties:**
- `text` (required, max 80 chars) - Heading text
- `font-weight` (optional) - `regular` (default) or `bold`

```json
{
  "type": "TextHeading",
  "text": "Welcome to Our Service"
}
```

**Usage:** Screen titles, main messages. Keep concise and clear.

---

### TextSubheading

Secondary heading, smaller than TextHeading.

**Properties:**
- `text` (required, max 80 chars) - Subheading text

```json
{
  "type": "TextSubheading",
  "text": "Step 1 of 3"
}
```

**Usage:** Progress indicators, section labels, secondary titles.

---

### TextBody

Body text for descriptions, instructions, and explanations.

**Properties:**
- `text` (required, max 4096 chars) - Body text
- `markdown` (optional, default: false, v5.1+) - Enable markdown formatting
- `font-weight` (optional) - `regular` or `bold`

**Markdown Support (v5.1+):**

To enable markdown, set `"markdown": true`. Supported formatting:
- Bold: `**text**`
- Italic: `*text*`
- Line breaks: `\n`
- Lists: `• item` or `1. item`

**Without markdown enabled:**
```json
{
  "type": "TextBody",
  "text": "Plain text only. Markdown syntax **won't** be formatted."
}
```

**With markdown enabled:**
```json
{
  "type": "TextBody",
  "text": "**Bold text** and *italic text* are supported.\n\n• List item\n• Another item",
  "markdown": true
}
```

**Important:**
- Markdown property only works on **TextBody**, not TextHeading
- Must explicitly set `"markdown": true` to enable formatting
- Without this property, markdown syntax displays as plain text
- RichText (v5.1+) always supports full markdown without needing the property

**Usage:** Descriptive text, instructions, regular content. Use markdown for formatted lists, bold labels, and emphasis.

---

### TextCaption

Small caption text for supplementary information.

**Properties:**
- `text` (required, max 409 chars) - Caption text
- `markdown` (optional, default: false, v5.1+) - Enable markdown formatting

**Markdown Support (v5.1+):** Set `"markdown": true` to use markdown (same as TextBody).

```json
{
  "type": "TextCaption",
  "text": "Your information is secure and will not be shared."
}
```

**With markdown:**
```json
{
  "type": "TextCaption",
  "text": "**Required:** *This field is mandatory*",
  "markdown": true
}
```

**Usage:** Disclaimers, privacy notices, helper text, small supporting information.

---

### RichText (v5.1+)

Large formatted text with full markdown support. Preferred for rich formatting.

**Properties:**
- `text` (required, max 4096 chars) - Rich text with markdown

**Full Markdown Support:**
```json
{
  "type": "RichText",
  "text": "# Heading 1\n## Heading 2\n\n**Bold** *italic* ~~strikethrough~~\n\n- Bullet\n1. Numbered\n\n| Header | Header |\n|--------|--------|\n| Cell   | Cell   |\n\n[Link](url)"
}
```

**Markdown features:**
- Headers: `# H1`, `## H2`, `### H3`
- **Bold**: `**text**`
- *Italic*: `*text*`
- ~~Strikethrough~~: `~~text~~` (v6.0+)
- Code: `` `code` ``
- Lists (bullet and numbered)
- Tables: Standard markdown syntax
- Links: `[text](url)`
- Blockquotes: `> text`

**Placement rules:**
- v5.1-v6.2: Must stand alone on screen
- v6.3+: Can combine with Footer and other components

**Usage:** FAQ sections, price comparisons, complex layouts, order details with tables.

---

## Input Components

Collect information from users.

### TextInput

Single-line text entry field with multiple input types.

**Properties:**
- `name` (required) - Field identifier for form data
- `label` (optional) - Visible label
- `input-type` (optional, default: `text`) - Type of input:
  - `text` - Plain text
  - `number` - Numeric only
  - `email` - Email validation
  - `phone` - Phone format
  - `password` - Masked input
  - `passcode` - Numeric masked (e.g., PIN)
  - `date` - Date picker (YYYY-MM-DD)
- `placeholder` (optional) - Placeholder text
- `required` (optional, default: false) - Must be filled
- `init-value` (optional) - Initial value
- `max-length` (optional, default: 80) - Max characters
- `error-message` (optional) - Custom error text
- `pattern` (optional, v6.2+) - Regex for validation

```json
{
  "type": "TextInput",
  "name": "email",
  "label": "Email Address",
  "input-type": "email",
  "required": true,
  "placeholder": "user@example.com"
}
```

**Validation:**
- Built-in for email, phone, number, date types
- Custom validation via `pattern` (v6.2+): `"pattern": "^[a-z0-9]+$"`
- Server-side validation via data_exchange

**Data binding:** `${form.email}`

---

### TextArea

Multi-line text entry field.

**Properties:**
- `name` (required) - Field identifier
- `label` (optional) - Visible label
- `placeholder` (optional) - Placeholder text
- `required` (optional, default: false) - Must be filled
- `init-value` (optional) - Initial value
- `max-length` (optional, default: 600) - Max characters

```json
{
  "type": "TextArea",
  "name": "feedback",
  "label": "How can we improve?",
  "placeholder": "Tell us your thoughts...",
  "max-length": 500
}
```

**Usage:** Feedback collection, longer text input, descriptions.

---

### DatePicker

Native date selection interface.

**Properties:**
- `name` (required) - Field identifier
- `label` (optional) - Field label
- `required` (optional, default: false) - Must select
- `init-value` (optional) - Initial date (YYYY-MM-DD)
- `min-date` (optional) - Earliest selectable (YYYY-MM-DD)
- `max-date` (optional) - Latest selectable (YYYY-MM-DD)

```json
{
  "type": "DatePicker",
  "name": "birth_date",
  "label": "Date of Birth",
  "required": true
}
```

**Format:** Always YYYY-MM-DD regardless of device locale.

**Data binding:** `${form.birth_date}` returns "1990-05-15"

---

### CalendarPicker (v6.1+)

Full calendar interface with single or range selection.

**Properties:**
- `name` (required) - Field identifier
- `label` (optional) - Field label
- `mode` (optional, default: `single`) - `single` or `range`
- `required` (optional, default: false) - Must select
- `init-value` (optional) - Initial date(s)
- `min-date` (optional) - Earliest date (YYYY-MM-DD)
- `max-date` (optional) - Latest date (YYYY-MM-DD)

```json
{
  "type": "CalendarPicker",
  "name": "trip_dates",
  "label": "Select Trip Dates",
  "mode": "range",
  "min-date": "2024-03-01",
  "max-date": "2024-12-31"
}
```

**Single date:** `${form.appointment_date}` returns "2024-03-15"

**Date range:** `${form.trip_dates}` returns `{"start": "2024-06-01", "end": "2024-06-15"}`

**Advantages:** Visual calendar, range selection, better mobile UX.

---

### PhotoPicker (v5.0+)

Allow users to upload photos from device.

**Properties:**
- `name` (required) - Field identifier
- `label` (optional) - Button label

```json
{
  "type": "PhotoPicker",
  "name": "user_photo",
  "label": "Upload Your Photo"
}
```

**Supported:** JPEG, PNG formats.

**Max size:** ~20MB per photo (handled by WhatsApp).

**Form value:** Reference to uploaded media (actual image sent separately).

---

### DocumentPicker (v5.0+)

Allow users to upload documents (PDF, Word, Excel, etc.).

**Properties:**
- `name` (required) - Field identifier
- `label` (optional) - Button label

```json
{
  "type": "DocumentPicker",
  "name": "contract",
  "label": "Upload Contract"
}
```

**Supported formats:** PDF, Word (.doc, .docx), Excel (.xls, .xlsx), Text (.txt).

**Max size:** ~20MB per document.

---

## Selection Components

Allow users to choose from options.

### CheckboxGroup

Multiple selection from a list of options.

**Properties:**
- `name` (required) - Field identifier
- `label` (optional) - Group label
- `data-source` (required) - Options (static or dynamic)
- `required` (optional) - Must select at least one (v5.0+)
- `init-value` (optional) - Pre-selected options (array)

```json
{
  "type": "CheckboxGroup",
  "name": "interests",
  "label": "Select your interests:",
  "data-source": {
    "type": "static",
    "values": ["Sports", "Music", "Travel", "Food"]
  }
}
```

**Dynamic options:**
```json
{
  "type": "CheckboxGroup",
  "name": "categories",
  "data-source": {
    "type": "dynamic",
    "values": "${data.categories}"
  }
}
```

**Limits:** 1-20 options.

**Form value:** Array of selected items. `${form.interests}` returns `["Sports", "Music"]`

---

### RadioButtonsGroup

Single selection from a list of options.

**Properties:**
- `name` (required) - Field identifier
- `label` (optional) - Group label
- `data-source` (required) - Options
- `required` (optional) - Must select (v5.0+)
- `init-value` (optional) - Pre-selected option (string, not array)

```json
{
  "type": "RadioButtonsGroup",
  "name": "shipping_method",
  "label": "Shipping method:",
  "data-source": {
    "type": "static",
    "values": ["Standard (5-7 days)", "Express (2-3 days)", "Overnight"]
  },
  "required": true
}
```

**Limits:** 1-20 options.

**Form value:** Single selected item. `${form.shipping_method}` returns "Express (2-3 days)"

---

### Dropdown

Dropdown selector with static or dynamic options.

**Properties:**
- `name` (required) - Field identifier
- `label` (optional) - Field label
- `data-source` (required) - Options
- `required` (optional, default: false) - Must select
- `init-value` (optional) - Pre-selected option

```json
{
  "type": "Dropdown",
  "name": "country",
  "label": "Country",
  "data-source": {
    "type": "static",
    "values": ["United States", "Canada", "Mexico"]
  },
  "required": true
}
```

**Dynamic with images (v5.0+):**
```json
{
  "type": "Dropdown",
  "name": "color",
  "data-source": {
    "type": "dynamic",
    "values": "${data.colors}"
  }
}
```

Server provides:
```json
{
  "colors": [
    { "title": "Red", "image": "https://example.com/red.jpg" },
    { "title": "Blue", "image": "https://example.com/blue.jpg" }
  ]
}
```

**Limits:**
- Static: 200 max
- Dynamic without images: 200 max
- Dynamic with images: 100 max

**Form value:** `${form.country}` returns "United States"

---

### OptIn

Checkbox with optional action link (newsletter signup, terms, etc.).

**Properties:**
- `name` (required) - Field identifier
- `label` (required, max 80 chars) - Checkbox label
- `description` (optional, max 200 chars) - Additional info
- `action-url` (optional) - URL for link
- `action-text` (optional) - Link text
- `required` (optional) - Must be checked

```json
{
  "type": "OptIn",
  "name": "terms_agree",
  "label": "I agree to the Terms of Service",
  "description": "Please read our full terms",
  "action-url": "https://example.com/terms",
  "action-text": "View Terms",
  "required": true
}
```

**Limits:** Max 5 per screen.

**Form value:** Boolean. `${form.terms_agree}` returns `true` or `false`

---

### ChipsSelector (v6.3+)

Multi-select buttons (chips) with visual feedback.

**Properties:**
- `name` (required) - Field identifier
- `data-source` (required) - Options
- `on-select-action` (optional) - Action on selection
- `on-unselect-action` (optional, v7.1+) - Action on deselection

```json
{
  "type": "ChipsSelector",
  "name": "interests",
  "data-source": {
    "type": "static",
    "values": ["Sports", "Music", "Travel"]
  }
}
```

**With images:**
```json
{
  "type": "ChipsSelector",
  "name": "payment",
  "data-source": {
    "type": "dynamic",
    "values": "${data.payment_methods}"
  }
}
```

**Limits:** 2-20 options.

**Form value:** Array of selected items.

---

### NavigationList (v6.2+)

Rich navigation list with descriptions and optional images.

**Properties:**
- `name` (required) - Field identifier
- `data-source` (required) - List items
- `on-select-action` (optional) - Action on selection

```json
{
  "type": "NavigationList",
  "name": "plan_choice",
  "data-source": {
    "type": "static",
    "values": [
      {
        "id": "basic",
        "title": "Basic Plan",
        "description": "For individuals"
      },
      {
        "id": "pro",
        "title": "Pro Plan",
        "description": "For teams"
      }
    ]
  }
}
```

**With images:**
```json
{
  "data-source": {
    "type": "dynamic",
    "values": "${data.plans}"
  }
}
```

Server provides:
```json
{
  "plans": [
    {
      "id": "basic",
      "title": "Basic",
      "description": "Simple",
      "image": "https://example.com/basic.jpg"
    }
  ]
}
```

**Limits:** 1-20 items, max 2 per screen.

**Constraints:** Cannot be on terminal screen.

---

## Media Components

Display and upload media.

### Image

Display static images on a screen.

**Properties:**
- `src` (required) - Image URL (must be HTTPS)
- `scale-type` (optional) - `center-crop` (default) or `fill`
- `aspect-ratio` (optional) - e.g., `1:1`, `16:9`

```json
{
  "type": "Image",
  "src": "https://example.com/product.jpg",
  "aspect-ratio": "1:1",
  "scale-type": "fill"
}
```

**Requirements:**
- HTTPS only (no HTTP)
- Publicly accessible
- Recommended: 600x400px or larger
- Max: 300KB
- Formats: JPEG, PNG, WebP

**Limits:** Max 3 per screen.

---

### ImageCarousel (v7.1+)

Slide through multiple images.

**Properties:**
- `images` (required) - Array of image objects
- `scale-type` (optional) - `center-crop` or `fill`
- `aspect-ratio` (optional) - Ratio for all images

```json
{
  "type": "ImageCarousel",
  "images": [
    { "src": "https://example.com/image1.jpg" },
    { "src": "https://example.com/image2.jpg" },
    { "src": "https://example.com/image3.jpg" }
  ],
  "aspect-ratio": "1:1"
}
```

**Limits:** 1-3 images, max 2 per screen.

**Use cases:** Product galleries, before/after, step-by-step guides.

---

## Action Components

Navigation and conditional rendering.

### Footer

Primary action button at bottom of screen.

**Properties:**
- `label` (required, max 30 chars) - Button text
- `on-click-action` (required) - What happens on click
- `enabled` (optional, default: true) - Enable/disable

```json
{
  "type": "Footer",
  "label": "Continue",
  "on-click-action": {
    "action": "navigate",
    "next_screen": "NEXT_SCREEN"
  }
}
```

**Rules:**
- Max 1 per screen
- Must be last component
- Required on terminal screens
- If inside If component, must appear in both then/else branches

**Actions supported:** navigate, data_exchange, complete, update_data

---

### EmbeddedLink

Clickable link within content (secondary action).

**Properties:**
- `text` (required, max 25 chars) - Link text
- `on-click-action` (required) - Action on click

```json
{
  "type": "EmbeddedLink",
  "text": "Learn more",
  "on-click-action": {
    "action": "open_url",
    "url": "https://example.com"
  }
}
```

**Limits:** Max 2 per screen.

**Actions supported:** navigate, data_exchange, open_url

---

### If

Conditional rendering with boolean logic.

**Properties:**
- `condition` (required) - Boolean expression
- `then` (required) - Components if true
- `else` (optional) - Components if false

```json
{
  "type": "If",
  "condition": "${`${form.age} >= 18`}",
  "then": [
    { "type": "TextBody", "text": "You are eligible" }
  ],
  "else": [
    { "type": "TextBody", "text": "You are not eligible" }
  ]
}
```

**Condition syntax:**
- Simple: `${form.field}` (truthy check)
- Comparison: `${`${form.age} >= 18`}`
- Logical: `${`${a} && ${b}`}` or `${`${a} || ${b}`}`
- Negation: `${`!${a}`}`

**Nesting:** Max 3 levels deep.

**Footer rule:** If Footer inside If, must be in both then and else.

---

### Switch

Multi-way conditional rendering based on value.

**Properties:**
- `value` (required) - The value to match
- `cases` (required) - Array of case objects
- `default` (optional) - Components if no case matches

```json
{
  "type": "Switch",
  "value": "${form.plan_type}",
  "cases": [
    {
      "value": "basic",
      "children": [
        { "type": "TextBody", "text": "Basic plan features" }
      ]
    },
    {
      "value": "pro",
      "children": [
        { "type": "TextBody", "text": "Pro plan features" }
      ]
    }
  ],
  "default": [
    { "type": "TextBody", "text": "Unknown plan" }
  ]
}
```

**Use when:** Multiple distinct values to match (cleaner than nested If).

---

## Component Limits Summary

| Type | Component | Max Per Screen | Character Limit |
|------|-----------|-----------------|-----------------|
| Text | TextHeading | Unlimited | 80 |
| Text | TextBody | Unlimited | 4096 |
| Text | RichText | 1 (v5.1-v6.2), unlimited (v6.3+) | 4096 |
| Input | TextInput | Unlimited | 80 |
| Input | DatePicker | Unlimited | - |
| Selection | Dropdown | Unlimited | - (200 options) |
| Selection | CheckboxGroup | Unlimited | - (20 options) |
| Selection | OptIn | 5 | 80 |
| Media | Image | 3 | - |
| Media | ImageCarousel | 2 | - (3 images) |
| Action | Footer | 1 | 30 |
| Action | EmbeddedLink | 2 | 25 |
| Logic | If/Switch | Unlimited | - |

**Total components per screen:** 50 max

---

## Common Component Patterns

### Form Inputs
TextInput, TextArea, DatePicker, CheckboxGroup, RadioButtonsGroup, Dropdown

### Display Information
TextHeading, TextBody, TextCaption, RichText, Image

### User Interaction
Footer, EmbeddedLink, OptIn, ChipsSelector, NavigationList

### Logic & Routing
If, Switch, Footer (with navigate action)

### Media Rich
Image, ImageCarousel, PhotoPicker, DocumentPicker, RichText
