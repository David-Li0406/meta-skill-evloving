#!/usr/bin/env node
/**
 * Test: Validate Domain Structure
 *
 * Validates that all expected domains exist with their expected agents
 *
 * @module tests/validate-domains
 */

const path = require('path');
const fs = require('fs');
const {
  directoryExists,
  fileExists,
  printSeparator
} = require('./utils');
const { AGENTS_DIR, EXPECTED_DOMAINS, EXPECTED_AGENTS } = require('./config');

// Test results
let passed = 0;
let failed = 0;

// Main execution
console.log('🧪 Validating Domain Structure\n');
printSeparator();

if (!directoryExists(AGENTS_DIR)) {
  console.error(`❌ Agents directory not found: ${AGENTS_DIR}`);
  process.exit(1);
}

console.log(`Checking ${EXPECTED_DOMAINS.length} expected domains...\n`);

for (const domain of EXPECTED_DOMAINS) {
  const domainPath = path.join(AGENTS_DIR, domain);

  if (!directoryExists(domainPath)) {
    console.log(`❌ Domain missing: ${domain}`);
    failed++;
    continue;
  }

  const expectedAgents = EXPECTED_AGENTS[domain] || [];
  let domainPassed = true;
  const missingAgents = [];

  for (const agent of expectedAgents) {
    const agentPath = path.join(domainPath, `${agent}.md`);
    if (!fileExists(agentPath)) {
      missingAgents.push(agent);
      domainPassed = false;
    }
  }

  if (domainPassed) {
    console.log(`✅ ${domain}/ (${expectedAgents.length} agents)`);
    passed++;
  } else {
    console.log(`❌ ${domain}/ - missing agents: ${missingAgents.join(', ')}`);
    failed++;
  }
}

// Check for unexpected domains
const actualDomains = fs.readdirSync(AGENTS_DIR).filter(f => {
  const fullPath = path.join(AGENTS_DIR, f);
  return fs.statSync(fullPath).isDirectory();
});

const unexpectedDomains = actualDomains.filter(d => !EXPECTED_DOMAINS.includes(d));
if (unexpectedDomains.length > 0) {
  console.log(`\n⚠️  Unexpected domains found: ${unexpectedDomains.join(', ')}`);
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
