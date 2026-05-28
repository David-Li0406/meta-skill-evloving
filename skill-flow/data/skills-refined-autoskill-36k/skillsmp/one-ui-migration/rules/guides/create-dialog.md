# Guide: Creating a Dialog

## Overview

Create a form dialog for creating or editing data.

## Required Tools

| Tool | Purpose |
|------|---------|
| [dialog](../tools/ui/dialogs.md) | Dialog basics |
| [form-builder](../tools/form-builder.md) | Form creation |
| [one-validators](../tools/one-validators.md) | Form validation |
| [mx-components](../tools/mx-components.md) | mxLabel, mxButtonIsLoading |
| [transloco](../tools/transloco.md) | Translation |

---

## Steps

### 1. Define Dialog Data Type

```typescript
// feature.model.ts
export interface FeatureDialogData {
  mode: 'create' | 'edit';
  item?: Item;
}
```

### 2. Create Dialog Component

```typescript
// feature-dialog.component.ts
@Component({
  selector: 'one-ui-feature-dialog',
  imports: [
    MatDialogModule, MatButtonModule, MatFormFieldModule, MatInputModule,
    ReactiveFormsModule, TranslocoModule,
    MxLoadingButtonDirective, MxLabelDirective, OneUiFormErrorDirective
  ],
  templateUrl: './feature-dialog.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class FeatureDialogComponent {
  readonly #dialogRef = inject(MatDialogRef<FeatureDialogComponent>);
  readonly #store = inject(FeatureStore);
  readonly #fb = inject(NonNullableFormBuilder);
  readonly data = inject<FeatureDialogData>(MAT_DIALOG_DATA);

  readonly loading = this.#store.loading;
  readonly isEditMode = this.data.mode === 'edit';

  form = this.#fb.group({
    name: [this.data.item?.name ?? '', [OneValidators.required, OneValidators.maxLength(32)]],
    description: [this.data.item?.description ?? '', [OneValidators.maxLength(255)]]
  });

  onSubmit() {
    if (this.form.invalid) return;
    const value = this.form.getRawValue();

    if (this.isEditMode) {
      this.#store.updateItem({
        id: this.data.item!.id,
        data: value,
        next: () => this.#dialogRef.close({ success: true })
      });
    } else {
      this.#store.createItem({
        input: value,
        next: () => this.#dialogRef.close({ success: true })
      });
    }
  }
}
```

### 3. Create Dialog Template

```html
<!-- feature-dialog.component.html -->
<h2 *transloco="let t" mat-dialog-title>
  {{ isEditMode ? t('features.xxx.edit_title') : t('features.xxx.create_title') }}
</h2>

<mat-dialog-content *transloco="let t">
  <form [formGroup]="form" class="dialog-form">
    <mat-form-field>
      <mat-label mxLabel [mxLabelTooltip]="t('features.xxx.name_hint')">
        {{ t('general.common.name') }}
      </mat-label>
      <input matInput formControlName="name" />
      <mat-error oneUiFormError="name"></mat-error>
    </mat-form-field>

    <mat-form-field>
      <mat-label>{{ t('general.common.description') }}</mat-label>
      <textarea matInput formControlName="description" rows="3"></textarea>
      <mat-hint align="end">{{ form.value.description?.length || 0 }} / 255</mat-hint>
      <mat-error oneUiFormError="description"></mat-error>
    </mat-form-field>
  </form>
</mat-dialog-content>

<div *transloco="let t" mat-dialog-actions align="end">
  <button mat-button color="primary" [disabled]="loading()" mat-dialog-close>
    {{ t('general.button.cancel') }}
  </button>
  <button mat-flat-button color="primary"
    [disabled]="form.invalid || loading()"
    [mxButtonIsLoading]="loading()"
    (click)="onSubmit()">
    {{ t('general.button.submit') }}
  </button>
</div>
```

### 4. Open Dialog from Page

```typescript
// feature-page.component.ts
readonly #dialog = inject(MatDialog);
readonly #viewContainerRef = inject(ViewContainerRef);

openCreateDialog() {
  this.#dialog.open(FeatureDialogComponent, {
    ...mediumDialogConfig,
    viewContainerRef: this.#viewContainerRef,  // Required!
    data: { mode: 'create' }
  });
}

openEditDialog(item: Item) {
  this.#dialog.open(FeatureDialogComponent, {
    ...mediumDialogConfig,
    viewContainerRef: this.#viewContainerRef,  // Required!
    data: { mode: 'edit', item }
  });
}
```

---

## Checklist

- [ ] Dialog is in Features Layer (not UI Layer)
- [ ] Uses `NonNullableFormBuilder`
- [ ] Uses `OneValidators` (not Angular `Validators`)
- [ ] Uses `oneUiFormError` directive
- [ ] Submit button has `loading()` in `[disabled]`
- [ ] Only closes on API success (`next:` callback)
- [ ] Opens with `viewContainerRef`
