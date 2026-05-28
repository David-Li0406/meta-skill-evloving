# UIDialog Pattern: Best Practices

Complete guide for using UIDialog components with the `v-slot="{ close }"` pattern. This is the **ONLY** correct way to manage dialogs in this application.

## Core Principle

**NEVER use refs to manage dialog state.** The `v-slot="{ close }"` pattern provides built-in state management through Shadcn Vue's internal mechanism.

## Why Not Use Refs?

```vue
<!-- ❌ WRONG: Manual dialog state management -->
<template>
  <UIButton @click="isOpen = true">Create Goal</UIButton>

  <UIDialog v-model:open="isOpen">
    <UIDialogContent>
      <UIDialogHeader>
        <UIDialogTitle>Create New Goal</UIDialogTitle>
      </UIDialogHeader>
      <GoalFormCreate @created="handleCreated" />
    </UIDialogContent>
  </UIDialog>
</template>

<script setup lang="ts">
const isOpen = ref(false) // ❌ Unnecessary state management

function handleCreated(goal: Goal) {
  isOpen.value = false // ❌ Manual state update
  toast.success({ title: 'Goal created!', description: goal.title })
}
</script>
```

**Problems with this approach:**
1. Introduces unnecessary state management
2. Requires manual state synchronization
3. Increases component complexity
4. More prone to bugs (forgetting to close, race conditions)
5. Goes against Shadcn Vue's built-in patterns

## The Correct Pattern: v-slot

```vue
<!-- ✅ CORRECT: v-slot pattern with close function -->
<template>
  <UIDialog v-slot="{ close }">
    <UIDialogTrigger as-child>
      <UIButton>Create Goal</UIButton>
    </UIDialogTrigger>
    <UIDialogContent>
      <UIDialogHeader>
        <UIDialogTitle>Create New Goal</UIDialogTitle>
        <UIDialogDescription>
          Add a new fitness goal to track your progress.
        </UIDialogDescription>
      </UIDialogHeader>
      <GoalFormCreate
        @created="(goal) => { handleGoalCreated(goal); close(); }"
        @cancelled="close"
      />
    </UIDialogContent>
  </UIDialog>
</template>

<script setup lang="ts">
// No dialog state needed!

function handleGoalCreated(goal: Goal) {
  toast.success({ title: 'Goal created!', description: goal.title })
  refresh() // Refresh data
}
</script>
```

**Advantages:**
1. No manual state management required
2. Built-in accessibility features
3. Cleaner component code
4. Follows Shadcn Vue conventions
5. Automatic focus management
6. Keyboard navigation (Escape to close)

## Key Components

### UIDialog
The root component that provides state management context via `v-slot="{ close }"`.

### UIDialogTrigger
Wraps the button or element that opens the dialog. Use `as-child` to pass props/events to the child element.

```vue
<UIDialogTrigger as-child>
  <UIButton>Open Dialog</UIButton>
</UIDialogTrigger>
```

### UIDialogContent
The actual dialog content container. Handles backdrop, positioning, and animations.

### UIDialogHeader
Optional container for title and description at the top of the dialog.

### UIDialogTitle
Required for accessibility. The dialog's main heading.

### UIDialogDescription
Optional description text that provides additional context.

### UIDialogFooter
Optional container for action buttons at the bottom of the dialog.

## Complete Dialog Structure

```vue
<UIDialog v-slot="{ close }">
  <UIDialogTrigger as-child>
    <UIButton>Open Dialog</UIButton>
  </UIDialogTrigger>

  <UIDialogContent>
    <UIDialogHeader>
      <UIDialogTitle>Dialog Title</UIDialogTitle>
      <UIDialogDescription>
        Optional description text for additional context.
      </UIDialogDescription>
    </UIDialogHeader>

    <!-- Main content -->
    <div class="py-4">
      <!-- Your content here -->
    </div>

    <UIDialogFooter>
      <UIButton variant="outline" @click="close">
        Cancel
      </UIButton>
      <UIButton @click="handleSubmit(); close()">
        Save Changes
      </UIButton>
    </UIDialogFooter>
  </UIDialogContent>
</UIDialog>
```

## Pattern: Dialog with Form

Forms should handle their own API calls and emit events on success:

```vue
<template>
  <UIDialog v-slot="{ close }">
    <UIDialogTrigger as-child>
      <UIButton icon="i-lucide-plus">Create Goal</UIButton>
    </UIDialogTrigger>

    <UIDialogContent>
      <UIDialogHeader>
        <UIDialogTitle>Create New Goal</UIDialogTitle>
        <UIDialogDescription>
          Set a new fitness goal to track your progress.
        </UIDialogDescription>
      </UIDialogHeader>

      <GoalFormCreate
        @created="(goal) => { handleCreated(goal); close(); }"
        @cancelled="close"
      />
    </UIDialogContent>
  </UIDialog>
</template>

<script setup lang="ts">
function handleCreated(goal: Goal) {
  toast.success({
    title: 'Goal Created',
    description: `${goal.title} has been added to your goals.`,
  })
  refresh() // Refresh the goals list
}
</script>
```

