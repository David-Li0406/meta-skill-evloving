# Form Validation with vee-validate and Zod

Complete guide for implementing forms with vee-validate and Zod schemas. **All forms MUST use this pattern.**

## Core Principle

**Every form in this application MUST use vee-validate with Zod schemas for validation.** Never create forms without proper schema validation.

## Why This Stack?

1. **Type Safety**: Zod schemas provide compile-time type safety
2. **Runtime Validation**: Client-side validation before API calls
3. **Reusability**: Schemas can be shared between client and server
4. **Accessibility**: vee-validate provides built-in error handling and ARIA attributes
5. **Developer Experience**: Clear, declarative validation rules

## Basic Form Pattern

```vue
<script setup lang="ts">
import { toTypedSchema } from '@vee-validate/zod'
import { z } from 'zod'
import { useForm } from 'vee-validate'

// 1. Define Zod schema
const formSchema = toTypedSchema(z.object({
  name: z.string().min(2, 'Name must be at least 2 characters').max(50),
  email: z.email('Invalid email address'),
}))

// 2. Initialize form with schema
const { handleSubmit, isSubmitting } = useForm({
  validationSchema: formSchema,
})

// 3. Define submit handler
const onSubmit = handleSubmit(async (values) => {
  // Values are already validated and typed
  console.log('Form values:', values)

  // Make API call
  const result = await $fetchResult('/api/users', {
    method: 'POST',
    body: values,
  })

  if (result.success) {
    toast.success({ title: 'Success!', description: 'User created.' })
  }
})
</script>

<template>
  <form @submit="onSubmit" class="space-y-4">
    <UIFormField v-slot="{ componentField }" name="name">
      <UIFormItem>
        <UIFormLabel>Name</UIFormLabel>
        <UIFormControl>
          <UIInput type="text" placeholder="Enter name" v-bind="componentField" />
        </UIFormControl>
        <UIFormDescription>This is your display name.</UIFormDescription>
        <UIFormMessage />
      </UIFormItem>
    </UIFormField>

    <UIFormField v-slot="{ componentField }" name="email">
      <UIFormItem>
        <UIFormLabel>Email</UIFormLabel>
        <UIFormControl>
          <UIInput type="email" placeholder="Enter email" v-bind="componentField" />
        </UIFormControl>
        <UIFormMessage />
      </UIFormItem>
    </UIFormField>

    <UIButton type="submit" :disabled="isSubmitting">
      {{ isSubmitting ? 'Submitting...' : 'Submit' }}
    </UIButton>
  </form>
</template>
```

## Form Component Structure

### UIFormField
Wraps individual form fields. Requires `v-slot="{ componentField }"` and `name` prop.

```vue
<UIFormField v-slot="{ componentField }" name="fieldName">
  <!-- Form item content -->
</UIFormField>
```

The `componentField` contains:
- `value`: Current field value
- `onBlur`: Blur event handler
- `onChange`: Change event handler
- Error state and messages

### UIFormItem
Container for label, control, description, and error messages.

### UIFormLabel
The field label. Automatically associated with the input via `for` attribute.

### UIFormControl
Wraps the actual input component. Required for proper error styling and accessibility.

### UIFormDescription
Optional help text displayed below the input.

### UIFormMessage
Displays validation error messages. Automatically shown/hidden based on validation state.

## Common Zod Validation Patterns

### String Validation

```typescript
const schema = z.object({
  // Required string
  name: z.string().min(1, 'Name is required'),

  // String with length constraints
  username: z.string().min(3).max(20),

  // Email
  email: z.email('Invalid email address'),

  // URL
  website: z.url('Invalid URL'),

  // Optional string
  bio: z.string().optional(),

  // String with default value
  title: z.string().default('Untitled'),

  // String with regex
  phoneNumber: z.string().regex(/^\d{3}-\d{3}-\d{4}$/, 'Format: XXX-XXX-XXXX'),
})
```

### Number Validation

