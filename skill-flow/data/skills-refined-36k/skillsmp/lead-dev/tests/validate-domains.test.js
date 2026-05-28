#!/usr/bin/env node
/**
 * Test: Validate Domain Structure
 * Validates that all expected domains exist with their agent files.
 * @module tests/validate-domains
 */

const path = require('path');
const { directoryExists, fileExists, TestReporter } = require('./utils');
const { SKILL_ROOT, DOMAINS, EXPECTED_AGENTS_PER_DOMAIN } = require('./config');

const reporter = new TestReporter('validate-domains');

reporter.header('Validating Lead Dev Domain Structure');

let totalExpected = 0;
let totalFound = 0;

for (const domain of DOMAINS) {
  reporter.section(`Domain: ${domain}`);

  const domainDir = path.join(SKILL_ROOT, 'agents', domain);

  if (!directoryExists(domainDir)) {
    reporter.fail(`Domain directory not found: ${domain}`);
    continue;
  }

  reporter.pass(`Domain directory exists: ${domain}`);

  const expectedAgents = EXPECTED_AGENTS_PER_DOMAIN[domain] || [];
  totalExpected += expectedAgents.length;

  for (const agent of expectedAgents) {
    const agentFile = path.join(domainDir, `${agent}.md`);

    if (fileExists(agentFile)) {
      reporter.pass(`${domain}/${agent}.md`);
      totalFound++;
    } else {
      reporter.fail(`Missing agent: ${domain}/${agent}.md`);
    }
  }
}

reporter.info(`Found ${totalFound}/${totalExpected} expected agents`);
reporter.summarize();
