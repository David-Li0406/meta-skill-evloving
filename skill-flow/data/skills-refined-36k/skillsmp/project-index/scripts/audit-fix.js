#!/usr/bin/env node
/**
 * Audit Fix - Automated AUDIT.md issue resolution
 *
 * Features:
 * - Reads AUDIT.md files and parses issues
 * - Classifies by severity and fixability
 * - Auto-fixes LOW/MEDIUM issues where possible
 * - Archives fixed issues to AUDIT_HISTORY.md
 * - Dashboard integration for tracking
 *
 * Usage:
 *   node audit-fix.js [options] [path]
 *
 * Options:
 *   --dry-run        Preview fixes without applying
 *   --severity=X     Only fix issues of severity X (LOW/MEDIUM/HIGH/CRITICAL)
 *   --module=path    Only fix specific module
 *   --concurrency=N  Parallel fix attempts (default 3)
 *   --status         Show last result
 *   --help           Show help
 */

import { promises as fs } from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { runCodeagent } from './batch-llm-runner.js';
import {
  readJsonSafe,
  writeJsonSafe,
  fileExists,
  loadConfig,
  parseArgs
} from './shared.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// Simple console logger
const log = {
  info: (...args) => console.log('[audit-fix]', ...args),
  warn: (...args) => console.warn('[audit-fix]', ...args),
  error: (...args) => console.error('[audit-fix]', ...args)
};

/**
 * Severity levels
 */
const Severity = {
  LOW: 'LOW',
  MEDIUM: 'MEDIUM',
  HIGH: 'HIGH',
  CRITICAL: 'CRITICAL'
};

/**
 * Issue types that can be auto-fixed
 */
const FIXABLE_TYPES = new Set([
  'missing_jsdoc',
  'console_log',
  'todo_fixme',
  'magic_number',
  'hardcoded_string',
  'missing_error_handling',
  'event_naming',
  'export_missing',
  'unused_import',
  'deprecated_api'
]);

/**
 * Parse AUDIT.md file
 * @param {string} filePath - Path to AUDIT.md
 * @returns {Promise<{modulePath: string, issues: Array}>}
 */
