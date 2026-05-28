#!/usr/bin/env node
/**
 * Test: Validate Workflow Integration
 *
 * Validates that workflows are properly configured and reference valid agents
 *
 * @module tests/validate-workflows
 */

const path = require('path');
const fs = require('fs');
const {
  findMarkdownFiles,
  safeReadFile,
  parseFrontmatter,
  directoryExists,
  fileExists,
  printSeparator
} = require('./utils');
const { SKILL_ROOT, WORKFLOWS_DIR, EXPECTED_WORKFLOWS, AGENTS_DIR } = require('./config');

// Test results
let passed = 0;
let failed = 0;
let warnings = 0;

/**
 * Extract agent references from workflow content
 */
function extractAgentRefs(content) {
  const refs = [];

  // Pattern: skill/agent or domain/agent
  const patterns = [
    /content-management\/([a-z-]+\/[a-z-]+)/g,
    /`([a-z-]+\/[a-z-]+)`/g,
    /→\s*`?([a-z-]+\/[a-z-]+)`?/g
  ];

  for (const pattern of patterns) {
    let match;
    while ((match = pattern.exec(content)) !== null) {
      refs.push(match[1]);
    }
  }

  return [...new Set(refs)];
}

/**
 * Validate agent reference exists
 */
function validateAgentRef(ref) {
  const parts = ref.split('/');
  if (parts.length !== 2) return { valid: false, reason: 'Invalid format' };

  const [domain, agent] = parts;
  const agentPath = path.join(AGENTS_DIR, domain, `${agent}.md`);

  if (fileExists(agentPath)) {
    return { valid: true };
  }

  // Check if it's an orchestrator reference
  const orchestratorPath = path.join(AGENTS_DIR, domain, 'orchestrator.md');
  if (agent === 'orchestrator' && fileExists(orchestratorPath)) {
    return { valid: true };
  }

  return { valid: false, reason: `Agent not found: ${agentPath}` };
}

/**
 * Validate workflow file
 */
function validateWorkflow(filePath) {
  const errors = [];
  const warns = [];

  const { content, error } = safeReadFile(filePath);
  if (error) return { errors: [error], warns: [] };

  // Check frontmatter
  const frontmatter = parseFrontmatter(content);
  if (!frontmatter) {
    errors.push('Missing frontmatter');
  } else {
    if (!frontmatter.name) errors.push('Missing "name" in frontmatter');
    if (!frontmatter.description) errors.push('Missing "description" in frontmatter');
    if (!frontmatter.version) errors.push('Missing "version" in frontmatter');
  }

  // Check required sections
  const requiredSections = [
    'Vue d\'Ensemble',
    'Triggers',
    'Phase'
  ];

  for (const section of requiredSections) {
    if (!content.includes(section)) {
      warns.push(`Missing section: ${section}`);
    }
  }

  // Check agent references
  const agentRefs = extractAgentRefs(content);
  for (const ref of agentRefs) {
    // Only validate content-management internal refs
    if (ref.startsWith('editorial/') ||
        ref.startsWith('redaction/') ||
        ref.startsWith('assets/') ||
        ref.startsWith('localization/')) {
      const result = validateAgentRef(ref);
      if (!result.valid) {
        errors.push(`Invalid agent reference: ${ref} - ${result.reason}`);
      }
    }
  }

  // Check for workflow chain references
  if (content.includes('→') && !content.includes('Workflow')) {
    warns.push('Contains workflow references but no Workflow section');
  }

  return { errors, warns };
}

// Main execution
console.log('🧪 Validating Workflow Integration\n');
printSeparator();

if (!directoryExists(WORKFLOWS_DIR)) {
  console.log('⚠️  Workflows directory not found, skipping...');
  process.exit(0);
}

// Find all workflow files
const files = findMarkdownFiles(WORKFLOWS_DIR);
console.log(`Found ${files.length} workflow files\n`);

// Check expected workflows exist
console.log('Checking expected workflows...\n');
for (const workflow of EXPECTED_WORKFLOWS) {
  const workflowPath = path.join(WORKFLOWS_DIR, `${workflow}.md`);
  if (fileExists(workflowPath)) {
    console.log(`✅ ${workflow}.md exists`);
    passed++;
  } else {
    console.log(`❌ ${workflow}.md missing`);
    failed++;
  }
}

console.log('\nValidating workflow content...\n');

for (const file of files) {
  const relativePath = path.relative(WORKFLOWS_DIR, file);
  const { errors, warns } = validateWorkflow(file);

  if (errors.length === 0 && warns.length === 0) {
    console.log(`✅ ${relativePath}`);
    passed++;
  } else if (errors.length === 0) {
    console.log(`⚠️  ${relativePath}`);
    for (const warn of warns) {
      console.log(`   └─ ⚠️  ${warn}`);
      warnings++;
    }
    passed++;
  } else {
    console.log(`❌ ${relativePath}`);
    for (const err of errors) {
      console.log(`   └─ ❌ ${err}`);
    }
    for (const warn of warns) {
      console.log(`   └─ ⚠️  ${warn}`);
      warnings++;
    }
    failed++;
  }
}

console.log('\n');
printSeparator();
console.log(`\n📊 Results: ${passed} passed, ${failed} failed, ${warnings} warnings`);

if (failed > 0) {
  console.log('\n❌ Some tests failed');
  process.exit(1);
} else {
  console.log('\n✅ All tests passed');
  process.exit(0);
}
