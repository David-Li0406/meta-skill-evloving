# Component Organization and Naming Patterns

Complete guide for component organization, naming conventions, and responsibility patterns in the fitness application.

## Folder-Based Structure

All components follow a folder-based naming structure where forms and related components are organized by feature/entity.

```
components/
├── {Feature}/
│   ├── Form/
│   │   ├── Create.vue      # Creation form
│   │   ├── Edit.vue        # Edit form
│   │   ├── Delete.vue      # Delete confirmation
│   │   └── {Action}.vue    # Other specific actions
│   ├── Card.vue            # Display card
│   ├── List.vue            # List view
│   ├── Item.vue            # Single item
│   └── {OtherComponents}.vue
```

## Auto-Import Naming

Nuxt 3+ automatically imports components based on their path:

```
components/Goal/Form/Create.vue  →  <GoalFormCreate />
components/Goal/Card.vue         →  <GoalCard />
components/BodyMeasurement/Chart.vue  →  <BodyMeasurementChart />
```

## Real Examples from Codebase

### Existing Structure
```
components/
├── SuperAdmin/
│   └── User/
│       └── Form/
│           ├── Ban.vue
│           ├── Create.vue
│           ├── Delete.vue
│           └── Edit.vue
│
├── Exercise/
│   └── Form/
│       └── Configure.vue
```

### Progress Analytics Feature Structure
```
components/
├── BodyMeasurement/
│   ├── Form/
│   │   ├── Create.vue      # Log new body measurement
│   │   └── Edit.vue        # Edit existing measurement
│   ├── Chart.vue           # Trend chart for measurements
│   └── List.vue            # History list
│
├── Goal/
│   ├── Form/
│   │   ├── Create.vue      # Create new goal
│   │   └── Edit.vue        # Edit existing goal
│   ├── Card.vue            # Single goal display with progress bar
│   └── List.vue            # Goals list
│
├── Progress/
│   ├── NotificationItem.vue   # Single notification display
│   └── NotificationList.vue   # Notifications list
│
├── Analytics/
│   ├── BaseChart.vue       # Base chart component
│   ├── VolumeChart.vue     # Volume over time chart
│   ├── PRTimeline.vue      # Personal records timeline
│   ├── FrequencyStats.vue  # Workout frequency metrics
│   └── MuscleGroupBreakdown.vue  # Volume by muscle group
```

## Component Responsibilities

### Form Components

**Location:** `components/{Feature}/Form/{Action}.vue`

