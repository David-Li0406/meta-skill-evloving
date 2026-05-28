# Common Migration Pitfalls

This document describes common mistakes when migrating to One-UI with DDD architecture.

---

## DDD Architecture Violations

### ❌ Violation 0: Page Form Template in Features Layer

**⚠️ THIS IS THE MOST COMMON MIGRATION MISTAKE**

Page setting forms **MUST** be extracted to the UI layer, NOT embedded directly in the page component template.

#### Wrong Structure

```
❌ WRONG:
libs/{scope}/{feature}/
├── features/
│   └── {feature}-page/
│       ├── {feature}-page.component.ts
│       └── {feature}-page.component.html   # ❌ Contains <form> with <mat-form-field>
└── ui/
    └── (empty or missing)                  # ❌ No form component!
```

#### Correct Structure

```
✅ CORRECT:
libs/{scope}/{feature}/
├── features/
│   └── {feature}-page/
│       ├── {feature}-page.component.ts     # Smart component - orchestrates
│       └── {feature}-page.component.html   # Only imports form UI component
└── ui/
    └── {feature}-form/
        ├── {feature}-form.component.ts    # Form logic - NO store injection
        └── {feature}-form.component.html  # Form template with mat-form-field
```

#### ❌ Wrong Code Example

```html
<!-- features/{feature}-page/{feature}-page.component.html -->
<div class="gl-page-content">
  <one-ui-breadcrumb />
  <mx-page-title [title]="t('features.{feature}.page_title')" />

  <!-- ❌ WRONG - Form template directly in page component -->
  <div class="content-wrapper">
    <form [formGroup]="form" (ngSubmit)="onSubmit()">
      <mat-form-field>
        <mat-label>{{ t('general.common.name') }}</mat-label>
        <mat-select formControlName="name">
          @for (option of options; track option.value) {
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

#### ✅ Correct Code Example

**Page Component (Features)**:
```html
<!-- features/{feature}-page/{feature}-page.component.html -->
<div class="gl-page-content">
  <one-ui-breadcrumb />
  <mx-page-title [title]="t('features.{feature}.page_title')" />

  <div class="content-wrapper">
    <!-- ✅ CORRECT - Use UI component -->
    <one-ui-{feature}-form
      [initialData]="store.data()"
      [loading]="store.loading()"
      [noPermission]="noPermission"
      (apply)="onApply($event)"
    />
  </div>
</div>
```

```typescript
// features/{feature}-page/{feature}-page.component.ts
@Component({
  selector: 'one-ui-{feature}-page',
  imports: [/* UI component */]
})
export class FeaturePageComponent {
  readonly store = inject(FeatureStore);

  onApply(payload: FormPayload) {
    this.store.updateSettings({ input: payload });
  }
}
```

**Form Component (UI)**:
```typescript
// ui/{feature}-form/{feature}-form.component.ts
@Component({
  selector: 'one-ui-{feature}-form'
})
export class FeatureFormComponent {
  // ✅ Inputs - receive data from parent
  initialData = input<SettingsData | null>(null);
  loading = input<boolean>(false);
  noPermission = input<boolean>(false);

  // ✅ Outputs - emit events to parent
  apply = output<FormPayload>();

  // ✅ Form logic only - NO store injection
  readonly #fb = inject(NonNullableFormBuilder);
  readonly form = this.#fb.group({ /* ... */ });

  onSubmit() {
    if (this.form.valid) {
      this.apply.emit(this.form.getRawValue());
    }
  }
}
```

#### Why This Matters

- **Reusability**: Form components can be reused in dialogs or other contexts
- **Testability**: Form logic can be tested without mocking stores
- **Separation of Concerns**: Features handle orchestration, UI handles presentation
- **Consistency**: Same pattern as table components

#### How to Fix

1. Create a new component in `ui/` directory (e.g., `{feature}-form/`)
2. Move the `<form>` template from page component to UI component
3. Move form-related logic (form group, validation, options) to UI component
4. Add `input()` for data and `output()` for events
5. Update page component to use the new UI component with input/output bindings

---

### ❌ Violation 1: UI Component Injecting Store

UI components should **NEVER** inject stores. They should only receive data via `input()` and emit events via `output()`.

#### ❌ Wrong Code

```typescript
// ui/user-table/user-table.component.ts
@Component({
  selector: 'one-ui-user-table'
})
export class UserTableComponent {
  private store = inject(UserManagementStore); // ❌ NO!

  users = this.store.users; // ❌ NO!

