#!/usr/bin/env node
/**
 * Test: Validate Agent Structure
 * Validates that each agent file follows the required structure.
 * @module tests/validate-agents
 */

const path = require('path');
const {
  findMarkdownFiles,
  safeReadFile,
  parseFrontmatter,
  directoryExists,
  countTechElements,
  TestReporter
} = require('./utils');
const { SKILL_ROOT, DOMAINS, AGENT_REQUIREMENTS } = require('./config');

const reporter = new TestReporter('validate-agents');

function validateAgent(filePath) {
  const errors = [];
  const warns = [];
  const isOrchestrator = filePath.includes('orchestrator');

  const { content, error } = safeReadFile(filePath);
  if (error) {
    return { errors: [error], warnings: [] };
  }

  // Check frontmatter
  const frontmatter = parseFrontmatter(content);
  if (!frontmatter) {
    errors.push('Missing YAML frontmatter');
  } else {
    for (const field of AGENT_REQUIREMENTS.frontmatter) {
      if (!frontmatter[field]) {
        errors.push(`Missing "${field}" in frontmatter`);
      }
    }
  }

  // Check main heading
  if (!content.match(/^#\s+.+/m)) {
    errors.push('Missing main heading (# Title)');
  }

  // Check minimum content length
  const minLength = isOrchestrator
    ? AGENT_REQUIREMENTS.minOrchestratorLength
    : AGENT_REQUIREMENTS.minAgentLength;

  if (content.length < minLength) {
    errors.push(`Content too short (${content.length} < ${minLength} chars)`);
  }

  // Check expected sections
  if (!isOrchestrator) {
    for (const section of AGENT_REQUIREMENTS.agentSections || []) {
      if (!content.includes(section)) {
        warns.push(`Missing recommended section: "${section}"`);
      }
    }
  }

  // Check for code blocks or tables
  const techElements = countTechElements(content);
  if (techElements.codeBlocks === 0 && techElements.tables === 0) {
    warns.push('No code blocks or tables found');
  }

  return { errors, warnings: warns };
}

reporter.header('Validating Lead Dev Agent Structure');

let totalAgents = 0;

for (const domain of DOMAINS) {
  const domainDir = path.join(SKILL_ROOT, 'agents', domain);

  if (!directoryExists(domainDir)) {
    reporter.warn(`Domain directory not found: ${domain}`);
    continue;
  }

  reporter.section(`Domain: ${domain}`);

  const files = findMarkdownFiles(domainDir);
  totalAgents += files.length;

  for (const file of files) {
    const relativePath = path.relative(SKILL_ROOT, file);
    const { errors, warnings } = validateAgent(file);

    if (errors.length === 0) {
      if (warnings.length === 0) {
        reporter.pass(relativePath);
      } else {
        reporter.pass(`${relativePath} (${warnings.length} warning${warnings.length > 1 ? 's' : ''})`);
      }
    } else {
      reporter.fail(`${relativePath}: ${errors.join(', ')}`);
    }
  }
}

reporter.info(`Total agents validated: ${totalAgents}`);
reporter.summarize();
