#!/usr/bin/env node
/**
 * Test: Validate Domain Structure
 *
 * Validates that each domain has:
 * - A directory under agents/
 * - An orchestrator.md file
 * - Expected agent files
 *
 * @module tests/validate-domains
 */

const path = require('path');
const fs = require('fs');
const {
  findMarkdownFiles,
  directoryExists,
  TestReporter
} = require('./utils');
const { SKILL_ROOT, DOMAINS, EXPECTED_AGENTS_PER_DOMAIN, getTotalExpectedAgents } = require('./config');

const reporter = new TestReporter('validate-domains');

reporter.header('Validating DevOps Domain Structure');

let totalExpected = 0;
let totalFound = 0;

for (const domain of DOMAINS) {
  reporter.section(`Domain: ${domain}`);

  const domainDir = path.join(SKILL_ROOT, 'agents', domain);

  // Check directory exists
  if (!directoryExists(domainDir)) {
    reporter.fail(`Directory not found: agents/${domain}/`);
    continue;
  }

  reporter.pass(`Directory exists: agents/${domain}/`);

  // Check orchestrator exists
  const orchestratorPath = path.join(domainDir, 'orchestrator.md');
  if (fs.existsSync(orchestratorPath)) {
    reporter.pass('orchestrator.md exists');
  } else {
    reporter.fail('orchestrator.md missing');
  }

  // Check expected agents
  const expectedAgents = EXPECTED_AGENTS_PER_DOMAIN[domain] || [];
  const foundFiles = findMarkdownFiles(domainDir).map(f => path.basename(f, '.md'));

  totalExpected += expectedAgents.length;

  for (const agent of expectedAgents) {
    if (foundFiles.includes(agent)) {
      reporter.pass(`${agent}.md`);
      totalFound++;
    } else {
      reporter.fail(`${agent}.md missing`);
    }
  }

  // Check for unexpected files
  const unexpected = foundFiles.filter(f => !expectedAgents.includes(f));
  for (const file of unexpected) {
    reporter.warn(`Unexpected file: ${file}.md`);
  }
}

reporter.info(`Expected agents: ${getTotalExpectedAgents()}`);
reporter.info(`Found agents: ${totalFound}/${totalExpected}`);
reporter.summarize();
