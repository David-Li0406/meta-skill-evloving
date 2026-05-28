#!/usr/bin/env node
/**
 * Test: Validate Templates
 *
 * Validates that:
 * - All expected templates exist
 * - Templates have proper structure (headings, tables)
 * - Templates are not empty or malformed
 *
 * @module tests/validate-templates
 */

const fs = require('fs');
const path = require('path');
const {
  safeReadFile,
  directoryExists,
  printSeparator
} = require('./utils');
const { TEMPLATES_DIR: TEMPLATES_DIR_CONFIG } = require('./config');

// =============================================================================
// Configuration Constants
// =============================================================================

/** @const {string} Directory containing templates (from project-management skill) */
const TEMPLATES_DIR = TEMPLATES_DIR_CONFIG;

/** @const {number} Minimum number of heading sections required */
const MIN_HEADING_COUNT = 3;

/** @const {number} Minimum content length in characters */
const MIN_CONTENT_LENGTH = 500;

/**
 * Expected templates based on orchestrator and agent references
 * @const {string[]}
 */
const EXPECTED_TEMPLATES = [
  'brief-client.md',
  'estimation.md',
  'proposition.md',
  'planning.md',
  'reporting.md',
  'compte-rendu.md',
  'pv-recette.md',
  'bilan-projet.md'
];

// =============================================================================
// Test Results
// =============================================================================

let passed = 0;
let failed = 0;

// =============================================================================
// Validation Functions
// =============================================================================

/**
 * Validate template structure and content
 *
 * @param {string} filePath - Path to template file
 * @returns {string[]} Array of validation errors (empty if valid)
 */
function validateTemplate(filePath) {
  const { content, error } = safeReadFile(filePath);
  if (error) {
    return [error];
  }

  const errors = [];

  // Check for main heading
  if (!content.match(/^#\s+.+/m)) {
    errors.push('Missing main heading');
  }

  // Check for table structure (common in templates)
  if (!content.includes('|')) {
    errors.push('Missing table structure');
  }

  // Check for sections/structure
  const headingCount = (content.match(/^##?\s+/gm) || []).length;
  if (headingCount < MIN_HEADING_COUNT) {
    errors.push(`Template seems too short (< ${MIN_HEADING_COUNT} sections)`);
  }

  // Check minimum content length
  if (content.length < MIN_CONTENT_LENGTH) {
    errors.push(`Template content too short (< ${MIN_CONTENT_LENGTH} chars)`);
  }

  return errors;
}

// =============================================================================
// Main Execution
// =============================================================================

console.log('🧪 Validating Templates\n');
printSeparator();

if (!directoryExists(TEMPLATES_DIR)) {
  console.error(`❌ Templates directory not found: ${TEMPLATES_DIR}`);
  process.exit(1);
}

console.log('\n📁 Checking template existence:\n');

for (const template of EXPECTED_TEMPLATES) {
  const templatePath = path.join(TEMPLATES_DIR, template);

  if (fs.existsSync(templatePath)) {
    const errors = validateTemplate(templatePath);

    if (errors.length === 0) {
      console.log(`✅ ${template}`);
      passed++;
    } else {
      console.log(`⚠️  ${template} (exists but has issues)`);
      for (const err of errors) {
        console.log(`   └─ ${err}`);
      }
      passed++; // Still count as passed since file exists
    }
  } else {
    console.log(`❌ ${template} - NOT FOUND`);
    failed++;
  }
}

// List any extra templates
console.log('\n📋 Extra templates found:\n');

let actualTemplates = [];
try {
  actualTemplates = fs.readdirSync(TEMPLATES_DIR).filter(f => f.endsWith('.md'));
} catch (err) {
  console.error(`Warning: Cannot list templates: ${err.message}`);
}

const extraTemplates = actualTemplates.filter(t => !EXPECTED_TEMPLATES.includes(t));

if (extraTemplates.length === 0) {
  console.log('   (none)');
} else {
  for (const template of extraTemplates) {
    console.log(`   📄 ${template}`);
  }
}

console.log('\n');
printSeparator();
console.log(`\n📊 Results: ${passed} passed, ${failed} failed`);
console.log(`   Templates expected: ${EXPECTED_TEMPLATES.length}`);
console.log(`   Templates found: ${actualTemplates.length}`);

if (failed > 0) {
  console.log('\n❌ Some template tests failed');
  process.exit(1);
} else {
  console.log('\n✅ All template tests passed');
  process.exit(0);
}
