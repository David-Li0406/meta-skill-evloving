#!/usr/bin/env node
/**
 * Generate comprehensive session recovery report
 *
 * Usage:
 *   node generate-recovery-report.js [options]
 *
 * Options:
 *   --minutes N      Analyze agents from last N minutes (default: 180)
 *   --project PATH   Specify project path (default: current directory)
 *   --agents IDS     Comma-separated agent IDs to analyze
 *   --format FMT     Output format: markdown, json, summary (default: markdown)
 *   --output FILE    Write to file instead of stdout
 *   --help           Show help
 *
 * Examples:
 *   node generate-recovery-report.js
 *   node generate-recovery-report.js --minutes 60
 *   node generate-recovery-report.js --agents a91845a,abec615
 *   node generate-recovery-report.js --format json
 */

import { readFile, stat, access, writeFile } from 'fs/promises';
import { readdir } from 'fs/promises';
import { constants } from 'fs';
import { homedir } from 'os';
import { join, resolve, basename } from 'path';
import { execSync } from 'child_process';

const DEFAULT_MINUTES = 180;

/**
 * Parse command line arguments
 */
function parseArgs() {
  const args = process.argv.slice(2);
  const options = {
    minutes: DEFAULT_MINUTES,
    project: process.cwd(),
    agents: null,
    format: 'markdown',
    output: null,
    help: false
  };

  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case '--minutes':
        options.minutes = parseInt(args[++i], 10);
        break;
      case '--project':
        options.project = resolve(args[++i]);
        break;
      case '--agents':
        options.agents = args[++i].split(',').map(a => a.trim());
        break;
      case '--format':
        options.format = args[++i];
        break;
      case '--output':
        options.output = args[++i];
        break;
      case '--help':
      case '-h':
        options.help = true;
        break;
    }
  }

  return options;
}

/**
 * Get log directory for project
 */
