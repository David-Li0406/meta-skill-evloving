/**
 * CommandPaletteDrawer - Slide-in panel variant
 *
 * Full-height or full-width panel that slides in from any edge.
 * Includes backdrop, slide animation, close button, and drag handle for mobile.
 *
 * @example
 * ```tsx
 * const [isOpen, setIsOpen] = useState(false);
 *
 * return (
 *   <CommandPaletteDrawer
 *     isOpen={isOpen}
 *     onOpenChange={setIsOpen}
 *     position="right"
 *     commands={commands}
 *     onSelect={handleSelect}
 *   />
 * );
 * ```
 */

import { useEffect, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import {
  BaseCommandPalette,
  BaseCommandPaletteProps,
  KeyboardLegend,
} from './BaseCommandPalette';

export type DrawerPosition = 'left' | 'right' | 'top' | 'bottom';

export interface CommandPaletteDrawerProps
  extends Omit<BaseCommandPaletteProps, 'searchQuery' | 'onSearchChange'> {
  /** Position of the drawer (default: "right") */
  position?: DrawerPosition;
  /** Width for left/right drawers (default: "400px") */
  width?: string;
  /** Height for top/bottom drawers (default: "60vh") */
  height?: string;
  /** Whether to show close button (default: true) */
  showCloseButton?: boolean;
  /** Whether to show drag handle for mobile (default: true) */
  showDragHandle?: boolean;
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
 * CommandPaletteDrawer component
 *
 * Slide-in panel from left, right, top, or bottom. Includes backdrop overlay,
 * close button, smooth slide animation, and mobile drag handle.
 */
export function CommandPaletteDrawer({
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
  position = 'right',
  width = '400px',
  height = '60vh',
  showCloseButton = true,
  showDragHandle = true,
  className = '',
  showKeyboardLegend = true,
  backdropBlur = true,
  animationDuration = 300,
}: CommandPaletteDrawerProps) {
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

  // Handle backdrop click to close
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

  // Get drawer styles based on position
  const getDrawerStyles = () => {
    const isHorizontal = position === 'left' || position === 'right';
    const baseStyles = {
      position: 'fixed' as const,
      background: 'var(--palette-bg)',
      border: '1px solid var(--palette-border)',
      boxShadow:
        '0 20px 25px -5px var(--palette-shadow-lg), 0 10px 10px -5px var(--palette-shadow)',
      display: 'flex',
      flexDirection: 'column' as const,
      zIndex: 10000,
    };

    switch (position) {
      case 'left':
        return {
          ...baseStyles,
          left: 0,
          top: 0,
          bottom: 0,
          width,
          borderLeft: 'none',
          borderTopLeftRadius: 0,
          borderBottomLeftRadius: 0,
          animation: `slideInLeft ${animationDuration}ms ease-out`,
        };
      case 'right':
        return {
          ...baseStyles,
          right: 0,
          top: 0,
          bottom: 0,
          width,
          borderRight: 'none',
          borderTopRightRadius: 0,
          borderBottomRightRadius: 0,
          animation: `slideInRight ${animationDuration}ms ease-out`,
        };
      case 'top':
        return {
          ...baseStyles,
          top: 0,
          left: 0,
          right: 0,
          height,
          borderTop: 'none',
          borderTopLeftRadius: 0,
          borderTopRightRadius: 0,
          animation: `slideInTop ${animationDuration}ms ease-out`,
        };
      case 'bottom':
        return {
          ...baseStyles,
          bottom: 0,
          left: 0,
          right: 0,
          height,
          borderBottom: 'none',
          borderBottomLeftRadius: 0,
          borderBottomRightRadius: 0,
          animation: `slideInBottom ${animationDuration}ms ease-out`,
        };
    }
  };

  if (!isOpen) return null;

  const content = (
    <div
      ref={backdropRef}
      className={`command-palette-drawer-backdrop ${className}`}
      onClick={handleBackdropClick}
      role="presentation"
      style={{
        position: 'fixed',
        inset: 0,
        zIndex: 9999,
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
        className="command-palette-drawer-container"
        style={getDrawerStyles()}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Drawer Header */}
        <div
          className="command-palette-drawer-header"
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            padding: '12px 16px',
            borderBottom: '1px solid var(--palette-border)',
            flexShrink: 0,
          }}
        >
          {/* Drag Handle (visual only) */}
          {showDragHandle && (
            <div
              className="drag-handle"
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '4px',
              }}
            >
              <div
                style={{
                  width: '32px',
                  height: '4px',
                  background: 'var(--palette-border)',
                  borderRadius: '2px',
                }}
              />
            </div>
          )}

          <div style={{ flex: 1 }} />

          {/* Close Button */}
          {showCloseButton && (
            <button
              onClick={() => {
                onOpenChange(false);
                setSearchQuery('');
              }}
              aria-label="Close palette"
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                width: '32px',
                height: '32px',
                border: 'none',
                background: 'transparent',
                color: 'var(--palette-text-muted)',
                borderRadius: '6px',
                cursor: 'pointer',
                transition: 'background-color 150ms ease',
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.background = 'var(--palette-hover-bg)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.background = 'transparent';
              }}
            >
              <svg
                width="16"
                height="16"
                viewBox="0 0 16 16"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
              >
                <path d="M12 4L4 12M4 4L12 12" />
              </svg>
            </button>
          )}
        </div>

        {/* Palette Content */}
        <div style={{ flex: 1, overflow: 'hidden', display: 'flex', flexDirection: 'column' }}>
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
            maxHeight={maxHeight || 'calc(100% - 80px)'}
            footer={footer || (showKeyboardLegend ? <KeyboardLegend /> : undefined)}
          />
        </div>
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

        @keyframes slideInLeft {
          from {
            transform: translateX(-100%);
          }
          to {
            transform: translateX(0);
          }
        }

        @keyframes slideInRight {
          from {
            transform: translateX(100%);
          }
          to {
            transform: translateX(0);
          }
        }

        @keyframes slideInTop {
          from {
            transform: translateY(-100%);
          }
          to {
            transform: translateY(0);
          }
        }

        @keyframes slideInBottom {
          from {
            transform: translateY(100%);
          }
          to {
            transform: translateY(0);
          }
        }

        @media (prefers-reduced-motion: reduce) {
          .command-palette-drawer-backdrop {
            animation: none !important;
          }

          .command-palette-drawer-container {
            animation: none !important;
          }
        }

        /* Mobile responsive */
        @media (max-width: 640px) {
          .command-palette-drawer-container {
            width: 100% !important;
            max-width: 100% !important;
          }
        }
      `}</style>
    </div>
  );

  return createPortal(content, document.body);
}

/**
 * Hook to control drawer state
 *
 * @example
 * ```tsx
 * const drawer = useDrawer();
 *
 * return (
 *   <>
 *     <button onClick={drawer.open}>Open</button>
 *     <CommandPaletteDrawer
 *       isOpen={drawer.isOpen}
 *       onOpenChange={drawer.setIsOpen}
 *       commands={commands}
 *       onSelect={handleSelect}
 *     />
 *   </>
 * );
 * ```
 */
export function useDrawer() {
  const [isOpen, setIsOpen] = useState(false);

  return {
    isOpen,
    setIsOpen,
    open: () => setIsOpen(true),
    close: () => setIsOpen(false),
    toggle: () => setIsOpen((prev) => !prev),
  };
}
