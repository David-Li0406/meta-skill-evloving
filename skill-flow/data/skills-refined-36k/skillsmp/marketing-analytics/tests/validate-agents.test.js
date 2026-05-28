#!/usr/bin/env node
/**
 * Validates marketing-analytics skill agents
 */

const fs = require('fs');
const path = require('path');
const { SKILL_ROOT, DOMAINS, EXPECTED_AGENTS_PER_DOMAIN } = require('./config');

let errors = 0;
let warnings = 0;

console.log('🔍 Validating marketing-analytics agents...\n');

// Check SKILL.md exists
const skillPath = path.join(SKILL_ROOT, 'SKILL.md');
if (!fs.existsSync(skillPath)) {
  console.log('❌ SKILL.md not found');
  errors++;
} else {
  console.log('✅ SKILL.md exists');
}

// Check agents directory exists
const agentsDir = path.join(SKILL_ROOT, 'agents');
if (!fs.existsSync(agentsDir)) {
  console.log('❌ agents/ directory not found');
  errors++;
  process.exit(1);
}

// Check each domain
let totalAgents = 0;
for (const domain of DOMAINS) {
  const domainPath = path.join(agentsDir, domain);

  if (!fs.existsSync(domainPath)) {
    console.log(`⚠️  Domain not found: ${domain}/ (may be expected)`);
    warnings++;
    continue;
  }

  const agents = fs.readdirSync(domainPath)
    .filter(f => f.endsWith('.md'))
    .map(f => f.replace('.md', ''));

  const expected = EXPECTED_AGENTS_PER_DOMAIN[domain] || [];

  // Check expected agents exist
  for (const agent of expected) {
    if (!agents.includes(agent)) {
      console.log(`⚠️  Missing expected agent: ${domain}/${agent}`);
      warnings++;
    }
  }

  totalAgents += agents.length;
  console.log(`✅ ${domain}/ (${agents.length} agents)`);
}

console.log(`\n📊 Total agents found: ${totalAgents}`);

console.log('\n================================');
if (errors > 0) {
  console.log(`❌ ${errors} error(s), ${warnings} warning(s)`);
  process.exit(1);
} else {
  console.log(`✅ All validations passed (${warnings} warning(s))`);
  process.exit(0);
}
