#!/usr/bin/env node
/**
 * Test: Validate Routing Consistency
 *
 * Validates that orchestrators reference agents that actually exist.
 * Checks for broken references and orphaned agents.
 *
 * @module tests/validate-routing
 */

const fs = require('fs');
const path = require('path');
const {
  findMarkdownFiles,
  safeReadFile,
  directoryExists,
  printSeparator
} = require('./utils');
const { PROJECT_MANAGEMENT_DIR } = require('./config');

// =============================================================================
// Configuration Constants
// =============================================================================

/** @const {string} Directory containing agents (from project-management skill) */
const AGENTS_DIR = PROJECT_MANAGEMENT_DIR;

/**
 * Regex patterns for extracting agent references from markdown
 * Pre-compiled for performance (avoids creating RegExp in loops)
 * @const {RegExp[]}
 */
const AGENT_REFERENCE_PATTERNS = [
  // Matches: `agent-name` (backtick-wrapped agent names)
  /`([a-z][a-z0-9-]*)`/g,

  // Matches: → subdir/agent-name (arrow followed by path)
  /→\s*([a-z][a-z0-9-]*\/[a-z][a-z0-9-]*)/g,

  // Matches: | `subdir/agent-name` (table cell with path)
  /\|\s*`([a-z][a-z0-9-]*\/[a-z][a-z0-9-]*)`/g,
];

/**
 * Keywords to skip when extracting agent references
 * These are structural terms, not actual agent names
 * @const {Set<string>}
 */
const SKIP_KEYWORDS = new Set([
  'orchestrator', 'templates', 'docs', 'agents',
  'project-management', 'web-agency', 'avant-projet',
  'pilotage', 'communication', 'livraison', 'facturation'
]);

// =============================================================================
// Test Results
// =============================================================================

let passed = 0;
let failed = 0;

// =============================================================================
// Helper Functions
// =============================================================================

/**
 * Get all agent names from file paths
 *
 * @param {string[]} files - Array of file paths
 * @returns {Set<string>} Set of agent names (both short and full path forms)
 */
function getAgentNames(files) {
  const agents = new Set();
  for (const file of files) {
    const relativePath = path.relative(AGENTS_DIR, file);
    const name = path.basename(file, '.md');
    agents.add(name);

    const dir = path.dirname(relativePath);
    if (dir !== '.') {
      agents.add(`${dir}/${name}`);
    }
  }
  return agents;
}

/**
 * Extract agent references from orchestrator content
 * Uses pre-compiled patterns for better performance
 *
 * @param {string} content - Orchestrator markdown content
 * @returns {string[]} Unique array of referenced agent names
 */
function extractAgentReferences(content) {
  const references = new Set();

  for (const pattern of AGENT_REFERENCE_PATTERNS) {
    // Reset regex lastIndex to ensure fresh matching
    pattern.lastIndex = 0;

    let match;
    while ((match = pattern.exec(content)) !== null) {
      const ref = match[1];
      const refRoot = ref.split('/')[0];

      // Skip structural keywords
      if (!SKIP_KEYWORDS.has(ref) && !SKIP_KEYWORDS.has(refRoot)) {
        references.add(ref);
      }
    }
  }

  return [...references];
}

/**
 * Validate orchestrator routing references
 *
 * @param {string} filePath - Path to orchestrator file
 * @param {Set<string>} existingAgents - Set of valid agent names
 * @returns {{ references: number, errors: string[] }} Validation result
 */
function validateOrchestrator(filePath, existingAgents) {
  const { content, error } = safeReadFile(filePath);
  if (error) {
    return { references: 0, errors: [error] };
  }

  const references = extractAgentReferences(content);
  const errors = [];

  for (const ref of references) {
    const agentName = ref.includes('/') ? path.basename(ref) : ref;

    if (!existingAgents.has(agentName) && !existingAgents.has(ref)) {
      const possiblePath = ref.includes('/')
        ? path.join(AGENTS_DIR, ref + '.md')
        : null;

      if (possiblePath && !fs.existsSync(possiblePath)) {
        errors.push(`Referenced agent not found: ${ref}`);
      }
    }
  }

  return { references: references.length, errors };
}

// =============================================================================
// Main Execution
// =============================================================================

console.log('🧪 Validating Routing Consistency\n');
printSeparator();

if (!directoryExists(AGENTS_DIR)) {
  console.error(`❌ Agents directory not found: ${AGENTS_DIR}`);
  process.exit(1);
}

const allFiles = findMarkdownFiles(AGENTS_DIR);
const orchestratorFiles = allFiles.filter(f => f.includes('orchestrator'));
const existingAgents = getAgentNames(allFiles);

console.log(`Found ${orchestratorFiles.length} orchestrators`);
console.log(`Found ${existingAgents.size} unique agent references\n`);

for (const file of orchestratorFiles) {
  const relativePath = path.relative(AGENTS_DIR, file);
  const { references, errors } = validateOrchestrator(file, existingAgents);

  if (errors.length === 0) {
    console.log(`✅ ${relativePath} (${references} references)`);
    passed++;
  } else {
    console.log(`❌ ${relativePath}`);
    for (const err of errors) {
      console.log(`   └─ ${err}`);
    }
    failed++;
  }
}

console.log('\n');
printSeparator();
console.log(`\n📊 Results: ${passed} passed, ${failed} failed`);

if (failed > 0) {
  console.log('\n❌ Some routing tests failed');
  process.exit(1);
} else {
  console.log('\n✅ All routing tests passed');
  process.exit(0);
}
