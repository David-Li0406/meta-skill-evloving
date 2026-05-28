---
title: Form Patterns (react-hook-form + zod)
impact: MEDIUM
impactDescription: Type-safe form handling - ensures validation consistency, reduces boilerplate, improves DX
tags: react-hook-form, zod, forms, validation, typescript
---

# Form Patterns (react-hook-form + zod) (MEDIUM)

Type-safe form handling patterns using react-hook-form with zod validation.

## Rule 1: Zod Schema Definition

**Define schemas with proper validation messages:**

```typescript
// ❌ INCORRECT - no validation messages
const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
})

// ✅ CORRECT - with translated messages
const schema = z.object({
  email: z.string()
    .min(1, t('validation.required'))
    .email(t('validation.invalidEmail')),
  password: z.string()
    .min(8, t('validation.minLength', { min: 8 })),
})

// ✅ BETTER - schema factory for i18n
const createUserSchema = (t: TFunction) => z.object({
  email: z.string()
    .min(1, t('validation.required'))
    .email(t('validation.invalidEmail')),
  name: z.string()
    .min(2, t('validation.minLength', { min: 2 }))
    .max(100, t('validation.maxLength', { max: 100 })),
})
```

## Rule 2: useForm with zodResolver

**Always use zodResolver for type inference:**

```typescript
// ❌ INCORRECT - manual validation
const { register, handleSubmit } = useForm()

const onSubmit = (data) => {
  if (!data.email) { /* manual check */ }
}

// ✅ CORRECT - zod resolver with type inference
import { zodResolver } from '@hookform/resolvers/zod'

const schema = z.object({
  email: z.string().email(),
  name: z.string().min(2),
})

type FormData = z.infer<typeof schema>

function MyForm() {
  const form = useForm<FormData>({
    resolver: zodResolver(schema),
    defaultValues: {
      email: '',
      name: '',
    },
  })

  const onSubmit = (data: FormData) => {
    // data is fully typed
  }

  return (
    <form onSubmit={form.handleSubmit(onSubmit)}>
      {/* ... */}
    </form>
  )
}
```

## Rule 3: Error Display Pattern

**Consistently display field errors:**

```typescript
// ❌ INCORRECT - inconsistent error handling
<input {...register('email')} />
{errors.email && <span>{errors.email.message}</span>}

// ✅ CORRECT - consistent pattern with styling
<div className="space-y-1">
  <Label htmlFor="email">{t('users.email')}</Label>
  <Input
    id="email"
    {...register('email')}
    className={errors.email ? 'border-destructive' : ''}
  />
  {errors.email && (
    <p className="text-sm text-destructive">{errors.email.message}</p>
  )}
</div>

// ✅ BETTER - FormField component (with Radix/shadcn)
<FormField
  control={form.control}
  name="email"
  render={({ field }) => (
    <FormItem>
      <FormLabel>{t('users.email')}</FormLabel>
      <FormControl>
        <Input {...field} />
      </FormControl>
      <FormMessage />
    </FormItem>
  )}
/>
```

## Rule 4: Form Submission with Mutation

**Integrate with TanStack Query mutations:**

```typescript
// ✅ CORRECT - form with mutation
function CreateUserForm({ onSuccess }: { onSuccess?: () => void }) {
  const { t } = useTranslation()
  const createUser = useCreateUser()

  const form = useForm<CreateUserInput>({
    resolver: zodResolver(createUserSchema),
  })

  const onSubmit = async (data: CreateUserInput) => {
    try {
      await createUser.mutateAsync(data)
      toast.success(t('users.createSuccess'))
      form.reset()
      onSuccess?.()
    } catch (error) {
      toast.error(t('common.error'))
    }
  }

  return (
    <form onSubmit={form.handleSubmit(onSubmit)}>
      {/* form fields */}
      <Button
        type="submit"
        disabled={createUser.isPending}
      >
        {createUser.isPending ? t('common.loading') : t('common.save')}
      </Button>
    </form>
  )
}
```

