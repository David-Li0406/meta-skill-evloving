# Angular Forms Migration

Complete guide for migrating Angular Reactive Forms to react-hook-form with Zod validation.

## Quick Reference

| Angular Forms | react-hook-form |
|---------------|-----------------|
| `FormGroup` | `useForm()` |
| `FormControl` | `register()` |
| `FormArray` | `useFieldArray()` |
| `Validators.required` | `{ required: true }` or Zod |
| `formControlName` | `{...register('name')}` |
| `(ngSubmit)` | `handleSubmit()` |
| `form.valid` | `formState.isValid` |
| `form.dirty` | `formState.isDirty` |
| `form.touched` | `formState.touchedFields` |
| `form.errors` | `formState.errors` |
| `form.get('field')` | `watch('field')` or `getValues('field')` |
| `form.patchValue()` | `setValue()` / `reset()` |
| `valueChanges` | `watch()` with `useEffect` |

---

## Basic Form Migration

### Simple Login Form

**Before (Angular Reactive Forms)**:
```typescript
// login.component.ts
@Component({
  selector: 'app-login',
  templateUrl: './login.component.html'
})
export class LoginComponent implements OnInit {
  loginForm!: FormGroup;

  constructor(private fb: FormBuilder, private authService: AuthService) {}

  ngOnInit(): void {
    this.loginForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(8)]],
      rememberMe: [false]
    });
  }

  onSubmit(): void {
    if (this.loginForm.valid) {
      this.authService.login(this.loginForm.value).subscribe({
        next: () => this.router.navigate(['/dashboard']),
        error: (err) => this.errorMessage = err.message
      });
    }
  }
}
```

```html
<!-- login.component.html -->
<form [formGroup]="loginForm" (ngSubmit)="onSubmit()">
  <div>
    <label for="email">Email</label>
    <input id="email" formControlName="email" type="email" />
    <span *ngIf="loginForm.get('email')?.errors?.['required']">
      Email is required
    </span>
    <span *ngIf="loginForm.get('email')?.errors?.['email']">
      Invalid email format
    </span>
  </div>

  <div>
    <label for="password">Password</label>
    <input id="password" formControlName="password" type="password" />
    <span *ngIf="loginForm.get('password')?.errors?.['minlength']">
      Password must be at least 8 characters
    </span>
  </div>

  <div>
    <label>
      <input formControlName="rememberMe" type="checkbox" />
      Remember me
    </label>
  </div>

  <button type="submit" [disabled]="!loginForm.valid">Login</button>
</form>
```

**After (react-hook-form + Zod)**:
```typescript
// components/login-form.tsx
'use client'

import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { useRouter } from 'next/navigation'
import { useState } from 'react'

const loginSchema = z.object({
  email: z.string().email('Invalid email format'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
  rememberMe: z.boolean().default(false)
})

type LoginFormData = z.infer<typeof loginSchema>

export function LoginForm() {
  const router = useRouter()
  const [errorMessage, setErrorMessage] = useState('')

  const {
    register,
    handleSubmit,
    formState: { errors, isValid, isSubmitting }
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
    mode: 'onChange'
  })

  const onSubmit = async (data: LoginFormData) => {
    try {
      await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      })
      router.push('/dashboard')
    } catch (err) {
      setErrorMessage(err instanceof Error ? err.message : 'Login failed')
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <div>
        <label htmlFor="email">Email</label>
        <input id="email" type="email" {...register('email')} />
        {errors.email && <span>{errors.email.message}</span>}
      </div>

      <div>
        <label htmlFor="password">Password</label>
        <input id="password" type="password" {...register('password')} />
        {errors.password && <span>{errors.password.message}</span>}
      </div>

      <div>
        <label>
          <input type="checkbox" {...register('rememberMe')} />
          Remember me
        </label>
      </div>

      {errorMessage && <div className="error">{errorMessage}</div>}

      <button type="submit" disabled={!isValid || isSubmitting}>
        {isSubmitting ? 'Logging in...' : 'Login'}
      </button>
    </form>
  )
}
```

---

## FormArray → useFieldArray

### Dynamic Form Fields

**Before (Angular)**:
```typescript
// order-form.component.ts
@Component({...})
export class OrderFormComponent {
  orderForm = this.fb.group({
    customerName: ['', Validators.required],
    items: this.fb.array([])
  });

  get items(): FormArray {
    return this.orderForm.get('items') as FormArray;
  }

  addItem(): void {
    this.items.push(this.fb.group({
      name: ['', Validators.required],
      quantity: [1, [Validators.required, Validators.min(1)]],
      price: [0, [Validators.required, Validators.min(0)]]
    }));
  }

  removeItem(index: number): void {
    this.items.removeAt(index);
  }
}
```

