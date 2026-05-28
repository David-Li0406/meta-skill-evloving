# Form Error Handling

## Template Error Display

### Required Import

You **MUST** import `OneUiFormErrorDirective` in your component to use the `oneUiFormError` directive:

```typescript
import { OneUiFormErrorDirective } from '@one-ui/shared/ui/form';

@Component({
  imports: [
    // ... other imports
    OneUiFormErrorDirective  // ✅ Required
  ]
})
```

### Basic Usage

Use `oneUiFormError` directive to automatically display error messages:

```html
<mat-form-field>
  <mat-label>{{ t('general.common_account.username') }}</mat-label>
  <input matInput formControlName="username" />
  <mat-error oneUiFormError="username"></mat-error>
</mat-form-field>
```

This will automatically show the correct i18n error message based on the validation error.

---

## CRITICAL: Always Specify Control Name

**CRITICAL:** Always specify the control name in `oneUiFormError` directive to prevent displaying errors from wrong controls:

### ❌ Wrong - No control name

```html
<mat-error oneUiFormError></mat-error>
<!-- May display errors from other controls! -->
```

### ✅ Correct - With control name

```html
<mat-error oneUiFormError="username"></mat-error>
<mat-error oneUiFormError="password"></mat-error>
<mat-error oneUiFormError="email"></mat-error>
```

---

## Handling Custom Errors

For custom errors (like `duplicate`, `notSame`) that are set manually via `setErrors()`, you must handle them separately since they don't have the `__renderErrorMessage__` function:

```html
<!-- Pattern: Check custom error first, fallback to oneUiFormError -->
<mat-form-field>
  <mat-label>{{ t('general.common_account.username') }}</mat-label>
  <input matInput formControlName="username" />
  @if (form.controls.username.hasError('duplicate')) {
    <mat-error>{{ t('features.account_management.username_taken') }}</mat-error>
  } @else {
    <mat-error oneUiFormError="username"></mat-error>
  }
</mat-form-field>

<!-- Password confirmation with notSame error -->
<mat-form-field>
  <mat-label>{{ t('general.common_account.confirm_password') }}</mat-label>
  <mx-password-input formControlName="confirmPassword"></mx-password-input>
  @if (form.controls.confirmPassword.hasError('notSame')) {
    <mat-error>{{ t('features.account_management.new_pwd_not_match') }}</mat-error>
  } @else {
    <mat-error oneUiFormError="confirmPassword"></mat-error>
  }
</mat-form-field>
```

---

## Long Error Messages (mat-long-error)

**CRITICAL**: When error messages are long (e.g., listing allowed characters), use the `mat-long-error` class on `mat-form-field` to prevent text truncation and alignment issues.

### When to Use

Use `mat-long-error` for error messages like:
- `invalid_format_system_symbol`: "Not in correct format, must be a-z, A-Z, 0-9 or . - _ @ ! # $ % ^ & * ( )"
- Any error message that lists multiple allowed/disallowed characters
- Field is inside a `.form-row` (horizontal layout) with long error message

### The Problem

Without `mat-long-error`, form fields in a row may not align properly when one has a long error message:

```
┌─────────────────┐      0 / 16
│ Common Name     │      ┌─────────────────┐
│ /]              │      │ Email Address   │
└─────────────────┘      └─────────────────┘
Not in correct format,        ← Misaligned!
must be a-z, A-Z, 0-9...
```

### Pattern: Conditional Class Binding

Apply `mat-long-error` only when the specific error is active:

```html
<!-- ✅ Correct: Conditional class binding -->
<mat-form-field [class.mat-long-error]="form.controls.fieldName.hasError('pattern')">
  @let fieldCtrl = form.controls.fieldName;
  <mat-label>{{ t('field.label') }}</mat-label>
  <input matInput formControlName="fieldName" />
  @if (fieldCtrl.hasError('pattern')) {
    <mat-error>{{ t('validators.invalid_format_system_symbol') }}</mat-error>
  } @else {
    <mat-error oneUiFormError="fieldName"></mat-error>
  }
</mat-form-field>

<!-- ❌ Incorrect: Static class always applied -->
<mat-form-field class="mat-long-error">
  ...
</mat-form-field>
```

### Complete Example (Form Row)

```html
<div class="form-row">
  <mat-form-field [class.mat-long-error]="form.controls.mailhub.hasError('pattern')">
    @let mailhubCtrl = form.controls.mailhub;
    <mat-label mxLabel mxLabelOptional>
      {{ t('features.email_settings.mail_server') }}
    </mat-label>
    <input matInput formControlName="mailhub" [maxlength]="128" />
    <mat-hint align="end">{{ mailhubCtrl.value.length }} / 128</mat-hint>
    @if (mailhubCtrl.hasError('pattern')) {
      <mat-error>{{ t('validators.invalid_format_system_symbol') }}</mat-error>
    } @else {
      <mat-error oneUiFormError="mailhub"></mat-error>
    }
  </mat-form-field>

  <mat-form-field>
    <mat-label>{{ t('features.cert_signing_request.email_address') }}</mat-label>
    <input matInput formControlName="ea" type="email" />
    <mat-error oneUiFormError="ea"></mat-error>
  </mat-form-field>
</div>
```

### Key Points

- Apply `[class.mat-long-error]` on `<mat-form-field>`, NOT on `<mat-error>`
- Use conditional binding to only apply when the long error is active
- Reference the form control directly in the binding (e.g., `form.controls.fieldName.hasError('pattern')`)
- This ensures proper display of long error messages without affecting other error states

### CSS Definition (in `_form.scss`)

```scss
.form-row {
  display: flex;
  flex-direction: row;
  align-items: flex-start;  // ✅ Use flex-start, not center
  gap: 8px;
}

mat-form-field.mat-long-error.ng-invalid.ng-touched {
  margin-bottom: 30px !important;
}
```

**Note:** `.form-row` uses `align-items: flex-start` to ensure fields align at the top when one has an error.

---

## Preserve Error Keys from Old System

When migrating validators, **preserve the same error keys** as the old system for easier verification and translation compatibility:

| Old Error Key | Description |
|---------------|-------------|
| `is_invalid_max_udp_port` | Exceeded max UDP port count |
| `is_invalid_udp_port` | Invalid UDP port (not a number) |
| `is_invalid_range` | Value out of range |
| `is_duplicate_udp_port` | Duplicate UDP port |
| `is_multicst` | Same inbound/outbound interface |
| `duplicate` | Duplicate entry |

---

## Full Form Example

```html
<form [formGroup]="form">
  <!-- Standard field with oneUiFormError -->
  <mat-form-field>
    <mat-label>{{ t('general.common_account.email') }}</mat-label>
    <input matInput formControlName="email" />
    <mat-error oneUiFormError="email"></mat-error>
  </mat-form-field>

  <!-- Field with custom error handling -->
  <mat-form-field>
    <mat-label>{{ t('general.common_account.username') }}</mat-label>
    <input matInput formControlName="username" maxlength="32" />
    <mat-hint align="end">{{ form.controls.username.value?.length || 0 }} / 32</mat-hint>
    @if (form.controls.username.hasError('duplicate')) {
      <mat-error>{{ t('features.account_management.username_taken') }}</mat-error>
    } @else {
      <mat-error oneUiFormError="username"></mat-error>
    }
  </mat-form-field>
</form>
```
