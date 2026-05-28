/**
 * Validation tests for DDD skill agents
 *
 * Run with: node tests/validate-agents.test.js
 */

const fs = require('fs');
const path = require('path');

const SKILL_DIR = path.join(__dirname, '..');
const AGENTS_DIR = path.join(SKILL_DIR, 'agents');

// Expected domains and their agent counts
const EXPECTED_STRUCTURE = {
  'strategic': [
    'orchestrator',
    'bounded-contexts',
    'context-mapping',
    'ubiquitous-language',
    'core-domain-identification',
    'event-storming',
    'domain-storytelling',
    'example-mapping'
  ],
  'tactical': [
    'orchestrator',
    'entities',
    'value-objects',
    'aggregates',
    'repositories',
    'domain-services',
    'domain-events',
    'domain-errors',
    'factories',
    'specifications',
    'domain-primitives',
    'application-services',
    'clean-architecture',
    'anti-corruption-layer',
    'cqrs',
    'event-sourcing',
    'saga-process-manager'
  ],
  'tooling': [
    'model-validator',
    'pattern-selector',
    'performance-guide'
  ],
  'templates': [
    'aggregate-template',
    'value-object-template',
    'repository-template'
  ],
  'case-studies': [
    'e-commerce-domain',
    'anemic-to-rich-migration'
  ],
  'integrations': [
    'nextjs-integration'
  ]
};

// Required sections in each agent file
const REQUIRED_SECTIONS = [
  'Tu FAIS',
  'Tu NE FAIS PAS'
];

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

function validateFrontmatter(content, filePath) {
  const frontmatterMatch = content.match(/^---\n([\s\S]*?)\n---/);
  if (!frontmatterMatch) {
    return { valid: false, error: 'Missing YAML frontmatter' };
  }

  const frontmatter = frontmatterMatch[1];
  const hasName = /^name:\s*.+$/m.test(frontmatter);
  const hasDescription = /^description:\s*.+$/m.test(frontmatter);

  if (!hasName) {
    return { valid: false, error: 'Missing "name" in frontmatter' };
  }
  if (!hasDescription) {
    return { valid: false, error: 'Missing "description" in frontmatter' };
  }

  return { valid: true };
}

function validateSections(content, filePath) {
  const missingSections = REQUIRED_SECTIONS.filter(section => !content.includes(section));
  if (missingSections.length > 0) {
    return { valid: false, error: `Missing required sections: ${missingSections.join(', ')}` };
  }
  return { valid: true };
}

function validateRoutingTable(content, filePath) {
  // Orchestrators should have a routing table
  if (!content.includes('Table de Routage') && !content.includes('Routing')) {
    return { valid: false, error: 'Missing routing table section' };
  }
  return { valid: true };
}

// Test SKILL.md exists
console.log('\n📁 Validating DDD skill structure...\n');

const skillMdPath = path.join(SKILL_DIR, 'SKILL.md');
test(
  'SKILL.md exists',
  fs.existsSync(skillMdPath),
  'SKILL.md not found'
);

// Test CHANGELOG.md exists
const changelogPath = path.join(SKILL_DIR, 'CHANGELOG.md');
test(
  'CHANGELOG.md exists',
  fs.existsSync(changelogPath),
  'CHANGELOG.md not found'
);

// Test README.md exists
const readmePath = path.join(SKILL_DIR, 'README.md');
test(
  'README.md exists',
  fs.existsSync(readmePath),
  'README.md not found'
);

// Test agents directory exists
test(
  'agents/ directory exists',
  fs.existsSync(AGENTS_DIR),
  'agents/ directory not found'
);

console.log('\n📂 Validating domains...\n');

// Verify total agent count
const totalExpectedAgents = Object.values(EXPECTED_STRUCTURE)
  .reduce((sum, agents) => sum + agents.length, 0);
test(
  `Total expected agents: ${totalExpectedAgents}`,
  totalExpectedAgents === 34,
  `Expected 34 agents, got ${totalExpectedAgents}`
);

// Test each domain
for (const [domain, expectedAgents] of Object.entries(EXPECTED_STRUCTURE)) {
  const domainPath = path.join(AGENTS_DIR, domain);

  test(
    `Domain "${domain}" exists`,
    fs.existsSync(domainPath),
    `Directory ${domain}/ not found`
  );

  if (fs.existsSync(domainPath)) {
    const files = fs.readdirSync(domainPath).filter(f => f.endsWith('.md'));
    const agentNames = files.map(f => f.replace('.md', ''));

    test(
      `Domain "${domain}" has ${expectedAgents.length} agents`,
      files.length === expectedAgents.length,
      `Expected ${expectedAgents.length} agents, found ${files.length}: ${agentNames.join(', ')}`
    );

    for (const agent of expectedAgents) {
      const agentFile = `${agent}.md`;
      const agentPath = path.join(domainPath, agentFile);

      test(
        `Agent "${domain}/${agent}" exists`,
        fs.existsSync(agentPath),
        `File ${agentFile} not found in ${domain}/`
      );
    }
  }
}

console.log('\n📄 Validating agent files...\n');

// Validate each agent file
for (const [domain, agents] of Object.entries(EXPECTED_STRUCTURE)) {
  const domainPath = path.join(AGENTS_DIR, domain);

  if (!fs.existsSync(domainPath)) continue;

  for (const agent of agents) {
    const agentPath = path.join(domainPath, `${agent}.md`);

    if (!fs.existsSync(agentPath)) continue;

    const content = fs.readFileSync(agentPath, 'utf-8');
    const relativePath = `${domain}/${agent}.md`;

    // Validate frontmatter
    const frontmatterResult = validateFrontmatter(content, relativePath);
    test(
      `${relativePath} has valid frontmatter`,
      frontmatterResult.valid,
      frontmatterResult.error || ''
    );

    // Validate sections
    const sectionsResult = validateSections(content, relativePath);
    test(
      `${relativePath} has required sections`,
      sectionsResult.valid,
      sectionsResult.error || ''
    );

    // Validate orchestrators have routing tables
    if (agent === 'orchestrator') {
      const routingResult = validateRoutingTable(content, relativePath);
      test(
        `${relativePath} has routing table`,
        routingResult.valid,
        routingResult.error || ''
      );
    }
  }
}

console.log('\n📊 Validating SKILL.md content...\n');

// Validate SKILL.md has required metadata
if (fs.existsSync(skillMdPath)) {
  const skillContent = fs.readFileSync(skillMdPath, 'utf-8');

  test(
    'SKILL.md has version metadata',
    skillContent.includes('version:'),
    'Missing version in SKILL.md frontmatter'
  );

  test(
    'SKILL.md has routing table',
    skillContent.includes('Table de Routage') || skillContent.includes('Routing'),
    'Missing routing table in SKILL.md'
  );

  test(
    'SKILL.md mentions all 6 domains',
    skillContent.includes('strategic') &&
    skillContent.includes('tactical') &&
    skillContent.includes('tooling') &&
    skillContent.includes('templates') &&
    skillContent.includes('case-studies') &&
    skillContent.includes('integrations'),
    'SKILL.md should mention all 6 domains: strategic, tactical, tooling, templates, case-studies, integrations'
  );
}

// Summary
console.log('\n' + '='.repeat(50));
console.log(`\n📊 Results: ${passed} passed, ${failed} failed\n`);

if (failed > 0) {
  console.log('❌ Validation failed\n');
  process.exit(1);
} else {
  console.log('✅ All validations passed\n');
  process.exit(0);
}
