# Common Pitfalls: DDD Architecture Violations

## ❌ **Violation 0: Page Form Template in Features Layer (MOST COMMON MISTAKE)**

**⚠️ THIS IS THE MOST COMMON MIGRATION MISTAKE - ALWAYS CHECK FOR THIS!**

Page setting forms **MUST** be extracted to the UI layer, NOT embedded directly in the page component template.

```
❌ WRONG STRUCTURE:
libs/mxsecurity/dosPolicy-page/
├── features/
│   └── dosPolicy-page/
│       ├── dosPolicy-page.component.ts
│       └── dosPolicy-page.component.html   # ❌ Contains <form> with <mat-form-field>
└── ui/
    └── (empty or missing)                  # ❌ No form component!

✅ CORRECT STRUCTURE:
libs/mxsecurity/dosPolicy-page/
├── features/
│   └── dosPolicy-page/
│       ├── dosPolicy-page.component.ts     # Smart component - orchestrates
│       └── dosPolicy-page.component.html   # Only imports <one-ui-dos-log-setting>
└── ui/
    └── dos-log-setting/
        ├── dos-log-setting.component.ts    # Form logic - NO store injection
        └── dos-log-setting.component.html  # Form template with mat-form-field
```

### ❌ WRONG - Form in Features Template

```html
<!-- features/dosPolicy-page/dosPolicy-page.component.html -->
<div class="gl-page-content">
  <one-ui-breadcrumb />
  <mx-page-title [title]="t('features.dos_policy.page_title')" />

  <!-- ❌ WRONG - Form template directly in page component -->
  <div class="content-wrapper">
    <form [formGroup]="logForm" (ngSubmit)="onApplyLogSettings()">
      <mat-form-field>
        <mat-label>{{ t('general.common.log') }}</mat-label>
        <mat-select formControlName="log">
          @for (option of logOptions; track option.value) {
            <mat-option [value]="option.value">{{ option.text }}</mat-option>
          }
        </mat-select>
      </mat-form-field>
      <!-- ... more form fields ... -->
      <button mat-flat-button type="submit">{{ t('general.button.apply') }}</button>
    </form>
  </div>
</div>
```

### ✅ CORRECT - Form Extracted to UI Layer

```html
<!-- features/dosPolicy-page/dosPolicy-page.component.html -->
<div class="gl-page-content">
  <one-ui-breadcrumb />
  <mx-page-title [title]="t('features.dos_policy.page_title')" />

  <div class="content-wrapper">
    <!-- ✅ CORRECT - Use UI component -->
    <one-ui-dos-log-setting
      [initialData]="store.rawData()"
      [loading]="store.loading()"
      [noPermission]="noPermission"
      (apply)="onApplyLogSettings($event)"
    />
  </div>
</div>
```

```typescript
// ui/dos-log-setting/dos-log-setting.component.ts
@Component({
  selector: 'one-ui-dos-log-setting'
})
export class DosLogSettingComponent {
  // ✅ Inputs - receive data from parent
  initialData = input<SRV_IPT_DOS | null>(null);
  loading = input<boolean>(false);
  noPermission = input<boolean>(false);

  // ✅ Outputs - emit events to parent
  apply = output<LogSettingsPayload>();

  // ✅ Form logic only - NO store injection
  readonly #fb = inject(NonNullableFormBuilder);
  readonly form = this.#fb.group({ ... });

  onSubmit() {
    if (this.form.valid) {
      this.apply.emit(buildLogSettingsPayload(this.form.getRawValue()));
    }
  }
}
```

### Why this matters

- **Reusability**: Form components can be reused in dialogs or other contexts
- **Testability**: Form logic can be tested without mocking stores
- **Separation of Concerns**: Features handle orchestration, UI handles presentation
- **Consistency**: Same pattern as table components

### How to fix existing violations

1. Create a new component in `ui/` directory (e.g., `dos-log-setting/`)
2. Move the `<form>` template from page component to UI component
3. Move form-related logic (form group, validation, options) to UI component
4. Add `input()` for data and `output()` for events
5. Update page component to use the new UI component with input/output bindings

---

## ❌ **Violation 1: UI Component Injecting Store**

```typescript
// ❌ WRONG - UI component should NOT inject store
@Component({
  selector: 'one-ui-user-table',
  template: `...`
})
export class UserTableComponent {
  private store = inject(UserManagementStore); // ❌ NO!

  users = this.store.users; // ❌ NO!

  deleteUser(id: string) {
    this.store.deleteUser(id); // ❌ NO!
  }
}
```

```typescript
// ✅ CORRECT - UI component receives data via input, emits events via output
@Component({
  selector: 'one-ui-user-table',
  template: ` <button (click)="deleteUser.emit(user.id)">Delete</button> `
})
export class UserTableComponent {
  users = input.required<User[]>(); // ✅ Input
  deleteUser = output<string>(); // ✅ Output
}

// Feature component handles the store interaction
@Component({
  selector: 'one-ui-user-management-page',
  template: ` <one-ui-user-table [users]="users()" (deleteUser)="onDeleteUser($event)" /> `
})
export class UserManagementPageComponent {
  private store = inject(UserManagementStore); // ✅ Features inject store
  users = this.store.users;

  onDeleteUser(id: string) {
    this.store.deleteUser(id); // ✅ Features call store
  }
}
```

