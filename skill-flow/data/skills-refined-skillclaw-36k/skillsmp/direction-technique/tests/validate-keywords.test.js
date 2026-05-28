#!/usr/bin/env node
/**
 * Test: Validate Keyword Coverage
 *
 * Validates that:
 * - Domain keywords in config match SKILL.md routing rules
 * - Each domain has keywords defined
 * - Keywords are not duplicated across domains
 *
 * @module tests/validate-keywords
 */

const path = require('path');
const {
  safeReadFile,
  TestReporter
} = require('./utils');
const { SKILL_ROOT, DOMAINS, DOMAIN_KEYWORDS } = require('./config');

const reporter = new TestReporter('validate-keywords');
reporter.header('Validating Keyword Coverage');

// 1. Check that all domains have keywords defined
reporter.section('Domain Keyword Definitions');

let domainsWithKeywords = 0;
const missingKeywordDomains = [];

for (const domain of DOMAINS) {
  if (DOMAIN_KEYWORDS[domain] && DOMAIN_KEYWORDS[domain].length > 0) {
    domainsWithKeywords++;
  } else {
    missingKeywordDomains.push(domain);
  }
}

if (missingKeywordDomains.length === 0) {
  reporter.pass(`All ${DOMAINS.length} domains have keywords defined`, { count: DOMAINS.length });
} else {
  reporter.fail(`${missingKeywordDomains.length} domains missing keywords: ${missingKeywordDomains.join(', ')}`, {
    missing: missingKeywordDomains
  });
}

// 2. Check for duplicate keywords across domains
reporter.section('Keyword Uniqueness');

const allKeywords = new Map(); // keyword -> [domains]
const duplicates = [];

for (const domain of DOMAINS) {
  const keywords = DOMAIN_KEYWORDS[domain] || [];
  for (const keyword of keywords) {
    const normalizedKeyword = keyword.toLowerCase();
    if (!allKeywords.has(normalizedKeyword)) {
      allKeywords.set(normalizedKeyword, []);
    }
    allKeywords.get(normalizedKeyword).push(domain);
  }
}

for (const [keyword, domains] of allKeywords) {
  if (domains.length > 1) {
    duplicates.push({ keyword, domains });
  }
}

if (duplicates.length === 0) {
  reporter.pass('No duplicate keywords across domains');
} else {
  reporter.warn(`${duplicates.length} keywords appear in multiple domains (may be intentional)`);
}

// 3. Check SKILL.md contains domain routing keywords
reporter.section('SKILL.md Keyword Coverage');

const skillMdPath = path.join(SKILL_ROOT, 'SKILL.md');
const { content: skillContent } = safeReadFile(skillMdPath);

if (skillContent) {
  let coveredDomains = 0;
  const uncoveredDomains = [];

  for (const domain of DOMAINS) {
    const keywords = DOMAIN_KEYWORDS[domain] || [];
    let hasKeywordInSkillMd = false;

    for (const keyword of keywords) {
      if (skillContent.toLowerCase().includes(keyword.toLowerCase())) {
        hasKeywordInSkillMd = true;
        break;
      }
    }

    const domainPattern = new RegExp(`\\|.*${domain}.*\\|`, 'i');
    const domainMentioned = domainPattern.test(skillContent);

    if (hasKeywordInSkillMd || domainMentioned) {
      coveredDomains++;
    } else {
      uncoveredDomains.push(domain);
    }
  }

  if (uncoveredDomains.length === 0) {
    reporter.pass('All domains have keyword coverage in SKILL.md', { covered: coveredDomains });
  } else {
    reporter.warn(`${uncoveredDomains.length} domains may lack keyword coverage: ${uncoveredDomains.join(', ')}`);
  }
}

// 4. Check orchestrators contain their domain keywords
reporter.section('Orchestrator Keyword Coverage');

let orchestratorsWithKeywords = 0;
const orchestratorsMissingKeywords = [];

for (const domain of DOMAINS) {
  const orchestratorPath = path.join(SKILL_ROOT, domain, 'orchestrator.md');
  const { content } = safeReadFile(orchestratorPath);

  if (!content) {
    orchestratorsMissingKeywords.push(domain);
    continue;
  }

  const keywords = DOMAIN_KEYWORDS[domain] || [];
  let keywordsFound = 0;

  for (const keyword of keywords) {
    if (content.toLowerCase().includes(keyword.toLowerCase())) {
      keywordsFound++;
    }
  }

  const threshold = Math.ceil(keywords.length * 0.5);
  if (keywordsFound >= threshold || keywords.length === 0) {
    orchestratorsWithKeywords++;
  } else {
    orchestratorsMissingKeywords.push(`${domain} (${keywordsFound}/${keywords.length})`);
  }
}

if (orchestratorsMissingKeywords.length === 0) {
  reporter.pass('All orchestrators have adequate keyword coverage', { count: orchestratorsWithKeywords });
} else {
  reporter.warn(`Some orchestrators may need keyword updates: ${orchestratorsMissingKeywords.slice(0, 3).join(', ')}`);
}

// 5. Keyword statistics (info only)
const totalKeywords = Array.from(allKeywords.keys()).length;
reporter.info(`Statistics: ${totalKeywords} unique keywords across ${domainsWithKeywords} domains`);

reporter.summarize();
