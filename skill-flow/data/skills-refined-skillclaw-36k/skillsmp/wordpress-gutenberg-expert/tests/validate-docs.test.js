#!/usr/bin/env node
/**
 * Test: Validate Documentation Files
 *
 * Validates that documentation exists and is complete:
 * - docs/ directory with guides
 * - CHANGELOG.md
 * - references/ if present
 *
 * @module tests/validate-docs
 */

const path = require('path');
const fs = require('fs');
const {
  directoryExists,
  fileExists,
  safeReadFile,
  findMarkdownFiles,
  printSeparator
} = require('./utils');
const { SKILL_ROOT, DOCS_DIR, REFERENCES_DIR } = require('./config');

let passed = 0;
let failed = 0;

console.log('🧪 Validating Documentation\n');
printSeparator();

// Check CHANGELOG.md
console.log('\n📄 Core Documentation:');
const changelogPath = path.join(SKILL_ROOT, 'CHANGELOG.md');
if (fileExists(changelogPath)) {
  const { content } = safeReadFile(changelogPath);
  if (content && content.length > 100) {
    console.log('  ✅ CHANGELOG.md exists and has content');
    passed++;
  } else {
    console.log('  ⚠️  CHANGELOG.md exists but is short');
  }
} else {
  console.log('  ❌ CHANGELOG.md missing');
  failed++;
}

// Check docs directory
console.log('\n📁 Documentation Directory:');
if (directoryExists(DOCS_DIR)) {
  console.log('  ✅ docs/ directory exists');
  passed++;

  const docFiles = findMarkdownFiles(DOCS_DIR);
  console.log(`  📄 Found ${docFiles.length} documentation file(s)`);

  // Check for common doc files
  const expectedDocs = ['getting-started', 'troubleshooting', 'migration'];
  for (const doc of expectedDocs) {
    const found = docFiles.some(f => f.toLowerCase().includes(doc));
    if (found) {
      console.log(`     ✅ ${doc} guide found`);
      passed++;
    } else {
      console.log(`     ⚠️  ${doc} guide not found`);
    }
  }
} else {
  console.log('  ⚠️  docs/ directory not found');
}

// Check references directory (optional)
console.log('\n📁 References Directory:');
if (directoryExists(REFERENCES_DIR)) {
  console.log('  ✅ references/ directory exists');
  passed++;

  try {
    const refFiles = fs.readdirSync(REFERENCES_DIR);
    console.log(`  📄 Found ${refFiles.length} reference file(s)`);

    for (const file of refFiles.slice(0, 5)) {
      console.log(`     - ${file}`);
    }
    if (refFiles.length > 5) {
      console.log(`     ... and ${refFiles.length - 5} more`);
    }
  } catch (err) {
    console.log(`  ⚠️  Cannot read references directory`);
  }
} else {
  console.log('  ⚠️  references/ directory not found (optional)');
}

// Validate doc content quality
console.log('\n📝 Documentation Quality:');
if (directoryExists(DOCS_DIR)) {
  const docFiles = findMarkdownFiles(DOCS_DIR);
  let goodDocs = 0;

  for (const file of docFiles) {
    const { content } = safeReadFile(file);
    if (content && content.length > 500) {
      goodDocs++;
    }
  }

  if (goodDocs === docFiles.length && docFiles.length > 0) {
    console.log(`  ✅ All ${docFiles.length} docs have substantial content`);
    passed++;
  } else if (docFiles.length > 0) {
    console.log(`  ⚠️  ${goodDocs}/${docFiles.length} docs have substantial content`);
  }
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
