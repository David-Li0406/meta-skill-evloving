/**
 * Shared utilities for skill tests
 * @module tests/utils
 *
 * NOTE: This module uses synchronous I/O intentionally for test simplicity.
 * For production use, consider async alternatives.
 */

const fs = require('fs');
const path = require('path');

/**
 * Default directories to ignore during file scanning
 * @type {string[]}
 */
const IGNORED_DIRS = ['node_modules', '.git', 'coverage', 'dist', 'tests'];

/**
 * Custom error class for test failures
 * @extends Error
 */
class TestError extends Error {
  constructor(message, context = {}) {
    super(message);
    this.name = 'TestError';
    this.context = context;
  }
}

/**
 * Escape special regex characters in a string
 * @param {string} str - String to escape
 * @returns {string} Escaped string safe for RegExp
 */
function escapeRegex(str) {
  return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

/**
 * Validate and normalize a directory path
 * Prevents path traversal attacks and validates existence
 *
 * @param {string} dir - Directory path to validate
 * @param {string} [rootBoundary] - Optional root boundary to prevent traversal
 * @returns {{ valid: boolean, normalized: string|null, error: string|null }}
 */
function validatePath(dir, rootBoundary = null) {
  if (!dir || typeof dir !== 'string') {
    return { valid: false, normalized: null, error: 'Invalid directory path: must be a non-empty string' };
  }

  const normalized = path.resolve(dir);

  // Check for path traversal if boundary is set
  if (rootBoundary) {
    const normalizedRoot = path.resolve(rootBoundary);
    if (!normalized.startsWith(normalizedRoot)) {
      return { valid: false, normalized: null, error: `Path traversal detected: ${dir} escapes ${rootBoundary}` };
    }
  }

  // Check if directory exists
  try {
    const stat = fs.statSync(normalized);
    if (!stat.isDirectory()) {
      return { valid: false, normalized: null, error: `Path is not a directory: ${dir}` };
    }
  } catch (err) {
    return { valid: false, normalized: null, error: `Directory does not exist: ${dir}` };
  }

  return { valid: true, normalized, error: null };
}

/**
 * Find all markdown files recursively in a directory
 *
 * @param {string} dir - Directory to scan
 * @param {Object} [options] - Scan options
 * @param {number} [options.maxDepth=5] - Maximum recursion depth
 * @param {string[]} [options.ignoreDirs] - Directories to skip
 * @param {string} [options.rootBoundary] - Root boundary for path traversal prevention
 * @returns {string[]} Array of absolute file paths
 * @throws {TestError} If directory validation fails
 */
function findMarkdownFiles(dir, options = {}) {
  const { maxDepth = 5, ignoreDirs = IGNORED_DIRS, rootBoundary = null } = options;

  // Validate directory exists before scanning
  const validation = validatePath(dir, rootBoundary);
  if (!validation.valid) {
    throw new TestError(validation.error, { dir, rootBoundary });
  }

  const files = [];

  function scan(currentDir, depth) {
    if (depth > maxDepth) return;

    try {
      const items = fs.readdirSync(currentDir);
      for (const item of items) {
        if (ignoreDirs.includes(item)) continue;

        const fullPath = path.join(currentDir, item);
        try {
          const stat = fs.statSync(fullPath);
          if (stat.isDirectory()) {
            scan(fullPath, depth + 1);
          } else if (item.endsWith('.md')) {
            files.push(fullPath);
          }
        } catch (err) {
          console.error(`Warning: Cannot access ${fullPath}: ${err.message}`);
        }
      }
    } catch (err) {
      console.error(`Warning: Cannot read directory ${currentDir}: ${err.message}`);
    }
  }

  scan(validation.normalized, 0);
  return files;
}

/**
 * Safely read a file and return its content
 *
 * @param {string} filePath - Path to the file
 * @returns {{ content: string|null, error: string|null }} File content or error message
 */
function safeReadFile(filePath) {
  try {
    return { content: fs.readFileSync(filePath, 'utf-8'), error: null };
  } catch (err) {
    return { content: null, error: `Cannot read file: ${err.message}` };
  }
}

/**
 * Parse YAML frontmatter from markdown content
 *
 * NOTE: This is a simple parser for basic key: value pairs.
 * Limitations:
 * - Does not support multi-line values
 * - Does not support YAML arrays or nested objects
 * - Quoted strings with colons may not parse correctly
 *
 * For complex frontmatter, consider using a proper YAML parser like js-yaml.
 *
 * @param {string} content - Markdown content with frontmatter
 * @returns {Object|null} Parsed frontmatter or null if not found/invalid
 */
function parseFrontmatter(content) {
  if (!content || typeof content !== 'string') {
    return null;
  }

  const match = content.match(/^---\n([\s\S]*?)\n---/);
  if (!match) return null;

  const frontmatter = {};
  const lines = match[1].split('\n');

  for (const line of lines) {
    if (!line.trim() || line.trim().startsWith('#')) continue;

    const colonIndex = line.indexOf(':');
    if (colonIndex > 0) {
      const key = line.substring(0, colonIndex).trim();
      let value = line.substring(colonIndex + 1).trim();

      // Skip empty values
      if (!value) continue;

      // Remove surrounding quotes if present
      if ((value.startsWith('"') && value.endsWith('"')) ||
          (value.startsWith("'") && value.endsWith("'"))) {
        value = value.slice(1, -1);
      }
      if (key) {
        frontmatter[key] = value;
      }
    }
  }

  return Object.keys(frontmatter).length > 0 ? frontmatter : null;
}

/**
 * Check if a directory exists
 *
 * @param {string} dirPath - Directory path to check
 * @returns {boolean} True if directory exists
 */
function directoryExists(dirPath) {
  try {
    return fs.statSync(dirPath).isDirectory();
  } catch {
    return false;
  }
}

/**
 * Check if a file exists
 *
 * @param {string} filePath - File path to check
 * @returns {boolean} True if file exists
 */
function fileExists(filePath) {
  try {
    return fs.statSync(filePath).isFile();
  } catch {
    return false;
  }
}

/**
 * Print a separator line
 *
 * @param {number} [length=50] - Length of the separator
 * @param {string} [char='='] - Character to use
 */
function printSeparator(length = 50, char = '=') {
  console.log(char.repeat(length));
}

/**
 * Count headings in markdown content
 *
 * @param {string} content - Markdown content
 * @returns {number} Number of headings
 */
function countHeadings(content) {
  const matches = content.match(/^#{1,6}\s+.+$/gm);
  return matches ? matches.length : 0;
}

module.exports = {
  // Core utilities
  findMarkdownFiles,
  safeReadFile,
  parseFrontmatter,
  directoryExists,
  fileExists,
  printSeparator,
  countHeadings,

  // Validation utilities
  validatePath,
  escapeRegex,

  // Error handling
  TestError,

  // Constants
  IGNORED_DIRS
};
