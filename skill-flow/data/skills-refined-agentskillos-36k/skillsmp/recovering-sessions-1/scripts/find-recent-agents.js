#!/usr/bin/env node
/**
 * Discover agent logs from recent Claude Code sessions
 *
 * Usage:
 *   node find-recent-agents.js [options]
 *
 * Options:
 *   --minutes N      Find agents active in last N minutes (default: 180)
 *   --project PATH   Specify project path (default: current directory)
 *   --json           Output as JSON
 *   --help           Show help
 *
 * Examples:
 *   node find-recent-agents.js
 *   node find-recent-agents.js --minutes 60
 *   node find-recent-agents.js --project /Users/name/dev/project
 *   node find-recent-agents.js --json | jq '.[] | .id'
 */

import { readdir, stat } from 'fs/promises';
import { homedir } from 'os';
import { join, resolve } from 'path';

const DEFAULT_MINUTES = 180; // 3 hours

/**
 * Parse command line arguments
 */
function parseArgs() {
  const args = process.argv.slice(2);
  const options = {
    minutes: DEFAULT_MINUTES,
    project: process.cwd(),
    json: false,
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
      case '--json':
        options.json = true;
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
 * Get Claude Code log directory for a project
 */
function getLogDirectory(projectPath) {
  // Transform project path to log directory name
  // /Users/name/dev/project -> -Users-name-dev-project
  const sanitized = projectPath.replace(/\//g, '-').replace(/^-/, '');
  return join(homedir(), '.claude', 'projects', sanitized);
}

/**
 * Find recent agent logs
 */
async function findRecentAgents(projectPath, minutes) {
  const logDir = getLogDirectory(projectPath);
  const cutoff = Date.now() - (minutes * 60 * 1000);

  let files;
  try {
    files = await readdir(logDir);
  } catch (error) {
    if (error.code === 'ENOENT') {
      return { logDir, agents: [], error: 'Log directory not found' };
    }
    throw error;
  }

  const agentLogs = [];

  for (const file of files) {
    // Only process agent-*.jsonl files
    if (!file.startsWith('agent-') || !file.endsWith('.jsonl')) {
      continue;
    }

    const filePath = join(logDir, file);
    const stats = await stat(filePath);

    // Check if modified within time window
    if (stats.mtimeMs > cutoff) {
      // Extract agent ID from filename: agent-{8-char-id}.jsonl
      const match = file.match(/agent-([a-f0-9]+)\.jsonl/);
      const id = match ? match[1] : file;

      agentLogs.push({
        id,
        path: filePath,
        filename: file,
        size: stats.size,
        sizeFormatted: formatSize(stats.size),
        modified: new Date(stats.mtimeMs),
        modifiedRelative: formatRelativeTime(stats.mtimeMs),
        lines: await countLines(filePath)
      });
    }
  }

  // Sort by modification time (most recent first)
  agentLogs.sort((a, b) => b.modified - a.modified);

  return { logDir, agents: agentLogs };
}

/**
 * Count lines in a file (approximate for large files)
 */
async function countLines(filePath) {
  try {
    const { createReadStream } = await import('fs');
    return new Promise((resolve) => {
      let count = 0;
      createReadStream(filePath)
        .on('data', (chunk) => {
          for (let i = 0; i < chunk.length; i++) {
            if (chunk[i] === 10) count++; // newline character
          }
        })
        .on('end', () => resolve(count))
        .on('error', () => resolve(0));
    });
  } catch {
    return 0;
  }
}

/**
 * Format file size for display
 */
function formatSize(bytes) {
  if (bytes < 1024) return `${bytes}B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)}KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)}MB`;
}

/**
 * Format relative time for display
 */
function formatRelativeTime(timestamp) {
  const now = Date.now();
  const diff = now - timestamp;

  if (diff < 60000) return 'just now';
  if (diff < 3600000) return `${Math.floor(diff / 60000)} minutes ago`;
  if (diff < 86400000) return `${Math.floor(diff / 3600000)} hours ago`;
  return `${Math.floor(diff / 86400000)} days ago`;
}

/**
 * Display help message
 */
function showHelp() {
  console.log(`
Discover agent logs from recent Claude Code sessions

Usage:
  node find-recent-agents.js [options]

Options:
  --minutes N      Find agents active in last N minutes (default: 180)
  --project PATH   Specify project path (default: current directory)
  --json           Output as JSON
  --help           Show this help message

Examples:
  node find-recent-agents.js
  node find-recent-agents.js --minutes 60
  node find-recent-agents.js --project /Users/name/dev/project
  node find-recent-agents.js --json | jq '.[] | .id'
`);
}

/**
 * Main entry point
 */
async function main() {
  const options = parseArgs();

  if (options.help) {
    showHelp();
    process.exit(0);
  }

  const result = await findRecentAgents(options.project, options.minutes);

  if (options.json) {
    console.log(JSON.stringify(result.agents, null, 2));
    return;
  }

  // Human-readable output
  console.log(`=== Recent Agent Logs ===`);
  console.log(`Project: ${options.project}`);
  console.log(`Log Directory: ${result.logDir}`);
  console.log(`Time Window: Last ${options.minutes} minutes`);
  console.log();

  if (result.error) {
    console.log(`Error: ${result.error}`);
    process.exit(1);
  }

  if (result.agents.length === 0) {
    console.log('No recent agent logs found');
    return;
  }

  console.log(`Found ${result.agents.length} agent log(s):`);
  console.log();

  for (const agent of result.agents) {
    console.log(`Agent: ${agent.id}`);
    console.log(`  File: ${agent.filename}`);
    console.log(`  Size: ${agent.sizeFormatted} (${agent.lines} lines)`);
    console.log(`  Modified: ${agent.modifiedRelative}`);
    console.log(`  Path: ${agent.path}`);
    console.log();
  }

  // Summary for quick copy
  console.log('=== Agent IDs (for filtering) ===');
  console.log(result.agents.map(a => a.id).join(', '));
}

main().catch(error => {
  console.error('Error:', error.message);
  process.exit(1);
});
