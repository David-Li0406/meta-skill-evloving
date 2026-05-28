/**
 * Tests for Base Command Palette Components
 *
 * Comprehensive test suite using Vitest and React Testing Library.
 * Tests keyboard navigation, search, selection, and accessibility.
 *
 * Run tests: npm test BaseCommandPalette.test.tsx
 */

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import {
  BaseCommandPalette,
  CommandPaletteModal,
  CommandPaletteEmbedded,
  CommandPaletteDrawer,
  type CommandItem,
} from './index';

/**
 * Mock commands for testing
 */
const mockCommands: CommandItem[] = [
  {
    id: 'create-task',
    label: 'Create Task',
    description: 'Create a new task',
    icon: '✅',
    shortcut: 'command+n',
    group: 'Actions',
    keywords: ['new', 'add'],
  },
  {
    id: 'delete-task',
    label: 'Delete Task',
    description: 'Remove a task',
    icon: '🗑️',
    group: 'Actions',
  },
  {
    id: 'nav-home',
    label: 'Go to Home',
    description: 'Navigate home',
    icon: '🏠',
    group: 'Navigation',
  },
];

describe('BaseCommandPalette', () => {
  let user: ReturnType<typeof userEvent.setup>;

  beforeEach(() => {
    user = userEvent.setup();
  });

  it('renders with commands', () => {
    const handleSelect = vi.fn();
    const handleChange = vi.fn();

    render(
      <BaseCommandPalette
        isOpen={true}
        onOpenChange={vi.fn()}
        searchQuery=""
        onSearchChange={handleChange}
        commands={mockCommands}
        onSelect={handleSelect}
      />
    );

    expect(screen.getByText('Create Task')).toBeInTheDocument();
    expect(screen.getByText('Delete Task')).toBeInTheDocument();
    expect(screen.getByText('Go to Home')).toBeInTheDocument();
  });

  it('filters commands by search query', async () => {
    const handleSelect = vi.fn();
    const handleChange = vi.fn();

    const { rerender } = render(
      <BaseCommandPalette
        isOpen={true}
        onOpenChange={vi.fn()}
        searchQuery=""
        onSearchChange={handleChange}
        commands={mockCommands}
        onSelect={handleSelect}
      />
    );

    // Type search query
    const input = screen.getByPlaceholderText('Search commands...');
    await user.type(input, 'create');

    // Rerender with updated query
    rerender(
      <BaseCommandPalette
        isOpen={true}
        onOpenChange={vi.fn()}
        searchQuery="create"
        onSearchChange={handleChange}
        commands={mockCommands}
        onSelect={handleSelect}
      />
    );

    expect(screen.getByText('Create Task')).toBeInTheDocument();
    expect(screen.queryByText('Delete Task')).not.toBeInTheDocument();
  });

  it('calls onSelect when command is clicked', async () => {
    const handleSelect = vi.fn();

    render(
      <BaseCommandPalette
        isOpen={true}
        onOpenChange={vi.fn()}
        searchQuery=""
        onSearchChange={vi.fn()}
        commands={mockCommands}
        onSelect={handleSelect}
      />
    );

    await user.click(screen.getByText('Create Task'));

    expect(handleSelect).toHaveBeenCalledWith(mockCommands[0]);
  });

  it('navigates with arrow keys', async () => {
    const handleSelect = vi.fn();

    render(
      <BaseCommandPalette
        isOpen={true}
        onOpenChange={vi.fn()}
        searchQuery=""
        onSearchChange={vi.fn()}
        commands={mockCommands}
        onSelect={handleSelect}
      />
    );

    const input = screen.getByPlaceholderText('Search commands...');
    input.focus();

    // Press down arrow
    await user.keyboard('{ArrowDown}');
    await user.keyboard('{Enter}');

    expect(handleSelect).toHaveBeenCalled();
  });

  it('shows empty state when no commands', () => {
    render(
      <BaseCommandPalette
        isOpen={true}
        onOpenChange={vi.fn()}
        searchQuery=""
        onSearchChange={vi.fn()}
        commands={[]}
        onSelect={vi.fn()}
      />
    );

    expect(screen.getByText(/No commands available/i)).toBeInTheDocument();
  });

  it('shows loading state', () => {
    render(
      <BaseCommandPalette
        isOpen={true}
        onOpenChange={vi.fn()}
        searchQuery=""
        onSearchChange={vi.fn()}
        commands={[]}
        onSelect={vi.fn()}
        isLoading={true}
      />
    );

    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });

  it('displays keyboard shortcuts', () => {
    render(
      <BaseCommandPalette
        isOpen={true}
        onOpenChange={vi.fn()}
        searchQuery=""
        onSearchChange={vi.fn()}
        commands={mockCommands}
        onSelect={vi.fn()}
      />
    );

    // Shortcut should be visible (formatted as ⌘N or Ctrl+N)
    const shortcuts = screen.getAllByText(/⌘|Ctrl/i);
    expect(shortcuts.length).toBeGreaterThan(0);
  });

  it('groups commands by group property', () => {
    render(
      <BaseCommandPalette
        isOpen={true}
        onOpenChange={vi.fn()}
        searchQuery=""
        onSearchChange={vi.fn()}
        commands={mockCommands}
        onSelect={vi.fn()}
      />
    );

    expect(screen.getByText('Actions')).toBeInTheDocument();
    expect(screen.getByText('Navigation')).toBeInTheDocument();
  });
});

