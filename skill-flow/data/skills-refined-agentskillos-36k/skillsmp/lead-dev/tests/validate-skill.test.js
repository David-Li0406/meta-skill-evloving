#!/usr/bin/env node
/**
 * Test: Validate SKILL.md
 * Validates that the main SKILL.md file exists and has required content.
 * @module tests/validate-skill
 */

const path = require('path');
const { safeReadFile, parseFrontmatter, fileExists, TestReporter } = require('./utils');
const { SKILL_ROOT, DOMAINS } = require('./config');

const reporter = new TestReporter('validate-skill');

reporter.header('Validating Lead Dev SKILL.md');

const skillFile = path.join(SKILL_ROOT, 'SKILL.md');

// Check SKILL.md exists
if (!fileExists(skillFile)) {
  reporter.fail('SKILL.md not found');
  reporter.summarize();
}

reporter.pass('SKILL.md exists');

// Read and validate content
const { content, error } = safeReadFile(skillFile);
if (error) {
  reporter.fail(`Cannot read SKILL.md: ${error}`);
  reporter.summarize();
}

// Check frontmatter
const frontmatter = parseFrontmatter(content);
if (!frontmatter) {
  reporter.fail('Missing frontmatter in SKILL.md');
} else {
  const requiredFields = ['name', 'description', 'version', 'status'];
  for (const field of requiredFields) {
    if (frontmatter[field]) {
      reporter.pass(`Frontmatter has "${field}": ${frontmatter[field]}`);
    } else {
      reporter.fail(`Missing "${field}" in frontmatter`);
    }
  }
}

// Check required sections
const requiredSections = [
  'Position dans l\'Architecture',
  'Philosophie',
  'Domaines et Agents',
  'Règles de Routage',
  'Points d\'Escalade'
];

for (const section of requiredSections) {
  if (content.includes(section)) {
    reporter.pass(`Section found: "${section}"`);
  } else {
    reporter.fail(`Missing section: "${section}"`);
  }
}

// Check all domains are mentioned
reporter.section('Domain references');
for (const domain of DOMAINS) {
  if (content.includes(domain)) {
    reporter.pass(`Domain "${domain}" referenced`);
  } else {
    reporter.fail(`Domain "${domain}" not referenced in SKILL.md`);
  }
}

// Check orchestrator.md exists
const orchestratorFile = path.join(SKILL_ROOT, 'orchestrator.md');
if (fileExists(orchestratorFile)) {
  reporter.pass('orchestrator.md exists');
} else {
  reporter.fail('orchestrator.md not found');
}

reporter.summarize();
