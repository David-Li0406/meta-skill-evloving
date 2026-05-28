#!/usr/bin/env node
/**
 * Test: Validate Agent Files
 *
 * Validates that all expected agent files exist and have required content.
 *
 * @module tests/validate-agents
 */

const path = require('path');
const {
  safeReadFile,
  fileExists,
  TestReporter
} = require('./utils');
const { SKILL_ROOT, DOMAINS, EXPECTED_AGENTS_PER_DOMAIN, AGENT_REQUIREMENTS } = require('./config');

const reporter = new TestReporter('validate-agents');
reporter.header('Validating React Expert Agents');

const agentsDir = path.join(SKILL_ROOT, 'agents');

reporter.section('Agent Files');
let totalAgents = 0;
let foundAgents = 0;

for (const domain of DOMAINS) {
  const expectedAgents = EXPECTED_AGENTS_PER_DOMAIN[domain] || [];
  totalAgents += expectedAgents.length;

  for (const agent of expectedAgents) {
    const agentPath = path.join(agentsDir, domain, `${agent}.md`);

    if (fileExists(agentPath)) {
      foundAgents++;
      const { content, error } = safeReadFile(agentPath);

      if (error) {
        reporter.fail(`${domain}/${agent}: Cannot read file`);
        continue;
      }

      // Check minimum content length
      const minLength = agent === 'orchestrator'
        ? AGENT_REQUIREMENTS.minOrchestratorLength
        : AGENT_REQUIREMENTS.minAgentLength;

      if (content.length >= minLength) {
        reporter.pass(`${domain}/${agent} (${content.length} chars)`);
      } else {
        reporter.warn(`${domain}/${agent}: Content too short (${content.length}/${minLength} chars)`);
      }
    } else {
      reporter.fail(`${domain}/${agent}: File not found`, { path: agentPath });
    }
  }
}

reporter.section('Summary');
if (foundAgents === totalAgents) {
  reporter.pass(`All ${totalAgents} agents found`);
} else {
  reporter.fail(`${foundAgents}/${totalAgents} agents found`);
}

reporter.summarize();
