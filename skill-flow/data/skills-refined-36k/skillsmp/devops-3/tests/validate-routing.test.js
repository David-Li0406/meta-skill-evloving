#!/usr/bin/env node
/**
 * Test: Validate Routing Keywords
 *
 * Validates that:
 * - SKILL.md contains routing information
 * - All domains have keywords defined
 * - Keywords are documented in SKILL.md or orchestrator.md
 *
 * @module tests/validate-routing
 */

const path = require('path');
const {
  safeReadFile,
  TestReporter
} = require('./utils');
const { SKILL_ROOT, DOMAINS, DOMAIN_KEYWORDS } = require('./config');

const reporter = new TestReporter('validate-routing');

reporter.header('Validating DevOps Routing Keywords');

// Read SKILL.md
const skillPath = path.join(SKILL_ROOT, 'SKILL.md');
const { content: skillContent, error: skillError } = safeReadFile(skillPath);

if (skillError) {
  reporter.fail(`Cannot read SKILL.md: ${skillError}`);
  reporter.summarize();
  process.exit(1);
}

reporter.pass('SKILL.md exists and is readable');

// Check routing section exists
if (skillContent.includes('Routing') || skillContent.includes('Routage') || skillContent.includes('Règles')) {
  reporter.pass('SKILL.md contains routing section');
} else {
  reporter.warn('SKILL.md may not have a clear routing section');
}

// Read orchestrator.md
const orchestratorPath = path.join(SKILL_ROOT, 'orchestrator.md');
const { content: orchestratorContent } = safeReadFile(orchestratorPath);

const combinedContent = (skillContent + (orchestratorContent || '')).toLowerCase();

// Check domain keywords
reporter.section('Domain Keywords');

for (const domain of DOMAINS) {
  const keywords = DOMAIN_KEYWORDS[domain] || [];

  if (keywords.length === 0) {
    reporter.warn(`No keywords defined for domain: ${domain}`);
    continue;
  }

  const foundKeywords = keywords.filter(kw =>
    combinedContent.includes(kw.toLowerCase())
  );

  if (foundKeywords.length > 0) {
    reporter.pass(`${domain}: ${foundKeywords.length}/${keywords.length} keywords found`);
  } else {
    reporter.fail(`${domain}: No keywords found in documentation`);
  }
}

// Check for domain references
reporter.section('Domain References');

for (const domain of DOMAINS) {
  if (combinedContent.includes(domain.toLowerCase())) {
    reporter.pass(`${domain} is referenced`);
  } else {
    reporter.fail(`${domain} is not referenced in SKILL.md or orchestrator.md`);
  }
}

reporter.summarize();
