# WhatsApp Flows Examples

Complete, working Flow JSON examples demonstrating common patterns.

## Example 0: Minimal Client-Side Flow (No Backend)

Demonstrates a simple flow with no server integration needed. Best for basic form collection without validation endpoints.

```json
{
  "version": "7.1",
  "screens": [
    {
      "id": "START",
      "title": "Welcome",
      "layout": {
        "type": "SingleColumnLayout",
        "children": [
          {
            "type": "TextHeading",
            "text": "Welcome!"
          },
          {
            "type": "TextBody",
            "text": "This is a simple client-side flow with no backend endpoint.",
            "markdown": true
          },
          {
            "type": "Footer",
            "label": "Continue",
            "on-click-action": {
              "name": "navigate",
              "next": {
                "type": "screen",
                "name": "COMPLETE"
              }
            }
          }
        ]
      }
    },
    {
      "id": "COMPLETE",
      "title": "Complete",
      "terminal": true,
      "success": true,
      "layout": {
        "type": "SingleColumnLayout",
        "children": [
          {
            "type": "TextHeading",
            "text": "Done!"
          },
          {
            "type": "Footer",
            "label": "Finish",
            "on-click-action": {
              "name": "complete",
              "payload": {}
            }
          }
        ]
      }
    }
  ]
}
```

**Note:** No `data_api_version` needed since this flow doesn't use server endpoints.

---

## Example 0a: Markdown Formatting with Server Integration

Demonstrates markdown formatting in TextBody with full Business 3.0 API structure including server integration.

```json
{
  "version": "7.1",
  "data_api_version": "3.0",
  "screens": [
    {
      "id": "WELCOME",
      "title": "Formatted Content",
      "layout": {
        "type": "SingleColumnLayout",
        "children": [
          {
            "type": "TextHeading",
            "text": "Important Information"
          },
          {
            "type": "TextBody",
            "text": "**Please note the following:**\n\n• Item 1 with important info\n• Item 2 with more details\n• Item 3 to remember\n\n*Last updated today*",
            "markdown": true
          },
          {
            "type": "Footer",
            "label": "Acknowledge",
            "on-click-action": {
              "name": "navigate",
              "next": {
                "type": "screen",
                "name": "COMPLETE"
              }
            }
          }
        ]
      }
    },
    {
      "id": "COMPLETE",
      "title": "Complete",
      "terminal": true,
      "success": true,
      "layout": {
        "type": "SingleColumnLayout",
        "children": [
          {
            "type": "TextHeading",
            "text": "Done!"
          },
          {
            "type": "TextBody",
            "text": "**Bold text** and *italic text* are rendered correctly."
          },
          {
            "type": "Footer",
            "label": "Finish",
            "on-click-action": {
              "name": "complete",
              "payload": {}
            }
          }
        ]
      }
    }
  ]
}
```

**Key points:**
- Every screen must have `title` property
- Only TextBody supports `markdown: true` (NOT TextHeading)
- Use Business 3.0 API structure with `name`, `next`, `type` in actions
- Set `markdown: true` to enable formatting
- Markdown syntax: `**bold**`, `*italic*`, `\n` for breaks, `• item` for lists
- `data_api_version: "3.0"` is only needed if calling backend endpoints

---

## Example 1: Simple Multi-Screen Form

A customer survey collecting name, rating, and feedback with a review screen.

```json
{
  "version": "7.1",
  "screens": [
    {
      "id": "WELCOME",
      "title": "Survey",
      "layout": {
        "type": "SingleColumnLayout",
        "children": [
          {
            "type": "TextHeading",
            "text": "Customer Feedback"
          },
          {
            "type": "TextBody",
            "text": "Help us improve with quick feedback."
          },
          {
            "type": "Footer",
            "label": "Start",
            "on-click-action": {
              "action": "navigate",
              "next_screen": "COLLECT_NAME"
            }
          }
        ]
      }
    },
    {
      "id": "COLLECT_NAME",
      "title": "Your Name",
      "layout": {
        "type": "SingleColumnLayout",
        "children": [
          {
            "type": "TextHeading",
            "text": "What's your name?"
          },
          {
            "type": "TextInput",
            "name": "first_name",
            "label": "First Name",
            "required": true
          },
          {
            "type": "TextInput",
            "name": "last_name",
            "label": "Last Name",
            "required": true
          },
          {
            "type": "Footer",
            "label": "Continue",
            "on-click-action": {
              "action": "navigate",
              "next_screen": "COLLECT_FEEDBACK"
            }
          }
        ]
      }
    },
    {
      "id": "COLLECT_FEEDBACK",
      "title": "Your Rating",
      "layout": {
        "type": "SingleColumnLayout",
        "children": [
          {
            "type": "TextHeading",
            "text": "Rate your experience"
          },
          {
            "type": "RadioButtonsGroup",
            "name": "rating",
            "label": "How would you rate us?",
            "data-source": {
              "type": "static",
              "values": ["Very Satisfied", "Satisfied", "Neutral", "Dissatisfied"]
            },
            "required": true
          },
          {
            "type": "TextArea",
            "name": "comments",
            "label": "Additional comments",
            "placeholder": "Tell us how to improve...",
            "max-length": 200
          },
          {
            "type": "Footer",
            "label": "Review",
            "on-click-action": {
              "action": "navigate",
              "next_screen": "CONFIRMATION"
            }
          }
        ]
      }
    },
    {
      "id": "CONFIRMATION",
      "title": "Review",
      "layout": {
        "type": "SingleColumnLayout",
        "children": [
          {
            "type": "TextHeading",
            "text": "Review Your Response"
          },
          {
            "type": "TextBody",
            "text": "Name: ${screen.COLLECT_NAME.form.first_name} ${screen.COLLECT_NAME.form.last_name}"
          },
          {
            "type": "TextBody",
            "text": "Rating: ${screen.COLLECT_FEEDBACK.form.rating}"
          },
          {
            "type": "TextBody",
            "text": "Comments: ${screen.COLLECT_FEEDBACK.form.comments}"
          },
          {
            "type": "Footer",
            "label": "Submit",
            "on-click-action": {
              "action": "complete",
              "payload": {
                "first_name": "${screen.COLLECT_NAME.form.first_name}",
                "last_name": "${screen.COLLECT_NAME.form.last_name}",
                "rating": "${screen.COLLECT_FEEDBACK.form.rating}",
                "comments": "${screen.COLLECT_FEEDBACK.form.comments}"
              }
            }
          }
        ]
      }
    }
  ]
}
```