  deleteUser(id: string) {
    this.store.deleteUser(id); // ❌ NO!
  }
}
```

#### ✅ Correct Code

```typescript
// ui/user-table/user-table.component.ts
@Component({
  selector: 'one-ui-user-table',
  template: `
    <button (click)="delete.emit(user.id)">Delete</button>
  `
})
export class UserTableComponent {
  users = input.required<User[]>();      // ✅ Input
  delete = output<string>();             // ✅ Output
}

// features/user-management-page/user-management-page.component.ts
@Component({
  template: `
    <one-ui-user-table
      [users]="users()"
      (delete)="onDelete($event)"
    />
  `
})
export class UserManagementPageComponent {
  private store = inject(UserManagementStore); // ✅ Features inject store
  users = this.store.users;

  onDelete(id: string) {
    this.store.deleteUser(id); // ✅ Features call store
  }
}
```

---

### ❌ Violation 2: Dialog in UI Layer

Dialogs manage their own lifecycle and often interact with stores, so they belong in the **features** layer, not the UI layer.

#### ❌ Wrong Structure

```
❌ libs/{scope}/{feature}/ui/create-user-dialog/
```

#### ✅ Correct Structure

```
✅ libs/{scope}/{feature}/features/create-user-dialog/
```

#### ✅ Correct Code

```typescript
// features/create-user-dialog/create-user-dialog.component.ts
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

  onSave(user: User) {
    this.dialogRef.close(user);
  }
}
```

---

### ❌ Violation 3: Business Logic in Features

Features components should only orchestrate. Business logic (HTTP calls, validation, data transformation) belongs in the **domain** layer.

#### ❌ Wrong Code

```typescript
// features/user-management-page/user-management-page.component.ts
@Component({
  selector: 'one-ui-user-management-page'
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

#### ✅ Correct Code

```typescript
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

// features/user-management-page/user-management-page.component.ts
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

### ❌ Violation 4: UI Form Making HTTP Calls

UI forms should only emit events. Features components handle the actual API calls via stores.

#### ❌ Wrong Code

```typescript
// ui/user-form/user-form.component.ts
@Component({
  selector: 'one-ui-user-form'
})
export class UserFormComponent {
  private http = inject(HttpClient); // ❌ NO!

  onSubmit() {
    // ❌ NO! HTTP calls belong in domain layer
    this.http.post('/api/users', this.form.value).subscribe();
  }
}
```

#### ✅ Correct Code

```typescript
// ui/user-form/user-form.component.ts
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

// features/user-management-page/user-management-page.component.ts
@Component({
  template: `
    <one-ui-user-form (save)="onSave($event)" />
  `
})
export class UserManagementPageComponent {
  private store = inject(UserManagementStore);

  onSave(user: User) {
    this.store.createUser(user); // ✅ Features call store
  }
}
```

---

### ❌ Violation 5: Shared Component in Wrong Layer

Generic, reusable components belong in **UI layer**. Feature-specific components belong in **features layer**.

#### ❌ Wrong Placement

```
❌ libs/{scope}/shared/ui/user-management-page/      # Feature-specific in shared
❌ libs/{scope}/{feature}/features/generic-table/    # Generic in features
```

#### ✅ Correct Placement

```
✅ libs/{scope}/{feature}/ui/user-table/             # Generic in UI
✅ libs/{scope}/{feature}/features/user-page/        # Feature-specific in features
```

---

## Quick Reference: Layer Responsibilities

| Layer | Responsibilities | Can Inject | Cannot Inject |
|-------|------------------|------------|---------------|
| **UI** | Presentational components, forms, tables | FormBuilder, TranslocoService | Store, HttpClient, MatDialog |
| **Features** | Page components, dialogs, orchestration | Store, MatDialog, ViewContainerRef | HttpClient (use store) |
| **Domain** | Business logic, state, API services | HttpClient, MxRestService | Nothing from features/ui |
| **Shell** | Routing, layout | Store (for guards) | Business logic |

---

## Quick Reference: What Goes Where

| Component Type | Layer | Can Use Store? | Can Make HTTP Calls? |
|----------------|-------|----------------|---------------------|
| Page component | Features | ✅ Yes | ❌ No (use store) |
| Dialog | Features | ✅ Yes | ❌ No (use store) |
| Form component | UI | ❌ No | ❌ No |
| Table component | UI | ❌ No | ❌ No |
| Store | Domain | N/A | ✅ Yes (via API service) |
| API service | Domain | N/A | ✅ Yes |

---

## Related References

- [ddd-architecture.md](./ddd-architecture.md) - Complete DDD architecture guide
- [checklist.md](./checklist.md) - Pre-PR validation checklist
