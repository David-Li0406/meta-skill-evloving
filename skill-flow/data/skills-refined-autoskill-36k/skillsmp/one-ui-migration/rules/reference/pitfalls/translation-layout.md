# Common Pitfalls: Translation & Layout

## ⚠️ Translation Keys - MUST Match Source Exactly

**CRITICAL**: Translation keys must be **exactly the same** as the old system. Do NOT create new translation keys or modify existing ones.

### Why This Matters

- Translation files are shared across the application
- Existing translation keys already have translations in multiple languages
- Creating new keys means missing translations and broken i18n

### ❌ **WRONG - Creating New Translation Keys**

```typescript
// ❌ WRONG - Inventing new translation keys
header: this.#transloco.translate('features.cert_signing_request.csr_table.name')
header: this.#transloco.translate('features.cert_signing_request.csr_table.subject')

// ❌ WRONG - Modifying key structure
{{ t('features.cert_signing_request.dialog.create_title') }}
{{ t('features.cert_signing_request.form.country') }}
```

### ✅ **CORRECT - Use Exact Keys from Source**

```typescript
// ✅ CORRECT - Copy exact keys from old system
header: this.#transloco.translate('general.common.name')
header: this.#transloco.translate('features.trusted_ca_cert.subject')

// ✅ CORRECT - Match source exactly
{{ t('features.cert_signing_request.title_create_csr_dialog_title') }}
{{ t('features.cert_signing_request.country_name') }}
```

### How to Find Correct Translation Keys

1. **Read the source HTML template** in the old project
2. **Copy the exact translation key** including the full path
3. **Do NOT abbreviate or restructure** the key path

Example - Check source file:
```html
<!-- Source: /Users/jayden/f2e-networking-jayden/apps/mxsecurity-web/src/app/pages/xxx/xxx.component.html -->
{{ 'features.cert_signing_request.title_create_csr_dialog_title' | translate }}
{{ 'general.common.name' | translate }}
{{ 'features.trusted_ca_cert.subject' | translate }}
```

Use these **exact same keys** in the migrated code:
```html
<!-- Target: New Angular 20 component -->
{{ t('features.cert_signing_request.title_create_csr_dialog_title') }}
{{ t('general.common.name') }}
{{ t('features.trusted_ca_cert.subject') }}
```

### Common Translation Key Patterns in MXsecurity

| Type | Pattern | Example |
|------|---------|---------|
| Page title | `features.{feature}.page_title` | `features.cert_signing_request.page_title` |
| Dialog title | `features.{feature}.title_{action}_{type}_dialog_title` | `features.cert_signing_request.title_create_csr_dialog_title` |
| Form field | `features.{feature}.{field_name}` | `features.cert_signing_request.country_name` |
| Common | `general.common.{name}` | `general.common.name` |
| Button | `general.button.{action}` | `general.button.create` |
| Tooltip | `general.tooltip.{action}` | `general.tooltip.export` |

---

## ⚠️ Form Layout - MUST Match Source Exactly

**CRITICAL**: Form field layouts (row groupings) must match the source exactly. Do NOT change which fields appear on the same row.

### Why This Matters

- UI consistency with the old system
- Users expect the same visual layout
- Field groupings often have logical meaning

### ❌ **WRONG - Changing Form Layout**

```html
<!-- Source has org + orgUnit on same row -->
<div fxLayout="row">
  <mat-form-field>organization_name</mat-form-field>
  <mat-form-field>organizational_unit_name</mat-form-field>
</div>

<!-- ❌ WRONG - Migrated with each field on separate row -->
<mat-form-field>organization_name</mat-form-field>
<mat-form-field>organizational_unit_name</mat-form-field>
```

### ✅ **CORRECT - Preserve Row Groupings**

```html
<!-- ✅ CORRECT - Use .form-row to maintain same layout -->
<div class="form-row">
  <mat-form-field>organization_name</mat-form-field>
  <mat-form-field>organizational_unit_name</mat-form-field>
</div>
```

### How to Preserve Form Layout

1. **Analyze source template** - Look for `fxLayout="row"` or similar row groupings
2. **Use `.form-row` class** - Available in `libs/mxsecurity/shared/styles/_form.scss`
3. **Group fields exactly as source** - Same fields on same row

---

## ⚠️ Page Component Styling - NO Padding

**CRITICAL**: Do NOT add `padding: 24px` to page components. The layout padding is handled by the shell/app layout.

### ❌ **WRONG - Adding Padding to Page Component**

```scss
// ❌ WRONG - page-name.component.scss
:host {
  display: block;
  padding: 24px;  // ❌ NO! Don't add padding
}
```

### ✅ **CORRECT - No Padding in Page Component**

```scss
// ✅ CORRECT - page-name.component.scss
:host {
  display: block;
}
```

---

## ⚠️ Page Layout - MUST Use gl-page-content

**CRITICAL**: All page components **MUST** use `class="gl-page-content"` on the root element. Without this class, **tables and content will NOT display correctly!**

### ❌ **WRONG - Using ng-container (Tables won't display!)**

```html
<!-- ❌ WRONG - ng-container doesn't create DOM element, so styles don't apply -->
<ng-container *transloco="let t">
  <one-ui-breadcrumb />
  <mx-page-title>{{ t('features.xxx.page_title') }}</mx-page-title>
  <div class="content-wrapper">
    <one-ui-my-table [tableData]="tableData()" />  <!-- ❌ Won't display! -->
  </div>
</ng-container>
```

### ✅ **CORRECT - Use div with gl-page-content class**

```html
<!-- ✅ CORRECT - div with gl-page-content class -->
<div *transloco="let t" class="gl-page-content">
  <one-ui-breadcrumb />
  <mx-page-title [title]="t('features.xxx.page_title')" />
  <div class="content-wrapper">
    <one-ui-my-table [tableData]="tableData()" />  <!-- ✅ Displays correctly -->
  </div>
</div>
```

### Why This Happens

`<ng-container>` is a logical grouping element that doesn't create a DOM element. The `gl-page-content` styles require a real DOM element to apply properly. Without it, the page layout CSS doesn't work and content (especially tables) won't be visible.

### Also Note

- Use `<mx-page-title [title]="t('...')" />` with input binding
- NOT `<mx-page-title>{{ t('...') }}</mx-page-title>` with content projection

---

## ⚠️ Table Toolbar Button Order

**CRITICAL**: Table toolbar buttons must follow a specific order: **Refresh → Create/Delete** (if applicable)

### Button Order Pattern

```html
<ng-template #rightToolbarTemplate>
  <!-- 1. Refresh button (only if old code has it, comes first) -->
  <button mat-button (click)="refresh.emit()">
    <mat-icon svgIcon="icon:refresh"></mat-icon>
    {{ t('general.tooltip.refresh') }}
  </button>

  <!-- 2. Create button (shown when nothing selected) -->
  @if (selection.length === 0) {
    <button mat-stroked-button (click)="add.emit()">
      {{ t('general.button.create') }}
    </button>
  }

  <!-- 3. Delete button (shown when items selected) -->
  @if (selection.length >= 1) {
    <button mat-stroked-button (click)="onDelete()">
      {{ t('general.button.delete') }}
    </button>
  }
</ng-template>
```

### Button Visibility Rules

| Button | Visibility | Position |
|--------|------------|----------|
| Refresh | Only if old code has it | First |
| Create | When `selection.length === 0` | After Refresh |
| Delete | When `selection.length >= 1` | After Refresh |
