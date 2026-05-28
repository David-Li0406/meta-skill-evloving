#!/usr/bin/env node
/**
 * Test: Validate Orchestrator Routing vs Agent Capabilities
 *
 * Ensures that orchestrator routing rules correctly map to
 * agents that can actually handle those requests.
 *
 * @module tests/validate-orchestrator-routing
 */

const fs = require('fs');
const path = require('path');
const {
  safeReadFile,
  parseFrontmatter,
  directoryExists,
  printSeparator
} = require('./utils');
const {
  PROJECT_MANAGEMENT_DIR,
  PROJECT_MANAGEMENT_AGENTS_DIR,
  EXPECTED_ROUTING,
  PROJECT_MANAGEMENT_SUBDOMAINS
} = require('./config');

// =============================================================================
// Test Results
// =============================================================================

let passed = 0;
let failed = 0;
const errors = [];

// =============================================================================
// Helper Functions
// =============================================================================

/**
 * Extract routing rules from orchestrator content
 * Parses the "Règles de Routage" table
 *
 * @param {string} content - Orchestrator markdown content
 * @returns {Object[]} Array of { intent, agent } objects
 */
function extractRoutingRules(content) {
  const rules = [];

  // Find the routing table section
  const routingMatch = content.match(/## Règles de Routage[\s\S]*?(?=\n##|\n$)/);
  if (!routingMatch) return rules;

  const section = routingMatch[0];

  // Parse table rows: | intent | agent |
  const tableRowPattern = /\|\s*"([^"]+)"[^|]*\|\s*`([^`]+)`/g;
  let match;

  while ((match = tableRowPattern.exec(section)) !== null) {
    rules.push({
      intent: match[1].toLowerCase(),
      agent: match[2]
    });
  }

  return rules;
}

/**
 * Get agent capabilities from its description
 *
 * @param {string} agentPath - Path to agent file
 * @returns {{ name: string, description: string, responsibility: string } | null}
 */
