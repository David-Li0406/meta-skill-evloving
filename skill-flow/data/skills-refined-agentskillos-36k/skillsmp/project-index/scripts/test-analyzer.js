#!/usr/bin/env node
/**
 * Test Analyzer - Detect test quality issues
 *
 * Usage:
 *   node test-analyzer.js [path]              # Full analysis
 *   node test-analyzer.js [path] --json       # JSON output
 *   node test-analyzer.js [path] --summary    # Summary only
 *   node test-analyzer.js [path] --fix        # Show fix suggestions
 *
 * Detects:
 *   - Pseudo tests: tests without assertions
 *   - Weak assertions: expect(true).toBe(true), toMatchObject({})
 *   - Skipped tests: test.skip, it.skip, describe.skip
 *   - Commented tests: // test(...), // it(...)
 *   - Empty tests: test bodies with no code
 *   - Flaky patterns: setTimeout in tests, Date.now() comparisons
 */

import { promises as fs } from 'fs';
import path from 'path';
import { loadConfig, parseArgs, shouldProcess } from './shared.js';

const IGNORE_DIRS = new Set([
  'node_modules', '.git', 'dist', 'build', 'coverage'
]);

/**
 * @typedef {'pseudo' | 'weak' | 'skipped' | 'commented' | 'empty' | 'flaky'} IssueType
 */

/**
 * @typedef {object} TestIssue
 * @property {IssueType} type
 * @property {string} file
 * @property {number} line
 * @property {string} testName
 * @property {string} description
 * @property {string} [context]
 * @property {string} [suggestion]
 */

/**
 * Patterns for detecting test issues
 */
