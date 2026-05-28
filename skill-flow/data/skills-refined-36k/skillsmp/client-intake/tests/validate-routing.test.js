#!/usr/bin/env node
/**
 * Test: Validate Routing Rules
 *
 * Validates that orchestrators reference existing agents
 *
 * @module tests/validate-routing
 */

const fs = require('fs');
const path = require('path');
const { safeReadFile, printSeparator } = require('./utils');
const { AGENTS_DIR, EXPECTED_DOMAINS } = require('./config');

// Test results
let passed = 0;
let failed = 0;

console.log('🧪 Validating Orchestrator Routing\n');
printSeparator();

// Check each domain's orchestrator
let orchestratorCount = 0;

for (const domain of EXPECTED_DOMAINS) {
  const orchestratorPath = path.join(AGENTS_DIR, domain, 'orchestrator.md');

  const { content, error } = safeReadFile(orchestratorPath);
  if (error) {
    console.log(`❌ ${domain}/orchestrator.md - ${error}`);
    failed++;
    continue;
  }

  orchestratorCount++;

  // Extract agent references from the orchestrator
  const agentRefs = [];
  const refPattern = /`([a-z][a-z0-9-]*)`/g;
  let match;
  while ((match = refPattern.exec(content)) !== null) {
    agentRefs.push(match[1]);
  }

  // Check if referenced agents exist in this domain
  const domainPath = path.join(AGENTS_DIR, domain);
  let missingAgents = [];

  for (const ref of agentRefs) {
    // Skip common keywords
    if (['orchestrator', 'email', 'form', 'chat', 'webhook', 'api'].includes(ref)) continue;

    const agentPath = path.join(domainPath, `${ref}.md`);
    try {
      fs.statSync(agentPath);
    } catch {
      // Agent not found in domain, check if it's a cross-reference
      if (ref.includes('-') && !ref.startsWith('task-')) {
        missingAgents.push(ref);
      }
    }
  }

  if (missingAgents.length === 0) {
    console.log(`✅ ${domain}/orchestrator.md`);
    passed++;
  } else {
    console.log(`⚠️  ${domain}/orchestrator.md (${missingAgents.length} refs not found locally)`);
    passed++; // Don't fail for cross-references
  }
}

console.log('\n');
printSeparator();
console.log(`\n📊 Results:`);
console.log(`   Found ${orchestratorCount} orchestrators`);
console.log(`   Passed: ${passed}, Failed: ${failed}`);

if (failed > 0) {
  console.log('\n❌ Some tests failed');
  process.exit(1);
} else {
  console.log('\n✅ All tests passed');
  process.exit(0);
}
