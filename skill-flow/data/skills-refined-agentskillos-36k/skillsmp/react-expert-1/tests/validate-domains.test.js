#!/usr/bin/env node
/**
 * Test: Validate Domain Structure
 *
 * Validates that all domains exist and have orchestrators.
 *
 * @module tests/validate-domains
 */

const path = require('path');
const {
  directoryExists,
  fileExists,
  safeReadFile,
  TestReporter
} = require('./utils');
const { SKILL_ROOT, DOMAINS } = require('./config');

const reporter = new TestReporter('validate-domains');
reporter.header('Validating React Expert Domains');

const agentsDir = path.join(SKILL_ROOT, 'agents');

reporter.section('Domain Directories');
let foundDomains = 0;

for (const domain of DOMAINS) {
  const domainPath = path.join(agentsDir, domain);

  if (directoryExists(domainPath)) {
    foundDomains++;
    reporter.pass(`${domain}/ exists`);
  } else {
    reporter.fail(`${domain}/ not found`, { path: domainPath });
  }
}

reporter.section('Orchestrators');
let foundOrchestrators = 0;

for (const domain of DOMAINS) {
  const orchestratorPath = path.join(agentsDir, domain, 'orchestrator.md');

  if (fileExists(orchestratorPath)) {
    foundOrchestrators++;
    const { content } = safeReadFile(orchestratorPath);

    // Check for routing rules
    if (content && /règles de routage|routing|agents disponibles/i.test(content)) {
      reporter.pass(`${domain}/orchestrator.md has routing`);
    } else {
      reporter.warn(`${domain}/orchestrator.md may lack routing rules`);
    }
  } else {
    reporter.fail(`${domain}/orchestrator.md not found`);
  }
}

reporter.section('Summary');
reporter.info(`Domains: ${foundDomains}/${DOMAINS.length}`);
reporter.info(`Orchestrators: ${foundOrchestrators}/${DOMAINS.length}`);

if (foundDomains === DOMAINS.length && foundOrchestrators === DOMAINS.length) {
  reporter.pass('All domains properly structured');
}

reporter.summarize();
