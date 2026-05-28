#!/usr/bin/env node
/**
 * Test: Validate Agent Structure for direction-operations
 *
 * Validates that each operations agent file follows the required structure:
 * - Valid YAML frontmatter with name and description
 * - Main heading (H1)
 * - Minimum content length
 * - Expected sections based on agent type
 *
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

/**
 * Validate a single agent file
 *
 * @param {string} filePath - Path to the agent file
 * @returns {{ errors: string[], warnings: string[] }} Validation results
 */
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

  // Check minimum content length - different thresholds
  const minLength = isOrchestrator
    ? AGENT_REQUIREMENTS.minOrchestratorLength
    : AGENT_REQUIREMENTS.minAgentLength;

  if (content.length < minLength) {
    errors.push(`Content too short (${content.length} < ${minLength} chars for ${isOrchestrator ? 'orchestrator' : 'agent'})`);
  }

  // Check expected sections based on type
  if (isOrchestrator) {
    for (const section of AGENT_REQUIREMENTS.orchestratorSections || []) {
      if (!content.includes(section)) {
        warns.push(`Missing recommended section: "${section}"`);
      }
    }
  }

  // Check for code blocks or tables (quality indicator)
  const techElements = countTechElements(content);
  if (techElements.codeBlocks === 0 && techElements.tables === 0) {
    warns.push('No code blocks or tables found');
  }

  return { errors, warnings: warns };
}

// Main execution
reporter.header('Validating Direction Operations Agent Structure');

let totalAgents = 0;
let totalWarnings = 0;

// Validate domain agents
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
    const { errors, warnings: fileWarnings } = validateAgent(file);

    if (errors.length === 0) {
      if (fileWarnings.length === 0) {
        reporter.pass(relativePath, { domain, file: relativePath });
      } else {
        reporter.pass(`${relativePath} (${fileWarnings.length} warning${fileWarnings.length > 1 ? 's' : ''})`, {
          domain,
          file: relativePath,
          warnings: fileWarnings
        });
        totalWarnings += fileWarnings.length;
      }
    } else {
      reporter.fail(`${relativePath}: ${errors.join(', ')}`, {
        domain,
        file: relativePath,
        errors
      });
    }
  }
}

reporter.info(`Total agents validated: ${totalAgents}`);
reporter.info(`Content thresholds: Orchestrators=${AGENT_REQUIREMENTS.minOrchestratorLength}, Agents=${AGENT_REQUIREMENTS.minAgentLength}`);
reporter.summarize();