```typescript
const schema = z.object({
  // Required number
  age: z.number().min(0).max(120),

  // Positive number
  weight: z.number().positive('Weight must be positive'),

  // Integer
  reps: z.number().int('Must be a whole number'),

  // Number with coercion (for form inputs that return strings)
  sets: z.coerce.number().int().min(1).max(10),

  // Optional number
  restTime: z.number().optional(),
})
```

### Boolean Validation

```typescript
const schema = z.object({
  // Required boolean
  termsAccepted: z.boolean().refine(val => val === true, {
    message: 'You must accept the terms',
  }),

  // Optional boolean
  newsletter: z.boolean().optional(),

  // Boolean with default
  isPublic: z.boolean().default(false),
})
```

### Date Validation

```typescript
const schema = z.object({
  // Date string
  dateOfBirth: z.iso.datetime(),

  // Date with min/max
  targetDate: z.iso.datetime().refine(
    (date) => new Date(date) > new Date(),
    { message: 'Target date must be in the future' }
  ),

  // Optional date
  completedAt: z.iso.datetime().optional(),
})
```

### Array Validation

```typescript
const schema = z.object({
  // Array of strings
  tags: z.array(z.string()).min(1, 'At least one tag is required'),

  // Array with max length
  categories: z.array(z.string()).max(5, 'Maximum 5 categories'),

  // Optional array
  notes: z.array(z.string()).optional(),

  // Array with default
  roles: z.array(z.string()).default(['user']),
})
```

### Enum Validation

```typescript
const schema = z.object({
  // Enum (use union instead of TypeScript enum)
  status: z.enum(['active', 'inactive', 'pending']),

  // With custom error message
  role: z.enum(['admin', 'user', 'guest'], {
    errorMap: () => ({ message: 'Invalid role selected' }),
  }),
})
```

### Object Validation

```typescript
const schema = z.object({
  // Nested object
  address: z.object({
    street: z.string().min(1),
    city: z.string().min(1),
    zipCode: z.string().regex(/^\d{5}$/),
  }),

  // Optional nested object
  settings: z.object({
    notifications: z.boolean(),
    theme: z.enum(['light', 'dark']),
  }).optional(),
})
```

## Form with Select Input

```vue
<script setup lang="ts">
import { toTypedSchema } from '@vee-validate/zod'
import { z } from 'zod'
import { useForm } from 'vee-validate'

const formSchema = toTypedSchema(z.object({
  exerciseType: z.enum(['strength', 'cardio', 'flexibility']),
  difficulty: z.enum(['beginner', 'intermediate', 'advanced']),
}))

const { handleSubmit } = useForm({ validationSchema: formSchema })

const onSubmit = handleSubmit((values) => {
  console.log(values)
})
</script>

<template>
  <form @submit="onSubmit" class="space-y-4">
    <UIFormField v-slot="{ componentField }" name="exerciseType">
      <UIFormItem>
        <UIFormLabel>Exercise Type</UIFormLabel>
        <UIFormControl>
          <UISelect v-bind="componentField">
            <UISelectTrigger>
              <UISelectValue placeholder="Select type" />
            </UISelectTrigger>
            <UISelectContent>
              <UISelectItem value="strength">Strength</UISelectItem>
              <UISelectItem value="cardio">Cardio</UISelectItem>
              <UISelectItem value="flexibility">Flexibility</UISelectItem>
            </UISelectContent>
          </UISelect>
        </UIFormControl>
        <UIFormMessage />
      </UIFormItem>
    </UIFormField>

    <UIButton type="submit">Submit</UIButton>
  </form>
</template>
```

## Form with Textarea

