---
title: Use Typed Reactive Forms (v14+)
impact: MEDIUM
impactDescription: Compile-time type checking
tags: forms, typed-forms, typescript
---

## Use Typed Reactive Forms (v14+)

Angular 14+ provides strictly typed reactive forms. Use `NonNullableFormBuilder` for non-nullable controls and explicit types for better IDE support.

**Incorrect (Untyped form):**

```typescript
@Component({...})
export class ProfileComponent {
  form = new FormGroup({
    name: new FormControl(''),
    email: new FormControl(''),
    age: new FormControl(0)
  });

  onSubmit() {
    const value = this.form.value;
    // value is Partial<{name: string | null, ...}>
    // Type is loose, nullable, and partial
    console.log(value.nmae); // Typo not caught
  }
}
```

**Correct (Typed form with NonNullableFormBuilder):**

```typescript
interface ProfileForm {
  name: FormControl<string>;
  email: FormControl<string>;
  age: FormControl<number>;
}

@Component({
  template: `
    <form [formGroup]="form" (ngSubmit)="onSubmit()">
      <input formControlName="name" />
      <input formControlName="email" type="email" />
      <input formControlName="age" type="number" />
      <button [disabled]="form.invalid">Save</button>
    </form>
  `
})
export class ProfileComponent {
  form: FormGroup<ProfileForm>;

  constructor(private fb: NonNullableFormBuilder) {
    this.form = this.fb.group({
      name: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      age: [0, [Validators.required, Validators.min(0)]]
    });
  }

  onSubmit() {
    // getRawValue() returns fully typed, non-nullable object
    const value = this.form.getRawValue();
    // Type: { name: string; email: string; age: number }

    // Compile error: Property 'nmae' does not exist
    // console.log(value.nmae);

    this.saveProfile(value);
  }

  // Safe typed access
  get nameControl() {
    return this.form.controls.name; // FormControl<string>
  }
}
```

**Typed FormArray:**

```typescript
interface OrderForm {
  customer: FormControl<string>;
  items: FormArray<FormGroup<{
    product: FormControl<string>;
    quantity: FormControl<number>;
  }>>;
}

@Component({...})
export class OrderComponent {
  form: FormGroup<OrderForm>;

  constructor(private fb: NonNullableFormBuilder) {
    this.form = this.fb.group({
      customer: ['', Validators.required],
      items: this.fb.array([this.createItemGroup()])
    });
  }

  get itemsArray() {
    return this.form.controls.items;
  }

  createItemGroup() {
    return this.fb.group({
      product: ['', Validators.required],
      quantity: [1, Validators.min(1)]
    });
  }

  addItem() {
    this.itemsArray.push(this.createItemGroup());
  }
}
```

Reference: [Angular Typed Forms](https://v16.angular.io/guide/typed-forms)
