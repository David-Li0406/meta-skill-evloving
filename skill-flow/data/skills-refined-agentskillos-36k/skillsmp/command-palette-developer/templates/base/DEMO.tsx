/**
 * Base Command Palette Components Demo
 *
 * Demonstrates all three variants with mock data and complete examples.
 * Copy-paste this file to test the components in your project.
 *
 * Usage:
 * 1. Install dependencies: npm install cmdk @floating-ui/react
 * 2. Copy all .tsx files from /base directory
 * 3. Import and use this demo: import { CommandPaletteDemo } from './DEMO'
 */

import { useState } from 'react';
import {
  CommandPaletteModal,
  CommandPaletteEmbedded,
  CommandPaletteDrawer,
  useCommandPaletteShortcut,
  useEmbeddedPalette,
  useDrawer,
  type CommandItem,
} from './index';

/**
 * Mock command data
 */
const mockCommands: CommandItem[] = [
  // Actions
  {
    id: 'create-task',
    label: 'Create Task',
    description: 'Create a new task or todo item',
    icon: '✅',
    shortcut: 'command+n',
    group: 'Actions',
    keywords: ['new', 'add', 'todo'],
  },
  {
    id: 'create-project',
    label: 'Create Project',
    description: 'Start a new project',
    icon: '📁',
    shortcut: 'command+shift+n',
    group: 'Actions',
    keywords: ['new', 'add'],
    badge: 'New',
  },
  {
    id: 'delete-item',
    label: 'Delete Selected',
    description: 'Remove the selected item',
    icon: '🗑️',
    shortcut: 'command+backspace',
    group: 'Actions',
    keywords: ['remove', 'trash'],
  },
  {
    id: 'deploy',
    label: 'Deploy to Production',
    description: 'Deploy the current branch',
    icon: '🚀',
    group: 'Actions',
    keywords: ['release', 'ship', 'publish'],
  },

  // Navigation
  {
    id: 'nav-home',
    label: 'Go to Home',
    description: 'Navigate to the home page',
    icon: '🏠',
    shortcut: 'command+h',
    group: 'Navigation',
    keywords: ['dashboard'],
  },
  {
    id: 'nav-settings',
    label: 'Open Settings',
    description: 'Configure application settings',
    icon: '⚙️',
    shortcut: 'command+,',
    group: 'Navigation',
    keywords: ['preferences', 'config'],
  },
  {
    id: 'nav-profile',
    label: 'View Profile',
    description: 'Go to your profile page',
    icon: '👤',
    group: 'Navigation',
    keywords: ['user', 'account'],
  },
  {
    id: 'nav-notifications',
    label: 'Notifications',
    description: 'View recent notifications',
    icon: '🔔',
    group: 'Navigation',
    badge: '3',
  },

  // Search
  {
    id: 'search-files',
    label: 'Search Files',
    description: 'Find files by name or content',
    icon: '🔍',
    shortcut: 'command+p',
    group: 'Search',
    keywords: ['find', 'locate'],
  },
  {
    id: 'search-commands',
    label: 'Search Commands',
    description: 'Find and execute commands',
    icon: '💻',
    shortcut: 'command+k',
    group: 'Search',
  },

  // Git
  {
    id: 'git-commit',
    label: 'Commit Changes',
    description: 'Commit staged changes',
    icon: '💾',
    shortcut: 'command+enter',
    group: 'Git',
    keywords: ['save', 'stage'],
  },
  {
    id: 'git-push',
    label: 'Push to Remote',
    description: 'Push commits to origin',
    icon: '⬆️',
    group: 'Git',
    keywords: ['upload', 'sync'],
  },
  {
    id: 'git-pull',
    label: 'Pull from Remote',
    description: 'Fetch and merge changes',
    icon: '⬇️',
    group: 'Git',
    keywords: ['download', 'sync', 'fetch'],
  },

  // Help
  {
    id: 'help-docs',
    label: 'View Documentation',
    description: 'Open the documentation',
    icon: '📖',
    group: 'Help',
    keywords: ['guide', 'manual', 'readme'],
  },
  {
    id: 'help-shortcuts',
    label: 'Keyboard Shortcuts',
    description: 'View all keyboard shortcuts',
    icon: '⌨️',
    shortcut: 'command+/',
    group: 'Help',
    keywords: ['keys', 'hotkeys'],
  },
];

/**
 * Modal Variant Demo
 */
export function ModalDemo() {
  const [isOpen, setIsOpen] = useState(false);
  const [lastSelected, setLastSelected] = useState<CommandItem | null>(null);

  // Toggle with ⌘K
  useCommandPaletteShortcut(() => setIsOpen((prev) => !prev));

  const handleSelect = (command: CommandItem) => {
    setLastSelected(command);
    console.log('Modal selected:', command);
    // Execute command action here
  };

  return (
    <div style={{ padding: '24px' }}>
      <h2>Modal Variant (⌘K Pattern)</h2>
      <p>Press ⌘K to open the command palette</p>

      <button
        onClick={() => setIsOpen(true)}
        style={{
          padding: '8px 16px',
          background: '#3b82f6',
          color: 'white',
          border: 'none',
          borderRadius: '6px',
          cursor: 'pointer',
        }}
      >
        Open Command Palette
      </button>

      {lastSelected && (
        <div style={{ marginTop: '16px', padding: '12px', background: '#f3f4f6', borderRadius: '6px' }}>
          <strong>Last selected:</strong> {lastSelected.label}
        </div>
      )}

      <CommandPaletteModal
        isOpen={isOpen}
        onOpenChange={setIsOpen}
        commands={mockCommands}
        onSelect={handleSelect}
        placeholder="Search commands..."
        showKeyboardLegend
      />
    </div>
  );
}