```html
<!-- order-form.component.html -->
<form [formGroup]="orderForm">
  <input formControlName="customerName" placeholder="Customer Name" />

  <div formArrayName="items">
    <div *ngFor="let item of items.controls; let i = index" [formGroupName]="i">
      <input formControlName="name" placeholder="Item name" />
      <input formControlName="quantity" type="number" />
      <input formControlName="price" type="number" />
      <button type="button" (click)="removeItem(i)">Remove</button>
    </div>
  </div>

  <button type="button" (click)="addItem()">Add Item</button>
</form>
```

**After (react-hook-form useFieldArray)**:
```typescript
// components/order-form.tsx
'use client'

import { useForm, useFieldArray } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'

const orderSchema = z.object({
  customerName: z.string().min(1, 'Customer name is required'),
  items: z.array(z.object({
    name: z.string().min(1, 'Item name is required'),
    quantity: z.number().min(1, 'Quantity must be at least 1'),
    price: z.number().min(0, 'Price cannot be negative')
  })).min(1, 'At least one item is required')
})

type OrderFormData = z.infer<typeof orderSchema>

export function OrderForm() {
  const { register, control, handleSubmit, formState: { errors } } = useForm<OrderFormData>({
    resolver: zodResolver(orderSchema),
    defaultValues: {
      customerName: '',
      items: [{ name: '', quantity: 1, price: 0 }]
    }
  })

  const { fields, append, remove } = useFieldArray({
    control,
    name: 'items'
  })

  const onSubmit = (data: OrderFormData) => {
    console.log('Order:', data)
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input
        {...register('customerName')}
        placeholder="Customer Name"
      />
      {errors.customerName && <span>{errors.customerName.message}</span>}

      {fields.map((field, index) => (
        <div key={field.id}>
          <input
            {...register(`items.${index}.name`)}
            placeholder="Item name"
          />
          <input
            {...register(`items.${index}.quantity`, { valueAsNumber: true })}
            type="number"
          />
          <input
            {...register(`items.${index}.price`, { valueAsNumber: true })}
            type="number"
          />
          <button type="button" onClick={() => remove(index)}>
            Remove
          </button>
        </div>
      ))}

      <button
        type="button"
        onClick={() => append({ name: '', quantity: 1, price: 0 })}
      >
        Add Item
      </button>

      <button type="submit">Submit Order</button>
    </form>
  )
}
```

---

## Custom Validators → Zod Refinements

### Cross-Field Validation

**Before (Angular)**:
```typescript
// password-match.validator.ts
export function passwordMatchValidator(control: AbstractControl): ValidationErrors | null {
  const password = control.get('password');
  const confirmPassword = control.get('confirmPassword');

  if (password && confirmPassword && password.value !== confirmPassword.value) {
    return { passwordMismatch: true };
  }
  return null;
}

// register.component.ts
this.registerForm = this.fb.group({
  email: ['', [Validators.required, Validators.email]],
  password: ['', [Validators.required, Validators.minLength(8)]],
  confirmPassword: ['', Validators.required]
}, { validators: passwordMatchValidator });
```

**After (Zod refine)**:
```typescript
const registerSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8, 'Password must be at least 8 characters'),
  confirmPassword: z.string()
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ['confirmPassword']
})

// Usage in component
const { register, handleSubmit, formState: { errors } } = useForm({
  resolver: zodResolver(registerSchema)
})

// Error display
{errors.confirmPassword && <span>{errors.confirmPassword.message}</span>}
```

### Async Validation

**Before (Angular)**:
```typescript
// email-exists.validator.ts
@Injectable({ providedIn: 'root' })
export class EmailExistsValidator {
  constructor(private userService: UserService) {}

  validate(): AsyncValidatorFn {
    return (control: AbstractControl): Observable<ValidationErrors | null> => {
      return this.userService.checkEmail(control.value).pipe(
        map(exists => exists ? { emailExists: true } : null),
        catchError(() => of(null))
      );
    };
  }
}
```

**After (react-hook-form async validation)**:
```typescript
const registerSchema = z.object({
  email: z.string().email(),
  // ... other fields
})

export function RegisterForm() {
  const {
    register,
    handleSubmit,
    setError,
    formState: { errors }
  } = useForm({
    resolver: zodResolver(registerSchema)
  })

  const onSubmit = async (data: RegisterFormData) => {
    // Check email availability before submit
    const emailExists = await checkEmailExists(data.email)
    if (emailExists) {
      setError('email', {
        type: 'manual',
        message: 'This email is already registered'
      })
      return
    }
    // Proceed with registration
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('email')} />
      {errors.email && <span>{errors.email.message}</span>}
      {/* ... */}
    </form>
  )
}
```