**Key features**: Multi-screen navigation, global references (`${screen.X.form.Y}`), form data collection, review screen, complete action.

---

## Example 2: Conditional Branching with Age Verification

Uses If component to show different screens based on user age.

```json
{
  "version": "7.1",
  "screens": [
    {
      "id": "AGE_INPUT",
      "title": "Age Verification",
      "layout": {
        "type": "SingleColumnLayout",
        "children": [
          {
            "type": "TextHeading",
            "text": "Age Verification"
          },
          {
            "type": "TextInput",
            "name": "age",
            "label": "Enter your age",
            "input-type": "number",
            "required": true
          },
          {
            "type": "Footer",
            "label": "Check",
            "on-click-action": {
              "action": "navigate",
              "next_screen": "ELIGIBILITY_CHECK"
            }
          }
        ]
      }
    },
    {
      "id": "ELIGIBILITY_CHECK",
      "layout": {
        "type": "SingleColumnLayout",
        "children": [
          {
            "type": "If",
            "condition": "${`${form.age} >= 18`}",
            "then": [
              {
                "type": "TextHeading",
                "text": "You're Eligible!"
              },
              {
                "type": "TextBody",
                "text": "You qualify for our premium services."
              },
              {
                "type": "Footer",
                "label": "Proceed",
                "on-click-action": {
                  "action": "navigate",
                  "next_screen": "ELIGIBLE_SUCCESS"
                }
              }
            ],
            "else": [
              {
                "type": "TextHeading",
                "text": "Not Yet Eligible"
              },
              {
                "type": "TextBody",
                "text": "You must be 18+ for this service. Parental consent available."
              },
              {
                "type": "Footer",
                "label": "Request Consent",
                "on-click-action": {
                  "action": "navigate",
                  "next_screen": "REQUEST_CONSENT"
                }
              }
            ]
          }
        ]
      }
    },
    {
      "id": "ELIGIBLE_SUCCESS",
      "terminal": true,
      "success": true,
      "layout": {
        "type": "SingleColumnLayout",
        "children": [
          {
            "type": "TextHeading",
            "text": "Welcome!"
          },
          {
            "type": "TextBody",
            "text": "Access granted (Age: ${form.age})"
          },
          {
            "type": "Footer",
            "label": "Done",
            "on-click-action": {
              "action": "complete",
              "payload": {
                "status": "eligible",
                "age": "${form.age}"
              }
            }
          }
        ]
      }
    },
    {
      "id": "REQUEST_CONSENT",
      "layout": {
        "type": "SingleColumnLayout",
        "children": [
          {
            "type": "TextHeading",
            "text": "Parental Consent"
          },
          {
            "type": "TextInput",
            "name": "parent_email",
            "label": "Parent/Guardian Email",
            "input-type": "email",
            "required": true
          },
          {
            "type": "Footer",
            "label": "Send Request",
            "on-click-action": {
              "action": "complete",
              "payload": {
                "status": "pending_consent",
                "age": "${form.age}",
                "parent_email": "${form.parent_email}"
              }
            }
          }
        ]
      }
    }
  ]
}
```

**Key features**: If component with conditional branching, nested expressions (`${`...`}`), different screen flows, age expression evaluation.

---

## Example 3: E-Commerce with Dynamic Server Data

Product selection with server-provided product list and dynamic data binding.