**Responsibilities:**
- Handle form state and validation
- Make API calls directly using `$fetchResult`
- Emit events on success/cancel
- Self-contained (parent doesn't manage form state)
- Handle loading/error states internally

**Props:**
- `Create.vue`: Usually none (creates new entity)
- `Edit.vue`: Entity ID or full entity object
- `Delete.vue`: Entity ID and confirmation info

### Card/Item Components

**Location:** `components/{Feature}/Card.vue` or `components/{Feature}/Item.vue`

**Responsibilities:**
- Display entity data
- Handle user interactions (edit, delete buttons)
- Emit events for actions (don't perform them)
- No API calls directly

**Props:**
- Entity object (full data)

**Emits:**
- `@edit`: When user clicks edit
- `@delete`: When user clicks delete
- `@click`: When card/item is clicked

**Example:**

```vue
<!-- components/Goal/Card.vue -->
<script setup lang="ts">
interface Props {
  goal: Goal
}

defineProps<Props>()

const emit = defineEmits<{
  edit: []
  delete: []
}>()
</script>

<template>
  <UICard>
    <UICardHeader>
      <UICardTitle>{{ goal.title }}</UICardTitle>
      <UICardDescription>
        Target: {{ goal.targetValue }} {{ goal.targetUnit }}
      </UICardDescription>
    </UICardHeader>
    <UICardContent>
      <!-- Progress display -->
    </UICardContent>
    <UICardFooter class="gap-2">
      <UIButton variant="outline" size="sm" @click="emit('edit')">
        Edit
      </UIButton>
      <UIButton variant="destructive" size="sm" @click="emit('delete')">
        Delete
      </UIButton>
    </UICardFooter>
  </UICard>
</template>
```

### List Components

**Location:** `components/{Feature}/List.vue`

**Responsibilities:**
- Fetch and display list of entities using `useFetch`/`useAsyncData`
- Handle pagination/infinite scroll
- Handle filtering/sorting
- Manage empty/loading/error states

**Props:**
- Optional filters (e.g., `status`, `userId`)
- Optional sort order

**Example:**

```vue
<!-- components/Goal/List.vue -->
<script setup lang="ts">
interface Props {
  status?: 'active' | 'completed'
}

const props = defineProps<Props>()

const { data: goals, pending, error, refresh } = useBaseFetch('/api/goals', {
  key: 'user-goals',
  query: computed(() => ({ status: props.status })),
  lazy: true,
  default: () => [],
})

// Expose refresh for parent components
defineExpose({ refresh })
</script>

<template>
  <div>
    <!-- Loading state -->
    <div v-if="pending" class="space-y-4">
      <UISkeleton class="h-32 w-full" />
      <UISkeleton class="h-32 w-full" />
    </div>

    <!-- Error state -->
    <UIAlert v-else-if="error" variant="destructive">
      <UIAlertTitle>Error</UIAlertTitle>
      <UIAlertDescription>Failed to load goals</UIAlertDescription>
    </UIAlert>

    <!-- Empty state -->
    <div v-else-if="goals.length === 0" class="text-center py-8">
      <p class="text-muted-foreground">No goals found</p>
    </div>

    <!-- Success state -->
    <div v-else class="space-y-4">
      <GoalCard
        v-for="goal in goals"
        :key="goal.id"
        :goal="goal"
        @edit="handleEdit(goal.id)"
        @delete="handleDelete(goal.id)"
      />
    </div>
  </div>
</template>
```

## State Management Patterns

### ❌ DON'T: Create state management composables

```typescript
// ❌ Wrong: Don't create state management composables
export function useGoals() {
  const goals = ref<Goal[]>([])
  const loading = ref(false)

  async function fetchGoals() {
    loading.value = true
    goals.value = await $fetch('/api/goals')
    loading.value = false
  }

  return { goals, loading, fetchGoals }
}
```

### ✅ DO: Manage state at page level

```vue
<!-- ✅ Correct: State in pages using useFetch -->
<script setup lang="ts">
// Page manages all data fetching and state
const { data: goals, pending, refresh } = useBaseFetch('/api/goals', {
  key: 'user-goals',
  lazy: true,
  default: () => [],
})

// Computed derived state
const activeGoals = computed(() =>
  goals.value.filter(goal => goal.status === 'active')
)

// Components receive data via props
</script>

<template>
  <div>
    <GoalCard
      v-for="goal in activeGoals"
      :key="goal.id"
      :goal="goal"
      @edit="handleEdit(goal.id)"
    />
  </div>
</template>
```

### Key Principles

1. **Page-Level State**: Use `useFetch`/`useAsyncData` in pages, not composables
2. **Props Down, Events Up**: Components are stateless, receive data via props
3. **Forms Are Self-Contained**: Forms manage their own internal form state and API calls
4. **No State Composables**: Only use composables for utilities (e.g., `useMobileMode()`), not data fetching
5. **Server-First**: Prefer SSR-compatible `useFetch` over client-only `$fetch`

## Variable Naming Conventions

### ❌ DON'T: Use abbreviations

```typescript
// ❌ Wrong: Abbreviated names
const secondAvg = average(data)
const numItems = items.length
const prData = await $fetch('/api/pr')
```

### ✅ DO: Use full, descriptive names

```typescript
// ✅ Correct: Full names
const secondAverage = average(data)
const numberOfItems = items.length
const personalRecordsData = await $fetch('/api/personal-records')
```

## Common Anti-Patterns

### ❌ DON'T: Flat naming

```vue
<!-- ❌ Wrong: Flat naming -->
<GoalForm />
<GoalCreateForm />
<GoalCard />

<!-- ❌ Wrong: Generic naming -->
<Form />
<CreateForm />
```

### ✅ DO: Folder-based naming

```vue
<!-- ✅ Correct: Folder-based -->
<GoalFormCreate />   <!-- Auto-imported from components/Goal/Form/Create.vue -->
<GoalFormEdit />     <!-- Auto-imported from components/Goal/Form/Edit.vue -->
<GoalCard />         <!-- Auto-imported from components/Goal/Card.vue -->

<!-- Or with explicit path -->
import GoalFormCreate from '~/components/Goal/Form/Create.vue'
```

## Decision Tree: Where Should This Component Go?

1. **Is it a form?** → `components/{Feature}/Form/{Action}.vue`
2. **Does it display a single entity?** → `components/{Feature}/Card.vue` or `Item.vue`
3. **Does it display a list?** → `components/{Feature}/List.vue`
4. **Is it a shared/base component?** → `components/Base/{ComponentName}.vue`
5. **Is it page-specific?** → Keep it in the page's `<script setup>`
6. **Does it need to fetch data?** → Put it in the page, not a composable

## Migration Guide

If you have existing components with flat naming:

**Before:**
```
components/
├── GoalForm.vue
├── GoalCard.vue
└── BodyMeasurementForm.vue
```

**After:**
```
components/
├── Goal/
│   ├── Form/
│   │   └── Create.vue  (rename from GoalForm.vue)
│   └── Card.vue        (rename from GoalCard.vue)
│
└── BodyMeasurement/
    └── Form/
        └── Create.vue  (rename from BodyMeasurementForm.vue)
```

**Update imports:** Auto-import will handle new names automatically.

## Benefits of This Convention

1. **Clear Organization**: Easy to find related components
2. **Scalability**: Supports growth (multiple forms per feature)
3. **Consistency**: Same pattern across entire codebase
4. **Auto-Import Friendly**: Works seamlessly with Nuxt auto-imports
5. **Action-Oriented**: Form names describe what they do (Create, Edit, Delete)
6. **Namespace Protection**: Prevents naming conflicts
