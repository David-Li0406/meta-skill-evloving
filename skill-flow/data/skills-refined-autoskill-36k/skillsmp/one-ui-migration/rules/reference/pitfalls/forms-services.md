# Common Pitfalls: Forms & Services

## ⚠️ Store Methods Import Path - Use shared/domain NOT shared/util

**CRITICAL**: `mutationMethod` and `queryMethod` must be imported from `@one-ui/mxsecurity/shared/domain`, NOT from `@one-ui/mxsecurity/shared/util`.

### ❌ **WRONG - Importing from shared/util**

```typescript
// ❌ WRONG - This path does not exist
import { mutationMethod, queryMethod } from '@one-ui/mxsecurity/shared/util';
```

### ✅ **CORRECT - Importing from shared/domain**

```typescript
// ✅ CORRECT - Import from shared/domain
import { loadingInitialState, mutationMethod, queryMethod } from '@one-ui/mxsecurity/shared/domain';
```

### Full Store Example

```typescript
import { inject } from '@angular/core';
import { patchState, signalStore, withMethods, withState } from '@ngrx/signals';
import type { LoadingState } from '@one-ui/mxsecurity/shared/domain';
import { loadingInitialState, mutationMethod, queryMethod } from '@one-ui/mxsecurity/shared/domain';
import { MyApiService } from './my-page.api';

export const MyStore = signalStore(
  withState(initialState),
  withMethods((store, api = inject(MyApiService)) => ({
    loadPageData: queryMethod<void, Response>({
      store,
      observe: () => api.getData$(),
      next: (data) => patchState(store, { data })
    }),
    updateData: mutationMethod<Request, Response>({
      store,
      observe: (input) => api.updateData$(input)
    })
  }))
);
```

---

## ⚠️ Constants and Enums - Don't Create Separate Definition Files

**CRITICAL**: Don't create separate `.def.ts` files for constants/enums that are only used in one place.

### ❌ **WRONG - Creating Unnecessary Definition Files**

```typescript
// ❌ WRONG - libs/mxsecurity/8021x-page/domain/src/lib/8021x-page.def.ts
export enum AuthMode {
  RADIUS = 0,
  LOCAL = 1,
  RADIUS_LOCAL = 2
}

export const LOCAL_DATABASE_SIZE_RANGE = { max: 32 };
export const PORT_AUTH_ENABLE = { ... };
```

### ✅ **CORRECT - Define Constants Where Used**

```typescript
// ✅ CORRECT - Define enum directly in the component that uses it
// libs/mxsecurity/8021x-page/ui/src/lib/general-settings-form/general-settings-form.component.ts
enum AuthMode {
  RADIUS = 0,
  LOCAL = 1,
  RADIUS_LOCAL = 2
}

@Component({ ... })
export class GeneralSettingsFormComponent {
  readonly authModeOptions = [
    { value: AuthMode.RADIUS, text: 'RADIUS' },
    { value: AuthMode.LOCAL, text: 'Local' },
    { value: AuthMode.RADIUS_LOCAL, text: 'RADIUS + Local' }
  ];
}
```

```typescript
// ✅ CORRECT - Define constant directly in the component
// libs/mxsecurity/8021x-page/ui/src/lib/local-database-table/local-database-table.component.ts
@Component({ ... })
export class LocalDatabaseTableComponent {
  readonly tableMaxSize = 32;  // Not imported from .def.ts
}
```

### Guidelines

- **Only extract to shared domain** when genuinely reused across multiple files
- **Use API types directly** from `@one-ui/mxsecurity/shared/domain` instead of creating local type aliases
- **Delete unused exports** - if a constant is no longer used, remove it completely

---

## ⚠️ Service Usage - Use MxSnackbarService

**CRITICAL**: Don't use `MatSnackBar` directly. Always use `MxSnackbarService` from `@moxa/formoxa/mx-snackbar`.

### ❌ **WRONG - Using MatSnackBar Directly**

```typescript
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({ ... })
export class MyComponent {
  readonly #snackBar = inject(MatSnackBar);  // ❌ WRONG

  showMessage() {
    this.#snackBar.open('Success!', 'Close', { duration: 3000 });  // ❌ WRONG
  }
}
```

### ✅ **CORRECT - Using MxSnackbarService**

```typescript
import { MxSnackbarService } from '@moxa/formoxa/mx-snackbar';

@Component({ ... })
export class MyComponent {
  readonly #snackBar = inject(MxSnackbarService);  // ✅ CORRECT

  showMessage() {
    this.#snackBar.open('Success!');  // ✅ CORRECT - consistent styling
  }
}
```

