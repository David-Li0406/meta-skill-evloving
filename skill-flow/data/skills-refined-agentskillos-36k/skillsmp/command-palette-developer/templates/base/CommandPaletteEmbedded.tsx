/**
 * CommandPaletteEmbedded - Floating palette variant
 *
 * Uses Floating UI for smart positioning relative to a trigger element.
 * Auto-flips to stay in viewport, includes arrow pointer, and closes on
 * click-outside or ESC key.
 *
 * @example
 * ```tsx
 * const [isOpen, setIsOpen] = useState(false);
 *
 * return (
 *   <>
 *     <button onClick={() => setIsOpen(true)}>
 *       Open Commands
 *     </button>
 *
 *     <CommandPaletteEmbedded
 *       isOpen={isOpen}
 *       onOpenChange={setIsOpen}
 *       triggerRef={buttonRef}
 *       commands={commands}
 *       onSelect={handleSelect}
 *       placement="bottom-start"
 *     />
 *   </>
 * );
 * ```
 */

import { useEffect, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import {
  useFloating,
  offset,
  flip,
  shift,
  autoUpdate,
  arrow,
  FloatingArrow,
  type Placement,
} from '@floating-ui/react';
import {
  BaseCommandPalette,
  BaseCommandPaletteProps,
  KeyboardLegend,
} from './BaseCommandPalette';

export interface CommandPaletteEmbeddedProps
  extends Omit<BaseCommandPaletteProps, 'searchQuery' | 'onSearchChange'> {
  /** Ref to the trigger element */
  triggerRef?: React.RefObject<HTMLElement>;
  /** Placement strategy (default: "bottom-start") */
  placement?: Placement;
  /** Offset from trigger in pixels (default: 8) */
  offsetDistance?: number;
  /** Whether to show arrow pointer (default: true) */
  showArrow?: boolean;
  /** Maximum width in pixels (default: 400) */
  maxWidth?: number;
  /** Optional CSS class for custom styling */
  className?: string;
  /** Whether to show keyboard legend in footer */
  showKeyboardLegend?: boolean;
}

/**
 * CommandPaletteEmbedded component
 *
 * Floating palette with Floating UI positioning. Auto-updates position on scroll,
 * flips to opposite side if no space, and shifts horizontally to stay in viewport.
 */
export function CommandPaletteEmbedded({
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
  triggerRef,
  placement = 'bottom-start',
  offsetDistance = 8,
  showArrow = true,
  maxWidth = 400,
  className = '',
  showKeyboardLegend = true,
}: CommandPaletteEmbeddedProps) {
  const [searchQuery, setSearchQuery] = useState('');
  const arrowRef = useRef<SVGSVGElement>(null);

  // Floating UI setup
  const { refs, floatingStyles, context } = useFloating({
    open: isOpen,
    onOpenChange,
    placement,
    middleware: [
      offset(offsetDistance + (showArrow ? 8 : 0)), // Extra offset for arrow
      flip({
        fallbackPlacements: ['top-start', 'bottom-end', 'top-end'],
        padding: 8,
      }),
      shift({ padding: 8 }),
      showArrow
        ? arrow({
            element: arrowRef,
            padding: 8,
          })
        : null,
    ].filter(Boolean),
    whileElementsMounted: autoUpdate,
  });

  // Connect trigger ref if provided
  useEffect(() => {
    if (triggerRef?.current) {
      refs.setReference(triggerRef.current);
    }
  }, [triggerRef, refs]);

  // Handle click outside to close
  useEffect(() => {
    if (!isOpen) return;

    const handleClickOutside = (e: MouseEvent) => {
      const target = e.target as Node;
      const floatingEl = refs.floating.current;
      const referenceEl = refs.reference.current as HTMLElement | null;

      if (
        floatingEl &&
        !floatingEl.contains(target) &&
        referenceEl &&
        !referenceEl.contains(target)
      ) {
        onOpenChange(false);
        setSearchQuery('');
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [isOpen, onOpenChange, refs]);

  // Reset search when closed
  useEffect(() => {
    if (!isOpen) {
      setSearchQuery('');
    }
  }, [isOpen]);

  if (!isOpen) return null;

  const content = (
    <div
      ref={refs.setFloating}
      style={{
        ...floatingStyles,
        zIndex: 9999,
        maxWidth: `${maxWidth}px`,
        width: 'max-content',
        minWidth: '320px',
      }}
      className={`command-palette-embedded ${className}`}
    >
      <div
        role="dialog"
        aria-modal="false"
        aria-label="Command Palette"
        style={{
          background: 'var(--palette-bg)',
          border: '1px solid var(--palette-border)',
          borderRadius: '8px',
          boxShadow:
            '0 10px 15px -3px var(--palette-shadow), 0 4px 6px -2px var(--palette-shadow)',
          overflow: 'hidden',
          animation: 'fadeIn 150ms ease-out',
        }}
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
          maxHeight={maxHeight || '300px'}
          footer={footer || (showKeyboardLegend ? <KeyboardLegend /> : undefined)}
        />
      </div>

      {/* Arrow Pointer */}
      {showArrow && (
        <FloatingArrow
          ref={arrowRef}
          context={context}
          fill="var(--palette-bg)"
          stroke="var(--palette-border)"
          strokeWidth={1}
          width={16}
          height={8}
        />
      )}

      {/* Animation Styles */}
      <style>{`
        @keyframes fadeIn {
          from {
            opacity: 0;
            transform: scale(0.95);
          }
          to {
            opacity: 1;
            transform: scale(1);
          }
        }

        @media (prefers-reduced-motion: reduce) {
          .command-palette-embedded {
            animation: none !important;
          }
        }

        /* Mobile responsive */
        @media (max-width: 640px) {
          .command-palette-embedded {
            max-width: calc(100vw - 16px) !important;
            min-width: calc(100vw - 16px) !important;
          }
        }
      `}</style>
    </div>
  );

  return createPortal(content, document.body);
}

/**
 * Hook to create a ref and control embedded palette
 *
 * @example
 * ```tsx
 * const { triggerRef, isOpen, setIsOpen } = useEmbeddedPalette();
 *
 * return (
 *   <>
 *     <button ref={triggerRef} onClick={() => setIsOpen(true)}>
 *       Commands
 *     </button>
 *     <CommandPaletteEmbedded
 *       triggerRef={triggerRef}
 *       isOpen={isOpen}
 *       onOpenChange={setIsOpen}
 *       commands={commands}
 *       onSelect={handleSelect}
 *     />
 *   </>
 * );
 * ```
 */
export function useEmbeddedPalette() {
  const [isOpen, setIsOpen] = useState(false);
  const triggerRef = useRef<HTMLButtonElement>(null);

  return {
    triggerRef,
    isOpen,
    setIsOpen,
    open: () => setIsOpen(true),
    close: () => setIsOpen(false),
    toggle: () => setIsOpen((prev) => !prev),
  };
}
