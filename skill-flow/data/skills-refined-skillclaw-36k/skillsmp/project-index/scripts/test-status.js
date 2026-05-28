#!/usr/bin/env node
/**
 * Test Status - Check test coverage via symbol-level import analysis
 *
 * Usage:
 *   node test-status.js [path]              # Full status report
 *   node test-status.js [path] --json       # JSON output
 *   node test-status.js [path] --untested   # Only show untested files
 *   node test-status.js [path] --stale      # Only show stale tests
 *   node test-status.js [path] --summary    # Summary only
 *   node test-status.js [path] --imports    # Show import details
 *
 * Analysis method:
 *   1. Build symbol→source mapping from index.js re-exports
 *   2. Parse test files for imported symbols
 *   3. Trace symbols back to actual source files
 *   4. Compare mtimes to detect stale tests
 *
 * Status types:
 *   - untested: No test file imports symbols from this source
 *   - stale: Test file exists but source code is newer
 *   - covered: Test file exists and is up-to-date
 */

import { promises as fs } from 'fs';
import path from 'path';
import { loadConfig, parseArgs, shouldProcess } from './shared.js';

const CODE_EXTENSIONS = new Set(['.js', '.mjs', '.cjs']);

const IGNORE_DIRS = new Set([
  'node_modules', '.git', 'dist', 'build', '.next', '__pycache__',
  'venv', '.venv', 'target', 'vendor', '.cache', 'coverage',
  '.turbo', '.nuxt', '.output', 'out'
]);

/**
 * Parse export statements from an index file to build symbol→source mapping
 * Handles: export { X, Y } from './file.js', export * from './file.js'
 * @param {string} content - File content
 * @param {string} indexDir - Directory containing the index file
 * @param {string} rootPath - Project root
 * @returns {Map<string, string>} Map of symbol name → source file (relative to root)
 */
function parseExports(content, indexDir, rootPath) {
  const symbolToSource = new Map();

  // Match: export { X, Y, Z as W } from './file.js'
  const namedExportRegex = /export\s*\{([^}]+)\}\s*from\s*['"]([^'"]+)['"]/g;
  let match;

  while ((match = namedExportRegex.exec(content)) !== null) {
    const symbols = match[1];
    const fromPath = match[2];

    // Resolve the source file path
    let resolvedPath = path.resolve(indexDir, fromPath);
    if (!path.extname(resolvedPath)) {
      resolvedPath += '.js';
    }
    const relativePath = path.relative(rootPath, resolvedPath);

    // Parse symbol names (handle "X as Y" syntax)
    const symbolList = symbols.split(',').map(s => s.trim());
    for (const sym of symbolList) {
      const asMatch = sym.match(/(\w+)\s+as\s+(\w+)/);
      const symbolName = asMatch ? asMatch[2] : sym.trim();
      if (symbolName) {
        symbolToSource.set(symbolName, relativePath);
      }
    }
  }

  // Match: export * from './file.js' (re-export all - mark with special key)
  const starExportRegex = /export\s*\*\s*from\s*['"]([^'"]+)['"]/g;
  while ((match = starExportRegex.exec(content)) !== null) {
    const fromPath = match[1];
    let resolvedPath = path.resolve(indexDir, fromPath);
    if (!path.extname(resolvedPath)) {
      resolvedPath += '.js';
    }
    const relativePath = path.relative(rootPath, resolvedPath);
    // Use special marker for star exports
    symbolToSource.set(`__star__${relativePath}`, relativePath);
  }

  return symbolToSource;
}

/**
 * Parse import statements from a test file
 * Returns both the imported symbols and the source path
 * @param {string} content - File content
 * @returns {Array<{symbols: string[], fromPath: string}>}
 */
