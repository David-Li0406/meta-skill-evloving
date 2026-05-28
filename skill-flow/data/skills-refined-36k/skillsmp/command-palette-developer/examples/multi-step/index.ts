/**
 * Multi-step command palette components and utilities
 *
 * Export all multi-step related components for easy importing
 */

export { MultiStepPalette } from './MultiStepPalette';
export type { MultiStepPaletteProps } from './MultiStepPalette';

export { CommandStep, CommandStepSkeleton } from './CommandStep';
export type { CommandStepProps } from './CommandStep';

export { useCommandFlow } from './useCommandFlow';
export type {
  Command,
  BreadcrumbItem,
  UseCommandFlowResult,
} from './useCommandFlow';

export { workflowTree } from './mock-workflows';
export type { CommandTree } from './mock-workflows';
