#!/usr/bin/env node
/**
 * Check Stale - Detect outdated documentation and tests
 * Usage: node check-stale.js [path] [--json] [--stale-only] [--type=doc|claude|audit|test|all]
 *
 * Types:
 *   doc/claude - Check CLAUDE.md freshness
 *   audit      - Check AUDIT.md freshness
 *   test       - Check test coverage freshness (from .test-map.json)
 *   all        - Check all types
 *
 * Compares doc/test mtime with source code mtime.
 * If code is newer than docs/tests, marks as stale.
 *
 * Supports .stale-config.json with include/ignore patterns
 */

import { promises as fs } from 'fs';
import path from 'path';
import { shouldProcess } from './shared.js';

const IGNORE_DIRS = new Set([
  'node_modules', '.git', 'dist', 'build', '.next', '__pycache__',
  'venv', '.venv', 'target', 'vendor', '.cache', 'coverage',
  '.turbo', '.nuxt', '.output', 'out'
]);

const CODE_EXTENSIONS = new Set([
  '.js', '.ts', '.jsx', '.tsx', '.mjs', '.cjs',
  '.py', '.go', '.rs', '.java', '.kt', '.rb', '.php',
  '.c', '.cpp', '.h', '.hpp', '.cs', '.swift', '.vue', '.svelte'
]);

const DOC_FILENAMES = new Set(['CLAUDE.md', 'AUDIT.md']);

const DOC_TYPES = {
  claude: 'CLAUDE.md',
  audit: 'AUDIT.md',
  test: '.test-map.json'  // Special: uses test-map data
};

/**
 * Load .test-map.json for test coverage tracking
 */
async function loadTestMap(rootPath) {
  const mapPath = path.join(rootPath, '.test-map.json');
  try {
    const content = await fs.readFile(mapPath, 'utf-8');
    return JSON.parse(content);
  } catch {
    return null;
  }
}

/**
 * Convert test-map data to stale results format
 */
function testMapToResults(testMap, config) {
  if (!testMap?.modules) return [];

  const results = [];

  for (const [modulePath, data] of Object.entries(testMap.modules)) {
    if (!shouldProcess(modulePath, config)) continue;

    const staleFiles = Object.entries(data.files || {})
      .filter(([, f]) => f.status === 'stale')
      .map(([name, f]) => ({ path: f.path, mtime: null }));

    const untestedFiles = Object.entries(data.files || {})
      .filter(([, f]) => f.status === 'untested')
      .map(([name, f]) => ({ path: f.path, mtime: null }));

    // Module is stale if has stale tests or low coverage
    const isStale = data.stale > 0;
    const isMissing = data.untested > 0 && data.covered === 0;

    results.push({
      path: modulePath,
      status: isMissing ? 'missing' : (isStale ? 'stale' : 'fresh'),
      coverage: data.coverage,
      stats: { covered: data.covered, stale: data.stale, untested: data.untested, total: data.total },
      changedFiles: staleFiles,
      untestedFiles
    });
  }

  // Sort: missing first, then stale, then fresh
  results.sort((a, b) => {
    const order = { missing: 0, stale: 1, fresh: 2 };
    return order[a.status] - order[b.status];
  });

  return results;
}

/**
 * Load .stale-config.json from project root
 * @param {string} rootPath
 * @returns {Promise<{ignore: string[], extensions: string[]}>}
 */
async function loadConfig(rootPath) {
  // Try .project-index/.stale-config.json first, then fallback to .stale-config.json
  const configPaths = [
    path.join(rootPath, '.project-index', '.stale-config.json'),
    path.join(rootPath, '.stale-config.json')
  ];

  for (const configFile of configPaths) {
    try {
      const content = await fs.readFile(configFile, 'utf-8');
      const config = JSON.parse(content);
      return {
        include: config.include || [],
        ignore: config.ignore || [],
        extensions: config.extensions || null  // null means use default
      };
    } catch {
      // Try next path
    }
  }
  return { include: [], ignore: [], extensions: null };
}

/**
 * Check if a path matches any ignore pattern
 * @param {string} relativePath
 * @param {string[]} patterns
 * @returns {boolean}
 */
