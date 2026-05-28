# MX Components

## What is this?

Moxa Formoxa UI components and directives for forms, status display, buttons, etc.

## When to use

Creating forms, displaying status, loading buttons, etc.

---

## Mat-Icon (CRITICAL)

**Must use `svgIcon` attribute, NOT text content.**

```typescript
import { MatIconModule } from '@angular/material/icon';
```

| ❌ Wrong | ✅ Correct |
|----------|-----------|
| `<mat-icon>refresh</mat-icon>` | `<mat-icon svgIcon="icon:refresh"></mat-icon>` |
| `<mat-icon>edit</mat-icon>` | `<mat-icon svgIcon="icon:edit"></mat-icon>` |
| `<mat-icon>delete</mat-icon>` | `<mat-icon svgIcon="icon:delete"></mat-icon>` |

### Common Icons

| Icon | svgIcon Value | Use Case |
|------|---------------|----------|
| Refresh | `icon:refresh` | Table refresh button |
| Edit | `icon:edit` | Edit row |
| Delete | `icon:delete` | Delete action |
| Add | `icon:add` | Create new |
| Search | `icon:search` | Search field |
| Info | `icon:info` | Information tooltip |
| Warning | `icon:warning` | Warning status |
| Error | `icon:error` | Error status |
| Check | `icon:task_alt` | Success/enabled status |
| Hide | `icon:hide_source` | Disabled status |
| Visibility | `icon:visibility` | Show password |
| Visibility Off | `icon:visibility_off` | Hide password |

```html
<!-- ❌ Wrong: Text icon -->
<button mat-button>
  <mat-icon>refresh</mat-icon>
  Refresh
</button>

<!-- ✅ Correct: svgIcon -->
<button mat-button (click)="refresh.emit()">
  <mat-icon svgIcon="icon:refresh"></mat-icon>
  {{ t('general.tooltip.refresh') }}
</button>
```

---

## MxStatus

Displays enabled/disabled and other statuses.

```typescript
import { MxStatusComponent } from '@moxa/formoxa/mx-status';
```

```html
@if (row.enabled) {
  <mx-status statusType="success" statusIcon="icon:task_alt" [statusText]="t('general.common.enable')" />
} @else {
  <mx-status statusType="neutral" statusIcon="icon:hide_source" [statusText]="t('general.common.disable')" />
}
```

| statusType | statusIcon | Use Case |
|------------|------------|----------|
| `success` | `icon:task_alt` | Enabled, connected, complete |
| `neutral` | `icon:hide_source` | Disabled, disconnected |
| `warning` | `icon:warning` | Warning |
| `error` | `icon:error` | Error |

---

## mxLabel

Form field label with tooltip and optional indicator support.

```typescript
import { MxLabelDirective } from '@moxa/formoxa/mx-label';
```

```html
<!-- Standard field with tooltip -->
<mat-form-field>
  <mat-label mxLabel [mxLabelTooltip]="t('field.hint')">{{ t('field.label') }}</mat-label>
  <input matInput formControlName="fieldName" />
</mat-form-field>

<!-- Optional field -->
<mat-form-field>
  <mat-label mxLabel mxLabelOptional [mxLabelOptionalText]="t('general.common.optional')">
    {{ t('field.label') }}
  </mat-label>
  <input matInput formControlName="optionalField" />
</mat-form-field>
```

| Directive | Use |
|-----------|-----|
| `mxLabel` | Base directive (required) |
| `mxLabelOptional` | Shows "Optional" |
| `[mxLabelOptionalText]` | Custom optional text |
| `[mxLabelTooltip]` | Info tooltip |

---

## mxButtonIsLoading

Button loading state (shows spinner).

```typescript
import { MxLoadingButtonDirective } from '@moxa/formoxa/mx-button';
```

```html
<button mat-flat-button color="primary"
  [mxButtonIsLoading]="loading()"
  [disabled]="form.invalid || loading()"
  (click)="onSubmit()">
  {{ t('general.button.submit') }}
</button>
```

⚠️ **Note**: `[mxButtonIsLoading]` only shows spinner, **does NOT auto-disable**! You must manually add `loading()` to `[disabled]`.

---

## Form Validation Directives

> 📖 For validator definitions, see [one-validators.md](./one-validators.md)

### Quick Reference

| Directive | Purpose | Example |
|-----------|---------|---------|
| `oneUiFormError` | Auto-display validation errors | `<mat-error oneUiFormError="name">` |
| `oneUiFormHint` | Auto-display hints (char count / range) | `<mat-hint oneUiFormHint="name">` |
| `oneUiNumberOnly` | Restrict input to numbers only | `<input type="text" oneUiNumberOnly>` |

