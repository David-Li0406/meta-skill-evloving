#!/usr/bin/env node
/**
 * Test: Validate Domain Structure
 *
 * Validates that all expected domains exist and contain expected agents
 *
 * @module tests/validate-domains
 */

const fs = require('fs');
const path = require('path');
const { directoryExists, printSeparator } = require('./utils');
const { AGENTS_DIR, EXPECTED_DOMAINS, EXPECTED_AGENTS } = require('./config');

// Test results
let passed = 0;
let failed = 0;

console.log('🧪 Validating Domain Structure\n');
printSeparator();

// Check each expected domain
for (const domain of EXPECTED_DOMAINS) {
  const domainPath = path.join(AGENTS_DIR, domain);

  if (!directoryExists(domainPath)) {
    console.log(`❌ Domain: ${domain} - directory not found`);
    failed++;
    continue;
  }

  // Check expected agents in this domain
  const expectedAgents = EXPECTED_AGENTS[domain] || [];
  let domainErrors = [];

  for (const agent of expectedAgents) {
    const agentPath = path.join(domainPath, `${agent}.md`);
    try {
      fs.statSync(agentPath);
    } catch {
      domainErrors.push(`Missing agent: ${agent}.md`);
    }
  }

  if (domainErrors.length === 0) {
    console.log(`✅ Domain: ${domain} (${expectedAgents.length} agents)`);
    passed++;
  } else {
    console.log(`❌ Domain: ${domain}`);
    for (const err of domainErrors) {
      console.log(`   └─ ${err}`);
    }
    failed++;
  }
}

console.log('\n');
printSeparator();

// Count total agents
let totalAgents = 0;
for (const domain of Object.keys(EXPECTED_AGENTS)) {
  totalAgents += EXPECTED_AGENTS[domain].length;
}

console.log(`\n📊 Results:`);
console.log(`   Domains: ${EXPECTED_DOMAINS.length}`);
console.log(`   Expected agents: ${totalAgents}`);
console.log(`   Passed: ${passed}, Failed: ${failed}`);

if (failed > 0) {
  console.log('\n❌ Some tests failed');
  process.exit(1);
} else {
  console.log('\n✅ All tests passed');
  process.exit(0);
}
