# Multi-Step Commands Example

Nested commands with breadcrumb navigation (Raycast-style).

## Features Demonstrated

- **Command chaining** - Select repository → Choose action → Execute
- **Breadcrumb trail** showing navigation path
- **Back navigation** with Backspace or ESC in empty search
- **State preservation** across command levels and palette close/open
- **Smooth transitions** between levels with slide animation
- **Dynamic commands** based on previous selections
- **Keyboard-first navigation** with arrow keys and shortcuts
- **Context-aware** level indicators and help text

## Key Implementation Details

### Command Stack

The `useCommandFlow` hook maintains a stack of selected commands to enable back navigation. Each command can define `nextLevel` commands that appear when selected.

```tsx
const {
  stack,           // Current command stack
  currentLevel,    // Depth in the tree (0-based)
  breadcrumb,      // Breadcrumb items for display
  currentCommands, // Commands at current level
  push,            // Navigate into command
  pop,             // Go back one level
  reset,           // Return to root
  navigateTo,      // Jump to specific level
} = useCommandFlow(rootCommands, onExecute, 'persist-key');
```

### Command Tree Structure

Commands are hierarchical with optional `nextLevel` arrays:

```tsx
interface Command {
  id: string;
  name: string;
  description?: string;
  icon?: React.ComponentType;
  action?: () => void | Promise<void>;  // Terminal action
  nextLevel?: Command[];                // Nested commands
}
```

- **Terminal commands**: Have `action`, no `nextLevel` → Execute and close
- **Navigation commands**: Have `nextLevel` → Push onto stack and show children
- **Hybrid commands**: Can have both for complex workflows

### Breadcrumb Navigation

Visual breadcrumb at top shows path like "Home → Repository → Actions":
- Click any breadcrumb item to jump to that level
- X button resets to root
- Auto-updates as user navigates

### Back Navigation

Multiple ways to go back:
1. **Backspace** in empty search → Pop one level
2. **ESC** in empty search → Pop one level
3. **ESC** with search → Clear search first, then pop
4. **Click breadcrumb** → Jump to specific level

### State Persistence

Optional localStorage persistence across sessions:

```tsx
<MultiStepPalette
  persistKey="repo-workflow"  // Saved to localStorage
  // ... other props
/>
```

State is cleared when palette closes with a terminal action.

## Usage Pattern

Best for complex workflows requiring multiple selections before executing an action.

### Common Use Cases

- **Repository/project management** - Select repo → Choose action → Confirm
- **Multi-tenant applications** - Select tenant → Choose resource → Execute
- **Nested configuration** - Select category → Choose setting → Adjust value
- **File operations** - Select directory → Choose file → Pick action
- **Deployment workflows** - Select environment → Choose service → Confirm deploy

### When to Use Multi-Step vs Single-Level

**Use multi-step when:**
- Workflow requires context from previous selections
- Actions apply to specific entities (repos, users, resources)
- Destructive actions need confirmation
- Options are too numerous for single list

**Use single-level when:**
- Actions are global (app-wide commands)
- No context dependencies between commands
- User knows exact command name (good search)

## Components

### `MultiStepPalette.tsx`

Main component with modal dialog, breadcrumb header, and keyboard navigation.

**Props:**
```tsx
interface MultiStepPaletteProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  rootCommands: Command[];
  onCommandExecute?: (command: Command) => void;
  persistKey?: string;
  placeholder?: string;
}
```

**Features:**
- Fuzzy search filtering at each level
- Arrow key navigation with auto-select
- Enter to execute selected command
- Smooth level transitions with opacity animation
- Footer with keyboard shortcuts and level indicator

### `CommandStep.tsx`

Individual step component for displaying commands at current level.

**Props:**
```tsx
interface CommandStepProps {
  commands: Command[];
  selectedId: string | null;
  onSelect: (command: Command) => void;
  isLoading?: boolean;
  description?: string;
  emptyMessage?: string;
}
```

**Features:**
- Icon + name + description layout
- Loading state with spinner
- Empty state with custom message
- Hover and selected states
- Scrollable list for many commands

### `useCommandFlow.ts`

Custom hook for managing multi-step state.

**Parameters:**
```tsx
function useCommandFlow(
  rootCommands: Command[],
  onCommandExecute?: (command: Command) => void,
  persistKey?: string
): UseCommandFlowResult
```

**Returns:**
```tsx
interface UseCommandFlowResult {
  stack: Command[];
  currentLevel: number;
  breadcrumb: BreadcrumbItem[];
  currentCommands: Command[];
  push: (command: Command) => void;
  pop: () => void;
  reset: () => void;
  navigateTo: (level: number) => void;
  executeCommand: (command: Command) => void;
}
```

### `mock-workflows.ts`

