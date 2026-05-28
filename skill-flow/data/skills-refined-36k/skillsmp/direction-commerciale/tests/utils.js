/**
 * Shared utilities for technical skill tests
 * @module tests/utils
 *
 * ## Output Modes
 * Set OUTPUT_FORMAT=json for CI-friendly JSON output.
 * Default is human-readable console output.
 *
 * Example: OUTPUT_FORMAT=json npm test
 */

const fs = require('fs');
const path = require('path');

/**
 * Check if JSON output mode is enabled
 * @returns {boolean}
 */
function isJsonMode() {
  return process.env.OUTPUT_FORMAT === 'json';
}

/**
 * Test Reporter class supporting console and JSON output modes
 */
class TestReporter {
  constructor(testName) {
    this.testName = testName;
    this.results = [];
    this.startTime = Date.now();
    this.passed = 0;
    this.failed = 0;
  }

  /**
   * Record a passing check
   * @param {string} message - Success message
   * @param {Object} [meta] - Optional metadata
   */
  pass(message, meta = {}) {
    this.passed++;
    this.results.push({ status: 'pass', message, ...meta });
    if (!isJsonMode()) {
      console.log(`  ✅ ${message}`);
    }
  }

  /**
   * Record a failing check
   * @param {string} message - Failure message
   * @param {Object} [meta] - Optional metadata
   */
  fail(message, meta = {}) {
    this.failed++;
    this.results.push({ status: 'fail', message, ...meta });
    if (!isJsonMode()) {
      console.log(`  ❌ ${message}`);
    }
  }

  /**
   * Log a warning (non-fatal)
   * @param {string} message - Warning message
   */
  warn(message) {
    this.results.push({ status: 'warn', message });
    if (!isJsonMode()) {
      console.log(`  ⚠️  ${message}`);
    }
  }

  /**
   * Log an info message
   * @param {string} message - Info message
   */
  info(message) {
    if (!isJsonMode()) {
      console.log(`  ℹ️  ${message}`);
    }
  }

  /**
   * Start a new section/group
   * @param {string} name - Section name
   */
  section(name) {
    if (!isJsonMode()) {
      console.log(`\n📁 ${name}`);
    }
  }

  /**
   * Print a header
   * @param {string} title - Header title
   */
  header(title) {
    if (!isJsonMode()) {
      console.log(`\n🧪 ${title}\n`);
      printSeparator();
    }
  }

  /**
   * Get the final report
   * @returns {Object} Test report object
   */
  getReport() {
    return {
      name: this.testName,
      duration: Date.now() - this.startTime,
      passed: this.passed,
      failed: this.failed,
      total: this.passed + this.failed,
      success: this.failed === 0,
      results: this.results,
    };
  }

  /**
   * Print summary and exit with appropriate code
   */
  summarize() {
    const report = this.getReport();

    if (isJsonMode()) {
      console.log(JSON.stringify(report, null, 2));
    } else {
      printSeparator();
      console.log(`\n📊 Summary:`);
      console.log(`   Passed: ${this.passed}`);
      console.log(`   Failed: ${this.failed}`);
      console.log(`   Duration: ${report.duration}ms`);
      console.log(this.failed === 0 ? '\n✅ All checks passed' : '\n❌ Some checks failed');
    }

    process.exit(this.failed > 0 ? 1 : 0);
  }
}

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
 * @param {number} [options.maxDepth=3] - Maximum recursion depth
 * @param {string[]} [options.ignoreDirs] - Directories to skip
 * @returns {string[]} Array of absolute file paths
 */
function findMarkdownFiles(dir, options = {}) {
  const { maxDepth = 3, ignoreDirs = IGNORED_DIRS } = options;
  const files = [];

  if (!directoryExists(dir)) {
    return files;
  }

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
 * Supports:
 * - Single-line values: key: value
 * - Multi-line values with | or > (literal/folded scalars)
 * - Arrays (both inline and indented list format)
 * - Quoted strings
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
  let currentKey = null;
  let multiLineValue = [];
  let isMultiLine = false;
  let multiLineIndent = 0;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const trimmed = line.trim();

    // Skip empty lines and comments (unless in multi-line mode)
    if (!isMultiLine && (!trimmed || trimmed.startsWith('#'))) continue;

    // Check if we're in multi-line mode
    if (isMultiLine) {
      // Check if this line is still part of the multi-line value
      const lineIndent = line.match(/^(\s*)/)[1].length;

      if (lineIndent >= multiLineIndent && (trimmed || multiLineValue.length > 0)) {
        multiLineValue.push(trimmed);
        continue;
      } else {
        // End of multi-line value
        if (currentKey) {
          frontmatter[currentKey] = multiLineValue.join('\n').trim();
        }
        isMultiLine = false;
        multiLineValue = [];
        currentKey = null;
      }
    }

    // Check for array item (starts with -)
    if (trimmed.startsWith('- ') && currentKey) {
      const arrayValue = trimmed.substring(2).trim();
      if (!Array.isArray(frontmatter[currentKey])) {
        frontmatter[currentKey] = [];
      }
      // Remove quotes if present
      const cleanValue = arrayValue.replace(/^["']|["']$/g, '');
      frontmatter[currentKey].push(cleanValue);
      continue;
    }

    const colonIndex = line.indexOf(':');
    if (colonIndex > 0) {
      const key = line.substring(0, colonIndex).trim();
      let value = line.substring(colonIndex + 1).trim();

      // Check for multi-line scalar indicators
      if (value === '|' || value === '>' || value === '|-' || value === '>-') {
        currentKey = key;
        isMultiLine = true;
        multiLineIndent = (lines[i + 1]?.match(/^(\s*)/)?.[1]?.length) || 2;
        multiLineValue = [];
        continue;
      }

      // Check for inline array
      if (value.startsWith('[') && value.endsWith(']')) {
        const items = value.slice(1, -1).split(',').map(item => {
          return item.trim().replace(/^["']|["']$/g, '');
        }).filter(Boolean);
        frontmatter[key] = items;
        currentKey = key;
        continue;
      }

      // Empty value might be followed by array items
      if (!value) {
        currentKey = key;
        continue;
      }

      // Remove surrounding quotes if present
      if ((value.startsWith('"') && value.endsWith('"')) ||
          (value.startsWith("'") && value.endsWith("'"))) {
        value = value.slice(1, -1);
      }
      if (key) {
        frontmatter[key] = value;
        currentKey = key;
      }
    }
  }

  // Handle any remaining multi-line value
  if (isMultiLine && currentKey && multiLineValue.length > 0) {
    frontmatter[currentKey] = multiLineValue.join('\n').trim();
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
 * Count technical elements in content
 *
 * @param {string} content - Markdown content
 * @returns {Object} Counts of technical elements
 */
function countTechElements(content) {
  return {
    codeBlocks: (content.match(/```\w+/g) || []).length,
    tables: (content.match(/\|.*\|/g) || []).length,
    checklists: (content.match(/- \[ \]/g) || []).length,
    diagrams: (content.match(/```(mermaid|ascii|diagram)/g) || []).length
  };
}

module.exports = {
  findMarkdownFiles,
  safeReadFile,
  parseFrontmatter,
  directoryExists,
  fileExists,
  printSeparator,
  countTechElements,
  isJsonMode,
  TestReporter,
  IGNORED_DIRS
};
