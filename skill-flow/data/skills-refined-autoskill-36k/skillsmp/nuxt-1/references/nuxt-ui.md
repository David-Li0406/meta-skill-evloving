# Nuxt UI Reference

**Last Updated:** 2025-11 (v4.1.0)

**Check:** `@nuxt/ui` in package.json

Nuxt UI is a component library built on Tailwind CSS that provides pre-built, accessible UI components for Nuxt applications.

## Version Detection

Check `package.json` to determine which version is installed:

- **v4.x** - Latest version (Nuxt 4 required, Tailwind v4, breaking changes from v3)
- **v3.x** - Previous stable (Nuxt 3, Tailwind v3)
- **v2.x** - Legacy version (deprecated)

For v4-specific features and migration, verify with official docs: https://ui.nuxt.com

## Installation & Setup

### v4 Setup (Current)

**Prerequisites:**

- Nuxt 4+
- Tailwind CSS v4

```bash
pnpm add @nuxt/ui
```

**Required Configuration:**

1. **nuxt.config.ts:**

```typescript
export default defineNuxtConfig({
  modules: ["@nuxt/ui"],

  // Optional: Configure color theme
  colorMode: {
    preference: "system", // 'light' | 'dark' | 'system'
  },
})
```

2. **app.vue - UApp Wrapper (Required):**

```vue
<template>
  <UApp>
    <NuxtLayout>
      <NuxtPage />
    </NuxtLayout>
  </UApp>
</template>
```

3. **assets/css/main.css - Tailwind v4 Import:**

```css
@import "tailwindcss";
```

4. **app.config.ts - Color Configuration:**

```typescript
export default defineAppConfig({
  ui: {
    colors: {
      primary: "blue",
      neutral: "slate",
    },
  },
})
```

### v3 Setup (Previous Version)

```bash
pnpm add @nuxt/ui
```

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  modules: ["@nuxt/ui"],
})
```

```css
/* assets/css/main.css */
@tailwind base;
@tailwind components;
@tailwind utilities;
```

## Breaking Changes

### v3 → v4 Migration

**Component Renames:**

- `UButtonGroup` → `UFieldGroup`
- `UFormGroup` → `UFieldGroup`
- `UVerticalNavigation` → `UNavigationTree`

**Modal/Popover/Slideover Structure Changes:**
Major structural changes - trigger button now goes inside component, content uses `#content` slot:

```vue
<!-- v3 -->
<UButton @click="open = true">Open</UButton>
<UModal v-model="open">
  <div class="p-4">Content</div>
</UModal>

<!-- v4 -->
<UModal>
  <UButton>Open</UButton>
  <template #content>
    <template #header>Title</template>
    <template #body>Content</template>
    <template #footer>Footer</template>
  </template>
</UModal>
```

**Composable Changes:**

- `useModal()` → `useOverlay()`
- Overlays now close automatically on close events (no manual `.close()` needed)

**Color System:**
Configure colors in `app.config.ts` instead of component props:

```typescript
// app.config.ts (v4)
export default defineAppConfig({
  ui: {
    colors: {
      primary: "blue", // Changed from 'primary' prop on components
      neutral: "slate",
    },
  },
})
```

**Tailwind v4 Requirement:**

- Must use `@import "tailwindcss"` in main.css
- Tailwind config now uses CSS-based configuration

For complete migration details, check: https://ui.nuxt.com/getting-started/migration

### v2 → v3 Migration

Major overhaul with many breaking changes. Recommend checking official migration guide for projects still on v2.

## Common Components

### Forms

#### UInput

```vue
<template>
  <UInput
    v-model="email"
    type="email"
    placeholder="Enter your email"
    icon="i-heroicons-envelope"
  />
</template>

<script setup lang="ts">
const email = ref("")
</script>
```

#### UTextarea

```vue
<template>
  <UTextarea
    v-model="description"
    placeholder="Enter description..."
    :rows="4"
  />
</template>

<script setup lang="ts">
const description = ref("")
</script>
```

#### USelect

