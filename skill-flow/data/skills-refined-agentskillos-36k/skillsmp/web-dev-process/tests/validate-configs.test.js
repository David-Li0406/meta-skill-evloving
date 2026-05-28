#!/usr/bin/env node
/**
 * Test: Validate Configuration Files
 *
 * Validates that configuration examples exist and are valid:
 * - ESLint config
 * - Prettier config
 * - Commitlint config
 * - Git hooks config
 *
 * @module tests/validate-configs
 */

const path = require('path');
const {
  directoryExists,
  fileExists,
  safeReadFile,
  printSeparator
} = require('./utils');
const { CONFIGS_DIR } = require('./config');

let passed = 0;
let failed = 0;

console.log('🧪 Validating Configuration Files\n');
printSeparator();

// Check configs directory exists
if (!directoryExists(CONFIGS_DIR)) {
  console.log('⚠️  Configs directory not found, skipping...');
  console.log('\n✅ Test skipped (no configs directory)');
  process.exit(0);
}

console.log('✅ Configs directory exists\n');
passed++;

// Expected configuration files
const expectedConfigs = [
  { name: 'ESLint', patterns: ['eslint', '.eslintrc'] },
  { name: 'Prettier', patterns: ['prettier', '.prettierrc'] },
  { name: 'Commitlint', patterns: ['commitlint'] },
  { name: 'Lefthook/Husky', patterns: ['lefthook', 'husky', 'hooks'] }
];

const fs = require('fs');
let configFiles = [];

try {
  configFiles = fs.readdirSync(CONFIGS_DIR);
} catch (err) {
  console.log(`❌ Cannot read configs directory: ${err.message}`);
  process.exit(1);
}

console.log(`Found ${configFiles.length} config file(s)\n`);

// Check each expected config
for (const config of expectedConfigs) {
  const found = configFiles.some(file =>
    config.patterns.some(pattern =>
      file.toLowerCase().includes(pattern.toLowerCase())
    )
  );

  if (found) {
    console.log(`✅ ${config.name} config found`);
    passed++;
  } else {
    console.log(`⚠️  ${config.name} config not found`);
    // Don't fail, just warn
  }
}

// Validate each config file has content
console.log('\n📄 Config file validation:');
for (const file of configFiles) {
  const filePath = path.join(CONFIGS_DIR, file);
  const { content, error } = safeReadFile(filePath);

  if (error) {
    console.log(`  ❌ ${file}: ${error}`);
    failed++;
  } else if (content.length < 10) {
    console.log(`  ❌ ${file}: empty or too short`);
    failed++;
  } else {
    console.log(`  ✅ ${file} (${content.length} chars)`);
    passed++;
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
