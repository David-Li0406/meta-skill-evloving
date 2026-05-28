#!/usr/bin/env node
/**
 * Test Organizer - Analyze and migrate tests to match source structure
 *
 * Mapping rule: js/agents/X/Y.js → tests/agents/X/Y.test.js
 *
 * Usage:
 *   node test-organizer.js --analyze          # Show current vs expected locations
 *   node test-organizer.js --misplaced        # Only show misplaced tests
 *   node test-organizer.js --migrate          # Generate migration commands
 *   node test-organizer.js --migrate --exec   # Execute migration
 */

import { promises as fs } from 'fs';
import path from 'path';

const ROOT = process.cwd();
const TESTS_DIR = path.join(ROOT, 'tests', 'agents');
const SOURCE_DIR = path.join(ROOT, 'js', 'agents');

const IGNORE_DIRS = new Set(['node_modules', '.git', 'dist', 'coverage']);

/**
 * Find all test files
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
        } else if (entry.isFile() && entry.name.endsWith('.test.js')) {
          results.push(fullPath);
        }
      }
    } catch { /* skip */ }
  }

  await scan(dir);
  return results;
}

/**
 * Find all source files
 */
async function findSourceFiles(dir) {
  const results = [];

  async function scan(currentDir) {
    try {
      const entries = await fs.readdir(currentDir, { withFileTypes: true });
      for (const entry of entries) {
        const fullPath = path.join(currentDir, entry.name);
        if (entry.isDirectory()) {
          if (IGNORE_DIRS.has(entry.name)) continue;
          await scan(fullPath);
        } else if (entry.isFile() && entry.name.endsWith('.js') && !entry.name.endsWith('.test.js')) {
          results.push(fullPath);
        }
      }
    } catch { /* skip */ }
  }

  await scan(dir);
  return results;
}

/**
 * Convert source path to expected test path
 * js/agents/core/kernel.js → tests/agents/core/kernel.test.js
 */
function sourceToTestPath(sourcePath) {
  const relative = path.relative(SOURCE_DIR, sourcePath);
  const parsed = path.parse(relative);
  const testName = `${parsed.name}.test.js`;
  return path.join(TESTS_DIR, parsed.dir, testName);
}

/**
 * Convert test path to expected source path
 * tests/agents/core/kernel.test.js → js/agents/core/kernel.js
 */
function testToSourcePath(testPath) {
  const relative = path.relative(TESTS_DIR, testPath);
  const parsed = path.parse(relative);
  const sourceName = parsed.name.replace(/\.test$/, '') + '.js';
  return path.join(SOURCE_DIR, parsed.dir, sourceName);
}

/**
 * Try to find actual source file for a test
 */
async function findActualSource(testPath, sourceFiles) {
  const testName = path.basename(testPath, '.test.js');

  // Direct match
  const directMatch = sourceFiles.find(s => path.basename(s, '.js') === testName);
  if (directMatch) return directMatch;

  // Fuzzy match (remove common prefixes/suffixes)
  const patterns = [
    testName,
    testName.replace(/^test-/, ''),
    testName.replace(/-test$/, ''),
    testName.replace(/\.vitest$/, ''),
    testName.replace(/\.integration$/, ''),
    testName.replace(/\.e2e$/, '')
  ];

  for (const pattern of patterns) {
    const match = sourceFiles.find(s => path.basename(s, '.js') === pattern);
    if (match) return match;
  }

  return null;
}

