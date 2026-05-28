# Data Binding Reference

How data flows through WhatsApp Flows - user input, server data, expressions, and global references.

## Quick Syntax Guide

```
${form.field_name}                    Form data (user input)
${data.field_name}                    Server data
${screen.SCREEN_ID.form.field}        Global reference to form data
${screen.SCREEN_ID.data.field}        Global reference to server data
${`expression`}                       Nested expressions (v6.0+)
```

---

## Form Data: User Input

When users fill out components (TextInput, Dropdown, DatePicker, etc.), their values are stored in `form`.

**Binding syntax:** `${form.field_name}`

**Field names must match component `name` property** (case-sensitive).

### Example: Collecting User Information

```json
{
  "id": "USER_INFO",
  "layout": {
    "type": "SingleColumnLayout",
    "children": [
      {
        "type": "TextInput",
        "name": "first_name",
        "label": "First Name",
        "required": true
      },
      {
        "type": "TextInput",
        "name": "email",
        "input-type": "email",
        "label": "Email",
        "required": true
      },
      {
        "type": "Footer",
        "label": "Continue",
        "on-click-action": {
          "action": "navigate",
          "next_screen": "CONFIRMATION"
        }
      }
    ]
  }
}
```

### Using Form Data on Another Screen

```json
{
  "id": "CONFIRMATION",
  "layout": {
    "type": "SingleColumnLayout",
    "children": [
      {
        "type": "TextHeading",
        "text": "Confirm Your Information"
      },
      {
        "type": "TextBody",
        "text": "Name: ${screen.USER_INFO.form.first_name}"
      },
      {
        "type": "TextBody",
        "text": "Email: ${screen.USER_INFO.form.email}"
      }
    ]
  }
}
```

---

## Form Data Types

Form values are strings by default unless component specifies otherwise:

| Component | Data Type | Example |
|-----------|-----------|---------|
| TextInput (text) | string | "John" |
| TextInput (email) | string | "user@example.com" |
| TextInput (number) | string (numeric) | "42" |
| TextInput (date) | string (YYYY-MM-DD) | "2024-03-15" |
| TextArea | string | "multi-line text" |
| DatePicker | string (YYYY-MM-DD) | "1990-05-15" |
| Checkbox Group | array | ["Sports", "Music"] |
| RadioButtons | string | "Option A" |
| Dropdown | string | "Category 1" |
| OptIn | boolean | true or false |
| ChipsSelector | array | ["tag1", "tag2"] |

---

## Server Data: From Data Endpoints

Server endpoints provide dynamic data to populate lists, prices, inventory, etc.

### Declaring Server Data

Define expected data structure using JSON Schema:

```json
{
  "id": "PRODUCT_LIST",
  "data": {
    "type": "object",
    "properties": {
      "products": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "id": { "type": "string" },
            "name": { "type": "string" },
            "price": { "type": "number" }
          }
        },
        "__example__": [
          {
            "id": "P001",
            "name": "Laptop",
            "price": 999.99
          }
        ]
      },
      "currency": {
        "type": "string",
        "__example__": "USD"
      }
    }
  },
  "layout": { ... }
}
```

**Critical:** Every field must have `__example__` for preview mode.

### Using Server Data

**Binding syntax:** `${data.field_name}`

```json
{
  "id": "PRODUCT_LIST",
  "data": { ... },
  "layout": {
    "type": "SingleColumnLayout",
    "children": [
      {
        "type": "TextBody",
        "text": "Available in: ${data.currency}"
      },
      {
        "type": "Dropdown",
        "name": "selected_product",
        "label": "Choose Product",
        "data-source": {
          "type": "dynamic",
          "values": "${data.products}"
        }
      }
    ]
  }
}
```

---

## Global Data Referencing (v4.0+)

Access form or data from **any screen** without passing through navigate payloads.

**Syntax:**
```
${screen.SCREEN_ID.form.field_name}
${screen.SCREEN_ID.data.field_name}
```

### Example: Multi-Step Checkout

```json
{
  "screens": [
    {
      "id": "SHIPPING",
      "layout": {
        "type": "SingleColumnLayout",
        "children": [
          {
            "type": "TextInput",
            "name": "address",
            "label": "Shipping Address",
            "required": true
          },
          {
            "type": "Footer",
            "label": "Next",
            "on-click-action": { "action": "navigate", "next_screen": "BILLING" }
          }
        ]
      }
    },
    {
      "id": "BILLING",
      "layout": {
        "type": "SingleColumnLayout",
        "children": [
          {
            "type": "TextBody",
            "text": "Ship to: ${screen.SHIPPING.form.address}"
          },
          {
            "type": "TextInput",
            "name": "billing_address",
            "label": "Billing Address"
          },
          {
            "type": "Footer",
            "label": "Review",
            "on-click-action": { "action": "navigate", "next_screen": "REVIEW" }
          }
        ]
      }
    },
    {
      "id": "REVIEW",
      "layout": {
        "type": "SingleColumnLayout",
        "children": [
          {
            "type": "TextBody",
            "text": "Shipping: ${screen.SHIPPING.form.address}"
          },
          {
            "type": "TextBody",
            "text": "Billing: ${screen.BILLING.form.billing_address}"
          },
          {
            "type": "Footer",
            "label": "Confirm",
            "on-click-action": {
              "action": "complete",
              "payload": {
                "shipping": "${screen.SHIPPING.form.address}",
                "billing": "${screen.BILLING.form.billing_address}"
              }
            }
          }
        ]
      }
    }
  ]
}
```

