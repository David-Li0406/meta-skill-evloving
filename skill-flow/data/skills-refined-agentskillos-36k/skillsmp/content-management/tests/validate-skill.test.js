#!/usr/bin/env node
/**
 * Test: Validate Skill Definition
 *
 * Validates the main SKILL.md file structure and content
 *
 * @module tests/validate-skill
 */

const path = require('path');
const {
  safeReadFile,
  parseFrontmatter,
  fileExists,
  printSeparator
} = require('./utils');
const { SKILL_ROOT, EXPECTED_DOMAINS } = require('./config');

// Test results
let passed = 0;
let failed = 0;

const SKILL_FILE = path.join(SKILL_ROOT, 'SKILL.md');

// Main execution
console.log('🧪 Validating SKILL.md\n');
printSeparator();

if (!fileExists(SKILL_FILE)) {
  console.error('❌ SKILL.md not found');
  process.exit(1);
}

const { content, error } = safeReadFile(SKILL_FILE);
if (error) {
  console.error(`❌ Cannot read SKILL.md: ${error}`);
  process.exit(1);
}

// Test: Frontmatter exists
const frontmatter = parseFrontmatter(content);
if (frontmatter) {
  console.log('✅ Frontmatter present');
  passed++;

  // Test: Required frontmatter fields
  const requiredFields = ['name', 'description', 'version'];
  for (const field of requiredFields) {
    if (frontmatter[field]) {
      console.log(`✅ Frontmatter has "${field}": ${frontmatter[field]}`);
      passed++;
    } else {
      console.log(`❌ Missing frontmatter field: ${field}`);
      failed++;
    }
  }

  // Test: ecosystem_version (recommended)
  if (frontmatter['ecosystem_version']) {
    console.log(`✅ Frontmatter has "ecosystem_version": ${frontmatter['ecosystem_version']}`);
    passed++;
  } else {
    console.log('⚠️  Missing recommended field: ecosystem_version');
  }
} else {
  console.log('❌ Missing frontmatter');
  failed++;
}

// Test: Main heading
if (content.match(/^#\s+Content Management/m)) {
  console.log('✅ Main heading present');
  passed++;
} else {
  console.log('❌ Missing or incorrect main heading');
  failed++;
}

// Test: Domains section
if (content.includes('## Domaines')) {
  console.log('✅ Domains section present');
  passed++;

  // Check each expected domain is mentioned
  for (const domain of EXPECTED_DOMAINS) {
    if (content.includes(`\`${domain}\``)) {
      console.log(`✅ Domain "${domain}" documented`);
      passed++;
    } else {
      console.log(`❌ Domain "${domain}" not documented`);
      failed++;
    }
  }
} else {
  console.log('❌ Missing Domains section');
  failed++;
}

// Test: Position in hierarchy
if (content.includes('## Position dans la Hiérarchie')) {
  console.log('✅ Hierarchy section present');
  passed++;
} else {
  console.log('❌ Missing Hierarchy section');
  failed++;
}

// Test: Coordination section
if (content.includes('## Coordination avec Autres Skills')) {
  console.log('✅ Coordination section present');
  passed++;
} else {
  console.log('❌ Missing Coordination section');
  failed++;
}

// Test: Marketing boundary clarification
if (content.includes('## Content Management vs Marketing')) {
  console.log('✅ Marketing boundary section present');
  passed++;
} else {
  console.log('⚠️  Missing Marketing boundary clarification section');
}

// Test: Livrables section
if (content.includes('## Livrables')) {
  console.log('✅ Livrables section present');
  passed++;
} else {
  console.log('❌ Missing Livrables section');
  failed++;
}

console.log('\n');
printSeparator();
console.log(`\n📊 Results: ${passed} passed, ${failed} failed`);

if (failed > 0) {
  console.log('\n❌ Some tests failed');
  process.exit(1);
} else {
  console.log('\n✅ All tests passed');
  process.exit(0);
}
