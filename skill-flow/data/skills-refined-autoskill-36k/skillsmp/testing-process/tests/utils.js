/**
 * Shared utility functions for Testing Process skill tests
 *
 * @module tests/utils
 */

const fs = require('fs');
const path = require('path');

/**
 * Find all markdown files in a directory (non-recursive)
 *
 * @param {string} dir - Directory path
 * @returns {string[]} Array of file paths
 */
function findMarkdownFiles(dir) {
  try {
    return fs.readdirSync(dir)
      .filter(f => f.endsWith('.md'))
      .map(f => path.join(dir, f));
  } catch {
    return [];
  }
}

/**
 * Safely read file content
 *
 * @param {string} filePath - Path to file
 * @returns {{ content: string|null, error: string|null }}
 */
function safeReadFile(filePath) {
  try {
    return { content: fs.readFileSync(filePath, 'utf8'), error: null };
  } catch (e) {
    return { content: null, error: `Failed to read: ${e.message}` };
  }
}

/**
 * Parse YAML frontmatter from markdown content
 *
 * @param {string} content - Markdown content
 * @returns {Object|null} Parsed frontmatter or null
 */
function parseFrontmatter(content) {
  const match = content.match(/^---\n([\s\S]*?)\n---/);
  if (!match) return null;

  const frontmatter = {};
  match[1].split('\n').forEach(line => {
    const [key, ...rest] = line.split(':');
    if (key && rest.length) {
      frontmatter[key.trim()] = rest.join(':').trim();
    }
  });
  return frontmatter;
}

/**
 * Check if directory exists
 *
 * @param {string} dir - Directory path
 * @returns {boolean}
 */
function directoryExists(dir) {
  try {
    return fs.statSync(dir).isDirectory();
  } catch {
    return false;
  }
}

/**
 * Count technical elements in content
 *
 * @param {string} content - Markdown content
 * @returns {{ codeBlocks: number, tables: number }}
 */
function countTechElements(content) {
  const codeBlocks = (content.match(/```/g) || []).length / 2;
  const tables = (content.match(/\|.*\|/g) || []).length;
  return { codeBlocks: Math.floor(codeBlocks), tables };
}

/**
 * Simple test reporter
 */
class TestReporter {
  constructor(testName) {
    this.testName = testName;
    this.passed = 0;
    this.failed = 0;
    this.warnings = 0;
  }

  header(text) {
    console.log('\n' + '='.repeat(50));
    console.log(`  ${text}`);
    console.log('='.repeat(50) + '\n');
  }

  section(text) {
    console.log(`\n  ${text}`);
  }

  pass(message) {
    console.log(`  [PASS] ${message}`);
    this.passed++;
  }

  fail(message) {
    console.log(`  [FAIL] ${message}`);
    this.failed++;
  }

  warn(message) {
    console.log(`  [WARN] ${message}`);
    this.warnings++;
  }

  info(message) {
    console.log(`\n  [INFO] ${message}`);
  }

  summarize() {
    console.log('\n' + '='.repeat(50));
    console.log(`\n  Results: ${this.passed} passed, ${this.failed} failed`);
    if (this.warnings > 0) {
      console.log(`  Warnings: ${this.warnings}`);
    }

    if (this.failed > 0) {
      process.exit(1);
    }
  }
}

module.exports = {
  findMarkdownFiles,
  safeReadFile,
  parseFrontmatter,
  directoryExists,
  countTechElements,
  TestReporter
};