async function main() {
  const args = process.argv.slice(2);
  const analyzeMode = args.includes('--analyze') || args.length === 0;
  const misplacedOnly = args.includes('--misplaced');
  const migrateMode = args.includes('--migrate');
  const execMode = args.includes('--exec');

  console.log('Scanning test files...\n');

  const testFiles = await findTestFiles(TESTS_DIR);
  const sourceFiles = await findSourceFiles(SOURCE_DIR);

  console.log(`Found ${testFiles.length} test files`);
  console.log(`Found ${sourceFiles.length} source files\n`);

  const analysis = [];
  const migrations = [];

  for (const testPath of testFiles) {
    const relativTest = path.relative(ROOT, testPath);
    const expectedSource = testToSourcePath(testPath);
    const relativeExpectedSource = path.relative(ROOT, expectedSource);

    // Check if expected source exists
    let sourceExists = false;
    try {
      await fs.access(expectedSource);
      sourceExists = true;
    } catch { /* doesn't exist */ }

    // Find actual source
    const actualSource = await findActualSource(testPath, sourceFiles);
    const relativeActualSource = actualSource ? path.relative(ROOT, actualSource) : null;

    // Determine status
    let status = 'unknown';
    let expectedTestPath = null;

    if (sourceExists) {
      status = 'correct';
    } else if (actualSource) {
      expectedTestPath = sourceToTestPath(actualSource);
      const relativeExpectedTest = path.relative(ROOT, expectedTestPath);

      if (relativeExpectedTest === relativTest) {
        status = 'correct';
      } else {
        status = 'misplaced';
        migrations.push({
          from: relativTest,
          to: relativeExpectedTest,
          source: relativeActualSource
        });
      }
    } else {
      status = 'orphan'; // No matching source found
    }

    analysis.push({
      test: relativTest,
      status,
      expectedSource: relativeExpectedSource,
      actualSource: relativeActualSource,
      expectedTest: expectedTestPath ? path.relative(ROOT, expectedTestPath) : null
    });
  }

  // Statistics
  const stats = {
    correct: analysis.filter(a => a.status === 'correct').length,
    misplaced: analysis.filter(a => a.status === 'misplaced').length,
    orphan: analysis.filter(a => a.status === 'orphan').length
  };

  if (analyzeMode || misplacedOnly) {
    if (!misplacedOnly) {
      console.log('=== CORRECT (test matches source location) ===\n');
      for (const a of analysis.filter(x => x.status === 'correct').slice(0, 10)) {
        console.log(`  ✓ ${a.test}`);
      }
      if (stats.correct > 10) {
        console.log(`  ... +${stats.correct - 10} more\n`);
      }
    }

    if (stats.misplaced > 0) {
      console.log('\n=== MISPLACED (test should be moved) ===\n');
      for (const a of analysis.filter(x => x.status === 'misplaced')) {
        console.log(`  ✗ ${a.test}`);
        console.log(`    source: ${a.actualSource}`);
        console.log(`    should be: ${a.expectedTest}\n`);
      }
    }

    if (stats.orphan > 0 && !misplacedOnly) {
      console.log('\n=== ORPHAN (no matching source found) ===\n');
      for (const a of analysis.filter(x => x.status === 'orphan').slice(0, 20)) {
        console.log(`  ? ${a.test}`);
      }
      if (stats.orphan > 20) {
        console.log(`  ... +${stats.orphan - 20} more`);
      }
    }

    console.log('\n' + '─'.repeat(50));
    console.log(`Total: ${testFiles.length} | Correct: ${stats.correct} | Misplaced: ${stats.misplaced} | Orphan: ${stats.orphan}`);
  }

  if (migrateMode && migrations.length > 0) {
    console.log('\n=== MIGRATION COMMANDS ===\n');

    for (const m of migrations) {
      const targetDir = path.dirname(m.to);
      console.log(`mkdir -p ${targetDir}`);
      console.log(`git mv ${m.from} ${m.to}`);
      console.log('');
    }

    if (execMode) {
      console.log('\nExecuting migrations...\n');
      for (const m of migrations) {
        const targetDir = path.dirname(path.join(ROOT, m.to));
        try {
          await fs.mkdir(targetDir, { recursive: true });
          const { execSync } = await import('child_process');
          execSync(`git mv "${m.from}" "${m.to}"`, { cwd: ROOT, stdio: 'pipe' });
          console.log(`  ✓ ${m.from} → ${m.to}`);
        } catch (err) {
          console.log(`  ✗ ${m.from}: ${err.message}`);
        }
      }
    }
  }
}

main().catch(console.error);
