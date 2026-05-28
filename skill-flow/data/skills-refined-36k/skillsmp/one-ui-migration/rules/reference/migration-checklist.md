# Migration Checklist

When migrating a component/feature from old project:

## Angular 20 Syntax

- [ ] Convert to standalone component
- [ ] Replace `*ngIf` → `@if`
- [ ] Replace `*ngFor` → `@for (item of items; track item.id)`
- [ ] Replace `*ngSwitch` → `@switch`
- [ ] Replace constructor injection → `inject()`
- [ ] Replace `BehaviorSubject` → `signal()`
- [ ] Replace `@Input()` → `input()` (Angular 17.1+)
- [ ] Replace `@Output()` → `output()` (Angular 17.3+)

## DDD Architecture

- [ ] Identify component type:
  - [ ] Business logic → `domain/`
  - [ ] Smart component → `features/`
  - [ ] Dialog → `features/`
  - [ ] Table → `ui/`
  - [ ] Form → `ui/`
  - [ ] Routes → `shell/`
- [ ] Create proper directory structure (domain/features/ui/shell)

### ⚠️ Page Forms Must Be in UI Layer (CRITICAL)

- [ ] **DO NOT put form templates directly in page components**
- [ ] Extract page forms to `ui/` layer as separate components (e.g., `*-setting`, `*-form`)
- [ ] Page component in `features/` should only:
  - [ ] Import and use the form component from `ui/`
  - [ ] Pass data to form via `input()`
  - [ ] Handle form submission via `output()`
- [ ] Form component in `ui/` should:
  - [ ] Receive initial values via `input()`
  - [ ] Emit form data via `output()` (e.g., `save`, `apply`)
  - [ ] Have NO store injection
  - [ ] Have NO direct API calls

**Example Structure:**
```
libs/mxsecurity/ddns-page/
├── features/
│   └── ddns-page/
│       └── ddns-page.component.ts  # Smart component - imports form, handles events
└── ui/
    └── ddns-setting/
        ├── ddns-setting.component.ts   # Form component - NO store
        └── ddns-setting.component.html # Form template
```

- [ ] Ensure UI components:
  - [ ] Use `input()` to receive data from parent
  - [ ] Use `output()` to emit events to parent
  - [ ] Have NO store injection
  - [ ] Have NO HTTP calls
  - [ ] Have NO business logic
- [ ] Ensure Feature components:
  - [ ] Inject stores
  - [ ] Pass data to UI components via `[property]`
  - [ ] Handle UI events via `(event)`
  - [ ] Manage dialog lifecycle
- [ ] Ensure Domain layer:
  - [ ] Use NgRx SignalStore for state management
  - [ ] Use `queryMethod` for GET requests
  - [ ] Use `mutationMethod` for POST/PUT/DELETE requests
  - [ ] Export public API via `index.ts`

## State Management

- [ ] Use NgRx SignalStore pattern
- [ ] Use `queryMethod`/`mutationMethod` for API calls
- [ ] Move data loading to route resolvers (shell layer)
- [ ] Use `sessionStorage` for token storage

## Code Quality

- [ ] Update imports to use `@one-ui/mxsecurity/*` path aliases
- [ ] Add proper TypeScript types (no `any`)
- [ ] Use `OnPush` change detection
- [ ] Add `track` expression in `@for` loops
- [ ] Check Context7 for latest Angular best practices

## Form Validation

- [ ] Replace `import { Validators }` with `import { OneValidators }`
- [ ] Replace `Validators.required` with `OneValidators.required`
- [ ] Replace `Validators.minLength(n)` with `OneValidators.minLength(n)` or `OneValidators.rangeLength(min, max, field)`
- [ ] Replace `Validators.min(n)` + `Validators.max(m)` with `OneValidators.range(n, m)` ⚠️ **NO separate min/max!**
- [ ] Replace `Validators.pattern(ValidatorPattern.XXX)` with corresponding `OneValidators` method
- [ ] Replace custom validators with OneValidators equivalents
- [ ] Add `oneUiFormError` directive to `<mat-error>` tags
- [ ] Remove manual error message handling code

## ⚠️ Password Input Component (CRITICAL)

- [ ] **DO NOT manually implement password visibility toggle**
- [ ] Use `MxPasswordInputComponent` from `@moxa/formoxa/mx-password-input`
- [ ] Import: `import { MxPasswordInputComponent } from '@moxa/formoxa/mx-password-input';`

