#!/usr/bin/env node
/**
 * Audit Status - Check AUDIT.md coverage and freshness
 *
 * Usage:
 *   node audit-status.js [path]              # Full status report
 *   node audit-status.js [path] --json       # JSON output
 *   node audit-status.js [path] --never      # Only show never-audited
 *   node audit-status.js [path] --stale      # Only show stale audits
 *   node audit-status.js [path] --summary    # Summary only
 *
 * Status types:
 *   - never: No AUDIT.md exists
 *   - stale: AUDIT.md exists but code has been modified since
 *   - fresh: AUDIT.md is up-to-date with code
 *   - clean: AUDIT.md exists with 0 issues (all resolved)
 */

import { promises as fs } from 'fs';
import path from 'path';
import { loadConfig, parseArgs, readJsonSafe, shouldProcess, writeJsonSafe, findProjectRoot } from './shared.js';

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

// Threshold for "large" directories that need their own CLAUDE.md
const LARGE_THRESHOLD = { files: 5, lines: 200 };

/**
 * Update audit history snapshots for trend tracking
 * @param {string} scanPath - Path being scanned (may be subdir)
 * @param {number} totalIssues
 * @param {AuditResult[]} results
 * @returns {Promise<{resolved: number, previous: number, new: number}>}
 */
async function updateAuditHistory(scanPath, totalIssues, results) {
  // Always store history in project root, not in scanned subdir
  const projectRoot = await findProjectRoot(scanPath);
  const stateDir = path.join(projectRoot, '.project-index');
  const historyPath = path.join(stateDir, '.audit-history.json');
  await fs.mkdir(stateDir, { recursive: true });

  const history = await readJsonSafe(historyPath, { snapshots: [] });
  const snapshots = Array.isArray(history.snapshots) ? history.snapshots : [];
  const lastSnapshot = snapshots[snapshots.length - 1];
  const date = new Date().toISOString().split('T')[0];

  const moduleIssues = {};
  for (const item of results) {
    if (!item?.path) continue;
    moduleIssues[item.path] = Number(item.issueCount || 0);
  }

  let resolved = 0;
  let created = 0;
  if (lastSnapshot && lastSnapshot.modules && typeof lastSnapshot.modules === 'object') {
    const previousModules = lastSnapshot.modules || {};
    const keys = new Set([...Object.keys(previousModules), ...Object.keys(moduleIssues)]);
    for (const key of keys) {
      const prev = Number(previousModules[key] || 0);
      const curr = Number(moduleIssues[key] || 0);
      if (curr > prev) created += curr - prev;
      if (curr < prev) resolved += prev - curr;
    }
  } else if (lastSnapshot && Number.isFinite(Number(lastSnapshot.total))) {
    const diff = Number(totalIssues || 0) - Number(lastSnapshot.total || 0);
    if (diff > 0) created = diff;
    if (diff < 0) resolved = Math.abs(diff);
  } else {
    created = Number(totalIssues || 0);
  }

  const snapshot = {
    date,
    total: Number(totalIssues || 0),
    resolved,
    new: created,
    modules: moduleIssues
  };

  const shouldAppend = !lastSnapshot || lastSnapshot.date !== date || lastSnapshot.total !== snapshot.total;
  if (shouldAppend) {
    snapshots.push(snapshot);
    history.snapshots = snapshots;
    await writeJsonSafe(historyPath, history);
  }

  const latest = shouldAppend ? snapshot : lastSnapshot;
  if (!latest) {
    return { resolved: 0, previous: 0, new: 0, totalResolved: 0 };
  }

  // Calculate cumulative resolved count
  const totalResolved = snapshots.reduce((sum, s) => sum + Number(s.resolved || 0), 0);

  return {
    resolved: Number(latest.resolved || 0),
    previous: Math.max(0, Number(latest.total || 0) - Number(latest.new || 0)),
    new: Number(latest.new || 0),
    totalResolved
  };
}

/**
 * Check if a path matches any ignore pattern
 * @param {string} relativePath
 * @param {string[]} patterns
 * @returns {boolean}
 */
