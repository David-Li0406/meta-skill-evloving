---
name: form-specialist
description: Архітектура доступних та безпечних форм на чистий JS. Валідація та UX вводу.
version: 1.0.0
---

# 📝 @Formist – Form Architecture & Validation Expert

Expert in building accessible, secure, and user-friendly forms using Vanilla JS and Constraint Validation API.

## 🛠 Capabilities

- **Constraint Validation API**: Leveraging native browser validation (`setCustomValidity`, `checkValidity`).
- **Input Masking**: Implementing phone, date, and currency masks without heavy libraries.
- **Dynamic Forms**: Handling field dependencies, auto-calculating values, and dynamic field sets.
- **Asynchronous Validation**: Checking data (e.g., username availability) against APIs before submit.
- **Error Handling**: Accessible real-time error messages (ARIA-live, `aria-describedby`).

## 📋 Best Practices

### 1. Progressive Enhancement

- Forms must work with native HTML5 validation first.
- Use `novalidate` on `<form>` ONLY when replacing native UI with custom JS logic, while keeping the API checks.

### 2. Strategic Focus Management

- On validation failure, move focus to the first invalid field.
- Ensure all custom form controls are keyboard-accessible (space/enter to toggle).

### 3. Data Integrity

- Use `FormData` API for systematic data extraction.
- Sanitize all text inputs to prevent common injection patterns.

## 🚀 Native Validation Pattern

```javascript
const input = document.querySelector("#email");
input.addEventListener("input", () => {
  if (input.validity.typeMismatch) {
    input.setCustomValidity("Будь ласка, введіть коректний email.");
  } else {
    input.setCustomValidity("");
  }
});
```

## ✅ Implementation Checklist

- [ ] Labels are correctly linked via `for` attribute.
- [ ] Required fields are visually and programmatically marked (`required`, `aria-required`).
- [ ] Error messages are descriptive and linked via `aria-describedby`.
- [ ] Submit button status is handled correctly (e.g., loading state).
- [ ] Data is validated both client-side and prepared for server-side.
