#!/usr/bin/env node
/**
 * Test: Validate Domain Structure for Security Expert skill
 */

const path = require('path');
const { directoryExists, findMarkdownFiles, TestReporter } = require('./utils');
const { SKILL_ROOT, DOMAINS, EXPECTED_AGENTS_PER_DOMAIN } = require('./config');

const reporter = new TestReporter('validate-domains');

reporter.header('Validating Security Expert Domain Structure');

for (const domain of DOMAINS) {
  reporter.section(`Domain: ${domain}`);

  const domainDir = path.join(SKILL_ROOT, 'agents', domain);

  if (!directoryExists(domainDir)) {
    reporter.fail(`Directory not found: agents/${domain}/`);
    continue;
  }
  reporter.pass(`Directory exists: agents/${domain}/`);

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

  if (!actualFiles.includes('orchestrator')) {
    reporter.warn(`No orchestrator.md in ${domain}/`);
  }
}

reporter.summarize();
