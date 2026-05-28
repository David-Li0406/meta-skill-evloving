#!/usr/bin/env node
/**
 * Shared utilities for project-index scripts
 * Reduces code duplication across modules
 */

import { promises as fs } from 'fs';
import path from 'path';

/** @type {number} Default max lines to read from a file */
export const DEFAULT_MAX_LINES = 100;

/** @type {number} Stale threshold in minutes for crash detection */
export const CRASH_THRESHOLD_MINUTES = 35;

/** @type {number} Default LLM timeout in ms (30 minutes) */
export const DEFAULT_TIMEOUT = 1800000;

/** @type {number} Default concurrency limit */
export const DEFAULT_CONCURRENCY = 6;

/**
 * Read file safely with line limit
 * @param {string} filePath - Absolute path to file
 * @param {number} [maxLines=100] - Maximum lines to read
 * @returns {Promise<string|null>} File content or null on error
 */
export async function readFileSafe(filePath, maxLines = DEFAULT_MAX_LINES) {
  try {
    const content = await fs.readFile(filePath, 'utf-8');
    const lines = content.split('\n');
    if (lines.length > maxLines) {
      return lines.slice(0, maxLines).join('\n') + `\n... (${lines.length - maxLines} more lines)`;
    }
    return content;
  } catch {
    return null;
  }
}

/**
 * Load .stale-config.json from project root
 * @param {string} cwd - Project root directory
 * @returns {Promise<object>} Configuration object (empty if not found)
 */
export async function loadConfig(cwd) {
  const configFile = path.join(cwd, '.project-index', '.stale-config.json');
  try {
    const content = await fs.readFile(configFile, 'utf-8');
    return JSON.parse(content);
  } catch {
    return {};
  }
}

/**
 * Check if a path matches any glob pattern
 * @param {string} relativePath - Path to check (relative to root)
 * @param {string[]} patterns - Glob patterns to match
 * @returns {boolean} True if matches any pattern
 */
export function matchesPattern(relativePath, patterns) {
  if (!patterns || patterns.length === 0) return false;

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
 * Check if a path should be processed based on include/ignore config
 * @param {string} relativePath - Path to check (relative to root)
 * @param {{include?: string[], ignore?: string[]}} config - Config object
 * @returns {boolean} True if should be processed
 */
export function shouldProcess(relativePath, config) {
  const { include, ignore } = config;

  // If include is defined, path must match at least one include pattern
  if (include && include.length > 0) {
    if (!matchesPattern(relativePath, include)) {
      return false;
    }
  }

  // Check ignore patterns
  if (ignore && ignore.length > 0) {
    if (matchesPattern(relativePath, ignore)) {
      return false;
    }
  }

  return true;
}

/**
 * Read JSON file safely
 * @param {string} filePath - Path to JSON file
 * @param {*} [defaultValue=null] - Default value on error
 * @returns {Promise<*>} Parsed JSON or default value
 */
export async function readJsonSafe(filePath, defaultValue = null) {
  try {
    const content = await fs.readFile(filePath, 'utf-8');
    return JSON.parse(content);
  } catch {
    return defaultValue;
  }
}

/**
 * Write JSON file with formatting
 * @param {string} filePath - Path to write
 * @param {*} data - Data to serialize
 * @returns {Promise<boolean>} Success status
 */
export async function writeJsonSafe(filePath, data) {
  try {
    await fs.writeFile(filePath, JSON.stringify(data, null, 2));
    return true;
  } catch {
    return false;
  }
}

/**
 * Delete file silently (no error on missing file)
 * @param {string} filePath - Path to delete
 * @returns {Promise<boolean>} True if deleted, false if not found or error
 */
export async function unlinkSafe(filePath) {
  try {
    await fs.unlink(filePath);
    return true;
  } catch {
    return false;
  }
}

/**
 * Get file modification time
 * @param {string} filePath - Path to file
 * @returns {Promise<Date|null>} Modification time or null
 */
export async function getMtime(filePath) {
  try {
    const stat = await fs.stat(filePath);
    return stat.mtime;
  } catch {
    return null;
  }
}

/**
 * Check if file exists
 * @param {string} filePath - Path to check
 * @returns {Promise<boolean>}
 */
export async function fileExists(filePath) {
  try {
    await fs.access(filePath);
    return true;
  } catch {
    return false;
  }
}

/**
 * Archive result to history file with limit
 * @param {string} historyPath - Path to history JSON file
 * @param {object} result - Result to archive
 * @param {number} [maxEntries=10] - Maximum entries to keep
 * @returns {Promise<boolean>} Success status
 */
export async function archiveToHistory(historyPath, result, maxEntries = 10) {
  try {
    let history = await readJsonSafe(historyPath, []);

    history.push({
      ...result,
      archivedAt: new Date().toISOString()
    });

    if (history.length > maxEntries) {
      history = history.slice(-maxEntries);
    }

    return await writeJsonSafe(historyPath, history);
  } catch {
    return false;
  }
}

/**
 * Parse CLI arguments into options object
 * @param {string[]} args - process.argv.slice(2)
 * @param {object} defaults - Default values
 * @returns {object} Parsed options
 */
export function parseArgs(args, defaults = {}) {
  const options = { ...defaults };

  for (const arg of args) {
    if (arg.startsWith('--')) {
      const [key, value] = arg.slice(2).split('=');
      const camelKey = key.replace(/-([a-z])/g, (_, c) => c.toUpperCase());

      if (value === undefined) {
        // --flag (boolean)
        options[camelKey] = true;
      } else if (value === 'true') {
        options[camelKey] = true;
      } else if (value === 'false') {
        options[camelKey] = false;
      } else if (/^\d+$/.test(value)) {
        options[camelKey] = parseInt(value, 10);
      } else {
        options[camelKey] = value;
      }
    } else if (!arg.startsWith('-')) {
      // Positional argument
      options._ = options._ || [];
      options._.push(arg);
    }
  }

  return options;
}

/**
 * Format duration in human-readable form
 * @param {number} ms - Duration in milliseconds
 * @returns {string} Formatted duration
 */
export function formatDuration(ms) {
  if (ms < 1000) return `${ms}ms`;
  if (ms < 60000) return `${(ms / 1000).toFixed(1)}s`;
  if (ms < 3600000) return `${(ms / 60000).toFixed(1)}min`;
  return `${(ms / 3600000).toFixed(1)}h`;
}

/**
 * Create a simple logger
 * @param {string} logFile - Path to log file
 * @param {boolean} [silent=false] - Suppress console output
 * @returns {object} Logger with log() method
 */
export function createLogger(logFile, silent = false) {
  return {
    async log(msg) {
      const timestamp = new Date().toISOString().slice(11, 19);
      const line = `[${timestamp}] ${msg}\n`;
      await fs.appendFile(logFile, line).catch(() => { });
      if (!silent) {
        console.log(line.trim());
      }
    }
  };
}

/**
 * Find project root by looking for .git, .stale-config.json, or package.json
 * @param {string} startPath - Directory to start searching from
 * @returns {Promise<string>} Project root path (or startPath if not found)
 */
export async function findProjectRoot(startPath) {
  const markers = ['.git', '.stale-config.json', 'package.json'];
  let current = path.resolve(startPath);
  const root = path.parse(current).root;

  while (current !== root) {
    for (const marker of markers) {
      try {
        await fs.access(path.join(current, marker));
        return current;
      } catch {
        // Continue searching
      }
    }
    current = path.dirname(current);
  }

  // Fallback to start path if no marker found
  return path.resolve(startPath);
}
