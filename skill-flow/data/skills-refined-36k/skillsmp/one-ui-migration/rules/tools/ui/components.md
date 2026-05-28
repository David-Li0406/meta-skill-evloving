# UI Components Guidelines

## File Upload Component (MxFileUploaderComponent)

**CRITICAL: Use `MxFileUploaderComponent` instead of manual file input**

When a form needs a file upload field, use `MxFileUploaderComponent` from `@moxa/formoxa/mx-file-uploader` instead of creating a manual `<input type="file">` with a folder icon button.

### ❌ Old Pattern (Manual File Input)

```html
<mat-form-field class="suffix-form-field">
  <mat-label>{{ t('general.common.select_file') }}</mat-label>
  <input
    matInput
    formControlName="fileSelection"
    readonly
    (click)="onFileInputClick()"
    (keydown)="$event.preventDefault()"
  />
  <button mat-icon-button matSuffix type="button" (click)="onFileInputClick()">
    <mat-icon>folder_open</mat-icon>
  </button>
  <mat-error oneUiFormError="fileSelection"></mat-error>
</mat-form-field>
<input
  #fileInput
  class="hidden-file-input"
  type="file"
  (change)="onLocalFileSelected($event)"
/>
```

```typescript
// Component code for manual approach
readonly fileInput = viewChild<ElementRef<HTMLInputElement>>('fileInput');

onFileInputClick(): void {
  this.fileInput()?.nativeElement.click();
}

onLocalFileSelected(event: Event): void {
  const input = event.target as HTMLInputElement;
  if (input.files && input.files.length > 0) {
    const file = input.files[0];
    // handle file...
  }
}
```

### ✅ New Pattern (MxFileUploaderComponent)

```html
<mat-form-field>
  <mat-label>{{ t('general.common.select_file') }}</mat-label>
  <mx-file-uploader
    data-testid="test-xxx-input-file"
    formControlName="fileSelection"
    (onUpload)="onLocalFileSelected($event)"
  ></mx-file-uploader>
  <mat-error oneUiFormError="fileSelection"></mat-error>
</mat-form-field>
```

```typescript
// Component code - much simpler!
onLocalFileSelected(file: File | null): void {
  if (file) {
    // handle file...
  }
}
```

### Required Import

```typescript
import { MxFileUploaderComponent } from '@moxa/formoxa/mx-file-uploader';

@Component({
  imports: [
    // ...
    MxFileUploaderComponent
  ]
})
```

### Key Points

- Use `MxFileUploaderComponent` for all file selection fields
- No need for hidden `<input type="file">` element
- No need for `viewChild` to reference the file input
- No need for `onFileInputClick()` method
- The `(onUpload)` event emits `File | null` directly (not `Event`)
- Works with reactive forms via `formControlName`
- Automatically handles the folder icon and file name display

### Reference Example

See `libs/switch/shared/features/src/lib/import-file/import-file.component.html` for a complete example.

---

## Form Components (UI Layer Pattern)

Forms should be in the `ui/` layer and emit events:

```typescript
@Component({
  selector: 'one-ui-my-form',
  standalone: true,
  imports: [ReactiveFormsModule, MatFormFieldModule, MatInputModule],
  template: `
    <form [formGroup]="form" (ngSubmit)="onSubmit()">
      <mat-form-field>
        <mat-label>Name</mat-label>
        <input matInput formControlName="name" />
        <mat-error oneUiFormError="name"></mat-error>
      </mat-form-field>

      <button mat-flat-button color="primary" type="submit">Save</button>
    </form>
  `,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class MyFormComponent {
  initialData = input<MyData | null>(null);

  save = output<MyData>();
  cancel = output<void>();

  private fb = inject(NonNullableFormBuilder);

  form = this.fb.group({
    name: ['', [OneValidators.required()]]
  });

  onSubmit() {
    if (this.form.valid) {
      this.save.emit(this.form.getRawValue());
    }
  }
}
```
