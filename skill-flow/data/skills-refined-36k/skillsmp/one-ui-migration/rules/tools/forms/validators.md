# OneValidators Usage Guide

## CRITICAL: Use OneValidators Instead of Angular Validators

**ALWAYS** use `OneValidators` from `@one-ui/mxsecurity/shared/domain` instead of Angular's built-in `Validators`.

### ❌ Old Pattern (Angular 16)

```typescript
import { Validators } from '@angular/forms';
import { ValidatorPattern } from '@mxsecurity-web/shared/validator/validators';

this.form = this.fb.group({
  username: ['', [Validators.required, Validators.minLength(4), Validators.maxLength(32)]],
  password: ['', [Validators.required, Validators.pattern(ValidatorPattern.VALID_REGEX_VIRGINIA_GUIDELINE)]],
  email: ['', [Validators.required, Validators.email]]
});
```

### ✅ New Pattern (Angular 20)

```typescript
import { OneValidators } from '@one-ui/mxsecurity/shared/domain';
import { OneUiFormErrorDirective } from '@one-ui/shared/ui/form';

@Component({
  imports: [
    ReactiveFormsModule,
    MatFormFieldModule,
    MatInputModule,
    OneUiFormErrorDirective  // ✅ Required for oneUiFormError directive
  ]
})
export class MyFormComponent {
  readonly #fb = inject(NonNullableFormBuilder);

  form = this.#fb.group({
    username: ['', [OneValidators.required, OneValidators.maxLength(32)]],
    password: ['', [OneValidators.required, OneValidators.minLength(8)]],
    email: ['', [OneValidators.required, OneValidators.email]]
  });
}
```

## Why OneValidators?

OneValidators provides:

- ✅ **Built-in i18n error messages** - Automatically translated
- ✅ **Better UX** - Error messages work with `oneUiFormError` directive
- ✅ **Type safety** - Full TypeScript support
- ✅ **Consistency** - Unified validation across the entire app

## Available OneValidators

### **Basic Validators**

```typescript
OneValidators.required        // Required field (no parentheses - already a ValidatorFn)
OneValidators.minLength(4)    // Minimum string length
OneValidators.maxLength(32)   // Maximum string length
OneValidators.pattern(REGEX)  // Regex pattern (import pattern constants from shared/domain)
OneValidators.range(1, 100)   // Number range (min/max) - USE THIS FOR NUMERIC VALUES
OneValidators.rangeLength(4, 32, 'Username')  // String length range with field name
OneValidators.email           // Email validation (no parentheses)
```

> **IMPORTANT:** `OneValidators` does NOT have separate `min()` or `max()` validators. For numeric range validation, always use `OneValidators.range(min, max)`.

> **Note:** `OneValidators` only provides basic, commonly-used validators. For pattern validation, always use `OneValidators.pattern()` with imported pattern constants.

### **MXsecurity Custom Validators**

```typescript
OneValidators.duplicate(tableData, 'name')  // Check uniqueness in table
OneValidators.checkHostMac()                // Ensure it's not a multicast MAC
OneValidators.checkSpaceCount(4)            // Max 4 spaces
OneValidators.matchFieldsValidator('password', 'confirmPassword')  // Cross-field match
```

---

## Using Shared Pattern Constants

**IMPORTANT**: When using `OneValidators.pattern()`, always import pattern constants from `@one-ui/mxsecurity/shared/domain` instead of defining local regex patterns. The pattern names are preserved from the original `ValidatorPattern` class for easier code review.

```typescript
// ❌ BAD: Local pattern definition
const VALID_REGEX = /^[0-9a-zA-Z_@!#$%^&*()./ -]+$/;
OneValidators.pattern(VALID_REGEX)

// ✅ GOOD: Import shared pattern constant (same name as ValidatorPattern.VAILD_REGEX)
import { OneValidators, VAILD_REGEX } from '@one-ui/mxsecurity/shared/domain';
OneValidators.pattern(VAILD_REGEX)
```

### Available Pattern Constants

