/**
 * Command Palette Base Components
 *
 * Production-ready command palette components with keyboard navigation,
 * fuzzy search, focus management, and accessibility.
 *
 * @example Modal (⌘K pattern)
 * ```tsx
 * import { CommandPaletteModal, useCommandPaletteShortcut } from './base';
 *
 * function App() {
 *   const [isOpen, setIsOpen] = useState(false);
 *   useCommandPaletteShortcut(() => setIsOpen(true));
 *
 *   return (
 *     <CommandPaletteModal
 *       isOpen={isOpen}
 *       onOpenChange={setIsOpen}
 *       commands={commands}
 *       onSelect={handleSelect}
 *     />
 *   );
 * }
 * ```
 *
 * @example Embedded (Floating)
 * ```tsx
 * import { CommandPaletteEmbedded, useEmbeddedPalette } from './base';
 *
 * function App() {
 *   const { triggerRef, isOpen, setIsOpen } = useEmbeddedPalette();
 *
 *   return (
 *     <>
 *       <button ref={triggerRef} onClick={() => setIsOpen(true)}>
 *         Commands
 *       </button>
 *       <CommandPaletteEmbedded
 *         triggerRef={triggerRef}
 *         isOpen={isOpen}
 *         onOpenChange={setIsOpen}
 *         commands={commands}
 *         onSelect={handleSelect}
 *       />
 *     </>
 *   );
 * }
 * ```
 *
 * @example Drawer (Slide-in panel)
 * ```tsx
 * import { CommandPaletteDrawer, useDrawer } from './base';
 *
 * function App() {
 *   const drawer = useDrawer();
 *
 *   return (
 *     <>
 *       <button onClick={drawer.open}>Open</button>
 *       <CommandPaletteDrawer
 *         isOpen={drawer.isOpen}
 *         onOpenChange={drawer.setIsOpen}
 *         position="right"
 *         commands={commands}
 *         onSelect={handleSelect}
 *       />
 *     </>
 *   );
 * }
 * ```
 */

// Base component and types
export {
  BaseCommandPalette,
  KeyboardLegend,
  type CommandItem,
  type CommandGroup,
  type BaseCommandPaletteProps,
} from './BaseCommandPalette';

// Modal variant
export {
  CommandPaletteModal,
  useCommandPaletteShortcut,
  type CommandPaletteModalProps,
} from './CommandPaletteModal';

// Embedded variant
export {
  CommandPaletteEmbedded,
  useEmbeddedPalette,
  type CommandPaletteEmbeddedProps,
} from './CommandPaletteEmbedded';

// Drawer variant
export {
  CommandPaletteDrawer,
  useDrawer,
  type CommandPaletteDrawerProps,
  type DrawerPosition,
} from './CommandPaletteDrawer';
