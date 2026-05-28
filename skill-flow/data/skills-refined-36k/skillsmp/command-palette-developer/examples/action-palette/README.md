# Action Palette Example

A production-ready action launcher with 40+ commands, keyboard shortcuts, and category grouping. Similar to VS Code's command palette or Sublime Text's command menu.

## Features Demonstrated

- **40+ realistic app commands** organized into 5 categories
- **Keyboard shortcuts** displayed and functional (⌘N, ⌘S, etc.)
- **Icon support** for visual command identification (Lucide React icons)
- **Single-column layout** optimized for action execution
- **Category grouping** with visual separators and headers
- **Smart search** across command names, descriptions, and categories
- **Platform-aware shortcuts** (⌘ on Mac, Ctrl on Windows)
- **Quick actions** with Cmd+1-9 for instant execution
- **Accessibility** with proper ARIA attributes and screen reader support
- **Disabled state** styling for unavailable commands
- **Destructive actions** with warning styling (delete/remove)

## Installation

```bash
# Install dependencies
pnpm add lucide-react

# Copy files to your project
cp -r .claude/skills/creating-command-palettes/examples/action-palette src/components/
```

## Quick Start

### 1. Register Your Commands

```tsx
import { registerMultiple } from '@/components/action-palette';
import { mockActions } from '@/components/action-palette';

// Register all mock commands
registerMultiple(mockActions);

// Or register individual commands
registerCommand({
  id: 'my-custom-action',
  name: 'My Custom Action',
  description: 'Does something cool',
  category: 'Actions',
  icon: Zap,
  shortcut: 'command+shift+x',
  action: () => {
    // Your action logic here
    console.log('Action executed!');
  },
});
```

### 2. Add the Action Palette to Your App

```tsx
import { useState } from 'react';
import { ActionPalette } from '@/components/action-palette';

function App() {
  const [isPaletteOpen, setIsPaletteOpen] = useState(false);

  // Listen for Cmd+K to open palette
  useEffect(() => {
    function handleKeyDown(e: KeyboardEvent) {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        setIsPaletteOpen(true);
      }
    }

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, []);

  return (
    <>
      <YourAppContent />

      <ActionPalette
        isOpen={isPaletteOpen}
        onClose={() => setIsPaletteOpen(false)}
      />
    </>
  );
}
```

## Components

### ActionPalette.tsx

Main modal component with search, keyboard navigation, and command execution.

**Props:**
- `isOpen: boolean` - Controls visibility
- `onClose: () => void` - Called when palette should close

**Features:**
- Search filter across all command metadata
- Arrow key navigation (↑↓ to navigate, ↵ to select, Esc to close)
- Quick actions (⌘1-9 to execute first 9 commands)
- Category grouping when not searching
- Flat list when searching
- Smooth scrolling to keep selection visible
- Focus trap to keep keyboard navigation within palette

### ActionResult.tsx

Individual command item with icon, name, description, and keyboard shortcut.

**Props:**
- `action: AppAction` - Command to display
- `isSelected: boolean` - Whether this command is currently selected
- `onClick: () => void` - Called when command is clicked

**Features:**
- Icon display (Lucide React icons)
- Keyboard shortcut formatting with platform detection
- Disabled state styling
- Destructive action warning (red text for dangerous operations)
- Hover and selection states
- Truncated descriptions for long text

### actions-registry.ts

Centralized command registry for managing all app commands.

**Core Functions:**

```tsx
// Register a single command
registerCommand(action: AppAction): void

// Remove a command
unregisterCommand(id: string): void

// Get all commands
getCommands(): AppAction[]

// Get commands grouped by category
getCommandsByCategory(): Record<string, AppAction[]>

// Search commands
searchCommands(query: string): AppAction[]

// Enable/disable commands dynamically
enableCommand(id: string): void
disableCommand(id: string): void

// Clear all commands
clearCommands(): void

// Register multiple commands at once
registerMultiple(actions: AppAction[]): void
```

**AppAction Interface:**

```tsx
interface AppAction {
  id: string;                    // Unique identifier
  name: string;                  // Display name
  description?: string;          // Optional description
  icon?: LucideIcon;            // Optional Lucide icon component
  shortcut?: string;            // Optional keyboard shortcut (e.g., "command+n")
  category: 'Navigation' | 'Actions' | 'Create' | 'Settings' | 'Help';
  action: () => void | Promise<void>;  // Function to execute
  disabled?: boolean;           // Whether command is currently disabled
  destructive?: boolean;        // Whether action is destructive (delete, remove)
}
```

### mock-actions.ts

45 realistic application commands demonstrating various use cases.

**Categories:**
- **Navigation (10 commands)** - Dashboard, Settings, Profile, Projects, Documents, Search, Notifications, Inbox, Calendar, Activity
- **Actions (12 commands)** - Save, Copy, Delete, Edit, Share, Archive, Star, Bookmark, Deploy, Run Tests, Export, Refresh
- **Create (10 commands)** - New Project, File, Folder, User, Team, Workspace, Database, Deployment, Tag, Branch
- **Settings (8 commands)** - Theme, Language, Keyboard, Account, Privacy, Notifications, Integrations, Advanced
- **Help (5 commands)** - Documentation, Keyboard Shortcuts, Support, Bug Report, Feedback

## Keyboard Shortcuts

### Global Shortcuts

| Shortcut | Action |
|----------|--------|
| ⌘K / Ctrl+K | Open/close palette |
| Esc | Close palette |
| ↑ / ↓ | Navigate commands |
| ↵ (Enter) | Execute selected command |
| Home | Jump to first command |
| End | Jump to last command |
| ⌘⌫ / Ctrl+Backspace | Clear search query |
| ⌘1-9 / Ctrl+1-9 | Quick execute first 9 commands |

