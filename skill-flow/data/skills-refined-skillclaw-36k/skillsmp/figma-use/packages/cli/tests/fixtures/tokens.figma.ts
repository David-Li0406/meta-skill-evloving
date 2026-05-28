/**
 * Example Figma design tokens using defineVars
 *
 * Usage:
 * ```tsx
 * import { colors, spacing } from './tokens.figma'
 *
 * <Frame style={{ backgroundColor: colors.primary, padding: spacing.md }}>
 * ```
 */

import { defineVars } from '../../src/render/index.ts'

// Color tokens - use Figma variable names!
// Names are resolved to IDs at render time
export const colors = defineVars({
  // Grays
  gray50: 'Colors/Gray/50',
  gray100: 'Colors/Gray/100',
  gray200: 'Colors/Gray/200',
  gray300: 'Colors/Gray/300',
  gray400: 'Colors/Gray/400',
  gray500: 'Colors/Gray/500',

  // Semantic aliases
  primary: 'Colors/Blue/500',
  secondary: 'Colors/Gray/500',
  background: 'Colors/Gray/50'
})

// Note: For non-color variables (spacing, radius),
// use the actual values directly since multiplayer
// variable binding currently only supports colors
export const spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32
}
