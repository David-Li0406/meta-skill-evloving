#!/usr/bin/env node
/**
 * elementary.mjs
 * 
 * Manage Elementary Design System assets and extract design information.
 * 
 * FUNCTIONAL CORE: Pure business logic for CSS parsing, token extraction, and installation preparation.
 * Reusable by any agent (Claude Code, VS Code agents, test harness, etc.)
 * 
 * Commands:
 *   list <css-file> [options]  - List component classes and design tokens
 *   install <target-dir>       - Install Elementary assets to target directory
 * 
 * Examples:
 *   elementary.mjs list assets/elementary/components.css
 *   elementary.mjs list assets/elementary/components.css --include-tokens --theme=polished
 *   elementary.mjs list assets/elementary/components.css --format=json
 *   elementary.mjs install ./my-project
 */

import { readFileSync, existsSync, cpSync, mkdirSync } from 'node:fs';
import { join, dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const SKILL_ROOT = join(__dirname, '..');

// =============================================================================
// FUNCTIONAL CORE: Pure business logic
// =============================================================================

/**
 * Extract component class names from CSS content
 * @param {string} cssContent - CSS file content
 * @returns {string[]} - Sorted array of unique class names
 */
export function extractClasses(cssContent) {
  // Extract class names: lines starting with . followed by lowercase/hyphens
  const classPattern = /^\.[a-z][a-z0-9-]*/gm;
  const matches = cssContent.match(classPattern) || [];
  return [...new Set(matches)].sort();
}

/**
 * Extract design tokens (CSS custom properties) from CSS content
 * @param {string} cssContent - CSS file content
 * @returns {string[]} - Sorted array of unique token names
 */
export function extractTokens(cssContent) {
  // Extract CSS custom properties (--var-name)
  const tokenPattern = /--([a-z][a-z0-9-]*)/g;
  const tokenMatches = cssContent.matchAll(tokenPattern);
  return [...new Set([...tokenMatches].map(m => `--${m[1]}`))].sort();
}

/**
 * Categorize tokens by prefix convention
 * @param {string[]} tokens - Array of token names
 * @returns {Object} - Tokens grouped by category
 */
export function categorizeTokens(tokens) {
  return {
    colors: tokens.filter(t => t.startsWith('--c-')),
    backgrounds: tokens.filter(t => t.startsWith('--bg-')),
    spacing: tokens.filter(t => t.startsWith('--s-')),
    radii: tokens.filter(t => t.startsWith('--r-')),
    borders: tokens.filter(t => t.startsWith('--b-')),
    effects: tokens.filter(t => t.startsWith('--x-')),
    typography: tokens.filter(t => t.startsWith('--t-')),
    zIndex: tokens.filter(t => t.startsWith('--z-')),
    animation: tokens.filter(t => t.startsWith('--a-')),
    other: tokens.filter(t => !t.match(/^--(c|bg|s|r|b|x|t|z|a)-/))
  };
}

/**
 * Prepare installation paths (functional core)
 * @param {string} sourcePath - Path to Elementary skill root
 * @param {string} targetPath - Target directory for installation
 * @returns {Object} - Installation paths { from, to }
 */
export function prepareInstallation(sourcePath, targetPath) {
  return {
    from: join(sourcePath, 'assets', 'elementary'),
    to: join(targetPath, 'assets', 'elementary')
  };
}

/**
 * Main extraction logic (pure function)
 * @param {Object} options - Extraction options
 * @returns {Object} - Extraction result
 */
export function extractDesignData(options) {
  const {
    cssFile,
    cssContent,
    includeTokens = true,
    theme = 'high-fidelity',
    themeContent = null
  } = options;

  if (!cssContent) {
    return { error: 'cssContent is required' };
  }

  const classes = extractClasses(cssContent);
  const result = {
    css_file: cssFile,
    classes,
    class_count: classes.length
  };

  if (includeTokens && themeContent) {
    const tokens = extractTokens(themeContent);
    result.tokens = tokens;
    result.token_count = tokens.length;
    result.tokens_by_category = categorizeTokens(tokens);
    result.theme = theme;
  }

  return result;
}

// =============================================================================
// IMPERATIVE SHELL: I/O, CLI parsing, error handling
// =============================================================================

/**
 * Read file with error handling
 * @param {string} filePath - Absolute path to file
 * @returns {string|null} - File content or null on error
 */
function readFile(filePath) {
  if (!existsSync(filePath)) {
    console.error(`Error: File not found: ${filePath}`);
    return null;
  }
  try {
    return readFileSync(filePath, 'utf-8');
  } catch (err) {
    console.error(`Error: Failed to read ${filePath}: ${err.message}`);
    return null;
  }
}

/**
 * Parse command-line arguments
 * @param {string[]} args - Process arguments
 * @returns {Object} - Parsed options
 */
function parseArgs(args) {
  const options = {
    command: null,
    cssFile: null,
    targetDir: null,
    includeTokens: false,
    theme: 'polished',
    format: 'human',
    help: false
  };

  // First arg is command (list or install) or help
  if (args.length > 0) {
    const firstArg = args[0];
    if (firstArg === 'list') {
      options.command = 'list';
      args = args.slice(1);
    } else if (firstArg === 'install') {
      options.command = 'install';
      if (args.length > 1) {
        options.targetDir = args[1];
      }
      return options;
    } else if (firstArg === '--help' || firstArg === '-h') {
      options.help = true;
      return options;
    } else {
      // Legacy mode: assume list command with css file
      options.command = 'list';
    }
  }

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    
    if (arg === '--help' || arg === '-h') {
      options.help = true;
    } else if (arg === '--include-tokens') {
      options.includeTokens = true;
    } else if (arg.startsWith('--theme=')) {
      options.theme = arg.split('=')[1];
    } else if (arg.startsWith('--format=')) {
      options.format = arg.split('=')[1];
    } else if (!arg.startsWith('--') && !options.cssFile) {
      options.cssFile = arg;
    }
  }

  return options;
}

