#!/usr/bin/env node
/**
 * Test: Validate SKILL.md Structure
 *
 * Validates that the main SKILL.md file:
 * - Has valid frontmatter with name, description, version
 * - Documents all domains
 * - Has routing rules
 *
 * @module tests/validate-skill
 */

const path = require('path');
const {
  safeReadFile,
  parseFrontmatter,
  fileExists,
  TestReporter
} = require('./utils');
const { SKILL_ROOT, DOMAINS, getTotalExpectedAgents } = require('./config');

const reporter = new TestReporter('validate-skill');
reporter.header('Validating React Expert SKILL.md');

const skillMdPath = path.join(SKILL_ROOT, 'SKILL.md');

if (!fileExists(skillMdPath)) {
  reporter.fail('SKILL.md not found', { path: skillMdPath });
  reporter.summarize();
}

const { content, error } = safeReadFile(skillMdPath);
if (error) {
  reporter.fail(`Cannot read SKILL.md: ${error}`, { path: skillMdPath });
  reporter.summarize();
}

reporter.section('Frontmatter');
const frontmatter = parseFrontmatter(content);
if (!frontmatter) {
  reporter.fail('Missing or invalid frontmatter');
} else {
  const requiredFields = ['name', 'description', 'version'];
  for (const field of requiredFields) {
    if (frontmatter[field]) {
      reporter.pass(`${field}: ${frontmatter[field]}`, { field, value: frontmatter[field] });
    } else {
      reporter.fail(`Missing ${field}`, { field });
    }
  }
}

reporter.section('Domain Documentation');
let documentedDomains = 0;
const missingDomains = [];

for (const domain of DOMAINS) {
  const headingPattern = new RegExp(`###\\s+\\d+\\.\\s+${domain}\\/`, 'i');
  const tablePattern = new RegExp(`\\|\\s*\`${domain}\\/`, 'i');
  const pathPattern = new RegExp(`${domain}\\/[a-z-]+`, 'i');

  if (headingPattern.test(content) || tablePattern.test(content) || pathPattern.test(content)) {
    documentedDomains++;
  } else {
    missingDomains.push(domain);
  }
}

if (documentedDomains === DOMAINS.length) {
  reporter.pass(`All ${DOMAINS.length} domains documented`, { count: DOMAINS.length });
} else {
  reporter.fail(`${documentedDomains}/${DOMAINS.length} domains documented - Missing: ${missingDomains.join(', ')}`, {
    documented: documentedDomains,
    total: DOMAINS.length,
    missing: missingDomains
  });
}

reporter.section('Essential Sections');
const essentialSections = [
  { name: 'Règles de Routage', pattern: /##\s+Règles de Routage/im },
  { name: 'Points d\'Escalade', pattern: /##\s+Points d'Escalade/im },
  { name: 'Skills Associés', pattern: /##\s+Skills Associés/im }
];

for (const section of essentialSections) {
  if (section.pattern.test(content)) {
    reporter.pass(section.name);
  } else {
    reporter.fail(`${section.name} missing`);
  }
}

reporter.section('Metadata');
const expectedCount = getTotalExpectedAgents();
const agentCountPattern = new RegExp(`${expectedCount}\\s+agents?`, 'i');
const parenPattern = new RegExp(`\\(${expectedCount}\\)`, 'i');

if (agentCountPattern.test(content) || parenPattern.test(content) || content.includes(String(expectedCount))) {
  reporter.pass(`Total agent count mentioned (${expectedCount})`, { expectedAgents: expectedCount });
} else {
  reporter.warn(`Agent count may be outdated (expected ${expectedCount})`);
}

if (frontmatter && frontmatter.name === 'react-expert') {
  reporter.pass('Skill name matches directory');
} else {
  reporter.fail('Skill name should be \'react-expert\'');
}

reporter.summarize();
