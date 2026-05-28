# Server Integration Reference

Build stateful flows with routing models and data endpoints (v4.0+).

## When to Use Server Integration

Use when:
- Validating user input with business logic
- Fetching dynamic data (products, categories, prices)
- Storing form submissions
- Implementing complex conditional routing
- Securing sensitive operations

Don't use when:
- Simple static flows
- No backend needed
- No dynamic data required

---

## Enabling Server Integration

Two required properties:

```json
{
  "version": "7.1",
  "data_api_version": "3.0",
  "routing_model": {
    "SCREEN_1": ["SCREEN_2", "ERROR"],
    "SCREEN_2": ["SUCCESS"]
  },
  "screens": [...]
}
```

**Properties:**
- `data_api_version` - Currently "3.0" (required)
- `routing_model` - Defines allowed transitions (required)

---

## Routing Model

Defines which screens can connect to which other screens.

**Structure:**
```json
{
  "routing_model": {
    "SOURCE_SCREEN": ["dest1", "dest2", "..."],
    "ANOTHER_SCREEN": ["next_screen"],
    "TERMINAL_SCREEN": []
  }
}
```

**Properties:**
- Key: Source screen ID
- Value: Array of screens that can be navigated to

### Example: Email Validation

```json
{
  "routing_model": {
    "EMAIL_INPUT": ["EMAIL_VALID", "EMAIL_ERROR"],
    "EMAIL_VALID": ["SUCCESS"],
    "EMAIL_ERROR": [],
    "SUCCESS": []
  }
}
```

**Flow:**
- Email input can go to valid or error
- Valid email goes to success
- Error is terminal
- Success is terminal

### Rules

1. **All referenced screens must exist** in screens array
2. **Entry screen** has no inbound edges (nothing routes to it)
3. **Terminal screens** have empty array (nothing routes from them)
4. **Max 10 branches** per screen
5. **No self-routes** (can't route to same screen)
6. **All paths must end** at terminal screen
7. **Reserved IDs**: `SUCCESS` (optional), `ERROR` (optional)

---

## Data Endpoint Configuration

Server endpoint URL configured via Facebook Developers API (not in Flow JSON):

```
POST /api/flows/create
{
  "name": "My Flow",
  "flow_json": { ... },
  "data_channel_uri": "https://your-server.com/whatsapp/flow"
}
```

### Endpoint Request

User submits form → Server receives:

```json
{
  "flow_id": "abc123",
  "flow_token": "token123",
  "data": {
    "screen": "CURRENT_SCREEN",
    "data": {
      "field1": "value1",
      "field2": "value2"
    }
  }
}
```

### Endpoint Response

Server processes and responds:

```json
{
  "version": "3.0",
  "screen": "NEXT_SCREEN",
  "data": {
    "field": "value",
    "list": ["item1", "item2"]
  },
  "errors": {
    "field1": "Error message for field1"
  }
}
```

**Response properties:**
- `screen` (required) - Next screen ID from routing_model
- `data` - Dynamic data for new screen (matches screen's data schema)
- `errors` (optional) - Field validation errors (stays on same screen)

---

## Request/Response Flow

```
1. User fills form on SCREEN_1
2. User taps Footer with data_exchange action
3. Client sends request to server endpoint
4. Server receives payload data
5. Server validates, processes, queries database
6. Server decides next screen from routing_model
7. Server sends response with:
   - "screen": SCREEN_2
   - "data": {...dynamic data...}
8. Client navigates to SCREEN_2
9. SCREEN_2 displays with ${data.field} values
```

---

## Example: Email Validation

### Flow Definition

```json
{
  "version": "7.1",
  "data_api_version": "3.0",
  "routing_model": {
    "ENTER_EMAIL": ["EMAIL_VALID", "EMAIL_ERROR"],
    "EMAIL_VALID": ["SUCCESS"],
    "EMAIL_ERROR": [],
    "SUCCESS": []
  },
  "screens": [
    {
      "id": "ENTER_EMAIL",
      "layout": {
        "type": "SingleColumnLayout",
        "children": [
          {
            "type": "TextInput",
            "name": "email",
            "input-type": "email",
            "label": "Email Address",
            "required": true
          },
          {
            "type": "Footer",
            "label": "Validate",
            "on-click-action": {
              "action": "data_exchange",
              "payload": {
                "email": "${form.email}"
              }
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
            "text": "Email validation failed. Please try again."
          },
          {
            "type": "Footer",
            "label": "Back",
            "on-click-action": {
              "action": "navigate",
              "next_screen": "ENTER_EMAIL"
            }
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
              "payload": {
                "status": "success",
                "email": "${form.email}"
              }
            }
          }
        ]
      }
    }
  ]
}
```

### Server Implementation (Python)

```python
from flask import Flask, request, jsonify
import re

app = Flask(__name__)

@app.route('/whatsapp/flow', methods=['POST'])
def handle_flow():
    data = request.json
    screen = data['data']['screen']
    form_data = data['data']['data']

    if screen == 'ENTER_EMAIL':
        email = form_data.get('email', '')

        # Validate email format
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            return jsonify({
                'version': '3.0',
                'screen': 'EMAIL_ERROR',
                'errors': {
                    'email': 'Invalid email format'
                }
            })

        # Check if email exists in database
        if email_exists_in_db(email):
            return jsonify({
                'version': '3.0',
                'screen': 'EMAIL_ERROR',
                'errors': {
                    'email': 'Email already registered'
                }
            })

        # Email valid, proceed
        return jsonify({
            'version': '3.0',
            'screen': 'EMAIL_VALID',
            'data': {}
        })

    return jsonify({
        'version': '3.0',
        'screen': 'EMAIL_ERROR'
    })

def email_exists_in_db(email):
    # Check your database
    return False
```

---

## Example: Dynamic Product Selection

### Flow with Server Data

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
          { "id": "P001", "name": "Laptop", "price": 999.99 }
        ]
      }
    }
  },
  "layout": {
    "type": "SingleColumnLayout",
    "children": [
      {
        "type": "Dropdown",
        "name": "product",
        "label": "Select Product",
        "data-source": {
          "type": "dynamic",
          "values": "${data.products}"
        }
      },
      {
        "type": "Footer",
        "label": "Order",
        "on-click-action": {
          "action": "data_exchange",
          "payload": {
            "product_id": "${form.product}"
          }
        }
      }
    ]
  }
}
```

### Server Returns Products

```python
@app.route('/whatsapp/flow', methods=['POST'])
def handle_flow():
    data = request.json
    screen = data['data']['screen']

    if screen == 'PRODUCT_LIST':
        # Query database for products
        products = [
            {'id': 'P001', 'name': 'Laptop', 'price': 999.99},
            {'id': 'P002', 'name': 'Mouse', 'price': 29.99},
            {'id': 'P003', 'name': 'Keyboard', 'price': 79.99}
        ]

        return jsonify({
            'version': '3.0',
            'screen': 'PRODUCT_LIST',
            'data': {
                'products': products
            }
        })
