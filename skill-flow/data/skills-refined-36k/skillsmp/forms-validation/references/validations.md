# Forms Validation - Validations

## Form without noValidate

### **Id**
form-no-novalidate
### **Severity**
info
### **Type**
regex
### **Pattern**
  - <form(?!.*noValidate)
### **Message**
Add noValidate to prevent browser validation competing with custom
### **Fix Action**
Add noValidate attribute to form
### **Applies To**
  - *.tsx
  - *.jsx

## Input without aria-invalid

### **Id**
input-no-aria-invalid
### **Severity**
info
### **Type**
regex
### **Pattern**
  - errors\.[\w]+.*\n.*<input(?!.*aria-invalid)
### **Message**
Add aria-invalid for accessibility
### **Fix Action**
Add aria-invalid={!!errors.fieldName}
### **Applies To**
  - *.tsx
  - *.jsx

## Error message without role=alert

### **Id**
error-no-role-alert
### **Severity**
info
### **Type**
regex
### **Pattern**
  - errors\.[\w]+\.message.*<span(?!.*role)
### **Message**
Add role=alert to error messages for screen readers
### **Fix Action**
Add role="alert" to error span
### **Applies To**
  - *.tsx
  - *.jsx

## Submit button not disabled during submission

### **Id**
submit-no-disabled
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - isSubmitting.*<button.*type="submit"(?!.*disabled)
### **Message**
Disable submit button during submission
### **Fix Action**
Add disabled={isSubmitting}
### **Applies To**
  - *.tsx
  - *.jsx

## Zod number without coercion for forms

### **Id**
zod-number-no-coerce
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - z\.number\(\)(?!.*coerce)
  - z\.object.*formData.*z\.number\(\)
### **Message**
Use z.coerce.number() for form data
### **Fix Action**
Replace z.number() with z.coerce.number()
### **Applies To**
  - *.ts
  - *.tsx

## Form without server-side validation

### **Id**
no-server-validation
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - export async function.*formData.*(?!.*safeParse|.*parse\()
### **Message**
Always validate form data on server
### **Fix Action**
Add Zod validation with safeParse
### **Applies To**
  - *.ts

## Form reset called in error path

### **Id**
form-reset-on-error
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - catch.*{[^}]*reset\(\)
  - error.*{[^}]*form\.reset
### **Message**
Do not reset form on error - preserve user input
### **Fix Action**
Remove reset() from error handler
### **Applies To**
  - *.tsx
  - *.jsx

## Using alert for form errors

### **Id**
alert-for-form-errors
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - alert\(["'].*error
  - alert\(["'].*required
  - alert\(["'].*invalid
### **Message**
Use inline errors instead of alert()
### **Fix Action**
Show errors next to form fields
### **Applies To**
  - *.tsx
  - *.jsx
  - *.ts
  - *.js