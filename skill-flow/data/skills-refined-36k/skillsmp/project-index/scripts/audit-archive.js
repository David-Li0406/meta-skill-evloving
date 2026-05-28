#!/usr/bin/env node
/**
 * Audit Archive - Archive resolved issues to AUDIT_HISTORY.md
 *
 * Usage:
 *   node audit-archive.js <module-path> [issue-ids...]   # Archive specific issues
 *   node audit-archive.js <module-path> --all            # Archive all issues (mark as resolved)
 *   node audit-archive.js <module-path> --show           # Show current issues
 *   node audit-archive.js <module-path> --history        # Show archive history
 *
 * When all issues are archived, AUDIT.md shows "No current issues".
 * Next audit run will generate fresh issues for any new/modified code.
 */

import { promises as fs } from 'fs';
import path from 'path';
import { parseArgs, fileExists } from './shared.js';

/**
 * Parse AUDIT.md content into structured data
 * @param {string} content - AUDIT.md content
 * @returns {{header: string, severity: string, summary: string, issues: Array<{id: number, title: string, content: string}>}}
 */
function parseAuditMd(content) {
  const lines = content.split('\n');

  // Extract header (everything before ## Summary, not ## Issues)
  // This prevents Summary duplication when generateAuditMd adds it back
  const summaryHeaderIdx = lines.findIndex(l => l.startsWith('## Summary'));
  const header = summaryHeaderIdx > 0 ? lines.slice(0, summaryHeaderIdx).join('\n') : '';

  // Extract severity
  const severityMatch = content.match(/Severity:\s*\*\*(\w+)\*\*/i);
  const severity = severityMatch ? severityMatch[1] : 'UNKNOWN';

  // Extract summary
  const summaryMatch = content.match(/## Summary\n([\s\S]*?)(?=\n## Issues|\n##[^#]|$)/);
  const summary = summaryMatch ? summaryMatch[1].trim() : '';

  // Parse issues
  const issues = [];
  const issueRegex = /### (\d+)\. ([^\n]+)\n([\s\S]*?)(?=\n### \d+\.|$)/g;

  let match;
  while ((match = issueRegex.exec(content)) !== null) {
    issues.push({
      id: parseInt(match[1], 10),
      title: match[2].trim(),
      content: match[3].trim()
    });
  }

  return { header, severity, summary, issues };
}

/**
 * Generate AUDIT.md content from structured data
 * @param {{header: string, severity: string, summary: string, issues: Array<{id: number, title: string, content: string}>}} data
 * @returns {string}
 */
function generateAuditMd(data) {
  const { header, severity, summary, issues } = data;

  // Update severity in header if changed
  let updatedHeader = header.trim();
  if (severity) {
    updatedHeader = updatedHeader.replace(
      /Severity:\s*\*\*\w+\*\*/i,
      `Severity: **${severity.toUpperCase()}**`
    );
  }

  let content = updatedHeader + '\n\n';

  if (issues.length === 0) {
    // All issues resolved
    content += `## Summary\n${summary}\n\n`;
    content += `## Issues (0)\n\nNo current issues. All previously identified issues have been resolved and archived to AUDIT_HISTORY.md.\n`;
  } else {
    content += `## Summary\n${summary}\n\n`;
    content += `## Issues (${issues.length})\n`;

    for (let i = 0; i < issues.length; i++) {
      const issue = issues[i];
      content += `### ${i + 1}. ${issue.title}\n${issue.content}\n\n`;
    }
  }

  return content.trim() + '\n';
}

/**
 * Generate or append to AUDIT_HISTORY.md
 * @param {string} historyPath - Path to AUDIT_HISTORY.md
 * @param {Array<{id: number, title: string, content: string}>} archivedIssues
 * @param {string} modulePath - Module path for context
 * @returns {Promise<void>}
 */
async function appendToHistory(historyPath, archivedIssues, modulePath) {
  const timestamp = new Date().toISOString();
  let existingContent = '';

  try {
    existingContent = await fs.readFile(historyPath, 'utf-8');
  } catch {
    // File doesn't exist, create new
    existingContent = `# Audit History - ${path.basename(modulePath)}\n\nArchived issues from security audits.\n\n---\n\n`;
  }

  // Append new archived issues
  let newSection = `## Archived: ${timestamp.slice(0, 10)}\n\n`;

  for (const issue of archivedIssues) {
    newSection += `### [RESOLVED] ${issue.title}\n`;
    newSection += `*Archived: ${timestamp}*\n\n`;
    newSection += issue.content + '\n\n';
  }

  newSection += '---\n\n';

  // Insert after header (before first ## Archived section or at end)
  const headerEndIdx = existingContent.indexOf('---\n\n');
  if (headerEndIdx > 0) {
    const header = existingContent.slice(0, headerEndIdx + 5);
    const rest = existingContent.slice(headerEndIdx + 5);
    existingContent = header + newSection + rest;
  } else {
    existingContent += newSection;
  }

  await fs.writeFile(historyPath, existingContent);
}

/**
 * Main function
 */
async function main() {
  const args = parseArgs(process.argv.slice(2), {
    all: false,
    show: false,
    history: false
  });

  const modulePath = args._?.[0];
  if (!modulePath) {
    console.error('Usage: node audit-archive.js <module-path> [issue-ids...] [--all] [--show] [--history]');
    process.exit(1);
  }

  const absPath = path.resolve(modulePath);
  const auditPath = path.join(absPath, 'AUDIT.md');
  const historyPath = path.join(absPath, 'AUDIT_HISTORY.md');

  // Check AUDIT.md exists
  if (!await fileExists(auditPath)) {
    console.error(`No AUDIT.md found at: ${auditPath}`);
    process.exit(1);
  }

  const content = await fs.readFile(auditPath, 'utf-8');
  const data = parseAuditMd(content);

  // --show: Display current issues
  if (args.show) {
    console.log(`Module: ${modulePath}`);
    console.log(`Severity: ${data.severity}`);
    console.log(`Issues: ${data.issues.length}\n`);

    for (const issue of data.issues) {
      console.log(`  ${issue.id}. ${issue.title}`);
    }
    return;
  }

  // --history: Display archive history
  if (args.history) {
    if (!await fileExists(historyPath)) {
      console.log('No archive history found.');
      return;
    }

    const historyContent = await fs.readFile(historyPath, 'utf-8');
    console.log(historyContent);
    return;
  }

  // Determine which issues to archive
  let issueIds = [];

  if (args.all) {
    issueIds = data.issues.map(i => i.id);
  } else {
    // Parse issue IDs from remaining positional args
    const positionalArgs = args._.slice(1);
    issueIds = positionalArgs.map(arg => parseInt(arg, 10)).filter(n => !isNaN(n));
  }

  if (issueIds.length === 0) {
    console.error('No issue IDs specified. Use --all to archive all issues, or specify issue numbers.');
    console.log('\nCurrent issues:');
    for (const issue of data.issues) {
      console.log(`  ${issue.id}. ${issue.title}`);
    }
    process.exit(1);
  }

  // Find issues to archive
  const toArchive = data.issues.filter(i => issueIds.includes(i.id));
  const remaining = data.issues.filter(i => !issueIds.includes(i.id));

  if (toArchive.length === 0) {
    console.error('No matching issues found for the specified IDs.');
    process.exit(1);
  }

  // Archive to AUDIT_HISTORY.md
  await appendToHistory(historyPath, toArchive, modulePath);

  // Update AUDIT.md with remaining issues
  data.issues = remaining;

  // Recalculate severity based on remaining issues
  if (remaining.length === 0) {
    data.severity = 'NONE';
  }

  await fs.writeFile(auditPath, generateAuditMd(data));

  // Output
  console.log(`Archived ${toArchive.length} issue(s) to AUDIT_HISTORY.md`);
  for (const issue of toArchive) {
    console.log(`  ✓ ${issue.id}. ${issue.title}`);
  }

  if (remaining.length > 0) {
    console.log(`\nRemaining issues: ${remaining.length}`);
  } else {
    console.log(`\n✅ All issues resolved! AUDIT.md is now clean.`);
  }
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