```vue
<template>
  <USelect
    v-model="selectedOption"
    :options="options"
    placeholder="Select an option"
  />
</template>

<script setup lang="ts">
const selectedOption = ref("")
const options = [
  { label: "Option 1", value: "opt1" },
  { label: "Option 2", value: "opt2" },
]
</script>
```

#### UCheckbox & URadio

```vue
<template>
  <div>
    <UCheckbox v-model="agreed" label="I agree to terms" />

    <URadioGroup v-model="plan">
      <URadio value="free" label="Free" />
      <URadio value="pro" label="Pro" />
    </URadioGroup>
  </div>
</template>

<script setup lang="ts">
const agreed = ref(false)
const plan = ref("free")
</script>
```

#### UFieldGroup (v4) / UFormGroup (v3)

```vue
<template>
  <!-- v4 -->
  <UFieldGroup label="Email" description="Your email address" required>
    <UInput v-model="email" type="email" />
  </UFieldGroup>

  <!-- v3 -->
  <UFormGroup label="Email" help="Your email address" required>
    <UInput v-model="email" type="email" />
  </UFormGroup>
</template>

<script setup lang="ts">
const email = ref("")
</script>
```

### Buttons

#### UButton

```vue
<template>
  <div class="flex gap-2">
    <!-- v4: Color defined in app.config.ts -->
    <UButton>Primary Button</UButton>
    <UButton variant="outline">Outline</UButton>
    <UButton variant="ghost">Ghost</UButton>
    <UButton size="sm" icon="i-heroicons-plus">Add</UButton>
    <UButton loading>Loading...</UButton>
    <UButton disabled>Disabled</UButton>
  </div>
</template>
```

#### UButtonGroup (v3) / UFieldGroup (v4)

```vue
<template>
  <!-- v3 -->
  <UButtonGroup>
    <UButton>One</UButton>
    <UButton>Two</UButton>
    <UButton>Three</UButton>
  </UButtonGroup>

  <!-- v4: Use flex utilities or UFieldGroup -->
  <div
    class="flex gap-0 [&>button]:rounded-none [&>button:first-child]:rounded-l [&>button:last-child]:rounded-r"
  >
    <UButton>One</UButton>
    <UButton>Two</UButton>
    <UButton>Three</UButton>
  </div>
</template>
```

### Overlays

#### UModal

```vue
<template>
  <!-- v4: Trigger button inside Modal, content in #content slot -->
  <UModal>
    <UButton>Open Modal</UButton>

    <template #content>
      <template #header>
        <h3>Modal Title</h3>
      </template>

      <template #body>
        <p>Modal content goes here...</p>
      </template>

      <template #footer>
        <div class="flex justify-end gap-2">
          <UButton variant="outline">Cancel</UButton>
          <UButton @click="handleSubmit">Submit</UButton>
        </div>
      </template>
    </template>
  </UModal>

  <!-- v3 (old structure) -->
  <div>
    <UButton @click="isOpen = true">Open Modal</UButton>

    <UModal v-model="isOpen">
      <UCard>
        <template #header>
          <h3>Modal Title</h3>
        </template>

        <p>Modal content goes here...</p>

        <template #footer>
          <div class="flex justify-end gap-2">
            <UButton variant="outline" @click="isOpen = false">Cancel</UButton>
            <UButton @click="handleSubmit">Submit</UButton>
          </div>
        </template>
      </UCard>
    </UModal>
  </div>
</template>

<script setup lang="ts">
function handleSubmit() {
  // Handle submission
}
</script>
```

#### UPopover

```vue
<template>
  <!-- v4: Similar structure to Modal -->
  <UPopover>
    <UButton>Open Popover</UButton>

    <template #content>
      <div class="p-4">
        <p>Popover content</p>
      </div>
    </template>
  </UPopover>

  <!-- v3 (old structure) -->
  <div>
    <UButton @click="isPopoverOpen = true">Open Popover</UButton>

    <UPopover v-model="isPopoverOpen">
      <div class="p-4">
        <p>Popover content</p>
      </div>
    </UPopover>
  </div>
</template>

<script setup lang="ts">
// v4: No state management needed
// v3: const isPopoverOpen = ref(false)
</script>
```

