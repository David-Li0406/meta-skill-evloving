#!/usr/bin/env node
/**
 * Test: Validate Domain Structure
 *
 * Validates that each WordPress domain:
 * - Has a dedicated directory
 * - Contains an orchestrator
 * - Contains expected specialized agents
 *
 * @module tests/validate-domains
 */

const path = require('path');
const {
  directoryExists,
  fileExists,
  printSeparator
} = require('./utils');
const { AGENTS_DIR, DOMAINS, EXPECTED_AGENTS_PER_DOMAIN, STANDALONE_AGENTS } = require('./config');

let passed = 0;
let failed = 0;
const issues = [];

console.log('🧪 Validating WordPress Domain Structure\n');
printSeparator();

// Check each domain
for (const domain of DOMAINS) {
  console.log(`\n📁 Domain: ${domain}`);

  const domainDir = path.join(AGENTS_DIR, domain);

  // Check domain directory exists
  if (!directoryExists(domainDir)) {
    console.log(`  ❌ Directory missing: agents/${domain}/`);
    issues.push(`Domain ${domain}: directory missing`);
    failed++;
    continue;
  }
  console.log(`  ✅ Directory exists`);
  passed++;

  // Check orchestrator exists
  const orchestratorPath = path.join(domainDir, 'orchestrator.md');
  if (!fileExists(orchestratorPath)) {
    console.log(`  ❌ Orchestrator missing: ${domain}/orchestrator.md`);
    issues.push(`Domain ${domain}: orchestrator missing`);
    failed++;
  } else {
    console.log(`  ✅ Orchestrator exists`);
    passed++;
  }

  // Check expected agents
  const expectedAgents = EXPECTED_AGENTS_PER_DOMAIN[domain] || [];
  let agentsPassed = 0;
  let agentsMissing = [];

  for (const agent of expectedAgents) {
    if (agent === 'orchestrator') continue;

    const agentPath = path.join(domainDir, `${agent}.md`);
    if (fileExists(agentPath)) {
      agentsPassed++;
    } else {
      agentsMissing.push(agent);
    }
  }

  const expectedCount = expectedAgents.length - 1;
  if (agentsMissing.length === 0) {
    console.log(`  ✅ All ${expectedCount} expected agents present`);
    passed++;
  } else {
    console.log(`  ⚠️  ${agentsPassed}/${expectedCount} expected agents present`);
    if (agentsMissing.length <= 3) {
      console.log(`     Missing: ${agentsMissing.join(', ')}`);
    } else {
      console.log(`     Missing: ${agentsMissing.length} agents`);
    }
  }
}

// Check standalone agents
console.log(`\n📁 Standalone Expert Agents`);
for (const agent of STANDALONE_AGENTS) {
  const agentPath = path.join(AGENTS_DIR, `${agent}.md`);
  if (fileExists(agentPath)) {
    console.log(`  ✅ ${agent}.md`);
    passed++;
  } else {
    console.log(`  ❌ ${agent}.md missing`);
    issues.push(`Standalone agent missing: ${agent}`);
    failed++;
  }
}

console.log('\n');
printSeparator();

// Summary
console.log('\n📊 Domain Summary:');
console.log(`   Domains: ${DOMAINS.length}`);
console.log(`   Standalone agents: ${STANDALONE_AGENTS.length}`);
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
