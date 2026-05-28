#!/usr/bin/env node
/**
 * Analyze a single agent log for session recovery
 *
 * Usage:
 *   node analyze-agent-log.js <log-path> [options]
 *
 * Options:
 *   --json           Output as JSON
 *   --verbose        Include additional details
 *   --help           Show help
 *
 * Examples:
 *   node analyze-agent-log.js ~/.claude/projects/.../agent-a91845a.jsonl
 *   node analyze-agent-log.js agent.jsonl --json
 *   node analyze-agent-log.js agent.jsonl --verbose
 */

import { readFile, stat } from 'fs/promises';
import { basename, resolve } from 'path';

/**
 * Parse command line arguments
 */
function parseArgs() {
  const args = process.argv.slice(2);
  const options = {
    logPath: null,
    json: false,
    verbose: false,
    help: false
  };

  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case '--json':
        options.json = true;
        break;
      case '--verbose':
      case '-v':
        options.verbose = true;
        break;
      case '--help':
      case '-h':
        options.help = true;
        break;
      default:
        if (!args[i].startsWith('-')) {
          options.logPath = resolve(args[i]);
        }
    }
  }

  return options;
}

/**
 * Analyze an agent log file
 */
async function analyzeLog(logPath) {
  const content = await readFile(logPath, 'utf-8');
  const lines = content.trim().split('\n').filter(l => l.trim());
  const stats = await stat(logPath);

  const result = {
    path: logPath,
    filename: basename(logPath),
    agentId: extractAgentId(basename(logPath)),
    totalMessages: lines.length,
    size: stats.size,
    modified: new Date(stats.mtimeMs),
    filesCreated: [],
    filesModified: [],
    filesRead: [],
    bashCommands: [],
    toolUseCounts: {},
    testResults: null,
    status: 'UNKNOWN',
    errors: [],
    warnings: [],
    taskId: null,
    lastActivityType: null
  };

  // Parse each line
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    try {
      const entry = JSON.parse(line);
      processEntry(entry, result, i === lines.length - 1);
    } catch (e) {
      // Track malformed lines
      result.warnings.push(`Line ${i + 1}: Malformed JSON`);
    }
  }

  // Determine final status
  result.status = determineStatus(result, lines);

  // Deduplicate arrays
  result.filesCreated = [...new Set(result.filesCreated)];
  result.filesModified = [...new Set(result.filesModified)];
  result.filesRead = [...new Set(result.filesRead)];

  return result;
}

/**
 * Extract agent ID from filename
 */
function extractAgentId(filename) {
  const match = filename.match(/agent-([a-f0-9]+)\.jsonl/);
  return match ? match[1] : filename.replace('.jsonl', '');
}

/**
 * Process a single log entry
 */
function processEntry(entry, result, isLast) {
  const content = entry.message?.content;
  if (!Array.isArray(content)) return;

  for (const block of content) {
    if (block.type === 'tool_use') {
      // Count tool usage
      const toolName = block.name;
      result.toolUseCounts[toolName] = (result.toolUseCounts[toolName] || 0) + 1;

      // Extract file paths
      if (toolName === 'Write' && block.input?.file_path) {
        result.filesCreated.push(block.input.file_path);
      }
      if (toolName === 'Edit' && block.input?.file_path) {
        result.filesModified.push(block.input.file_path);
      }
      if (toolName === 'Read' && block.input?.file_path) {
        result.filesRead.push(block.input.file_path);
      }
      if (toolName === 'Bash' && block.input?.command) {
        result.bashCommands.push(block.input.command);
      }

      if (isLast) {
        result.lastActivityType = `tool_use:${toolName}`;
      }
    }

    if (block.type === 'text' && block.text) {
      const text = block.text;

      // Look for task IDs
      const taskMatch = text.match(/TASK-\d+\.\d+/);
      if (taskMatch && !result.taskId) {
        result.taskId = taskMatch[0];
      }

      // Look for test results
      const testMatch = text.match(/(\d+)\s+(passed|tests?\s+passed)/i);
      if (testMatch) {
        result.testResults = testMatch[0];
      }

      const failedMatch = text.match(/(\d+)\s+failed/i);
      if (failedMatch && result.testResults) {
        result.testResults += `, ${failedMatch[0]}`;
      }

      // Look for errors
      const errorPatterns = [
        /error:\s*.+/i,
        /failed:\s*.+/i,
        /exception:\s*.+/i,
        /TypeError:\s*.+/i,
        /ReferenceError:\s*.+/i,
        /SyntaxError:\s*.+/i
      ];

      for (const pattern of errorPatterns) {
        const match = text.match(pattern);
        if (match) {
          result.errors.push(match[0].slice(0, 200));
        }
      }

      if (isLast) {
        result.lastActivityType = 'text';
      }
    }
  }
}

/**
 * Determine agent completion status
 */