## Rule 5: Default Values from Server

**Handle async default values properly:**

```typescript
// ❌ INCORRECT - defaultValues won't update after mount
function EditUserForm({ userId }: { userId: string }) {
  const { data: user } = useQuery(...)

  const form = useForm({
    defaultValues: {
      name: user?.name || '', // Won't update when user loads
    },
  })
}

// ✅ CORRECT - use reset() when data loads
function EditUserForm({ userId }: { userId: string }) {
  const { data: user } = useQuery({
    queryKey: userKeys.detail(userId),
    queryFn: () => getUser(userId),
  })

  const form = useForm<UpdateUserInput>({
    resolver: zodResolver(updateUserSchema),
  })

  // Reset form when user data loads
  useEffect(() => {
    if (user) {
      form.reset({
        name: user.name,
        email: user.email,
      })
    }
  }, [user, form.reset])

  // ...
}
```

## Rule 6: Conditional Fields

**Handle conditional validation with zod:**

```typescript
// ✅ CORRECT - conditional validation
const schema = z.discriminatedUnion('type', [
  z.object({
    type: z.literal('individual'),
    name: z.string().min(2),
  }),
  z.object({
    type: z.literal('company'),
    companyName: z.string().min(2),
    registrationNumber: z.string().min(10),
  }),
])

// Or with refine
const schema = z.object({
  hasCompany: z.boolean(),
  companyName: z.string().optional(),
}).refine(
  (data) => !data.hasCompany || (data.hasCompany && data.companyName),
  { message: t('validation.required'), path: ['companyName'] }
)
```

## Rule 7: Array Fields

**Handle dynamic array fields:**

```typescript
// ✅ CORRECT - useFieldArray pattern
const schema = z.object({
  items: z.array(z.object({
    name: z.string().min(1),
    quantity: z.number().min(1),
  })).min(1, t('validation.minItems', { min: 1 })),
})

function OrderForm() {
  const form = useForm<FormData>({
    resolver: zodResolver(schema),
    defaultValues: {
      items: [{ name: '', quantity: 1 }],
    },
  })

  const { fields, append, remove } = useFieldArray({
    control: form.control,
    name: 'items',
  })

  return (
    <form>
      {fields.map((field, index) => (
        <div key={field.id}>
          <Input {...form.register(`items.${index}.name`)} />
          <Input
            type="number"
            {...form.register(`items.${index}.quantity`, { valueAsNumber: true })}
          />
          <Button onClick={() => remove(index)}>Remove</Button>
        </div>
      ))}
      <Button onClick={() => append({ name: '', quantity: 1 })}>
        Add Item
      </Button>
    </form>
  )
}
```

## Rule 8: Form State Indicators

**Show form state to users:**

```typescript
// ✅ CORRECT - use form state for UX
function MyForm() {
  const form = useForm<FormData>({...})
  const { isDirty, isValid, isSubmitting } = form.formState

  return (
    <form onSubmit={form.handleSubmit(onSubmit)}>
      {/* fields */}

      <div className="flex gap-2">
        <Button
          type="button"
          variant="outline"
          onClick={() => form.reset()}
          disabled={!isDirty || isSubmitting}
        >
          {t('common.reset')}
        </Button>
        <Button
          type="submit"
          disabled={!isDirty || !isValid || isSubmitting}
        >
          {isSubmitting ? <Spinner /> : t('common.save')}
        </Button>
      </div>
    </form>
  )
}
```

## Compliance Checklist

Before submitting code:

- [ ] Zod schema with i18n validation messages
- [ ] useForm with zodResolver
- [ ] Type inference from schema (`z.infer<typeof schema>`)
- [ ] Consistent error display pattern
- [ ] Form integrated with mutations
- [ ] Loading/disabled states on submit button
- [ ] Toast notifications for success/error
