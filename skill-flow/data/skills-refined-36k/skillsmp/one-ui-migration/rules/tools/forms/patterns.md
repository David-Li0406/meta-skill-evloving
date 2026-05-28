# Form Patterns and Best Practices

## Use NonNullableFormBuilder and getRawValue()

**ALWAYS** use `NonNullableFormBuilder` instead of `FormBuilder` for better type safety:

### ❌ Old Pattern

```typescript
import { FormBuilder } from '@angular/forms';

readonly #fb = inject(FormBuilder);

onSubmit() {
  const formValue = this.form.value;  // Type: { name?: string | null, email?: string | null }
  // Need type assertion or null checks
}
```

### ✅ New Pattern

```typescript
import { NonNullableFormBuilder } from '@angular/forms';

readonly #fb = inject(NonNullableFormBuilder);

onSubmit() {
  const { name, email } = this.form.getRawValue();  // Type: { name: string, email: string }
  // No null checks needed, cleaner destructuring
}
```

**Benefits:**
- `NonNullableFormBuilder` - Form control values are non-nullable by default
- `getRawValue()` - Returns all values (including disabled controls) with proper typing
- Better type inference, no need for type assertions

---

## Dialog Best Practices

### Use mat-dialog-close for Cancel Button

Use `mat-dialog-close` directive instead of creating an `onCancel()` method:

#### ❌ Verbose Pattern

```typescript
// Component
onCancel() {
  this.#dialogRef.close();
}
```

```html
<!-- Template -->
<button mat-button (click)="onCancel()">Cancel</button>
```

#### ✅ Simplified Pattern

```html
<!-- Template - no component method needed -->
<button mat-button mat-dialog-close>Cancel</button>

<!-- With return value -->
<button mat-button [mat-dialog-close]="{ cancelled: true }">Cancel</button>
```

### Dialog Form Initialization

When creating forms in dialogs with edit mode support, initialize form values directly instead of using `ngOnInit` with `patchValue`:

### ❌ Verbose Pattern

```typescript
readonly form = this.#fb.group({
  inboundInterface: ['', [OneValidators.required]],
  outboundInterface: ['', [OneValidators.required]]
});

ngOnInit() {
  if (this.dialogData.row) {
    this.form.patchValue({
      inboundInterface: this.dialogData.row.inboundInterfaceRaw,
      outboundInterface: this.dialogData.row.outboundInterfaceRaw
    });
  }
}
```

### ✅ Simplified Pattern

```typescript
readonly form = this.#fb.group({
  inboundInterface: [this.dialogData.row?.inboundInterfaceRaw ?? '', [OneValidators.required]],
  outboundInterface: [this.dialogData.row?.outboundInterfaceRaw ?? '', [OneValidators.required]]
});
```

This approach:
- Eliminates the need for conditional `patchValue` in `ngOnInit`
- Uses optional chaining (`?.`) and nullish coalescing (`??`) for cleaner code
- Reduces boilerplate when handling create/edit modes in the same dialog

---

## Cross-Field Validation

For validators that depend on multiple fields (e.g., "inbound interface !== outbound interface"), use **control-level validators** instead of **group-level validators**:

### ❌ Old Pattern - Group Validator with setErrors()

```typescript
// Group validator - AVOID
broadcastForwardingForm = new FormGroup(
  {
    inboundInterface: new FormControl(null, [Validators.required]),
    outboundInterface: new FormControl(null, [Validators.required])
  },
  [this.checkIfDuplicate()]  // Group validator
);

private checkIfDuplicate(): ValidatorFn {
  return (form: FormGroup): ValidationErrors | null => {
    if (form.value.inboundInterface === form.value.outboundInterface) {
      // ⚠️ setErrors() overwrites ALL errors on the control!
      form.get('inboundInterface').setErrors({ is_multicst: true });
      form.get('outboundInterface').setErrors({ is_multicst: true });
    } else {
      form.get('inboundInterface').setErrors(null);  // Clears required error too!
      form.get('outboundInterface').setErrors(null);
    }
    return null;
  };
}
```

### ✅ New Pattern - Control Validator with updateValueAndValidity()

```typescript
readonly form = this.#fb.group({
  inboundInterface: ['', [OneValidators.required]],
  outboundInterface: ['', [OneValidators.required, this.#sameInterfaceValidator()]],
  udp: ['', [OneValidators.required]]
});

constructor() {
  // Re-validate outboundInterface when inboundInterface changes
  merge(
    this.form.controls.inboundInterface.valueChanges,
    this.form.controls.udp.valueChanges
  )
    .pipe(takeUntilDestroyed())
    .subscribe(() => this.form.controls.outboundInterface.updateValueAndValidity());
}

#sameInterfaceValidator(): ValidatorFn {
  return (control: AbstractControl): ValidationErrors | null => {
    const outbound = control.value;
    const inbound = control.parent?.get('inboundInterface')?.value;
    if (inbound && outbound && inbound === outbound) {
      return { is_multicst: true };  // Returns error, doesn't overwrite others
    }
    return null;
  };
}
```

