/**
 * Shared utilities for frontend skill tests
 * @module tests/utils
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

  pass(message, meta = {}) {
    this.passed++;
    this.results.push({ status: 'pass', message, ...meta });
    if (!isJsonMode()) {
      console.log(`  ✅ ${message}`);
    }
  }

  fail(message, meta = {}) {
    this.failed++;
    this.results.push({ status: 'fail', message, ...meta });
    if (!isJsonMode()) {
      console.log(`  ❌ ${message}`);
    }
  }

  warn(message) {
    this.results.push({ status: 'warn', message });
    if (!isJsonMode()) {
      console.log(`  ⚠️  ${message}`);
    }
  }

  info(message) {
    if (!isJsonMode()) {
      console.log(`  ℹ️  ${message}`);
    }
  }

  section(name) {
    if (!isJsonMode()) {
      console.log(`\n📁 ${name}`);
    }
  }

  header(title) {
    if (!isJsonMode()) {
      console.log(`\n🧪 ${title}\n`);
      printSeparator();
    }
  }

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

const IGNORED_DIRS = ['node_modules', '.git', 'coverage', 'dist', 'tests'];

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

function safeReadFile(filePath) {
  try {
    return { content: fs.readFileSync(filePath, 'utf-8'), error: null };
  } catch (err) {
    return { content: null, error: `Cannot read file: ${err.message}` };
  }
}

function parseFrontmatter(content) {
  if (!content || typeof content !== 'string') {
    return null;
  }

  const match = content.match(/^---\n([\s\S]*?)\n---/);
  if (!match) return null;

  const frontmatter = {};
  const lines = match[1].split('\n');

  for (const line of lines) {
    const colonIndex = line.indexOf(':');
    if (colonIndex > 0) {
      const key = line.substring(0, colonIndex).trim();
      let value = line.substring(colonIndex + 1).trim();

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

function directoryExists(dirPath) {
  try {
    return fs.statSync(dirPath).isDirectory();
  } catch {
    return false;
  }
}

function fileExists(filePath) {
  try {
    return fs.statSync(filePath).isFile();
  } catch {
    return false;
  }
}

function printSeparator(length = 50, char = '=') {
  console.log(char.repeat(length));
}

module.exports = {
  findMarkdownFiles,
  safeReadFile,
  parseFrontmatter,
  directoryExists,
  fileExists,
  printSeparator,
  isJsonMode,
  TestReporter,
  IGNORED_DIRS
};
