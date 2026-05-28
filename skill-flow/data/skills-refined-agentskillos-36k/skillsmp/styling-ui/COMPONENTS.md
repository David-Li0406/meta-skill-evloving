# UI Components Reference

Detailed component specifications for the todo-me application.

## Task Card

The primary component for displaying tasks in lists.

```html
<div class="bg-white shadow rounded-lg p-4 hover:shadow-md transition-shadow group">
  <!-- Checkbox + Title Row -->
  <div class="flex items-start gap-3">
    <input type="checkbox"
           class="mt-1 h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500">
    <div class="flex-1 min-w-0">
      <h3 class="text-sm font-medium text-gray-900 truncate">Task title here</h3>
      <p class="text-sm text-gray-500 mt-1 line-clamp-2">Optional description...</p>
    </div>
  </div>

  <!-- Metadata Row -->
  <div class="mt-3 flex items-center gap-2 text-sm text-gray-500">
    <!-- Priority stars -->
    <span class="text-yellow-500">★★★</span>

    <!-- Project chip -->
    <span class="inline-flex items-center gap-1 rounded-full px-2 py-0.5 text-xs bg-blue-100 text-blue-700">
      <span class="w-2 h-2 rounded-full bg-blue-500"></span>
      Work
    </span>

    <!-- Due date -->
    <span class="text-gray-500">Jan 24</span>
  </div>
</div>
```

### Task Card States

**Completed Task**:
```html
<div class="bg-white shadow rounded-lg p-4 opacity-60">
  <div class="flex items-start gap-3">
    <input type="checkbox" checked class="...">
    <h3 class="text-sm font-medium text-gray-500 line-through">Completed task</h3>
  </div>
</div>
```

**Overdue Task**:
```html
<div class="bg-white shadow rounded-lg p-4 border-l-4 border-red-500">
  <!-- Content with red date styling -->
  <span class="text-red-600 font-medium">Overdue: Jan 20</span>
</div>
```

**Selected Task** (for bulk actions):
```html
<div class="bg-indigo-50 shadow rounded-lg p-4 ring-2 ring-indigo-500">
```

## Priority Indicators

Display task priority (0-4 scale).

```html
<!-- Priority 0 (None): No indicator shown -->

<!-- Priority 1 (Low) -->
<span class="text-gray-400">★</span>

<!-- Priority 2 (Medium) -->
<span class="text-yellow-400">★★</span>

<!-- Priority 3 (High) -->
<span class="text-yellow-500">★★★</span>

<!-- Priority 4 (Urgent) -->
<span class="text-red-500">★★★★</span>
```

Alternative badge style:
```html
<span class="inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium bg-red-100 text-red-800">
  Urgent
</span>
```

## Project Chips

Display project assignment with color indicator.

```html
<!-- Standard project chip -->
<span class="inline-flex items-center gap-1.5 rounded-full px-2.5 py-0.5 text-xs font-medium bg-gray-100 text-gray-700">
  <span class="w-2 h-2 rounded-full" style="background-color: #3498db;"></span>
  Project Name
</span>

<!-- With hierarchy -->
<span class="inline-flex items-center gap-1.5 rounded-full px-2.5 py-0.5 text-xs font-medium bg-gray-100 text-gray-700">
  <span class="w-2 h-2 rounded-full" style="background-color: #e74c3c;"></span>
  Work / Meetings
</span>
```

## Tag Chips

Display tags with optional colors.

```html
<!-- Standard tag -->
<span class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium bg-gray-100 text-gray-700">
  @urgent
</span>

<!-- Colored tag -->
<span class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium"
      style="background-color: #fef3c7; color: #92400e;">
  @important
</span>

<!-- Removable tag (in forms) -->
<span class="inline-flex items-center gap-1 rounded-full pl-2.5 pr-1 py-0.5 text-xs font-medium bg-gray-100 text-gray-700">
  @work
  <button class="ml-1 rounded-full p-0.5 hover:bg-gray-200">
    <svg class="w-3 h-3"><!-- x icon --></svg>
  </button>
</span>
```

## Form Components

### Text Input
```html
<div>
  <label for="title" class="block text-sm font-medium text-gray-700 mb-1">Title</label>
  <input type="text" id="title" name="title"
         class="w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 text-sm"
         placeholder="Enter task title...">
</div>
```

### Textarea
```html
<div>
  <label for="description" class="block text-sm font-medium text-gray-700 mb-1">Description</label>
  <textarea id="description" name="description" rows="3"
            class="w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 text-sm"
            placeholder="Add details..."></textarea>
</div>
```

### Select
```html
<div>
  <label for="project" class="block text-sm font-medium text-gray-700 mb-1">Project</label>
  <select id="project" name="project"
          class="w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 text-sm">
    <option value="">No project</option>
    <option value="1">Work</option>
    <option value="2">Personal</option>
  </select>
</div>
```

### Checkbox
```html
<div class="flex items-center gap-2">
  <input type="checkbox" id="recurring" name="recurring"
         class="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500">
  <label for="recurring" class="text-sm text-gray-700">Recurring task</label>
</div>
```

### Date Picker
```html
<div>
  <label for="due_date" class="block text-sm font-medium text-gray-700 mb-1">Due Date</label>
  <input type="date" id="due_date" name="due_date"
         class="w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 text-sm">
</div>
```

## Buttons

### Primary Button
```html
<button type="submit"
        class="inline-flex items-center justify-center rounded-md bg-indigo-600 px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition-colors">
  Save Task
</button>
```

### Secondary Button
```html
<button type="button"
        class="inline-flex items-center justify-center rounded-md bg-white px-4 py-2 text-sm font-semibold text-gray-700 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition-colors">
  Cancel
</button>
```

### Danger Button
```html
<button type="button"
        class="inline-flex items-center justify-center rounded-md bg-red-600 px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 transition-colors">
  Delete
</button>
```

### Icon Button
```html
<button type="button"
        class="rounded-md p-2 text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-colors"
        aria-label="Edit task">
  <svg class="w-5 h-5"><!-- pencil icon --></svg>
</button>
```

### Button with Icon
```html
<button type="button"
        class="inline-flex items-center gap-2 rounded-md bg-indigo-600 px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-700 transition-colors">
  <svg class="w-5 h-5"><!-- plus icon --></svg>
  Add Task
</button>
```

## Dropdowns

### Standard Dropdown Menu
```html
<div x-data="{ open: false }" class="relative">
  <button @click="open = !open" @click.away="open = false"
          class="inline-flex items-center gap-2 rounded-md bg-white px-3 py-2 text-sm font-medium text-gray-700 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50">
    Options
    <svg class="w-4 h-4 text-gray-400"><!-- chevron-down --></svg>
  </button>

  <div x-show="open"
       x-transition:enter="transition ease-out duration-100"
       x-transition:enter-start="transform opacity-0 scale-95"
       x-transition:enter-end="transform opacity-100 scale-100"
       x-transition:leave="transition ease-in duration-75"
       x-transition:leave-start="transform opacity-100 scale-100"
       x-transition:leave-end="transform opacity-0 scale-95"
       class="absolute right-0 z-10 mt-2 w-56 origin-top-right rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
    <div class="py-1">
      <a href="#" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Edit</a>
      <a href="#" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Duplicate</a>
      <a href="#" class="block px-4 py-2 text-sm text-red-600 hover:bg-gray-100">Delete</a>
    </div>
  </div>
</div>
```