function determineStatus(result, lines) {
  // Check last 10 lines for completion markers
  const lastLines = lines.slice(-10).join(' ').toLowerCase();

  // Success markers
  if (lastLines.includes('complete') ||
      lastLines.includes('successfully') ||
      lastLines.includes('finished') ||
      lastLines.includes('task done')) {
    return 'COMPLETE';
  }

  // Error markers in final lines
  if (result.errors.length > 0) {
    const lastError = result.errors[result.errors.length - 1];
    if (lastLines.includes(lastError.toLowerCase())) {
      return 'FAILED';
    }
  }

  // Check for uncaught errors in final lines
  if (lastLines.includes('error') ||
      lastLines.includes('failed') ||
      lastLines.includes('exception')) {
    // But not test failure reports (which include "X failed")
    if (!lastLines.includes('passed') && !lastLines.includes('test')) {
      return 'FAILED';
    }
  }

  // Large log with file operations but no completion = likely crashed
  if (result.totalMessages > 50 &&
      result.filesCreated.length > 0 &&
      result.size > 10000) {
    return 'IN_PROGRESS';
  }

  // Small log with no file operations = not started
  if (result.totalMessages < 10 &&
      result.filesCreated.length === 0 &&
      result.filesModified.length === 0) {
    return 'NOT_STARTED';
  }

  return 'UNKNOWN';
}

/**
 * Format size for display
 */
function formatSize(bytes) {
  if (bytes < 1024) return `${bytes}B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)}KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)}MB`;
}

/**
 * Display help message
 */
function showHelp() {
  console.log(`
Analyze a single agent log for session recovery

Usage:
  node analyze-agent-log.js <log-path> [options]

Options:
  --json           Output as JSON
  --verbose, -v    Include additional details
  --help, -h       Show this help message

Examples:
  node analyze-agent-log.js agent-a91845a.jsonl
  node analyze-agent-log.js ~/.claude/projects/.../agent.jsonl --json
  node analyze-agent-log.js agent.jsonl --verbose

Output includes:
  - Agent ID and basic stats
  - Files created/modified
  - Test results (if any)
  - Errors encountered
  - Completion status determination
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

  if (!options.logPath) {
    console.error('Error: Log path required');
    console.error('Usage: node analyze-agent-log.js <log-path> [options]');
    process.exit(1);
  }

  const result = await analyzeLog(options.logPath);

  if (options.json) {
    console.log(JSON.stringify(result, null, 2));
    return;
  }

  // Human-readable output
  console.log(`=== Agent Log Analysis ===`);
  console.log(`Agent ID: ${result.agentId}`);
  if (result.taskId) {
    console.log(`Task: ${result.taskId}`);
  }
  console.log(`Status: ${result.status}`);
  console.log();

  console.log(`=== Basic Info ===`);
  console.log(`Messages: ${result.totalMessages}`);
  console.log(`Size: ${formatSize(result.size)}`);
  console.log(`Modified: ${result.modified.toISOString()}`);
  console.log();

  console.log(`=== Tool Usage ===`);
  for (const [tool, count] of Object.entries(result.toolUseCounts)) {
    console.log(`  ${tool}: ${count}`);
  }
  console.log();

  if (result.filesCreated.length > 0) {
    console.log(`=== Files Created (${result.filesCreated.length}) ===`);
    for (const file of result.filesCreated) {
      console.log(`  ${file}`);
    }
    console.log();
  }

  if (result.filesModified.length > 0) {
    console.log(`=== Files Modified (${result.filesModified.length}) ===`);
    for (const file of result.filesModified) {
      console.log(`  ${file}`);
    }
    console.log();
  }

  if (result.testResults) {
    console.log(`=== Test Results ===`);
    console.log(`  ${result.testResults}`);
    console.log();
  }

  if (result.errors.length > 0) {
    console.log(`=== Errors (${result.errors.length}) ===`);
    for (const error of result.errors.slice(0, 5)) {
      console.log(`  ${error}`);
    }
    if (result.errors.length > 5) {
      console.log(`  ... and ${result.errors.length - 5} more`);
    }
    console.log();
  }

  if (options.verbose) {
    if (result.filesRead.length > 0) {
      console.log(`=== Files Read (${result.filesRead.length}) ===`);
      for (const file of result.filesRead.slice(0, 10)) {
        console.log(`  ${file}`);
      }
      if (result.filesRead.length > 10) {
        console.log(`  ... and ${result.filesRead.length - 10} more`);
      }
      console.log();
    }

    if (result.bashCommands.length > 0) {
      console.log(`=== Bash Commands (${result.bashCommands.length}) ===`);
      for (const cmd of result.bashCommands.slice(0, 5)) {
        console.log(`  ${cmd.slice(0, 80)}${cmd.length > 80 ? '...' : ''}`);
      }
      console.log();
    }

    if (result.warnings.length > 0) {
      console.log(`=== Warnings ===`);
      for (const warning of result.warnings.slice(0, 5)) {
        console.log(`  ${warning}`);
      }
      console.log();
    }
  }

  console.log(`=== Summary ===`);
  console.log(`Status: ${result.status}`);
  console.log(`Files Created: ${result.filesCreated.length}`);
  console.log(`Files Modified: ${result.filesModified.length}`);
  console.log(`Errors: ${result.errors.length}`);
}

main().catch(error => {
  console.error('Error:', error.message);
  process.exit(1);
});
