# Accessible Component Patterns

Accessible, theme-aware component patterns for Tailwind CSS v4.1.

## Buttons

### Primary Button

```html
<button class="
  inline-flex items-center justify-center gap-2
  px-4 py-2 min-h-11
  bg-primary-500 text-white font-medium
  rounded-sm shadow-xs
  hover:bg-primary-600
  focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary-500
  disabled:bg-gray-300 disabled:text-gray-500 disabled:cursor-not-allowed
  dark:disabled:bg-gray-700 dark:disabled:text-gray-400
">
  Button text
</button>
```

### Secondary Button

```html
<button class="
  inline-flex items-center justify-center gap-2
  px-4 py-2 min-h-11
  bg-white text-gray-900 font-medium
  border border-gray-300
  rounded-sm shadow-xs
  hover:bg-gray-50
  focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary-500
  dark:bg-gray-800 dark:text-white dark:border-gray-600 dark:hover:bg-gray-700
">
  Button text
</button>
```

### Icon Button

```html
<button class="
  inline-flex items-center justify-center
  size-11 p-2
  text-gray-500 hover:text-gray-700
  rounded-sm
  hover:bg-gray-100
  focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary-500
  dark:text-gray-400 dark:hover:text-white dark:hover:bg-gray-800
">
  <svg class="size-5" aria-hidden="true">...</svg>
  <span class="sr-only">Close</span>
</button>
```

## Form Inputs

### Text Input

```html
<div>
  <label for="email" class="block text-sm/6 font-medium text-gray-900 dark:text-white">
    Email
  </label>
  <input
    type="email"
    id="email"
    class="
      mt-2 block w-full
      px-3 py-2
      bg-white text-gray-900 placeholder-gray-400
      border border-gray-300 rounded-sm shadow-xs
      focus:ring-2 focus:ring-primary-500 focus:border-primary-500
      dark:bg-gray-800 dark:text-white dark:placeholder-gray-500
      dark:border-gray-600 dark:focus:ring-primary-400
    "
    placeholder="you@example.com"
  />
</div>
```

### Input with Error

```html
<div>
  <label for="email-error" class="block text-sm/6 font-medium text-gray-900 dark:text-white">
    Email
  </label>
  <input
    type="email"
    id="email-error"
    aria-invalid="true"
    aria-describedby="email-error-message"
    class="
      mt-2 block w-full
      px-3 py-2
      bg-white text-gray-900
      border-2 border-red-500 rounded-sm
      focus:ring-2 focus:ring-red-500 focus:border-red-500
      dark:bg-gray-800 dark:text-white
    "
  />
  <p id="email-error-message" class="mt-2 text-sm text-red-600 dark:text-red-400" role="alert">
    Please enter a valid email address.
  </p>
</div>
```

### Select

```html
<div>
  <label for="country" class="block text-sm/6 font-medium text-gray-900 dark:text-white">
    Country
  </label>
  <select
    id="country"
    class="
      mt-2 block w-full
      px-3 py-2
      bg-white text-gray-900
      border border-gray-300 rounded-sm shadow-xs
      focus:ring-2 focus:ring-primary-500 focus:border-primary-500
      dark:bg-gray-800 dark:text-white dark:border-gray-600
    "
  >
    <option>United States</option>
    <option>Canada</option>
  </select>
</div>
```

### Checkbox

```html
<div class="flex items-center gap-3">
  <input
    type="checkbox"
    id="remember"
    class="
      size-4
      rounded-xs border-gray-300
      text-primary-500 
      focus:ring-2 focus:ring-primary-500 focus:ring-offset-2
      dark:border-gray-600 dark:bg-gray-800
      dark:focus:ring-offset-gray-900
    "
  />
  <label for="remember" class="text-sm/6 text-gray-900 dark:text-white">
    Remember me
  </label>
</div>
```

## Cards

### Basic Card

```html
<article class="
  bg-white rounded-sm shadow-sm
  border border-gray-200
  overflow-hidden
  dark:bg-gray-800 dark:border-gray-700
">
  <div class="p-6">
    <h3 class="text-lg/7 font-semibold text-gray-900 dark:text-white">
      Card Title
    </h3>
    <p class="mt-2 text-sm/6 text-gray-600 dark:text-gray-300">
      Card description text goes here.
    </p>
  </div>
</article>
```

### Interactive Card

```html
<a 
  href="#"
  class="
    block
    bg-white rounded-sm shadow-sm
    border border-gray-200
    overflow-hidden
    hover:shadow-md hover:border-gray-300
    focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary-500
    transition-shadow
    dark:bg-gray-800 dark:border-gray-700
    dark:hover:border-gray-600
  "
>
  <div class="p-6">
    <h3 class="text-lg/7 font-semibold text-gray-900 dark:text-white">
      Clickable Card
    </h3>
    <p class="mt-2 text-sm/6 text-gray-600 dark:text-gray-300">
      The entire card is clickable.
    </p>
  </div>
</a>
```

### Card with Image

```html
<article class="
  bg-white rounded-sm shadow-sm
  border border-gray-200
  overflow-hidden
  dark:bg-gray-800 dark:border-gray-700
">
  <img 
    src="image.jpg" 
    alt="Description of image"
    class="w-full h-48 object-cover"
  />
  <div class="p-6">
    <h3 class="text-lg/7 font-semibold text-gray-900 dark:text-white">
      Card Title
    </h3>
    <p class="mt-2 text-sm/6 text-gray-600 dark:text-gray-300">
      Card description text.
    </p>
  </div>
</article>
```

