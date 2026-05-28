#!/usr/bin/env node
/**
 * Test: Validate Domain Structure for AI Integration skill
 *
 * @module tests/validate-domains
 */

const path = require('path');
const { directoryExists, findMarkdownFiles, TestReporter } = require('./utils');
const { SKILL_ROOT, DOMAINS, EXPECTED_AGENTS_PER_DOMAIN } = require('./config');

const reporter = new TestReporter('validate-domains');

reporter.header('Validating AI Integration Domain Structure');

for (const domain of DOMAINS) {
  reporter.section(`Domain: ${domain}`);

  const domainDir = path.join(SKILL_ROOT, 'agents', domain);

  // Check domain directory exists
  if (!directoryExists(domainDir)) {
    reporter.fail(`Directory not found: agents/${domain}/`);
    continue;
  }
  reporter.pass(`Directory exists: agents/${domain}/`);

  // Check expected agents
  const expectedAgents = EXPECTED_AGENTS_PER_DOMAIN[domain] || [];
  const actualFiles = findMarkdownFiles(domainDir)
    .map(f => path.basename(f, '.md'));

  for (const agent of expectedAgents) {
    if (actualFiles.includes(agent)) {
      reporter.pass(`Agent found: ${agent}.md`);
    } else {
      reporter.fail(`Missing agent: ${agent}.md`);
    }
  }

  // Check for orchestrator
  if (!actualFiles.includes('orchestrator')) {
    reporter.warn(`No orchestrator.md in ${domain}/`);
  }
}

reporter.summarize();
