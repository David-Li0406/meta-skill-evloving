/**
 * Layout Components for Command Palettes
 *
 * This module exports flexible, reusable layout components for organizing
 * command results in various patterns. All layouts support:
 * - Full keyboard navigation with arrow keys
 * - Accessible ARIA attributes
 * - Responsive design (mobile-first)
 * - Smooth 60fps scrolling and animations
 * - Generic item types via TypeScript interfaces
 *
 * Choose the appropriate layout based on your use case:
 * - SingleColumnLayout: Simple text-based commands, mobile-friendly
 * - TwoColumnLayout: File browsers, document search with preview
 * - MultiPanelLayout: Complex filtering, admin interfaces
 * - CardGridLayout: Visual content, extensions, plugins
 * - HorizontalCardsLayout: Mixed content types, recent items
 */

// Single Column Layout
export { SingleColumnLayout } from './SingleColumnLayout';
export type { Command, SingleColumnLayoutProps } from './SingleColumnLayout';

// Two Column Layout
export { TwoColumnLayout } from './TwoColumnLayout';
export type { TwoColumnLayoutProps } from './TwoColumnLayout';

// Multi Panel Layout
export { MultiPanelLayout } from './MultiPanelLayout';
export type { Filter, FilterOption, MultiPanelLayoutProps } from './MultiPanelLayout';

// Card Grid Layout
export { CardGridLayout } from './CardGridLayout';
export type { CardItem, CardGridLayoutProps } from './CardGridLayout';

// Horizontal Cards Layout
export { HorizontalCardsLayout } from './HorizontalCardsLayout';
export type { HorizontalCardsLayoutProps } from './HorizontalCardsLayout';