```vue
<script setup lang="ts">
const formSchema = toTypedSchema(z.object({
  description: z.string().min(10).max(500),
}))

const { handleSubmit } = useForm({ validationSchema: formSchema })
</script>

<template>
  <form @submit="handleSubmit(onSubmit)">
    <UIFormField v-slot="{ componentField }" name="description">
      <UIFormItem>
        <UIFormLabel>Description</UIFormLabel>
        <UIFormControl>
          <UITextarea
            placeholder="Enter description"
            rows="4"
            v-bind="componentField"
          />
        </UIFormControl>
        <UIFormDescription>
          Provide a detailed description (10-500 characters).
        </UIFormDescription>
        <UIFormMessage />
      </UIFormItem>
    </UIFormField>

    <UIButton type="submit">Submit</UIButton>
  </form>
</template>
```

## Form with Checkbox

```vue
<script setup lang="ts">
const formSchema = toTypedSchema(z.object({
  acceptTerms: z.boolean().refine(val => val === true, {
    message: 'You must accept the terms and conditions',
  }),
  newsletter: z.boolean().default(false),
}))

const { handleSubmit } = useForm({ validationSchema: formSchema })
</script>

<template>
  <form @submit="handleSubmit(onSubmit)" class="space-y-4">
    <UIFormField v-slot="{ componentField }" name="acceptTerms">
      <UIFormItem class="flex items-start gap-3">
        <UIFormControl>
          <UICheckbox v-bind="componentField" />
        </UIFormControl>
        <div class="space-y-1 leading-none">
          <UIFormLabel>Accept Terms and Conditions</UIFormLabel>
          <UIFormDescription>
            You agree to our Terms of Service and Privacy Policy.
          </UIFormDescription>
          <UIFormMessage />
        </div>
      </UIFormItem>
    </UIFormField>

    <UIFormField v-slot="{ componentField }" name="newsletter">
      <UIFormItem class="flex items-center gap-3">
        <UIFormControl>
          <UICheckbox v-bind="componentField" />
        </UIFormControl>
        <UIFormLabel>Subscribe to newsletter</UIFormLabel>
      </UIFormItem>
    </UIFormField>

    <UIButton type="submit">Submit</UIButton>
  </form>
</template>
```

## Form with Dynamic Fields

```vue
<script setup lang="ts">
import { useFieldArray } from 'vee-validate'

const formSchema = toTypedSchema(z.object({
  exercises: z.array(z.object({
    name: z.string().min(1),
    sets: z.coerce.number().int().min(1),
    reps: z.coerce.number().int().min(1),
  })).min(1, 'At least one exercise is required'),
}))

const { handleSubmit } = useForm({ validationSchema: formSchema })

const { fields, push, remove } = useFieldArray('exercises')

function addExercise() {
  push({ name: '', sets: 3, reps: 10 })
}
</script>

<template>
  <form @submit="handleSubmit(onSubmit)" class="space-y-4">
    <div v-for="(field, index) in fields" :key="field.key" class="space-y-2">
      <UIFormField v-slot="{ componentField }" :name="`exercises[${index}].name`">
        <UIFormItem>
          <UIFormLabel>Exercise Name</UIFormLabel>
          <UIFormControl>
            <UIInput v-bind="componentField" />
          </UIFormControl>
          <UIFormMessage />
        </UIFormItem>
      </UIFormField>

      <div class="flex gap-2">
        <UIFormField v-slot="{ componentField }" :name="`exercises[${index}].sets`">
          <UIFormItem class="flex-1">
            <UIFormLabel>Sets</UIFormLabel>
            <UIFormControl>
              <UIInput type="number" v-bind="componentField" />
            </UIFormControl>
            <UIFormMessage />
          </UIFormItem>
        </UIFormField>

        <UIFormField v-slot="{ componentField }" :name="`exercises[${index}].reps`">
          <UIFormItem class="flex-1">
            <UIFormLabel>Reps</UIFormLabel>
            <UIFormControl>
              <UIInput type="number" v-bind="componentField" />
            </UIFormControl>
            <UIFormMessage />
          </UIFormItem>
        </UIFormField>
      </div>

      <UIButton
        type="button"
        variant="destructive"
        size="sm"
        @click="remove(index)"
      >
        Remove
      </UIButton>
    </div>

    <UIButton type="button" variant="outline" @click="addExercise">
      Add Exercise
    </UIButton>

    <UIButton type="submit">Submit</UIButton>
  </form>
</template>
```