function shouldIgnore(relativePath, patterns) {
  for (const pattern of patterns) {
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
 * Get the newest code file mtime in a directory (non-recursive, only this module)
 * @param {string} dir - Directory to scan
 * @returns {Promise<{mtime: Date | null, file: string | null, fileCount: number}>}
 */
async function getNewestCodeMtime(dir) {
  let newestMtime = null;
  let newestFile = null;
  let fileCount = 0;

  try {
    const entries = await fs.readdir(dir, { withFileTypes: true });

    for (const entry of entries) {
      if (!entry.isFile()) continue;

      const ext = path.extname(entry.name).toLowerCase();
      if (!CODE_EXTENSIONS.has(ext)) continue;

      // Skip test files
      if (entry.name.includes('.test.') || entry.name.includes('.spec.')) continue;

      fileCount++;

      const filePath = path.join(dir, entry.name);
      try {
        const stat = await fs.stat(filePath);
        if (!newestMtime || stat.mtime > newestMtime) {
          newestMtime = stat.mtime;
          newestFile = entry.name;
        }
      } catch {
        // Skip inaccessible files
      }
    }
  } catch {
    // Skip inaccessible dirs
  }

  return { mtime: newestMtime, file: newestFile, fileCount };
}

/**
 * Check if path matches any include pattern (or is a parent of patterns)
 * @param {string} relativePath
 * @param {string[]} patterns
 * @returns {{canEnter: boolean, shouldCount: boolean}} canEnter: can traverse into, shouldCount: should count files
 */
function matchesInclude(relativePath, patterns) {
  if (!patterns || patterns.length === 0) return { canEnter: true, shouldCount: true };

  let canEnter = false;
  let shouldCount = false;

  for (const pattern of patterns) {
    // Convert glob to regex
    const regex = pattern
      .replace(/\./g, '\\.')
      .replace(/\*\*/g, '.*')
      .replace(/\*/g, '[^/]*');

    // Check if path matches pattern (should count files)
    if (new RegExp(`^${regex}(/|$)`).test(relativePath)) {
      shouldCount = true;
      canEnter = true;
      break;
    }

    // Check if path is a parent of pattern (can enter but don't count)
    if (pattern.startsWith(relativePath + '/')) {
      canEnter = true;
    }
  }

  return { canEnter, shouldCount };
}

/**
 * Recursively count all code files in a directory tree
 * @param {string} dir - Directory to scan
 * @param {string} rootPath - Project root
 * @param {object} config - Config with include/ignore patterns
 * @returns {Promise<{total: number, totalDirs: number, byDir: Object<string, {discovered: number, audited: number}>}>}
 */
async function countAllCodeFiles(dir, rootPath, config) {
  let total = 0;
  let totalDirs = 0;
  const byDir = {};
  const ignorePatterns = config.ignore || [];
  const includePatterns = config.include || [];

  async function scan(currentDir) {
    const relativePath = path.relative(rootPath, currentDir);

    // Apply ignore patterns
    if (relativePath && shouldIgnore(relativePath, ignorePatterns)) {
      return;
    }

    // Apply include patterns - check if we can enter and if we should count files
    let shouldCount = true;
    if (relativePath && includePatterns.length > 0) {
      const match = matchesInclude(relativePath, includePatterns);
      if (!match.canEnter) {
        return;
      }
      shouldCount = match.shouldCount;
    }

    try {
      const entries = await fs.readdir(currentDir, { withFileTypes: true });
      let dirCount = 0;

      for (const entry of entries) {
        if (entry.isFile() && shouldCount) {
          const ext = path.extname(entry.name).toLowerCase();
          if (CODE_EXTENSIONS.has(ext)) {
            // Skip test files
            if (!entry.name.includes('.test.') && !entry.name.includes('.spec.')) {
              total++;
              dirCount++;
            }
          }
        } else if (entry.isDirectory() && !IGNORE_DIRS.has(entry.name)) {
          await scan(path.join(currentDir, entry.name));
        }
      }

      // Count directories with code files (only if shouldCount)
      if (dirCount > 0 && shouldCount) {
        totalDirs++;
      }

      // Track by top-level directory (only if shouldCount)
      if (relativePath && shouldCount && dirCount > 0) {
        const topDir = relativePath.split('/').slice(0, 2).join('/');
        if (!byDir[topDir]) byDir[topDir] = { discovered: 0, audited: 0 };
        byDir[topDir].discovered += dirCount;
      }
    } catch {
      // Skip inaccessible dirs
    }
  }

  await scan(dir);
  return { total, totalDirs, byDir };
}

/**
 * Calculate effective doc coverage considering parent-child relationships
 * Small dirs (<5 files AND <200 lines) are covered if parent has CLAUDE.md
 * @param {string} dir - Directory to scan
 * @param {string} rootPath - Project root
 * @param {object} config - Config with include/ignore patterns
 * @returns {Promise<{
 *   withClaude: number,
 *   largeMissing: number,
 *   smallCoveredByParent: number,
 *   smallOrphan: number,
 *   effectiveTotal: number,
 *   effectiveCovered: number,
 *   effectivePercent: number,
 *   actualPercent: number
 * }>}
 */
async function calculateEffectiveDocCoverage(dir, rootPath, config) {
  const ignorePatterns = config.ignore || [];
  const includePatterns = config.include || [];

  // Track all directories with code
  const allDirs = []; // { path, fileCount, lineCount, hasClaude, isLarge }

  async function analyzeDir(dirPath) {
    let fileCount = 0;
    let lineCount = 0;

    try {
      const entries = await fs.readdir(dirPath, { withFileTypes: true });
      for (const e of entries) {
        if (!e.isFile()) continue;
        const ext = path.extname(e.name).toLowerCase();
        if (!CODE_EXTENSIONS.has(ext)) continue;
        if (e.name.includes('.test.') || e.name.includes('.spec.')) continue;

        fileCount++;
        try {
          const content = await fs.readFile(path.join(dirPath, e.name), 'utf-8');
          lineCount += content.split('\n').length;
        } catch {}
      }
    } catch {}

    return { fileCount, lineCount };
  }

  async function hasClaude(dirPath) {
    try {
      await fs.access(path.join(dirPath, 'CLAUDE.md'));
      return true;
    } catch {
      return false;
    }
  }

  async function scan(currentDir) {
    const relativePath = path.relative(rootPath, currentDir);

    if (relativePath && shouldIgnore(relativePath, ignorePatterns)) return;

    // Apply include patterns
    let shouldCount = true;
    if (relativePath && includePatterns.length > 0) {
      const match = matchesInclude(relativePath, includePatterns);
      if (!match.canEnter) return;
      shouldCount = match.shouldCount;
    }

    try {
      const entries = await fs.readdir(currentDir, { withFileTypes: true });

      if (shouldCount) {
        const stats = await analyzeDir(currentDir);
        if (stats.fileCount > 0) {
          const hasClaudeMd = await hasClaude(currentDir);
          const isLarge = stats.fileCount >= LARGE_THRESHOLD.files ||
                         stats.lineCount >= LARGE_THRESHOLD.lines;

          allDirs.push({
            path: relativePath || '.',
            fileCount: stats.fileCount,
            lineCount: stats.lineCount,
            hasClaude: hasClaudeMd,
            isLarge
          });
        }
      }

      for (const e of entries) {
        if (e.isDirectory() && !IGNORE_DIRS.has(e.name)) {
          await scan(path.join(currentDir, e.name));
        }
      }
    } catch {}
  }

  await scan(dir);

  // Build set of dirs with CLAUDE.md for parent lookup
  const claudeDirs = new Set(allDirs.filter(d => d.hasClaude).map(d => d.path));

  // Check if a dir has a parent with CLAUDE.md
  function hasParentWithClaude(dirPath) {
    const parts = dirPath.split('/');
    for (let i = parts.length - 1; i >= 0; i--) {
      const parentPath = parts.slice(0, i).join('/') || '.';
      if (claudeDirs.has(parentPath)) return true;
    }
    return false;
  }

  // Categorize
  let withClaude = 0;
  let largeMissing = 0;
  let smallCoveredByParent = 0;
  let smallOrphan = 0;

  for (const d of allDirs) {
    if (d.hasClaude) {
      withClaude++;
    } else if (d.isLarge) {
      largeMissing++;
    } else if (hasParentWithClaude(d.path)) {
      smallCoveredByParent++;
    } else {
      smallOrphan++;
    }
  }

  const totalDirs = allDirs.length;
  const effectiveTotal = withClaude + largeMissing; // Only count dirs that NEED their own CLAUDE.md
  const effectiveCovered = withClaude;

  return {
    withClaude,
    largeMissing,
    smallCoveredByParent,
    smallOrphan,
    effectiveTotal,
    effectiveCovered,
    effectivePercent: effectiveTotal > 0 ? Math.round((effectiveCovered / effectiveTotal) * 100) : 0,
    actualPercent: totalDirs > 0 ? Math.round((withClaude / totalDirs) * 100) : 0
  };
}

/**
 * Recursively find all directories with CLAUDE.md
 * @param {string} dir - Directory to scan
 * @param {string} rootPath - Project root
 * @param {string[]} ignorePatterns - Patterns to ignore
 * @returns {Promise<string[]>} List of directories with CLAUDE.md
 */
async function findClaudeDirs(dir, rootPath, ignorePatterns) {
  const results = [];

  async function scan(currentDir) {
    const relativePath = path.relative(rootPath, currentDir);

    if (relativePath && shouldIgnore(relativePath, ignorePatterns)) {
      return;
    }

    try {
      const entries = await fs.readdir(currentDir, { withFileTypes: true });

      const hasClaudeMd = entries.some(e => e.isFile() && e.name === 'CLAUDE.md');
      if (hasClaudeMd) {
        results.push(currentDir);
      }

      for (const entry of entries) {
        if (entry.isDirectory() && !IGNORE_DIRS.has(entry.name)) {
          await scan(path.join(currentDir, entry.name));
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
 * @typedef {'never' | 'stale' | 'fresh' | 'clean'} AuditStatus
 */

/**
 * Check audit status for a directory
 * @param {string} dir - Directory to check
 * @returns {Promise<{status: AuditStatus, auditMtime?: Date, codeMtime?: Date, newestFile?: string, severity?: string, issueCount?: number, fileCount?: number}>}
 */
async function checkAuditStatus(dir) {
  const auditPath = path.join(dir, 'AUDIT.md');

  // Get code file info first (for fileCount)
  const { mtime: codeMtime, file: newestFile, fileCount } = await getNewestCodeMtime(dir);

  // Check if AUDIT.md exists
  let auditStat, auditContent;
  try {
    auditStat = await fs.stat(auditPath);
    auditContent = await fs.readFile(auditPath, 'utf-8');
  } catch {
    return { status: 'never', fileCount };
  }

  // Parse AUDIT.md content
  const severityMatch = auditContent.match(/Severity:\s*\*\*(\w+)\*\*/i);
  const severity = severityMatch ? severityMatch[1].toLowerCase() : 'unknown';

  const issueMatch = auditContent.match(/## Issues \((\d+)\)/);
  const issueCount = issueMatch ? parseInt(issueMatch[1], 10) : 0;

  // Determine status
  let status;
  if (issueCount === 0) {
    status = 'clean';
  } else if (codeMtime && codeMtime > auditStat.mtime) {
    status = 'stale';
  } else {
    status = 'fresh';
  }

  return {
    status,
    auditMtime: auditStat.mtime,
    codeMtime,
    newestFile,
    severity,
    issueCount,
    fileCount
  };
}

/**
 * @typedef {object} AuditResult
 * @property {string} path - Relative path
 * @property {AuditStatus} status - Audit status
 * @property {string} [severity] - Audit severity
 * @property {number} [issueCount] - Number of issues
 * @property {Date} [auditMtime] - AUDIT.md mtime
 * @property {Date} [codeMtime] - Newest code file mtime
 * @property {string} [newestFile] - Newest code file name
 */

/**
 * Main function
 */
async function main() {
  const args = parseArgs(process.argv.slice(2), {
    json: false,
    never: false,
    stale: false,
    summary: false
  });

  const targetPath = args._?.[0] || process.cwd();
  const rootPath = path.resolve(targetPath);

  // Load config
  const config = await loadConfig(rootPath);
  const ignorePatterns = config.ignore || [];

  if (!args.json && !args.summary) {
    console.log(`Scanning: ${rootPath}\n`);
  }

  // Find all CLAUDE.md directories
  const claudeDirs = await findClaudeDirs(rootPath, rootPath, ignorePatterns);

  // Count all code files in scope (for coverage calculation)
  const fileStats = await countAllCodeFiles(rootPath, rootPath, config);
  const totalDiscoveredFiles = fileStats.total;
  const totalDiscoveredDirs = fileStats.totalDirs;
  const byDir = fileStats.byDir;

  // Calculate effective doc coverage
  const effectiveCoverage = await calculateEffectiveDocCoverage(rootPath, rootPath, config);

  // Check audit status for each, filtering by include/ignore
  /** @type {AuditResult[]} */
  const results = [];

  for (const dir of claudeDirs) {
    const relativePath = path.relative(rootPath, dir) || '.';

    // Apply include/ignore filter
    if (!shouldProcess(relativePath, config)) continue;

    const audit = await checkAuditStatus(dir);

    results.push({
      path: relativePath,
      status: audit.status,
      severity: audit.severity,
      issueCount: audit.issueCount,
      fileCount: audit.fileCount,
      auditMtime: audit.auditMtime,
      codeMtime: audit.codeMtime,
      newestFile: audit.newestFile
    });
  }

  // Sort by status priority, then severity
  const statusOrder = { never: 0, stale: 1, fresh: 2, clean: 3 };
  const severityOrder = { critical: 0, high: 1, medium: 2, low: 3, unknown: 4 };

  results.sort((a, b) => {
    const statusDiff = statusOrder[a.status] - statusOrder[b.status];
    if (statusDiff !== 0) return statusDiff;

    if (a.severity && b.severity) {
      return (severityOrder[a.severity] ?? 5) - (severityOrder[b.severity] ?? 5);
    }
    return a.path.localeCompare(b.path);
  });

  // Filter based on flags
  let filtered = results;
  if (args.never) {
    filtered = results.filter(r => r.status === 'never');
  } else if (args.stale) {
    filtered = results.filter(r => r.status === 'stale');
  }

  // Calculate stats
  const total = results.length;
  const stats = {
    never: results.filter(r => r.status === 'never').length,
    stale: results.filter(r => r.status === 'stale').length,
    fresh: results.filter(r => r.status === 'fresh').length,
    clean: results.filter(r => r.status === 'clean').length
  };

  const severityCounts = { critical: 0, high: 0, medium: 0, low: 0 };
  let totalIssues = 0;
  let totalFiles = 0;

  for (const r of results) {
    if (r.status !== 'never' && r.severity && severityCounts[r.severity] !== undefined) {
      severityCounts[r.severity]++;
    }
    if (r.issueCount) totalIssues += r.issueCount;
    if (r.fileCount) totalFiles += r.fileCount;

    // Track audited files by top-level directory
    if (r.fileCount && r.path !== '.') {
      const topDir = r.path.split('/').slice(0, 2).join('/');
      if (byDir[topDir]) {
        byDir[topDir].audited += r.fileCount;
      }
    }
  }

  const historySummary = await updateAuditHistory(rootPath, totalIssues, results);

  // Output
  if (args.json) {
    // Calculate coverage per directory
    const dirCoverage = {};
    for (const [dir, counts] of Object.entries(byDir)) {
      if (counts.discovered > 0) {
        dirCoverage[dir] = {
          discovered: counts.discovered,
          audited: counts.audited,
          coveragePercent: Math.round((counts.audited / counts.discovered) * 100)
        };
      }
    }

    console.log(JSON.stringify({
      total,
      totalFiles,
      totalDiscoveredFiles,
      totalDiscoveredDirs,
      uncoveredFiles: totalDiscoveredFiles - totalFiles,
      coveragePercent: totalDiscoveredFiles > 0 ? Math.round((totalFiles / totalDiscoveredFiles) * 100) : 0,
      docCoveragePercent: totalDiscoveredDirs > 0 ? Math.round((total / totalDiscoveredDirs) * 100) : 0,
      // Effective doc coverage (small dirs covered by parent count as covered)
      effectiveDocCoverage: {
        withClaude: effectiveCoverage.withClaude,
        largeMissing: effectiveCoverage.largeMissing,
        smallCoveredByParent: effectiveCoverage.smallCoveredByParent,
        smallOrphan: effectiveCoverage.smallOrphan,
        effectiveTotal: effectiveCoverage.effectiveTotal,
        effectiveCovered: effectiveCoverage.effectiveCovered,
        effectivePercent: effectiveCoverage.effectivePercent,
        actualPercent: effectiveCoverage.actualPercent
      },
      stats,
      severityCounts,
      totalIssues,
      history: historySummary,
      dirCoverage,
      modules: filtered
    }, null, 2));
    return;
  }

  if (args.summary) {
    console.log(`Total Modules: ${total}`);
    console.log(`  ⚫ Never audited: ${stats.never}`);
    console.log(`  🟤 Stale (code changed): ${stats.stale}`);
    console.log(`  🔵 Fresh (up-to-date): ${stats.fresh}`);
    console.log(`  ✅ Clean (0 issues): ${stats.clean}`);
    console.log(`\nTotal Issues: ${totalIssues}`);
    console.log(`  Critical: ${severityCounts.critical}, High: ${severityCounts.high}, Medium: ${severityCounts.medium}, Low: ${severityCounts.low}`);
    return;
  }

  // Full output
  if (stats.never > 0 && !args.stale) {
    console.log(`=== ⚫ NEVER AUDITED (${stats.never}) ===`);
    for (const r of filtered.filter(r => r.status === 'never')) {
      console.log(`  ○ ${r.path}`);
    }
    console.log('');
  }

  if (stats.stale > 0 && !args.never) {
    console.log(`=== 🟤 STALE - Code Modified Since Audit (${stats.stale}) ===`);
    for (const r of filtered.filter(r => r.status === 'stale')) {
      const file = r.newestFile ? ` [${r.newestFile}]` : '';
      console.log(`  ◐ ${r.path} (${r.issueCount || 0} issues)${file}`);
    }
    console.log('');
  }

  if (!args.never && !args.stale) {
    // Group fresh by severity
    for (const severity of ['critical', 'high', 'medium', 'low']) {
      const group = filtered.filter(r => r.status === 'fresh' && r.severity === severity);
      if (group.length > 0) {
        const icon = { critical: '🔴', high: '🟠', medium: '🟡', low: '🟢' }[severity];
        console.log(`=== ${icon} ${severity.toUpperCase()} (${group.length}) ===`);
        for (const r of group) {
          console.log(`  ● ${r.path} (${r.issueCount || 0} issues)`);
        }
        console.log('');
      }
    }

    // Show clean modules
    if (stats.clean > 0) {
      console.log(`=== ✅ CLEAN - All Issues Resolved (${stats.clean}) ===`);
      for (const r of filtered.filter(r => r.status === 'clean')) {
        console.log(`  ✓ ${r.path}`);
      }
      console.log('');
    }
  }

  // Summary line
  console.log('────────────────────────────────────────────────────────────');
  console.log(`Total: ${total} | Never: ${stats.never} | Stale: ${stats.stale} | Fresh: ${stats.fresh} | Clean: ${stats.clean} | Issues: ${totalIssues}`);
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
