#!/usr/bin/env node
/**
 * Test: Validate Routing Configuration
 *
 * Validates that orchestrators properly route to their agents
 *
 * @module tests/validate-routing
 */

const path = require('path');
const {
  safeReadFile,
  fileExists,
  printSeparator
} = require('./utils');
const { AGENTS_DIR, EXPECTED_DOMAINS, EXPECTED_ROUTING } = require('./config');

// Test results
let passed = 0;
let failed = 0;

// Main execution
console.log('🧪 Validating Routing Configuration\n');
printSeparator();

for (const domain of EXPECTED_DOMAINS) {
  const orchestratorPath = path.join(AGENTS_DIR, domain, 'orchestrator.md');

  if (!fileExists(orchestratorPath)) {
    console.log(`❌ ${domain}/orchestrator.md not found`);
    failed++;
    continue;
  }

  const { content, error } = safeReadFile(orchestratorPath);
  if (error) {
    console.log(`❌ ${domain}/orchestrator.md: ${error}`);
    failed++;
    continue;
  }

  const routing = EXPECTED_ROUTING[domain] || [];
  let allRoutesFound = true;
  const missingRoutes = [];

  for (const route of routing) {
    // Check if the agent is mentioned in the orchestrator
    if (!content.includes(route.agent)) {
      missingRoutes.push(`${route.intent} → ${route.agent}`);
      allRoutesFound = false;
    }
  }

  if (allRoutesFound) {
    console.log(`✅ ${domain}/orchestrator.md (${routing.length} routes)`);
    passed++;
  } else {
    console.log(`❌ ${domain}/orchestrator.md - missing routes:`);
    for (const route of missingRoutes) {
      console.log(`   └─ ${route}`);
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