3-level command hierarchy for demonstration:
- **Level 0**: 5 repositories
- **Level 1**: 10 actions per repository (deploy, branches, settings, etc.)
- **Level 2**: Confirmation or branch selection

**Structure:**
```tsx
export const workflowTree: CommandTree = {
  repositories: [
    {
      name: 'web-app',
      nextLevel: [
        { name: 'Deploy', nextLevel: [confirm, cancel] },
        { name: 'Switch Branch', nextLevel: branches },
        { name: 'Create PR', action: () => {} },
        // ... more actions
      ]
    },
    // ... more repos
  ]
};
```

## Example Usage

### Basic Implementation

```tsx
import { MultiStepPalette } from './multi-step';
import { workflowTree } from './multi-step/mock-workflows';
import { useCommandPalette } from '@/hooks/useCommandPalette';

function App() {
  const { open, setOpen } = useCommandPalette();

  return (
    <MultiStepPalette
      open={open}
      onOpenChange={setOpen}
      rootCommands={workflowTree.repositories}
      onCommandExecute={(cmd) => {
        console.log('Executed:', cmd.name);
        // Track analytics, show toast, etc.
      }}
      persistKey="repo-workflow"
    />
  );
}
```

### Custom Workflow

```tsx
import { Command } from './multi-step';

const deployWorkflow: Command[] = [
  {
    id: 'prod',
    name: 'Production',
    description: 'Deploy to production environment',
    icon: Rocket,
    nextLevel: [
      {
        id: 'confirm-prod',
        name: 'Confirm Production Deploy',
        description: 'This will deploy to live users',
        icon: Check,
        action: async () => {
          await deployToProduction();
          toast.success('Deployed to production');
        },
      },
      {
        id: 'cancel',
        name: 'Cancel',
        icon: X,
      },
    ],
  },
  {
    id: 'staging',
    name: 'Staging',
    description: 'Deploy to staging environment',
    icon: FileText,
    action: async () => {
      await deployToStaging();
      toast.success('Deployed to staging');
    },
  },
];
```

### Loading Dynamic Commands

```tsx
function useRepositoryActions(repoId: string): Command[] {
  const { data, isLoading } = useQuery({
    queryKey: ['repo-actions', repoId],
    queryFn: () => fetchRepositoryActions(repoId),
  });

  return data?.map((action) => ({
    id: action.id,
    name: action.name,
    description: action.description,
    icon: getIconForAction(action.type),
    action: () => executeAction(action.id),
  })) ?? [];
}
```

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `↑` `↓` | Navigate through commands |
| `Enter` | Execute selected command |
| `Backspace` | Go back (empty search only) |
| `Escape` | Clear search or go back |
| `⌘K` | Open/close palette (global) |

## Adapting for Your Use Case

### 1. Define Your Command Tree

Identify your multi-step workflows:
```
Select X → Choose Y → Confirm Z
```

### 2. Create Command Hierarchy

Build nested command structure with `nextLevel` arrays:
```tsx
const myCommands: Command[] = [
  {
    id: 'parent',
    name: 'Parent Command',
    nextLevel: [
      { id: 'child1', name: 'Child 1', action: () => {} },
      { id: 'child2', name: 'Child 2', action: () => {} },
    ],
  },
];
```

### 3. Add Confirmations for Destructive Actions

Always confirm destructive operations:
```tsx
{
  id: 'delete',
  name: 'Delete Item',
  nextLevel: [
    {
      id: 'confirm-delete',
      name: 'Confirm Delete (DANGER)',
      action: () => deleteItem(),
    },
    {
      id: 'cancel',
      name: 'Cancel',
    },
  ],
}
```

### 4. Customize Breadcrumb Display

The breadcrumb automatically uses command names, but you can customize in `MultiStepPalette`:

```tsx
// Show more context in breadcrumb
<span>
  {crumb.name} ({someMetadata})
</span>
```

### 5. Add Loading States

Use `CommandStep` loading prop for async operations:
```tsx
<CommandStep
  isLoading={isFetching}
  commands={dynamicCommands}
  // ... other props
/>
```

## Performance Considerations

- **Lazy command loading**: Only load `nextLevel` commands when parent is selected
- **Memoize command trees**: Use `useMemo` for static command hierarchies
- **Debounce search**: Search filtering is real-time, consider debouncing for large lists
- **Virtual scrolling**: For 100+ commands at a level, add virtualization

## Testing

See `useCommandFlow.test.ts` for unit tests covering:
- Stack push/pop operations
- Breadcrumb generation
- State persistence
- Navigation to specific levels
- Command execution

## See Also

- **Design principles**: `../../references/design-principles.md`
- **State management**: `../../references/state-management.md`
- **Keyboard navigation**: `../../references/keyboard-navigation.md`
- **Single-level example**: `../action-palette/`
- **Server search example**: `../server-search/`