function parseImports(content) {
  const imports = [];

  // Match: import { X, Y } from 'path'
  const namedImportRegex = /import\s*\{([^}]+)\}\s*from\s*['"]([^'"]+)['"]/g;
  let match;

  while ((match = namedImportRegex.exec(content)) !== null) {
    const symbols = match[1].split(',').map(s => {
      const asMatch = s.trim().match(/(\w+)\s+as\s+(\w+)/);
      return asMatch ? asMatch[1] : s.trim();
    }).filter(Boolean);
    const fromPath = match[2];

    if (fromPath.startsWith('.')) {
      imports.push({ symbols, fromPath });
    }
  }

  // Match: import X from 'path' (default import)
  const defaultImportRegex = /import\s+(\w+)\s+from\s*['"]([^'"]+)['"]/g;
  while ((match = defaultImportRegex.exec(content)) !== null) {
    const symbol = match[1];
    const fromPath = match[2];
    if (fromPath.startsWith('.') && symbol !== '{') {
      imports.push({ symbols: [symbol], fromPath });
    }
  }

  return imports;
}

/**
 * Resolve import path to absolute path
 * @param {string} importPath - Import path from source
 * @param {string} fromFile - File containing the import
 * @returns {string} Resolved absolute path
 */
function resolveImport(importPath, fromFile) {
  const dir = path.dirname(fromFile);
  let resolved = path.resolve(dir, importPath);

  if (!path.extname(resolved)) {
    resolved += '.js';
  }

  return resolved;
}

/**
 * Check if a path is an index file
 * @param {string} filePath
 * @returns {boolean}
 */
function isIndexFile(filePath) {
  const basename = path.basename(filePath);
  return basename === 'index.js' || basename === 'index.mjs';
}

/**
 * Find all test files in tests/ directory
 * @param {string} testsDir - Tests directory path
 * @returns {Promise<string[]>} List of test file paths
 */
async function findTestFiles(testsDir) {
  const results = [];

  async function scan(dir) {
    try {
      const entries = await fs.readdir(dir, { withFileTypes: true });

      for (const entry of entries) {
        const fullPath = path.join(dir, entry.name);

        if (entry.isDirectory()) {
          if (IGNORE_DIRS.has(entry.name)) continue;
          await scan(fullPath);
        } else if (entry.isFile()) {
          if (entry.name.includes('.test.') || entry.name.includes('.spec.') ||
              entry.name.endsWith('.js')) {
            results.push(fullPath);
          }
        }
      }
    } catch {
      // Skip inaccessible dirs
    }
  }

  await scan(testsDir);
  return results;
}

/**
 * Build index file symbol mappings for the entire project
 * @param {string} rootPath - Project root
 * @returns {Promise<Map<string, Map<string, string>>>} Map of index file → (symbol → source file)
 */
async function buildIndexMappings(rootPath) {
  const indexMappings = new Map();

  async function scan(dir) {
    try {
      const entries = await fs.readdir(dir, { withFileTypes: true });

      for (const entry of entries) {
        const fullPath = path.join(dir, entry.name);

        if (entry.isDirectory()) {
          if (IGNORE_DIRS.has(entry.name)) continue;
          await scan(fullPath);
        } else if (entry.isFile() && isIndexFile(fullPath)) {
          try {
            const content = await fs.readFile(fullPath, 'utf-8');
            const symbolMap = parseExports(content, path.dirname(fullPath), rootPath);
            if (symbolMap.size > 0) {
              const relativePath = path.relative(rootPath, fullPath);
              indexMappings.set(relativePath, symbolMap);
            }
          } catch {
            // Skip unreadable files
          }
        }
      }
    } catch {
      // Skip inaccessible dirs
    }
  }

  await scan(rootPath);
  return indexMappings;
}

/**
 * Build source→test mapping by analyzing imports in test files
 * Uses symbol-level tracing through index files
 * @param {string} rootPath - Project root
 * @param {Map<string, Map<string, string>>} indexMappings - Index file symbol mappings
 * @returns {Promise<Map<string, {testFiles: string[], testMtime: Date}>>} Map of source→test info
 */
