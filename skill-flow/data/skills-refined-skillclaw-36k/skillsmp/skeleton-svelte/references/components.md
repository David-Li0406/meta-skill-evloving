# Skeleton Components Reference

## Component Composition Pattern

Skeleton components use a **composed pattern** with granular child elements. This allows passing arbitrary props and attributes directly to template elements, including `required`, `data-*`, `style`, and `class` attributes.

### Basic Pattern

```svelte
<ParentComponent>
  <ChildComponent.SubComponent>Content</ChildComponent.SubComponent>
</ParentComponent>
```

## Common Components

### Avatar

Display user profile images with fallback support.

```svelte
<script>
  import { Avatar } from '@skeletonlabs/skeleton-svelte';
</script>

<!-- With image -->
<Avatar>
  <Avatar.Image src="/avatar.jpg" alt="User Name" />
  <Avatar.Fallback>UN</Avatar.Fallback>
</Avatar>

<!-- Size variants -->
<Avatar class="h-8 w-8">
  <Avatar.Image src="/avatar.jpg" alt="Small" />
  <Avatar.Fallback>SM</Avatar.Fallback>
</Avatar>

<Avatar class="h-16 w-16">
  <Avatar.Image src="/avatar.jpg" alt="Large" />
  <Avatar.Fallback>LG</Avatar.Fallback>
</Avatar>

<!-- Themed styling -->
<Avatar class="ring-2 ring-primary-500">
  <Avatar.Image src="/avatar.jpg" alt="Themed" />
  <Avatar.Fallback class="bg-primary-500 text-primary-contrast-500">TH</Avatar.Fallback>
</Avatar>
```

### Button

Interactive buttons with variants and states.

```svelte
<script>
  import { Button } from '@skeletonlabs/skeleton-svelte';
</script>

<!-- Preset variants -->
<Button class="preset-filled-primary-500">Primary</Button>
<Button class="preset-tonal-secondary">Secondary</Button>
<Button class="preset-outlined-surface-300-700">Outlined</Button>

<!-- With icons -->
<Button class="preset-filled-primary-500">
  <svg><!-- Icon --></svg>
  Button Text
</Button>

<!-- States -->
<Button disabled class="preset-filled-primary-500">Disabled</Button>
<Button class="hover:preset-filled-primary-600 preset-filled-primary-500">Hover Effect</Button>

<!-- Sizes -->
<Button class="preset-filled-primary-500 px-3 py-1 text-sm">Small</Button>
<Button class="preset-filled-primary-500 px-4 py-2">Default</Button>
<Button class="preset-filled-primary-500 px-6 py-3 text-lg">Large</Button>

<!-- Full width -->
<Button class="w-full preset-filled-primary-500">Full Width</Button>
```

### Card

Container component for grouping related content.

```svelte
<script>
  import { Card } from '@skeletonlabs/skeleton-svelte';
</script>

<!-- Basic card -->
<Card class="preset-filled-surface-100-900">
  <Card.Header>
    <Card.Title>Card Title</Card.Title>
    <Card.Description>Optional description</Card.Description>
  </Card.Header>
  <Card.Content>
    <p class="text-surface-700-300">Main content goes here</p>
  </Card.Content>
  <Card.Footer class="flex justify-end gap-2">
    <Button class="preset-outlined-surface-300-700">Cancel</Button>
    <Button class="preset-filled-primary-500">Confirm</Button>
  </Card.Footer>
</Card>

<!-- Minimal card -->
<Card class="preset-outlined-surface-300-700 p-4">
  <Card.Content>
    <p>Simple card content</p>
  </Card.Content>
</Card>

<!-- Interactive card -->
<Card class="cursor-pointer preset-filled-surface-100-900 transition-shadow hover:shadow-lg">
  <Card.Content>
    <h3 class="text-lg font-semibold">Clickable Card</h3>
    <p class="text-surface-700-300">Click to navigate</p>
  </Card.Content>
</Card>
```

### Dialog (Modal)

Modal dialogs for focused user interactions.

```svelte
<script>
  import { Dialog, Button } from '@skeletonlabs/skeleton-svelte';
  let open = $state(false);
</script>

<Button onclick={() => (open = true)} class="preset-filled-primary-500">Open Dialog</Button>

<Dialog bind:open>
  <Dialog.Content class="bg-surface-50-950">
    <Dialog.Header>
      <Dialog.Title>Dialog Title</Dialog.Title>
      <Dialog.Description>Optional description text</Dialog.Description>
    </Dialog.Header>

    <Dialog.Body>
      <p class="text-surface-700-300">Dialog content goes here</p>
    </Dialog.Body>

    <Dialog.Footer class="flex justify-end gap-2">
      <Button onclick={() => (open = false)} class="preset-outlined-surface-300-700">Cancel</Button>
      <Button onclick={() => (open = false)} class="preset-filled-primary-500">Confirm</Button>
    </Dialog.Footer>
  </Dialog.Content>
</Dialog>
```

