#!/usr/bin/env node
/**
 * Validates direction-artistique skill agents
 */

const fs = require('fs');
const path = require('path');
const { SKILL_ROOT, DOMAINS, EXPECTED_AGENTS_PER_DOMAIN, TOTAL_EXPECTED_AGENTS } = require('./config');

let errors = 0;
let warnings = 0;

console.log('🔍 Validating direction-artistique agents...\n');

// Check SKILL.md exists
const skillPath = path.join(SKILL_ROOT, 'SKILL.md');
if (!fs.existsSync(skillPath)) {
  console.log('❌ SKILL.md not found');
  errors++;
} else {
  console.log('✅ SKILL.md exists');
}

// Check each domain
let totalAgents = 0;
for (const domain of DOMAINS) {
  const domainPath = path.join(SKILL_ROOT, 'agents', domain);

  if (!fs.existsSync(domainPath)) {
    console.log(`❌ Domain missing: ${domain}/`);
    errors++;
    continue;
  }

  const agents = fs.readdirSync(domainPath)
    .filter(f => f.endsWith('.md'))
    .map(f => f.replace('.md', ''));

  const expected = EXPECTED_AGENTS_PER_DOMAIN[domain] || [];

  // Check expected agents exist
  for (const agent of expected) {
    if (!agents.includes(agent)) {
      console.log(`❌ Missing agent: ${domain}/${agent}`);
      errors++;
    }
  }

  // Check for unexpected agents
  for (const agent of agents) {
    if (!expected.includes(agent)) {
      console.log(`⚠️  Unexpected agent: ${domain}/${agent}`);
      warnings++;
    }
  }

  totalAgents += agents.length;
  console.log(`✅ ${domain}/ (${agents.length} agents)`);
}

console.log(`\n📊 Total agents found: ${totalAgents}`);
console.log(`📊 Expected agents: ${TOTAL_EXPECTED_AGENTS}`);

if (totalAgents !== TOTAL_EXPECTED_AGENTS) {
  console.log(`⚠️  Agent count mismatch`);
  warnings++;
}

console.log('\n================================');
if (errors > 0) {
  console.log(`❌ ${errors} error(s), ${warnings} warning(s)`);
  process.exit(1);
} else {
  console.log(`✅ All validations passed (${warnings} warning(s))`);
  process.exit(0);
}