**Key points:**
1. Form emits `@created` with the created entity
2. Form emits `@cancelled` when user cancels
3. Inline handler combines success logic and `close()`
4. No manual state management needed

## Pattern: Multiple Dialogs

When you need multiple dialogs (create + edit), track entity IDs instead of dialog state:

```vue
<template>
  <!-- Create Dialog -->
  <UIDialog v-slot="{ close }">
    <UIDialogTrigger as-child>
      <UIButton icon="i-lucide-plus">Create Goal</UIButton>
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

  <!-- Edit Dialog -->
  <UIDialog v-if="editingGoalId" v-slot="{ close }">
    <UIDialogContent>
      <UIDialogHeader>
        <UIDialogTitle>Edit Goal</UIDialogTitle>
      </UIDialogHeader>
      <GoalFormEdit
        :goal-id="editingGoalId"
        @updated="(goal) => { handleUpdated(goal); close(); editingGoalId = null; }"
        @cancelled="() => { close(); editingGoalId = null; }"
      />
    </UIDialogContent>
  </UIDialog>

  <!-- Goals List -->
  <div class="space-y-4">
    <GoalCard
      v-for="goal in goals"
      :key="goal.id"
      :goal="goal"
      @edit="editingGoalId = goal.id"
      @delete="handleDelete(goal.id)"
    />
  </div>
</template>

<script setup lang="ts">
// Only track which entity is being edited, not dialog state
const editingGoalId = ref<string | null>(null)

const { data: goals, refresh } = useBaseFetch('/api/goals', {
  key: 'user-goals',
  lazy: true,
  default: () => [],
})

function handleCreated(goal: Goal) {
  toast.success({ title: 'Created!', description: goal.title })
  refresh()
}

function handleUpdated(goal: Goal) {
  toast.success({ title: 'Updated!', description: goal.title })
  refresh()
}

function handleDelete(goalId: string) {
  // Handle delete logic
}
</script>
```

**Key points:**
1. Create dialog uses `UIDialogTrigger` pattern
2. Edit dialog uses `v-if` with entity ID to control visibility
3. Only track entity ID, not dialog open state
4. Clear entity ID when dialog closes (`editingGoalId = null`)

## Pattern: Confirmation Dialog

For delete or destructive actions, use UIAlertDialog (not UIDialog):

```vue
<template>
  <UIAlertDialog v-slot="{ close }">
    <UIAlertDialogTrigger as-child>
      <UIButton variant="destructive" icon="i-lucide-trash">
        Delete Goal
      </UIButton>
    </UIAlertDialogTrigger>

    <UIAlertDialogContent>
      <UIAlertDialogHeader>
        <UIAlertDialogTitle>Are you sure?</UIAlertDialogTitle>
        <UIAlertDialogDescription>
          This action cannot be undone. This will permanently delete your goal.
        </UIAlertDialogDescription>
      </UIAlertDialogHeader>

      <UIAlertDialogFooter>
        <UIAlertDialogCancel @click="close">
          Cancel
        </UIAlertDialogCancel>
        <UIAlertDialogAction @click="handleDelete(); close()">
          Delete
        </UIAlertDialogAction>
      </UIAlertDialogFooter>
    </UIAlertDialogContent>
  </UIAlertDialog>
</template>

<script setup lang="ts">
async function handleDelete() {
  const result = await $fetchResult(`/api/goals/${goalId}`, {
    method: 'DELETE',
  })

  if (result.success) {
    toast.success({ title: 'Deleted', description: 'Goal has been removed.' })
    refresh()
  }
}
</script>
```

## Pattern: Dialog Without Trigger

Sometimes you need to open a dialog programmatically (e.g., edit from a list item):

```vue
<template>
  <!-- Edit Dialog - opened via v-if -->
  <UIDialog v-if="editingGoalId" v-slot="{ close }">
    <UIDialogContent>
      <UIDialogHeader>
        <UIDialogTitle>Edit Goal</UIDialogTitle>
      </UIDialogHeader>
      <GoalFormEdit
        :goal-id="editingGoalId"
        @updated="(goal) => { handleUpdated(goal); close(); editingGoalId = null; }"
        @cancelled="() => { close(); editingGoalId = null; }"
      />
    </UIDialogContent>
  </UIDialog>

  <!-- Goal Cards with Edit Buttons -->
  <GoalCard
    v-for="goal in goals"
    :key="goal.id"
    :goal="goal"
    @edit="editingGoalId = goal.id"
  />
</template>

<script setup lang="ts">
const editingGoalId = ref<string | null>(null)

function handleUpdated(goal: Goal) {
  toast.success({ title: 'Updated!', description: goal.title })
  refresh()
}
</script>
```

