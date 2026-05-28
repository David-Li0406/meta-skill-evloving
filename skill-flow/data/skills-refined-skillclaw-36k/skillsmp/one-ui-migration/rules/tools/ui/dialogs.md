# Dialog Components Guidelines

## Dialog Configuration

Use the shared dialog config instead of custom CSS for dialog sizing:

**Import from shared domain:**

```typescript
import { smallDialogConfig, mediumDialogConfig, largeDialogConfig } from '@one-ui/mxsecurity/shared/domain';
```

**Available Configs:**

| Config | Width | Use Case |
| ------ | ----- | -------- |
| `smallDialogConfig` | 400px | Confirmation dialogs, simple alerts |
| `mediumDialogConfig` | 560px | Standard forms, settings dialogs |
| `largeDialogConfig` | 720px | Complex forms, multi-step dialogs |
| `extraLargeDialogConfig` | 960px | Large data tables, wizard dialogs |

---

## Opening a Dialog

```typescript
// ✅ Correct: Use shared config with viewContainerRef
const dialogRef = this.#dialog.open(MyDialogComponent, {
  ...smallDialogConfig,
  viewContainerRef: this.#viewContainerRef,  // REQUIRED when dialog uses store
  data: { ... }
});

// ❌ Incorrect: Don't use panelClass for sizing
const dialogRef = this.#dialog.open(MyDialogComponent, {
  panelClass: 'mx-dialog-sm',  // Don't use this
  data: { ... }
});
```

---

## CRITICAL: viewContainerRef is Required for Store Access

When a dialog component injects the store (e.g., for loading state or API calls), you MUST set `viewContainerRef` when opening the dialog. This ensures the dialog uses the same injector as the parent component and can access the provided store.

```typescript
// In page component
readonly #viewContainerRef = inject(ViewContainerRef);

openDialog() {
  this.#dialog.open(MyDialogComponent, {
    ...mediumDialogConfig,
    viewContainerRef: this.#viewContainerRef,  // Required for store access
    data: dialogData
  });
}
```

---

## Don't Add Custom Width in SCSS

```scss
// ❌ Incorrect: Don't add custom width in dialog SCSS
mat-dialog-content {
  min-width: 300px;
}

// ✅ Correct: Use shared dialog config instead
// The config already handles width and common settings:
// - autoFocus: false
// - disableClose: true
```

---

## Dialog Component Structure

Dialogs should be in the `features/` layer:

```typescript
@Component({
  selector: 'one-ui-create-item-dialog',
  standalone: true,
  imports: [MatDialogModule, MyFormComponent],
  template: `
    <h2 mat-dialog-title>{{ 'create.title' | transloco }}</h2>
    <mat-dialog-content>
      <one-ui-my-form (save)="onSave($event)" />
    </mat-dialog-content>
    <mat-dialog-actions align="end">
      <button mat-button mat-dialog-close>{{ 'general.button.cancel' | transloco }}</button>
    </mat-dialog-actions>
  `
})
export class CreateItemDialogComponent {
  private dialogRef = inject(MatDialogRef<CreateItemDialogComponent>);

  onSave(data: MyData) {
    this.dialogRef.close(data);
  }
}
```

---

## Dialog Loading State Pattern

**CRITICAL**: Dialogs that perform API calls must show loading state and close only after the API completes successfully.

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

### Dialog Component Pattern

Dialogs should inject the store directly and call API methods within the dialog:

```typescript
@Component({
  selector: 'one-ui-my-dialog',
  standalone: true,
  imports: [MatButtonModule, MatDialogModule, MxLoadingButtonDirective, TranslocoModule],
  templateUrl: './my-dialog.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class MyDialogComponent {
  readonly #dialogRef = inject(MatDialogRef<MyDialogComponent>);
  readonly #store = inject(MyStore);
  readonly dialogData = inject<MyDialogData>(MAT_DIALOG_DATA);

  /** Use store's loading signal for button state */
  readonly loading = this.#store.loading;

  onSubmit() {
    // Call store mutation method with next callback for dialog close
    this.#store.createEntry(() => ({
      input: this.formData,
      next: () => {
        this.#store.loadPageData(); // Refresh data
        this.#dialogRef.close(); // Close dialog on success
      }
    }));
  }
}
```

