#!/usr/bin/env node
/**
 * Test: Validate Domain Structure
 *
 * Validates that each technical domain:
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
  TestReporter
} = require('./utils');
const { SKILL_ROOT, DOMAINS, EXPECTED_AGENTS_PER_DOMAIN, getTotalExpectedAgents } = require('./config');

const reporter = new TestReporter('validate-domains');
reporter.header('Validating Technical Domain Structure');

// Check each domain
for (const domain of DOMAINS) {
  reporter.section(`Domain: ${domain}`);

  const domainDir = path.join(SKILL_ROOT, 'agents', domain);

  // Check domain directory exists
  if (!directoryExists(domainDir)) {
    reporter.fail(`Directory missing: ${domain}/`, { domain, path: domainDir });
    continue;
  }
  reporter.pass('Directory exists', { domain });

  // Check orchestrator exists
  const orchestratorPath = path.join(domainDir, 'orchestrator.md');
  if (!fileExists(orchestratorPath)) {
    reporter.fail(`Orchestrator missing: ${domain}/orchestrator.md`, { domain, path: orchestratorPath });
  } else {
    reporter.pass('Orchestrator exists', { domain });
  }

  // Check expected agents
  const expectedAgents = EXPECTED_AGENTS_PER_DOMAIN[domain] || [];
  let agentsMissing = [];

  for (const agent of expectedAgents) {
    if (agent === 'orchestrator') continue;

    const agentPath = path.join(domainDir, `${agent}.md`);
    if (!fileExists(agentPath)) {
      agentsMissing.push(agent);
    }
  }

  const expectedCount = expectedAgents.length - 1; // -1 for orchestrator
  if (agentsMissing.length === 0) {
    reporter.pass(`All ${expectedCount} expected agents present`, { domain, count: expectedCount });
  } else {
    reporter.fail(`Missing ${agentsMissing.length}/${expectedCount} agents: ${agentsMissing.join(', ')}`, {
      domain,
      missing: agentsMissing
    });
  }
}

// Check SKILL.md exists
reporter.section('Main Files');
const skillMdPath = path.join(SKILL_ROOT, 'SKILL.md');
if (fileExists(skillMdPath)) {
  reporter.pass('SKILL.md exists');
} else {
  reporter.fail('SKILL.md missing', { path: skillMdPath });
}

reporter.summarize();
