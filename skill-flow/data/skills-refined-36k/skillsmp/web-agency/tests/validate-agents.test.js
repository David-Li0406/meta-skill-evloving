#!/usr/bin/env node
/**
 * Test: Validate Agent Structure
 *
 * Validates that each agent file follows the required structure:
 * - Valid YAML frontmatter with name and description
 * - Main heading (H1)
 * - "Ta Responsabilité Unique" section (for specialized agents)
 * - "Tu NE fais PAS" section (for specialized agents)
 * - Routing rules (for orchestrators)
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
const { PROJECT_MANAGEMENT_DIR } = require('./config');

const AGENTS_DIR = PROJECT_MANAGEMENT_DIR;

// Test results
let passed = 0;
let failed = 0;

/**
 * Validate a single agent file against required structure
 *
 * @param {string} filePath - Path to the agent file
 * @returns {string[]} Array of error messages (empty if valid)
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

  // Non-orchestrator specific checks
  if (!isOrchestrator) {
    if (!content.includes('Ta Responsabilité Unique') && !content.includes('Responsabilité Unique')) {
      fileErrors.push('Missing "Ta Responsabilité Unique" section');
    }

    if (!content.includes('Tu NE fais PAS') && !content.includes('Tu NE Fais PAS')) {
      fileErrors.push('Missing "Tu NE fais PAS" section');
    }
  }

  // Orchestrator specific checks
  if (isOrchestrator) {
    if (!content.includes('Règles de Routage') && !content.includes('Routage')) {
      fileErrors.push('Missing routing rules section');
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

// Exclude templates and SKILL.md from agent validation
const allFiles = findMarkdownFiles(AGENTS_DIR);
const files = allFiles.filter(f =>
  !f.includes('/templates/') &&
  !f.endsWith('SKILL.md')
);
console.log(`Found ${files.length} agent files\n`);

for (const file of files) {
  const relativePath = path.relative(AGENTS_DIR, file);
  const fileErrors = validateAgent(file);

  if (fileErrors.length === 0) {
    console.log(`✅ ${relativePath}`);
    passed++;
  } else {
    console.log(`❌ ${relativePath}`);
    for (const err of fileErrors) {
      console.log(`   └─ ${err}`);
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
