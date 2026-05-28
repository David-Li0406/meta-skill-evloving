#!/usr/bin/env node
/**
 * Test: Validate Atomic Design Levels
 *
 * Validates that each Atomic Design level has:
 * - All expected agents
 * - An orchestrator with proper routing
 * - Cross-references between levels
 *
 * @module tests/validate-levels
 */

const path = require('path');
const {
  safeReadFile,
  fileExists,
  directoryExists,
  printSeparator
} = require('./utils');
const {
  AGENTS_DIR,
  LEVELS,
  EXPECTED_AGENTS_PER_LEVEL,
  LEVEL_DESCRIPTIONS
} = require('./config');

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
console.log('🧪 Validating Atomic Design Levels\n');
printSeparator();

if (!directoryExists(AGENTS_DIR)) {
  console.error(`❌ Agents directory not found: ${AGENTS_DIR}`);
  process.exit(1);
}

// Check each level
for (const level of LEVELS) {
  console.log(`\n📁 ${level.charAt(0).toUpperCase() + level.slice(1)}`);
  console.log(`   ${LEVEL_DESCRIPTIONS[level]}\n`);

  const levelDir = path.join(AGENTS_DIR, level);

  // Check directory exists
  const dirExists = directoryExists(levelDir);
  logResult(dirExists, `Directory exists: agents/${level}`);

  if (!dirExists) continue;

  // Check expected agents
  const expectedAgents = EXPECTED_AGENTS_PER_LEVEL[level];

  for (const agentName of expectedAgents) {
    const agentFile = path.join(levelDir, `${agentName}.md`);
    const exists = fileExists(agentFile);
    logResult(exists, `${agentName}.md exists`);
  }

  // Check orchestrator has routing
  const orchestratorFile = path.join(levelDir, 'orchestrator.md');
  if (fileExists(orchestratorFile)) {
    const { content } = safeReadFile(orchestratorFile);
    const contentLower = content.toLowerCase();

    // Check routing to other agents in level
    // Match either with dash (hero-sections) or without (herosections)
    const hasRouting = expectedAgents
      .filter(a => a !== 'orchestrator')
      .every(agent => {
        const withDash = agent.toLowerCase();
        const withoutDash = agent.toLowerCase().replace(/-/g, '');
        return contentLower.includes(withDash) || contentLower.includes(withoutDash);
      });

    logResult(hasRouting, 'Orchestrator routes to all level agents');
  }
}

// Check cross-level references
console.log('\n🔗 Cross-Level References\n');

// Atoms should reference foundations
const buttonsFile = path.join(AGENTS_DIR, 'atoms', 'buttons.md');
if (fileExists(buttonsFile)) {
  const { content } = safeReadFile(buttonsFile);
  const referencesFoundations =
    content.includes('--color-') ||
    content.includes('--space-') ||
    content.includes('foundations');
  logResult(referencesFoundations, 'Atoms reference foundation tokens');
}

// Molecules should reference atoms
const formsFile = path.join(AGENTS_DIR, 'molecules', 'forms.md');
if (fileExists(formsFile)) {
  const { content } = safeReadFile(formsFile);
  const referencesAtoms =
    content.toLowerCase().includes('button') ||
    content.toLowerCase().includes('input') ||
    content.toLowerCase().includes('label');
  logResult(referencesAtoms, 'Molecules reference atom components');
}

// Templates should reference molecules
const layoutsFile = path.join(AGENTS_DIR, 'templates', 'layouts.md');
if (fileExists(layoutsFile)) {
  const { content } = safeReadFile(layoutsFile);
  const referencesMolecules =
    content.toLowerCase().includes('card') ||
    content.toLowerCase().includes('navigation') ||
    content.toLowerCase().includes('form');
  logResult(referencesMolecules, 'Templates reference molecule components');
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
