# OneValidators

## What is this?

One-UI's form validation utility, replacing Angular's native `Validators`.

## When to use

When forms need validation (required, length, range, pattern, etc.).

## Quick Reference

| Need | How to Use |
|------|------------|
| Basic validation | `OneValidators.required` / `.maxLength(n)` / `.range(min, max)` |
| Custom error message | `OneValidators.maxLength(8).error('i18n.key')` |
| Custom validator + message | `validatorFnWithMessage(fn, errorMsg, hintMsg?)` |
| Display error (basic validators) | `<mat-error oneUiFormError="field">` → see [Error Display Strategy](#error-display-strategy) |
| Display error (pattern/custom) | `@if/@else` with custom messages → see [Error Display Strategy](#error-display-strategy) |
| Display hint | `<mat-hint oneUiFormHint="field">` → see [mx-components.md](./mx-components.md#form-validation-directives) |

## Validation Flow

**Step 1: Define Validators (TypeScript)**
- Option A: `OneValidators.required`, `OneValidators.maxLength(n)` — built-in validators
- Option B: `validatorFnWithMessage(fn, errorMsg, hintMsg?)` — custom validator with message

**Step 2: Display in Template (HTML)**
- `<mat-error oneUiFormError="fieldName">` — auto-displays error message
- `<mat-hint oneUiFormHint="fieldName">` — auto-displays hint (character count / range)

---

## Error Display Strategy

**CRITICAL**: The way you display error messages depends on the validator type.

### Strategy Decision Table

| Validator Type | Display Method | Reason |
|---------------|----------------|--------|
| **Basic 6** (`required`, `minLength`, `maxLength`, `range`, `rangeLength`, `email`) | ✅ Use `oneUiFormError` directive | Built-in i18n messages |
| **pattern** | ❌ MUST use `@if/@else` | Needs specific message per pattern type |
| **duplicate** | ❌ MUST use `@if/@else` | Needs context-specific message |
| **Custom validators** | ❌ MUST use `@if/@else` | No built-in messages |
| **All other validators** | ❌ MUST use `@if/@else` | Not in basic 6 |

### Pattern 1: Basic Validators (Use Directive)

For the **6 basic validators** with built-in i18n support:

```html
<mat-form-field>
  <mat-label>{{ t('label') }}</mat-label>
  <input matInput formControlName="name" />
  <mat-error oneUiFormError="name"></mat-error>
</mat-form-field>
```

**Built-in i18n messages:**
- `required` → `validators.required`
- `minLength` → `validators.require_min_length`
- `maxLength` → `validators.invalid_max_length`
- `range` → `validators.invalid_range`
- `rangeLength` → `validators.invalid_range`
- `email` → `validators.invalid_email`

### Pattern 2: Pattern/Custom Validators (Use @if/@else)

For **pattern validators** and **custom validators**, you MUST use `@if/@else`:

```html
<mat-form-field>
  <mat-label>{{ t('general.common_account.account') }}</mat-label>
  <input matInput formControlName="account" />
  @if (form.controls.account.hasError('pattern')) {
    <mat-error>{{ t('validators.invalid_format_not_space') }}</mat-error>
  } @else if (form.controls.account.hasError('duplicate')) {
    <mat-error>{{ t('validators.duplicate_account') }}</mat-error>
  } @else {
    <mat-error oneUiFormError="account"></mat-error>
  }
</mat-form-field>
```

### Why This Strategy?

1. **`oneUiFormError` directive** handles the 6 basic validators with built-in i18n
2. **Pattern validation** errors are too generic (`validators.invalid`) without context
3. **Custom validators** need specific messages that only you know
4. **Legacy consistency** - this matches the pattern used in the original codebase

### Common Pattern Error Messages

When using `OneValidators.pattern()` with shared constants from `@one-ui/shared/domain`:

| Pattern Constant | Error Message i18n Key |
|------------------|----------------------|
| `VAILD_REGEX_NOT_SPACE` | `validators.invalid_format_not_space` |
| `VAILD_REGEX_LEVEL_1` | `validators.invalid_regex_level_1` |
| `IPADDR_REGEX` | `validators.invalid_ip_address` |
| `VAILD_MAC` | `validators.invalid_mac_address` |
| `VALID_REGEX_VIRGINIA_GUIDELINE` | `validators.notMeetPolicy` |

### Complete Examples

#### Example 1: Mix of Basic and Pattern Validators

```typescript
// Component
import { OneValidators } from '@one-ui/shared/domain';

form = this.#fb.group({
  name: ['', [OneValidators.required, OneValidators.maxLength(32)]],  // Basic only
  account: ['', [
    OneValidators.required,     // Basic
    OneValidators.maxLength(31), // Basic
    OneValidators.pattern(VAILD_REGEX_NOT_SPACE)  // Pattern - needs custom message!
  ]]
});
```

```html
<!-- Template -->
<!-- Name: Basic validators only - use directive -->
<mat-form-field>
  <mat-label>{{ t('general.common.name') }}</mat-label>
  <input matInput formControlName="name" />
  <mat-error oneUiFormError="name"></mat-error>
</mat-form-field>

<!-- Account: Has pattern validator - use @if/@else -->
<mat-form-field>
  <mat-label>{{ t('general.common_account.account') }}</mat-label>
  <input matInput maxlength="31" formControlName="account" />
  <mat-hint align="end">{{ form.controls.account.value.length }} / 31</mat-hint>
  @if (form.controls.account.hasError('pattern')) {
    <mat-error>{{ t('validators.invalid_format_not_space') }}</mat-error>
  } @else {
    <mat-error oneUiFormError="account"></mat-error>
  }
</mat-form-field>
```

#### Example 2: IP Address with Pattern Validation

```typescript
form = this.#fb.group({
  ipAddress: ['', [
    OneValidators.required,
    OneValidators.pattern(IPADDR_REGEX)
  ]]
});
```

```html
<mat-form-field>
  <mat-label>{{ t('general.common.server_ip_address') }}</mat-label>
  <input matInput formControlName="ipAddress" />
  @if (form.controls.ipAddress.hasError('pattern')) {
    <mat-error>{{ t('validators.invalid_ip_address') }}</mat-error>
  } @else {
    <mat-error oneUiFormError="ipAddress"></mat-error>
  }
</mat-form-field>
```

#### Example 3: Configuration Name with Multiple Patterns

```typescript
form = this.#fb.group({
  configurationName: ['', [
    OneValidators.required,
    OneValidators.maxLength(32),
    OneValidators.pattern(VAILD_REGEX_LEVEL_1)
  ]]
});
```

```html
<mat-form-field>
  <mat-label>{{ t('features.config_bk_res.configuration_name') }}</mat-label>
  <input matInput maxlength="32" formControlName="configurationName" />
  <mat-hint align="end">{{ form.controls.configurationName.value.length }} / 32</mat-hint>
  @if (form.controls.configurationName.hasError('pattern')) {
    <mat-error>{{ t('validators.invalid_regex_level_1') }}</mat-error>
  } @else {
    <mat-error oneUiFormError="configurationName"></mat-error>
  }
</mat-form-field>
```

### ❌ Common Mistakes

```html
<!-- ❌ WRONG: Using directive for pattern validator -->
<mat-form-field>
  <input matInput formControlName="account" />
  <mat-error oneUiFormError="account"></mat-error>  <!-- Will show generic "invalid" message -->
</mat-form-field>

<!-- ✅ CORRECT: Using @if/@else for pattern validator -->
<mat-form-field>
  <input matInput formControlName="account" />
  @if (form.controls.account.hasError('pattern')) {
    <mat-error>{{ t('validators.invalid_format_not_space') }}</mat-error>
  } @else {
    <mat-error oneUiFormError="account"></mat-error>
  }
</mat-form-field>
```

---

## Import

```typescript
import { OneValidators } from '@one-ui/shared/domain';
```

---

## Basic Usage

```typescript
form = this.#fb.group({
  name: ['', [OneValidators.required, OneValidators.maxLength(32)]],
  description: ['', [OneValidators.maxLength(255)]],
  port: ['', [OneValidators.required, OneValidators.range(1, 65535)]]
});
```

---

## Full API

### Basic Validators

| Method | Description | Has Built-in i18n? |
|--------|-------------|-------------------|
| `OneValidators.required` | Required field | ✅ Yes - use directive |
| `OneValidators.minLength(n)` | Minimum length | ✅ Yes - use directive |
| `OneValidators.maxLength(n)` | Maximum length | ✅ Yes - use directive |
| `OneValidators.min(n)` | Minimum value | ⚠️ Use `range()` instead |
| `OneValidators.max(n)` | Maximum value | ⚠️ Use `range()` instead |
| `OneValidators.range(min, max)` | Numeric range | ✅ Yes - use directive |
| `OneValidators.rangeLength(min, max, fieldName)` | Length range | ✅ Yes - use directive |
| `OneValidators.email` | Email format | ✅ Yes - use directive |
| `OneValidators.pattern(regex)` | Regex pattern | ❌ No - use @if/@else |

> **Note**: For numeric range validation, always use `OneValidators.range(min, max)` instead of separate `min()` and `max()` validators.

### Custom Validators

| Method | Description |
|--------|-------------|
| `OneValidators.duplicate(tableData, 'fieldName')` | Duplicate check |
| `OneValidators.matchFieldsValidator('password', 'confirmPassword')` | Field matching |

### Override Error Messages

```typescript
// Default message
OneValidators.minLength(8)

// Custom message
OneValidators.minLength(8).error('validators.notMeetPolicy')
OneValidators.pattern(PATTERN).error('validators.notMeetPolicy')
```

---

## Enhanced Validators

For custom validators that need automatic error/hint message rendering with `oneUiFormError` and `oneUiFormHint` directives.

> 📖 For template usage, see [mx-components.md - Form Validation Directives](./mx-components.md#form-validation-directives)

### validatorFnWithMessage

Wraps a simple `ValidatorFn` with error and optional hint message renderers.

```typescript
import { validatorFnWithMessage } from '@one-ui/shared/domain';

// Basic usage - error message only
const myValidator = validatorFnWithMessage(
  (control) => control.value === 'invalid' ? { invalid: true } : null,
  'validators.invalidValue'  // i18n key for error message
);

// With hint message (common for character count)
const maxLengthValidator = validatorFnWithMessage(
  (control) => control.value?.length > 32 ? { maxLength: true } : null,
  'validators.maxLength',
  (control) => `${control.value?.length ?? 0} / 32`
);
```

### validatorWithMessage

For validators that need parameters (factory function pattern).

```typescript
import { validatorWithMessage } from '@one-ui/shared/domain';

const maxLength = validatorWithMessage(
  (max: number) => (control) =>
    control.value?.length > max ? { maxLength: true } : null,
  (max: number) => `validators.maxLength`,
  (max: number) => (control) => `${control.value?.length ?? 0} / ${max}`
);
```

### Error/Hint Message Types

| Type | Example |
|------|---------|
| i18n key | `'validators.required'` |
| Dynamic function | `(control) => ({ key: 'validators.maxLength', params: { max: 32 } })` |
| String function (hint) | `(control) => \`${control.value?.length ?? 0} / 32\`` |

### Why Use Enhanced Validators?

| Without Enhanced Validators | With Enhanced Validators |
|----------------------------|--------------------------|
| Manual `{{ form.get('x')?.value?.length }} / 32` | `<mat-hint oneUiFormHint="x">` |
| Manual `*ngIf` for each error type | `<mat-error oneUiFormError="x">` |
| Repeated error message logic | Centralized in validator |
| No i18n support in hints | Automatic i18n translation |

---

## MXSecurity-specific Validators

```typescript
import { Validators } from '@one-ui/mxsecurity/shared/ui';

// Pattern validators
Validators.name32          // a-z, A-Z, 0-9, . _ - (max 32)
Validators.name50          // a-z, A-Z, 0-9, . _ - (max 50)
Validators.ipv4            // IPv4 format
Validators.domain          // FQDN format
Validators.portPattern     // 1-65535

// Function validators
Validators.ipOrDomain      // IPv4 OR domain
Validators.port            // Port number
Validators.passwordStrength(level, minLen)
Validators.passwordMatch() // FormGroup-level

// Async validators
Validators.usernameExists(500)
Validators.emailExists(500, excludeEmail?)
```

---

## Common Mistakes

```typescript
// ❌ WRONG: Using Angular's native Validators
import { Validators } from '@angular/forms';
Validators.required
Validators.minLength(3)

// ✅ CORRECT: Using OneValidators
import { OneValidators } from '@one-ui/shared/domain';
OneValidators.required
OneValidators.minLength(3)
```

---

## Complete Example

```typescript
// ===== Component =====
import { OneValidators, validatorFnWithMessage } from '@one-ui/shared/domain';

// Custom validator with character count hint
const descriptionValidator = validatorFnWithMessage(
  (c) => (c.value?.length ?? 0) > 255 ? { maxLength: true } : null,
  'validators.maxLength',
  (c) => `${c.value?.length ?? 0} / 255`
);

form = this.#fb.group({
  name: ['', [OneValidators.required, OneValidators.maxLength(32)]],
  port: [514, [OneValidators.required, OneValidators.range(1, 65535)]],
  description: ['', [descriptionValidator]]
});
```

```html
<!-- ===== Template ===== -->
<form [formGroup]="form">
  <!-- Name field -->
  <mat-form-field>
    <mat-label>{{ t('field.name') }}</mat-label>
    <input matInput formControlName="name" />
    <mat-error oneUiFormError="name"></mat-error>
  </mat-form-field>

  <!-- Port field with number-only input -->
  <mat-form-field>
    <mat-label>{{ t('field.port') }}</mat-label>
    <input matInput type="text" oneUiNumberOnly formControlName="port" />
    <mat-hint oneUiFormHint="port"></mat-hint>  <!-- Shows "1 ~ 65535" -->
    <mat-error oneUiFormError="port"></mat-error>
  </mat-form-field>

  <!-- Description with character count -->
  <mat-form-field>
    <mat-label>{{ t('field.description') }}</mat-label>
    <textarea matInput formControlName="description"></textarea>
    <mat-hint oneUiFormHint="description"></mat-hint>  <!-- Shows "0 / 255" -->
    <mat-error oneUiFormError="description"></mat-error>
  </mat-form-field>
</form>
```

---

## Related Tools

- [form-builder.md](./form-builder.md) - NonNullableFormBuilder
- [mx-components.md](./mx-components.md#form-validation-directives) - oneUiFormError / oneUiFormHint directives