async function parseAuditFile(filePath) {
  const content = await fs.readFile(filePath, 'utf-8');
  const issues = [];

  // Parse markdown structure
  // Expected format:
  // ## Issues
  // ### [SEVERITY] Title
  // - **File**: path/to/file.js:line
  // - **Description**: ...
  // - **Suggestion**: ...

  const issueBlocks = content.split(/(?=###\s*\[)/);

  for (const block of issueBlocks) {
    if (!block.startsWith('###')) continue;

    const headerMatch = block.match(/###\s*\[(LOW|MEDIUM|HIGH|CRITICAL)\]\s*(.+)/);
    if (!headerMatch) continue;

    const severity = headerMatch[1];
    const title = headerMatch[2].trim();

    const fileMatch = block.match(/\*\*File\*\*:\s*([^\n]+)/);
    const descMatch = block.match(/\*\*Description\*\*:\s*([^\n]+)/);
    const suggestionMatch = block.match(/\*\*Suggestion\*\*:\s*([^\n]+)/);
    const codeMatch = block.match(/```[\s\S]*?```/);

    // Extract line number from file path
    const filePart = fileMatch ? fileMatch[1].trim() : '';
    const [file, lineStr] = filePart.split(':');
    const line = parseInt(lineStr) || 0;

    // Infer issue type from title/description
    const type = inferIssueType(title, descMatch?.[1] || '');

    issues.push({
      id: `issue-${issues.length}`,
      severity,
      title,
      file: file?.trim() || '',
      line,
      description: descMatch?.[1]?.trim() || '',
      suggestion: suggestionMatch?.[1]?.trim() || '',
      codeSnippet: codeMatch?.[0] || '',
      type,
      fixable: FIXABLE_TYPES.has(type) && severity !== Severity.CRITICAL
    });
  }

  return {
    modulePath: path.dirname(filePath),
    issues
  };
}

/**
 * Infer issue type from title and description
 */
function inferIssueType(title, description) {
  const text = (title + ' ' + description).toLowerCase();

  if (text.includes('jsdoc') || text.includes('documentation')) return 'missing_jsdoc';
  if (text.includes('console.log') || text.includes('console.')) return 'console_log';
  if (text.includes('todo') || text.includes('fixme')) return 'todo_fixme';
  if (text.includes('magic number') || text.includes('hardcoded')) return 'magic_number';
  if (text.includes('event') && text.includes('naming')) return 'event_naming';
  if (text.includes('export')) return 'export_missing';
  if (text.includes('import') && text.includes('unused')) return 'unused_import';
  if (text.includes('error') && text.includes('handling')) return 'missing_error_handling';
  if (text.includes('deprecated')) return 'deprecated_api';

  return 'unknown';
}

/**
 * Find all AUDIT.md files in a directory
 * @param {string} dir - Directory to search
 * @returns {Promise<string[]>}
 */
async function findAuditFiles(dir) {
  const results = [];

  async function walk(currentDir) {
    try {
      const entries = await fs.readdir(currentDir, { withFileTypes: true });

      for (const entry of entries) {
        const fullPath = path.join(currentDir, entry.name);

        if (entry.isDirectory() && !entry.name.startsWith('.') && entry.name !== 'node_modules') {
          await walk(fullPath);
        } else if (entry.name === 'AUDIT.md') {
          results.push(fullPath);
        }
      }
    } catch { }
  }

  await walk(dir);
  return results;
}

/**
 * Generate fix for an issue using LLM
 * @param {object} issue - Issue object
 * @param {string} cwd - Working directory
 * @returns {Promise<{success: boolean, fix: object|null}>}
 */
async function generateFix(issue, cwd) {
  const filePath = path.join(cwd, issue.file);

  // Read the source file
  let sourceContent = '';
  try {
    sourceContent = await fs.readFile(filePath, 'utf-8');
  } catch {
    return { success: false, fix: null, error: 'Cannot read source file' };
  }

  // Extract context around the line
  const lines = sourceContent.split('\n');
  const startLine = Math.max(0, issue.line - 10);
  const endLine = Math.min(lines.length, issue.line + 10);
  const context = lines.slice(startLine, endLine).join('\n');

  const prompt = `Fix this audit issue:

File: ${issue.file}
Line: ${issue.line}
Severity: ${issue.severity}
Type: ${issue.type}
Title: ${issue.title}
Description: ${issue.description}
Suggestion: ${issue.suggestion}

Context (lines ${startLine + 1}-${endLine}):
\`\`\`javascript
${context}
\`\`\`

Provide the fix. Output JSON:
{
  "analysis": "Brief explanation",
  "canFix": true/false,
  "changes": [
    {
      "lineStart": number,
      "lineEnd": number,
      "oldCode": "exact text to replace",
      "newCode": "replacement text"
    }
  ]
}`;

  try {
    const result = await runCodeagent(prompt, cwd, 90000);
    if (result.success) {
      const json = JSON.parse(result.output);
      return { success: true, fix: json };
    }
  } catch (e) {
    log.warn(`LLM fix generation failed: ${e.message}`);
  }

  return { success: false, fix: null };
}

/**
 * Apply fix to a file
 * @param {object} fix - Fix object with changes array
 * @param {string} filePath - Path to file
 * @returns {Promise<boolean>}
 */
async function applyFix(fix, filePath) {
  if (!fix.canFix || !fix.changes || fix.changes.length === 0) {
    return false;
  }

  try {
    let content = await fs.readFile(filePath, 'utf-8');

    // Apply changes in reverse order (to preserve line numbers)
    const sortedChanges = [...fix.changes].sort((a, b) => b.lineStart - a.lineStart);

    for (const change of sortedChanges) {
      if (change.oldCode && change.newCode) {
        content = content.replace(change.oldCode, change.newCode);
      }
    }

    await fs.writeFile(filePath, content);
    return true;
  } catch (e) {
    log.error(`Failed to apply fix: ${e.message}`);
    return false;
  }
}

/**
 * Archive fixed issue to AUDIT_HISTORY.md
 * @param {object} issue - The fixed issue
 * @param {string} modulePath - Module path
 */
async function archiveIssue(issue, modulePath) {
  const historyFile = path.join(modulePath, 'AUDIT_HISTORY.md');

  const entry = `
## ${new Date().toISOString().split('T')[0]} - [${issue.severity}] ${issue.title}

- **File**: ${issue.file}:${issue.line}
- **Type**: ${issue.type}
- **Resolution**: Auto-fixed by audit-fix
- **Description**: ${issue.description}
`;

  try {
    const existing = await fs.readFile(historyFile, 'utf-8').catch(() => '# Audit History\n\nArchive of resolved audit issues.\n');
    await fs.writeFile(historyFile, existing + entry);
  } catch (e) {
    log.warn(`Failed to archive issue: ${e.message}`);
  }
}

/**
 * Remove fixed issue from AUDIT.md
 * @param {string} auditFile - Path to AUDIT.md
 * @param {object} issue - Issue to remove
 */
async function removeFromAudit(auditFile, issue) {
  try {
    let content = await fs.readFile(auditFile, 'utf-8');

    // Find and remove the issue block
    const pattern = new RegExp(
      `###\\s*\\[${issue.severity}\\]\\s*${escapeRegex(issue.title)}[\\s\\S]*?(?=###|## |$)`,
      'g'
    );

    content = content.replace(pattern, '');

    // Clean up empty sections
    content = content.replace(/\n{3,}/g, '\n\n');

    await fs.writeFile(auditFile, content);
  } catch (e) {
    log.warn(`Failed to update AUDIT.md: ${e.message}`);
  }
}

function escapeRegex(str) {
  return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

/**
 * Main entry point
 */
async function main() {
  const args = parseArgs(process.argv.slice(2));

  if (args.help) {
    console.log(`
Audit Fix - Automated AUDIT.md issue resolution

Usage: node audit-fix.js [options] [path]

Options:
  --dry-run        Preview fixes without applying
  --severity=X     Only fix issues of severity X (LOW/MEDIUM/HIGH)
  --module=path    Only fix specific module
  --concurrency=N  Parallel fix attempts (default 3)
  --status         Show last result
  --help           Show this help
`);
    return;
  }

  const cwd = process.cwd();
  const targetPath = args._[0] || '';
  const dryRun = args['dry-run'] || false;
  const severityFilter = args.severity?.toUpperCase();
  const moduleFilter = args.module;
  const concurrency = parseInt(args.concurrency) || 3;

  // State files for dashboard tracking
  const stateDir = path.join(cwd, '.project-index');
  const tasksFile = path.join(stateDir, '.audit-fix-tasks.json');
  const resultFile = path.join(stateDir, '.audit-fix-result.json');

  await fs.mkdir(stateDir, { recursive: true });

  if (args.status) {
    const result = await readJsonSafe(resultFile, null);
    if (result) {
      console.log(JSON.stringify(result, null, 2));
    } else {
      console.log('No previous result found');
    }
    return;
  }

  log.info('Starting audit-fix...');

  const startTime = Date.now();
  const stats = {
    modulesScanned: 0,
    totalIssues: 0,
    fixable: 0,
    fixed: 0,
    skipped: 0,
    failed: 0,
    bySeverity: { LOW: 0, MEDIUM: 0, HIGH: 0, CRITICAL: 0 }
  };

  // Find AUDIT.md files
  const searchDir = targetPath ? path.join(cwd, targetPath) : cwd;
  const auditFiles = await findAuditFiles(searchDir);

  log.info(`Found ${auditFiles.length} AUDIT.md files`);

  // Parse all audit files
  const allIssues = [];

  for (const auditFile of auditFiles) {
    const { modulePath, issues } = await parseAuditFile(auditFile);
    stats.modulesScanned++;

    // Apply filters
    let filtered = issues;

    if (moduleFilter) {
      if (!modulePath.includes(moduleFilter)) continue;
    }

    if (severityFilter) {
      filtered = filtered.filter(i => i.severity === severityFilter);
    }

    for (const issue of filtered) {
      allIssues.push({
        ...issue,
        auditFile,
        modulePath
      });
    }
  }

  stats.totalIssues = allIssues.length;
  stats.fixable = allIssues.filter(i => i.fixable).length;

  log.info(`Total issues: ${stats.totalIssues}, Fixable: ${stats.fixable}`);

  // Save task state for dashboard
  const tasks = allIssues.map((issue, i) => ({
    id: issue.id || `issue-${i}`,
    module: issue.modulePath,
    status: 'pending',
    severity: issue.severity,
    type: issue.type,
    title: issue.title,
    fixable: issue.fixable
  }));
  await writeJsonSafe(tasksFile, { tasks, startedAt: new Date().toISOString() });

  // Process fixable issues
  const fixableIssues = allIssues.filter(i => i.fixable);

  // Process in batches
  for (let i = 0; i < fixableIssues.length; i += concurrency) {
    const batch = fixableIssues.slice(i, i + concurrency);

    const results = await Promise.all(
      batch.map(async (issue) => {
        stats.bySeverity[issue.severity]++;

        log.info(`Processing: [${issue.severity}] ${issue.title}`);

        const { success, fix } = await generateFix(issue, cwd);

        if (!success || !fix?.canFix) {
          log.info(`  Cannot auto-fix: ${fix?.analysis || 'LLM failed'}`);
          stats.skipped++;
          return { issue, success: false };
        }

        if (dryRun) {
          log.info(`  [dry-run] Would fix with ${fix.changes?.length || 0} changes`);
          return { issue, success: true, dryRun: true };
        }

        const filePath = path.join(cwd, issue.file);
        const applied = await applyFix(fix, filePath);

        if (applied) {
          log.info(`  Fixed!`);
          await archiveIssue(issue, issue.modulePath);
          await removeFromAudit(issue.auditFile, issue);
          stats.fixed++;
          return { issue, success: true };
        } else {
          log.info(`  Failed to apply fix`);
          stats.failed++;
          return { issue, success: false };
        }
      })
    );

    // Update task statuses
    for (const result of results) {
      const task = tasks.find(t => t.id === result.issue.id);
      if (task) {
        task.status = result.success ? 'completed' : 'failed';
      }
    }
    await writeJsonSafe(tasksFile, { tasks, startedAt: new Date().toISOString() });
  }

  // Final result
  const result = {
    success: stats.fixed > 0 || stats.totalIssues === 0,
    duration: Date.now() - startTime,
    ...stats,
    completedAt: new Date().toISOString()
  };

  await writeJsonSafe(resultFile, result);

  log.info(`\n=== Summary ===`);
  log.info(`Modules scanned: ${stats.modulesScanned}`);
  log.info(`Total issues: ${stats.totalIssues}`);
  log.info(`Fixable: ${stats.fixable}`);
  log.info(`Fixed: ${stats.fixed}`);
  log.info(`Skipped: ${stats.skipped}`);
  log.info(`Failed: ${stats.failed}`);
  log.info(`By severity: LOW=${stats.bySeverity.LOW}, MEDIUM=${stats.bySeverity.MEDIUM}, HIGH=${stats.bySeverity.HIGH}, CRITICAL=${stats.bySeverity.CRITICAL}`);
}

main().catch(e => {
  console.error('Fatal error:', e);
  process.exit(1);
});