#### UTooltip

```vue
<template>
  <UTooltip text="Helpful tooltip">
    <UButton icon="i-heroicons-information-circle" />
  </UTooltip>
</template>
```

### Navigation

#### ULink

```vue
<template>
  <div>
    <!-- Internal link -->
    <ULink to="/about">About Us</ULink>

    <!-- External link -->
    <ULink to="https://example.com" target="_blank"> External Link </ULink>

    <!-- With icon -->
    <ULink to="/settings" icon="i-heroicons-cog"> Settings </ULink>
  </div>
</template>
```

#### UTabs

```vue
<template>
  <UTabs v-model="selectedTab" :items="tabs">
    <template #account>
      <div class="p-4">Account settings content</div>
    </template>

    <template #security>
      <div class="p-4">Security settings content</div>
    </template>
  </UTabs>
</template>

<script setup lang="ts">
const selectedTab = ref("account")
const tabs = [
  { key: "account", label: "Account" },
  { key: "security", label: "Security" },
]
</script>
```

#### UBreadcrumb

```vue
<template>
  <UBreadcrumb :items="breadcrumbs" />
</template>

<script setup lang="ts">
const route = useRoute()

const breadcrumbs = computed(() => [
  { label: "Home", to: "/" },
  { label: "Products", to: "/products" },
  { label: route.params.id as string },
])
</script>
```

### Data Display

#### UCard

```vue
<template>
  <UCard>
    <template #header>
      <h3>Card Title</h3>
    </template>

    <p>Card body content goes here.</p>

    <template #footer>
      <div class="flex justify-end gap-2">
        <UButton>Action</UButton>
      </div>
    </template>
  </UCard>
</template>
```

#### UTable

```vue
<template>
  <UTable :columns="columns" :rows="users">
    <template #name-data="{ row }">
      <span class="font-medium">{{ row.name }}</span>
    </template>

    <template #actions-data="{ row }">
      <UButton size="xs" @click="editUser(row)">Edit</UButton>
    </template>
  </UTable>
</template>

<script setup lang="ts">
const columns = [
  { key: "name", label: "Name" },
  { key: "email", label: "Email" },
  { key: "actions", label: "Actions" },
]

const users = ref([
  { id: 1, name: "John Doe", email: "john@example.com" },
  { id: 2, name: "Jane Smith", email: "jane@example.com" },
])

function editUser(user: any) {
  // Handle edit
}
</script>
```

#### UBadge

```vue
<template>
  <div class="flex gap-2">
    <UBadge>Default</UBadge>
    <UBadge variant="subtle">Subtle</UBadge>
    <UBadge size="sm">Small</UBadge>
  </div>
</template>
```

#### UAlert

```vue
<template>
  <div class="space-y-2">
    <UAlert
      title="Success"
      description="Your changes have been saved."
      icon="i-heroicons-check-circle"
    />

    <UAlert
      title="Error"
      description="Something went wrong."
      variant="error"
      icon="i-heroicons-x-circle"
    />
  </div>
</template>
```

### Feedback

#### UNotification (Toast)

```vue
<template>
  <UButton @click="showToast">Show Toast</UButton>
</template>

<script setup lang="ts">
const toast = useToast()

function showToast() {
  toast.add({
    title: "Success",
    description: "Your action was successful!",
    timeout: 3000,
  })
}
</script>
```

#### UProgress

```vue
<template>
  <div>
    <UProgress :value="progress" :max="100" />
    <UButton @click="progress += 10">Increase</UButton>
  </div>
</template>

<script setup lang="ts">
const progress = ref(30)
</script>
```

## Form Validation

### Using with Zod (Recommended)

