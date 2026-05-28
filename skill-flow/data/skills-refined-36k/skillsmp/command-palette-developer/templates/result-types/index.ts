/**
 * Result Type Components
 *
 * Specialized result components for different data types in command palettes.
 * Each component follows consistent patterns for accessibility, theming, and UX.
 *
 * All components accept:
 * - selected: boolean - whether the result is currently selected
 * - onClick: () => void - callback when the result is clicked
 *
 * All components provide skeleton loading states for async data.
 */

export { PersonResult, PersonResultSkeleton } from './PersonResult';
export type { PersonResultProps } from './PersonResult';

export { FileResult, FileResultSkeleton } from './FileResult';
export type { FileResultProps } from './FileResult';

export { ActionResult, ActionResultSkeleton } from './ActionResult';
export type { ActionResultProps } from './ActionResult';

export { CardResult, CardResultSkeleton } from './CardResult';
export type { CardResultProps } from './CardResult';

export { NavigationResult, NavigationResultSkeleton } from './NavigationResult';
export type { NavigationResultProps } from './NavigationResult';
