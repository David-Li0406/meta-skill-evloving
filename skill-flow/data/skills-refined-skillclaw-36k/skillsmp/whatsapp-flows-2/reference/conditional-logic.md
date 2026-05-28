# Conditional Logic Reference

Build dynamic flows with If and Switch components (v4.0+).

## If Component

Show content conditionally based on boolean logic.

**Syntax:**
```json
{
  "type": "If",
  "condition": "${`expression`}",
  "then": [/* components if true */],
  "else": [/* components if false (optional) */]
}
```

**Properties:**
- `condition` (required) - Boolean expression to evaluate
- `then` (required) - Components shown if condition is true
- `else` (optional) - Components shown if condition is false

### Simple Condition

```json
{
  "type": "If",
  "condition": "${form.has_account}",
  "then": [
    { "type": "TextBody", "text": "Welcome back!" }
  ],
  "else": [
    { "type": "TextBody", "text": "Create an account to continue" }
  ]
}
```

### Comparison Condition

```json
{
  "type": "If",
  "condition": "${`${form.age} >= 18`}",
  "then": [
    { "type": "TextBody", "text": "You are eligible" }
  ],
  "else": [
    { "type": "TextBody", "text": "You must be 18 or older" }
  ]
}
```

### Complex Condition

```json
{
  "type": "If",
  "condition": "${`${form.country} == 'USA' && ${form.age} >= 21`}",
  "then": [
    { "type": "TextBody", "text": "You qualify for premium" }
  ],
  "else": [
    { "type": "TextBody", "text": "You don't qualify" }
  ]
}
```

### Without Else

```json
{
  "type": "If",
  "condition": "${`${form.is_premium} == true`}",
  "then": [
    { "type": "TextBody", "text": "Premium features available" }
  ]
}
```

---

## Switch Component

Multi-way branching based on a single value.

**Syntax:**
```json
{
  "type": "Switch",
  "value": "${form.field}",
  "cases": [
    {
      "value": "case1",
      "children": [/* components */]
    },
    {
      "value": "case2",
      "children": [/* components */]
    }
  ],
  "default": [/* optional: fallback components */]
}
```

**Properties:**
- `value` (required) - The value to match against
- `cases` (required) - Array of case objects with `value` and `children`
- `default` (optional) - Components if no case matches

### Switch on Form Data

```json
{
  "type": "Switch",
  "value": "${form.account_type}",
  "cases": [
    {
      "value": "free",
      "children": [
        { "type": "TextBody", "text": "You have a free account with basic features" }
      ]
    },
    {
      "value": "premium",
      "children": [
        { "type": "TextBody", "text": "You have premium with all features" }
      ]
    },
    {
      "value": "enterprise",
      "children": [
        { "type": "TextBody", "text": "You have enterprise support" }
      ]
    }
  ],
  "default": [
    { "type": "TextBody", "text": "Unknown account type" }
  ]
}
```

### Switch on Server Data

```json
{
  "type": "Switch",
  "value": "${data.order_status}",
  "cases": [
    {
      "value": "pending",
      "children": [
        { "type": "TextBody", "text": "Your order is being processed" }
      ]
    },
    {
      "value": "shipped",
      "children": [
        { "type": "TextBody", "text": "Your order has shipped" }
      ]
    },
    {
      "value": "delivered",
      "children": [
        { "type": "TextBody", "text": "Your order has been delivered" }
      ]
    }
  ]
}
```

---

## When to Use If vs Switch

Use **If** when:
- Two outcomes (true/false)
- Comparisons: `>`, `<`, `==`, `!=`
- Logical operators: `&&`, `||`, `!`
- Complex conditions with multiple checks

Use **Switch** when:
- Multiple discrete values
- String matching
- Clean cases for each value
- Better than nested If statements

**Example:**
```javascript
// If: binary decision
if (age >= 18) { ... } else { ... }

// Switch: multiple values
switch (planType) {
  case 'free': ...
  case 'pro': ...
  case 'enterprise': ...
}
```

---

## Conditional Inputs

Show/hide input fields based on previous selections.

```json
{
  "type": "RadioButtonsGroup",
  "name": "address_type",
  "label": "Address Type",
  "data-source": {
    "type": "static",
    "values": ["Home", "Work", "Other"]
  },
  "required": true
},
{
  "type": "If",
  "condition": "${`${form.address_type} == 'Other'`}",
  "then": [
    {
      "type": "TextInput",
      "name": "other_type",
      "label": "Please specify",
      "required": true
    }
  ]
}
```

When user selects "Other", TextInput appears. For other selections, it's hidden.

---

## Conditional Footer

Show different buttons based on form state.

**Rule:** If Footer is inside If, it must appear in **both** then and else branches.

```json
{
  "type": "CheckboxGroup",
  "name": "accepted",
  "data-source": {
    "type": "static",
    "values": ["I accept terms"]
  }
},
{
  "type": "If",
  "condition": "${form.accepted}",
  "then": [
    {
      "type": "Footer",
      "label": "Continue",
      "on-click-action": {
        "action": "navigate",
        "next_screen": "NEXT"
      }
    }
  ],
  "else": [
    {
      "type": "Footer",
      "label": "Continue",
      "enabled": false
    }
  ]
}
```

