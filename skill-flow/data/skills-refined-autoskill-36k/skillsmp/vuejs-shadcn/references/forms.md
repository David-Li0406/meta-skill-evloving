# Forms

Form handling with VeeValidate, Zod, and TanStack Form.

## Table of Contents
- [VeeValidate + Zod](#veevalidate--zod)
- [Form Components](#form-components)
- [Field Component](#field-component)
- [TanStack Form](#tanstack-form)
- [Validation Patterns](#validation-patterns)

---

## VeeValidate + Zod

### Installation

```bash
pnpm add vee-validate @vee-validate/zod zod
pnpm dlx shadcn-vue@latest add form input button
```

### Basic Form

```vue
<script setup lang="ts">
import { toTypedSchema } from '@vee-validate/zod'
import { useForm } from 'vee-validate'
import * as z from 'zod'
import { Button } from '@/components/ui/button'
import {
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form'
import { Input } from '@/components/ui/input'

const formSchema = toTypedSchema(z.object({
  username: z.string().min(2, 'Username must be at least 2 characters').max(50),
  email: z.string().email('Invalid email address'),
}))

const form = useForm({
  validationSchema: formSchema,
})

const onSubmit = form.handleSubmit((values) => {
  console.log('Form submitted!', values)
})
</script>

<template>
  <form @submit="onSubmit" class="space-y-6">
    <FormField v-slot="{ componentField }" name="username">
      <FormItem>
        <FormLabel>Username</FormLabel>
        <FormControl>
          <Input type="text" placeholder="shadcn" v-bind="componentField" />
        </FormControl>
        <FormDescription>
          This is your public display name.
        </FormDescription>
        <FormMessage />
      </FormItem>
    </FormField>

    <FormField v-slot="{ componentField }" name="email">
      <FormItem>
        <FormLabel>Email</FormLabel>
        <FormControl>
          <Input type="email" placeholder="email@example.com" v-bind="componentField" />
        </FormControl>
        <FormMessage />
      </FormItem>
    </FormField>

    <Button type="submit">Submit</Button>
  </form>
</template>
```

### Form with Initial Values

```vue
<script setup lang="ts">
const form = useForm({
  validationSchema: formSchema,
  initialValues: {
    username: 'johndoe',
    email: 'john@example.com',
  },
})
</script>
```

### Form with Select

```vue
<script setup lang="ts">
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'

const formSchema = toTypedSchema(z.object({
  role: z.string({ required_error: 'Please select a role' }),
}))
</script>

<template>
  <FormField v-slot="{ componentField }" name="role">
    <FormItem>
      <FormLabel>Role</FormLabel>
      <Select v-bind="componentField">
        <FormControl>
          <SelectTrigger>
            <SelectValue placeholder="Select a role" />
          </SelectTrigger>
        </FormControl>
        <SelectContent>
          <SelectItem value="admin">Admin</SelectItem>
          <SelectItem value="user">User</SelectItem>
          <SelectItem value="guest">Guest</SelectItem>
        </SelectContent>
      </Select>
      <FormMessage />
    </FormItem>
  </FormField>
</template>
```

### Form with Checkbox

```vue
<script setup lang="ts">
import { Checkbox } from '@/components/ui/checkbox'

const formSchema = toTypedSchema(z.object({
  terms: z.boolean().refine(val => val === true, {
    message: 'You must accept the terms',
  }),
}))
</script>

<template>
  <FormField v-slot="{ value, handleChange }" name="terms">
    <FormItem class="flex items-start space-x-3 space-y-0">
      <FormControl>
        <Checkbox :checked="value" @update:checked="handleChange" />
      </FormControl>
      <div class="space-y-1 leading-none">
        <FormLabel>Accept terms and conditions</FormLabel>
        <FormDescription>
          You agree to our Terms of Service and Privacy Policy.
        </FormDescription>
      </div>
      <FormMessage />
    </FormItem>
  </FormField>
</template>
```

### Form with Radio Group

```vue
<script setup lang="ts">
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group'

const formSchema = toTypedSchema(z.object({
  type: z.enum(['all', 'mentions', 'none'], {
    required_error: 'Please select a notification type',
  }),
}))
</script>

<template>
  <FormField v-slot="{ componentField }" name="type">
    <FormItem class="space-y-3">
      <FormLabel>Notify me about...</FormLabel>
      <FormControl>
        <RadioGroup v-bind="componentField" class="flex flex-col space-y-1">
          <FormItem class="flex items-center space-x-3 space-y-0">
            <FormControl>
              <RadioGroupItem value="all" />
            </FormControl>
            <FormLabel class="font-normal">All new messages</FormLabel>
          </FormItem>
          <FormItem class="flex items-center space-x-3 space-y-0">
            <FormControl>
              <RadioGroupItem value="mentions" />
            </FormControl>
            <FormLabel class="font-normal">Direct messages and mentions</FormLabel>
          </FormItem>
          <FormItem class="flex items-center space-x-3 space-y-0">
            <FormControl>
              <RadioGroupItem value="none" />
            </FormControl>
            <FormLabel class="font-normal">Nothing</FormLabel>
          </FormItem>
        </RadioGroup>
      </FormControl>
      <FormMessage />
    </FormItem>
  </FormField>
</template>
```

### Form with Textarea

```vue
<script setup lang="ts">
import { Textarea } from '@/components/ui/textarea'

const formSchema = toTypedSchema(z.object({
  bio: z.string().min(10).max(160),
}))
</script>

<template>
  <FormField v-slot="{ componentField }" name="bio">
    <FormItem>
      <FormLabel>Bio</FormLabel>
      <FormControl>
        <Textarea
          placeholder="Tell us about yourself"
          class="resize-none"
          v-bind="componentField"
        />
      </FormControl>
      <FormDescription>
        You can @mention other users and organizations.
      </FormDescription>
      <FormMessage />
    </FormItem>
  </FormField>
</template>
```

---

## Form Components

### FormField

Wraps form controls with validation state.

```vue
<FormField v-slot="{ componentField, value, handleChange }" name="fieldName">
  <!-- Form control here -->
</FormField>
```

**Slot Props:**
- `componentField` - Object to bind to input (contains value, onChange, onBlur)
- `value` - Current field value
- `handleChange` - Function to update value

### FormItem

Container for form field elements.

```vue
<FormItem>
  <FormLabel>Label</FormLabel>
  <FormControl><!-- Input --></FormControl>
  <FormDescription>Description</FormDescription>
  <FormMessage />
</FormItem>
```

### FormLabel

Accessible label linked to form control.

### FormControl

Wrapper that provides accessibility attributes.

### FormDescription

Helper text below the input.

### FormMessage

Displays validation error messages.

---

## Field Component

Modern field component for simpler forms.

```bash
pnpm dlx shadcn-vue@latest add field
```

### Basic Usage

```vue
<script setup lang="ts">
import {
  Field,
  FieldDescription,
  FieldError,
  FieldGroup,
  FieldLabel,
  FieldLegend,
  FieldSet,
} from '@/components/ui/field'
import { Input } from '@/components/ui/input'
</script>

<template>
  <FieldGroup>
    <Field>
      <FieldLabel for="email">Email</FieldLabel>
      <Input id="email" type="email" placeholder="email@example.com" />
      <FieldDescription>We'll never share your email.</FieldDescription>
    </Field>
  </FieldGroup>
</template>
```

### Field with Error State

```vue
<template>
  <Field data-invalid>
    <FieldLabel for="email">Email</FieldLabel>
    <Input id="email" type="email" aria-invalid />
    <FieldError>Enter a valid email address.</FieldError>
  </Field>
</template>
```

### FieldSet with Legend

```vue
<template>
  <FieldSet>
    <FieldLegend>Contact Information</FieldLegend>
    <FieldDescription>Please provide your contact details.</FieldDescription>
    <FieldGroup>
      <Field>
        <FieldLabel for="name">Name</FieldLabel>
        <Input id="name" />
      </Field>
      <Field>
        <FieldLabel for="phone">Phone</FieldLabel>
        <Input id="phone" type="tel" />
      </Field>
    </FieldGroup>
  </FieldSet>
</template>
```

---

## TanStack Form

Alternative form library with different API.

### Installation

```bash
pnpm add @tanstack/vue-form
```

### Basic Usage

```vue
<script setup lang="ts">
import { useForm } from '@tanstack/vue-form'
import { z } from 'zod'
import { Button } from '@/components/ui/button'
import { Field, FieldError, FieldGroup, FieldLabel } from '@/components/ui/field'
import { Input } from '@/components/ui/input'

const formSchema = z.object({
  username: z.string().min(2).max(50),
})

const form = useForm({
  defaultValues: {
    username: '',
  },
  onSubmit: async ({ value }) => {
    console.log('Submitted:', value)
  },
})

function isInvalid(field: any) {
  return field.state.meta.isTouched && field.state.meta.errors.length > 0
}
</script>

<template>
  <form @submit.prevent="form.handleSubmit()">
    <FieldGroup>
      <form.Field name="username" :validators="{ onChange: formSchema.shape.username }">
        <template #default="{ field }">
          <Field :data-invalid="isInvalid(field)">
            <FieldLabel for="username">Username</FieldLabel>
            <Input
              id="username"
              :value="field.state.value"
              :aria-invalid="isInvalid(field)"
              @input="field.handleChange($event.target.value)"
              @blur="field.handleBlur"
            />
            <FieldError v-if="isInvalid(field)" :errors="field.state.meta.errors" />
          </Field>
        </template>
      </form.Field>
    </FieldGroup>
    <Button type="submit">Submit</Button>
  </form>
</template>
```

---

## Validation Patterns

### Common Zod Schemas

```typescript
import * as z from 'zod'

// String validations
const username = z.string()
  .min(2, 'Too short')
  .max(50, 'Too long')
  .regex(/^[a-z0-9]+$/, 'Only lowercase letters and numbers')

const email = z.string().email('Invalid email')

const password = z.string()
  .min(8, 'At least 8 characters')
  .regex(/[A-Z]/, 'Must contain uppercase')
  .regex(/[0-9]/, 'Must contain number')

// Optional fields
const bio = z.string().max(160).optional()

// Enum
const role = z.enum(['admin', 'user', 'guest'])

// Boolean
const terms = z.boolean().refine(v => v, 'Must accept terms')

// Number
const age = z.coerce.number().min(18).max(120)

// Date
const birthdate = z.coerce.date()

// Array
const tags = z.array(z.string()).min(1, 'At least one tag')

// Object
const address = z.object({
  street: z.string(),
  city: z.string(),
  zip: z.string().regex(/^\d{5}$/),
})
```

### Conditional Validation

```typescript
const schema = z.object({
  hasPhone: z.boolean(),
  phone: z.string().optional(),
}).refine(
  data => !data.hasPhone || (data.hasPhone && data.phone),
  {
    message: 'Phone is required when enabled',
    path: ['phone'],
  }
)
```

### Password Confirmation

```typescript
const schema = z.object({
  password: z.string().min(8),
  confirmPassword: z.string(),
}).refine(data => data.password === data.confirmPassword, {
  message: 'Passwords must match',
  path: ['confirmPassword'],
})
```