All patterns from `ValidatorPattern` class are available with the **same names**:

| Pattern Constant                          | Description                                      |
| ----------------------------------------- | ------------------------------------------------ |
| `IPADDR_REGEX`                            | IPv4 address (0.0.0.0 - 255.255.255.255)         |
| `IPADDR_NOT_ZERO_REGEX`                   | IPv4 address (first octet 1-255)                 |
| `VAILD_REGEX`                             | Alphanumeric + special chars + space             |
| `VALID_REGEX_NEWLINE`                     | Same as VAILD_REGEX + newline                    |
| `VALID_REGEX_VIRGINIA_GUIDELINE`          | Virginia guideline password chars                |
| `VALID_REGEX_VIRGINIA_GUIDELINE_WITH_ANGLE` | Virginia guideline + angle brackets            |
| `VAILD_REGEX_ALLOW_COMMA`                 | VAILD_REGEX + comma                              |
| `VAILD_REGEX_NOT_SPACE`                   | Alphanumeric + special chars (no space)          |
| `VAILD_REGEX_NOT_SPACE_WITH_FIRST_NOT_NUMBER` | No space, first char not number              |
| `VALID_REGEX_FIRST_NOT_NUMBER_AND_NOT_SPACE` | First char must be letter                     |
| `VAILD_REGEX_SYSTEM_SYMBOL`               | System symbol chars                              |
| `VAILD_REGEX_SYSTEM_SYMBOL_NO_PERCENT`    | System symbol chars (no %)                       |
| `VAILD_REGEX_SYSTEM_SYMBOL_PPPOE`         | PPPoE symbol chars                               |
| `VAILD_NUMBER`                            | Digits only                                      |
| `VAILD_NUMBER_WITH_COMMA_AND_DASH`        | Number ranges (e.g., 1,2,5-10)                   |
| `VAILD_HEX`                               | Hex with 0x prefix                               |
| `VAILD_MAC`                               | MAC address                                      |
| `VAILD_REGEX_LEVEL_1`                     | Alphanumeric + dot/underscore/dash               |
| `VAILD_REGEX_RESERVED_CHAR_NOT_SPACE`     | Alphanumeric only                                |
| `VAILD_REGEX_DOMAIN_NAME`                 | Domain name                                      |
| `VAILD_REGEX_ASCII`                       | Printable ASCII                                  |
| `VALID_PURE_HEX`                          | Hex without 0x prefix                            |
| `VALID_EVEN`                              | Even length string                               |
| `VALID_NOT_CHAR_AND_DOT_DASH_IN_BEGIN_END`| No dot/dash at begin/end                         |
| `IPV6_ADDR_REGEX`                         | IPv6 address                                     |

### Pattern Usage Example

```typescript
import { Component, inject } from '@angular/core';
import { NonNullableFormBuilder, ReactiveFormsModule } from '@angular/forms';
import { OneValidators, VAILD_REGEX, VAILD_MAC } from '@one-ui/mxsecurity/shared/domain';

@Component({
  // ...
})
export class MyFormComponent {
  readonly #fb = inject(NonNullableFormBuilder);

  readonly form = this.#fb.group({
    name: ['', [OneValidators.required, OneValidators.maxLength(32), OneValidators.pattern(VAILD_REGEX)]],
    macAddress: ['', [OneValidators.required, OneValidators.pattern(VAILD_MAC)]]
  });
}
```

---

## Usage Examples

### Example 1: Login Form

```typescript
import { NonNullableFormBuilder } from '@angular/forms';
import { OneValidators } from '@one-ui/mxsecurity/shared/domain';

form = this.fb.group({
  username: ['', [OneValidators.required, OneValidators.rangeLength(4, 32, 'Username')]],
  password: ['', [OneValidators.required, OneValidators.rangeLength(4, 64, 'Password')]]
});
```

### Example 2: User Form with Password Confirmation

