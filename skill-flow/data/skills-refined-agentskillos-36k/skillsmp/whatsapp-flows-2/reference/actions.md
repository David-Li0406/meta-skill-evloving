# Actions Reference

Complete documentation of all action types that control user interactions and flow progression.

## Actions Overview

Actions define what happens when users interact with components. Available actions: navigate, data_exchange, complete, update_data, open_url.

## Navigate Action

Move to another screen in the flow.

**Syntax:**
```json
{
  "action": "navigate",
  "next_screen": "SCREEN_ID"
}
```

**Properties:**
- `next_screen` (required) - Target screen ID (must exist in screens array)

**Full example:**
```json
{
  "type": "Footer",
  "label": "Continue",
  "on-click-action": {
    "action": "navigate",
    "next_screen": "STEP_2"
  }
}
```

**Rules:**
- Target screen must exist
- Cannot navigate to current screen (no self-reference)
- Used for progression through flow
- No data transformation or validation

**Component support:** Footer, EmbeddedLink, OptIn, NavigationList, ChipsSelector

---

## Data Exchange Action

Send data to server endpoint and receive response. For stateful flows with backend integration.

**Syntax:**
```json
{
  "action": "data_exchange",
  "payload": {
    "field1": "value1",
    "field2": "value2"
  }
}
```

**Properties:**
- `payload` (required) - Data to send to server as JSON

**Full example:**
```json
{
  "type": "Footer",
  "label": "Submit",
  "on-click-action": {
    "action": "data_exchange",
    "payload": {
      "email": "${form.email}",
      "name": "${form.name}",
      "check_type": "registration"
    }
  }
}
```

**How it works:**
1. User submits form
2. Payload sent to data endpoint
3. Server receives and validates
4. Server responds with:
   - `screen`: Next screen ID
   - `data`: Dynamic data for new screen
   - `errors` (optional): Field validation errors
5. Flow continues to specified screen

**Server request format:**
```json
{
  "data": {
    "screen": "CURRENT_SCREEN",
    "data": { "payload": "values" }
  }
}
```

**Server response format:**
```json
{
  "screen": "NEXT_SCREEN",
  "data": { "field": "value" },
  "errors": { "field": "error message" }
}
```

**Response on error:**
If server returns errors, same screen displays with error messages. No navigation occurs.

**Component support:** Footer, DatePicker, all selection components, EmbeddedLink, OptIn

**Requirements:**
- Must have `routing_model` and `data_api_version` defined
- Server endpoint configured via Facebook Developers API
- Response must match screen's `data` schema (if declared)

---

## Complete Action

End the flow and return data to caller. Only for terminal screens.

**Syntax:**
```json
{
  "action": "complete",
  "payload": {
    "key": "value"
  }
}
```

**Properties:**
- `payload` (required) - Data to return in response

**Full example:**
```json
{
  "id": "SUCCESS",
  "terminal": true,
  "success": true,
  "layout": {
    "type": "SingleColumnLayout",
    "children": [
      {
        "type": "TextHeading",
        "text": "Thank You!"
      },
      {
        "type": "Footer",
        "label": "Done",
        "on-click-action": {
          "action": "complete",
          "payload": {
            "status": "success",
            "user_id": "12345",
            "email": "${form.email}",
            "timestamp": "2024-03-15T10:30:00Z"
          }
        }
      }
    ]
  }
}
```

**Rules:**
- Only valid on terminal screens (`terminal: true`)
- Ends the flow immediately
- Caller receives payload in response
- No further screens displayed

**Component support:** Footer (terminal screens only)

---

## Update Data Action (v6.0+)

Update screen state without navigating. For dynamic component updates.

**Syntax:**
```json
{
  "action": "update_data",
  "payload": {
    "field": "new_value"
  }
}
```

**Properties:**
- `payload` (required) - Data to update in screen state

**Full example:**
```json
{
  "type": "Dropdown",
  "name": "category",
  "label": "Category",
  "data-source": {
    "type": "static",
    "values": ["Electronics", "Clothing", "Books"]
  },
  "on-select-action": {
    "action": "update_data",
    "payload": {
      "selected_category": "${form.category}"
    }
  }
}
```

