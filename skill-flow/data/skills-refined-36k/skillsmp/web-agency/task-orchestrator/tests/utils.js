/**
 * Shared utilities for task-orchestrator skill tests
 * @module tests/utils
 */

const fs = require('fs');
const path = require('path');

/**
 * Default directories to ignore during file scanning
 * @type {string[]}
 */
const IGNORED_DIRS = ['node_modules', '.git', 'coverage', 'dist', 'tests'];

/**
 * Find all markdown files recursively in a directory
 *
 * @param {string} dir - Directory to scan
 * @param {Object} [options] - Scan options
 * @param {number} [options.maxDepth=5] - Maximum recursion depth
 * @param {string[]} [options.ignoreDirs] - Directories to skip
 * @returns {string[]} Array of absolute file paths
 */
function findMarkdownFiles(dir, options = {}) {
  const { maxDepth = 5, ignoreDirs = IGNORED_DIRS } = options;
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

  scan(dir, 0);
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
 * @param {string} content - Markdown content with frontmatter
 * @returns {Object|null} Parsed frontmatter or null if not found
 */
function parseFrontmatter(content) {
  const match = content.match(/^---\n([\s\S]*?)\n---/);
  if (!match) return null;

  const frontmatter = {};
  const lines = match[1].split('\n');

  for (const line of lines) {
    if (!line.trim() || line.trim().startsWith('#')) continue;

    const colonIndex = line.indexOf(':');
    if (colonIndex > 0) {
      const key = line.substring(0, colonIndex).trim();
      const value = line.substring(colonIndex + 1).trim();
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
 * Print a separator line
 *
 * @param {number} [length=50] - Length of the separator
 * @param {string} [char='='] - Character to use
 */
function printSeparator(length = 50, char = '=') {
  console.log(char.repeat(length));
}

module.exports = {
  findMarkdownFiles,
  safeReadFile,
  parseFrontmatter,
  directoryExists,
  printSeparator,
  IGNORED_DIRS
};
