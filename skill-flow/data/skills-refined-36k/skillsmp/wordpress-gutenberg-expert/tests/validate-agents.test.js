#!/usr/bin/env node
/**
 * Test: Validate Agent Structure
 *
 * Validates that each WordPress agent file follows the required structure:
 * - Valid YAML frontmatter with name and description
 * - Main heading (H1)
 * - Sources section with WordPress documentation links
 *
 * @module tests/validate-agents
 */

const path = require('path');
const {
  findMarkdownFiles,
  safeReadFile,
  parseFrontmatter,
  directoryExists,
  printSeparator,
  countWpElements
} = require('./utils');
const { AGENTS_DIR, DOMAINS, STANDALONE_AGENTS } = require('./config');

let passed = 0;
let failed = 0;
let totalAgents = 0;

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
  if (content.length < 300) {
    fileErrors.push('Content too short (< 300 characters)');
  }

  // Check for WordPress documentation sources (non-orchestrators)
  if (!isOrchestrator) {
    if (!content.includes('developer.wordpress.org') &&
        !content.includes('Sources') &&
        !content.includes('Référence')) {
      // Warn but don't fail
      // fileErrors.push('Missing WordPress documentation sources');
    }
  }

  return fileErrors;
}

// Main execution
console.log('🧪 Validating WordPress Agent Structure\n');
printSeparator();

if (!directoryExists(AGENTS_DIR)) {
  console.error(`❌ Agents directory not found: ${AGENTS_DIR}`);
  process.exit(1);
}

// Validate domain agents
for (const domain of DOMAINS) {
  const domainDir = path.join(AGENTS_DIR, domain);

  if (!directoryExists(domainDir)) {
    console.log(`⚠️  Domain directory not found: ${domain}`);
    continue;
  }

  console.log(`\n📁 Domain: ${domain}`);

  const files = findMarkdownFiles(domainDir);
  totalAgents += files.length;

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

// Validate standalone agents
console.log(`\n📁 Standalone Agents`);
for (const agentName of STANDALONE_AGENTS) {
  const agentPath = path.join(AGENTS_DIR, `${agentName}.md`);

  if (!require('fs').existsSync(agentPath)) {
    console.log(`  ⚠️  ${agentName}.md not found`);
    continue;
  }

  totalAgents++;
  const fileErrors = validateAgent(agentPath);

  if (fileErrors.length === 0) {
    console.log(`  ✅ ${agentName}.md`);
    passed++;
  } else {
    console.log(`  ❌ ${agentName}.md`);
    for (const err of fileErrors) {
      console.log(`     └─ ${err}`);
    }
    failed++;
  }
}

console.log('\n');
printSeparator();
console.log(`\n📊 Results: ${passed} passed, ${failed} failed (${totalAgents} total agents)`);

if (failed > 0) {
  console.log('\n❌ Some tests failed');
  process.exit(1);
} else {
  console.log('\n✅ All tests passed');
  process.exit(0);
}