```typescript
import { OneValidators, VALID_REGEX_VIRGINIA_GUIDELINE_WITH_ANGLE } from '@one-ui/mxsecurity/shared/domain';

form = this.fb.group(
  {
    username: ['', [OneValidators.required]],
    password: ['', [
      OneValidators.required,
      OneValidators.minLength(8),
      OneValidators.pattern(VALID_REGEX_VIRGINIA_GUIDELINE_WITH_ANGLE)
    ]],
    confirmPassword: ['', [OneValidators.required]]
  },
  {
    validators: [OneValidators.matchFieldsValidator('password', 'confirmPassword')]
  }
);
```

### Example 3: Network Configuration Form

```typescript
form = this.fb.group({
  macAddress: [
    '',
    [
      OneValidators.required,
      OneValidators.pattern(/^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$/),
      OneValidators.checkHostMac() // Ensure it's not a multicast MAC
    ]
  ],
  description: ['', [OneValidators.checkSpaceCount(4)]] // Max 4 spaces
});
```

### Example 4: Table Entry Form (Unique Check)

```typescript
// Existing table data
existingUsers = [
  { name: 'admin', role: 'admin' },
  { name: 'user1', role: 'user' }
];

form = this.fb.group({
  name: ['', [OneValidators.required, OneValidators.duplicate(this.existingUsers, 'name')]],
  role: ['', [OneValidators.required]]
});
```

### Example 5: Numeric Range Validation

```typescript
// ❌ BAD: OneValidators.min and OneValidators.max DO NOT EXIST!
form = this.fb.group({
  keyId: [null, [OneValidators.required, OneValidators.min(1), OneValidators.max(65535)]]  // ❌ WRONG!
});

// ✅ GOOD: Use OneValidators.range(min, max) for numeric range validation
const KEY_ID_MIN = 1;
const KEY_ID_MAX = 65535;

form = this.fb.group({
  keyId: [null, [OneValidators.required, OneValidators.range(KEY_ID_MIN, KEY_ID_MAX)]]  // ✅ Correct
});
```

---

## Common Patterns from Old System → New System

| Old Pattern                                                                    | New Pattern                                                         |
| ------------------------------------------------------------------------------ | ------------------------------------------------------------------- |
| `Validators.required`                                                          | `OneValidators.required`                                            |
| `Validators.minLength(4)`                                                      | `OneValidators.minLength(4)`                                        |
| `Validators.min(1), Validators.max(100)`                                       | `OneValidators.range(1, 100)` ⚠️ **IMPORTANT**                      |
| `Validators.pattern(ValidatorPattern.VALID_REGEX_VIRGINIA_GUIDELINE)`          | `OneValidators.pattern(VALID_REGEX_VIRGINIA_GUIDELINE)`             |
| `Validators.pattern(ValidatorPattern.VALID_REGEX_VIRGINIA_GUIDELINE_WITH_ANGLE)` | `OneValidators.pattern(VALID_REGEX_VIRGINIA_GUIDELINE_WITH_ANGLE)` |
| `Validators.pattern(ValidatorPattern.VAILD_REGEX)`                             | `OneValidators.pattern(VAILD_REGEX)`                                |
| `Validators.pattern(/^[0-9a-zA-Z_@!#$%^&*()./ -]+$/)`                          | `OneValidators.pattern(VAILD_REGEX)`                                |
| `ValidatorFunction.checkHostMac()`                                             | `OneValidators.checkHostMac()`                                      |
| `ValidatorFunction.checkSpaceCount(4)`                                         | `OneValidators.checkSpaceCount(4)`                                  |
| `ValidatorFunction.requiredUniqueEntry(data, 'name')`                          | `OneValidators.duplicate(data, 'name')`                             |
| `ValidatorFunction.matchFieldsValidator('pwd', 'confirm')`                     | `OneValidators.matchFieldsValidator('pwd', 'confirm')`              |

> ⚠️ **IMPORTANT:** `OneValidators` does NOT have separate `min()` or `max()` validators. Always combine them into `OneValidators.range(min, max)` for numeric validation.

---

