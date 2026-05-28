#!/usr/bin/env node
/**
 * Test: Validate SKILL.md
 *
 * Validates that the main SKILL.md orchestrator:
 * - Has proper frontmatter
 * - Documents all WordPress domains
 * - Has routing rules with WordPress keywords
 * - References web-dev-process composition
 *
 * @module tests/validate-skill
 */

const path = require('path');
const {
  safeReadFile,
  parseFrontmatter,
  fileExists,
  printSeparator,
  escapeRegex,
  TestError
} = require('./utils');
const { SKILL_ROOT, DOMAINS, STANDALONE_AGENTS } = require('./config');

let passed = 0;
let failed = 0;

console.log('🧪 Validating SKILL.md\n');
printSeparator();

const skillPath = path.join(SKILL_ROOT, 'SKILL.md');

// Check SKILL.md exists
if (!fileExists(skillPath)) {
  console.error(`❌ SKILL.md not found at: ${skillPath}`);
  throw new TestError('SKILL.md not found', { path: skillPath });
}
console.log('✅ SKILL.md exists');
passed++;

const { content, error } = safeReadFile(skillPath);
if (error) {
  console.error(`❌ Cannot read SKILL.md: ${error}`);
  throw new TestError(`Cannot read SKILL.md: ${error}`, { path: skillPath });
}

// Check frontmatter
console.log('\n📋 Frontmatter:');
const frontmatter = parseFrontmatter(content);
if (!frontmatter) {
  console.log('  ❌ Missing frontmatter');
  failed++;
} else {
  if (frontmatter.name) {
    console.log(`  ✅ name: ${frontmatter.name}`);
    passed++;
  } else {
    console.log('  ❌ Missing name');
    failed++;
  }

  if (frontmatter.description) {
    const desc = frontmatter.description.substring(0, 60);
    console.log(`  ✅ description: ${desc}...`);
    passed++;
  } else {
    console.log('  ❌ Missing description');
    failed++;
  }
}

// Check domains are documented
console.log('\n📁 Domains documented:');
for (const domain of DOMAINS) {
  // Escape special regex characters first, then handle hyphen-to-space pattern
  const escapedDomain = escapeRegex(domain).replace(/-/g, '[-\\s]');
  const domainRegex = new RegExp(escapedDomain, 'i');
  if (domainRegex.test(content)) {
    console.log(`  ✅ ${domain}`);
    passed++;
  } else {
    console.log(`  ❌ ${domain} not mentioned`);
    failed++;
  }
}

// Check standalone agents mentioned
console.log('\n👤 Standalone agents:');
let standaloneFound = 0;
for (const agent of STANDALONE_AGENTS) {
  if (content.includes(agent) || content.includes(agent.replace(/-/g, ' '))) {
    standaloneFound++;
  }
}
if (standaloneFound >= 3) {
  console.log(`  ✅ ${standaloneFound}/${STANDALONE_AGENTS.length} standalone agents referenced`);
  passed++;
} else {
  console.log(`  ⚠️  Only ${standaloneFound}/${STANDALONE_AGENTS.length} standalone agents referenced`);
}

// Check routing section
console.log('\n🔀 Routing:');
if (content.includes('Routage') || content.includes('Routing')) {
  console.log('  ✅ Routing section present');
  passed++;
} else {
  console.log('  ❌ Routing section missing');
  failed++;
}

// Check WordPress keywords in routing
const wpKeywords = ['CPT', 'taxonomy', 'block', 'theme.json', 'Gutenberg', 'WP-CLI'];
let keywordsFound = 0;
for (const keyword of wpKeywords) {
  if (content.includes(keyword)) {
    keywordsFound++;
  }
}
if (keywordsFound >= 4) {
  console.log(`  ✅ WordPress keywords present (${keywordsFound}/${wpKeywords.length})`);
  passed++;
} else {
  console.log(`  ⚠️  Few WordPress keywords (${keywordsFound}/${wpKeywords.length})`);
}

// Check composition with web-dev-process
console.log('\n🔗 Composition:');
if (content.includes('web-dev-process')) {
  console.log('  ✅ References web-dev-process');
  passed++;
} else {
  console.log('  ⚠️  Does not reference web-dev-process');
}

// Check WordPress documentation sources
console.log('\n📚 Documentation Sources:');
if (content.includes('developer.wordpress.org')) {
  console.log('  ✅ WordPress developer docs referenced');
  passed++;
} else {
  console.log('  ⚠️  WordPress developer docs not referenced');
}

if (content.includes('github.com/WordPress')) {
  console.log('  ✅ WordPress GitHub referenced');
  passed++;
}

console.log('\n');
printSeparator();
console.log(`\n📊 Results: ${passed} passed, ${failed} failed`);

if (failed > 0) {
  console.log('\n❌ Some tests failed');
  // Use process.exit for test runner compatibility, but with clear message
  process.exit(1);
} else {
  console.log('\n✅ All tests passed');
  process.exit(0);
}

// Export for test runner integration
module.exports = { passed, failed };