**Benefits of control-level validators:**
- Doesn't use `setErrors()` which can overwrite other errors
- Returns validation errors directly
- Uses `updateValueAndValidity()` to trigger re-validation when dependencies change
- Error keys are clearer and more specific

---

## Accessing Form Controls in Templates

Use `form.controls.xxx` instead of `form.get('xxx')` for type safety and cleaner code. For commonly accessed values, use `@let` to avoid repetition.

### ❌ Old Pattern

```html
<form [formGroup]="form">
  @if (form.get('method')?.value === 'SCP' || form.get('method')?.value === 'SFTP') {
    <mat-form-field>
      <input matInput formControlName="account" />
      <mat-hint>{{ form.get('account')?.value?.length ?? 0 }} / 31</mat-hint>
    </mat-form-field>
  }

  @if (form.get('method')?.value === 'TFTP' || form.get('method')?.value === 'SCP') {
    <!-- More fields... -->
  }
</form>
```

### ✅ New Pattern

```html
<form [formGroup]="form">
  @let method = form.controls.method.value;

  @if (method === 'SCP' || method === 'SFTP') {
    <mat-form-field>
      <input matInput formControlName="account" />
      <mat-hint>{{ form.controls.account.value?.length ?? 0 }} / 31</mat-hint>
    </mat-form-field>
  }

  @if (method === 'TFTP' || method === 'SCP') {
    <!-- More fields... -->
  }
</form>
```

**Guidelines:**
- Use `form.controls.xxx` instead of `form.get('xxx')` - better type safety, no optional chaining needed on the control itself
- Use `@let` for values accessed multiple times (e.g., `@let method = form.controls.method.value;`)
- For single-use access, direct `form.controls.xxx.value` is sufficient
- `@let` must be placed inside the `<form>` tag (within the template scope)

---

## Reactive Effects with Form Controls

When using Angular `effect()` to react to form control changes, you **MUST** use `toSignal()` to convert the form control's `valueChanges` to a signal. Reading form control values directly in an effect is **NOT reactive**.

### ❌ Wrong Pattern - Not Reactive

```typescript
constructor() {
  // This effect will NOT re-run when the form control value changes!
  effect(() => {
    const retryEnabled = this.form.controls.authenticationRetry.value;  // Not a signal!
    if (retryEnabled) {
      this.form.controls.authenticationRetryInterval.enable();
    } else {
      this.form.controls.authenticationRetryInterval.disable();
    }
  });
}
```

### ✅ Correct Pattern - Using toSignal()

```typescript
import { toSignal } from '@angular/core/rxjs-interop';

// Convert valueChanges to a signal
readonly #authenticationRetryChange = toSignal(
  this.form.controls.authenticationRetry.valueChanges,
  { initialValue: false }
);

constructor() {
  // Effect will re-run when the signal changes
  effect(
    () => {
      const retryEnabled = this.#authenticationRetryChange();  // Reading a signal!
      if (retryEnabled) {
        this.form.controls.authenticationRetryInterval.enable();
      } else {
        this.form.controls.authenticationRetryInterval.disable();
      }
    },
    { allowSignalWrites: true }  // Required when effect modifies form state
  );
}
```

### Key Points

1. **Use `toSignal()`** - Convert `valueChanges` Observable to a signal
2. **Provide `initialValue`** - Required for synchronous access before first emission
3. **Use `allowSignalWrites: true`** - Required when the effect modifies signals or form state
4. **Use private naming `#`** - For internal signal fields

### Real-World Example: Mutual Exclusion

When two form controls should be mutually exclusive (only one can be enabled at a time):

```typescript
readonly #primaryLocalRadiusServerChange = toSignal(
  this.form.controls.primaryLocalRadiusServer.valueChanges,
  { initialValue: 0 }
);

readonly #secondaryLocalRadiusServerChange = toSignal(
  this.form.controls.secondaryLocalRadiusServer.valueChanges,
  { initialValue: 0 }
);

constructor() {
  // When primary is enabled, disable secondary and reset its value
  effect(
    () => {
      const primaryLocal = this.#primaryLocalRadiusServerChange();
      if (primaryLocal === 1) {
        this.form.controls.serverAddress1.disable();
        // Reset secondary if also enabled (mutual exclusion)
        if (this.form.controls.secondaryLocalRadiusServer.value === 1) {
          this.form.controls.secondaryLocalRadiusServer.setValue(0);
        }
      } else {
        this.form.controls.serverAddress1.enable();
      }
    },
    { allowSignalWrites: true }
  );

  // Similar effect for secondary...
}
```

### When to Use Each Pattern

| Scenario | Pattern |
| --- | --- |
| Re-validate field when another field changes | `valueChanges.pipe(takeUntilDestroyed()).subscribe(() => control.updateValueAndValidity())` |
| Enable/disable fields based on another field | `toSignal()` + `effect()` with `allowSignalWrites: true` |
| Complex state updates based on form changes | `toSignal()` + `effect()` |
| Simple value transformation | `valueChanges` with RxJS operators |