function shouldIgnore(relativePath, patterns) {
  for (const pattern of patterns) {
    // Simple glob matching: * matches anything, ** matches any path
    const regex = pattern
      .replace(/\./g, '\\.')
      .replace(/\*\*/g, '.*')
      .replace(/\*/g, '[^/]*');
    if (new RegExp(`^${regex}(/|$)`).test(relativePath)) {
      return true;
    }
  }
  return false;
}

/**
 * @typedef {'fresh' | 'stale' | 'missing'} StaleStatus
 * @typedef {{path: string, mtime: Date}} FileInfo
 * @typedef {{
 *   path: string,
 *   status: StaleStatus,
 *   docMtime?: Date,
 *   codeMtime?: Date,
 *   newestFile?: string,
 *   changedFiles?: FileInfo[]
 * }} CheckResult
 */

/**
 * Recursively find all doc files
 * @param {string} dir
 * @param {string} rootPath
 * @param {string} docName
 * @returns {Promise<string[]>}
 */
async function findDocFiles(dir, rootPath, docName) {
  const results = [];

  try {
    const entries = await fs.readdir(dir, { withFileTypes: true });

    for (const entry of entries) {
      if (entry.name === docName && entry.isFile()) {
        results.push(dir);
      }

      if (entry.isDirectory() && !IGNORE_DIRS.has(entry.name)) {
        const subResults = await findDocFiles(
          path.join(dir, entry.name),
          rootPath,
          docName
        );
        results.push(...subResults);
      }
    }
  } catch (e) {
    // Permission denied or other errors, skip
  }

  return results;
}

/**
 * Get max mtime of code files in directory (recursive)
 * @param {string} dir
 * @param {Date|null} docMtime - If provided, also collect files newer than this
 * @param {string} rootPath - Project root for relative path calculation
 * @param {string[]} ignorePatterns - Patterns to ignore
 * @param {string} docName - Doc filename (CLAUDE.md or AUDIT.md)
 * @returns {Promise<{mtime: Date | null, file: string | null, changedFiles: FileInfo[]}>}
 */
async function getMaxCodeMtime(
  dir,
  docMtime = null,
  rootPath = dir,
  ignorePatterns = [],
  docName = 'CLAUDE.md'
) {
  let maxMtime = null;
  let maxFile = null;
  /** @type {FileInfo[]} */
  const changedFiles = [];

  try {
    const entries = await fs.readdir(dir, { withFileTypes: true });

    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name);
      const relativePath = path.relative(rootPath, fullPath);

      // Check ignore patterns
      if (shouldIgnore(relativePath, ignorePatterns)) continue;

      if (entry.isFile()) {
        const ext = path.extname(entry.name).toLowerCase();

        // Skip doc files and non-code files
        if (DOC_FILENAMES.has(entry.name)) continue;
        if (!CODE_EXTENSIONS.has(ext)) continue;

        const stat = await fs.stat(fullPath);
        if (!maxMtime || stat.mtime > maxMtime) {
          maxMtime = stat.mtime;
          maxFile = fullPath;
        }
        // Collect files newer than doc
        if (docMtime && stat.mtime > docMtime) {
          changedFiles.push({ path: fullPath, mtime: stat.mtime });
        }
      } else if (entry.isDirectory() && !IGNORE_DIRS.has(entry.name)) {
        // Check if subdir has its own doc file (separate tracking)
        const subDocPath = path.join(fullPath, docName);
        let hasOwnDoc = false;
        try {
          await fs.access(subDocPath);
          hasOwnDoc = true;
        } catch {}

        // If subdir has own doc, skip it (tracked separately)
        if (hasOwnDoc) continue;

        const sub = await getMaxCodeMtime(fullPath, docMtime, rootPath, ignorePatterns, docName);
        if (sub.mtime && (!maxMtime || sub.mtime > maxMtime)) {
          maxMtime = sub.mtime;
          maxFile = sub.file;
        }
        changedFiles.push(...sub.changedFiles);
      }
    }
  } catch (e) {
    // Permission denied or other errors
  }

  return { mtime: maxMtime, file: maxFile, changedFiles };
}

