#!/usr/bin/env node
/**
 * Test: Validate SKILL.md Structure
 *
 * Validates that the main SKILL.md file follows the required structure:
 * - Valid YAML frontmatter
 * - Proper routing table
 * - Links to all Atomic Design levels
 *
 * @module tests/validate-skill
 */

const path = require('path');
const {
  safeReadFile,
  parseFrontmatter,
  fileExists,
  printSeparator
} = require('./utils');
const { SKILL_ROOT, LEVELS, LEVEL_DESCRIPTIONS } = require('./config');

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

// Main execution
console.log('🧪 Validating SKILL.md Structure\n');
printSeparator();

const skillFile = path.join(SKILL_ROOT, 'SKILL.md');

if (!fileExists(skillFile)) {
  console.error(`❌ SKILL.md not found: ${skillFile}`);
  process.exit(1);
}

const { content, error } = safeReadFile(skillFile);
if (error) {
  console.error(`❌ Cannot read SKILL.md: ${error}`);
  process.exit(1);
}

console.log('\n📄 SKILL.md Validation\n');

// Check frontmatter
const frontmatter = parseFrontmatter(content);
logResult(!!frontmatter, 'Has YAML frontmatter');

if (frontmatter) {
  logResult(!!frontmatter.name, 'Frontmatter has "name" field');
  logResult(!!frontmatter.description, 'Frontmatter has "description" field');
  logResult(!!frontmatter.version, 'Frontmatter has "version" field');
}

// Check main heading
logResult(/^#\s+.+/m.test(content), 'Has main heading (# Title)');

// Check for Atomic Design levels routing
console.log('\n📁 Atomic Design Levels Routing\n');

for (const level of LEVELS) {
  const hasLevelMention = content.toLowerCase().includes(level);
  const hasLevelLink = content.includes(`agents/${level}`);
  logResult(hasLevelMention, `Mentions "${level}" level`);
  logResult(hasLevelLink, `Links to agents/${level}`);
}

// Check for routing logic
console.log('\n🔀 Routing Configuration\n');

logResult(content.includes('Routing') || content.includes('routing'), 'Has routing section');
logResult(/foundations|atoms|molecules|templates/i.test(content), 'Routes to Atomic Design levels');

// Check for code examples
console.log('\n💻 Code Examples\n');

logResult(/```/.test(content), 'Contains code blocks');
logResult(/--[a-z]+-/.test(content) || content.includes('CSS'), 'References CSS tokens or styling');

// Summary
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