### Input and Label

Form input fields with labels.

```svelte
<script>
  import { Input, Label } from '@skeletonlabs/skeleton-svelte';
  let value = $state('');
</script>

<!-- Basic input -->
<div>
  <Label for="email">Email</Label>
  <Input
    id="email"
    type="email"
    bind:value
    placeholder="Enter your email"
    class="border-surface-300-700"
  />
</div>

<!-- With validation states -->
<div>
  <Label for="password">Password</Label>
  <Input
    id="password"
    type="password"
    bind:value
    aria-invalid={value.length < 8}
    class="border-surface-300-700"
  />
  {#if value.length < 8}
    <p class="mt-1 text-sm text-error-500">Password must be at least 8 characters</p>
  {/if}
</div>

<!-- Disabled state -->
<div>
  <Label for="disabled">Disabled Input</Label>
  <Input id="disabled" disabled value="Cannot edit" class="border-surface-300-700" />
</div>
```

### Select

Dropdown select menus.

```svelte
<script>
  import { Select, Label } from '@skeletonlabs/skeleton-svelte';
  let selected = $state('');
</script>

<div>
  <Label for="country">Country</Label>
  <Select id="country" bind:value={selected} class="border-surface-300-700">
    <option value="">Select a country</option>
    <option value="us">United States</option>
    <option value="uk">United Kingdom</option>
    <option value="ca">Canada</option>
  </Select>
</div>
```

### Checkbox and Radio

Selection controls for forms.

```svelte
<script>
  import { Checkbox, Radio, Label } from '@skeletonlabs/skeleton-svelte';
  let checked = $state(false);
  let selected = $state('');
</script>

<!-- Checkbox -->
<div class="flex items-center gap-2">
  <Checkbox id="terms" bind:checked class="text-primary-500" />
  <Label for="terms">I agree to the terms and conditions</Label>
</div>

<!-- Radio group -->
<fieldset>
  <legend class="mb-2 font-semibold">Choose an option</legend>

  <div class="flex items-center gap-2">
    <Radio id="option1" name="options" value="1" bind:group={selected} class="text-primary-500" />
    <Label for="option1">Option 1</Label>
  </div>

  <div class="flex items-center gap-2">
    <Radio id="option2" name="options" value="2" bind:group={selected} class="text-primary-500" />
    <Label for="option2">Option 2</Label>
  </div>
</fieldset>
```

### Badge

Small labels for statuses and categories.

```svelte
<script>
  import { Badge } from '@skeletonlabs/skeleton-svelte';
</script>

<!-- Status badges -->
<Badge class="preset-tonal-success">Active</Badge>
<Badge class="preset-tonal-warning">Pending</Badge>
<Badge class="preset-tonal-error">Inactive</Badge>

<!-- Category badges -->
<Badge class="preset-filled-primary-500">Featured</Badge>
<Badge class="preset-outlined-secondary-500">New</Badge>
```

## Advanced Component Patterns

### Provider Pattern

Most components support a provider approach for programmatic control using Zag.js APIs.

```svelte
<script>
  import { Dialog } from '@skeletonlabs/skeleton-svelte';

  let dialogApi;

  function openDialog() {
    dialogApi?.open();
  }

  function closeDialog() {
    dialogApi?.close();
  }
</script>

<Dialog.Provider bind:api={dialogApi}>
  <!-- Programmatic control of dialog -->
</Dialog.Provider>

<Button onclick={openDialog}>Open via API</Button>
```

### Custom Animation Integration

Components support custom animations through extensible markup patterns.

```svelte
<script>
  import { fade, slide } from 'svelte/transition';
  import { Dialog } from '@skeletonlabs/skeleton-svelte';
</script>

<Dialog bind:open>
  <Dialog.Content transition={fade}>
    <!-- Dialog with custom transition -->
  </Dialog.Content>
</Dialog>
```

### Element Prop for Custom HTML

The `element` prop enables custom HTML replacement (advanced feature).

```svelte
<script>
  import { Button } from '@skeletonlabs/skeleton-svelte';

  function customElement(attrs) {
    return `<a href="/link" ${attrs}>Custom Link Button</a>`;
  }
</script>

<Button element={customElement} class="preset-filled-primary-500">Button as Link</Button>
```

## Best Practices

1. **Use composed pattern** - Access child components for granular control
2. **Pass classes for styling** - Component classes get automatic precedence
3. **Leverage Svelte 5 runes** - Use `$state`, `$derived`, `$effect` for reactivity
4. **Apply theme-aware colors** - Use color pairings for consistent theming
5. **Semantic attributes** - Include aria-_ and data-_ attributes for accessibility
6. **Preset combinations** - Combine presets with additional Tailwind utilities
7. **State management** - Components use Zag.js internally for consistent behavior
