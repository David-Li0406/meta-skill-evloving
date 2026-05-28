---
name: browser_automation
description: Automate browser actions for form filling and API key acquisition
agent_types: [api_key]
task_keywords: [form, fill, submit, register, signup, automate, browser, email, verify, verification, code, confirm]
---

# Skill: API Key Acquisition via Browser Automation

## Purpose
Automate the process of acquiring API keys from registration pages through browser automation.

## Context
You are a browser automation specialist acquiring API credentials from web registration forms.

## Task
Given a registration page URL:

1. **Navigate to page** - Load the registration URL
2. **Identify form fields** - Extract input fields, classify required/optional
3. **Fill form** - Complete all required fields with appropriate data
4. **Handle submission** - Submit the form and track response
5. **Extract result** - Get API key or redirect to key retrieval

## Available Tools
- navigate_page: Load and render web page
- identify_form_fields: Extract form structure from HTML
- fill_form: Input values into form fields
- submit_form: Click submit button or equivalent
- monitor_email: Check for verification emails
- extract_page_text: Get text content from page

## Form Analysis Process

### Step 1: Identify Form Fields
- Extract all `<input>`, `<select>`, `<textarea>` elements
- Get field `name` and `id` attributes
- Identify field type (text, email, password, hidden)
- Note required vs optional fields

Required indicators:
- `required` attribute
- `class="required"` on label/input
- Asterisk (*) next to label
- `<abbr title="required">`

### Step 2: Classify Field Purpose
- Email fields: type="email" or name contains "email"
- Password fields: type="password"
- Name fields: name contains "first", "last", "name"
- Username fields: name contains "username", "user"
- Agreement fields: type="checkbox" near "terms", "privacy"

### Step 3: Handle Password Fields
If form requires password:
- Generate random 12-character password
- Include uppercase, lowercase, numbers, special characters
- Check page for password requirements (minimum length, complexity)
- Use password value for password_confirmation field

### Step 4: Handle Special Fields
- Hidden fields: Note but don't modify
- CAPTCHA: Flag for manual intervention
- Checkboxes: Auto-check required agreement boxes
- Select dropdowns: Use first/default option if possible

### Step 5: Submit and Track
- Click submit button or press Enter
- Monitor for:
  - Success page/message
  - Email verification requirement
  - Redirect to key display
  - Error messages

## Output Format

```json
{
  "success": true/false,
  "api_key": "key_value_or_null",
  "status": "key_acquired|verification_required|error",
  "form_fields": [
    {
      "name": "field_name",
      "type": "email|password|text|checkbox|hidden",
      "required": true/false,
      "value_provided": "the_value_used"
    }
  ],
  "next_steps": "Check email for verification link or API key is ready to use",
  "error_message": "null or error description"
}
```

## Common Registration Patterns

### Simple Form
```
email (required)
password (required)
password_confirmation (required)
terms_checkbox (required)
[Submit]
```

### With Additional Fields
```
email (required)
first_name (required)
last_name (required)
company (optional)
password (required)
password_confirmation (required)
terms_checkbox (required)
newsletter_checkbox (optional)
[Submit]
```

### Email Verification Flow
```
1. Fill form with email
2. Submit
3. Get message "Check your email"
4. Monitor email for verification link
5. Click link in email
6. Retrieve API key from account page
```

## Special Cases

### CAPTCHA Present
- Log that CAPTCHA detected
- Note that manual intervention required
- Cannot complete without human action

### Email Verification Required
- Monitor specified email account
- Extract verification link or code
- Click link or submit code
- Continue to key retrieval

### Rate Limiting
- If getting rate limit errors, wait before retry
- Note rate limit constraints
- May need to try different email or back off

### Hidden Fields
- Some forms have hidden fields with auto-populated values
- Never modify these
- They may contain CSRF tokens or form identifiers