function getLogDirectory(projectPath) {
  const sanitized = projectPath.replace(/\//g, '-').replace(/^-/, '');
  return join(homedir(), '.claude', 'projects', sanitized);
}

/**
 * Find recent agent logs
 */
async function findAgentLogs(logDir, minutes, specificAgents) {
  const cutoff = Date.now() - (minutes * 60 * 1000);

  let files;
  try {
    files = await readdir(logDir);
  } catch (error) {
    return [];
  }

  const logs = [];
  for (const file of files) {
    if (!file.startsWith('agent-') || !file.endsWith('.jsonl')) continue;

    // Extract agent ID
    const match = file.match(/agent-([a-f0-9]+)\.jsonl/);
    const id = match ? match[1] : null;

    // Filter by specific agents if provided
    if (specificAgents && !specificAgents.includes(id)) continue;

    const filePath = join(logDir, file);
    const stats = await stat(filePath);

    // Filter by time
    if (stats.mtimeMs > cutoff) {
      logs.push({
        id,
        path: filePath,
        size: stats.size,
        modified: new Date(stats.mtimeMs)
      });
    }
  }

  return logs.sort((a, b) => b.modified - a.modified);
}

/**
 * Analyze a single log file
 */
async function analyzeLog(logPath) {
  const content = await readFile(logPath, 'utf-8');
  const lines = content.trim().split('\n').filter(l => l.trim());
  const stats = await stat(logPath);

  const result = {
    path: logPath,
    agentId: basename(logPath).match(/agent-([a-f0-9]+)/)?.[1] || 'unknown',
    totalMessages: lines.length,
    size: stats.size,
    modified: new Date(stats.mtimeMs),
    filesCreated: new Set(),
    filesModified: new Set(),
    testResults: null,
    status: 'UNKNOWN',
    errors: [],
    taskId: null
  };

  for (const line of lines) {
    try {
      const entry = JSON.parse(line);
      const content = entry.message?.content || [];

      for (const block of content) {
        if (block.type === 'tool_use') {
          if (block.name === 'Write' && block.input?.file_path) {
            result.filesCreated.add(block.input.file_path);
          }
          if (block.name === 'Edit' && block.input?.file_path) {
            result.filesModified.add(block.input.file_path);
          }
        }
        if (block.type === 'text' && block.text) {
          // Task ID
          const taskMatch = block.text.match(/TASK-\d+\.\d+/);
          if (taskMatch && !result.taskId) {
            result.taskId = taskMatch[0];
          }
          // Test results
          const testMatch = block.text.match(/(\d+)\s+(passed|tests?\s+passed)/i);
          if (testMatch) {
            result.testResults = testMatch[0];
          }
          // Errors
          if (/error|failed|exception/i.test(block.text)) {
            const snippet = block.text.slice(0, 200);
            if (!result.errors.some(e => e.includes(snippet.slice(0, 50)))) {
              result.errors.push(snippet);
            }
          }
        }
      }
    } catch (e) {
      // Skip malformed lines
    }
  }

  // Convert Sets to Arrays
  result.filesCreated = [...result.filesCreated];
  result.filesModified = [...result.filesModified];

  // Determine status
  const lastLines = lines.slice(-10).join(' ').toLowerCase();
  if (lastLines.includes('complete') || lastLines.includes('successfully')) {
    result.status = 'COMPLETE';
  } else if (result.errors.length > 0 && !lastLines.includes('passed')) {
    result.status = 'FAILED';
  } else if (result.totalMessages > 50 && result.filesCreated.length > 0) {
    result.status = 'IN_PROGRESS';
  } else if (result.totalMessages < 10 && result.filesCreated.length === 0) {
    result.status = 'NOT_STARTED';
  }

  return result;
}

/**
 * Verify files exist on disk
 */
async function verifyFiles(files) {
  const results = { verified: [], missing: [] };

  for (const file of files) {
    try {
      await access(file, constants.R_OK);
      const stats = await stat(file);
      if (stats.size > 0) {
        results.verified.push({ path: file, size: stats.size });
      } else {
        results.missing.push({ path: file, reason: 'empty' });
      }
    } catch {
      results.missing.push({ path: file, reason: 'not found' });
    }
  }

  return results;
}

/**
 * Get git status
 */
function getGitStatus() {
  try {
    const status = execSync('git status --short', { encoding: 'utf-8' });
    return status.trim().split('\n').filter(l => l.trim());
  } catch {
    return [];
  }
}

/**
 * Generate resumption command for a task
 */
function generateResumptionCommand(analysis) {
  const agent = determineAgent(analysis);
  const taskId = analysis.taskId || 'Unknown Task';

  if (analysis.status === 'IN_PROGRESS') {
    return `Task("${agent}", "Complete ${taskId}

Last state: Work in progress (crashed mid-execution)
Files created: ${analysis.filesCreated.length}
Files modified: ${analysis.filesModified.length}

Please verify existing files and complete the task.
Check for partial implementations and test coverage.")`;
  }

  if (analysis.status === 'FAILED') {
    const lastError = analysis.errors[analysis.errors.length - 1] || 'Unknown error';
    return `Task("${agent}", "Fix ${taskId}

Error encountered: ${lastError.slice(0, 100)}

Please investigate and fix the error.
Verify the fix with tests.")`;
  }

  return null;
}

/**
 * Determine appropriate agent for task
 */
function determineAgent(analysis) {
  const files = [...analysis.filesCreated, ...analysis.filesModified];

  // Check file types
  const hasPython = files.some(f => f.endsWith('.py'));
  const hasTypescript = files.some(f => f.endsWith('.ts') || f.endsWith('.tsx'));
  const hasComponent = files.some(f => f.includes('component') || f.includes('Component'));

  if (hasComponent || (hasTypescript && !hasPython)) {
    return 'ui-engineer-enhanced';
  }
  if (hasPython) {
    return 'python-backend-engineer';
  }
  return 'codebase-explorer';
}

/**
 * Generate commit message
 */
function generateCommitMessage(analyses) {
  const completed = analyses.filter(a => a.status === 'COMPLETE');
  const interrupted = analyses.filter(a => a.status === 'IN_PROGRESS');
  const failed = analyses.filter(a => a.status === 'FAILED');

  let message = 'feat: recover work from interrupted session\n\n';

  if (completed.length > 0) {
    message += 'Completed:\n';
    for (const a of completed) {
      message += `- ${a.taskId || a.agentId}: ${a.filesCreated.length} files\n`;
    }
    message += '\n';
  }

  if (interrupted.length > 0) {
    message += 'Interrupted (to resume):\n';
    for (const a of interrupted) {
      message += `- ${a.taskId || a.agentId}\n`;
    }
    message += '\n';
  }

  if (failed.length > 0) {
    message += 'Failed (needs fix):\n';
    for (const a of failed) {
      message += `- ${a.taskId || a.agentId}\n`;
    }
    message += '\n';
  }

  message += 'Recovered via session-recovery skill';
  return message;
}

/**
 * Format size
 */
function formatSize(bytes) {
  if (bytes < 1024) return `${bytes}B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)}KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)}MB`;
}

/**
 * Generate markdown report
 */
function generateMarkdownReport(report) {
  const lines = [];

  lines.push('# Session Recovery Report');
  lines.push('');
  lines.push(`**Generated**: ${report.generated}`);
  lines.push(`**Project**: ${report.project}`);
  lines.push(`**Time Window**: Last ${report.minutes} minutes`);
  lines.push('');

  // Quick summary
  lines.push('## Quick Summary');
  lines.push('');
  lines.push('| Status | Count |');
  lines.push('|--------|-------|');
  for (const [status, count] of Object.entries(report.statusCounts)) {
    lines.push(`| ${status} | ${count} |`);
  }
  lines.push('');

  // Agent status table
  lines.push('## Agent Status Summary');
  lines.push('');
  lines.push('| Agent ID | Task | Status | Files | Tests | Notes |');
  lines.push('|----------|------|--------|-------|-------|-------|');
  for (const analysis of report.analyses) {
    const task = analysis.taskId || '-';
    const files = analysis.filesCreated.length + analysis.filesModified.length;
    const tests = analysis.testResults || '-';
    const notes = analysis.errors.length > 0 ? `${analysis.errors.length} errors` : '-';
    lines.push(`| ${analysis.agentId} | ${task} | ${analysis.status} | ${files} | ${tests} | ${notes} |`);
  }
  lines.push('');

  // Completed work
  const completed = report.analyses.filter(a => a.status === 'COMPLETE');
  if (completed.length > 0) {
    lines.push('## Completed Work');
    lines.push('');
    for (const analysis of completed) {
      lines.push(`### ${analysis.taskId || analysis.agentId}`);
      lines.push('');
      lines.push('**Files Created:**');
      for (const file of analysis.filesCreated) {
        lines.push(`- \`${file}\``);
      }
      if (analysis.testResults) {
        lines.push('');
        lines.push(`**Tests:** ${analysis.testResults}`);
      }
      lines.push('');
    }
  }

  // Interrupted tasks
  const interrupted = report.analyses.filter(a => a.status === 'IN_PROGRESS');
  if (interrupted.length > 0) {
    lines.push('## Interrupted Tasks');
    lines.push('');
    for (const analysis of interrupted) {
      lines.push(`### ${analysis.taskId || analysis.agentId}`);
      lines.push('');
      lines.push(`**Status**: IN_PROGRESS (crashed mid-execution)`);
      lines.push('');
      lines.push('**Files Created:**');
      for (const file of analysis.filesCreated) {
        lines.push(`- \`${file}\``);
      }
      lines.push('');
      lines.push('**Resumption Command:**');
      lines.push('```');
      lines.push(generateResumptionCommand(analysis));
      lines.push('```');
      lines.push('');
    }
  }

  // Failed tasks
  const failed = report.analyses.filter(a => a.status === 'FAILED');
  if (failed.length > 0) {
    lines.push('## Failed Tasks');
    lines.push('');
    for (const analysis of failed) {
      lines.push(`### ${analysis.taskId || analysis.agentId}`);
      lines.push('');
      lines.push(`**Status**: FAILED`);
      lines.push('');
      if (analysis.errors.length > 0) {
        lines.push('**Last Error:**');
        lines.push('```');
        lines.push(analysis.errors[analysis.errors.length - 1]);
        lines.push('```');
      }
      lines.push('');
      lines.push('**Remediation Command:**');
      lines.push('```');
      lines.push(generateResumptionCommand(analysis));
      lines.push('```');
      lines.push('');
    }
  }

  // Recommended actions
  lines.push('## Recommended Actions');
  lines.push('');
  lines.push('### 1. Commit Completed Work');
  lines.push('');
  lines.push('```bash');
  const allFiles = report.verification.verified.map(f => f.path);
  if (allFiles.length > 0) {
    lines.push(`git add ${allFiles.slice(0, 5).join(' ')}${allFiles.length > 5 ? ' ...' : ''}`);
  }
  lines.push('git commit -m "$(cat <<\'EOF\'');
  lines.push(generateCommitMessage(report.analyses));
  lines.push('EOF');
  lines.push(')"');
  lines.push('```');
  lines.push('');

  if (interrupted.length > 0 || failed.length > 0) {
    lines.push('### 2. Resume/Fix Interrupted Work');
    lines.push('');
    lines.push('Execute resumption commands above in priority order:');
    lines.push('1. Fix FAILED tasks first (may block others)');
    lines.push('2. Complete IN_PROGRESS tasks');
    lines.push('');
  }

  lines.push('### 3. Update Progress Tracking');
  lines.push('');
  lines.push('```');
  lines.push('Task("artifact-tracker", "Update progress:');
  for (const a of completed) {
    lines.push(`- ${a.taskId || a.agentId}: complete (recovered)`);
  }
  for (const a of interrupted) {
    lines.push(`- ${a.taskId || a.agentId}: in_progress (interrupted)`);
  }
  lines.push('")');
  lines.push('```');
  lines.push('');

  return lines.join('\n');
}

/**
 * Main entry point
 */
async function main() {
  const options = parseArgs();

  if (options.help) {
    console.log(`
Generate comprehensive session recovery report

Usage:
  node generate-recovery-report.js [options]

Options:
  --minutes N      Analyze agents from last N minutes (default: 180)
  --project PATH   Specify project path (default: current directory)
  --agents IDS     Comma-separated agent IDs to analyze
  --format FMT     Output format: markdown, json, summary (default: markdown)
  --output FILE    Write to file instead of stdout
  --help           Show this help message
`);
    process.exit(0);
  }

  const logDir = getLogDirectory(options.project);
  const logs = await findAgentLogs(logDir, options.minutes, options.agents);

  if (logs.length === 0) {
    console.error('No agent logs found');
    process.exit(1);
  }

  // Analyze all logs
  const analyses = [];
  for (const log of logs) {
    const analysis = await analyzeLog(log.path);
    analyses.push(analysis);
  }

  // Verify files
  const allFiles = analyses.flatMap(a => [...a.filesCreated, ...a.filesModified]);
  const verification = await verifyFiles([...new Set(allFiles)]);

  // Count statuses
  const statusCounts = { COMPLETE: 0, IN_PROGRESS: 0, FAILED: 0, NOT_STARTED: 0, UNKNOWN: 0 };
  for (const a of analyses) {
    statusCounts[a.status]++;
  }

  // Build report
  const report = {
    generated: new Date().toISOString(),
    project: options.project,
    logDir,
    minutes: options.minutes,
    analyses,
    verification,
    statusCounts,
    gitStatus: getGitStatus()
  };

  // Output
  let output;
  if (options.format === 'json') {
    output = JSON.stringify(report, null, 2);
  } else if (options.format === 'summary') {
    output = `Session Recovery Summary
========================
Agents analyzed: ${analyses.length}
Complete: ${statusCounts.COMPLETE}
In Progress: ${statusCounts.IN_PROGRESS}
Failed: ${statusCounts.FAILED}
Files verified: ${verification.verified.length}
Files missing: ${verification.missing.length}`;
  } else {
    output = generateMarkdownReport(report);
  }

  if (options.output) {
    await writeFile(options.output, output);
    console.log(`Report written to: ${options.output}`);
  } else {
    console.log(output);
  }
}

main().catch(error => {
  console.error('Error:', error.message);
  process.exit(1);
});