```json
{
  "version": "7.1",
  "screens": [
    {
      "id": "CATEGORY_SELECT",
      "title": "Shop",
      "layout": {
        "type": "SingleColumnLayout",
        "children": [
          {
            "type": "TextHeading",
            "text": "Select Category"
          },
          {
            "type": "RadioButtonsGroup",
            "name": "category",
            "data-source": {
              "type": "static",
              "values": ["Electronics", "Clothing", "Home", "Sports"]
            },
            "required": true
          },
          {
            "type": "Footer",
            "label": "Show Products",
            "on-click-action": {
              "action": "navigate",
              "next_screen": "PRODUCT_LIST"
            }
          }
        ]
      }
    },
    {
      "id": "PRODUCT_LIST",
      "title": "Products",
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
              { "id": "001", "name": "Product A", "price": 29.99 }
            ]
          }
        }
      },
      "layout": {
        "type": "SingleColumnLayout",
        "children": [
          {
            "type": "TextHeading",
            "text": "Products"
          },
          {
            "type": "TextBody",
            "text": "Category: ${form.category}"
          },
          {
            "type": "Dropdown",
            "name": "selected_product",
            "label": "Choose Product",
            "data-source": {
              "type": "dynamic",
              "values": "${data.products}"
            },
            "required": true
          },
          {
            "type": "Footer",
            "label": "Details",
            "on-click-action": {
              "action": "navigate",
              "next_screen": "PRODUCT_DETAILS"
            }
          }
        ]
      }
    },
    {
      "id": "PRODUCT_DETAILS",
      "title": "Details",
      "layout": {
        "type": "SingleColumnLayout",
        "children": [
          {
            "type": "TextHeading",
            "text": "Order Details"
          },
          {
            "type": "TextBody",
            "text": "Product: ${screen.PRODUCT_LIST.form.selected_product}"
          },
          {
            "type": "TextInput",
            "name": "quantity",
            "label": "Quantity",
            "input-type": "number",
            "init-value": "1",
            "required": true
          },
          {
            "type": "CheckboxGroup",
            "name": "gift_wrap",
            "data-source": {
              "type": "static",
              "values": ["Add Gift Wrapping ($5)"]
            }
          },
          {
            "type": "Footer",
            "label": "Add to Cart",
            "on-click-action": {
              "action": "complete",
              "payload": {
                "category": "${form.category}",
                "product": "${screen.PRODUCT_LIST.form.selected_product}",
                "quantity": "${form.quantity}",
                "gift_wrap": "${form.gift_wrap}"
              }
            }
          }
        ]
      }
    }
  ]
}
```

**Key features**: Dynamic data from server (`${data.products}`), dynamic dropdown binding, global references across multiple screens, e-commerce pattern.

---

## Pattern: Multi-Step Form with Server Validation

For forms that validate with a server endpoint, use `routing_model`:

```json
{
  "version": "7.1",
  "data_api_version": "3.0",
  "routing_model": {
    "EMAIL_INPUT": ["EMAIL_VALID", "EMAIL_ERROR"],
    "EMAIL_VALID": ["SUCCESS"],
    "EMAIL_ERROR": []
  },
  "screens": [
    {
      "id": "EMAIL_INPUT",
      "layout": {
        "type": "SingleColumnLayout",
        "children": [
          {
            "type": "TextInput",
            "name": "email",
            "input-type": "email",
            "label": "Email",
            "required": true
          },
          {
            "type": "Footer",
            "label": "Validate",
            "on-click-action": {
              "action": "data_exchange",
              "payload": { "email": "${form.email}" }
            }
          }
        ]
      }
    },
    {
      "id": "EMAIL_VALID",
      "layout": {
        "type": "SingleColumnLayout",
        "children": [
          {
            "type": "TextHeading",
            "text": "Email Verified"
          },
          {
            "type": "Footer",
            "label": "Continue",
            "on-click-action": {
              "action": "navigate",
              "next_screen": "SUCCESS"
            }
          }
        ]
      }
    },
    {
      "id": "EMAIL_ERROR",
      "terminal": true,
      "success": false,
      "layout": {
        "type": "SingleColumnLayout",
        "children": [
          {
            "type": "TextBody",
            "text": "Email validation failed"
          },
          {
            "type": "Footer",
            "label": "Back"
          }
        ]
      }
    },
    {
      "id": "SUCCESS",
      "terminal": true,
      "success": true,
      "layout": {
        "type": "SingleColumnLayout",
        "children": [
          {
            "type": "TextHeading",
            "text": "Success!"
          },
          {
            "type": "Footer",
            "label": "Done",
            "on-click-action": {
              "action": "complete",
              "payload": { "email": "${form.email}" }
            }
          }
        ]
      }
    }
  ]
}
```

Server endpoint receives:
```json
{
  "data": {
    "screen": "EMAIL_INPUT",
    "data": { "email": "user@example.com" }
  }
}
```

Server responds with:
```json
{
  "screen": "EMAIL_VALID",
  "data": {}
}
```

Or on error:
```json
{
  "screen": "EMAIL_ERROR",
  "errors": { "email": "Email already registered" }
}
```