### oneUiFormError

Automatically displays form validation error messages. Reads i18n error messages from Enhanced Validators (`validatorFnWithMessage` / `validatorWithMessage`).

```typescript
import { OneUiFormErrorDirective } from '@one-ui/shared/ui/form';
```

```html
<mat-form-field>
  <mat-label>{{ t('field.label') }}</mat-label>
  <input matInput formControlName="fieldName" />
  <mat-error oneUiFormError="fieldName"></mat-error>
</mat-form-field>
```

**How It Works:**
1. Directive reads the `__renderErrorMessage__` property from the validator
2. If validator was created with `validatorFnWithMessage`, error message is automatically resolved
3. Supports both i18n keys and dynamic message functions

### oneUiFormHint

Automatically displays hints from Enhanced Validators. Supports character count, range hints, and custom hint messages.

```typescript
import { OneUiFormHintDirective } from '@one-ui/shared/ui/form';
```

```html
<mat-form-field>
  <mat-label>{{ t('field.port') }}</mat-label>
  <input matInput type="text" oneUiNumberOnly formControlName="port" />
  <mat-hint oneUiFormHint="port"></mat-hint>  <!-- Shows "1 ~ 65535" -->
  <mat-error oneUiFormError="port"></mat-error>
</mat-form-field>
```

**Multiple Hints (hintIndex):**

When a form control has multiple validators with hints, use `[hintIndex]` to select which hint to display:

```html
<!-- Display first hint (default, hintIndex=0) -->
<mat-hint oneUiFormHint="password"></mat-hint>

<!-- Display second hint (hintIndex=1) -->
<mat-hint oneUiFormHint="password" [hintIndex]="1"></mat-hint>
```

### oneUiNumberOnly

Restricts input to numbers only, replacing native HTML `type="number"`.

```typescript
import { NumberOnlyDirective } from '@one-ui/mxsecurity/shared/domain';
```

```html
<!-- ✅ Correct: Use type="text" with oneUiNumberOnly -->
<input matInput type="text" formControlName="port" oneUiNumberOnly />

<!-- ❌ Wrong: Don't use type="number" -->
<input matInput type="number" formControlName="port" />
```

| `type="number"` Problems | `oneUiNumberOnly` Solution |
|--------------------------|---------------------------|
| Scroll wheel accidentally changes value | No such issue |
| Allows `e`, `+`, `-` characters | Only allows 0-9 |
| Scientific notation input (e.g., `1e5`) | Not allowed |
| Inconsistent behavior across browsers | Unified behavior |

### Complete Form Example

```typescript
// ===== Component =====
import { OneValidators, validatorFnWithMessage } from '@one-ui/shared/domain';
import { OneUiFormErrorDirective, OneUiFormHintDirective } from '@one-ui/shared/ui/form';
import { NumberOnlyDirective } from '@one-ui/mxsecurity/shared/domain';

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
    <mat-label mxLabel [mxLabelTooltip]="t('field.name.hint')">{{ t('field.name') }}</mat-label>
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
    <mat-label mxLabel mxLabelOptional [mxLabelOptionalText]="t('general.common.optional')">
      {{ t('field.description') }}
    </mat-label>
    <textarea matInput formControlName="description"></textarea>
    <mat-hint oneUiFormHint="description"></mat-hint>  <!-- Shows "0 / 255" -->
    <mat-error oneUiFormError="description"></mat-error>
  </mat-form-field>

  <button mat-flat-button color="primary"
    [mxButtonIsLoading]="loading()"
    [disabled]="form.invalid || loading()">
    {{ t('general.button.submit') }}
  </button>
</form>
```

### Common Mistakes

| ❌ Wrong | ✅ Correct |
|----------|-----------|
| `{{ form.get('name')?.value?.length }} / 32` | `<mat-hint oneUiFormHint="name">` |
| `*ngIf="form.get('x')?.hasError('required')"` | `<mat-error oneUiFormError="x">` |
| `[maxlength]="32"` + manual char count | `OneValidators.maxLength(32)` + `oneUiFormHint` |
| Hardcoded error messages | i18n keys in `validatorFnWithMessage` |
| `<input type="number">` | `<input type="text" oneUiNumberOnly>` |
| `min="1" max="65535"` HTML attributes | `OneValidators.range(1, 65535)` |

### Form Directives Import

```typescript
import { OneUiFormErrorDirective, OneUiFormHintDirective } from '@one-ui/shared/ui/form';
import { NumberOnlyDirective } from '@one-ui/mxsecurity/shared/domain';

@Component({
  imports: [
    // ... other imports
    OneUiFormErrorDirective,
    OneUiFormHintDirective,
    NumberOnlyDirective
  ]
})
```

