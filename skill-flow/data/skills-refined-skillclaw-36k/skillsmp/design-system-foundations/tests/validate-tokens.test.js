#!/usr/bin/env node
/**
 * Test: Validate CSS Token Definitions
 *
 * Validates that CSS custom properties (design tokens) are properly defined:
 * - Color tokens follow naming convention
 * - Spacing tokens use consistent scale
 * - Typography tokens are complete
 * - Shadow/elevation tokens are present
 *
 * @module tests/validate-tokens
 */

const path = require('path');
const {
  safeReadFile,
  fileExists,
  extractCSSVariables,
  printSeparator
} = require('./utils');
const { AGENTS_DIR, TOKEN_PATTERNS } = require('./config');

let passed = 0;
let failed = 0;

/**
 * Log a test result
 * @param {boolean} success - Test passed
 * @param {string} message - Test description
 * @param {string[]} [details] - Optional details to show on failure
 */
function logResult(success, message, details = []) {
  if (success) {
    console.log(`  ✅ ${message}`);
    passed++;
  } else {
    console.log(`  ❌ ${message}`);
    for (const detail of details) {
      console.log(`     └─ ${detail}`);
    }
    failed++;
  }
}

/**
 * Validate color tokens
 * @param {string} content - File content
 * @returns {{ passed: boolean, details: string[] }}
 */
function validateColorTokens(content) {
  const details = [];
  const cssVars = extractCSSVariables(content);

  // Check for color palette (50-900 scale)
  const colorScales = ['50', '100', '200', '300', '400', '500', '600', '700', '800', '900'];
  const hasColorScale = colorScales.some(scale =>
    cssVars.some(v => v.includes(`-${scale}`))
  );

  if (!hasColorScale) {
    details.push('Missing color scale (50-900)');
  }

  // Check for semantic colors
  const semanticColors = ['primary', 'secondary', 'success', 'warning', 'error'];
  const missingSemantics = semanticColors.filter(semantic =>
    !cssVars.some(v => v.includes(semantic))
  );

  if (missingSemantics.length > 0) {
    details.push(`Missing semantic colors: ${missingSemantics.join(', ')}`);
  }

  // Check for background/foreground
  const hasBackground = cssVars.some(v => v.includes('background'));
  const hasForeground = cssVars.some(v => v.includes('foreground'));

  if (!hasBackground) details.push('Missing background color tokens');
  if (!hasForeground) details.push('Missing foreground color tokens');

  return { passed: details.length === 0, details };
}

/**
 * Validate spacing tokens
 * @param {string} content - File content
 * @returns {{ passed: boolean, details: string[] }}
 */
function validateSpacingTokens(content) {
  const details = [];
  const cssVars = extractCSSVariables(content);

  // Check for spacing scale
  const spacingVars = cssVars.filter(v => v.startsWith('--space'));
  if (spacingVars.length < 8) {
    details.push(`Only ${spacingVars.length} spacing tokens defined (expected 8+)`);
  }

  // Check for radius tokens
  const radiusVars = cssVars.filter(v => v.startsWith('--radius'));
  if (radiusVars.length < 4) {
    details.push(`Only ${radiusVars.length} radius tokens defined (expected 4+)`);
  }

  return { passed: details.length === 0, details };
}

/**
 * Validate typography tokens
 * @param {string} content - File content
 * @returns {{ passed: boolean, details: string[] }}
 */
function validateTypographyTokens(content) {
  const details = [];
  const cssVars = extractCSSVariables(content);

  // Check for font size scale
  const fontSizes = cssVars.filter(v => v.includes('font-size') || v.includes('text-'));
  if (fontSizes.length < 5) {
    details.push(`Only ${fontSizes.length} font size tokens (expected 5+)`);
  }

  // Check for font weights
  const fontWeights = cssVars.filter(v => v.includes('font-weight') || v.includes('weight'));
  if (fontWeights.length < 3) {
    details.push(`Only ${fontWeights.length} font weight tokens (expected 3+)`);
  }

  // Check for line heights
  const lineHeights = cssVars.filter(v => v.includes('leading') || v.includes('line-height'));
  if (lineHeights.length < 3) {
    details.push(`Only ${lineHeights.length} line height tokens (expected 3+)`);
  }

  return { passed: details.length === 0, details };
}

/**
 * Validate shadow/elevation tokens
 * @param {string} content - File content
 * @returns {{ passed: boolean, details: string[] }}
 */
function validateShadowTokens(content) {
  const details = [];
  const cssVars = extractCSSVariables(content);

  // Check for shadow scale
  const shadows = cssVars.filter(v => v.includes('shadow'));
  if (shadows.length < 4) {
    details.push(`Only ${shadows.length} shadow tokens (expected 4+)`);
  }

  // Check for z-index scale
  const zIndex = cssVars.filter(v => v.includes('z-') || v.includes('zindex'));
  if (zIndex.length < 3) {
    details.push(`Only ${zIndex.length} z-index tokens (expected 3+)`);
  }

  // Check for focus ring
  const focusRing = cssVars.filter(v => v.includes('focus') || v.includes('ring'));
  if (focusRing.length < 1) {
    details.push('Missing focus ring tokens');
  }

  return { passed: details.length === 0, details };
}

// Main execution
console.log('🧪 Validating CSS Token Definitions\n');
printSeparator();

// Validate colors.md
console.log('\n🎨 Color Tokens (colors.md)\n');
const colorsFile = path.join(AGENTS_DIR, 'foundations', 'colors.md');
if (fileExists(colorsFile)) {
  const { content } = safeReadFile(colorsFile);
  const colorResult = validateColorTokens(content);
  logResult(colorResult.passed, 'Color tokens properly defined', colorResult.details);
} else {
  logResult(false, 'colors.md exists', ['File not found']);
}

// Validate spacing.md
console.log('\n📐 Spacing Tokens (spacing.md)\n');
const spacingFile = path.join(AGENTS_DIR, 'foundations', 'spacing.md');
if (fileExists(spacingFile)) {
  const { content } = safeReadFile(spacingFile);
  const spacingResult = validateSpacingTokens(content);
  logResult(spacingResult.passed, 'Spacing tokens properly defined', spacingResult.details);
} else {
  logResult(false, 'spacing.md exists', ['File not found']);
}

// Validate typography.md
console.log('\n🔤 Typography Tokens (typography.md)\n');
const typographyFile = path.join(AGENTS_DIR, 'foundations', 'typography.md');
if (fileExists(typographyFile)) {
  const { content } = safeReadFile(typographyFile);
  const typographyResult = validateTypographyTokens(content);
  logResult(typographyResult.passed, 'Typography tokens properly defined', typographyResult.details);
} else {
  logResult(false, 'typography.md exists', ['File not found']);
}

// Validate shadows.md
console.log('\n🌑 Shadow/Elevation Tokens (shadows.md)\n');
const shadowsFile = path.join(AGENTS_DIR, 'foundations', 'shadows.md');
if (fileExists(shadowsFile)) {
  const { content } = safeReadFile(shadowsFile);
  const shadowResult = validateShadowTokens(content);
  logResult(shadowResult.passed, 'Shadow tokens properly defined', shadowResult.details);
} else {
  logResult(false, 'shadows.md exists', ['File not found']);
}

console.log('\n');
printSeparator();
console.log(`\n📊 Results: ${passed} passed, ${failed} failed`);

if (failed > 0) {
  console.log('\n❌ Some tests failed');
  process.exit(1);
} else {
  console.log('\n✅ All tests passed');
  process.exit(0);
}