const ISSUE_PATTERNS = {
  // Pseudo tests: no expect/assert calls
  pseudo: {
    // Match test/it blocks and check if they have assertions
    testBlock: /(?:test|it)\s*\(\s*['"`]([^'"`]+)['"`]\s*,\s*(?:async\s*)?\(\s*\)\s*=>\s*\{([^}]*(?:\{[^}]*\}[^}]*)*)\}/g,
    assertions: /expect\s*\(|assert\.|should\./
  },

  // Weak assertions
  weak: [
    { pattern: /expect\s*\(\s*true\s*\)\s*\.toBe\s*\(\s*true\s*\)/g, desc: 'expect(true).toBe(true) - 无意义断言' },
    { pattern: /expect\s*\(\s*false\s*\)\s*\.toBe\s*\(\s*false\s*\)/g, desc: 'expect(false).toBe(false) - 无意义断言' },
    { pattern: /expect\s*\([^)]+\)\s*\.toMatchObject\s*\(\s*\{\s*\}\s*\)/g, desc: 'toMatchObject({}) - 空对象匹配' },
    { pattern: /expect\s*\([^)]+\)\s*\.toBeDefined\s*\(\s*\)/g, desc: 'toBeDefined() - 弱断言，应验证具体值' },
    { pattern: /expect\s*\([^)]+\)\s*\.toBeTruthy\s*\(\s*\)/g, desc: 'toBeTruthy() - 弱断言，应验证具体值' },
    { pattern: /expect\s*\(\s*\d+\s*\)\s*\.toBeGreaterThan\s*\(\s*0\s*\)/g, desc: '常量断言 - 应验证变量' }
  ],

  // Skipped tests
  skipped: [
    { pattern: /(?:test|it|describe)\.skip\s*\(/g, desc: '跳过的测试' },
    { pattern: /(?:test|it|describe)\.todo\s*\(/g, desc: 'TODO 测试' },
    { pattern: /x(?:test|it|describe)\s*\(/g, desc: 'x 前缀跳过的测试' }
  ],

  // Commented tests
  commented: [
    { pattern: /\/\/\s*(?:test|it|describe)\s*\(/g, desc: '注释掉的测试' },
    { pattern: /\/\*[\s\S]*?(?:test|it|describe)\s*\([\s\S]*?\*\//g, desc: '块注释掉的测试' }
  ],

  // Flaky patterns
  flaky: [
    { pattern: /setTimeout\s*\([^,]+,\s*\d+\s*\)/g, desc: 'setTimeout - 可能导致不稳定' },
    { pattern: /Date\.now\s*\(\s*\)/g, desc: 'Date.now() - 时间依赖可能导致不稳定' },
    { pattern: /Math\.random\s*\(\s*\)/g, desc: 'Math.random() - 随机性可能导致不稳定' },
    { pattern: /new Date\s*\(\s*\)/g, desc: 'new Date() - 时间依赖可能导致不稳定' }
  ]
};

/**
 * Find all test files
 * @param {string} dir
 * @returns {Promise<string[]>}
 */
async function findTestFiles(dir) {
  const results = [];

  async function scan(currentDir) {
    try {
      const entries = await fs.readdir(currentDir, { withFileTypes: true });

      for (const entry of entries) {
        const fullPath = path.join(currentDir, entry.name);

        if (entry.isDirectory()) {
          if (IGNORE_DIRS.has(entry.name)) continue;
          await scan(fullPath);
        } else if (entry.isFile()) {
          if (entry.name.includes('.test.') || entry.name.includes('.spec.')) {
            results.push(fullPath);
          }
        }
      }
    } catch {
      // Skip inaccessible dirs
    }
  }

  await scan(dir);
  return results;
}

/**
 * Get line number for a match position
 * @param {string} content
 * @param {number} position
 * @returns {number}
 */
function getLineNumber(content, position) {
  return content.substring(0, position).split('\n').length;
}

/**
 * Analyze a test file for issues
 * @param {string} filePath
 * @param {string} rootPath
 * @returns {Promise<TestIssue[]>}
 */
async function analyzeTestFile(filePath, rootPath) {
  const issues = [];
  const relativePath = path.relative(rootPath, filePath);

  let content;
  try {
    content = await fs.readFile(filePath, 'utf-8');
  } catch {
    return issues;
  }

  // Check for pseudo tests (no assertions)
  const testBlockRegex = /(?:test|it)\s*\(\s*['"`]([^'"`]+)['"`]\s*,\s*(?:async\s*)?\([^)]*\)\s*=>\s*\{/g;
  let match;

  while ((match = testBlockRegex.exec(content)) !== null) {
    const testName = match[1];
    const startPos = match.index + match[0].length;

    // Find the matching closing brace
    let braceCount = 1;
    let endPos = startPos;
    while (braceCount > 0 && endPos < content.length) {
      if (content[endPos] === '{') braceCount++;
      if (content[endPos] === '}') braceCount--;
      endPos++;
    }

    const testBody = content.substring(startPos, endPos - 1);

    // Check for assertions
    if (!ISSUE_PATTERNS.pseudo.assertions.test(testBody)) {
      issues.push({
        type: 'pseudo',
        file: relativePath,
        line: getLineNumber(content, match.index),
        testName,
        description: '测试没有断言 - 伪测试',
        context: testBody.substring(0, 100).trim(),
        suggestion: '添加 expect() 断言验证行为'
      });
    }

    // Check for empty test
    if (testBody.trim().length < 10) {
      issues.push({
        type: 'empty',
        file: relativePath,
        line: getLineNumber(content, match.index),
        testName,
        description: '空测试或几乎空的测试',
        suggestion: '实现测试逻辑或删除占位符'
      });
    }
  }

  // Check for weak assertions
  for (const { pattern, desc } of ISSUE_PATTERNS.weak) {
    pattern.lastIndex = 0;
    while ((match = pattern.exec(content)) !== null) {
      issues.push({
        type: 'weak',
        file: relativePath,
        line: getLineNumber(content, match.index),
        testName: '',
        description: desc,
        context: match[0],
        suggestion: '使用更具体的断言验证实际值'
      });
    }
  }

  // Check for skipped tests
  for (const { pattern, desc } of ISSUE_PATTERNS.skipped) {
    pattern.lastIndex = 0;
    while ((match = pattern.exec(content)) !== null) {
      issues.push({
        type: 'skipped',
        file: relativePath,
        line: getLineNumber(content, match.index),
        testName: '',
        description: desc,
        suggestion: '修复并启用测试，或删除不再需要的测试'
      });
    }
  }

  // Check for commented tests
  for (const { pattern, desc } of ISSUE_PATTERNS.commented) {
    pattern.lastIndex = 0;
    while ((match = pattern.exec(content)) !== null) {
      issues.push({
        type: 'commented',
        file: relativePath,
        line: getLineNumber(content, match.index),
        testName: '',
        description: desc,
        suggestion: '恢复测试或删除注释代码'
      });
    }
  }

  // Check for flaky patterns
  for (const { pattern, desc } of ISSUE_PATTERNS.flaky) {
    pattern.lastIndex = 0;
    while ((match = pattern.exec(content)) !== null) {
      issues.push({
        type: 'flaky',
        file: relativePath,
        line: getLineNumber(content, match.index),
        testName: '',
        description: desc,
        context: match[0],
        suggestion: '使用 fake timers 或固定值替代'
      });
    }
  }

  return issues;
}

/**
 * Main function
 */
async function main() {
  const args = parseArgs(process.argv.slice(2), {
    json: false,
    summary: false,
    fix: false
  });

  const targetPath = args._?.[0] || path.join(process.cwd(), 'tests');
  const rootPath = path.resolve(targetPath);

  const config = await loadConfig(process.cwd());

  if (!args.json && !args.summary) {
    console.log(`Analyzing test quality in: ${rootPath}\n`);
  }

  // Find all test files
  const testFiles = await findTestFiles(rootPath);

  if (!args.json && !args.summary) {
    console.log(`Found ${testFiles.length} test files\n`);
  }

  // Analyze each file
  /** @type {TestIssue[]} */
  const allIssues = [];

  for (const testFile of testFiles) {
    const issues = await analyzeTestFile(testFile, process.cwd());
    allIssues.push(...issues);
  }

  // Calculate stats
  const stats = {
    total: allIssues.length,
    byType: {
      pseudo: allIssues.filter(i => i.type === 'pseudo').length,
      weak: allIssues.filter(i => i.type === 'weak').length,
      skipped: allIssues.filter(i => i.type === 'skipped').length,
      commented: allIssues.filter(i => i.type === 'commented').length,
      empty: allIssues.filter(i => i.type === 'empty').length,
      flaky: allIssues.filter(i => i.type === 'flaky').length
    }
  };

  // Output
  if (args.json) {
    console.log(JSON.stringify({
      testFiles: testFiles.length,
      stats,
      issues: allIssues
    }, null, 2));
    return;
  }

  if (args.summary) {
    console.log(`Test Files: ${testFiles.length}`);
    console.log(`Total Issues: ${stats.total}\n`);
    console.log(`  🔴 Pseudo (无断言): ${stats.byType.pseudo}`);
    console.log(`  🟠 Weak (弱断言): ${stats.byType.weak}`);
    console.log(`  ⚪ Skipped (跳过): ${stats.byType.skipped}`);
    console.log(`  ⚫ Commented (注释): ${stats.byType.commented}`);
    console.log(`  ⬜ Empty (空测试): ${stats.byType.empty}`);
    console.log(`  🟡 Flaky (不稳定): ${stats.byType.flaky}`);
    return;
  }

  // Full output grouped by type
  const typeLabels = {
    pseudo: '🔴 PSEUDO - 无断言的伪测试',
    weak: '🟠 WEAK - 弱断言',
    skipped: '⚪ SKIPPED - 跳过的测试',
    commented: '⚫ COMMENTED - 注释掉的测试',
    empty: '⬜ EMPTY - 空测试',
    flaky: '🟡 FLAKY - 不稳定模式'
  };

  for (const [type, label] of Object.entries(typeLabels)) {
    const typeIssues = allIssues.filter(i => i.type === type);
    if (typeIssues.length === 0) continue;

    console.log(`=== ${label} (${typeIssues.length}) ===`);
    for (const issue of typeIssues.slice(0, 20)) {
      console.log(`  ${issue.file}:${issue.line}`);
      if (issue.testName) console.log(`    Test: ${issue.testName}`);
      console.log(`    ${issue.description}`);
      if (args.fix && issue.suggestion) {
        console.log(`    Fix: ${issue.suggestion}`);
      }
    }
    if (typeIssues.length > 20) {
      console.log(`  ... and ${typeIssues.length - 20} more`);
    }
    console.log('');
  }

  // Summary
  console.log('────────────────────────────────────────────────────────────');
  console.log(`Total: ${stats.total} issues in ${testFiles.length} files`);
  console.log(`Pseudo: ${stats.byType.pseudo} | Weak: ${stats.byType.weak} | Skipped: ${stats.byType.skipped} | Flaky: ${stats.byType.flaky}`);
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
