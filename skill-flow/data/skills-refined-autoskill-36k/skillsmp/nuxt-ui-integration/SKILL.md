---
name: nuxt-ui-integration
description: Verify correct Nuxt UI 4 component usage with MCP-first workflow. Use when adding Nuxt UI components or experiencing component issues.
---

# Nuxt UI Component Integration Skill

Verifies correct Nuxt UI 4 component usage with MCP-first workflow to prevent common mistakes.

## Purpose

USE this skill when:
- Adding new Nuxt UI component (UButton, UModal, UDropdownMenu, etc.)
- Uncertain about component API (props, slots, events)
- Experiencing issues with component behavior

## Critical Rules

⚠️ **MCP-first verification** - ALWAYS verify component API via MCP before implementation
⚠️ **Correct component names** - UDropdownMenu (not UDropdown), UFormField (not UFormGroup)
⚠️ **Proper event handlers** - onSelect for dropdown items (NOT click or onClick)
⚠️ **Slot structure matters** - UModal has specific slot hierarchy

## Workflow Steps

### Step 1: Identify Component Need
- Determine which Nuxt UI component is needed
- Verify correct component name

### Step 2: Fetch Component API via MCP
Execute: `mcp__nuxt-ui__get_component(componentName: "ComponentName")`

Review:
- Available props and types
- Slot structure and slot props
- Emitted events
- TypeScript types to import

### Step 3: Verify Props, Slots, and Events
Check all component API details before implementation

### Step 4: Check Component-Specific Patterns

**UModal Pattern:**
```vue
<UModal v-model:open="isOpen">
  <UButton label="Open" />
  <template #body>
    <UForm ref="form" @submit="handleSubmit">
      <!-- Form fields -->
    </UForm>
  </template>
  <template #footer="{ close }">
    <UButton @click="close" />
    <UButton @click="form?.submit()" />
  </template>
</UModal>
```

**UDropdownMenu Pattern:**
```vue
<script setup lang="ts">
import type { DropdownMenuItem } from "@nuxt/ui"

const items: DropdownMenuItem[] = [{
  label: "Edit",
  onSelect: () => handleEdit(), // ✅ onSelect, not click
}]
</script>
```

### Step 5: Import TypeScript Types
```typescript
import type { DropdownMenuItem, FormSubmitEvent } from "@nuxt/ui"
```

### Step 6: Implement Component
- Use verified API from MCP
- Add data-testid attributes
- Follow component-specific patterns

### Step 7: Verify Against Anti-Patterns
- UModal: Content in #body slot, NOT default
- UDropdownMenu: Use onSelect, NOT click
- UFormField: NOT UFormGroup

## References
- Nuxt UI integration: `.agents/nuxt-ui-4-integration.md`
- Frontend guidelines: `app/AGENTS.md`
