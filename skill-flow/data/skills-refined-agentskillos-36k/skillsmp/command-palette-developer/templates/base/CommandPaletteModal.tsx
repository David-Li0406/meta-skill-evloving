/**
 * CommandPaletteModal - Modal dialog variant of command palette
 *
 * Centered overlay with backdrop, following the standard ⌘K pattern.
 * Renders in a portal, includes focus trap, and handles click-outside to close.
 *
 * @example
 * ```tsx
 * const [isOpen, setIsOpen] = useState(false);
 *
 * // Trigger with ⌘K
 * useKeyboardShortcut('command+k', () => setIsOpen(true));
 *
 * return (
 *   <CommandPaletteModal
 *     isOpen={isOpen}
 *     onOpenChange={setIsOpen}
 *     commands={commands}
 *     onSelect={handleSelect}
 *   />
 * );
 * ```
 */

import { useEffect, useRef } from 'react';
import { createPortal } from 'react-dom';
import {
  BaseCommandPalette,
  BaseCommandPaletteProps,
  KeyboardLegend,
} from './BaseCommandPalette';

export interface CommandPaletteModalProps
  extends Omit<BaseCommandPaletteProps, 'searchQuery' | 'onSearchChange'> {
  /** Optional CSS class for custom styling */
  className?: string;
  /** Whether to show keyboard legend in footer */
  showKeyboardLegend?: boolean;
  /** Enable backdrop blur effect */
  backdropBlur?: boolean;
  /** Animation duration in milliseconds */
  animationDuration?: number;
}

/**
 * CommandPaletteModal component
 *
 * Modal dialog variant positioned 20vh from top (GitHub style).
 * Includes backdrop, focus trap, ESC/click-outside to close,
 * and smooth fade-in/scale animations.
 */
export function CommandPaletteModal({
  isOpen,
  onOpenChange,
  commands,
  groups,
  onSelect,
  placeholder,
  footer,
  emptyState,
  isLoading,
  maxHeight,
  className = '',
  showKeyboardLegend = true,
  backdropBlur = true,
  animationDuration = 300,
}: CommandPaletteModalProps) {
  const [searchQuery, setSearchQuery] = useState('');
  const backdropRef = useRef<HTMLDivElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const previousActiveElement = useRef<HTMLElement | null>(null);

  // Save and restore focus
  useEffect(() => {
    if (isOpen) {
      previousActiveElement.current = document.activeElement as HTMLElement;
    } else if (previousActiveElement.current) {
      previousActiveElement.current.focus();
      previousActiveElement.current = null;
    }
  }, [isOpen]);

  // Prevent body scroll when open
  useEffect(() => {
    if (isOpen) {
      const scrollbarWidth =
        window.innerWidth - document.documentElement.clientWidth;
      document.body.style.overflow = 'hidden';
      document.body.style.paddingRight = `${scrollbarWidth}px`;
    } else {
      document.body.style.overflow = '';
      document.body.style.paddingRight = '';
    }

    return () => {
      document.body.style.overflow = '';
      document.body.style.paddingRight = '';
    };
  }, [isOpen]);

  // Handle click outside to close
  const handleBackdropClick = (e: React.MouseEvent<HTMLDivElement>) => {
    if (e.target === backdropRef.current) {
      onOpenChange(false);
      setSearchQuery('');
    }
  };

  // Focus trap implementation
  useEffect(() => {
    if (!isOpen || !containerRef.current) return;

    const container = containerRef.current;
    const focusableElements = container.querySelectorAll<HTMLElement>(
      'a, button, input, textarea, select, [tabindex]:not([tabindex="-1"])'
    );

    const firstElement = focusableElements[0];
    const lastElement = focusableElements[focusableElements.length - 1];

    const handleTab = (e: KeyboardEvent) => {
      if (e.key !== 'Tab') return;

      if (e.shiftKey) {
        if (document.activeElement === firstElement) {
          e.preventDefault();
          lastElement?.focus();
        }
      } else {
        if (document.activeElement === lastElement) {
          e.preventDefault();
          firstElement?.focus();
        }
      }
    };

    container.addEventListener('keydown', handleTab);
    return () => container.removeEventListener('keydown', handleTab);
  }, [isOpen]);

  // Reset search when closed
  useEffect(() => {
    if (!isOpen) {
      setSearchQuery('');
    }
  }, [isOpen]);

  if (!isOpen) return null;

  const content = (
    <div
      ref={backdropRef}
      className={`command-palette-modal-backdrop ${className}`}
      onClick={handleBackdropClick}
      role="presentation"
      style={{
        position: 'fixed',
        inset: 0,
        zIndex: 9999,
        display: 'flex',
        alignItems: 'flex-start',
        justifyContent: 'center',
        padding: '20vh 16px 16px',
        background: 'rgba(0, 0, 0, 0.5)',
        backdropFilter: backdropBlur ? 'blur(4px)' : undefined,
        animation: `fadeIn ${animationDuration}ms ease-out`,
      }}
    >
      <div
        ref={containerRef}
        role="dialog"
        aria-modal="true"
        aria-label="Command Palette"
        className="command-palette-modal-container"
        style={{
          width: '100%',
          maxWidth: '640px',
          background: 'var(--palette-bg)',
          border: '1px solid var(--palette-border)',
          borderRadius: '12px',
          boxShadow:
            '0 20px 25px -5px var(--palette-shadow-lg), 0 10px 10px -5px var(--palette-shadow)',
          overflow: 'hidden',
          animation: `slideUpScale ${animationDuration}ms ease-out`,
        }}
        onClick={(e) => e.stopPropagation()}
      >
        <BaseCommandPalette
          isOpen={isOpen}
          onOpenChange={onOpenChange}
          searchQuery={searchQuery}
          onSearchChange={setSearchQuery}
          commands={commands}
          groups={groups}
          onSelect={onSelect}
          placeholder={placeholder}
          emptyState={emptyState}
          isLoading={isLoading}
          maxHeight={maxHeight || '400px'}
          footer={footer || (showKeyboardLegend ? <KeyboardLegend /> : undefined)}
        />
      </div>

      {/* Animation Styles */}
      <style>{`
        @keyframes fadeIn {
          from {
            opacity: 0;
          }
          to {
            opacity: 1;
          }
        }

        @keyframes slideUpScale {
          from {
            opacity: 0;
            transform: translateY(20px) scale(0.95);
          }
          to {
            opacity: 1;
            transform: translateY(0) scale(1);
          }
        }

        @media (prefers-reduced-motion: reduce) {
          .command-palette-modal-backdrop {
            animation: none !important;
          }

          .command-palette-modal-container {
            animation: none !important;
          }
        }

        /* Mobile responsive */
        @media (max-width: 640px) {
          .command-palette-modal-backdrop {
            padding: 8px;
            align-items: center;
          }

          .command-palette-modal-container {
            max-height: 80vh;
          }
        }
      `}</style>
    </div>
  );

  return createPortal(content, document.body);
}

/**
 * Hook for keyboard shortcut to open modal
 *
 * @example
 * ```tsx
 * const [isOpen, setIsOpen] = useState(false);
 * useCommandPaletteShortcut(() => setIsOpen(true));
 * ```
 */
export function useCommandPaletteShortcut(onOpen: () => void) {
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'k' && (e.metaKey || e.ctrlKey)) {
        e.preventDefault();
        onOpen();
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [onOpen]);
}

import { useState } from 'react';
