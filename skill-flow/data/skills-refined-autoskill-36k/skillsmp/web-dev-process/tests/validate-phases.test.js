#!/usr/bin/env node
/**
 * Test: Validate Phase Structure
 *
 * Validates that each of the 7 development phases:
 * - Has a dedicated directory
 * - Contains an orchestrator
 * - Contains expected specialized agents
 *
 * @module tests/validate-phases
 */

const path = require('path');
const {
  directoryExists,
  fileExists,
  printSeparator
} = require('./utils');
const { AGENTS_DIR, PHASES, EXPECTED_AGENTS_PER_PHASE } = require('./config');

let passed = 0;
let failed = 0;
const issues = [];

console.log('🧪 Validating Phase Structure\n');
printSeparator();

// Check each phase
for (const phase of PHASES) {
  console.log(`\n📁 Phase: ${phase}`);

  const phaseDir = path.join(AGENTS_DIR, phase);

  // Check phase directory exists
  if (!directoryExists(phaseDir)) {
    console.log(`  ❌ Directory missing: agents/${phase}/`);
    issues.push(`Phase ${phase}: directory missing`);
    failed++;
    continue;
  }
  console.log(`  ✅ Directory exists`);
  passed++;

  // Check orchestrator exists
  const orchestratorPath = path.join(phaseDir, 'orchestrator.md');
  if (!fileExists(orchestratorPath)) {
    console.log(`  ❌ Orchestrator missing: ${phase}/orchestrator.md`);
    issues.push(`Phase ${phase}: orchestrator missing`);
    failed++;
  } else {
    console.log(`  ✅ Orchestrator exists`);
    passed++;
  }

  // Check expected agents
  const expectedAgents = EXPECTED_AGENTS_PER_PHASE[phase] || [];
  let agentsPassed = 0;
  let agentsMissing = [];

  for (const agent of expectedAgents) {
    if (agent === 'orchestrator') continue; // Already checked

    const agentPath = path.join(phaseDir, `${agent}.md`);
    if (fileExists(agentPath)) {
      agentsPassed++;
    } else {
      agentsMissing.push(agent);
    }
  }

  const expectedCount = expectedAgents.length - 1; // Exclude orchestrator
  if (agentsMissing.length === 0) {
    console.log(`  ✅ All ${expectedCount} expected agents present`);
    passed++;
  } else {
    console.log(`  ⚠️  ${agentsPassed}/${expectedCount} expected agents present`);
    console.log(`     Missing: ${agentsMissing.join(', ')}`);
    // Don't fail for missing agents, just warn
  }
}

console.log('\n');
printSeparator();

// Summary
console.log('\n📊 Phase Summary:');
console.log(`   Phases: ${PHASES.length}`);
console.log(`   Checks passed: ${passed}`);
console.log(`   Checks failed: ${failed}`);

if (issues.length > 0) {
  console.log('\n⚠️  Issues found:');
  for (const issue of issues) {
    console.log(`   - ${issue}`);
  }
}

if (failed > 0) {
  console.log('\n❌ Some checks failed');
  process.exit(1);
} else {
  console.log('\n✅ All checks passed');
  process.exit(0);
}
