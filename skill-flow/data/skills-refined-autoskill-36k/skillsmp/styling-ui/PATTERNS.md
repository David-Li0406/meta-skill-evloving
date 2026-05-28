# UI Interaction Patterns

Common interaction patterns for the todo-me application.

## Toast Notifications

Temporary messages that appear and auto-dismiss.

### Basic Toast
```html
<div x-data="{ show: true }"
     x-show="show"
     x-init="setTimeout(() => show = false, 5000)"
     x-transition:enter="transition ease-out duration-300"
     x-transition:enter-start="translate-y-4 opacity-0"
     x-transition:enter-end="translate-y-0 opacity-100"
     x-transition:leave="transition ease-in duration-200"
     x-transition:leave-start="translate-y-0 opacity-100"
     x-transition:leave-end="translate-y-4 opacity-0"
     class="fixed bottom-4 right-4 z-50 bg-gray-900 text-white rounded-lg shadow-lg px-4 py-3 flex items-center gap-4 max-w-md">
  <span class="text-sm flex-1">Task completed successfully</span>
  <button @click="show = false" class="text-gray-400 hover:text-gray-200">
    <svg class="w-4 h-4"><!-- x icon --></svg>
  </button>
</div>
```

### Undo Toast (with countdown)
```html
<div x-data="{ show: true, countdown: 5 }"
     x-show="show"
     x-init="let i = setInterval(() => { countdown--; if(countdown <= 0) { clearInterval(i); show = false; } }, 1000)"
     x-transition:enter="transition ease-out duration-300"
     x-transition:enter-start="translate-y-4 opacity-0"
     x-transition:enter-end="translate-y-0 opacity-100"
     x-transition:leave="transition ease-in duration-200"
     class="fixed bottom-4 right-4 z-50 bg-gray-900 text-white rounded-lg shadow-lg px-4 py-3 flex items-center gap-4 max-w-md">
  <span class="text-sm flex-1">Task completed</span>
  <button @click="executeUndo()" class="text-indigo-400 hover:text-indigo-300 font-medium transition-colors">
    Undo
  </button>
  <span class="text-xs text-gray-400" x-text="countdown + 's'"></span>
  <button @click="show = false" class="text-gray-400 hover:text-gray-200">
    <svg class="w-4 h-4"><!-- x icon --></svg>
  </button>
</div>
```

### Toast Variants
- **Success**: `bg-green-900` or keep neutral `bg-gray-900`
- **Error**: `bg-red-900 text-red-100`
- **Warning**: `bg-yellow-900 text-yellow-100`
- **Info**: `bg-gray-900` (default)

## Loading States

### Spinner
```html
<div class="flex items-center justify-center p-8">
  <svg class="animate-spin h-8 w-8 text-indigo-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
  </svg>
</div>
```

### Skeleton Loading
```html
<!-- Task card skeleton -->
<div class="bg-white shadow rounded-lg p-4 animate-pulse">
  <div class="flex items-start gap-3">
    <div class="h-4 w-4 bg-gray-200 rounded"></div>
    <div class="flex-1">
      <div class="h-4 bg-gray-200 rounded w-3/4"></div>
      <div class="h-3 bg-gray-200 rounded w-1/2 mt-2"></div>
    </div>
  </div>
  <div class="mt-3 flex gap-2">
    <div class="h-5 w-16 bg-gray-200 rounded-full"></div>
    <div class="h-5 w-20 bg-gray-200 rounded-full"></div>
  </div>
</div>
```

### Button Loading State
```html
<button type="submit" disabled
        class="inline-flex items-center gap-2 rounded-md bg-indigo-600 px-4 py-2 text-sm font-semibold text-white opacity-75 cursor-not-allowed">
  <svg class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
  </svg>
  Saving...
</button>
```

## Empty States

### No Tasks
```html
<div class="text-center py-12">
  <svg class="mx-auto h-12 w-12 text-gray-300">
    <!-- clipboard-list icon -->
  </svg>
  <h3 class="mt-4 text-sm font-semibold text-gray-900">No tasks</h3>
  <p class="mt-1 text-sm text-gray-500">Get started by creating a new task.</p>
  <div class="mt-6">
    <button type="button"
            class="inline-flex items-center gap-2 rounded-md bg-indigo-600 px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-700">
      <svg class="w-5 h-5"><!-- plus icon --></svg>
      New Task
    </button>
  </div>
</div>
```

### No Search Results
```html
<div class="text-center py-12">
  <svg class="mx-auto h-12 w-12 text-gray-300">
    <!-- magnifying-glass icon -->
  </svg>
  <h3 class="mt-4 text-sm font-semibold text-gray-900">No results found</h3>
  <p class="mt-1 text-sm text-gray-500">Try different keywords or adjust your filters.</p>
</div>
```

### Empty Project
```html
<div class="text-center py-12 border-2 border-dashed border-gray-200 rounded-lg">
  <svg class="mx-auto h-12 w-12 text-gray-300">
    <!-- folder icon -->
  </svg>
  <h3 class="mt-4 text-sm font-semibold text-gray-900">No tasks in this project</h3>
  <p class="mt-1 text-sm text-gray-500">Add tasks to organize your work.</p>
</div>
```

## Error States

### Inline Error (Form Field)
```html
<div>
  <label for="title" class="block text-sm font-medium text-gray-700 mb-1">Title</label>
  <input type="text" id="title" name="title"
         class="w-full rounded-md border-red-300 shadow-sm focus:border-red-500 focus:ring-red-500 text-sm"
         aria-invalid="true" aria-describedby="title-error">
  <p class="mt-1 text-sm text-red-600" id="title-error">Title is required.</p>
</div>
```