```vue
<template>
  <UForm :state="state" :schema="schema" @submit="onSubmit">
    <UFieldGroup label="Email" name="email" required>
      <UInput v-model="state.email" type="email" />
    </UFieldGroup>

    <UFieldGroup label="Password" name="password" required>
      <UInput v-model="state.password" type="password" />
    </UFieldGroup>

    <UButton type="submit">Submit</UButton>
  </UForm>
</template>

<script setup lang="ts">
import { z } from "zod"

const schema = z.object({
  email: z.string().email("Invalid email address"),
  password: z.string().min(8, "Password must be at least 8 characters"),
})

const state = reactive({
  email: "",
  password: "",
})

async function onSubmit() {
  // Form is validated, handle submission
  console.log("Valid form data:", state)
}
</script>
```

## Composables

### useToast

Show toast notifications:

```vue
<script setup lang="ts">
const toast = useToast()

function notify() {
  toast.add({
    title: "Success",
    description: "Operation completed",
    icon: "i-heroicons-check-circle",
    timeout: 5000,
    color: "success",
  })
}
</script>
```

### useOverlay

Programmatically control overlays (modals, slidevers, drawers):

```vue
<script setup lang="ts">
const overlay = useOverlay()

// Open a modal component programmatically
async function openConfirm() {
  const result = await overlay.create(ConfirmDialog, {
    title: "Confirm Action",
    message: "Are you sure?",
  })
  if (result) {
    // User confirmed
  }
}
</script>
```

### defineShortcuts

Define keyboard shortcuts:

```vue
<script setup lang="ts">
defineShortcuts({
  // Simple shortcut
  meta_k: () => openSearch(),
  // With modifier
  ctrl_shift_p: () => openCommandPalette(),
  // Escape to close
  escape: () => closeModal(),
})
</script>
```

### useFormField

Integrate custom inputs with UForm validation:

```vue
<script setup lang="ts">
// Inside custom input component
const { inputId, name, error, ...field } = useFormField()
</script>

<template>
  <div>
    <input :id="inputId" :name="name" v-bind="field" />
    <span v-if="error">{{ error }}</span>
  </div>
</template>
```

## Additional Components

Nuxt UI v4 includes 100+ components. Key categories beyond basics:

### Dashboard Components

Pre-built dashboard layout system:

```vue
<template>
  <UDashboardGroup>
    <UDashboardSidebar collapsible>
      <UDashboardSidebarToggle />
      <UNavigationTree :items="navItems" />
    </UDashboardSidebar>

    <UDashboardPanel>
      <UDashboardNavbar>
        <template #left>
          <UDashboardSearchButton />
        </template>
      </UDashboardNavbar>

      <UDashboardToolbar>
        <!-- Toolbar content -->
      </UDashboardToolbar>

      <slot />
    </UDashboardPanel>
  </UDashboardGroup>
</template>
```

Components: `UDashboardGroup`, `UDashboardSidebar`, `UDashboardPanel`, `UDashboardNavbar`, `UDashboardToolbar`, `UDashboardSearch`, `UDashboardResizeHandle`

### Chat Components (AI Integration)

For building AI chat interfaces (Vercel AI SDK compatible):

```vue
<template>
  <UChatMessages :messages="messages">
    <template #message="{ message }">
      <UChatMessage
        :content="message.content"
        :role="message.role"
        :avatar="message.role === 'user' ? userAvatar : aiAvatar"
      />
    </template>
  </UChatMessages>

  <UChatPrompt v-model="input" @submit="sendMessage">
    <template #submit>
      <UChatPromptSubmit :loading="isLoading" />
    </template>
  </UChatPrompt>
</template>
```

Components: `UChatMessage`, `UChatMessages`, `UChatPrompt`, `UChatPromptSubmit`, `UChatPalette`

### Calendar & Date Components

```vue
<template>
  <UCalendar v-model="selectedDate" />

  <UInputDate v-model="date" placeholder="Select date" />
</template>
```

### Page Layout Components

Pre-built page sections for marketing/docs sites:

```vue
<template>
  <UPageHero title="Welcome" description="Build faster with Nuxt UI">
    <template #actions>
      <UButton>Get Started</UButton>
    </template>
  </UPageHero>

  <UPageSection>
    <UPageGrid>
      <UPageCard title="Feature 1" description="..." />
      <UPageCard title="Feature 2" description="..." />
    </UPageGrid>
  </UPageSection>
</template>
```