---

## MxFileUploader

File upload component.

```typescript
import { MxFileUploaderComponent } from '@moxa/formoxa/mx-file-uploader';
```

```html
<mat-form-field>
  <mat-label>{{ t('general.common.select_file') }}</mat-label>
  <mx-file-uploader
    formControlName="fileSelection"
    (onUpload)="onLocalFileSelected($event)"
  ></mx-file-uploader>
  <mat-error oneUiFormError="fileSelection"></mat-error>
</mat-form-field>
```

---

## MxPasswordVisibility

Password field visibility toggle component.

```typescript
import { MxPasswordVisibilityComponent } from '@moxa/formoxa/mx-password-visibility';
```

```html
<mat-form-field>
  <mat-label mxLabel>{{ t('general.common.password') }}</mat-label>
  <input matInput [type]="passwordVisible ? 'text' : 'password'" formControlName="password" />
  <mx-password-visibility matSuffix [(visible)]="passwordVisible" />
  <mat-error oneUiFormError="password"></mat-error>
</mat-form-field>
```

```typescript
// In component
passwordVisible = false;
```

---

## mxAutoTooltip

Auto-detects text overflow and shows tooltip only when text is truncated.

```typescript
import { MxAutoTooltipDirective } from '@moxa/formoxa/mx-auto-tooltip';
import { MatTooltipModule } from '@angular/material/tooltip';
```

**Must use with `gl-ellipsis-text` class:**

```html
<td mat-cell *matCellDef="let row">
  <span class="gl-ellipsis-text" mxAutoTooltip [matTooltip]="row.description">
    {{ row.description }}
  </span>
</td>
```

```scss
// Set column width constraints
.mat-column-description {
  min-width: 300px;
  max-width: 300px;
}
```

| Class/Directive | Purpose |
|-----------------|---------|
| `gl-ellipsis-text` | CSS class for text truncation with ellipsis |
| `mxAutoTooltip` | Only shows tooltip when text overflows |
| `[matTooltip]` | The full text to display in tooltip |

---

## Form Row Layout

Use `.form-row` class to group multiple fields on the same row.

```html
<!-- ❌ Wrong: Fields on separate rows when Legacy has them on same row -->
<mat-form-field>
  <mat-label>{{ t('organization_name') }}</mat-label>
  <input matInput formControlName="organizationName" />
</mat-form-field>
<mat-form-field>
  <mat-label>{{ t('organizational_unit') }}</mat-label>
  <input matInput formControlName="organizationalUnit" />
</mat-form-field>

<!-- ✅ Correct: Keep same row grouping as Legacy -->
<div class="form-row">
  <mat-form-field>
    <mat-label>{{ t('organization_name') }}</mat-label>
    <input matInput formControlName="organizationName" />
  </mat-form-field>
  <mat-form-field>
    <mat-label>{{ t('organizational_unit') }}</mat-label>
    <input matInput formControlName="organizationalUnit" />
  </mat-form-field>
</div>
```

⚠️ **Migration Rule**: Analyze Legacy source for `fxLayout="row"` patterns and replicate with `.form-row` class.

---

## MxTabGroup

Tab component directive.

```typescript
import { MxTabGroupDirective } from '@moxa/formoxa/mx-tabs';
```

```html
<mat-tab-group mxTabGroup animationDuration="0ms" [mat-stretch-tabs]="false">
  <mat-tab [label]="t('tab.general')">...</mat-tab>
  <mat-tab [label]="t('tab.advanced')">...</mat-tab>
</mat-tab-group>
```

---

## Common Import List

```typescript
// Forms
import { ReactiveFormsModule, NonNullableFormBuilder } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';

// MX Components
import { MxLabelDirective } from '@moxa/formoxa/mx-label';
import { MxLoadingButtonDirective } from '@moxa/formoxa/mx-button';
import { MxStatusComponent } from '@moxa/formoxa/mx-status';

// Form Validation & Hints
import { OneUiFormErrorDirective, OneUiFormHintDirective } from '@one-ui/shared/ui/form';
import { OneValidators, validatorFnWithMessage, validatorWithMessage } from '@one-ui/shared/domain';

// Number Input
import { NumberOnlyDirective } from '@one-ui/mxsecurity/shared/domain';
```

---

## Related Tools

- [form-builder.md](./form-builder.md) - Form creation
- [one-validators.md](./one-validators.md) - Form validation
- [dialogs.md](./ui/dialogs.md) - Forms in dialogs