/**
 * Embedded Variant Demo
 */
export function EmbeddedDemo() {
  const { triggerRef, isOpen, setIsOpen } = useEmbeddedPalette();
  const [lastSelected, setLastSelected] = useState<CommandItem | null>(null);

  const handleSelect = (command: CommandItem) => {
    setLastSelected(command);
    console.log('Embedded selected:', command);
  };

  return (
    <div style={{ padding: '24px' }}>
      <h2>Embedded Variant (Floating)</h2>
      <p>Click the button to show the floating palette</p>

      <button
        ref={triggerRef}
        onClick={() => setIsOpen(true)}
        style={{
          padding: '8px 16px',
          background: '#10b981',
          color: 'white',
          border: 'none',
          borderRadius: '6px',
          cursor: 'pointer',
        }}
      >
        Show Commands
      </button>

      {lastSelected && (
        <div style={{ marginTop: '16px', padding: '12px', background: '#f3f4f6', borderRadius: '6px' }}>
          <strong>Last selected:</strong> {lastSelected.label}
        </div>
      )}

      <CommandPaletteEmbedded
        triggerRef={triggerRef}
        isOpen={isOpen}
        onOpenChange={setIsOpen}
        commands={mockCommands}
        onSelect={handleSelect}
        placement="bottom-start"
        showArrow
      />
    </div>
  );
}

/**
 * Drawer Variant Demo
 */
export function DrawerDemo() {
  const drawer = useDrawer();
  const [position, setPosition] = useState<'left' | 'right' | 'top' | 'bottom'>('right');
  const [lastSelected, setLastSelected] = useState<CommandItem | null>(null);

  const handleSelect = (command: CommandItem) => {
    setLastSelected(command);
    console.log('Drawer selected:', command);
  };

  return (
    <div style={{ padding: '24px' }}>
      <h2>Drawer Variant (Slide-in Panel)</h2>
      <p>Choose a position and open the drawer</p>

      <div style={{ display: 'flex', gap: '8px', marginBottom: '16px' }}>
        {(['left', 'right', 'top', 'bottom'] as const).map((pos) => (
          <button
            key={pos}
            onClick={() => setPosition(pos)}
            style={{
              padding: '8px 16px',
              background: position === pos ? '#8b5cf6' : '#e5e7eb',
              color: position === pos ? 'white' : '#111827',
              border: 'none',
              borderRadius: '6px',
              cursor: 'pointer',
              textTransform: 'capitalize',
            }}
          >
            {pos}
          </button>
        ))}
      </div>

      <button
        onClick={drawer.open}
        style={{
          padding: '8px 16px',
          background: '#8b5cf6',
          color: 'white',
          border: 'none',
          borderRadius: '6px',
          cursor: 'pointer',
        }}
      >
        Open Drawer
      </button>

      {lastSelected && (
        <div style={{ marginTop: '16px', padding: '12px', background: '#f3f4f6', borderRadius: '6px' }}>
          <strong>Last selected:</strong> {lastSelected.label}
        </div>
      )}

      <CommandPaletteDrawer
        isOpen={drawer.isOpen}
        onOpenChange={drawer.setIsOpen}
        position={position}
        commands={mockCommands}
        onSelect={handleSelect}
        showCloseButton
        showDragHandle
      />
    </div>
  );
}

/**
 * Complete Demo App
 */
export function CommandPaletteDemo() {
  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', fontFamily: 'system-ui, sans-serif' }}>
      <h1>Command Palette Components Demo</h1>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '32px' }}>
        <ModalDemo />
        <hr />
        <EmbeddedDemo />
        <hr />
        <DrawerDemo />
      </div>

      {/* CSS Variables for theming */}
      <style>{`
        :root {
          --palette-bg: #ffffff;
          --palette-bg-secondary: #f9fafb;
          --palette-selection-bg: #eff6ff;
          --palette-hover-bg: #f3f4f6;
          --palette-text: #111827;
          --palette-text-muted: #6b7280;
          --palette-text-placeholder: #9ca3af;
          --palette-border: #e5e7eb;
          --palette-separator: #f3f4f6;
          --palette-accent: #3b82f6;
          --palette-accent-hover: #2563eb;
          --palette-shadow: rgba(0, 0, 0, 0.1);
          --palette-shadow-lg: rgba(0, 0, 0, 0.15);
          --palette-shortcut-bg: #f3f4f6;
          --palette-shortcut-text: #374151;
          --palette-shortcut-border: #d1d5db;
        }

        [data-theme="dark"] {
          --palette-bg: #1f2937;
          --palette-bg-secondary: #111827;
          --palette-selection-bg: #374151;
          --palette-hover-bg: #2d3748;
          --palette-text: #f9fafb;
          --palette-text-muted: #9ca3af;
          --palette-text-placeholder: #6b7280;
          --palette-border: #374151;
          --palette-separator: #2d3748;
          --palette-accent: #60a5fa;
          --palette-accent-hover: #3b82f6;
          --palette-shadow: rgba(0, 0, 0, 0.3);
          --palette-shadow-lg: rgba(0, 0, 0, 0.5);
          --palette-shortcut-bg: #374151;
          --palette-shortcut-text: #d1d5db;
          --palette-shortcut-border: #4b5563;
        }
      `}</style>
    </div>
  );
}

export default CommandPaletteDemo;