### Template Pattern

```html
<div mat-dialog-actions align="end">
  <!-- Cancel button: use mat-dialog-close directive, no onCancel() needed -->
  <button mat-button color="primary" [disabled]="loading()" mat-dialog-close>
    {{ t('general.button.cancel') }}
  </button>

  <!-- Submit button: disabled when invalid or loading, shows spinner when loading -->
  <button
    mat-flat-button
    color="primary"
    [disabled]="form.invalid || loading()"
    [mxButtonIsLoading]="loading()"
    (click)="onSubmit()"
  >
    {{ t('general.button.submit') }}
  </button>
</div>
```

### Delete Dialog Pattern

```html
<div mat-dialog-actions align="end">
  <button mat-button color="primary" [disabled]="loading()" mat-dialog-close>
    {{ t('general.button.cancel') }}
  </button>
  <button
    mat-flat-button
    color="warn"
    [disabled]="loading()"
    [mxButtonIsLoading]="loading()"
    (click)="onDelete()"
  >
    {{ t('general.button.delete') }}
  </button>
</div>
```

---

## Page Component Opening Dialog

When opening a dialog that uses the store, you MUST set `viewContainerRef`:

```typescript
// Page component
readonly #dialog = inject(MatDialog);
readonly #viewContainerRef = inject(ViewContainerRef);

openSettingDialog() {
  this.#dialog.open(SettingDialogComponent, {
    ...mediumDialogConfig,
    viewContainerRef: this.#viewContainerRef,  // Required for store access
    data: dialogData
  });
}
```

---

## ConfirmDialogComponent Return Type

**CRITICAL**: `ConfirmDialogComponent` returns `boolean` directly, NOT an object like `{ confirm: boolean }`.

### ❌ Wrong - Incorrect return type

```typescript
const dialogRef = this.#dialog.open<ConfirmDialogComponent, ConfirmDialogData, { confirm: boolean }>(
  ConfirmDialogComponent,
  { ...mediumDialogConfig, data: { title: '...', desc: '...' } }
);

dialogRef.afterClosed().subscribe((result) => {
  if (result?.confirm) {  // ❌ Wrong! result is boolean, not { confirm: boolean }
    this.doSomething();
  }
});
```

### ✅ Correct - Boolean return type

```typescript
const dialogRef = this.#dialog.open<ConfirmDialogComponent, ConfirmDialogData, boolean>(
  ConfirmDialogComponent,
  {
    ...mediumDialogConfig,
    viewContainerRef: this.#viewContainerRef,
    data: {
      title: this.#transloco.translate('features.xxx.confirm_title'),
      desc: this.#transloco.translate('features.xxx.confirm_desc')
    }
  }
);

dialogRef.afterClosed().subscribe((result) => {
  if (result) {  // ✅ Correct! result is boolean (true/false)
    this.doSomething();
  }
});
```

### ConfirmDialogComponent Behavior

- Returns `true` when user clicks confirm/submit button
- Returns `false` or `undefined` when user clicks cancel or closes dialog
- Always use `if (result)` to check for confirmation

---

## Key Points Summary

- Import `MxLoadingButtonDirective` from `@moxa/formoxa/mx-button`
- Use store's `loading` signal: `readonly loading = this.#store.loading`
- Use `[mxButtonIsLoading]="loading()"` on submit/action buttons
- Use `[disabled]="form.invalid || loading()"` for form dialogs
- Use `[disabled]="loading()"` for confirmation dialogs (both cancel and action buttons)
- **Use `mat-dialog-close` directive for cancel button** - no `onCancel()` method needed
- Call API via store mutation method inside the dialog
- Close dialog with `this.#dialogRef.close()` in the `next` callback after API success
- Refresh data with `this.#store.loadPageData()` before closing
- **CRITICAL**: Set `viewContainerRef: this.#viewContainerRef` when opening the dialog