### Why Use MxSnackbarService

- Provides consistent styling and behavior across the application
- Automatically handles i18n and theming
- Follows Moxa design system guidelines

---

## ⚠️ Form Controls - Use controls.xxx Instead of .get()

**CRITICAL**: Use typed `controls.xxx` instead of `.get('xxx')` for better type safety.

### ❌ **WRONG - Using .get()**

```typescript
// ❌ WRONG - No type safety, requires null check
const value = this.form.get('username')?.value;
const control = this.form.get('password');
if (control) {
  control.setErrors({ ... });
}
```

### ✅ **CORRECT - Using controls.xxx**

```typescript
// ✅ CORRECT - Type safe, no null check needed
const value = this.form.controls.username.value;
const control = this.form.controls.password;
control.setErrors({ ... });
```

### In ValidatorFn (with type assertion)

When using `ValidatorFn`, the parameter is `AbstractControl` which doesn't have typed controls. Use type assertion:

```typescript
#myValidator(): ValidatorFn {
  return (formGroup: AbstractControl): null => {
    // ✅ Cast to typed form to access controls
    const controls = (formGroup as typeof this.form).controls;
    const fieldA = controls.fieldA.value;
    const fieldB = controls.fieldB.value;
    const fieldBControl = controls.fieldB;

    // No null check needed - typed controls are guaranteed to exist
    if (fieldA > fieldB) {
      fieldBControl.setErrors({ customError: true });
    }

    return null;
  };
}
```

### Why Use controls.xxx

- **Type safety** - TypeScript knows the control types
- **No null checks** - Typed controls are guaranteed to exist
- **Better IDE support** - Autocomplete and refactoring work correctly
- **Compile-time errors** - Typos in control names are caught at build time

---

## ⚠️ Effect with Form Controls - MUST Use toSignal()

**CRITICAL**: When using Angular `effect()` to react to form control value changes, you **MUST** use `toSignal()` to convert `valueChanges` to a signal. Reading form control values directly is **NOT reactive**.

### ❌ **WRONG - Not Reactive**

```typescript
constructor() {
  // ❌ WRONG - This effect will NOT re-run when the form control value changes!
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

### ✅ **CORRECT - Using toSignal()**

```typescript
import { toSignal } from '@angular/core/rxjs-interop';

// Convert valueChanges to a signal
readonly #authenticationRetryChange = toSignal(
  this.form.controls.authenticationRetry.valueChanges,
  { initialValue: false }
);