/**
 * Check staleness of a single doc file
 * @param {string} dirPath - Directory containing doc file
 * @param {string} rootPath
 * @param {string[]} ignorePatterns
 * @param {string} docName
 * @returns {Promise<CheckResult>}
 */
async function checkStaleness(dirPath, rootPath, ignorePatterns = [], docName = 'CLAUDE.md') {
  const docPath = path.join(dirPath, docName);
  const relativePath = path.relative(rootPath, dirPath) || '.';

  try {
    const docStat = await fs.stat(docPath);
    const { mtime: codeMtime, file: newestFile, changedFiles } = await getMaxCodeMtime(
      dirPath,
      docStat.mtime,
      rootPath,
      ignorePatterns,
      docName
    );

    if (!codeMtime) {
      // No code files found, doc is fresh by default
      return {
        path: relativePath,
        status: 'fresh',
        docMtime: docStat.mtime,
        codeMtime: null,
        newestFile: null,
        changedFiles: []
      };
    }

    const isStale = codeMtime > docStat.mtime;

    // Sort changed files by mtime desc
    changedFiles.sort((a, b) => b.mtime.getTime() - a.mtime.getTime());

    return {
      path: relativePath,
      status: isStale ? 'stale' : 'fresh',
      docMtime: docStat.mtime,
      codeMtime,
      newestFile: newestFile ? path.relative(rootPath, newestFile) : null,
      changedFiles: changedFiles.map(f => ({
        path: path.relative(rootPath, f.path),
        mtime: f.mtime
      }))
    };
  } catch (e) {
    return {
      path: relativePath,
      status: 'missing',
      docMtime: null,
      codeMtime: null,
      newestFile: null,
      changedFiles: []
    };
  }
}

function formatDate(date) {
  if (!date) return 'N/A';
  return date.toISOString().split('T')[0];
}

function colorize(status) {
  const colors = {
    stale: '\x1b[33m',   // yellow
    fresh: '\x1b[32m',   // green
    missing: '\x1b[31m', // red
    reset: '\x1b[0m'
  };
  return `${colors[status] || ''}${status.padEnd(7)}${colors.reset}`;
}

function normalizeType(typeArg) {
  if (!typeArg) return 'claude';
  const normalized = typeArg.trim().toLowerCase();
  if (normalized === 'doc' || normalized === 'claude') return 'claude';
  if (normalized === 'audit') return 'audit';
  if (normalized === 'test') return 'test';
  if (normalized === 'all') return 'all';
  return null;
}

function parseTypeArg(args) {
  const flag = '--type';
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg.startsWith(`${flag}=`)) {
      return { value: arg.slice(flag.length + 1), consumedIndex: null };
    }
    if (arg === flag) {
      const value = args[i + 1];
      if (value && !value.startsWith('--')) {
        return { value, consumedIndex: i + 1 };
      }
      return { value: null, consumedIndex: null };
    }
  }
  return { value: null, consumedIndex: null };
}

async function collectResults(docName, rootPath, config, ignorePatterns) {
  const docDirs = await findDocFiles(rootPath, rootPath, docName);
  const results = [];

  for (const dir of docDirs) {
    const relativePath = path.relative(rootPath, dir) || '.';

    if (!shouldProcess(relativePath, config)) continue;

    const result = await checkStaleness(dir, rootPath, ignorePatterns, docName);
    results.push(result);
  }

  results.sort((a, b) => {
    const order = { stale: 0, missing: 1, fresh: 2 };
    return order[a.status] - order[b.status];
  });

  return results;
}

