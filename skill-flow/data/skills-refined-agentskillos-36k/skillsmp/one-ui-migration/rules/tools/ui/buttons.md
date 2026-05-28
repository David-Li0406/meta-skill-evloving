# Buttons Guidelines

## Buttons (Material Buttons)

**Button Types in MXsecurity:**

- **`mat-button`**: Text button - use for secondary actions (Cancel, Close)
- **`mat-flat-button`**: ✅ **REQUIRED** - Use for primary/secondary actions in dialogs and forms
- **`mat-raised-button`**: ❌ **DO NOT USE** - deprecated in mxsecurity, use `mat-flat-button` instead
- **`mat-stroked-button`**: Outlined button - for tertiary actions

### Dialog Action Buttons Example

```html
<div mat-dialog-actions align="end">
  <!-- Secondary action: text button -->
  <button mat-button mat-dialog-close color="primary">{{ 'general.button.cancel' | transloco }}</button>

  <!-- Primary action: flat button ✅ -->
  <button mat-flat-button color="primary" (click)="submit()">{{ 'general.button.submit' | transloco }}</button>
</div>
```

### Migration Guide

Replace all `mat-raised-button` with `mat-flat-button`:

```html
<!-- ❌ OLD -->
<button mat-raised-button color="primary">Save</button>

<!-- ✅ NEW -->
<button mat-flat-button color="primary">Save</button>
```

---

## Loading States

Use the loading pattern from shared domain:

```typescript
@if (store.loading()) {
  <mat-progress-bar mode="indeterminate" />
}

@if (store.fetching()) {
  <mat-spinner />
}
```

---

## Page Form Apply Button Pattern

**CRITICAL**: Page-level form Apply buttons must use `mxButtonIsLoading` for loading state AND include `loading()` in the disabled condition.

### Required Import

```typescript
import { MxLoadingButtonDirective } from '@moxa/formoxa/mx-button';

@Component({
  imports: [
    // ...
    MxLoadingButtonDirective
  ]
})
```

### Template Pattern

```html
<!-- ✅ Correct: Both disabled and mxButtonIsLoading -->
<button
  mat-flat-button
  color="primary"
  type="submit"
  [disabled]="noPermission || loading()"
  [mxButtonIsLoading]="loading()"
>
  {{ t('general.button.apply') }}
</button>

<!-- ❌ Incorrect: Only mxButtonIsLoading without loading() in disabled -->
<button
  mat-flat-button
  color="primary"
  type="submit"
  [disabled]="noPermission"
  [mxButtonIsLoading]="loading()"
>
  {{ t('general.button.apply') }}
</button>

<!-- ❌ Incorrect: Only disabled without mxButtonIsLoading -->
<button
  mat-flat-button
  color="primary"
  type="submit"
  [disabled]="noPermission || loading()"
>
  {{ t('general.button.apply') }}
</button>
```

### Complete Page Example

```html
<div *transloco="let t" class="gl-page-content">
  <one-ui-breadcrumb />
  <mx-page-title [title]="t('features.xxx.page_title')" />

  <div class="content-wrapper">
    <form [formGroup]="form" (ngSubmit)="onApply()">
      <div class="form-column">
        <mat-checkbox color="primary" formControlName="enable">
          {{ t('features.xxx.enable_option') }}
        </mat-checkbox>
        <div>
          <button
            mat-flat-button
            color="primary"
            type="submit"
            [disabled]="noPermission || loading()"
            [mxButtonIsLoading]="loading()"
          >
            {{ t('general.button.apply') }}
          </button>
        </div>
      </div>
    </form>
  </div>
</div>
```

**Key Points:**

- **ALWAYS use both** `[disabled]` and `[mxButtonIsLoading]` together
- `[disabled]="noPermission || loading()"` - prevents interaction during loading AND when user lacks permission
- `[mxButtonIsLoading]="loading()"` - shows visual loading spinner on the button
- Import `MxLoadingButtonDirective` from `@moxa/formoxa/mx-button`
- The `mxButtonIsLoading` directive does NOT automatically disable the button - you must include `loading()` in the disabled condition

---

## Table Toolbar Buttons

**Refresh Button Pattern:**

> **Note:** Only add refresh button if the old code has one. Not all tables need refresh buttons.

Toolbar action buttons should be placed in `#rightToolbarTemplate`:

```html
<one-ui-common-table *transloco="let t" [data]="tableData()" [columns]="columns()">
  <!-- Right Toolbar: Action buttons -->
  <ng-template #rightToolbarTemplate>
    <button data-testid="test-xxx-table-btn-xxx" mat-button (click)="refresh.emit()">
      <mat-icon data-testid="test-xxx-table-icon-xxx" svgIcon="icon:refresh"></mat-icon>
      {{ t('general.tooltip.refresh') }}
    </button>
  </ng-template>
</one-ui-common-table>
```

**Key Points:**

- Use `#rightToolbarTemplate` for action buttons (not `#leftToolbarTemplate`)
- Use `mat-button` (text button) for toolbar actions
- Use `svgIcon="icon:refresh"` for icon (not `<mat-icon>refresh</mat-icon>`)
- Include both icon and text label for accessibility
- Add `data-testid` attributes for testing