## Form Component Pattern

Forms should be self-contained components that emit events:

```vue
<!-- components/Goal/Form/Create.vue -->
<script setup lang="ts">
import { toTypedSchema } from '@vee-validate/zod'
import { z } from 'zod'
import { useForm } from 'vee-validate'

const emit = defineEmits<{
  created: [goal: Goal]
  cancelled: []
}>()

const formSchema = toTypedSchema(z.object({
  title: z.string().min(1).max(100),
  goalType: z.enum(['pr', 'volume', 'consistency']),
  targetValue: z.coerce.number().positive(),
  targetUnit: z.string(),
  targetDate: z.iso.datetime(),
}))

const { handleSubmit, isSubmitting } = useForm({ validationSchema: formSchema })

const onSubmit = handleSubmit(async (values) => {
  const result = await $fetchResult('/api/goals', {
    method: 'POST',
    body: values,
  })

  if (result.success) {
    emit('created', result.data)
  }
  else {
    toast.error({
      title: 'Error',
      description: result.error.message,
    })
  }
})
</script>

<template>
  <form @submit="onSubmit" class="space-y-4">
    <!-- Form fields -->

    <div class="flex gap-2">
      <UIButton type="submit" :disabled="isSubmitting">
        {{ isSubmitting ? 'Creating...' : 'Create Goal' }}
      </UIButton>
      <UIButton type="button" variant="outline" @click="emit('cancelled')">
        Cancel
      </UIButton>
    </div>
  </form>
</template>
```

**Usage in parent component:**

```vue
<template>
  <UIDialog v-slot="{ close }">
    <UIDialogTrigger as-child>
      <UIButton>Create Goal</UIButton>
    </UIDialogTrigger>
    <UIDialogContent>
      <UIDialogHeader>
        <UIDialogTitle>Create New Goal</UIDialogTitle>
      </UIDialogHeader>
      <GoalFormCreate
        @created="(goal) => { handleCreated(goal); close(); }"
        @cancelled="close"
      />
    </UIDialogContent>
  </UIDialog>
</template>
```

## Schema Reusability

Schemas can be reused and extended:

```typescript
// shared/schemas/workout.ts
import { z } from 'zod'

// Base schema
export const baseWorkoutSchema = z.object({
  name: z.string().min(1).max(100),
  description: z.string().max(500).optional(),
  isPublic: z.boolean().default(false),
})

// Create schema (extends base)
export const createWorkoutSchema = baseWorkoutSchema.extend({
  exercises: z.array(z.uuid()).min(1),
})

// Update schema (partial)
export const updateWorkoutSchema = baseWorkoutSchema.partial()
```

**Usage in components:**

```vue
<script setup lang="ts">
import { toTypedSchema } from '@vee-validate/zod'
import { createWorkoutSchema } from '~/shared/schemas/workout'

const formSchema = toTypedSchema(createWorkoutSchema)
</script>
```

## Custom Validation Rules

```typescript
const schema = z.object({
  // Custom refinement
  password: z.string().min(8).refine(
    (val) => /[A-Z]/.test(val) && /[a-z]/.test(val) && /[0-9]/.test(val),
    { message: 'Password must contain uppercase, lowercase, and number' }
  ),

  // Conditional validation
  otherExercise: z.string().optional(),
}).refine(
  (data) => {
    if (data.exerciseType === 'other') {
      return data.otherExercise && data.otherExercise.length > 0
    }
    return true
  },
  {
    message: 'Please specify the exercise name',
    path: ['otherExercise'],
  }
)

// Dependent fields
const schema = z.object({
  password: z.string().min(8),
  confirmPassword: z.string(),
}).refine(
  (data) => data.password === data.confirmPassword,
  {
    message: 'Passwords do not match',
    path: ['confirmPassword'],
  }
)
```