### Alert Banner
```html
<div class="rounded-md bg-red-50 p-4">
  <div class="flex">
    <div class="flex-shrink-0">
      <svg class="h-5 w-5 text-red-400"><!-- exclamation-circle icon --></svg>
    </div>
    <div class="ml-3">
      <h3 class="text-sm font-medium text-red-800">There were errors with your submission</h3>
      <div class="mt-2 text-sm text-red-700">
        <ul class="list-disc pl-5 space-y-1">
          <li>Title is required</li>
          <li>Due date must be in the future</li>
        </ul>
      </div>
    </div>
  </div>
</div>
```

### Success Banner
```html
<div class="rounded-md bg-green-50 p-4">
  <div class="flex">
    <div class="flex-shrink-0">
      <svg class="h-5 w-5 text-green-400"><!-- check-circle icon --></svg>
    </div>
    <div class="ml-3">
      <p class="text-sm font-medium text-green-800">Task created successfully!</p>
    </div>
  </div>
</div>
```

## Modal Dialog

```html
<div x-data="{ open: false }">
  <!-- Trigger -->
  <button @click="open = true">Open Modal</button>

  <!-- Modal -->
  <div x-show="open" class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
    <!-- Backdrop -->
    <div x-show="open"
         x-transition:enter="ease-out duration-300"
         x-transition:enter-start="opacity-0"
         x-transition:enter-end="opacity-100"
         x-transition:leave="ease-in duration-200"
         x-transition:leave-start="opacity-100"
         x-transition:leave-end="opacity-0"
         class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"
         @click="open = false"></div>

    <!-- Panel -->
    <div class="fixed inset-0 z-10 overflow-y-auto">
      <div class="flex min-h-full items-center justify-center p-4">
        <div x-show="open"
             x-transition:enter="ease-out duration-300"
             x-transition:enter-start="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
             x-transition:enter-end="opacity-100 translate-y-0 sm:scale-100"
             x-transition:leave="ease-in duration-200"
             x-transition:leave-start="opacity-100 translate-y-0 sm:scale-100"
             x-transition:leave-end="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
             class="relative transform overflow-hidden rounded-lg bg-white shadow-xl transition-all sm:w-full sm:max-w-lg">

          <!-- Header -->
          <div class="px-6 py-4 border-b border-gray-200">
            <h3 class="text-lg font-semibold text-gray-900" id="modal-title">Modal Title</h3>
          </div>

          <!-- Content -->
          <div class="px-6 py-4">
            <p class="text-sm text-gray-500">Modal content goes here...</p>
          </div>

          <!-- Footer -->
          <div class="px-6 py-4 bg-gray-50 flex justify-end gap-3">
            <button @click="open = false"
                    class="rounded-md bg-white px-4 py-2 text-sm font-semibold text-gray-700 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50">
              Cancel
            </button>
            <button type="submit"
                    class="rounded-md bg-indigo-600 px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-700">
              Confirm
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
```

## Confirmation Dialog

For destructive actions like delete.

```html
<div x-data="{ open: false }">
  <!-- Delete button triggers dialog -->
  <button @click="open = true" class="text-red-600 hover:text-red-700">Delete</button>

  <!-- Confirmation Modal -->
  <div x-show="open" class="fixed inset-0 z-50" aria-labelledby="confirm-title" role="dialog" aria-modal="true">
    <div class="fixed inset-0 bg-gray-500 bg-opacity-75" @click="open = false"></div>

    <div class="fixed inset-0 flex items-center justify-center p-4">
      <div x-show="open" x-transition class="bg-white rounded-lg shadow-xl max-w-sm w-full p-6">
        <div class="flex items-start gap-4">
          <div class="flex-shrink-0 flex items-center justify-center h-10 w-10 rounded-full bg-red-100">
            <svg class="h-6 w-6 text-red-600"><!-- exclamation-triangle --></svg>
          </div>
          <div class="flex-1">
            <h3 class="text-lg font-semibold text-gray-900" id="confirm-title">Delete task?</h3>
            <p class="mt-2 text-sm text-gray-500">
              This action cannot be undone. This will permanently delete the task.
            </p>
          </div>
        </div>
        <div class="mt-6 flex justify-end gap-3">
          <button @click="open = false"
                  class="rounded-md bg-white px-4 py-2 text-sm font-semibold text-gray-700 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50">
            Cancel
          </button>
          <button @click="deleteTask(); open = false"
                  class="rounded-md bg-red-600 px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-red-700">
            Delete
          </button>
        </div>
      </div>
    </div>
  </div>
</div>
```

## Keyboard Shortcuts

Implement keyboard navigation for power users.

```javascript
// Global keyboard shortcuts
document.addEventListener('keydown', (e) => {
  // Ignore if typing in input/textarea
  if (['INPUT', 'TEXTAREA'].includes(document.activeElement.tagName)) return;

  switch(e.key) {
    case '/':
      e.preventDefault();
      document.getElementById('search-input').focus();
      break;
    case 'n':
      e.preventDefault();
      document.getElementById('quick-add-input').focus();
      break;
    case '?':
      // Show keyboard shortcuts help modal
      break;
  }
});
```

### Shortcut Help Display
```html
<div class="text-xs text-gray-400">
  <span class="bg-gray-100 rounded px-1.5 py-0.5 font-mono">/</span> Search
  <span class="ml-3 bg-gray-100 rounded px-1.5 py-0.5 font-mono">n</span> New task
  <span class="ml-3 bg-gray-100 rounded px-1.5 py-0.5 font-mono">?</span> Help
</div>
```