describe('CommandPaletteModal', () => {
  let user: ReturnType<typeof userEvent.setup>;

  beforeEach(() => {
    user = userEvent.setup();
  });

  afterEach(() => {
    // Clean up body overflow styles
    document.body.style.overflow = '';
    document.body.style.paddingRight = '';
  });

  it('renders when open', () => {
    render(
      <CommandPaletteModal
        isOpen={true}
        onOpenChange={vi.fn()}
        commands={mockCommands}
        onSelect={vi.fn()}
      />
    );

    expect(screen.getByRole('dialog')).toBeInTheDocument();
    expect(screen.getByLabelText('Command Palette')).toBeInTheDocument();
  });

  it('does not render when closed', () => {
    render(
      <CommandPaletteModal
        isOpen={false}
        onOpenChange={vi.fn()}
        commands={mockCommands}
        onSelect={vi.fn()}
      />
    );

    expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
  });

  it('closes on backdrop click', async () => {
    const handleOpenChange = vi.fn();

    render(
      <CommandPaletteModal
        isOpen={true}
        onOpenChange={handleOpenChange}
        commands={mockCommands}
        onSelect={vi.fn()}
      />
    );

    const backdrop = screen.getByRole('dialog').parentElement;
    await user.click(backdrop!);

    expect(handleOpenChange).toHaveBeenCalledWith(false);
  });

  it('closes on ESC key', async () => {
    const handleOpenChange = vi.fn();

    render(
      <CommandPaletteModal
        isOpen={true}
        onOpenChange={handleOpenChange}
        commands={mockCommands}
        onSelect={vi.fn()}
      />
    );

    await user.keyboard('{Escape}');

    expect(handleOpenChange).toHaveBeenCalledWith(false);
  });

  it('prevents body scroll when open', () => {
    render(
      <CommandPaletteModal
        isOpen={true}
        onOpenChange={vi.fn()}
        commands={mockCommands}
        onSelect={vi.fn()}
      />
    );

    expect(document.body.style.overflow).toBe('hidden');
  });

  it('shows keyboard legend by default', () => {
    render(
      <CommandPaletteModal
        isOpen={true}
        onOpenChange={vi.fn()}
        commands={mockCommands}
        onSelect={vi.fn()}
      />
    );

    expect(screen.getByText(/to navigate/i)).toBeInTheDocument();
    expect(screen.getByText(/to select/i)).toBeInTheDocument();
  });

  it('hides keyboard legend when disabled', () => {
    render(
      <CommandPaletteModal
        isOpen={true}
        onOpenChange={vi.fn()}
        commands={mockCommands}
        onSelect={vi.fn()}
        showKeyboardLegend={false}
      />
    );

    expect(screen.queryByText(/to navigate/i)).not.toBeInTheDocument();
  });
});

describe('CommandPaletteEmbedded', () => {
  let user: ReturnType<typeof userEvent.setup>;
  let triggerRef: React.RefObject<HTMLButtonElement>;

  beforeEach(() => {
    user = userEvent.setup();
    triggerRef = { current: document.createElement('button') };
    document.body.appendChild(triggerRef.current);
  });

  afterEach(() => {
    if (triggerRef.current) {
      document.body.removeChild(triggerRef.current);
    }
  });

  it('renders when open', () => {
    render(
      <CommandPaletteEmbedded
        isOpen={true}
        onOpenChange={vi.fn()}
        triggerRef={triggerRef}
        commands={mockCommands}
        onSelect={vi.fn()}
      />
    );

    expect(screen.getByRole('dialog')).toBeInTheDocument();
  });

  it('does not render when closed', () => {
    render(
      <CommandPaletteEmbedded
        isOpen={false}
        onOpenChange={vi.fn()}
        triggerRef={triggerRef}
        commands={mockCommands}
        onSelect={vi.fn()}
      />
    );

    expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
  });

  it('closes on click outside', async () => {
    const handleOpenChange = vi.fn();

    render(
      <CommandPaletteEmbedded
        isOpen={true}
        onOpenChange={handleOpenChange}
        triggerRef={triggerRef}
        commands={mockCommands}
        onSelect={vi.fn()}
      />
    );

    await user.click(document.body);

    await waitFor(() => {
      expect(handleOpenChange).toHaveBeenCalledWith(false);
    });
  });

  it('shows arrow by default', () => {
    const { container } = render(
      <CommandPaletteEmbedded
        isOpen={true}
        onOpenChange={vi.fn()}
        triggerRef={triggerRef}
        commands={mockCommands}
        onSelect={vi.fn()}
      />
    );

    const arrow = container.querySelector('svg');
    expect(arrow).toBeInTheDocument();
  });

  it('hides arrow when disabled', () => {
    const { container } = render(
      <CommandPaletteEmbedded
        isOpen={true}
        onOpenChange={vi.fn()}
        triggerRef={triggerRef}
        commands={mockCommands}
        onSelect={vi.fn()}
        showArrow={false}
      />
    );

    const arrow = container.querySelector('svg');
    expect(arrow).not.toBeInTheDocument();
  });
});