---

## valueChanges → watch

### Reactive Field Changes

**Before (Angular)**:
```typescript
ngOnInit(): void {
  this.form.get('country')?.valueChanges.pipe(
    takeUntil(this.destroy$)
  ).subscribe(country => {
    this.loadCities(country);
    this.form.get('city')?.reset();
  });
}
```

**After (react-hook-form watch)**:
```typescript
'use client'

import { useForm } from 'react-hook-form'
import { useEffect } from 'react'
import useSWR from 'swr'

export function AddressForm() {
  const { register, watch, setValue, resetField } = useForm()

  const country = watch('country')

  // Load cities when country changes
  const { data: cities } = useSWR(
    country ? `/api/cities?country=${country}` : null,
    fetcher
  )

  // Reset city when country changes
  useEffect(() => {
    if (country) {
      resetField('city')
    }
  }, [country, resetField])

  return (
    <form>
      <select {...register('country')}>
        <option value="">Select Country</option>
        <option value="us">United States</option>
        <option value="uk">United Kingdom</option>
      </select>

      <select {...register('city')} disabled={!country}>
        <option value="">Select City</option>
        {cities?.map(city => (
          <option key={city.id} value={city.id}>{city.name}</option>
        ))}
      </select>
    </form>
  )
}
```

---

## Form State Management

### Form State Comparison

| Angular | react-hook-form |
|---------|-----------------|
| `form.valid` | `formState.isValid` |
| `form.invalid` | `!formState.isValid` |
| `form.dirty` | `formState.isDirty` |
| `form.pristine` | `!formState.isDirty` |
| `form.touched` | `formState.touchedFields` |
| `form.pending` | `formState.isValidating` |
| `form.submitted` | `formState.isSubmitted` |

### Complete Form State Example

```typescript
export function FormWithState() {
  const {
    register,
    handleSubmit,
    formState: {
      errors,
      isDirty,
      isValid,
      isSubmitting,
      isSubmitted,
      isSubmitSuccessful,
      touchedFields,
      dirtyFields
    },
    reset
  } = useForm<FormData>({
    mode: 'onChange' // Validate on change like Angular
  })

  // Reset form after successful submit
  useEffect(() => {
    if (isSubmitSuccessful) {
      reset()
    }
  }, [isSubmitSuccessful, reset])

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      {/* Form fields */}

      {/* Show unsaved changes warning */}
      {isDirty && <div>You have unsaved changes</div>}

      {/* Disable submit until valid and not submitting */}
      <button
        type="submit"
        disabled={!isValid || isSubmitting}
      >
        {isSubmitting ? 'Submitting...' : 'Submit'}
      </button>

      {/* Reset button */}
      <button type="button" onClick={() => reset()} disabled={!isDirty}>
        Reset
      </button>
    </form>
  )
}
```

---

## Integration with shadcn/ui

### Form with shadcn/ui Components

```typescript
// components/contact-form.tsx
'use client'

import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage
} from '@/components/ui/form'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'

const contactSchema = z.object({
  name: z.string().min(2, 'Name must be at least 2 characters'),
  email: z.string().email('Invalid email address'),
  message: z.string().min(10, 'Message must be at least 10 characters')
})

type ContactFormData = z.infer<typeof contactSchema>

export function ContactForm() {
  const form = useForm<ContactFormData>({
    resolver: zodResolver(contactSchema),
    defaultValues: {
      name: '',
      email: '',
      message: ''
    }
  })

  const onSubmit = async (data: ContactFormData) => {
    console.log('Form data:', data)
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        <FormField
          control={form.control}
          name="name"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Name</FormLabel>
              <FormControl>
                <Input placeholder="Your name" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="email"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Email</FormLabel>
              <FormControl>
                <Input type="email" placeholder="your@email.com" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="message"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Message</FormLabel>
              <FormControl>
                <textarea
                  className="flex min-h-[80px] w-full rounded-md border px-3 py-2"
                  placeholder="Your message..."
                  {...field}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <Button type="submit" disabled={form.formState.isSubmitting}>
          {form.formState.isSubmitting ? 'Sending...' : 'Send Message'}
        </Button>
      </form>
    </Form>
  )
}
```

---

Version: 1.0.0
Source: jikime-migration-angular-to-nextjs SKILL.md
