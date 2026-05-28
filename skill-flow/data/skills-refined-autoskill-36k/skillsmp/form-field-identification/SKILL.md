---
name: form_field_identification
description: Identify and classify form fields for API key registration
agent_types: [examination, api_key]
task_keywords: [form, field, input, required, optional]
---

# Skill: Identify API Key Registration Form Fields

## Purpose
Analyze HTML pages containing API key request forms and identify the form fields required for submission.

## Context
You are a web crawler analyzing a registration/signup page to programmatically submit API key requests.

## Task
Given an HTML page with an API key registration form:

1. **Identify all input fields** - Extract `name` and/or `id` attributes
2. **Classify fields as required or optional** - Look for:
   - `required` attribute
   - `class="required"` on label or input
   - `<abbr title="required">` markers
3. **Identify the submit element** - Find the button/input that submits the form

## Field Classification

### Required Field Indicators
- `required` attribute on input
- Label contains `class="required"`
- Label contains `<abbr title="required">`
- Asterisk (*) next to label text

### Optional Field Indicators
- `class="optional"` on input
- "(optional)" in label text
- No required indicators present

## Output Format

```
## Required Fields
- field_id_1 (name="field_name_1") - description
- field_id_2 (name="field_name_2") - description

## Optional Fields
- field_id_3 (name="field_name_3") - description

## Submit Element
<element html snippet>
```

## Password Handling
If the form requires a password:
- Generate a random 12-character password
- Include uppercase, lowercase, numbers, and special characters
- Check for any password requirements indicated on the page

## Common Form Patterns

### Standard API Signup
```
user[first_name], user[last_name], user[email]
```

### Account Creation
```
user[username], user[email], user[password], user[password_confirmation]
```

## Additional Considerations

- **Hidden fields**: Note `type="hidden"` fields that may need specific values
- **Checkboxes**: Identify required agreement/consent checkboxes (terms, age verification)
- **CAPTCHA**: Note if reCAPTCHA or similar is present (may require manual intervention)
- **Form ID**: Capture the form's `id` attribute for targeting