function getAgentCapabilities(agentPath) {
  const { content, error } = safeReadFile(agentPath);
  if (error) return null;

  const frontmatter = parseFrontmatter(content);
  if (!frontmatter) return null;

  // Extract responsibility section
  const responsibilityMatch = content.match(/## Ta Responsabilité Unique[\s\S]*?(?=\n##|\n$)/);
  const responsibility = responsibilityMatch
    ? responsibilityMatch[0].replace(/## Ta Responsabilité Unique\s*/, '').trim()
    : '';

  return {
    name: frontmatter.name,
    description: frontmatter.description,
    responsibility
  };
}

/**
 * Check if agent capability matches the routing intent
 *
 * @param {string} intent - User intent from routing rule
 * @param {Object} capabilities - Agent capabilities
 * @returns {boolean} True if likely match
 */
function intentMatchesCapability(intent, capabilities) {
  if (!capabilities) return false;

  const searchText = `${capabilities.description} ${capabilities.responsibility}`.toLowerCase();

  // Split intent into keywords and check if at least one matches
  const keywords = intent.split(/\s+/).filter(w => w.length > 3);

  for (const keyword of keywords) {
    if (searchText.includes(keyword)) {
      return true;
    }
  }

  // Common synonyms matching
  const synonyms = {
    'email': ['mail', 'message', 'courrier'],
    'client': ['prospect', 'destinataire'],
    'chiffrage': ['estimation', 'devis', 'coût'],
    'planning': ['calendrier', 'jalons', 'dates'],
    'risques': ['hypothèses', 'alertes']
  };

  for (const [key, values] of Object.entries(synonyms)) {
    if (intent.includes(key)) {
      for (const syn of values) {
        if (searchText.includes(syn)) return true;
      }
    }
  }

  return false;
}

// =============================================================================
// Test Functions
// =============================================================================

/**
 * Test orchestrator has routing section
 *
 * @param {string} subdomain - Subdomain name
 * @param {string} content - Orchestrator content
 */
function testHasRoutingSection(subdomain, content) {
  if (content.includes('## Règles de Routage')) {
    console.log(`   ✅ Has routing rules section`);
    passed++;
    return true;
  } else {
    console.log(`   ❌ Missing "Règles de Routage" section`);
    errors.push(`[${subdomain}] Missing routing section`);
    failed++;
    return false;
  }
}

/**
 * Test expected agents are referenced in routing
 *
 * @param {string} subdomain - Subdomain name
 * @param {Object[]} expectedRoutes - Expected routing rules
 * @param {Object[]} actualRoutes - Actual routing rules from orchestrator
 */
function testExpectedRoutesExist(subdomain, expectedRoutes, actualRoutes) {
  const actualAgents = new Set(actualRoutes.map(r => r.agent));
  const missingAgents = [];

  for (const expected of expectedRoutes) {
    if (!actualAgents.has(expected.agent)) {
      missingAgents.push(expected.agent);
    }
  }

  if (missingAgents.length === 0) {
    console.log(`   ✅ All expected agents (${expectedRoutes.length}) are routed`);
    passed++;
  } else {
    console.log(`   ❌ Missing routing for: ${missingAgents.join(', ')}`);
    errors.push(`[${subdomain}] Missing routes: ${missingAgents.join(', ')}`);
    failed++;
  }
}

/**
 * Test routing agents actually exist
 *
 * @param {string} subdomain - Subdomain name
 * @param {Object[]} routes - Routing rules
 */
function testRoutedAgentsExist(subdomain, routes) {
  const missingAgents = [];

  for (const route of routes) {
    const agentPath = path.join(PROJECT_MANAGEMENT_AGENTS_DIR, subdomain, `${route.agent}.md`);
    if (!fs.existsSync(agentPath)) {
      missingAgents.push(route.agent);
    }
  }

  if (missingAgents.length === 0) {
    console.log(`   ✅ All routed agents exist`);
    passed++;
  } else {
    console.log(`   ❌ Routed agents not found: ${missingAgents.join(', ')}`);
    errors.push(`[${subdomain}] Missing agents: ${missingAgents.join(', ')}`);
    failed++;
  }
}

/**
 * Test routing intents match agent capabilities
 *
 * @param {string} subdomain - Subdomain name
 * @param {Object[]} routes - Routing rules
 */
function testRoutingMatchesCapabilities(subdomain, routes) {
  let mismatches = 0;

  for (const route of routes) {
    const agentPath = path.join(PROJECT_MANAGEMENT_AGENTS_DIR, subdomain, `${route.agent}.md`);
    const capabilities = getAgentCapabilities(agentPath);

    if (capabilities && !intentMatchesCapability(route.intent, capabilities)) {
      console.log(`   ⚠️  Intent "${route.intent}" may not match ${route.agent}`);
      mismatches++;
    }
  }

  if (mismatches === 0) {
    console.log(`   ✅ Routing intents match agent capabilities`);
    passed++;
  } else {
    console.log(`   ⚠️  ${mismatches} potential mismatches (review recommended)`);
    // Warning only, not failure
    passed++;
  }
}

// =============================================================================
// Main Execution
// =============================================================================

console.log('🎯 Validating Orchestrator Routing vs Agent Capabilities\n');
printSeparator();

if (!directoryExists(PROJECT_MANAGEMENT_DIR)) {
  console.error(`❌ Project management directory not found: ${PROJECT_MANAGEMENT_DIR}`);
  process.exit(1);
}

console.log(`Testing ${PROJECT_MANAGEMENT_SUBDOMAINS.length} subdomain orchestrators\n`);

for (const subdomain of PROJECT_MANAGEMENT_SUBDOMAINS) {
  const orchestratorPath = path.join(PROJECT_MANAGEMENT_AGENTS_DIR, subdomain, 'orchestrator.md');
  console.log(`\n📂 ${subdomain}/orchestrator.md`);

  if (!fs.existsSync(orchestratorPath)) {
    console.log(`   ❌ Orchestrator not found`);
    errors.push(`[${subdomain}] Orchestrator missing`);
    failed++;
    continue;
  }

  const { content, error } = safeReadFile(orchestratorPath);
  if (error) {
    console.log(`   ❌ ${error}`);
    errors.push(`[${subdomain}] ${error}`);
    failed++;
    continue;
  }

  passed++; // Orchestrator exists

  if (!testHasRoutingSection(subdomain, content)) {
    continue;
  }

  const actualRoutes = extractRoutingRules(content);
  const expectedRoutes = EXPECTED_ROUTING[subdomain] || [];

  console.log(`   Found ${actualRoutes.length} routing rules`);

  if (expectedRoutes.length > 0) {
    testExpectedRoutesExist(subdomain, expectedRoutes, actualRoutes);
  }

  testRoutedAgentsExist(subdomain, actualRoutes);
  testRoutingMatchesCapabilities(subdomain, actualRoutes);
}

// =============================================================================
// Summary
// =============================================================================

console.log('\n');
printSeparator();
console.log(`\n📊 Results: ${passed} passed, ${failed} failed`);

if (errors.length > 0) {
  console.log('\n❌ Orchestrator routing errors:');
  for (const err of errors) {
    console.log(`   └─ ${err}`);
  }
  process.exit(1);
} else {
  console.log('\n✅ All orchestrator routing tests passed');
  process.exit(0);
}
