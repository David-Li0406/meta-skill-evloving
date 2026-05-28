#!/usr/bin/env node
/**
 * Test: Validate Documentation Files
 *
 * Validates that documentation files exist and have proper structure:
 * - All expected docs are present
 * - Proper headings and structure
 * - Code examples where appropriate
 *
 * @module tests/validate-docs
 */

const path = require('path');
const {
  safeReadFile,
  fileExists,
  directoryExists,
  hasCodeBlocks,
  countHeadings,
  printSeparator
} = require('./utils');
const { DOCS_DIR, EXPECTED_DOCS } = require('./config');

let passed = 0;
let failed = 0;

/**
 * Log a test result
 * @param {boolean} success - Test passed
 * @param {string} message - Test description
 */
function logResult(success, message) {
  if (success) {
    console.log(`  ✅ ${message}`);
    passed++;
  } else {
    console.log(`  ❌ ${message}`);
    failed++;
  }
}

/**
 * Validate a documentation file
 *
 * @param {string} filePath - Path to the doc file
 * @returns {string[]} Array of error messages
 */
function validateDoc(filePath) {
  const docErrors = [];
  const fileName = path.basename(filePath);

  const { content, error } = safeReadFile(filePath);
  if (error) {
    return [error];
  }

  // Check main heading
  if (!content.match(/^#\s+.+/m)) {
    docErrors.push('Missing main heading (# Title)');
  }

  // Check minimum content length (docs should be substantial)
  if (content.length < 1000) {
    docErrors.push('Content too short for documentation (< 1000 characters)');
  }

  // Check for proper structure (multiple headings)
  const headingCount = countHeadings(content);
  if (headingCount < 3) {
    docErrors.push('Documentation should have multiple sections (at least 3 headings)');
  }

  // Technical docs should have code examples
  const technicalDocs = [
    'testing-guide.md',
    'dark-mode.md',
    'bundle-optimization.md',
    'animation-performance.md'
  ];

  if (technicalDocs.includes(fileName) && !hasCodeBlocks(content)) {
    docErrors.push('Technical documentation should include code examples');
  }

  return docErrors;
}

// Main execution
console.log('🧪 Validating Documentation\n');
printSeparator();

if (!directoryExists(DOCS_DIR)) {
  console.error(`❌ Docs directory not found: ${DOCS_DIR}`);
  process.exit(1);
}

// Check all expected docs exist
console.log('\n📄 Expected Documentation Files\n');

for (const docFile of EXPECTED_DOCS) {
  const docPath = path.join(DOCS_DIR, docFile);
  const exists = fileExists(docPath);
  logResult(exists, `${docFile} exists`);
}

// Validate each doc file
console.log('\n📋 Documentation Content Validation\n');

for (const docFile of EXPECTED_DOCS) {
  const docPath = path.join(DOCS_DIR, docFile);

  if (!fileExists(docPath)) {
    continue;
  }

  const docErrors = validateDoc(docPath);

  if (docErrors.length === 0) {
    console.log(`  ✅ ${docFile} - valid structure`);
    passed++;
  } else {
    console.log(`  ❌ ${docFile}`);
    for (const err of docErrors) {
      console.log(`     └─ ${err}`);
    }
    failed++;
  }
}

console.log('\n');
printSeparator();
console.log(`\n📊 Results: ${passed} passed, ${failed} failed`);

if (failed > 0) {
  console.log('\n❌ Some tests failed');
  process.exit(1);
} else {
  console.log('\n✅ All tests passed');
  process.exit(0);
}