```

---

## Error Handling

When validation fails, return errors without navigation:

```json
{
  "version": "3.0",
  "screen": "SAME_SCREEN",
  "errors": {
    "email": "Email is already registered",
    "phone": "Invalid phone format"
  }
}
```

**Rules:**
- Stay on same screen
- Display field errors to user
- User corrects and retries
- No screen change until valid

---

## Data Exchange Action

```json
{
  "type": "Footer",
  "label": "Submit",
  "on-click-action": {
    "action": "data_exchange",
    "payload": {
      "email": "${form.email}",
      "name": "${form.name}",
      "category": "${form.category}"
    }
  }
}
```

Payload can include:
- Form data: `${form.field}`
- Server data from same screen: `${data.field}`
- Global references: `${screen.X.form.field}`
- Nested expressions: `${`${form.age} >= 18`}`

---

## Security Considerations

1. **Validate all input** - Never trust client data
2. **HTTPS only** - Encrypt all communication
3. **Authenticate requests** - Verify flow_token
4. **Rate limiting** - Prevent abuse
5. **Sanitize data** - Prevent injection attacks
6. **Secure sensitive data** - Don't expose passwords, SSNs
7. **Log submissions** - Audit trail
8. **GDPR compliance** - Handle user data properly
9. **Timeout requests** - Long responses harm UX
10. **Monitor errors** - Track failed requests

---

## Best Practices

1. **Fast responses** - Keep latency < 1 second
2. **Meaningful errors** - Tell users what's wrong
3. **Validate comprehensively** - Check everything server-side
4. **Handle edge cases** - NULL, empty, invalid values
5. **Test thoroughly** - All paths, error scenarios
6. **Monitor performance** - Track endpoint metrics
7. **Version your API** - Support multiple flow versions
8. **Document clearly** - Help developers understand flow
9. **Rollback capability** - Revert flows if needed
10. **Audit logging** - Track all submissions

---

## Debugging

**Test locally:**
```bash
# Simulate client request
curl -X POST http://localhost:5000/whatsapp/flow \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "screen": "ENTER_EMAIL",
      "data": {"email": "test@example.com"}
    }
  }'
```

**Check routing:**
- Verify all screens in routing_model exist
- Verify entry screen has no inbound edges
- Verify terminal screens have no outbound
- Check max 10 branches rule

**Validate responses:**
- `screen` must be in routing_model destinations
- `data` must match screen's data schema
- `errors` should match form field names