async function buildImportMap(rootPath, indexMappings) {
  const testsDir = path.join(rootPath, 'tests');
  const sourceToTests = new Map();

  try {
    await fs.access(testsDir);
  } catch {
    return sourceToTests;
  }

  const testFiles = await findTestFiles(testsDir);

  for (const testFile of testFiles) {
    try {
      const content = await fs.readFile(testFile, 'utf-8');
      const imports = parseImports(content);
      const testStat = await fs.stat(testFile);

      for (const { symbols, fromPath } of imports) {
        const resolvedPath = resolveImport(fromPath, testFile);
        const relativePath = path.relative(rootPath, resolvedPath);

        // Check if this is an index file with known symbol mappings
        const symbolMap = indexMappings.get(relativePath);

        if (symbolMap && symbols.length > 0) {
          // Trace each imported symbol to its actual source file
          for (const symbol of symbols) {
            const sourceFile = symbolMap.get(symbol);
            if (sourceFile) {
              // Map to the actual source file, not the index
              addMapping(sourceToTests, sourceFile, testFile, testStat.mtime);
            }
          }
          // Also map the index.js itself (it's still being imported)
          addMapping(sourceToTests, relativePath, testFile, testStat.mtime);
        } else {
          // Direct import (not through index), map as-is
          addMapping(sourceToTests, relativePath, testFile, testStat.mtime);
        }
      }
    } catch {
      // Skip unreadable test files
    }
  }

  return sourceToTests;
}

/**
 * Helper to add a source→test mapping
 */
function addMapping(map, sourceFile, testFile, testMtime) {
  if (!map.has(sourceFile)) {
    map.set(sourceFile, { testFiles: [], testMtime: null });
  }
  const entry = map.get(sourceFile);
  if (!entry.testFiles.includes(testFile)) {
    entry.testFiles.push(testFile);
  }
  if (!entry.testMtime || testMtime > entry.testMtime) {
    entry.testMtime = testMtime;
  }
}

/**
 * Find all code files in a directory recursively
 * @param {string} dir - Directory to scan
 * @param {string} rootPath - Project root
 * @param {object} config - Config with include/ignore
 * @returns {Promise<string[]>} List of code file paths (relative)
 */
