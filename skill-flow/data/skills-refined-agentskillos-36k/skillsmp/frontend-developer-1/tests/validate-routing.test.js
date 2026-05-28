#!/usr/bin/env node
/**
 * Test: Validate Routing Keywords
 *
 * Validates that domain keywords are documented in SKILL.md routing rules.
 *
 * @module tests/validate-routing
 */

const path = require('path');
const {
  safeReadFile,
  fileExists,
  TestReporter
} = require('./utils');
const { SKILL_ROOT, DOMAIN_KEYWORDS } = require('./config');

const reporter = new TestReporter('validate-routing');
reporter.header('Validating Frontend Developer Routing');

const skillMdPath = path.join(SKILL_ROOT, 'SKILL.md');

if (!fileExists(skillMdPath)) {
  reporter.fail('SKILL.md not found');
  reporter.summarize();
}

const { content, error } = safeReadFile(skillMdPath);
if (error) {
  reporter.fail(`Cannot read SKILL.md: ${error}`);
  reporter.summarize();
}

// Extract routing section (from "## Règles de Routage" to next "## " level-2 heading)
const routingMatch = content.match(/## Règles de Routage[\s\S]*?(?=\n## [^#]|$)/i);
const routingSection = routingMatch ? routingMatch[0].toLowerCase() : content.toLowerCase();

reporter.section('Keyword Coverage');

for (const [domain, keywords] of Object.entries(DOMAIN_KEYWORDS)) {
  const foundKeywords = [];
  const missingKeywords = [];

  for (const keyword of keywords) {
    if (routingSection.includes(keyword.toLowerCase())) {
      foundKeywords.push(keyword);
    } else {
      missingKeywords.push(keyword);
    }
  }

  const coverage = foundKeywords.length / keywords.length;

  if (coverage >= 0.5) {
    reporter.pass(`${domain}: ${foundKeywords.length}/${keywords.length} keywords (${Math.round(coverage * 100)}%)`);
  } else if (coverage > 0) {
    reporter.warn(`${domain}: ${foundKeywords.length}/${keywords.length} keywords - Missing: ${missingKeywords.join(', ')}`);
  } else {
    reporter.fail(`${domain}: No keywords found - Expected: ${keywords.join(', ')}`);
  }
}

reporter.section('Routing Patterns');

// Check for SI/ALORS pattern or similar
const hasConditionalRouting = /si\s+.*→|if\s+.*→|contient\s*\[/i.test(content);
if (hasConditionalRouting) {
  reporter.pass('Conditional routing patterns found');
} else {
  reporter.warn('No clear conditional routing patterns (SI...→)');
}

// Check for domain references
const domainRefs = content.match(/→\s*[a-z-]+\/[a-z-]+/gi) || [];
if (domainRefs.length > 0) {
  reporter.pass(`${domainRefs.length} routing targets found`);
} else {
  reporter.warn('No routing targets found (domain/agent pattern)');
}

reporter.summarize();
