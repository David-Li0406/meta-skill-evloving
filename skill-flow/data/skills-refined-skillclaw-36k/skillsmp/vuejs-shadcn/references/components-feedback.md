# Feedback Components

Alert, Toast, Progress, Skeleton, and other feedback components.

## Table of Contents
- [Alert](#alert)
- [Toast](#toast)
- [Sonner](#sonner)
- [Progress](#progress)
- [Skeleton](#skeleton)
- [Spinner](#spinner)
- [Kbd](#kbd)

---

## Alert

```bash
pnpm dlx shadcn-vue@latest add alert
```

### Basic Usage

```vue
<script setup lang="ts">
import { Terminal } from 'lucide-vue-next'
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert'
</script>

<template>
  <Alert>
    <Terminal class="h-4 w-4" />
    <AlertTitle>Heads up!</AlertTitle>
    <AlertDescription>
      You can add components to your app using the cli.
    </AlertDescription>
  </Alert>
</template>
```

### Variants

```vue
<!-- Default -->
<Alert>
  <AlertTitle>Default</AlertTitle>
  <AlertDescription>This is a default alert.</AlertDescription>
</Alert>

<!-- Destructive -->
<Alert variant="destructive">
  <AlertCircle class="h-4 w-4" />
  <AlertTitle>Error</AlertTitle>
  <AlertDescription>Your session has expired. Please log in again.</AlertDescription>
</Alert>
```

### Alert Types

```vue
<!-- Info -->
<Alert class="border-blue-200 bg-blue-50 text-blue-900 [&>svg]:text-blue-600">
  <Info class="h-4 w-4" />
  <AlertTitle>Info</AlertTitle>
  <AlertDescription>This is an informational message.</AlertDescription>
</Alert>

<!-- Success -->
<Alert class="border-green-200 bg-green-50 text-green-900 [&>svg]:text-green-600">
  <CheckCircle class="h-4 w-4" />
  <AlertTitle>Success</AlertTitle>
  <AlertDescription>Your changes have been saved.</AlertDescription>
</Alert>

<!-- Warning -->
<Alert class="border-yellow-200 bg-yellow-50 text-yellow-900 [&>svg]:text-yellow-600">
  <AlertTriangle class="h-4 w-4" />
  <AlertTitle>Warning</AlertTitle>
  <AlertDescription>Your free trial is ending soon.</AlertDescription>
</Alert>
```

---

## Toast

```bash
pnpm dlx shadcn-vue@latest add toast
```

### Setup

Add the Toaster component to your app root:

```vue
<!-- App.vue -->
<script setup lang="ts">
import { Toaster } from '@/components/ui/toast'
</script>

<template>
  <div>
    <router-view />
    <Toaster />
  </div>
</template>
```

### Basic Usage

```vue
<script setup lang="ts">
import { useToast } from '@/components/ui/toast/use-toast'
import { Button } from '@/components/ui/button'

const { toast } = useToast()
</script>

<template>
  <Button
    @click="toast({
      title: 'Scheduled: Catch up',
      description: 'Friday, February 10, 2023 at 5:57 PM',
    })"
  >
    Show Toast
  </Button>
</template>
```

### Toast Variants

```typescript
// Default
toast({ title: 'Default toast' })

// Destructive
toast({
  title: 'Uh oh! Something went wrong.',
  description: 'There was a problem with your request.',
  variant: 'destructive',
})

// With action
toast({
  title: 'Undo',
  description: 'Your message has been sent.',
  action: h(ToastAction, { altText: 'Undo' }, { default: () => 'Undo' }),
})
```

### Toast with Action

```vue
<script setup lang="ts">
import { useToast } from '@/components/ui/toast/use-toast'
import { ToastAction } from '@/components/ui/toast'

const { toast } = useToast()

function showToast() {
  toast({
    title: 'Event has been created',
    description: 'Sunday, December 03, 2023 at 9:00 AM',
    action: h(ToastAction, {
      altText: 'Undo',
      onClick: () => console.log('Undo clicked'),
    }, { default: () => 'Undo' }),
  })
}
</script>
```

---

## Sonner

Alternative toast library with more features.

```bash
pnpm dlx shadcn-vue@latest add sonner
```

### Setup

```vue
<!-- App.vue -->
<script setup lang="ts">
import { Toaster } from '@/components/ui/sonner'
</script>

<template>
  <div>
    <router-view />
    <Toaster />
  </div>
</template>
```

### Basic Usage

```vue
<script setup lang="ts">
import { toast } from 'vue-sonner'
import { Button } from '@/components/ui/button'
</script>

<template>
  <Button @click="toast('Event has been created')">
    Show Toast
  </Button>
</template>
```

### Toast Types

```typescript
import { toast } from 'vue-sonner'

// Default
toast('Event has been created')

// Success
toast.success('Successfully saved!')

// Error
toast.error('Something went wrong')

// Warning
toast.warning('Be careful!')

// Info
toast.info('Here is some info')

// Loading
const toastId = toast.loading('Loading...')
// Later:
toast.success('Done!', { id: toastId })

// Promise
toast.promise(fetchData(), {
  loading: 'Loading...',
  success: 'Data loaded!',
  error: 'Error loading data',
})
```

### With Description

```typescript
toast('Event has been created', {
  description: 'Monday, January 3rd at 6:00pm',
})
```

### With Action

```typescript
toast('Event has been created', {
  action: {
    label: 'Undo',
    onClick: () => console.log('Undo'),
  },
})
```

### Custom Duration

```typescript
toast('This will stay longer', {
  duration: 10000, // 10 seconds
})

toast.success('This will stay forever', {
  duration: Infinity,
})
```

### Dismiss Toast

```typescript
const toastId = toast('Hello')
toast.dismiss(toastId)

// Dismiss all
toast.dismiss()
```

---

## Progress

```bash
pnpm dlx shadcn-vue@latest add progress
```

### Basic Usage

```vue
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Progress } from '@/components/ui/progress'

const progress = ref(13)

onMounted(() => {
  const timer = setTimeout(() => progress.value = 66, 500)
  return () => clearTimeout(timer)
})
</script>

<template>
  <Progress :model-value="progress" class="w-[60%]" />
</template>
```

### Indeterminate

```vue
<Progress :model-value="undefined" class="w-[60%]" />
```

### With Label

```vue
<template>
  <div class="space-y-2">
    <div class="flex justify-between text-sm">
      <span>Progress</span>
      <span>{{ progress }}%</span>
    </div>
    <Progress :model-value="progress" />
  </div>
</template>
```

---

## Skeleton

```bash
pnpm dlx shadcn-vue@latest add skeleton
```

### Basic Usage

```vue
<script setup lang="ts">
import { Skeleton } from '@/components/ui/skeleton'
</script>

<template>
  <div class="flex items-center space-x-4">
    <Skeleton class="h-12 w-12 rounded-full" />
    <div class="space-y-2">
      <Skeleton class="h-4 w-[250px]" />
      <Skeleton class="h-4 w-[200px]" />
    </div>
  </div>
</template>
```

### Card Skeleton

```vue
<template>
  <div class="flex flex-col space-y-3">
    <Skeleton class="h-[125px] w-[250px] rounded-xl" />
    <div class="space-y-2">
      <Skeleton class="h-4 w-[250px]" />
      <Skeleton class="h-4 w-[200px]" />
    </div>
  </div>
</template>
```

### Table Skeleton

```vue
<template>
  <div class="space-y-2">
    <Skeleton class="h-8 w-full" />
    <Skeleton class="h-8 w-full" />
    <Skeleton class="h-8 w-full" />
    <Skeleton class="h-8 w-full" />
    <Skeleton class="h-8 w-full" />
  </div>
</template>
```

### Loading State Pattern

```vue
<script setup lang="ts">
import { ref, onMounted } from 'vue'

const loading = ref(true)
const data = ref(null)

onMounted(async () => {
  data.value = await fetchData()
  loading.value = false
})
</script>

<template>
  <div v-if="loading" class="flex items-center space-x-4">
    <Skeleton class="h-12 w-12 rounded-full" />
    <div class="space-y-2">
      <Skeleton class="h-4 w-[250px]" />
      <Skeleton class="h-4 w-[200px]" />
    </div>
  </div>
  <div v-else class="flex items-center space-x-4">
    <Avatar>
      <AvatarImage :src="data.avatar" />
      <AvatarFallback>{{ data.initials }}</AvatarFallback>
    </Avatar>
    <div>
      <p class="font-medium">{{ data.name }}</p>
      <p class="text-sm text-muted-foreground">{{ data.email }}</p>
    </div>
  </div>
</template>
```

---

## Spinner

```bash
pnpm dlx shadcn-vue@latest add spinner
```

### Basic Usage

```vue
<script setup lang="ts">
import { Spinner } from '@/components/ui/spinner'
</script>

<template>
  <Spinner />
</template>
```

### Sizes

```vue
<Spinner class="h-4 w-4" />
<Spinner class="h-6 w-6" />
<Spinner class="h-8 w-8" />
```

### With Text

```vue
<div class="flex items-center space-x-2">
  <Spinner class="h-4 w-4" />
  <span>Loading...</span>
</div>
```

### Button Loading State

```vue
<Button disabled>
  <Spinner class="mr-2 h-4 w-4" />
  Please wait
</Button>
```

---

## Kbd

Keyboard key indicator.

```bash
pnpm dlx shadcn-vue@latest add kbd
```

### Basic Usage

```vue
<script setup lang="ts">
import { Kbd } from '@/components/ui/kbd'
</script>

<template>
  <div class="flex items-center gap-1">
    <Kbd>⌘</Kbd>
    <Kbd>K</Kbd>
  </div>
</template>
```

### Common Shortcuts

```vue
<!-- Copy -->
<div class="flex items-center gap-1">
  <Kbd>⌘</Kbd>
  <Kbd>C</Kbd>
</div>

<!-- Save -->
<div class="flex items-center gap-1">
  <Kbd>⌘</Kbd>
  <Kbd>S</Kbd>
</div>

<!-- Search -->
<div class="flex items-center gap-1">
  <Kbd>⌘</Kbd>
  <Kbd>K</Kbd>
</div>

<!-- Enter -->
<Kbd>↵</Kbd>

<!-- Shift -->
<Kbd>⇧</Kbd>

<!-- Escape -->
<Kbd>Esc</Kbd>
```

### In Context

```vue
<p class="text-sm text-muted-foreground">
  Press <Kbd>⌘</Kbd> <Kbd>K</Kbd> to open command palette
</p>
```

---

## Common Patterns

### Loading Button

```vue
<script setup lang="ts">
import { ref } from 'vue'
import { Loader2 } from 'lucide-vue-next'

const loading = ref(false)

async function handleClick() {
  loading.value = true
  try {
    await doSomething()
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <Button :disabled="loading" @click="handleClick">
    <Loader2 v-if="loading" class="mr-2 h-4 w-4 animate-spin" />
    {{ loading ? 'Saving...' : 'Save' }}
  </Button>
</template>
```

### Form Submission Feedback

```vue
<script setup lang="ts">
import { toast } from 'vue-sonner'

async function onSubmit(values) {
  try {
    await saveData(values)
    toast.success('Changes saved successfully')
  } catch (error) {
    toast.error('Failed to save changes', {
      description: error.message,
    })
  }
}
</script>
```

### Optimistic Updates

```vue
<script setup lang="ts">
import { toast } from 'vue-sonner'

async function deleteItem(id) {
  // Optimistically remove from UI
  items.value = items.value.filter(i => i.id !== id)
  
  const toastId = toast.loading('Deleting...')
  
  try {
    await api.delete(id)
    toast.success('Deleted', { id: toastId })
  } catch (error) {
    // Revert on failure
    items.value = [...items.value, deletedItem]
    toast.error('Failed to delete', { id: toastId })
  }
}
</script>
```
