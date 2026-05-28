#!/usr/bin/env node

/**
 * Workflow Session Analyzer Script
 *
 * Analyzes Claude Code session transcripts to identify workflow improvements,
 * inefficiencies, and optimization opportunities.
 *
 * Usage:
 *   node analyze-session.js                    # List available sessions
 *   node analyze-session.js YYYYMMDD           # Analyze specific date
 *   node analyze-session.js YYYYMMDD sessionId # Analyze specific session
 *   node analyze-session.js --help             # Show help
 *
 * Examples:
 *   node analyze-session.js
 *   node analyze-session.js 20251012
 *   node analyze-session.js 20251012 c6d23edd
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

// Constants
const LOGS_DIR = path.join(process.cwd(), '.claude', 'logs');
const HOME_DIR = os.homedir();

// Color codes for terminal output
const colors = {
  reset: '\x1b[0m',
  bold: '\x1b[1m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  cyan: '\x1b[36m'
};

/**
 * Print colored output
 */
function print(message, color = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

/**
 * Print error and exit
 */
function error(message) {
  print(`❌ ERROR: ${message}`, 'red');
  process.exit(1);
}

/**
 * Print help message
 */
function showHelp() {
  print('Workflow Session Analyzer', 'bold');
  print('');
  print('Analyzes Claude Code session transcripts from .claude/logs/', 'cyan');
  print('');
  print('Usage:', 'bold');
  print('  node analyze-session.js                    # List available sessions');
  print('  node analyze-session.js YYYYMMDD           # Analyze all sessions from date');
  print('  node analyze-session.js YYYYMMDD sessionId # Analyze specific session');
  print('  node analyze-session.js --help             # Show this help');
  print('');
  print('Examples:', 'bold');
  print('  node analyze-session.js', 'green');
  print('  node analyze-session.js 20251012', 'green');
  print('  node analyze-session.js 20251012 c6d23edd', 'green');
  process.exit(0);
}

/**
 * Format date for display (YYYYMMDD -> Month DD, YYYY)
 */
function formatDate(dateStr) {
  const year = dateStr.substring(0, 4);
  const month = dateStr.substring(4, 6);
  const day = dateStr.substring(6, 8);
  const date = new Date(year, parseInt(month) - 1, day);
  return date.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
}

/**
 * List available session dates
 */
function listAvailableSessions() {
  if (!fs.existsSync(LOGS_DIR)) {
    error(`Logs directory not found: ${LOGS_DIR}`);
  }

  const entries = fs.readdirSync(LOGS_DIR, { withFileTypes: true });
  const dateDirs = entries
    .filter(entry => entry.isDirectory() && /^\d{8}$/.test(entry.name))
    .map(entry => entry.name)
    .sort()
    .reverse();

  if (dateDirs.length === 0) {
    error('No session logs found. Check if logging is enabled.');
  }

  print('Available Claude Code session logs:', 'bold');
  print('');
  dateDirs.forEach((dateDir, index) => {
    print(`  ${index + 1}. ${formatDate(dateDir)} (${dateDir})`, 'cyan');
  });
  print('');
  print('Run with date to analyze:', 'yellow');
  print(`  node analyze-session.js ${dateDirs[0]}`, 'green');
}

/**
 * Get session info from directory
 */
function getSessionsInDirectory(dateDir) {
  const dirPath = path.join(LOGS_DIR, dateDir);

  if (!fs.existsSync(dirPath)) {
    error(`Directory not found: ${dirPath}`);
  }

  const files = fs.readdirSync(dirPath);
  const sessions = new Map();

  // Group files by session ID
  files.forEach(file => {
    const match = file.match(/transcript_(?:subagent_)?([a-f0-9]+)_(\d{8})_(\d{6})\.json/);
    if (match) {
      const [, sessionId, date, time] = match;
      const isSubagent = file.includes('subagent');

      if (!sessions.has(sessionId)) {
        sessions.set(sessionId, {
          id: sessionId,
          mainFile: null,
          subagentFiles: [],
          startTime: time
        });
      }

      const session = sessions.get(sessionId);
      if (isSubagent) {
        session.subagentFiles.push(file);
      } else {
        session.mainFile = file;
      }
    }
  });

  return Array.from(sessions.values()).sort((a, b) =>
    a.startTime.localeCompare(b.startTime)
  );
}

/**
 * Analyze specific session
 */
function analyzeSession(dateDir, sessionId) {
  const sessions = getSessionsInDirectory(dateDir);
  const session = sessions.find(s => s.id === sessionId);

  if (!session) {
    error(`Session ${sessionId} not found in ${dateDir}`);
  }

  print(`\nAnalyzing session: ${session.id}`, 'bold');
  print(`Date: ${formatDate(dateDir)}`, 'cyan');
  print(`Main transcript: ${session.mainFile}`, 'green');
  print(`Subagent transcripts: ${session.subagentFiles.length}`, 'green');
  print('');

  if (session.subagentFiles.length > 0) {
    print('Subagent transcripts:', 'bold');
    session.subagentFiles.forEach(file => {
      print(`  - ${file}`, 'cyan');
    });
    print('');
  }

  // TODO: Implement actual analysis logic
  print('Analysis complete! (Implementation pending)', 'yellow');
  print('');
  print('Next steps:', 'bold');
  print('  - Add transcript parsing logic');
  print('  - Implement workflow analysis');
  print('  - Generate metrics and recommendations');
}

/**
 * List sessions for a specific date
 */
function listSessionsForDate(dateDir) {
  const sessions = getSessionsInDirectory(dateDir);

  if (sessions.length === 0) {
    error(`No sessions found for ${dateDir}`);
  }

  print(`\nSessions for ${formatDate(dateDir)}:`, 'bold');
  print('');

  sessions.forEach((session, index) => {
    print(`  ${index + 1}. Session ${session.id}`, 'cyan');
    print(`     Time: ${session.startTime.substring(0, 2)}:${session.startTime.substring(2, 4)}:${session.startTime.substring(4, 6)}`, 'yellow');
    print(`     Main: ${session.mainFile || 'N/A'}`, 'green');
    print(`     Subagents: ${session.subagentFiles.length}`, 'green');
    print('');
  });

  print('Run with session ID to analyze:', 'yellow');
  print(`  node analyze-session.js ${dateDir} ${sessions[0].id}`, 'green');
}

/**
 * Main entry point
 */
function main() {
  const args = process.argv.slice(2);

  // Show help
  if (args.includes('--help') || args.includes('-h')) {
    showHelp();
  }

  // No arguments - list available sessions
  if (args.length === 0) {
    listAvailableSessions();
    return;
  }

  const dateArg = args[0];

  // Validate date format
  if (!/^\d{8}$/.test(dateArg)) {
    error(`Invalid date format: ${dateArg}. Expected YYYYMMDD (e.g., 20251012)`);
  }

  // If session ID provided, analyze specific session
  if (args.length === 2) {
    const sessionId = args[1];
    analyzeSession(dateArg, sessionId);
    return;
  }

  // Otherwise list sessions for the date
  listSessionsForDate(dateArg);
}

// Run the script
main();