Components: `UPage`, `UPageHero`, `UPageSection`, `UPageGrid`, `UPageCard`, `UPageFeature`, `UPageCTA`, `UPageColumns`

### Other Notable Components

- `UCommandPalette` - Fuzzy search command menu
- `UTree` - Hierarchical data display
- `UTimeline` - Event sequences
- `UStepper` - Multi-step processes
- `UFileUpload` - File upload with drag-drop
- `UColorPicker` - Color selection
- `UDrawer` - Sliding panel

Full component list: https://ui.nuxt.com/components

## Theming & Customization

### Color Configuration (v4)

```typescript
// app.config.ts
export default defineAppConfig({
  ui: {
    colors: {
      primary: "blue",
      secondary: "purple",
      success: "green",
      warning: "yellow",
      error: "red",
      neutral: "slate",
    },
  },
})
```

### Component Styling

Override component styles using Tailwind classes:

```vue
<template>
  <UButton
    class="custom-button"
    :ui="{
      base: 'font-bold',
      rounded: 'rounded-full',
      size: { sm: 'px-4 py-2' },
    }"
  >
    Custom Styled Button
  </UButton>
</template>
```

### Dark Mode

Nuxt UI automatically supports dark mode when `@nuxtjs/color-mode` is configured:

```vue
<template>
  <div>
    <!-- Components automatically adapt to dark mode -->
    <UCard>
      <p>This card adapts to light/dark mode</p>
    </UCard>

    <!-- Toggle dark mode -->
    <UButton @click="toggleDark"> Toggle Dark Mode </UButton>
  </div>
</template>

<script setup lang="ts">
const colorMode = useColorMode()

function toggleDark() {
  colorMode.preference = colorMode.value === "dark" ? "light" : "dark"
}
</script>
```

## Nuxt UI-Specific Tailwind Configuration

When using Nuxt UI v4 with Tailwind v4, the Tailwind setup is automatically configured by the module. However, you may need custom configuration:

### Custom Tailwind Classes with Nuxt UI

```css
/* assets/css/main.css */
@import "tailwindcss";

/* Custom utilities that work with Nuxt UI */
@layer utilities {
  .text-gradient {
    @apply bg-gradient-to-r from-blue-500 to-purple-500 bg-clip-text text-transparent;
  }
}
```

### Extending Nuxt UI Colors

```typescript
// tailwind.config.ts
import type { Config } from "tailwindcss"

export default {
  theme: {
    extend: {
      colors: {
        // Add custom colors that integrate with Nuxt UI
        brand: {
          50: "#f0f9ff",
          100: "#e0f2fe",
          // ... more shades
          900: "#0c4a6e",
        },
      },
    },
  },
} satisfies Config
```

Reference `app.config.ts` to use custom color in Nuxt UI:

```typescript
// app.config.ts
export default defineAppConfig({
  ui: {
    colors: {
      primary: "brand", // Use custom Tailwind color
    },
  },
})
```

## Common Patterns

### Loading States

```vue
<template>
  <div>
    <UButton :loading="isLoading" @click="handleAction"> Submit </UButton>
  </div>
</template>

<script setup lang="ts">
const isLoading = ref(false)

async function handleAction() {
  isLoading.value = true
  try {
    await $fetch("/api/action")
  } finally {
    isLoading.value = false
  }
}
</script>
```

### Confirmation Dialogs

```vue
<template>
  <!-- v4 structure -->
  <UModal>
    <UButton>Delete</UButton>

    <template #content>
      <template #header>
        <h3>Confirm Deletion</h3>
      </template>

      <template #body>
        <p>Are you sure you want to delete this item?</p>
      </template>

      <template #footer>
        <div class="flex justify-end gap-2">
          <UButton variant="outline">Cancel</UButton>
          <UButton variant="error" @click="handleDelete">Delete</UButton>
        </div>
      </template>
    </template>
  </UModal>
</template>

<script setup lang="ts">
async function handleDelete() {
  // Perform deletion
  // Modal closes automatically
}
</script>
```

