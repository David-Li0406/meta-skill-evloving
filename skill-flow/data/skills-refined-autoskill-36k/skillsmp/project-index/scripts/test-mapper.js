#!/usr/bin/env node
/**
 * Test Mapper - Generate .test-map.json with source→test mappings
 *
 * Usage:
 *   node test-mapper.js [path]              # Generate/update .test-map.json
 *   node test-mapper.js [path] --dry-run    # Preview without writing
 *   node test-mapper.js [path] --verbose    # Show detailed mappings
 *   node test-mapper.js [path] --module X   # Only update specific module
 *
 * Features:
 *   - Symbol-level import analysis (traces through index.js re-exports)
 *   - Supports unit/integration/e2e test types
 *   - Stale detection (source mtime > test mtime)
 *   - Per-module TEST.md generation
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
 * @typedef {'unit' | 'integration' | 'e2e'} TestType
 * @typedef {'untested' | 'stale' | 'covered'} TestStatus
 */

/**
 * @typedef {object} SourceTestInfo
 * @property {string} source - Source file path
 * @property {TestStatus} status - Test status
 * @property {string[]} tests - Test files covering this source
 * @property {Date} [sourceMtime] - Source modification time
 * @property {Date} [testMtime] - Latest test modification time
 */

/**
 * @typedef {object} ModuleTestInfo
 * @property {string} module - Module path (e.g., js/agents/core)
 * @property {number} total - Total source files
 * @property {number} covered - Covered files count
 * @property {number} stale - Stale files count
 * @property {number} untested - Untested files count
 * @property {string} coverage - Coverage percentage
 * @property {SourceTestInfo[]} files - Per-file test info
 */

/**
 * Parse export statements from index file
 */
function parseExports(content, indexDir, rootPath) {
  const symbolToSource = new Map();

  const namedExportRegex = /export\s*\{([^}]+)\}\s*from\s*['"]([^'"]+)['"]/g;
  let match;

  while ((match = namedExportRegex.exec(content)) !== null) {
    const symbols = match[1];
    const fromPath = match[2];

    let resolvedPath = path.resolve(indexDir, fromPath);
    if (!path.extname(resolvedPath)) resolvedPath += '.js';
    const relativePath = path.relative(rootPath, resolvedPath);

    const symbolList = symbols.split(',').map(s => s.trim());
    for (const sym of symbolList) {
      const asMatch = sym.match(/(\w+)\s+as\s+(\w+)/);
      const symbolName = asMatch ? asMatch[2] : sym.trim();
      if (symbolName) {
        symbolToSource.set(symbolName, relativePath);
      }
    }
  }

  const starExportRegex = /export\s*\*\s*from\s*['"]([^'"]+)['"]/g;
  while ((match = starExportRegex.exec(content)) !== null) {
    const fromPath = match[1];
    let resolvedPath = path.resolve(indexDir, fromPath);
    if (!path.extname(resolvedPath)) resolvedPath += '.js';
    const relativePath = path.relative(rootPath, resolvedPath);
    symbolToSource.set(`__star__${relativePath}`, relativePath);
  }

  return symbolToSource;
}

/**
 * Parse import statements from test file
 */
function parseImports(content) {
  const imports = [];

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
 * Build index file symbol mappings
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
        } else if (entry.isFile() && (entry.name === 'index.js' || entry.name === 'index.mjs')) {
          try {
            const content = await fs.readFile(fullPath, 'utf-8');
            const symbolMap = parseExports(content, path.dirname(fullPath), rootPath);
            if (symbolMap.size > 0) {
              const relativePath = path.relative(rootPath, fullPath);
              indexMappings.set(relativePath, symbolMap);
            }
          } catch { /* skip */ }
        }
      }
    } catch { /* skip */ }
  }

  await scan(rootPath);
  return indexMappings;
}

/**
 * Classify test file type
 * @param {string} filename
 * @returns {TestType}
 */
function classifyTestType(filename) {
  if (filename.includes('.e2e.') || filename.includes('/e2e/')) return 'e2e';
  if (filename.includes('.int.') || filename.includes('/integration/')) return 'integration';
  return 'unit';
}

/**
 * Find all test files
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
          if (entry.name.includes('.test.') || entry.name.includes('.spec.')) {
            results.push(fullPath);
          }
        }
      }
    } catch { /* skip */ }
  }

  await scan(testsDir);
  return results;
}

/**
 * Build source→test mapping with test type classification
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
      const testType = classifyTestType(testFile);
      const relativeTestFile = path.relative(rootPath, testFile);

      for (const { symbols, fromPath } of imports) {
        const resolvedPath = resolveImport(fromPath, testFile);
        const relativePath = path.relative(rootPath, resolvedPath);

        const symbolMap = indexMappings.get(relativePath);

        if (symbolMap && symbols.length > 0) {
          for (const symbol of symbols) {
            const sourceFile = symbolMap.get(symbol);
            if (sourceFile) {
              addMapping(sourceToTests, sourceFile, relativeTestFile, testStat.mtime, testType);
            }
          }
          addMapping(sourceToTests, relativePath, relativeTestFile, testStat.mtime, testType);
        } else {
          addMapping(sourceToTests, relativePath, relativeTestFile, testStat.mtime, testType);
        }
      }
    } catch { /* skip */ }
  }

  return sourceToTests;
}