/**
 * Format output for human readability
 * @param {Object} result - Extraction result
 * @returns {string} - Formatted output
 */
function formatHuman(result) {
  if (result.error) {
    return `Error: ${result.error}`;
  }

  let output = `\n📄 CSS File: ${result.css_file}\n`;
  output += `\n🎨 Component Classes (${result.class_count}):\n`;
  result.classes.forEach(cls => {
    output += `  ${cls}\n`;
  });

  if (result.tokens) {
    output += `\n🎯 Design Tokens (${result.token_count}) from ${result.theme} theme:\n\n`;
    
    const categories = result.tokens_by_category;
    const categoryNames = {
      colors: '🌈 Colors',
      backgrounds: '📄 Backgrounds',
      spacing: '📏 Spacing',
      radii: '⭕ Radii',
      borders: '🔲 Borders',
      effects: '✨ Effects',
      typography: '📝 Typography',
      zIndex: '📚 Z-Index',
      animation: '🎬 Animation',
      other: '📦 Other'
    };

    Object.entries(categories).forEach(([category, tokens]) => {
      if (tokens.length > 0) {
        output += `${categoryNames[category]} (${tokens.length}):\n`;
        tokens.forEach(token => {
          output += `  ${token}\n`;
        });
        output += '\n';
      }
    });
  }

  return output;
}

/**
 * Format output as JSON
 * @param {Object} result - Extraction result
 * @returns {string} - JSON string
 */
function formatJson(result) {
  return JSON.stringify(result, null, 2);
}

/**
 * Display help text
 */
function showHelp() {
  console.log(`
elementary.mjs - Manage Elementary Design System assets

Usage:
  elementary.mjs <command> [arguments] [options]

Commands:
  list <css-file>     List component classes and design tokens
  install <dir>       Install Elementary assets to target directory

List Options:
  --include-tokens    Also extract design tokens from theme file
  --theme=<name>      Theme name for token extraction (default: polished)
  --format=<format>   Output format: human, json (default: human)

Global Options:
  --help, -h          Show this help message

Examples:
  # List component classes only
  elementary.mjs list assets/elementary/components.css

  # List classes and tokens from polished theme
  elementary.mjs list assets/elementary/components.css --include-tokens

  # List classes and tokens from sketch theme
  elementary.mjs list assets/elementary/components.css --include-tokens --theme=sketch

  # Output as JSON
  elementary.mjs list assets/elementary/components.css --include-tokens --format=json

  # Install Elementary assets to current directory
  elementary.mjs install .

  # Install Elementary assets to specific directory
  elementary.mjs install ./my-project
`);
}

/**
 * Execute install command (imperative shell)
 * @param {string} targetDir - Target directory for installation
 */
function installAssets(targetDir) {
  if (!targetDir) {
    console.error('Error: Target directory required for install command');
    console.log('Usage: elementary.mjs install <target-dir>');
    process.exit(1);
  }

  const targetPath = resolve(targetDir);
  const { from, to } = prepareInstallation(SKILL_ROOT, targetPath);

  // Check if source exists
  if (!existsSync(from)) {
    console.error(`Error: Elementary assets not found at ${from}`);
    process.exit(1);
  }

  // Create target directory if needed
  try {
    mkdirSync(targetPath, { recursive: true });
  } catch (err) {
    console.error(`Error: Failed to create target directory: ${err.message}`);
    process.exit(1);
  }

  // Copy assets
  try {
    cpSync(from, to, { recursive: true });
    console.log(`✓ Elementary assets installed to: ${to}`);
    console.log('\nImport in your CSS:');
    console.log('  @import \'./assets/elementary/tokens/polished.css\';');
    console.log('  @import \'./assets/elementary/components.css\';');
  } catch (err) {
    console.error(`Error: Failed to copy assets: ${err.message}`);
    process.exit(1);
  }
}

/**
 * Main CLI entry point
 */
function main() {
  const args = process.argv.slice(2);
  const options = parseArgs(args);

  if (options.help) {
    showHelp();
    process.exit(0);
  }

  // Handle install command
  if (options.command === 'install') {
    installAssets(options.targetDir);
    return;
  }

  // Handle list command (default)
  if (!options.cssFile) {
    showHelp();
    process.exit(1);
  }

  // Resolve CSS file path
  const cssPath = join(SKILL_ROOT, options.cssFile);
  const cssContent = readFile(cssPath);
  if (!cssContent) {
    process.exit(1);
  }

  // Read theme file if tokens requested
  let themeContent = null;
  if (options.includeTokens) {
    const themePath = join(SKILL_ROOT, 'assets', 'elementary', 'tokens', `${options.theme}.css`);
    themeContent = readFile(themePath);
    if (!themeContent) {
      console.error(`Warning: Could not read theme file, skipping token extraction`);
    }
  }

  // Extract design data (functional core)
  const result = extractDesignData({
    cssFile: options.cssFile,
    cssContent,
    includeTokens: options.includeTokens,
    theme: options.theme,
    themeContent
  });

  // Format and output (imperative shell)
  const output = options.format === 'json' 
    ? formatJson(result)
    : formatHuman(result);

  console.log(output);

  // Exit with error code if extraction failed
  process.exit(result.error ? 1 : 0);
}

// Run CLI if executed directly
if (import.meta.url === `file://${process.argv[1]}`) {
  main();
}