### Data Tables with Actions

```vue
<template>
  <UTable :columns="columns" :rows="items" :loading="pending">
    <template #actions-data="{ row }">
      <UDropdown :items="getActions(row)">
        <UButton icon="i-heroicons-ellipsis-horizontal" variant="ghost" />
      </UDropdown>
    </template>
  </UTable>
</template>

<script setup lang="ts">
const columns = [
  { key: "name", label: "Name" },
  { key: "status", label: "Status" },
  { key: "actions", label: "" },
]

const { data: items, pending } = await useFetch("/api/items")

function getActions(row: any) {
  return [
    [
      {
        label: "Edit",
        icon: "i-heroicons-pencil",
        click: () => editItem(row),
      },
    ],
    [
      {
        label: "Delete",
        icon: "i-heroicons-trash",
        click: () => deleteItem(row),
      },
    ],
  ]
}

function editItem(item: any) {
  // Handle edit
}

function deleteItem(item: any) {
  // Handle delete
}
</script>
```

## Icons

Nuxt UI v4 uses Iconify with the `i-` prefix:

```vue
<template>
  <div>
    <!-- Heroicons (default icon set) -->
    <UButton icon="i-heroicons-home">Home</UButton>

    <!-- Material Design Icons -->
    <UButton icon="i-mdi-github">GitHub</UButton>

    <!-- Font Awesome -->
    <UButton icon="i-fa-brands-twitter">Twitter</UButton>
  </div>
</template>
```

Browse icons at: https://icones.js.org

## Best Practices

1. **Wrap app with UApp (v4)** - Required for proper functioning
2. **Use v-model:open for modals** (v4) - Breaking change from v3
3. **Configure colors in app.config.ts** (v4) - Centralized theming
4. **Check package.json version** - Use version-appropriate syntax
5. **Leverage auto-completion** - TypeScript types are fully supported
6. **Use built-in validation** - Integrate with Zod for form validation
7. **Prefer composition** - Use slots and composables over prop overload
8. **Follow Tailwind patterns** - Nuxt UI components accept Tailwind classes
9. **Test dark mode** - Verify components in both light and dark modes

## Troubleshooting

### Common Issues (v4)

**Missing UApp wrapper:**

```
Error: Nuxt UI components require <UApp> wrapper
```

Solution: Wrap your app in `app.vue`:

```vue
<template>
  <UApp>
    <NuxtLayout>
      <NuxtPage />
    </NuxtLayout>
  </UApp>
</template>
```

**Tailwind not working:**
Ensure `main.css` has:

```css
@import "tailwindcss";
```

**v-model not working on Modal:**
Use `v-model:open` instead of `v-model` in v4.

## Migration Checklist

When upgrading from v3 to v4:

- [ ] Upgrade to Nuxt 4
- [ ] Install Tailwind CSS v4
- [ ] Update `main.css` to use `@import "tailwindcss"`
- [ ] Wrap app with `<UApp>` in `app.vue`
- [ ] Move color config to `app.config.ts`
- [ ] Update `v-model` to `v-model:open` on Modal/Popover/Dialog
- [ ] Rename `UButtonGroup` → `UFieldGroup`
- [ ] Rename `UFormGroup` → `UFieldGroup`
- [ ] Rename `UVerticalNavigation` → `UNavigationTree`
- [ ] Test all components in both light and dark mode
- [ ] Review official migration guide for additional breaking changes

## Official Resources

- **Documentation:** https://ui.nuxt.com
- **Migration Guide:** https://ui.nuxt.com/getting-started/migration
- **Component Reference:** https://ui.nuxt.com/components
- **GitHub:** https://github.com/nuxt/ui
- **Iconify Icons:** https://icones.js.org

---

**Note:** Verify version-specific syntax with official documentation at https://ui.nuxt.com. This reference covers v3 and v4, but breaking changes may occur in future releases.