### Forward References

You can reference screens that haven't been filled yet:

```json
{
  "id": "CONFIRMATION",
  "layout": {
    "type": "SingleColumnLayout",
    "children": [
      {
        "type": "TextBody",
        "text": "You selected: ${screen.PRODUCT_PICKER.form.product}"
      }
    ]
  }
}
```

Even if PRODUCT_PICKER hasn't been visited yet, the reference will work once completed.

---

## Nested Expressions (v6.0+)

Perform calculations and logical operations.

**Syntax:** `${`expression`}`

### Comparison Operators

```json
${`${form.age} >= 18`}
${`${form.quantity} > 0`}
${`${form.status} == 'active'`}
${`${form.price} != 0`}
```

### Logical Operators

```json
${`${form.age} >= 18 && ${form.country} == 'USA'`}
${`${form.type} == 'business' || ${form.type} == 'nonprofit'`}
${`!${form.is_blocked}`}
```

### Math Operations

```json
${`${form.quantity} * ${data.unit_price}`}
${`${form.subtotal} + ${data.tax}`}
${`${data.total} - ${form.discount}`}
${`${form.distance} / ${data.speed}`}
${`${form.number} % 2`}
```

### String Concatenation

```json
${`${form.first_name} + ' ' + ${form.last_name}`}
${`'Order #' + ${data.order_id}`}
```

### In Conditional Logic

```json
{
  "type": "If",
  "condition": "${`${form.age} >= 18`}",
  "then": [
    { "type": "TextBody", "text": "You are eligible" }
  ],
  "else": [
    { "type": "TextBody", "text": "You must be 18+" }
  ]
}
```

### Limitations

**What works:**
- Comparisons: `==`, `!=`, `<`, `>`, `<=`, `>=`
- Logic: `&&`, `||`, `!`
- Math: `+`, `-`, `*`, `/`, `%`
- String concatenation with `+`
- Field references

**What doesn't work:**
- Method calls (mostly): `.length`, `.toUpperCase()`
- Array operations: `[0]`, `.map()`, `.filter()`
- Object access: `.property`, `['key']`
- Regular expressions
- Custom functions

---

## Form vs Data: When to Use Each

| Need | Use | Binding | Example |
|------|-----|---------|---------|
| User enters text | Form | `${form.name}` | Name, email, address |
| Server provides options | Data | `${data.products}` | Product list, categories |
| User selects from list | Form | `${form.choice}` | Dropdown selection |
| Display server info | Data | `${data.balance}` | Account balance, inventory |
| Conditional logic | Either | `${form.age}` or `${data.status}` | Check eligibility |
| Review user input | Global ref | `${screen.X.form.field}` | Confirmation screen |
| Cross-screen reference | Global ref | `${screen.X.form/data.field}` | Multi-step flow |

---

## Data Exchange Flow

When user submits form via `data_exchange` action:

1. **Client collects data** from form fields
2. **Payload constructed** using `${form.field}` values
3. **Sent to server** endpoint
4. **Server processes** validation, business logic
5. **Server responds** with next screen and data
6. **Components updated** with new data
7. **Display refreshed** with `${data.field}` values

Example server response:
```json
{
  "screen": "PRODUCTS",
  "data": {
    "products": [
      { "id": "P1", "name": "Widget", "price": 9.99 }
    ]
  }
}
```

---

## Best Practices

1. **Use global references** instead of navigate payloads
2. **Always include `__example__`** in data schemas
3. **Validate server-side** - never trust client data alone
4. **Keep expressions simple** - one or two operations max
5. **Use meaningful field names** - `first_name` not `fn`
6. **Test with example data** - use `__example__` values
7. **Check field name matching** - case-sensitive
8. **Document complex logic** - explain conditional expressions
9. **Monetary values on server** - don't calculate client-side
10. **Global refs for reviews** - cleaner than payloads

---

## Common Patterns

### Simple Confirmation
```
User enters: ${form.email}
Confirmation shows: Email: ${screen.STEP1.form.email}
```

### Conditional Paths
```
If: ${`${form.age} >= 18`}
Then: Show adult content
Else: Request parental consent
```

### Dynamic Lists
```
User selects: ${form.category}
Server returns: ${data.products_for_category}
Dropdown shows: ${data.products}
```

### Price Calculation
```
Display: Total: $${`${form.quantity} * ${data.unit_price}`}
(Send actual calculation to server for precision)
```

### Multi-Step Review
```
Step 1 data: ${screen.STEP1.form.field}
Step 2 data: ${screen.STEP2.form.field}
Final review: Combines both via global references
```