When terms not accepted, Footer is disabled. When accepted, it's enabled.

---

## Nested Conditionals

Up to 3 levels of nesting allowed.

```json
{
  "type": "If",
  "condition": "${`${form.has_discount}`}",
  "then": [
    { "type": "TextBody", "text": "You have a discount code" },
    {
      "type": "If",
      "condition": "${`${form.discount_percent} > 20`}",
      "then": [
        { "type": "TextBody", "text": "Premium discount (>20%)" }
      ],
      "else": [
        { "type": "TextBody", "text": "Standard discount (≤20%)" }
      ]
    }
  ]
}
```

**Nesting limit:** 3 levels maximum. Beyond that, use Switch or separate screens.

---

## Conditional Navigation

Show different next screens based on conditions.

```json
{
  "type": "If",
  "condition": "${`${form.has_account}`}",
  "then": [
    {
      "type": "Footer",
      "label": "Login",
      "on-click-action": {
        "action": "navigate",
        "next_screen": "LOGIN"
      }
    }
  ],
  "else": [
    {
      "type": "Footer",
      "label": "Register",
      "on-click-action": {
        "action": "navigate",
        "next_screen": "REGISTER"
      }
    }
  ]
}
```

---

## Expression Operators

| Operator | Meaning | Example |
|----------|---------|---------|
| `==` | Equal | `${`${form.status} == 'active'`}` |
| `!=` | Not equal | `${`${form.type} != 'free'`}` |
| `<` | Less than | `${`${form.age} < 18`}` |
| `<=` | Less or equal | `${`${form.age} <= 65`}` |
| `>` | Greater than | `${`${form.age} > 18`}` |
| `>=` | Greater or equal | `${`${form.balance} >= 100`}` |
| `&&` | AND (both true) | `${`${a} && ${b}`}` |
| `\|\|` | OR (either true) | `${`${a} \|\| ${b}`}` |
| `!` | NOT (invert) | `${`!${form.is_blocked}`}` |

---

## Common Patterns

### Age Verification

```json
{
  "type": "If",
  "condition": "${`${form.age} >= 18`}",
  "then": [
    { "type": "TextBody", "text": "You're eligible!" },
    { "type": "Footer", "label": "Continue", ... }
  ],
  "else": [
    { "type": "TextBody", "text": "Parental consent required" },
    { "type": "Footer", "label": "Request Consent", ... }
  ]
}
```

### Account Type Routing

```json
{
  "type": "Switch",
  "value": "${form.account_type}",
  "cases": [
    {
      "value": "business",
      "children": [
        { "type": "TextBody", "text": "Business features..." },
        { "type": "Footer", "label": "Business Setup", ... }
      ]
    },
    {
      "value": "individual",
      "children": [
        { "type": "TextBody", "text": "Individual features..." },
        { "type": "Footer", "label": "Personal Setup", ... }
      ]
    }
  ]
}
```

### Payment Method Selection

```json
{
  "type": "Switch",
  "value": "${form.payment_method}",
  "cases": [
    {
      "value": "credit_card",
      "children": [
        { "type": "TextInput", "name": "card_number", ... }
      ]
    },
    {
      "value": "paypal",
      "children": [
        { "type": "TextInput", "name": "paypal_email", ... }
      ]
    },
    {
      "value": "bank",
      "children": [
        { "type": "TextBody", "text": "Bank transfer details will be sent" }
      ]
    }
  ]
}
```

### Membership Status

```json
{
  "type": "Switch",
  "value": "${data.membership_status}",
  "cases": [
    {
      "value": "active",
      "children": [
        { "type": "TextBody", "text": "Welcome member! You get 15% off" }
      ]
    },
    {
      "value": "expired",
      "children": [
        { "type": "TextBody", "text": "Your membership expired. Renew for benefits" }
      ]
    },
    {
      "value": "inactive",
      "children": [
        { "type": "TextBody", "text": "Join membership for exclusive discounts" }
      ]
    }
  ]
}
```

---

## Validation Rules

1. **Condition must be boolean** - Evaluates to true or false
2. **Both branches if Footer** - If Footer in If, must appear in then AND else
3. **Maximum 3 levels** - Don't nest deeper than 3 levels
4. **Use expressions for logic** - Backticks required for comparisons
5. **Case-sensitive** - Field names and values are case-sensitive

---

## Troubleshooting

**Condition always false:**
- Check field name matches component `name` (case-sensitive)
- Verify field exists before referencing
- Test with `__example__` values

**Footer not appearing:**
- If Footer inside If, add to both then and else
- Place Footer outside If as alternative

**Nested conditionals too deep:**
- Use Switch instead of nested If
- Break into separate screens
- Simplify logic

---

## Best Practices

1. **Keep conditions simple** - One or two checks max
2. **Use Switch for many values** - Cleaner than nested If
3. **Test all branches** - Ensure every path works
4. **Meaningful labels** - Help users understand choices
5. **Clear error messages** - Explain why fields appear/disappear
6. **Document logic** - Comment complex conditions
7. **Validate server-side** - Don't rely only on client logic
8. **User-friendly messaging** - Explain conditional content
9. **Mobile testing** - Verify on actual device
10. **Progressive disclosure** - Hide advanced options until needed
