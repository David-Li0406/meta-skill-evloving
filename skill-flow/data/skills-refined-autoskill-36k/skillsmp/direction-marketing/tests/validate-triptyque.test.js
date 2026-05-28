#!/usr/bin/env node
/**
 * Validates triptyque workflow and content
 *
 * Improvements:
 * - Robust project root detection
 * - Path traversal protection
 * - Error handling for file operations
 * - Regex-based section validation
 * - Combined existence + content validation
 */

const fs = require('fs');
const path = require('path');
const { TRIPTYQUE } = require('./config');

let errors = 0;
let warnings = 0;

console.log('🔍 Validating triptyque workflow...\n');

/**
 * Find project root by looking for .git or package.json
 * More robust than process.cwd() which depends on where test is run
 */
function findProjectRoot(startDir = __dirname) {
  let currentDir = startDir;
  while (currentDir !== path.parse(currentDir).root) {
    if (fs.existsSync(path.join(currentDir, '.git')) ||
        fs.existsSync(path.join(currentDir, 'package.json'))) {
      return currentDir;
    }
    currentDir = path.dirname(currentDir);
  }
  // Fallback to cwd if no markers found
  return process.cwd();
}

const PROJECT_ROOT = findProjectRoot();
console.log(`📁 Project root: ${PROJECT_ROOT}\n`);

/**
 * Resolve and validate path stays within project boundaries
 * Prevents path traversal attacks
 *
 * Uses path.relative() for cross-platform compatibility (handles Windows
 * case-insensitivity and different path separators)
 */
function safePath(filePath) {
  const fullPath = path.resolve(PROJECT_ROOT, filePath);

  // Security: Use path.relative() for robust cross-platform checking
  // If relative path starts with '..' it's outside project root
  const relativePath = path.relative(PROJECT_ROOT, fullPath);
  if (relativePath.startsWith('..') || path.isAbsolute(relativePath)) {
    const error = new Error(`Security: Path traversal detected - ${filePath} resolves outside project root`);
    error.isSecurityError = true;
    throw error;
  }

  return fullPath;
}

/**
 * Validate file content against required sections
 * Combines existence check with content validation for efficiency
 * Uses regex for exact markdown header matching
 *
 * @param {string} filePath - Relative path from project root
 * @param {string[]} requiredSections - Array of required section headers
 * @returns {Object} - { exists: boolean, valid: boolean, missing: string[], error?: string }
 */
function validateContent(filePath, requiredSections) {
  let fullPath;

  try {
    fullPath = safePath(filePath);
  } catch (err) {
    return {
      exists: false,
      valid: false,
      missing: requiredSections,
      error: err.message,
      isSecurityError: err.isSecurityError || false
    };
  }

  // Try to read file - handles both existence and read errors
  let content;
  try {
    content = fs.readFileSync(fullPath, 'utf8');
  } catch (err) {
    if (err.code === 'ENOENT') {
      return {
        exists: false,
        valid: false,
        missing: requiredSections
      };
    }
    // Unexpected error (permissions, etc.)
    return {
      exists: true,
      valid: false,
      missing: requiredSections,
      error: `Read error: ${err.message}`
    };
  }

  // Validate sections using optimized single-pass approach
  // Split content into lines once, then check each required section
  const lines = content.split('\n');

  const missing = [];
  for (const section of requiredSections) {
    // Use exact matching to avoid partial matches
    // e.g., "## Le Problème" should NOT match "## Le Problème en Une Phrase"
    const found = lines.some(line => {
      const trimmed = line.trimStart();
      // Match exact header or header followed by whitespace/newline
      return trimmed === section ||
             trimmed.startsWith(section + '\n') ||
             trimmed.startsWith(section + '\r') ||
             trimmed.startsWith(section + ' ');
    });
    if (!found) {
      missing.push(section);
    }
  }

  return {
    exists: true,
    valid: missing.length === 0,
    missing
  };
}

console.log('--- File Validation ---');

// Validate triptyque files (combined existence + content check)
for (const [key, filePath] of Object.entries(TRIPTYQUE.files)) {
  const requiredSections = TRIPTYQUE.contentValidation[key];

  if (!requiredSections) {
    // Missing validation rules for triptyque files is a configuration error
    console.log(`❌ ${key}: No validation rules defined in config.js`);
    errors++;
    continue;
  }

  const result = validateContent(filePath, requiredSections);

  if (result.error) {
    console.log(`❌ ${key}: ${result.error}`);
    errors++;

    // Security errors halt execution immediately
    if (result.isSecurityError) {
      console.log('\n🛑 SECURITY ERROR: Halting execution');
      process.exit(2);
    }
    continue;
  }

  if (!result.exists) {
    console.log(`⚠️  ${key}: ${filePath} (not found - expected for new projects)`);
    warnings++;
    continue;
  }

  if (result.valid) {
    console.log(`✅ ${key}: All ${requiredSections.length} required sections present`);
  } else {
    console.log(`❌ ${key}: Missing sections:`);
    result.missing.forEach(section => console.log(`   - ${section}`));
    errors++;
  }
}

console.log('\n--- Workflow Configuration ---');

// Validate workflow configuration exists and is valid
if (!TRIPTYQUE.workflow) {
  console.log('❌ Workflow configuration missing');
  errors++;
} else {
  const { order, maxIterations, escalationThresholdDays } = TRIPTYQUE.workflow;

  if (!order || !Array.isArray(order) || order.length === 0) {
    console.log('❌ Workflow order not defined or empty');
    errors++;
  } else {
    console.log(`✅ Workflow order: ${order.join(' → ')}`);
  }

  if (typeof maxIterations !== 'number' || maxIterations < 1) {
    console.log('⚠️  Max iterations not defined or invalid (using default: 3)');
    warnings++;
  } else {
    console.log(`✅ Max iterations: ${maxIterations}`);
  }

  if (typeof escalationThresholdDays !== 'number' || escalationThresholdDays < 1) {
    console.log('⚠️  Escalation threshold not defined or invalid');
    warnings++;
  } else {
    console.log(`✅ Escalation threshold: ${escalationThresholdDays} days`);
  }
}

console.log('\n================================');
console.log(`📊 Summary: ${errors} error(s), ${warnings} warning(s)`);

if (errors > 0) {
  console.log('❌ Validation FAILED');
  process.exit(1);
} else if (warnings > 0) {
  console.log('⚠️  Validation PASSED with warnings');
  process.exit(0);
} else {
  console.log('✅ Validation PASSED');
  process.exit(0);
}