## Navigation

### Primary Navigation

```html
<nav aria-label="Main navigation" class="bg-white border-b border-gray-200 dark:bg-gray-900 dark:border-gray-700">
  <div class="max-w-7xl mx-auto px-4">
    <div class="flex items-center justify-between h-16">
      <a href="/" class="text-xl font-bold text-gray-900 dark:text-white">
        Logo
      </a>
      <ul class="flex items-center gap-1">
        <li>
          <a 
            href="#" 
            class="
              px-4 py-2 rounded-sm
              text-sm/6 font-medium
              text-gray-900 hover:bg-gray-100
              focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary-500
              dark:text-white dark:hover:bg-gray-800
            "
            aria-current="page"
          >
            Home
          </a>
        </li>
        <li>
          <a 
            href="#"
            class="
              px-4 py-2 rounded-sm
              text-sm/6 font-medium
              text-gray-600 hover:text-gray-900 hover:bg-gray-100
              focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary-500
              dark:text-gray-300 dark:hover:text-white dark:hover:bg-gray-800
            "
          >
            About
          </a>
        </li>
      </ul>
    </div>
  </div>
</nav>
```

### Skip Link

Always include a skip link for keyboard users:

```html
<a 
  href="#main-content"
  class="
    sr-only focus:not-sr-only
    focus:absolute focus:top-4 focus:left-4 focus:z-50
    focus:px-4 focus:py-2
    focus:bg-primary-500 focus:text-white
    focus:rounded-sm focus:shadow-lg
  "
>
  Skip to main content
</a>
```

### Breadcrumbs

```html
<nav aria-label="Breadcrumb">
  <ol class="flex items-center gap-2 text-sm/6">
    <li>
      <a href="#" class="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-white">
        Home
      </a>
    </li>
    <li aria-hidden="true" class="text-gray-400">/</li>
    <li>
      <a href="#" class="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-white">
        Products
      </a>
    </li>
    <li aria-hidden="true" class="text-gray-400">/</li>
    <li>
      <span class="text-gray-900 font-medium dark:text-white" aria-current="page">
        Current Page
      </span>
    </li>
  </ol>
</nav>
```

## Alerts

### Info Alert

```html
<div 
  role="alert"
  class="
    flex gap-3 p-4
    bg-blue-50 text-blue-800 
    border border-blue-200 rounded-sm
    dark:bg-blue-900/20 dark:text-blue-300 dark:border-blue-800
  "
>
  <svg class="size-5 shrink-0 mt-0.5" aria-hidden="true">...</svg>
  <div>
    <h4 class="font-medium">Information</h4>
    <p class="mt-1 text-sm/6">This is an informational message.</p>
  </div>
</div>
```

### Error Alert

```html
<div 
  role="alert"
  class="
    flex gap-3 p-4
    bg-red-50 text-red-800
    border border-red-200 rounded-sm
    dark:bg-red-900/20 dark:text-red-300 dark:border-red-800
  "
>
  <svg class="size-5 shrink-0 mt-0.5" aria-hidden="true">...</svg>
  <div>
    <h4 class="font-medium">Error</h4>
    <p class="mt-1 text-sm/6">Something went wrong. Please try again.</p>
  </div>
</div>
```

## Modals/Dialogs

### Dialog Structure

```html
<!-- Backdrop -->
<div 
  class="fixed inset-0 bg-black/50 dark:bg-black/70"
  aria-hidden="true"
></div>

<!-- Dialog -->
<div
  role="dialog"
  aria-modal="true"
  aria-labelledby="dialog-title"
  class="
    fixed inset-0 flex items-center justify-center p-4
  "
>
  <div class="
    w-full max-w-md
    bg-white rounded-sm shadow-xl
    dark:bg-gray-800
  ">
    <div class="p-6">
      <h2 id="dialog-title" class="text-lg/7 font-semibold text-gray-900 dark:text-white">
        Dialog Title
      </h2>
      <p class="mt-2 text-sm/6 text-gray-600 dark:text-gray-300">
        Dialog content goes here.
      </p>
    </div>
    <div class="flex justify-end gap-3 px-6 py-4 bg-gray-50 dark:bg-gray-900/50">
      <button class="px-4 py-2 text-sm font-medium text-gray-700 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white">
        Cancel
      </button>
      <button class="px-4 py-2 text-sm font-medium bg-primary-500 text-white rounded-sm hover:bg-primary-600">
        Confirm
      </button>
    </div>
  </div>
</div>
```

## Loading States

### Spinner

```html
<div role="status" class="flex items-center gap-2">
  <svg 
    class="size-5 animate-spin text-primary-500" 
    viewBox="0 0 24 24"
    aria-hidden="true"
  >
    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"/>
    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
  </svg>
  <span class="sr-only">Loading...</span>
</div>
```

### Skeleton

```html
<div class="animate-pulse">
  <div class="h-4 bg-gray-200 rounded-sm w-3/4 dark:bg-gray-700"></div>
  <div class="mt-2 h-4 bg-gray-200 rounded-sm w-1/2 dark:bg-gray-700"></div>
</div>
```

## Accessibility Checklist per Component

- [ ] Visible focus states with adequate contrast
- [ ] Proper ARIA attributes where needed
- [ ] Screen reader text for icon-only buttons
- [ ] Labels associated with form inputs
- [ ] Error states announced with `role="alert"`
- [ ] Light and dark mode both styled
- [ ] Minimum 44×44px touch targets
- [ ] Motion respects `prefers-reduced-motion`