function resolveImport(importPath, fromFile) {
  const dir = path.dirname(fromFile);
  let resolved = path.resolve(dir, importPath);
  if (!path.extname(resolved)) resolved += '.js';
  return resolved;
}

function addMapping(map, sourceFile, testFile, testMtime, testType) {
  if (!map.has(sourceFile)) {
    map.set(sourceFile, { unit: [], integration: [], e2e: [], testMtime: null });
  }
  const entry = map.get(sourceFile);
  if (!entry[testType].includes(testFile)) {
    entry[testType].push(testFile);
  }
  if (!entry.testMtime || testMtime > entry.testMtime) {
    entry.testMtime = testMtime;
  }
}

/**
 * Find all code files
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
          if (entry.name.includes('.test.') || entry.name.includes('.spec.')) continue;
          if (!shouldProcess(relativePath, config)) continue;
          results.push(relativePath);
        }
      }
    } catch { /* skip */ }
  }

  await scan(dir);
  return results;
}

/**
 * Detect module from file path
 * @param {string} filePath
 * @returns {string} Module path (e.g., js/agents/core)
 */
function detectModule(filePath) {
  const parts = filePath.split(path.sep);
  // Find module boundary (2-3 levels deep typically)
  if (parts[0] === 'js' && parts[1] === 'agents') {
    return parts.slice(0, 3).join('/');
  }
  if (parts[0] === 'js') {
    return parts.slice(0, 2).join('/');
  }
  return parts[0];
}

/**
 * Generate TEST.md content for a module
 */
function generateTestMd(moduleInfo) {
  const lines = [
    `# ${moduleInfo.module.split('/').pop()} 测试状态`,
    '',
    `> 自动生成于 ${new Date().toISOString().split('T')[0]}`,
    '',
    '## 概览',
    '',
    `| 指标 | 值 |`,
    `|------|-----|`,
    `| 总文件数 | ${moduleInfo.total} |`,
    `| 已覆盖 | ${moduleInfo.covered} |`,
    `| 过期 | ${moduleInfo.stale} |`,
    `| 未测试 | ${moduleInfo.untested} |`,
    `| 覆盖率 | ${moduleInfo.coverage} |`,
    ''
  ];

  // Group by status
  const untested = moduleInfo.files.filter(f => f.status === 'untested');
  const stale = moduleInfo.files.filter(f => f.status === 'stale');
  const covered = moduleInfo.files.filter(f => f.status === 'covered');

  if (untested.length > 0) {
    lines.push('## ⚫ 未测试', '');
    lines.push('| 文件 | 备注 |');
    lines.push('|------|------|');
    for (const f of untested.slice(0, 30)) {
      const basename = path.basename(f.source);
      lines.push(`| \`${basename}\` | - |`);
    }
    if (untested.length > 30) {
      lines.push(`| ... | +${untested.length - 30} 更多 |`);
    }
    lines.push('');
  }

  if (stale.length > 0) {
    lines.push('## 🟤 过期 (源码已修改)', '');
    lines.push('| 文件 | 测试文件 |');
    lines.push('|------|----------|');
    for (const f of stale) {
      const basename = path.basename(f.source);
      const testNames = f.tests.slice(0, 2).map(t => path.basename(t)).join(', ');
      lines.push(`| \`${basename}\` | ${testNames} |`);
    }
    lines.push('');
  }

  if (covered.length > 0) {
    lines.push('## ✅ 已覆盖', '');
    lines.push('| 文件 | 测试文件 |');
    lines.push('|------|----------|');
    for (const f of covered.slice(0, 20)) {
      const basename = path.basename(f.source);
      const testNames = f.tests.slice(0, 2).map(t => path.basename(t)).join(', ');
      lines.push(`| \`${basename}\` | ${testNames} |`);
    }
    if (covered.length > 20) {
      lines.push(`| ... | +${covered.length - 20} 更多 |`);
    }
    lines.push('');
  }

  return lines.join('\n');
}

/**
 * Main function
 */
