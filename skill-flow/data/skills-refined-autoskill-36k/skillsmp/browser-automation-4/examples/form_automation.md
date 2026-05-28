# Form Automation Example

## Use Case
Automating form submission with multiple field types.

## Task Setup

```
TaskName: "Submitting Contact Form"

Task: Navigate to https://example.com/contact and complete the contact form:
1. Fill "First Name" field with "John"
2. Fill "Last Name" field with "Doe"
3. Fill "Email" field with "john.doe@example.com"
4. Fill "Phone" field with "+1-555-0100"
5. Select "Technical Support" from the "Department" dropdown
6. Check the "Subscribe to newsletter" checkbox
7. Fill the "Message" textarea with "I need help with product installation"
8. Click the "Submit" button
9. Wait for form submission to complete
10. Verify success message appears
11. Return the confirmation message and any reference number provided

RecordingName: contact_form_submit
```

## Expected Return

```
Status: Form submitted successfully
Confirmation: "Thank you for contacting us! We'll respond within 24 hours."
Reference Number: #CS-2024-0123
Screenshot: Saved to artifacts
```

## Variations

### Multi-Page Form
```
Task: Complete a multi-page registration form:
Page 1: Enter personal details (name, email, phone), click "Next"
Page 2: Enter address details (street, city, zip), click "Next"
Page 3: Choose preferences (newsletter, notifications), click "Submit"
Return confirmation from final page.
```

### Form with File Upload
```
Task: Navigate to the upload form, select the file "document.pdf" using 
the file input, fill in the description field with "Annual Report 2024", 
click upload, wait for upload progress to complete, and return the 
uploaded file URL.
```

### Form Validation Testing
```
Task: Test form validation by:
1. Submitting the form completely empty
2. Note validation errors that appear
3. Fill only email field with invalid format "notanemail"
4. Note email validation error
5. Return all validation messages observed
```

### Dynamic Form Fields
```
Task: On the registration form:
1. Select "Business" from account type dropdown
2. Wait for additional business fields to appear (Company Name, Tax ID)
3. Fill in the newly appeared fields
4. Complete and submit the form
5. Return success confirmation
```

## Common Field Types

### Text Inputs
```
Fill "Username" field with "johndoe123"
```

### Dropdowns/Selects
```
Select "United States" from the "Country" dropdown
```

### Checkboxes
```
Check the "I agree to terms" checkbox
```

### Radio Buttons
```
Select the radio button labeled "Monthly subscription"
```

### Date Pickers
```
Click the "Birth Date" field, select January 15, 1990 from the date picker
```

### Rich Text Editors
```
Click into the rich text editor, type the message, apply bold formatting 
to the first sentence
```
