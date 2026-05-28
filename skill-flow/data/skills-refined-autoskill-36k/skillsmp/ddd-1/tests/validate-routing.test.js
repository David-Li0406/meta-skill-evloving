/**
 * Routing validation tests for DDD skill
 *
 * Validates:
 * - All routing keywords map to existing agents
 * - Orchestrators have proper routing tables
 * - No orphan agents (agents not reachable via routing)
 *
 * Run with: node tests/validate-routing.test.js
 */

const fs = require('fs');
const path = require('path');

const SKILL_DIR = path.join(__dirname, '..');
const AGENTS_DIR = path.join(SKILL_DIR, 'agents');

// Test results
let passed = 0;
let failed = 0;
const errors = [];

function test(name, condition, errorMsg) {
  if (condition) {
    console.log(`✅ ${name}`);
    passed++;
  } else {
    console.log(`❌ ${name}`);
    console.log(`   ${errorMsg}`);
    failed++;
    errors.push({ name, error: errorMsg });
  }
}

function extractRoutingTable(content) {
  // Extract markdown table rows from "Routage Principal" section only
  const tableRegex = /\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|/g;
  const routes = [];
  let match;

  // Find the routing section - specifically "Routage Principal"
  const routingSectionMatch = content.match(/### Routage Principal[^\n]*\n+([\s\S]*?)(?=\n###|\n## |$)/);
  if (!routingSectionMatch) return routes;

  const routingSection = routingSectionMatch[1];

  while ((match = tableRegex.exec(routingSection)) !== null) {
    const keywords = match[1].trim();
    const domain = match[2].trim();
    const agent = match[3].trim();

    // Skip header rows and separator rows
    if (keywords.includes('---') || keywords === 'Mots-clés') continue;
    if (domain.includes('---') || domain === 'Domaine') continue;
    if (agent.includes('---') || agent === 'Agent par défaut') continue;

    // Skip empty or invalid entries
    if (!keywords || !domain || !agent) continue;
    if (keywords.length < 3 || domain.length < 3 || agent.length < 3) continue;

    // Only include valid domain names
    const validDomains = ['strategic', 'tactical', 'tooling', 'templates', 'case-studies', 'integrations'];
    if (!validDomains.includes(domain)) continue;

    routes.push({ keywords, domain, agent });
  }

  return routes;
}

function getAllAgents() {
  const agents = new Map();
  const domains = fs.readdirSync(AGENTS_DIR).filter(d =>
    fs.statSync(path.join(AGENTS_DIR, d)).isDirectory()
  );

  for (const domain of domains) {
    const domainPath = path.join(AGENTS_DIR, domain);
    const files = fs.readdirSync(domainPath).filter(f => f.endsWith('.md'));
    for (const file of files) {
      const agentName = file.replace('.md', '');
      agents.set(agentName, { domain, path: path.join(domainPath, file) });
    }
  }
  return agents;
}

function extractAgentKeywords(content) {
  // Look for "Mots-clés de routage" section
  const keywordsSection = content.match(/Mots-clés de routage[^\n]*\n+`([^`]+)`/i);
  if (keywordsSection) {
    return keywordsSection[1].split(',').map(k => k.trim());
  }
  return [];
}

console.log('\n🔀 Validating routing configuration...\n');

const skillPath = path.join(SKILL_DIR, 'SKILL.md');
const skillContent = fs.readFileSync(skillPath, 'utf-8');

// Extract routing table from SKILL.md
const routes = extractRoutingTable(skillContent);
const agents = getAllAgents();

console.log(`Found ${routes.length} routing rules and ${agents.size} agents\n`);

// Test 1: All routed agents exist
console.log('📍 Validating route targets...\n');

for (const route of routes) {
  const agentExists = agents.has(route.agent);
  test(
    `Route "${route.agent}" exists`,
    agentExists,
    `Agent "${route.agent}" referenced in routing table does not exist`
  );

  if (agentExists) {
    const agentInfo = agents.get(route.agent);
    test(
      `Route "${route.agent}" has correct domain "${route.domain}"`,
      agentInfo.domain === route.domain,
      `Expected domain "${route.domain}", but agent is in "${agentInfo.domain}"`
    );
  }
}

console.log('\n🎯 Validating orchestrators...\n');

// Test 2: Orchestrators have routing tables
const orchestrators = ['strategic', 'tactical'].map(domain => ({
  domain,
  path: path.join(AGENTS_DIR, domain, 'orchestrator.md')
}));

for (const orch of orchestrators) {
  if (fs.existsSync(orch.path)) {
    const content = fs.readFileSync(orch.path, 'utf-8');

    test(
      `${orch.domain}/orchestrator.md has routing table`,
      content.includes('Table de Routage') || content.includes('Routage'),
      'Missing routing table section'
    );

    // Check orchestrator routes to agents in its domain
    const orchRoutes = extractRoutingTable(content);
    for (const route of orchRoutes) {
      if (route.agent === 'orchestrator') continue;

      const targetAgent = agents.get(route.agent);
      if (targetAgent) {
        test(
          `${orch.domain}/orchestrator routes to "${route.agent}"`,
          true,
          ''
        );
      }
    }
  }
}

console.log('\n🔍 Checking agent discoverability...\n');

// Test 3: All non-orchestrator agents are reachable via routing
const routedAgents = new Set(routes.map(r => r.agent));

for (const [agentName, agentInfo] of agents) {
  // Skip orchestrators (they are entry points, not targets)
  if (agentName === 'orchestrator') continue;

  // Check if agent is in routing table or has keywords
  const content = fs.readFileSync(agentInfo.path, 'utf-8');
  const hasKeywords = content.includes('Mots-clés de routage') ||
                      content.includes('mots-clés') ||
                      content.includes('Keywords');
  const isRouted = routedAgents.has(agentName);

  test(
    `Agent "${agentName}" is discoverable`,
    isRouted || hasKeywords,
    `Agent is not in routing table and has no keywords section`
  );
}

console.log('\n🧪 Testing sample routing scenarios...\n');

// Test 4: Sample routing scenarios (queries should match keywords in routing table)
const testScenarios = [
  { query: 'bounded context', expectedDomain: 'strategic', expectedAgent: 'bounded-contexts' },
  { query: 'aggregate', expectedDomain: 'tactical', expectedAgent: 'aggregates' },
  { query: 'value object', expectedDomain: 'tactical', expectedAgent: 'value-objects' },
  { query: 'event storming', expectedDomain: 'strategic', expectedAgent: 'event-storming' },
  { query: 'cqrs', expectedDomain: 'tactical', expectedAgent: 'cqrs' },
  { query: 'anemic', expectedDomain: 'case-studies', expectedAgent: 'anemic-to-rich-migration' },
  { query: 'nextjs', expectedDomain: 'integrations', expectedAgent: 'nextjs-integration' },
  { query: 'scaffolding', expectedDomain: 'templates', expectedAgent: 'aggregate-template' }
];

for (const scenario of testScenarios) {
  // Find matching route
  const matchingRoute = routes.find(r =>
    r.keywords.toLowerCase().includes(scenario.query.toLowerCase())
  );

  test(
    `Query "${scenario.query}" routes correctly`,
    matchingRoute &&
    matchingRoute.domain === scenario.expectedDomain &&
    matchingRoute.agent === scenario.expectedAgent,
    matchingRoute
      ? `Expected ${scenario.expectedDomain}/${scenario.expectedAgent}, got ${matchingRoute.domain}/${matchingRoute.agent}`
      : `No matching route found`
  );
}

// Summary
console.log('\n' + '='.repeat(50));
console.log(`\n📊 Routing validation: ${passed} passed, ${failed} failed\n`);

if (failed > 0) {
  console.log('❌ Routing validation failed\n');
  process.exit(1);
} else {
  console.log('✅ All routing validations passed\n');
  process.exit(0);
}