---

## ❌ **Violation 2: Dialog in UI Layer**

```typescript
// ❌ WRONG - Dialog in ui/
libs/mxsecurity/user-management/ui/create-user-dialog/  // ❌ NO!
```

```typescript
// ✅ CORRECT - Dialog in features/
libs/mxsecurity/user-management/features/create-user-dialog/  // ✅ YES!

// Dialog can use UI components inside
@Component({
  selector: 'one-ui-create-user-dialog',
  template: `
    <h2 mat-dialog-title>Create User</h2>
    <mat-dialog-content>
      <one-ui-user-form          <!-- ✅ Use UI component -->
        [user]="null"
        (save)="onSave($event)"
      />
    </mat-dialog-content>
  `
})
export class CreateUserDialogComponent {
  private dialogRef = inject(MatDialogRef); // ✅ Features manage dialog
}
```

---

## ❌ **Violation 3: Business Logic in Features**

```typescript
// ❌ WRONG - Business logic in features component
@Component({
  selector: 'one-ui-user-management-page',
  template: `...`
})
export class UserManagementPageComponent {
  private http = inject(HttpClient);

  loadUsers() {
    // ❌ NO! Business logic belongs in domain layer
    this.http.get('/api/users').subscribe((users) => {
      this.users = users;
    });
  }

  validateUser(user: User): boolean {
    // ❌ NO! Validation logic belongs in domain layer
    return user.email.includes('@') && user.age >= 18;
  }
}
```

```typescript
// ✅ CORRECT - Business logic in domain layer
// domain/user-management.store.ts
export const UserManagementStore = signalStore(
  withMethods((store, api = inject(UserManagementApiService)) => ({
    loadUsers: queryMethod<void, User[]>({
      store,
      observe: () => api.getUsers(), // ✅ API call in domain
      next: (users) => patchState(store, { users })
    })
  }))
);

// domain/user.validator.ts
export function validateUser(user: User): boolean {
  return user.email.includes('@') && user.age >= 18; // ✅ Logic in domain
}

// features/user-management-page.component.ts
export class UserManagementPageComponent {
  private store = inject(UserManagementStore);

  constructor() {
    effect(() => {
      this.store.loadUsers(); // ✅ Features just call store methods
    });
  }
}
```

---

## ❌ **Violation 4: Form with HTTP Calls in UI**

```typescript
// ❌ WRONG - UI form making HTTP calls
@Component({
  selector: 'one-ui-user-form',
  template: `...`
})
export class UserFormComponent {
  private http = inject(HttpClient); // ❌ NO!

  onSubmit() {
    // ❌ NO! HTTP calls belong in domain layer
    this.http.post('/api/users', this.form.value).subscribe();
  }
}
```

```typescript
// ✅ CORRECT - UI form emits events, features handle API
// ui/user-form.component.ts
@Component({
  selector: 'one-ui-user-form',
  template: `
    <form [formGroup]="form" (ngSubmit)="onSubmit()">
      <button type="submit">Save</button>
    </form>
  `
})
export class UserFormComponent {
  save = output<User>(); // ✅ Output event

  onSubmit() {
    if (this.form.valid) {
      this.save.emit(this.form.value); // ✅ Just emit
    }
  }
}

// features/user-management-page.component.ts
@Component({
  template: ` <one-ui-user-form (save)="onSave($event)" /> `
})
export class UserManagementPageComponent {
  private store = inject(UserManagementStore);

  onSave(user: User) {
    this.store.createUser(user); // ✅ Features call store
  }
}
```

---

## ❌ **Violation 5: Shared Component in Wrong Layer**

```typescript
// ❌ WRONG - Generic table in features (not reusable)
libs/mxsecurity/user-management/features/user-table/  // ❌ NO!

// ❌ WRONG - Feature-specific component in ui (not generic)
libs/mxsecurity/shared/ui/user-management-page/      // ❌ NO!
```

```typescript
// ✅ CORRECT - Generic components in ui, specific in features
libs/mxsecurity/user-management/ui/user-table/        // ✅ Generic table in ui
libs/mxsecurity/user-management/features/user-management-page/  // ✅ Specific page in features
```

---

## Quick Reference: Layer Responsibilities

| Layer | Responsibilities | Can Inject |
|-------|------------------|------------|
| **UI** | Presentational components, forms, tables | Services (NOT stores) |
| **Features** | Page components, dialogs, orchestration | Stores, Services |
| **Domain** | Business logic, state, API services | HttpClient, Services |
| **Shell** | Routing, layout | Stores (for guards) |

## Quick Reference: What Goes Where

| Component Type | Layer | Can Use Store? |
|----------------|-------|----------------|
| Page component | Features | ✅ Yes |
| Dialog | Features | ✅ Yes |
| Form component | UI | ❌ No |
| Table component | UI | ❌ No |
| Button/Input | UI | ❌ No |