function displayResults(results, docName, rootPath, staleOnly) {
  console.log(`Checking ${docName} freshness in: ${rootPath}\n`);

  const staleCount = results.filter(r => r.status === 'stale').length;
  const freshCount = results.filter(r => r.status === 'fresh').length;

  for (const r of results) {
    if (staleOnly && r.status !== 'stale') continue;

    const pathDisplay = r.path.padEnd(40);

    if (r.status === 'stale') {
      console.log(`${colorize('stale')} ${pathDisplay} (code: ${formatDate(r.codeMtime)}, doc: ${formatDate(r.docMtime)})`);
      if (r.changedFiles && r.changedFiles.length > 0) {
        const maxShow = 5;
        const files = r.changedFiles.slice(0, maxShow);
        for (const f of files) {
          console.log(`        ├─ ${f.path} (${formatDate(f.mtime)})`);
        }
        if (r.changedFiles.length > maxShow) {
          console.log(`        └─ ... and ${r.changedFiles.length - maxShow} more files`);
        }
      }
    } else if (r.status === 'fresh') {
      console.log(`${colorize('fresh')} ${pathDisplay} (doc: ${formatDate(r.docMtime)})`);
    } else {
      console.log(`${colorize('missing')} ${pathDisplay}`);
    }
  }

  console.log(`\n${'─'.repeat(60)}`);
  console.log(`Total: ${results.length} | Stale: ${staleCount} | Fresh: ${freshCount}`);

  if (staleCount > 0) {
    if (docName === DOC_TYPES.claude) {
      console.log(`\nRun 'node generate.js --module <path>' to update stale docs.`);
    } else if (docName === DOC_TYPES.audit) {
      console.log(`\nRun 'node scripts/code-audit.js <path>' to update stale audits.`);
    }
  }
}

/**
 * Display test coverage results
 */
function displayTestResults(results, rootPath, staleOnly) {
  console.log(`Checking test coverage in: ${rootPath}\n`);

  const staleCount = results.filter(r => r.status === 'stale').length;
  const missingCount = results.filter(r => r.status === 'missing').length;
  const freshCount = results.filter(r => r.status === 'fresh').length;

  for (const r of results) {
    if (staleOnly && r.status !== 'stale' && r.status !== 'missing') continue;

    const pathDisplay = r.path.replace('js/agents/', '').padEnd(35);
    const stats = r.stats || {};

    if (r.status === 'missing') {
      console.log(`${colorize('missing')} ${pathDisplay} ${r.coverage} (untested: ${stats.untested})`);
    } else if (r.status === 'stale') {
      console.log(`${colorize('stale')} ${pathDisplay} ${r.coverage} (stale: ${stats.stale}, untested: ${stats.untested})`);
      if (r.changedFiles && r.changedFiles.length > 0) {
        const maxShow = 3;
        const files = r.changedFiles.slice(0, maxShow);
        for (const f of files) {
          console.log(`        ├─ ${path.basename(f.path)}`);
        }
        if (r.changedFiles.length > maxShow) {
          console.log(`        └─ ... +${r.changedFiles.length - maxShow} more stale`);
        }
      }
    } else {
      console.log(`${colorize('fresh')} ${pathDisplay} ${r.coverage} (covered: ${stats.covered}/${stats.total})`);
    }
  }

  // Summary
  const totalStale = results.reduce((sum, r) => sum + (r.stats?.stale || 0), 0);
  const totalUntested = results.reduce((sum, r) => sum + (r.stats?.untested || 0), 0);
  const totalCovered = results.reduce((sum, r) => sum + (r.stats?.covered || 0), 0);
  const totalFiles = results.reduce((sum, r) => sum + (r.stats?.total || 0), 0);

  console.log(`\n${'─'.repeat(60)}`);
  console.log(`Modules: ${results.length} | Stale: ${staleCount} | Missing: ${missingCount} | Fresh: ${freshCount}`);
  console.log(`Files: ${totalFiles} | Covered: ${totalCovered} | Stale: ${totalStale} | Untested: ${totalUntested}`);

  if (staleCount > 0 || missingCount > 0) {
    console.log(`\nRun 'node scripts/test-mapper.js --refresh' to update test map.`);
  }
}

