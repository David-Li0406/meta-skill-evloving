# Forms Guidelines

## Form Row Usage (form-row)

**IMPORTANT**: Only use `<div class="form-row">` when there are **multiple elements** in the same row. If there's only one element, don't wrap it.

### ✅ Correct - Multiple elements in one row

```html
<div class="form-row">
  <mat-form-field>
    <mat-label>{{ t('features.radius.server_address') }}</mat-label>
    <input matInput formControlName="serverAddress" />
  </mat-form-field>

  <mat-form-field>
    <mat-label>{{ t('general.common_port.port') }}</mat-label>
    <input matInput type="number" formControlName="port" />
  </mat-form-field>
</div>
```

### ✅ Correct - Single element, no wrapper needed

```html
<mat-form-field>
  <mat-label>{{ t('features.radius.share_key') }}</mat-label>
  <mx-password-input formControlName="shareKey"></mx-password-input>
</mat-form-field>

<button mat-flat-button color="primary" type="submit">
  {{ t('general.button.apply') }}
</button>
```

### ❌ Wrong - Unnecessary wrapper for single element

```html
<div class="form-row">
  <mat-form-field>
    <mat-label>{{ t('features.radius.share_key') }}</mat-label>
    <mx-password-input formControlName="shareKey"></mx-password-input>
  </mat-form-field>
</div>

<div class="form-row">
  <button mat-flat-button color="primary" type="submit">
    {{ t('general.button.apply') }}
  </button>
</div>
```

---

## Form Submit Button Disabled State

**CRITICAL**: Submit buttons must be disabled when the form is invalid.

```html
<!-- ✅ Correct: Disable button when form is invalid -->
<div mat-dialog-actions align="end">
  <button mat-button color="primary" mat-dialog-close>
    {{ t('general.button.cancel') }}
  </button>
  <button mat-flat-button color="primary" [disabled]="form.invalid" (click)="onSubmit()">
    {{ t('general.button.submit') }}
  </button>
</div>

<!-- ❌ Incorrect: No disabled state -->
<button mat-flat-button color="primary" (click)="onSubmit()">
  {{ t('general.button.submit') }}
</button>
```

**Key Points:**

- Use `[disabled]="form.invalid"` on submit buttons
- This provides immediate visual feedback to users
- Prevents submission of invalid forms
- Works with both form-level and control-level validation

---

## Form Label Patterns (mxLabel, mxLabelOptional, mxLabelTooltip)

See `rules/tools/forms/patterns.md` → "Form Label Patterns" section.

---

## Long Error Messages (mat-long-error)

See `forms/error-handling.md` → "Long Error Messages (mat-long-error)" section.