**How it works:**
1. User interacts with component
2. `update_data` updates local state
3. Components using updated data re-render
4. Stays on same screen (no navigation)

**Use cases:**
- Filtering results based on selection
- Showing/hiding content dynamically
- Updating dependent fields

**Component support:** Footer, Dropdown, RadioButtons, CheckboxGroup, ChipsSelector

---

## Open URL Action (v6.0+)

Open external link in browser. For links to external resources.

**Syntax:**
```json
{
  "action": "open_url",
  "url": "https://example.com"
}
```

**Properties:**
- `url` (required) - URL to open (must be HTTPS)

**Full example:**
```json
{
  "type": "EmbeddedLink",
  "text": "Read Terms",
  "on-click-action": {
    "action": "open_url",
    "url": "https://example.com/terms"
  }
}
```

**OptIn example:**
```json
{
  "type": "OptIn",
  "name": "privacy_agree",
  "label": "I agree to privacy policy",
  "action-url": "https://example.com/privacy",
  "action-text": "View Policy"
}
```

**Requirements:**
- Must be HTTPS (no HTTP)
- Public URL
- Opens in external browser
- Returns user to Flow after closing

**Component support:** EmbeddedLink, OptIn

---

## Action Support Matrix

| Component | navigate | data_exchange | complete | update_data | open_url |
|-----------|----------|---------------|----------|-------------|----------|
| Footer | ✓ | ✓ | ✓ | ✓ | ✗ |
| EmbeddedLink | ✓ | ✓ | ✗ | ✗ | ✓ |
| OptIn | ✓ | ✓ | ✗ | ✗ | ✓ |
| DatePicker | ✗ | ✓ | ✗ | ✗ | ✗ |
| Dropdown | ✓* | ✓ | ✗ | ✓ | ✗ |
| RadioButtonsGroup | ✓* | ✓ | ✗ | ✓ | ✗ |
| CheckboxGroup | ✓* | ✓ | ✗ | ✓ | ✗ |
| ChipsSelector | ✓* | ✓ | ✗ | ✓ | ✗ |
| NavigationList | ✓ | ✓ | ✗ | ✗ | ✗ |

*via `on-select-action`

---

## Common Action Patterns

### Multi-Step Form Submission

```
Screen 1: Collect name, email
  → Footer with navigate to Screen 2
Screen 2: Show confirmation
  → Footer with data_exchange to validate
Screen 3 (if valid): Success
  → Footer with complete action
```

### Conditional Routing

```
Screen 1: Collect user type
  → If condition in next screen:
     - Business users: Screen 2A
     - Individual users: Screen 2B
  → Both lead to SUCCESS
```

### Dynamic Filtering

```
Screen 1: Select category
  → on-select-action data_exchange to server
  → Server returns products for category
Screen 2: Products dropdown with ${data.products}
  → on-select-action updates local state
  → Display changes without navigation
```

### Server Validation

```
Screen 1: Email input
  → Footer with data_exchange
  → Server validates email format
  → If valid: navigate to NEXT
  → If invalid: return error, stay on screen
```

---

## Action Execution Flow

### Navigate
```
User clicks → Check component → Execute action → Load next screen → Display screen
```

### Data Exchange
```
User submits → Collect form data → Send to server → Wait for response →
  If success: navigate to screen → If error: show errors, stay on screen
```

### Complete
```
User confirms → Collect payload → Close flow → Return data to caller
```

### Update Data
```
User interacts → Update state → Re-render components using new state → Stay on screen
```

### Open URL
```
User clicks → Open URL in browser → User navigates away → Returns to flow when done
```

---

## Best Practices

1. **Validate server-side** - Never trust client validation alone
2. **Clear button labels** - "Submit", "Continue", "Confirm"
3. **Handle errors gracefully** - Show field errors, allow retry
4. **Use appropriate actions** - Don't use navigate when validation needed
5. **Provide feedback** - Loading states, success messages
6. **Test all paths** - Every navigate, data_exchange, complete
7. **HTTPS only** - open_url must be HTTPS
8. **Meaningful payloads** - Include essential data in complete
9. **Global references** - Use `${screen.X.form.field}` in payloads
10. **Version awareness** - update_data and open_url require v6.0+