## Loading States

```vue
<script setup lang="ts">
const { handleSubmit, isSubmitting } = useForm({ validationSchema: formSchema })
</script>

<template>
  <form @submit="handleSubmit(onSubmit)">
    <!-- Form fields -->

    <UIButton type="submit" :disabled="isSubmitting">
      <Icon v-if="isSubmitting" name="i-lucide-loader-2" class="mr-2 h-4 w-4 animate-spin" />
      {{ isSubmitting ? 'Submitting...' : 'Submit' }}
    </UIButton>
  </form>
</template>
```

## Error Handling

```vue
<script setup lang="ts">
const onSubmit = handleSubmit(async (values) => {
  const result = await $fetchResult('/api/endpoint', {
    method: 'POST',
    body: values,
  })

  if (!result.success) {
    // Show error toast
    toast.error({
      title: 'Error',
      description: result.error.message,
    })
    return
  }

  // Success
  toast.success({ title: 'Success!', description: 'Item created.' })
  emit('created', result.data)
})
</script>
```

## Common Mistakes to Avoid

### ❌ Mistake 1: Not using toTypedSchema

```typescript
// ❌ Wrong: Zod schema directly
const { handleSubmit } = useForm({ validationSchema: z.object({...}) })

// ✅ Correct: Wrapped with toTypedSchema
const formSchema = toTypedSchema(z.object({...}))
const { handleSubmit } = useForm({ validationSchema: formSchema })
```

### ❌ Mistake 2: Not binding componentField

```vue
<!-- ❌ Wrong: Manual v-model -->
<UIInput v-model="name" />

<!-- ✅ Correct: Bind componentField -->
<UIFormField v-slot="{ componentField }" name="name">
  <UIFormControl>
    <UIInput v-bind="componentField" />
  </UIFormControl>
</UIFormField>
```

### ❌ Mistake 3: Wrapping in try/catch

```vue
<!-- ❌ Wrong: try/catch in submit handler -->
<script setup lang="ts">
const onSubmit = handleSubmit(async (values) => {
  try {
    await $fetchResult('/api/endpoint', { method: 'POST', body: values })
  } catch (error) {
    // $fetchResult handles errors automatically
  }
})
</script>

<!-- ✅ Correct: Check result.success -->
<script setup lang="ts">
const onSubmit = handleSubmit(async (values) => {
  const result = await $fetchResult('/api/endpoint', { method: 'POST', body: values })
  if (!result.success) {
    toast.error({ title: 'Error', description: result.error.message })
  }
})
</script>
```

### ❌ Mistake 4: Missing UIFormMessage

```vue
<!-- ❌ Wrong: No error message component -->
<UIFormField v-slot="{ componentField }" name="email">
  <UIFormItem>
    <UIFormLabel>Email</UIFormLabel>
    <UIFormControl>
      <UIInput v-bind="componentField" />
    </UIFormControl>
  </UIFormItem>
</UIFormField>

<!-- ✅ Correct: Include UIFormMessage -->
<UIFormField v-slot="{ componentField }" name="email">
  <UIFormItem>
    <UIFormLabel>Email</UIFormLabel>
    <UIFormControl>
      <UIInput v-bind="componentField" />
    </UIFormControl>
    <UIFormMessage />
  </UIFormItem>
</UIFormField>
```

## Summary: Form Best Practices

1. **Always use vee-validate + Zod** - Never create forms without validation
2. **Use toTypedSchema** - Wrap Zod schemas for vee-validate compatibility
3. **Bind componentField** - Use `v-bind="componentField"` on inputs
4. **Include UIFormMessage** - Always display validation errors
5. **Handle loading states** - Use `isSubmitting` to disable submit button
6. **Emit events, don't navigate** - Forms emit success/cancel events
7. **Use $fetchResult** - Don't wrap in try/catch
8. **Reuse schemas** - Share validation logic between client and server