## ⚠️ CRITICAL: Error Display Patterns

### Which Validators Can Use `oneUiFormError` Directly?

| Validator | Built-in Message | Usage |
| --------- | ---------------- | ----- |
| `required` | `validators.required` | ✅ Use `oneUiFormError` directly |
| `minLength` | `validators.require_min_length` | ✅ Use `oneUiFormError` directly |
| `maxLength` | `validators.invalid_max_length` | ✅ Use `oneUiFormError` directly |
| `range` | `validators.invalid_range` | ✅ Use `oneUiFormError` directly |
| `rangeLength` | `validators.invalid_range` | ✅ Use `oneUiFormError` directly |
| `email` | `validators.invalid_email` | ✅ Use `oneUiFormError` directly |
| `pattern` | `validators.invalid` (too generic) | ❌ **MUST** use `@if/@else` |
| `duplicate` | `validators.duplicate` (may need specificity) | ❌ **MUST** use `@if/@else` |
| Custom validators | No built-in message | ❌ **MUST** use `@if/@else` |
| **All other validators** | Not in above 6 basic validators | ❌ **MUST** use `@if/@else` |

### Pattern 1: Simple Usage (Validators with Built-in Messages)

```html
<mat-form-field>
  <mat-label>{{ t('label') }}</mat-label>
  <input matInput formControlName="name" />
  <mat-error oneUiFormError="name"></mat-error>
</mat-form-field>
```

### Pattern 2: Custom Messages (All Other Validators)

```html
<mat-form-field>
  <mat-label>{{ t('label') }}</mat-label>
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

### ❌ Incorrect Pattern

```html
<!-- oneUiFormError directive cannot display pattern-specific error messages -->
<mat-form-field>
  <mat-label>{{ t('general.common_account.account') }}</mat-label>
  <input matInput formControlName="account" />
  <mat-error oneUiFormError="account"></mat-error>  <!-- ❌ Pattern error will not display correctly -->
</mat-form-field>
```

### ✅ Correct Pattern

```html
<!-- Use @if/@else to handle pattern errors -->
<mat-form-field>
  <mat-label>{{ t('general.common_account.account') }}</mat-label>
  <input matInput formControlName="account" />
  @if (form.controls.account.hasError('pattern')) {
    <mat-error>{{ t('validators.invalid_format_not_space') }}</mat-error>  <!-- ✅ Custom pattern error message -->
  } @else {
    <mat-error oneUiFormError="account"></mat-error>  <!-- ✅ Other errors handled by directive -->
  }
</mat-form-field>
```

### Common Pattern Error Messages

| Pattern Constant | Error Message Translation Key |
|------------------|------------------------------|
| `VAILD_REGEX_NOT_SPACE` | `validators.invalid_format_not_space` |
| `VAILD_REGEX_LEVEL_1` | `validators.invalid_regex_level_1` |
| `IPADDR_REGEX` | `validators.invalid_ip_address` |

### Complete Example

```html
<!-- Configuration Name with pattern validation -->
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

<!-- Account with pattern validation -->
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

<!-- IP Address with pattern validation -->
<mat-form-field>
  <mat-label>{{ t('general.common.server_ip_address') }}</mat-label>
  <input matInput maxlength="31" formControlName="ipAddress" />
  <mat-hint align="end">{{ form.controls.ipAddress.value.length }} / 31</mat-hint>
  @if (form.controls.ipAddress.hasError('pattern')) {
    <mat-error>{{ t('validators.invalid_ip_address') }}</mat-error>
  } @else {
    <mat-error oneUiFormError="ipAddress"></mat-error>
  }
</mat-form-field>
```

### Why is this necessary?

1. **`oneUiFormError` directive** is designed to handle built-in `OneValidators` error messages (e.g., `required`, `minLength`, `maxLength`)
2. **Pattern validation** error messages need to display different messages based on the specific pattern type, which cannot be automatically inferred by the directive
3. **Legacy code** uses the same `@if`/`@else` pattern, so migration must maintain consistency
