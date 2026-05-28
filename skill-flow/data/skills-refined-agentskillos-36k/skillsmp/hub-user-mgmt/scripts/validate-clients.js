#!/usr/bin/env node
/**
 * Client Configuration Validator
 * Pre-deploy validation for multi-user client configs
 *
 * Usage:
 *   node validate-clients.js [--dir <clients-dir>]
 *
 * Exit codes:
 *   0 - All configs valid
 *   1 - One or more configs invalid
 *   2 - Script error
 */

const fs = require('fs').promises;
const path = require('path');

// ============================================================
// ADAPT THESE TO YOUR SETUP
// ============================================================

// Valid usernames for your hub (Götterboten theme)
const VALID_USERS = [
  'hermes',    // Admin
  'iris',
  'mercury',
  'thoth',
  'gabriel',
  'angelos',
  'arke',
  'jibril'
];

// Reserved names (cannot be used)
const RESERVED_NAMES = ['admin', 'root', 'system', 'hub'];

// Folders to skip during validation
const SKIP_FOLDERS = ['_template'];

// Required files in each client folder
const REQUIRED_FILES = ['client.config.json'];

// Optional companion files (warning if missing)
const COMPANION_FILES = ['README.md'];

// ============================================================
// VALIDATION LOGIC
// ============================================================

const colors = {
  reset: '\x1b[0m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  cyan: '\x1b[36m'
};

/**
 * Validate a single client config
 */
function validateConfig(config, dirName) {
  const errors = [];
  const warnings = [];

  // Check required fields
  if (!config.username) {
    errors.push('Missing required field: username');
  } else {
    // Validate username
    if (typeof config.username !== 'string') {
      errors.push('username must be a string');
    } else if (!/^[a-z][a-z0-9_-]*$/.test(config.username)) {
      errors.push('username must be lowercase, start with letter, contain only a-z, 0-9, _, -');
    }

    // Check if reserved
    if (RESERVED_NAMES.includes(config.username)) {
      errors.push(`'${config.username}' is a reserved name`);
    }

    // Check if in valid users list
    if (!VALID_USERS.includes(config.username)) {
      warnings.push(`'${config.username}' is not in the standard user pool`);
    }
  }

  // Check role
  if (config.role && !['admin', 'user'].includes(config.role)) {
    errors.push(`Invalid role: ${config.role} (must be 'admin' or 'user')`);
  }

  // Check tools config if present
  if (config.tools) {
    if (config.tools.mode && !['whitelist', 'blacklist'].includes(config.tools.mode)) {
      errors.push(`Invalid tools.mode: ${config.tools.mode}`);
    }
    if (config.tools.allowed && !Array.isArray(config.tools.allowed)) {
      errors.push('tools.allowed must be an array');
    }
    if (config.tools.denied && !Array.isArray(config.tools.denied)) {
      errors.push('tools.denied must be an array');
    }
  }

  return { errors, warnings };
}

/**
 * Validate all client configurations in a directory
 */
async function validateAllClients(clientsDir) {
  const results = [];
  const seenUsernames = new Set();

  console.log(`\n${colors.cyan}🔍 Validating client configs in: ${clientsDir}${colors.reset}\n`);

  // Check if directory exists
  try {
    await fs.access(clientsDir);
  } catch {
    console.error(`${colors.red}❌ Clients directory not found: ${clientsDir}${colors.reset}`);
    return { valid: false, results: [{ error: 'Directory not found' }] };
  }

  // Get all subdirectories
  const entries = await fs.readdir(clientsDir, { withFileTypes: true });
  const clientDirs = entries.filter(e =>
    e.isDirectory() &&
    !e.name.startsWith('_') &&
    !e.name.startsWith('.') &&
    !SKIP_FOLDERS.includes(e.name)
  );

  if (clientDirs.length === 0) {
    console.log(`${colors.yellow}⚠️  No client directories found${colors.reset}`);
    return { valid: true, results: [] };
  }

  for (const dir of clientDirs) {
    const configPath = path.join(clientsDir, dir.name, 'client.config.json');
    const result = {
      directory: dir.name,
      configPath,
      valid: true,
      errors: [],
      warnings: []
    };

    // Check if config file exists
    try {
      await fs.access(configPath);
    } catch {
      result.valid = false;
      result.errors.push('Missing client.config.json');
      results.push(result);
      continue;
    }

    // Read and parse config
    let config;
    try {
      const raw = await fs.readFile(configPath, 'utf8');
      config = JSON.parse(raw);
    } catch (err) {
      result.valid = false;
      result.errors.push(`JSON parse error: ${err.message}`);
      results.push(result);
      continue;
    }

    // Validate config
    const validation = validateConfig(config, dir.name);
    result.errors.push(...validation.errors);
    result.warnings.push(...validation.warnings);

    if (validation.errors.length > 0) {
      result.valid = false;
    }

    // Check for duplicate usernames
    if (config.username) {
      if (seenUsernames.has(config.username)) {
        result.valid = false;
        result.errors.push(`Duplicate username: ${config.username}`);
      } else {
        seenUsernames.add(config.username);
      }
    }

    // Check for companion files
    for (const file of COMPANION_FILES) {
      const filePath = path.join(clientsDir, dir.name, file);
      try {
        await fs.access(filePath);
      } catch {
        result.warnings.push(`Missing companion file: ${file}`);
      }
    }

    results.push(result);
  }

  // Print results
  let hasErrors = false;
  for (const result of results) {
    const icon = result.valid ? `${colors.green}✓${colors.reset}` : `${colors.red}✗${colors.reset}`;
    console.log(`${icon} ${result.directory}`);

    for (const error of result.errors) {
      console.log(`  ${colors.red}ERROR: ${error}${colors.reset}`);
      hasErrors = true;
    }
    for (const warning of result.warnings) {
      console.log(`  ${colors.yellow}WARN: ${warning}${colors.reset}`);
    }
  }

  // Summary
  const validCount = results.filter(r => r.valid).length;
  const invalidCount = results.filter(r => !r.valid).length;

  console.log(`\n${colors.cyan}Summary:${colors.reset}`);
  console.log(`  Total: ${results.length}`);
  console.log(`  ${colors.green}Valid: ${validCount}${colors.reset}`);
  if (invalidCount > 0) {
    console.log(`  ${colors.red}Invalid: ${invalidCount}${colors.reset}`);
  }

  return { valid: !hasErrors, results };
}

// CLI Entry point
async function main() {
  const args = process.argv.slice(2);

  // Default to clients/ relative to repo root
  const scriptDir = path.dirname(__filename);
  let clientsDir = path.resolve(scriptDir, '../../../../clients');

  // Parse --dir argument
  const dirIndex = args.indexOf('--dir');
  if (dirIndex !== -1 && args[dirIndex + 1]) {
    clientsDir = path.resolve(args[dirIndex + 1]);
  }

  try {
    const { valid } = await validateAllClients(clientsDir);
    process.exit(valid ? 0 : 1);
  } catch (err) {
    console.error(`${colors.red}Script error: ${err.message}${colors.reset}`);
    process.exit(2);
  }
}

main();

module.exports = { validateAllClients };