**Key points:**
1. Use `v-if` with an entity ID to show/hide dialog
2. No `UIDialogTrigger` needed
3. Dialog appears when entity ID is set
4. Clear entity ID on close to hide dialog

## Accessibility Features (Built-in)

When using the `v-slot` pattern, you automatically get:

1. **Keyboard Navigation**:
   - Escape key closes the dialog
   - Tab cycles through focusable elements
   - Focus is trapped within the dialog

2. **Screen Reader Support**:
   - `UIDialogTitle` is announced as the dialog heading
   - `UIDialogDescription` provides additional context
   - Proper ARIA attributes are applied automatically

3. **Focus Management**:
   - Focus moves to the dialog when opened
   - Focus returns to the trigger when closed
   - First focusable element receives focus

4. **Backdrop Click**:
   - Clicking outside closes the dialog (can be disabled)

## Common Mistakes to Avoid

### ❌ Mistake 1: Using v-model

```vue
<!-- ❌ Wrong -->
<UIDialog v-model:open="isOpen">
  <!-- This requires manual state management -->
</UIDialog>
```

### ❌ Mistake 2: Not Using as-child

```vue
<!-- ❌ Wrong: Event handlers won't work correctly -->
<UIDialogTrigger>
  <UIButton>Open</UIButton>
</UIDialogTrigger>

<!-- ✅ Correct: Use as-child -->
<UIDialogTrigger as-child>
  <UIButton>Open</UIButton>
</UIDialogTrigger>
```

### ❌ Mistake 3: Forgetting to Call close()

```vue
<!-- ❌ Wrong: Dialog won't close -->
<UIButton @click="handleSubmit">Save</UIButton>

<!-- ✅ Correct: Call close() after success -->
<UIButton @click="handleSubmit(); close()">Save</UIButton>
```

### ❌ Mistake 4: Not Providing Title

```vue
<!-- ❌ Wrong: Missing required title for accessibility -->
<UIDialogContent>
  <div>Content</div>
</UIDialogContent>

<!-- ✅ Correct: Always include UIDialogTitle -->
<UIDialogContent>
  <UIDialogHeader>
    <UIDialogTitle>Dialog Title</UIDialogTitle>
  </UIDialogHeader>
  <div>Content</div>
</UIDialogContent>
```

## Summary: The Five Rules of Dialogs

1. **Always use `v-slot="{ close }"`** - Never manage state with refs
2. **Always use `as-child` on UIDialogTrigger** - Ensures proper event handling
3. **Always call `close()` explicitly** - When form succeeds or is cancelled
4. **Always provide UIDialogTitle** - Required for accessibility
5. **Use `v-if` with entity IDs for edit dialogs** - Track what's being edited, not dialog state

## Quick Reference

```vue
<!-- Basic Pattern -->
<UIDialog v-slot="{ close }">
  <UIDialogTrigger as-child>
    <UIButton>Open</UIButton>
  </UIDialogTrigger>
  <UIDialogContent>
    <UIDialogHeader>
      <UIDialogTitle>Title</UIDialogTitle>
    </UIDialogHeader>
    <div>Content</div>
    <UIDialogFooter>
      <UIButton @click="close">Cancel</UIButton>
      <UIButton @click="handleSubmit(); close()">Save</UIButton>
    </UIDialogFooter>
  </UIDialogContent>
</UIDialog>

<!-- Edit Dialog (No Trigger) -->
<UIDialog v-if="editingId" v-slot="{ close }">
  <UIDialogContent>
    <UIDialogHeader>
      <UIDialogTitle>Edit</UIDialogTitle>
    </UIDialogHeader>
    <MyFormEdit
      :id="editingId"
      @updated="() => { refresh(); close(); editingId = null; }"
      @cancelled="() => { close(); editingId = null; }"
    />
  </UIDialogContent>
</UIDialog>

<!-- Confirmation Dialog -->
<UIAlertDialog v-slot="{ close }">
  <UIAlertDialogTrigger as-child>
    <UIButton variant="destructive">Delete</UIButton>
  </UIAlertDialogTrigger>
  <UIAlertDialogContent>
    <UIAlertDialogHeader>
      <UIAlertDialogTitle>Are you sure?</UIAlertDialogTitle>
      <UIAlertDialogDescription>
        This action cannot be undone.
      </UIAlertDialogDescription>
    </UIAlertDialogHeader>
    <UIAlertDialogFooter>
      <UIAlertDialogCancel @click="close">Cancel</UIAlertDialogCancel>
      <UIAlertDialogAction @click="handleDelete(); close()">Delete</UIAlertDialogAction>
    </UIAlertDialogFooter>
  </UIAlertDialogContent>
</UIAlertDialog>
```