### Command-Specific Shortcuts

Commands can define their own shortcuts that work globally when palette is closed:

```tsx
{
  id: 'action-save',
  name: 'Save',
  shortcut: 'command+s',  // Works globally when palette is closed
  action: () => save(),
}
```

## Usage Patterns

### Feature-Based Command Registration

Each feature can register its own commands when mounted:

```tsx
// features/projects/useProjectCommands.ts
import { useEffect } from 'react';
import { registerCommand, unregisterCommand } from '@/components/action-palette';
import { FolderOpen, Plus, Trash2 } from 'lucide-react';

export function useProjectCommands() {
  useEffect(() => {
    registerCommand({
      id: 'projects-view',
      name: 'View Projects',
      category: 'Navigation',
      icon: FolderOpen,
      action: () => navigate('/projects'),
    });

    registerCommand({
      id: 'projects-create',
      name: 'New Project',
      category: 'Create',
      icon: Plus,
      shortcut: 'command+shift+n',
      action: () => openCreateProjectModal(),
    });

    return () => {
      unregisterCommand('projects-view');
      unregisterCommand('projects-create');
    };
  }, []);
}
```

### Dynamic Enable/Disable

Enable or disable commands based on app state:

```tsx
import { enableCommand, disableCommand } from '@/components/action-palette';

function useCommandState() {
  const { hasSelection } = useSelection();

  useEffect(() => {
    if (hasSelection) {
      enableCommand('action-delete');
      enableCommand('action-copy');
    } else {
      disableCommand('action-delete');
      disableCommand('action-copy');
    }
  }, [hasSelection]);
}
```

### Context-Aware Actions

Commands can access app context when executed:

```tsx
registerCommand({
  id: 'export-current-view',
  name: 'Export Current View',
  category: 'Actions',
  icon: Download,
  action: () => {
    // Access current app state
    const currentData = store.getCurrentViewData();
    exportToCSV(currentData);
  },
});
```

## Customization

### Styling

The components use Tailwind CSS with dark mode support. Customize by modifying the classes:

```tsx
// Change primary color from blue to purple
className={`
  ${isSelected
    ? 'bg-purple-50 dark:bg-purple-900/20'  // Changed from blue
    : 'hover:bg-gray-50 dark:hover:bg-gray-800'
  }
`}
```

### Custom Icons

Use any Lucide React icon or create custom icon components:

```tsx
import { MyCustomIcon } from '@/icons';

registerCommand({
  id: 'custom-action',
  name: 'Custom Action',
  icon: MyCustomIcon,  // Must be a React component
  // ...
});
```

### Custom Categories

Add new categories by extending the type:

```tsx
// In actions-registry.ts
type Category = 'Navigation' | 'Actions' | 'Create' | 'Settings' | 'Help' | 'Custom';

// Then in getCommandsByCategory, add the new category
const commandsByCategory: Record<string, AppAction[]> = {
  Navigation: [],
  Actions: [],
  Create: [],
  Settings: [],
  Help: [],
  Custom: [],  // New category
};
```

## Testing

Run the included Vitest tests:

```bash
pnpm test actions-registry.test.ts
```

**Test coverage:**
- Command registration and unregistration
- Search functionality with prioritization
- Category grouping
- Enable/disable commands
- Multiple command registration
- Singleton instance behavior

## Best Practices

1. **Use semantic categories** - Group related commands together
2. **Provide descriptions** - Help users understand what each command does
3. **Choose meaningful shortcuts** - Avoid conflicts with browser shortcuts
4. **Add icons** - Visual cues improve scannability
5. **Disable unavailable actions** - Don't show commands that can't be executed
6. **Mark destructive actions** - Warn users about dangerous operations
7. **Test keyboard navigation** - Ensure all commands are keyboard accessible
8. **Register commands per feature** - Keep command registration colocated with features
9. **Clean up on unmount** - Unregister commands when features unmount
10. **Handle async actions** - Support promises for async operations

## Adapting for Your Use Case

### Adding a Custom Action

```tsx
import { registerCommand } from '@/components/action-palette';
import { Rocket } from 'lucide-react';

registerCommand({
  id: 'deploy-prod',
  name: 'Deploy to Production',
  description: 'Deploy current branch to production environment',
  category: 'Actions',
  icon: Rocket,
  shortcut: 'command+shift+d',
  destructive: true,  // Shows warning styling
  action: async () => {
    if (await confirmDeploy()) {
      await deployToProduction();
      showSuccessToast('Deployed successfully!');
    }
  },
});
```

### Integrating with Router

```tsx
import { useNavigate } from 'react-router-dom';
import { registerCommand } from '@/components/action-palette';

function useNavigationCommands() {
  const navigate = useNavigate();

  useEffect(() => {
    registerCommand({
      id: 'nav-home',
      name: 'Go Home',
      category: 'Navigation',
      action: () => navigate('/'),
    });
  }, [navigate]);
}
```

### Adding User Feedback

```tsx
registerCommand({
  id: 'save-document',
  name: 'Save Document',
  icon: Save,
  shortcut: 'command+s',
  action: async () => {
    try {
      await saveDocument();
      toast.success('Document saved!');
    } catch (error) {
      toast.error('Failed to save document');
    }
  },
});
```

## Accessibility Features

- **Keyboard navigation** - Full keyboard control
- **ARIA attributes** - Proper roles and labels
- **Screen reader support** - Announces search results and selected items
- **Focus management** - Traps focus within palette when open
- **Visual indicators** - Clear selection and hover states
- **Semantic HTML** - Uses proper button and list elements

## Browser Support

- Modern browsers with ES2020+ support
- Keyboard shortcuts work in Chrome, Firefox, Safari, Edge
- Dark mode follows system preferences

## License

MIT - Free to use in personal and commercial projects.
