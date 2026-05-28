/**
 * Validation tests for backend-developer skill agents
 *
 * Run with: node tests/validate-agents.test.js
 */

const fs = require('fs');
const path = require('path');

const SKILL_DIR = path.join(__dirname, '..');
const AGENTS_DIR = path.join(SKILL_DIR, 'agents');

// Expected domains and their agent counts
// Note: DevOps domain was extracted to standalone `devops` skill in v2.0.0
const EXPECTED_STRUCTURE = {
  'api': ['orchestrator', 'rest-design', 'graphql-design', 'openapi-spec', 'versioning', 'rate-limiting', 'validation'],
  'database': ['orchestrator', 'modeling', 'migrations', 'queries', 'optimization', 'transactions', 'nosql'],
  'auth-security': ['orchestrator', 'authentication', 'authorization', 'vulnerabilities', 'cryptography', 'audit'],
  'architecture': ['orchestrator', 'patterns', 'microservices', 'monolith', 'event-driven', 'ddd'],
  'performance': ['orchestrator', 'caching', 'profiling', 'query-optimization', 'concurrency', 'resource-optimization'],
  'testing': ['orchestrator', 'unit', 'integration', 'api', 'fixtures', 'coverage']
};

// Required sections in each agent file
const REQUIRED_SECTIONS = [
  'Ta Responsabilité Unique',
  'Tu NE fais PAS'
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
  const missingSection = REQUIRED_SECTIONS.find(section => !content.includes(section));
  if (missingSection) {
    return { valid: false, error: `Missing required section: "${missingSection}"` };
  }
  return { valid: true };
}

// Test SKILL.md exists
console.log('\n📁 Validating skill structure...\n');

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

    // Validate sections (skip orchestrators)
    if (agent !== 'orchestrator') {
      const sectionsResult = validateSections(content, relativePath);
      test(
        `${relativePath} has required sections`,
        sectionsResult.valid,
        sectionsResult.error || ''
      );
    }
  }
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