async function main() {
  const args = parseArgs(process.argv.slice(2), {
    'dry-run': false,
    verbose: false,
    module: null,
    'generate-md': false
  });

  const targetPath = args._?.[0] || process.cwd();
  const rootPath = path.resolve(targetPath);
  const config = await loadConfig(rootPath);

  console.log(`Scanning: ${rootPath}`);
  console.log(`Building symbol-level import mappings...\n`);

  // Build mappings
  const indexMappings = await buildIndexMappings(rootPath);
  console.log(`Found ${indexMappings.size} index files with re-exports`);

  const importMap = await buildImportMap(rootPath, indexMappings);
  const codeFiles = await findCodeFiles(rootPath, rootPath, config);

  // Group by module
  const moduleMap = new Map();

  for (const sourceFile of codeFiles) {
    const modulePath = detectModule(sourceFile);
    if (!moduleMap.has(modulePath)) {
      moduleMap.set(modulePath, []);
    }
    moduleMap.get(modulePath).push(sourceFile);
  }

  // Build module test info
  /** @type {Map<string, ModuleTestInfo>} */
  const moduleTestInfo = new Map();

  for (const [modulePath, files] of moduleMap) {
    if (args.module && modulePath !== args.module) continue;

    /** @type {SourceTestInfo[]} */
    const fileInfos = [];

    for (const sourceFile of files) {
      const sourcePath = path.join(rootPath, sourceFile);
      let sourceStat;
      try {
        sourceStat = await fs.stat(sourcePath);
      } catch {
        continue;
      }

      const testInfo = importMap.get(sourceFile);
      const allTests = testInfo
        ? [...testInfo.unit, ...testInfo.integration, ...testInfo.e2e]
        : [];

      let status = 'untested';
      if (allTests.length > 0) {
        const isStale = testInfo.testMtime && sourceStat.mtime > testInfo.testMtime;
        status = isStale ? 'stale' : 'covered';
      }

      fileInfos.push({
        source: sourceFile,
        status,
        tests: allTests,
        sourceMtime: sourceStat.mtime,
        testMtime: testInfo?.testMtime
      });
    }

    const covered = fileInfos.filter(f => f.status === 'covered').length;
    const stale = fileInfos.filter(f => f.status === 'stale').length;
    const untested = fileInfos.filter(f => f.status === 'untested').length;
    const total = fileInfos.length;
    const coverage = total > 0 ? `${((covered / total) * 100).toFixed(1)}%` : '0.0%';

    moduleTestInfo.set(modulePath, {
      module: modulePath,
      total,
      covered,
      stale,
      untested,
      coverage,
      files: fileInfos
    });
  }

  // Build output
  const testMapPath = path.join(rootPath, '.test-map.json');
  let existingMap = { version: 1, conventions: {}, modules: {} };

  try {
    const content = await fs.readFile(testMapPath, 'utf-8');
    existingMap = JSON.parse(content);
  } catch { /* use default */ }

  // Update modules section
  const modulesOutput = {};
  let totalFiles = 0;
  let totalCovered = 0;
  let totalStale = 0;
  let totalUntested = 0;

  for (const [modulePath, info] of moduleTestInfo) {
    totalFiles += info.total;
    totalCovered += info.covered;
    totalStale += info.stale;
    totalUntested += info.untested;

    modulesOutput[modulePath] = {
      total: info.total,
      covered: info.covered,
      stale: info.stale,
      untested: info.untested,
      coverage: info.coverage,
      files: info.files.reduce((acc, f) => {
        const basename = path.basename(f.source);
        acc[basename] = {
          path: f.source,
          status: f.status,
          tests: f.tests
        };
        return acc;
      }, {})
    };
  }

  const overallCoverage = totalFiles > 0
    ? `${((totalCovered / totalFiles) * 100).toFixed(1)}%`
    : '0.0%';

  const outputMap = {
    ...existingMap,
    generated: new Date().toISOString(),
    coverage: {
      ...existingMap.coverage,
      current: parseFloat(overallCoverage)
    },
    summary: {
      total: totalFiles,
      covered: totalCovered,
      stale: totalStale,
      untested: totalUntested,
      coverage: overallCoverage
    },
    modules: modulesOutput
  };

  // Output
  if (args['dry-run']) {
    console.log('\n=== DRY RUN ===\n');
    console.log(`Total modules: ${moduleTestInfo.size}`);
    console.log(`Total files: ${totalFiles}`);
    console.log(`Covered: ${totalCovered} | Stale: ${totalStale} | Untested: ${totalUntested}`);
    console.log(`Overall coverage: ${overallCoverage}`);

    if (args.verbose) {
      console.log('\n=== Module Details ===\n');
      for (const [mod, info] of moduleTestInfo) {
        console.log(`${mod}: ${info.coverage} (${info.covered}/${info.total})`);
      }
    }
  } else {
    await fs.writeFile(testMapPath, JSON.stringify(outputMap, null, 2) + '\n');
    console.log(`\nWritten: ${testMapPath}`);

    // Generate TEST.md files if requested
    if (args['generate-md']) {
      for (const [modulePath, info] of moduleTestInfo) {
        const mdPath = path.join(rootPath, modulePath, 'TEST.md');
        const mdContent = generateTestMd(info);
        try {
          await fs.writeFile(mdPath, mdContent);
          console.log(`  Written: ${mdPath}`);
        } catch (err) {
          console.log(`  Skip: ${mdPath} (${err.message})`);
        }
      }
    }

    console.log(`\n=== Summary ===`);
    console.log(`Total: ${totalFiles} | Covered: ${totalCovered} | Stale: ${totalStale} | Untested: ${totalUntested}`);
    console.log(`Coverage: ${overallCoverage}`);
  }
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
