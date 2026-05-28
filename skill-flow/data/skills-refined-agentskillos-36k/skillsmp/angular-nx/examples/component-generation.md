# Component Generation Examples

This guide shows how to generate Angular components in the Sentinel monorepo using Nx.

## Basic Component Generation

### Standalone Component (Default for Sentinel)

```bash
npx nx generate @angular/core:component \
  --name=my-component \
  --project=sentinel \
  --standalone=true
```

This generates:
```
apps/sentinel/src/app/
└── my-component/
    ├── my-component.component.ts
    ├── my-component.component.html
    ├── my-component.component.scss
    └── my-component.component.spec.ts
```

## Feature Components

For feature-specific components, specify a path:

```bash
npx nx generate @angular/core:component \
  --name=violation-list \
  --project=sentinel \
  --path=apps/sentinel/src/app/features/violations \
  --standalone=true
```

## Component with Signal Forms

When creating a component that needs forms:

```bash
npx nx generate @angular/core:component \
  --name=user-profile-form \
  --project=sentinel \
  --standalone=true
```

Then update the component to use Signal Forms:

```typescript
import { Component, signal } from '@angular/core';
import { Field, form } from '@angular/forms/signals';

@Component({
  selector: 'app-user-profile-form',
  standalone: true,
  imports: [Field],
  templateUrl: './user-profile-form.component.html',
})
export class UserProfileFormComponent {
  private readonly formState = signal({
    name: '',
    email: '',
  });

  protected readonly userForm = form(this.formState);

  protected submitForm() {
    console.log(this.userForm().value());
  }
}
```

See [signal-forms.md](signal-forms.md) for detailed form examples.

## Library Components

Generate a component in a shared library:

```bash
npx nx generate @angular/core:component \
  --name=custom-button \
  --project=ui-components \
  --standalone=true \
  --export=true
```

## Component Templates

### Modern Angular Component Template

```typescript
import { Component, inject, input, output, signal } from '@angular/core';

@Component({
  selector: 'app-my-component',
  standalone: true,
  imports: [],
  template: `
    <div>
      @if (isLoading()) {
        <p>Loading...</p>
      } @else {
        <h1>{{ title() }}</h1>
        @for (item of items(); track item.id) {
          <div>{{ item.name }}</div>
        }
      }
    </div>
  `,
})
export class MyComponent {
  // Inputs
  title = input.required<string>();
  items = input<Array<{id: string; name: string}>>([]);

  // Outputs
  itemClicked = output<string>();

  // State
  isLoading = signal(false);

  // Dependency injection
  private myService = inject(MyService);
}
```

### Key Patterns

1. **Use signals for state**: `signal()`, `computed()`, `effect()`
2. **Use inject() for DI**: Avoid constructor injection
3. **Input/Output decorators**: `input()`, `output()`
4. **Modern control flow**: `@if`, `@for`, `@switch` instead of structural directives
5. **Standalone**: Always set `standalone: true`

## Route Components

Components that serve as route targets:

```bash
npx nx generate @angular/core:component \
  --name=dashboard \
  --project=sentinel \
  --path=apps/sentinel/src/app/pages/dashboard \
  --standalone=true
```

Then configure the route:

```typescript
// app.routes.ts
export const routes: Routes = [
  {
    path: 'dashboard',
    loadComponent: () =>
      import('./pages/dashboard/dashboard.component')
        .then(m => m.DashboardComponent),
  },
];
```

## Testing Generated Components

Nx automatically generates a spec file. Update it for modern Angular:

```typescript
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { MyComponent } from './my-component.component';

describe('MyComponent', () => {
  let component: MyComponent;
  let fixture: ComponentFixture<MyComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MyComponent], // Import the standalone component
    }).compileComponents();

    fixture = TestBed.createComponent(MyComponent);
    component = fixture.componentInstance;

    // Set required inputs
    fixture.componentRef.setInput('title', 'Test Title');

    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
```

## Common Flags

- `--name`: Component name (required)
- `--project`: Target project (usually 'sentinel')
- `--standalone`: Generate standalone component (default: true for Angular 19)
- `--path`: Custom path for the component
- `--export`: Export from library index (for shared libraries)
- `--skip-tests`: Skip generating spec file
- `--inline-template`: Use inline template instead of separate HTML file
- `--inline-style`: Use inline styles instead of separate CSS/SCSS file

## Best Practices

1. **Always use `--standalone=true`** (or rely on default in Angular 19+)
2. **Organize by feature**: Place related components together
3. **Use descriptive names**: `violation-details` not `details`
4. **Follow naming conventions**: kebab-case for files, PascalCase for classes
5. **Keep components focused**: Single responsibility principle
6. **Leverage Nx generators**: Don't create files manually
