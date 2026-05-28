#!/usr/bin/env node
/**
 * Test: Validate Agent Structure
 *
 * Validates that each agent file follows the required structure:
 * - Valid YAML frontmatter with name and description
 * - Main heading (H1)
 * - Appropriate sections based on agent type
 *
 * @module tests/validate-agents
 */

const path = require('path');
const {
  findMarkdownFiles,
  safeReadFile,
  parseFrontmatter,
  directoryExists,
  printSeparator
} = require('./utils');
const { AGENTS_DIR, PHASES } = require('./config');

let passed = 0;
let failed = 0;

/**
 * Validate a single agent file
 *
 * @param {string} filePath - Path to the agent file
 * @returns {string[]} Array of error messages
 */
function validateAgent(filePath) {
  const isOrchestrator = filePath.includes('orchestrator');
  const fileErrors = [];

  const { content, error } = safeReadFile(filePath);
  if (error) {
    return [error];
  }

  // Check frontmatter
  const frontmatter = parseFrontmatter(content);
  if (!frontmatter) {
    fileErrors.push('Missing YAML frontmatter');
  } else {
    if (!frontmatter.name) {
      fileErrors.push('Missing "name" in frontmatter');
    }
    if (!frontmatter.description) {
      fileErrors.push('Missing "description" in frontmatter');
    }
  }

  // Check main heading
  if (!content.match(/^#\s+.+/m)) {
    fileErrors.push('Missing main heading (# Title)');
  }

  // Check minimum content length
  if (content.length < 200) {
    fileErrors.push('Content too short (< 200 characters)');
  }

  // Orchestrator specific checks
  if (isOrchestrator) {
    if (!content.includes('Agent') && !content.includes('Agents')) {
      fileErrors.push('Orchestrator missing agent listing');
    }
  }

  return fileErrors;
}

// Main execution
console.log('🧪 Validating Agent Structure\n');
printSeparator();

if (!directoryExists(AGENTS_DIR)) {
  console.error(`❌ Agents directory not found: ${AGENTS_DIR}`);
  process.exit(1);
}

// Validate each phase
for (const phase of PHASES) {
  const phaseDir = path.join(AGENTS_DIR, phase);

  if (!directoryExists(phaseDir)) {
    console.log(`⚠️  Phase directory not found: ${phase}`);
    continue;
  }

  console.log(`\n📁 Phase: ${phase}`);

  const files = findMarkdownFiles(phaseDir);

  for (const file of files) {
    const relativePath = path.relative(AGENTS_DIR, file);
    const fileErrors = validateAgent(file);

    if (fileErrors.length === 0) {
      console.log(`  ✅ ${relativePath}`);
      passed++;
    } else {
      console.log(`  ❌ ${relativePath}`);
      for (const err of fileErrors) {
        console.log(`     └─ ${err}`);
      }
      failed++;
    }
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