constructor() {
  // ✅ CORRECT - Effect will re-run when the signal changes
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

See `forms/patterns.md` for detailed examples and patterns.

---

## ⚠️ Empty Value Display - Use EMPTY_DASH

**CRITICAL**: When migrating code that displays empty/null values, replace `this.utils.emptyDash` and `this.utils.emptyData` with `EMPTY_DASH` from shared domain.

### ❌ **Old System**

```typescript
// Old patterns using utils service
this.utils.emptyDash    // returns '--' or '---'
this.utils.emptyData    // returns '--' or '---'
```

### ✅ **New System - Use EMPTY_DASH**

```typescript
import { EMPTY_DASH } from '@one-ui/mxsecurity/shared/domain';

// Use EMPTY_DASH constant
const display = value ? value : EMPTY_DASH;

// In template data transformation
sport: row.sport ? `${row.sport}` : EMPTY_DASH,
dport: row.dport ? `${row.dport}` : EMPTY_DASH,
```

### Location

```
libs/mxsecurity/shared/domain/src/lib/helpers/text.helper.ts
```

### Exception

If the old code uses `emptyDash`/`emptyData` with special conditional logic (e.g., checking if value equals the empty string for specific behavior), handle those cases separately rather than blindly replacing.

---

## ⚠️ appNumberOnly Directive - MUST Migrate to oneUiNumberOnly

**CRITICAL**: When migrating from the old project, if you see `appNumberOnly` directive on input fields, you **MUST** replace it with `oneUiNumberOnly` from the new shared library.

### ❌ **Old Project - appNumberOnly**

```html
<!-- Old project uses appNumberOnly -->
<input matInput formControlName="port" appNumberOnly />
```

### ✅ **New Project - oneUiNumberOnly**

```html
<!-- New project uses oneUiNumberOnly -->
<input matInput formControlName="port" oneUiNumberOnly />
```

### Import and Setup

```typescript
import { NumberOnlyDirective } from '@one-ui/mxsecurity/shared/domain';

@Component({
  imports: [
    // ...
    NumberOnlyDirective  // Add to imports
  ]
})
export class MyComponent {}
```

### What It Does

The `NumberOnlyDirective` (`libs/mxsecurity/shared/domain/src/lib/directives/number-only.directive.ts`):

- Restricts input to numeric characters only (0-9)
- Automatically strips non-numeric characters on input
- Sets the form control value to `number | null` (not string)
- Uses `{ emitEvent: false }` to prevent unnecessary form change events

### Common Use Cases

- Port number inputs (e.g., RADIUS port, SSH port)
- Numeric ID fields
- Count/quantity fields

### Migration Search Pattern

When migrating a page, search for `appNumberOnly` in the old project:

```bash
grep -r "appNumberOnly" /path/to/old/project/src/app/pages/{page-name}/
```

Replace all occurrences with `oneUiNumberOnly` and ensure the directive is imported.

---

## ⚠️ Password Fields - Use mx-password-input

**CRITICAL**: For password input fields, use the `<mx-password-input>` component instead of manually implementing show/hide password toggle.

### ❌ **WRONG - Manual Password Toggle**

```html
<!-- ❌ WRONG - Manual implementation -->
<mat-form-field>
  <mat-label>Password</mat-label>
  <input matInput [type]="hidePassword ? 'password' : 'text'" formControlName="password" />
  <button mat-icon-button matSuffix (click)="hidePassword = !hidePassword">
    <mat-icon>{{ hidePassword ? 'visibility_off' : 'visibility' }}</mat-icon>
  </button>
</mat-form-field>
```

### ✅ **CORRECT - Use mx-password-input**

```html
<!-- ✅ CORRECT - Use component -->
<mx-password-input
  formControlName="password"
  [maxlength]="32"
></mx-password-input>
```

```typescript
import { MxPasswordInputComponent } from '@moxa/formoxa/mx-password-input';

@Component({
  imports: [MxPasswordInputComponent]
})
export class MyComponent {}
```

---

## ⚠️ TRANSLOCO_SCOPE - DO NOT USE

**CRITICAL**: Do NOT use `TRANSLOCO_SCOPE` provider in components. The mxsecurity project uses global translation keys, not scoped translations.

### ❌ **WRONG - Using TRANSLOCO_SCOPE**

```typescript
import { TRANSLOCO_SCOPE } from '@jsverse/transloco';

@Component({
  selector: 'one-ui-my-page',
  providers: [
    {
      provide: TRANSLOCO_SCOPE,
      useValue: {
        scope: 'my-feature',
        alias: 'feature'
      }
    }
  ]
})
export class MyPageComponent {}
```

### ✅ **CORRECT - No TRANSLOCO_SCOPE**

```typescript
import { TranslocoModule } from '@jsverse/transloco';

@Component({
  selector: 'one-ui-my-page',
  imports: [TranslocoModule]
  // NO providers for TRANSLOCO_SCOPE
})
export class MyPageComponent {}
```

### Template Usage

```html
<!-- Use global keys directly -->
<div *transloco="let t">
  <mx-page-title [title]="t('features.my_feature.page_title')" />
  <button>{{ t('general.button.apply') }}</button>
</div>
```

### Reference

For correct patterns, refer to `libs/switch` projects which use global translation keys.

---

## ⚠️ Readonly Display - Use mx-key-value

**CRITICAL**: For displaying readonly key-value pairs (like "Current Time: 2024-01-01 12:00:00"), use `<mx-key-value>` instead of disabled form fields.

### ❌ **WRONG - Disabled Form Field**

```html
<!-- ❌ WRONG - Don't use disabled form field for readonly display -->
<mat-form-field>
  <mat-label>Current Time</mat-label>
  <input matInput [value]="currentTime()" disabled />
</mat-form-field>
```

### ✅ **CORRECT - Use mx-key-value**

```html
<!-- ✅ CORRECT - Use mx-key-value component -->
<mx-key-value
  [key]="t('features.time.current_time')"
  [value]="currentTime()"
></mx-key-value>
```

```typescript
import { MxKeyValueComponent } from '@moxa/formoxa/mx-key-value';

@Component({
  imports: [MxKeyValueComponent]
})
export class MyComponent {}
```

### Note

Use `[key]` attribute (NOT `[label]`) for the label text.
