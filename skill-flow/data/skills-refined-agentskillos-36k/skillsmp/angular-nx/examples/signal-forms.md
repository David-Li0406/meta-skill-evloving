# Signal Forms Examples

Angular 19 introduces Signal-based forms (`@angular/forms/signals`) as the modern approach to form handling. These examples show how to use Signal Forms in the Sentinel project.

## Basic Signal Form Example

From [login.component.ts](../../../sentinel-frontend/libs/shared/login/src/lib/login/login.component.ts):

```typescript
import { Component, signal } from '@angular/core';
import { Field, form } from '@angular/forms/signals';

@Component({
  selector: 'lib-login',
  standalone: true,
  imports: [Field],
  templateUrl: './login.component.html',
})
export class LoginComponent {
  // Define the initial form state
  private readonly initialLoginFormValue = {
    email: '',
  };

  // Create a signal to hold the form state
  private readonly loginFormState = signal(this.initialLoginFormValue);

  // Create the form from the signal
  protected readonly loginForm = form(this.loginFormState);

  // Access form values
  protected submitForm(e: Event) {
    e.preventDefault();
    const formValue = this.loginForm().value();
    // Use formValue...
  }
}
```

## Template Usage

Use the `Field` component in your template:

```html
<form (submit)="submitForm($event)">
  <Field [name]="'email'" [form]="loginForm()">
    <label>Email</label>
    <input type="email" placeholder="Enter your email" />
  </Field>

  <button type="submit">Submit</button>
</form>
```

## Key Concepts

### 1. Signal State
```typescript
// Form state is managed with signals
private readonly formState = signal<MyFormType>({
  field1: '',
  field2: ''
});
```

### 2. Form Creation
```typescript
// Create form from signal state
protected readonly myForm = form(this.formState);
```

### 3. Accessing Values
```typescript
// Get current form value
const currentValue = this.myForm().value();

// React to form changes with effects
effect(() => {
  console.log('Form changed:', this.myForm().value());
});
```

## Benefits of Signal Forms

1. **Reactive by default**: Leverage Angular's signal-based reactivity
2. **Better performance**: Automatic change detection optimization
3. **Type safety**: Full TypeScript support
4. **Simpler API**: Less boilerplate than traditional forms
5. **Modern pattern**: Aligns with Angular 19+ best practices

## Migration from Traditional Forms

**Old approach (FormControl/FormGroup):**
```typescript
// ❌ Don't use this in new code
loginForm = new FormGroup({
  email: new FormControl(''),
  password: new FormControl('')
});
```

**New approach (Signal Forms):**
```typescript
// ✅ Use this pattern
private readonly loginFormState = signal({
  email: '',
  password: ''
});
protected readonly loginForm = form(this.loginFormState);
```

## Additional Resources

- See [login.component.ts](../../../sentinel-frontend/libs/shared/login/src/lib/login/login.component.ts) for a complete working example
- Angular Signal Forms documentation: https://angular.dev/guide/forms/signals