describe('CommandPaletteDrawer', () => {
  let user: ReturnType<typeof userEvent.setup>;

  beforeEach(() => {
    user = userEvent.setup();
  });

  afterEach(() => {
    document.body.style.overflow = '';
    document.body.style.paddingRight = '';
  });

  it('renders when open', () => {
    render(
      <CommandPaletteDrawer
        isOpen={true}
        onOpenChange={vi.fn()}
        commands={mockCommands}
        onSelect={vi.fn()}
      />
    );

    expect(screen.getByRole('dialog')).toBeInTheDocument();
  });

  it('does not render when closed', () => {
    render(
      <CommandPaletteDrawer
        isOpen={false}
        onOpenChange={vi.fn()}
        commands={mockCommands}
        onSelect={vi.fn()}
      />
    );

    expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
  });

  it('shows close button by default', () => {
    render(
      <CommandPaletteDrawer
        isOpen={true}
        onOpenChange={vi.fn()}
        commands={mockCommands}
        onSelect={vi.fn()}
      />
    );

    expect(screen.getByLabelText('Close palette')).toBeInTheDocument();
  });

  it('closes when close button clicked', async () => {
    const handleOpenChange = vi.fn();

    render(
      <CommandPaletteDrawer
        isOpen={true}
        onOpenChange={handleOpenChange}
        commands={mockCommands}
        onSelect={vi.fn()}
      />
    );

    await user.click(screen.getByLabelText('Close palette'));

    expect(handleOpenChange).toHaveBeenCalledWith(false);
  });

  it('closes on backdrop click', async () => {
    const handleOpenChange = vi.fn();

    render(
      <CommandPaletteDrawer
        isOpen={true}
        onOpenChange={handleOpenChange}
        commands={mockCommands}
        onSelect={vi.fn()}
      />
    );

    const backdrop = screen.getByRole('dialog').parentElement;
    await user.click(backdrop!);

    expect(handleOpenChange).toHaveBeenCalledWith(false);
  });

  it('shows drag handle by default', () => {
    const { container } = render(
      <CommandPaletteDrawer
        isOpen={true}
        onOpenChange={vi.fn()}
        commands={mockCommands}
        onSelect={vi.fn()}
      />
    );

    const dragHandle = container.querySelector('.drag-handle');
    expect(dragHandle).toBeInTheDocument();
  });

  it('supports different positions', () => {
    const positions = ['left', 'right', 'top', 'bottom'] as const;

    positions.forEach((position) => {
      const { container } = render(
        <CommandPaletteDrawer
          isOpen={true}
          onOpenChange={vi.fn()}
          position={position}
          commands={mockCommands}
          onSelect={vi.fn()}
        />
      );

      expect(container.querySelector('.command-palette-drawer-container')).toBeInTheDocument();
    });
  });
});

describe('Accessibility', () => {
  it('has proper ARIA attributes', () => {
    render(
      <CommandPaletteModal
        isOpen={true}
        onOpenChange={vi.fn()}
        commands={mockCommands}
        onSelect={vi.fn()}
      />
    );

    const dialog = screen.getByRole('dialog');
    expect(dialog).toHaveAttribute('aria-modal', 'true');
    expect(dialog).toHaveAttribute('aria-label', 'Command Palette');
  });

  it('auto-focuses input when opened', async () => {
    render(
      <CommandPaletteModal
        isOpen={true}
        onOpenChange={vi.fn()}
        commands={mockCommands}
        onSelect={vi.fn()}
      />
    );

    await waitFor(() => {
      const input = screen.getByPlaceholderText('Search commands...');
      expect(input).toHaveFocus();
    });
  });

  it('respects reduced motion preference', () => {
    const { container } = render(
      <CommandPaletteModal
        isOpen={true}
        onOpenChange={vi.fn()}
        commands={mockCommands}
        onSelect={vi.fn()}
      />
    );

    const style = container.querySelector('style');
    expect(style?.textContent).toContain('prefers-reduced-motion');
  });
});
