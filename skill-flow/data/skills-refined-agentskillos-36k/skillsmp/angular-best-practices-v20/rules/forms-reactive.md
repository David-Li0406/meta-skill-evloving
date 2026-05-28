---
title: Use Reactive Forms for Complex Forms
impact: MEDIUM
impactDescription: Better testability, synchronous access
tags: forms, reactive-forms, validation
---

## Use Reactive Forms for Complex Forms

Reactive forms provide synchronous access to form state, making them easier to test and offering better control over validation.

**Incorrect (Template-driven with complex validation):**

```typescript
@Component({
  template: `
    <form #userForm="ngForm" (ngSubmit)="onSubmit()">
      <input [(ngModel)]="user.email" name="email" required email />
      <input [(ngModel)]="user.password" name="password" required />
      <input [(ngModel)]="user.confirmPassword" name="confirmPassword" />

      <!-- Complex validation in template -->
      @if (userForm.controls['password']?.value !== userForm.controls['confirmPassword']?.value) {
        <div>Passwords don't match</div>
      }
    </form>
  `
})
export class RegisterComponent {
  user = { email: '', password: '', confirmPassword: '' };
}
```

**Correct (Reactive form with typed controls):**

```typescript
@Component({
  imports: [ReactiveFormsModule],
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <form [formGroup]="form" (ngSubmit)="onSubmit()">
      <input formControlName="email" />
      <input type="password" formControlName="password" />
      <input type="password" formControlName="confirmPassword" />

      @if (form.errors?.['passwordMismatch']) {
        <span class="error">Passwords don't match</span>
      }

      <button [disabled]="form.invalid">Submit</button>
    </form>
  `
})
export class RegisterComponent {
  private fb = inject(NonNullableFormBuilder);

  form = this.fb.group({
    email: ['', [Validators.required, Validators.email]],
    password: ['', [Validators.required, Validators.minLength(8)]],
    confirmPassword: ['', Validators.required]
  }, {
    validators: [this.passwordMatchValidator]
  });

  passwordMatchValidator(group: FormGroup): ValidationErrors | null {
    const password = group.get('password')?.value;
    const confirm = group.get('confirmPassword')?.value;
    return password === confirm ? null : { passwordMismatch: true };
  }

  onSubmit() {
    if (this.form.valid) {
      const { email, password } = this.form.getRawValue();
    }
  }
}
```

**Why it matters:**
- Typed form values with `NonNullableFormBuilder`
- Cross-field validation in component logic
- Synchronous access to form state
- Easy to test without template

Reference: [Angular Reactive Forms](https://angular.dev/guide/forms/reactive-forms)