**❌ Wrong - Manual implementation:**
```html
<input matInput [type]="hidePassword() ? 'password' : 'text'" />
<button mat-icon-button (click)="togglePasswordVisibility()">
  <mat-icon>{{ hidePassword() ? 'visibility_off' : 'visibility' }}</mat-icon>
</button>
```

**✅ Correct - Use mx-password-input:**
```html
<mat-form-field>
  @let passwordCtrl = form.controls.password;
  <mat-label>{{ t('general.common_account.password') }}</mat-label>
  <mx-password-input formControlName="password" [maxlength]="45"></mx-password-input>
  <mat-hint align="end">{{ passwordCtrl.value.length }} / 45</mat-hint>
  <mat-error oneUiFormError="password"></mat-error>
</mat-form-field>
```

## ⚠️ Translation Keys (CRITICAL)

- [ ] **DO NOT create new translation keys**
- [ ] **DO NOT modify existing translation keys**
- [ ] Read source HTML templates to find exact translation keys
- [ ] Copy translation keys exactly as they appear in source
- [ ] Verify all translation keys match source:
  - [ ] Page titles
  - [ ] Tab labels
  - [ ] Dialog titles and descriptions
  - [ ] Form field labels
  - [ ] Button labels
  - [ ] Tooltip texts
  - [ ] Table column headers
  - [ ] Error messages
  - [ ] Hints and placeholders

## ⚠️ Form Layout (CRITICAL)

- [ ] **DO NOT change form field row groupings**
- [ ] Analyze source for `fxLayout="row"` patterns
- [ ] Use `.form-row` class to maintain same layout
- [ ] Verify field groupings match source exactly:
  - [ ] Which fields appear on same row
  - [ ] Order of fields within rows
  - [ ] Single-field rows vs multi-field rows

## ⚠️ Page Component Styling (CRITICAL)

- [ ] **DO NOT add `padding: 24px` to page components**
- [ ] Layout padding is handled by shell/app layout
- [ ] Page component SCSS should only have `:host { display: block; }`

## ⚠️ Table Toolbar Button Order (CRITICAL)

- [ ] Button order must be: **Refresh → Create/Delete** (if applicable)
- [ ] Refresh button: only add if old code has refresh button, comes first
- [ ] Create button: shown when `selection.length === 0`
- [ ] Delete button: shown when `selection.length >= 1`

## ⚠️ No data-testid Attributes (CRITICAL)

- [ ] **DO NOT add `data-testid` attributes**
- [ ] This project does not use `data-testid` for testing
- [ ] Remove any `data-testid` attributes from migrated code
- [ ] Remove any `[attr.data-testid]` bindings from templates

## ⚠️ Tab Group Configuration (CRITICAL)

- [ ] Import `MxTabGroupDirective` from `@moxa/formoxa/mx-tabs`
- [ ] Add `MxTabGroupDirective` to component's `imports` array
- [ ] `<mat-tab-group>` must include the following attributes:
  - [ ] `mxTabGroup` directive
  - [ ] `animationDuration="0ms"`
  - [ ] `[mat-stretch-tabs]="false"`
- [ ] Example:
  ```typescript
  import { MxTabGroupDirective } from '@moxa/formoxa/mx-tabs';

  @Component({
    imports: [MatTabsModule, MxTabGroupDirective, ...]
  })
  ```
  ```html
  <mat-tab-group mxTabGroup animationDuration="0ms" [mat-stretch-tabs]="false">
  ```

## ⚠️ Number-Only Input Directive (CRITICAL)

- [ ] **Replace `appNumberOnly` with `oneUiNumberOnly`**
- [ ] Search old project for `appNumberOnly` usage
- [ ] Import `NumberOnlyDirective` from `@one-ui/mxsecurity/shared/domain`
- [ ] Add `NumberOnlyDirective` to component's `imports` array

**❌ Old project:**
```html
<input matInput formControlName="port" appNumberOnly />
```

**✅ New project:**
```typescript
import { NumberOnlyDirective } from '@one-ui/mxsecurity/shared/domain';

@Component({
  imports: [NumberOnlyDirective, ...]
})
```
```html
<input matInput formControlName="port" oneUiNumberOnly />
```

**Location:** `libs/mxsecurity/shared/domain/src/lib/directives/number-only.directive.ts`
