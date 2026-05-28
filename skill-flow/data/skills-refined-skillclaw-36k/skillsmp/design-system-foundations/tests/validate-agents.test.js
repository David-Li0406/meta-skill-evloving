#!/usr/bin/env node
/**
 * Test: Validate Agent Structure
 *
 * Validates that each agent file follows the required structure:
 * - Valid YAML frontmatter with name and description
 * - Main heading (H1)
 * - Appropriate sections based on agent type
 * - CSS code examples for design system agents
 *
 * @module tests/validate-agents
 */

const path = require('path');
const {
  findMarkdownFiles,
  safeReadFile,
  parseFrontmatter,
  directoryExists,
  hasCodeBlocks,
  extractCSSVariables,
  printSeparator
} = require('./utils');
const { AGENTS_DIR, LEVELS, AGENT_REQUIREMENTS } = require('./config');

let passed = 0;
let failed = 0;

/**
 * Validate a single agent file
 *
 * @param {string} filePath - Path to the agent file
 * @param {string} level - Atomic Design level
 * @returns {string[]} Array of error messages
 */
function validateAgent(filePath, level) {
  const isOrchestrator = filePath.includes('orchestrator');
  const isFoundation = level === 'foundations';
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
  if (content.length < AGENT_REQUIREMENTS.minContentLength) {
    fileErrors.push(`Content too short (< ${AGENT_REQUIREMENTS.minContentLength} characters)`);
  }

  // Orchestrator specific checks
  if (isOrchestrator) {
    if (!content.includes('Agent') && !content.includes('Agents')) {
      fileErrors.push('Orchestrator missing agent listing');
    }
    if (!content.toLowerCase().includes('routing') && !content.toLowerCase().includes('route')) {
      fileErrors.push('Orchestrator missing routing information');
    }
  } else {
    // Non-orchestrator agents should have code examples
    if (!hasCodeBlocks(content)) {
      fileErrors.push('Missing code examples (code blocks)');
    }

    // Foundation agents should have CSS tokens
    if (isFoundation) {
      try {
        const cssVars = extractCSSVariables(content) || [];
        if (cssVars.length < 3) {
          fileErrors.push('Foundation agent should define multiple CSS custom properties');
        }
      } catch (err) {
        fileErrors.push(`Error extracting CSS variables: ${err.message}`);
      }
    }

    // Component agents should have variant documentation
    if (!isFoundation && !isOrchestrator) {
      if (!content.toLowerCase().includes('variant')) {
        fileErrors.push('Component agent missing variant documentation');
      }
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

// Validate each Atomic Design level
for (const level of LEVELS) {
  const levelDir = path.join(AGENTS_DIR, level);

  if (!directoryExists(levelDir)) {
    console.log(`⚠️  Level directory not found: ${level}`);
    continue;
  }

  console.log(`\n📁 Level: ${level}`);

  const files = findMarkdownFiles(levelDir);

  for (const file of files) {
    const relativePath = path.relative(AGENTS_DIR, file);
    const fileErrors = validateAgent(file, level);

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