async function main() {
  const args = process.argv.slice(2);
  const jsonMode = args.includes('--json');
  const staleOnly = args.includes('--stale-only');
  const touchMode = args.includes('--touch');
  const touchAll = args.includes('--touch-all');
  const { value: typeArg, consumedIndex } = parseTypeArg(args);
  const normalizedType = normalizeType(typeArg);
  const consumedIndexes = new Set();
  if (consumedIndex !== null) consumedIndexes.add(consumedIndex);

  if (!normalizedType) {
    console.error(`Invalid --type value: ${typeArg}. Expected doc|claude|audit|all.`);
    process.exit(1);
  }

  const typesToCheck = normalizedType === 'all' ? ['claude', 'audit', 'test'] : [normalizedType];

  // For touch mode, paths come after --touch flag
  const touchIndex = args.indexOf('--touch');
  const pathsToTouch = touchMode && touchIndex !== -1
    ? args
      .slice(touchIndex + 1)
      .filter((a, index) => {
        const absoluteIndex = touchIndex + 1 + index;
        return !a.startsWith('--') && !consumedIndexes.has(absoluteIndex);
      })
    : [];

  const targetPath = (!touchMode && !touchAll)
    ? (args.find((a, index) => !a.startsWith('--') && !consumedIndexes.has(index)) || process.cwd())
    : process.cwd();
  const rootPath = path.resolve(targetPath);

  // Load config
  const config = await loadConfig(rootPath);
  const ignorePatterns = config.ignore || [];

  if (!jsonMode && ignorePatterns.length > 0) {
    console.log(`Ignore patterns: ${ignorePatterns.join(', ')}`);
  }
  if (!jsonMode && config.include?.length > 0) {
    console.log(`Include patterns: ${config.include.join(', ')}`);
  }
  if (!jsonMode && (ignorePatterns.length > 0 || config.include?.length > 0)) {
    console.log('');
  }

  // Touch mode: update mtime of specified doc files
  if (touchMode || touchAll) {
    let touched = 0;

    for (const type of typesToCheck) {
      const docName = DOC_TYPES[type];
      const docDirs = await findDocFiles(rootPath, rootPath, docName);

      for (const dir of docDirs) {
        const result = await checkStaleness(dir, rootPath, ignorePatterns, docName);
        if (result.status !== 'stale') continue;

        // --touch-all touches all stale, --touch requires path match
        const shouldTouch = touchAll || pathsToTouch.some(p =>
          result.path === p || result.path.startsWith(p + '/') || result.path.startsWith(p)
        );

        if (shouldTouch) {
          const docPath = path.join(dir, docName);
          const now = new Date();
          await fs.utimes(docPath, now, now);
          console.log(`touched: ${result.path}/${docName}`);
          touched++;
        }
      }
    }

    console.log(`\n${touched} file(s) touched.`);
    return;
  }

  const resultsByType = {};

  for (const type of typesToCheck) {
    if (type === 'test') {
      // Test type uses .test-map.json data
      const testMap = await loadTestMap(rootPath);
      if (testMap) {
        resultsByType[type] = testMapToResults(testMap, config);
      } else {
        console.log('Warning: .test-map.json not found. Run test-mapper.js first.\n');
        resultsByType[type] = [];
      }
    } else {
      const docName = DOC_TYPES[type];
      resultsByType[type] = await collectResults(docName, rootPath, config, ignorePatterns);
    }
  }

  if (jsonMode) {
    if (typesToCheck.length === 1) {
      console.log(JSON.stringify(resultsByType[typesToCheck[0]], null, 2));
    } else {
      console.log(JSON.stringify({
        claude: resultsByType.claude || [],
        audit: resultsByType.audit || [],
        test: resultsByType.test || []
      }, null, 2));
    }
    return;
  }

  if (typesToCheck.length === 1) {
    const type = typesToCheck[0];
    if (type === 'test') {
      displayTestResults(resultsByType[type], rootPath, staleOnly);
    } else {
      displayResults(resultsByType[type], DOC_TYPES[type], rootPath, staleOnly);
    }
    return;
  }

  const sections = [
    { type: 'claude', title: DOC_TYPES.claude },
    { type: 'audit', title: DOC_TYPES.audit },
    { type: 'test', title: 'Test Coverage' }
  ];

  sections.forEach((section, index) => {
    if (!resultsByType[section.type]) return;
    if (index > 0) console.log('');
    console.log(`=== ${section.title} ===`);
    if (section.type === 'test') {
      displayTestResults(resultsByType[section.type] || [], rootPath, staleOnly);
    } else {
      displayResults(resultsByType[section.type] || [], DOC_TYPES[section.type], rootPath, staleOnly);
    }
  });
}

main().catch(console.error);