async function findCodeFiles(dir, rootPath, config) {
  const results = [];

  async function scan(currentDir) {
    try {
      const entries = await fs.readdir(currentDir, { withFileTypes: true });

      for (const entry of entries) {
        const fullPath = path.join(currentDir, entry.name);
        const relativePath = path.relative(rootPath, fullPath);

        if (entry.isDirectory()) {
          if (IGNORE_DIRS.has(entry.name)) continue;
          await scan(fullPath);
        } else if (entry.isFile()) {
          const ext = path.extname(entry.name).toLowerCase();
          if (!CODE_EXTENSIONS.has(ext)) continue;

          // Skip test files
          if (entry.name.includes('.test.') || entry.name.includes('.spec.')) continue;

          // Apply include/ignore filter
          if (!shouldProcess(relativePath, config)) continue;

          results.push(relativePath);
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
 * @typedef {'untested' | 'stale' | 'covered'} TestStatus
 */

/**
 * @typedef {object} TestResult
 * @property {string} path - Source file path (relative)
 * @property {TestStatus} status - Test status
 * @property {string[]} [testFiles] - Test files that import this source
 * @property {Date} [sourceMtime] - Source file mtime
 * @property {Date} [testMtime] - Newest test file mtime
 */

/**
 * Main function
 */
async function main() {
  const args = parseArgs(process.argv.slice(2), {
    json: false,
    untested: false,
    stale: false,
    summary: false,
    imports: false
  });

  const targetPath = args._?.[0] || process.cwd();
  const rootPath = path.resolve(targetPath);

  // Load config
  const config = await loadConfig(rootPath);

  if (!args.json && !args.summary) {
    console.log(`Scanning: ${rootPath}`);
    console.log(`Analyzing symbol-level import relationships...\n`);
  }

  // Build index file symbol mappings
  const indexMappings = await buildIndexMappings(rootPath);

  if (!args.json && !args.summary) {
    console.log(`Found ${indexMappings.size} index files with re-exports`);
  }

  // Build import map from test files with symbol tracing
  const importMap = await buildImportMap(rootPath, indexMappings);

  // Find all code files
  const codeFiles = await findCodeFiles(rootPath, rootPath, config);

  // Check test status for each source file
  /** @type {TestResult[]} */
  const results = [];

  for (const sourceFile of codeFiles) {
    const sourcePath = path.join(rootPath, sourceFile);

    let sourceStat;
    try {
      sourceStat = await fs.stat(sourcePath);
    } catch {
      continue;
    }

    const testInfo = importMap.get(sourceFile);

    if (!testInfo || testInfo.testFiles.length === 0) {
      results.push({
        path: sourceFile,
        status: 'untested',
        sourceMtime: sourceStat.mtime,
        testFiles: []
      });
    } else {
      // Check if source is newer than test
      const isStale = testInfo.testMtime && sourceStat.mtime > testInfo.testMtime;

      results.push({
        path: sourceFile,
        status: isStale ? 'stale' : 'covered',
        sourceMtime: sourceStat.mtime,
        testMtime: testInfo.testMtime,
        testFiles: testInfo.testFiles.map(f => path.relative(rootPath, f))
      });
    }
  }

  // Sort by status priority
  const statusOrder = { untested: 0, stale: 1, covered: 2 };
  results.sort((a, b) => {
    const statusDiff = statusOrder[a.status] - statusOrder[b.status];
    if (statusDiff !== 0) return statusDiff;
    return a.path.localeCompare(b.path);
  });

  // Filter based on flags
  let filtered = results;
  if (args.untested) {
    filtered = results.filter(r => r.status === 'untested');
  } else if (args.stale) {
    filtered = results.filter(r => r.status === 'stale');
  }

  // Calculate stats
  const total = results.length;
  const stats = {
    untested: results.filter(r => r.status === 'untested').length,
    stale: results.filter(r => r.status === 'stale').length,
    covered: results.filter(r => r.status === 'covered').length
  };

  const coveragePercent = total > 0
    ? ((stats.covered / total) * 100).toFixed(1)
    : '0.0';

  // Output
  if (args.json) {
    console.log(JSON.stringify({
      total,
      stats,
      coveragePercent: parseFloat(coveragePercent),
      indexFilesAnalyzed: indexMappings.size,
      files: filtered
    }, null, 2));
    return;
  }

  if (args.summary) {
    console.log(`Total Files: ${total}`);
    console.log(`  ⚫ Untested: ${stats.untested}`);
    console.log(`  🟤 Stale: ${stats.stale}`);
    console.log(`  ✅ Covered: ${stats.covered}`);
    console.log(`\nTest Coverage: ${coveragePercent}%`);
    return;
  }

  // Full output
  if (stats.untested > 0 && !args.stale) {
    console.log(`=== ⚫ UNTESTED (${stats.untested}) ===`);
    const toShow = filtered.filter(r => r.status === 'untested').slice(0, 30);
    for (const r of toShow) {
      console.log(`  ○ ${r.path}`);
    }
    if (stats.untested > 30) {
      console.log(`  ... and ${stats.untested - 30} more`);
    }
    console.log('');
  }

  if (stats.stale > 0 && !args.untested) {
    console.log(`=== 🟤 STALE - Source Modified Since Test (${stats.stale}) ===`);
    for (const r of filtered.filter(r => r.status === 'stale')) {
      console.log(`  ◐ ${r.path}`);
      if (args.imports && r.testFiles?.length > 0) {
        for (const tf of r.testFiles.slice(0, 3)) {
          console.log(`      ← ${tf}`);
        }
      }
    }
    console.log('');
  }

  if (!args.untested && !args.stale && stats.covered > 0) {
    console.log(`=== ✅ COVERED (${stats.covered}) ===`);
    const toShow = filtered.filter(r => r.status === 'covered').slice(0, 20);
    for (const r of toShow) {
      console.log(`  ✓ ${r.path}`);
      if (args.imports && r.testFiles?.length > 0) {
        for (const tf of r.testFiles.slice(0, 2)) {
          console.log(`      ← ${tf}`);
        }
      }
    }
    if (stats.covered > 20) {
      console.log(`  ... and ${stats.covered - 20} more`);
    }
    console.log('');
  }

  // Summary line
  console.log('────────────────────────────────────────────────────────────');
  console.log(`Total: ${total} | Untested: ${stats.untested} | Stale: ${stats.stale} | Covered: ${stats.covered} | Coverage: ${coveragePercent}%`);
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
