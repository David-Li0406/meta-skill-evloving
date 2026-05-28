#!/usr/bin/env node
/**
 * Test: Validate Agent Structure
 *
 * Validates that each agent file follows the required structure:
 * - Valid YAML frontmatter with name, description, version
 * - Main heading (H1)
 * - "Ta Responsabilité Unique" section (for specialized agents)
 * - Routing/workflow rules (for orchestrators)
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
const { AGENTS_DIR, AGENT_REQUIREMENTS } = require('./config');

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
  const isOrchestrator = path.basename(filePath) === 'orchestrator.md';
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
    for (const field of AGENT_REQUIREMENTS.frontmatter) {
      if (!frontmatter[field]) {
        fileErrors.push(`Missing "${field}" in frontmatter`);
      }
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
  }

  // Orchestrator specific checks
  if (isOrchestrator) {
    const hasWorkflow = content.includes('Workflow') || content.includes('workflow');
    const hasAgents = content.includes('Agents') || content.includes('agents');
    if (!hasWorkflow && !hasAgents) {
      fileErrors.push('Missing workflow or agents section');
    }
  }

  // Check minimum content length
  if (content.length < AGENT_REQUIREMENTS.minContentLength) {
    fileErrors.push(`Content too short (${content.length} < ${AGENT_REQUIREMENTS.minContentLength})`);
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

// Find all agent files
const allFiles = findMarkdownFiles(AGENTS_DIR);
const files = allFiles.filter(f => !f.endsWith('SKILL.md'));
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
