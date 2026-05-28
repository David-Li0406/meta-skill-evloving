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

      <div *ngIf="userForm.controls['password']?.value !== userForm.controls['confirmPassword']?.value">
        Passwords don't match
      </div>
    </form>
  `
})
export class RegisterComponent {
  user = { email: '', password: '', confirmPassword: '' };
}
```

**Correct (Reactive form with FormBuilder):**

```typescript
@Component({
  template: `
    <form [formGroup]="form" (ngSubmit)="onSubmit()">
      <input formControlName="email" />
      <input type="password" formControlName="password" />
      <input type="password" formControlName="confirmPassword" />

      <div *ngIf="form.errors?.['passwordMismatch']" class="error">
        Passwords don't match
      </div>

      <button [disabled]="form.invalid">Submit</button>
    </form>
  `,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class RegisterComponent implements OnInit {
  form!: FormGroup;

  constructor(private fb: FormBuilder) {}

  ngOnInit() {
    this.form = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(8)]],
      confirmPassword: ['', Validators.required]
    }, {
      validators: [this.passwordMatchValidator]
    });
  }

  passwordMatchValidator(group: FormGroup): ValidationErrors | null {
    const password = group.get('password')?.value;
    const confirm = group.get('confirmPassword')?.value;
    return password === confirm ? null : { passwordMismatch: true };
  }
}
```

**Why it matters:**
- Cross-field validation in component logic
- Synchronous access to form state
- Easy to test without template
- Works well with OnPush change detection

Reference: [Angular Reactive Forms](https://v16.angular.io/guide/reactive-forms)
