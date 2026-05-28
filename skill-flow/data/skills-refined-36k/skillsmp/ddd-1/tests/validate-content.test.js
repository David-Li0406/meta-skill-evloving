/**
 * Content quality validation tests for DDD skill
 *
 * Validates:
 * - Code blocks have valid language tags
 * - Minimum content length per agent
 * - Required sections are present
 * - No broken internal references
 *
 * Run with: node tests/validate-content.test.js
 */

const fs = require('fs');
const path = require('path');

const SKILL_DIR = path.join(__dirname, '..');
const AGENTS_DIR = path.join(SKILL_DIR, 'agents');

// Minimum content requirements
const MIN_LINES_ORCHESTRATOR = 50;
const MIN_LINES_AGENT = 80;
const MIN_CODE_BLOCKS = 1;

// Valid code block languages
const VALID_LANGUAGES = [
  'typescript', 'ts', 'javascript', 'js',
  'java', 'csharp', 'cs', 'go', 'python', 'py',
  'markdown', 'md', 'yaml', 'yml', 'json',
  'bash', 'sh', 'shell', 'sql', 'graphql',
  'mermaid', 'plantuml', 'text', 'txt', '',
  'gherkin', 'cucumber', 'feature'
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

function extractCodeBlocks(content) {
  const regex = /```(\w*)\n([\s\S]*?)```/g;
  const blocks = [];
  let match;
  while ((match = regex.exec(content)) !== null) {
    blocks.push({
      language: match[1].toLowerCase(),
      code: match[2]
    });
  }
  return blocks;
}

function extractInternalRefs(content) {
  // Match references like → `agent-name` or (→ `agent-name`)
  const regex = /→\s*`([a-z-]+)`/g;
  const refs = [];
  let match;
  while ((match = regex.exec(content)) !== null) {
    refs.push(match[1]);
  }
  return refs;
}

function countLines(content) {
  return content.split('\n').length;
}

function getAllAgents() {
  const agents = [];
  const domains = fs.readdirSync(AGENTS_DIR).filter(d =>
    fs.statSync(path.join(AGENTS_DIR, d)).isDirectory()
  );

  for (const domain of domains) {
    const domainPath = path.join(AGENTS_DIR, domain);
    const files = fs.readdirSync(domainPath).filter(f => f.endsWith('.md'));
    for (const file of files) {
      agents.push({
        domain,
        name: file.replace('.md', ''),
        path: path.join(domainPath, file)
      });
    }
  }
  return agents;
}

console.log('\n📝 Validating content quality...\n');

const agents = getAllAgents();

// Test each agent file
for (const agent of agents) {
  const content = fs.readFileSync(agent.path, 'utf-8');
  const relativePath = `${agent.domain}/${agent.name}.md`;
  const lines = countLines(content);
  const isOrchestrator = agent.name === 'orchestrator';

  // Check minimum content length
  const minLines = isOrchestrator ? MIN_LINES_ORCHESTRATOR : MIN_LINES_AGENT;
  test(
    `${relativePath} has sufficient content (${lines} lines)`,
    lines >= minLines,
    `Expected at least ${minLines} lines, got ${lines}`
  );

  // Check code blocks have valid languages
  const codeBlocks = extractCodeBlocks(content);

  if (!isOrchestrator) {
    test(
      `${relativePath} has code examples (${codeBlocks.length} blocks)`,
      codeBlocks.length >= MIN_CODE_BLOCKS,
      `Expected at least ${MIN_CODE_BLOCKS} code block(s)`
    );
  }

  for (let i = 0; i < codeBlocks.length; i++) {
    const block = codeBlocks[i];
    test(
      `${relativePath} code block ${i + 1} has valid language "${block.language || '(none)'}"`,
      VALID_LANGUAGES.includes(block.language),
      `Unknown language: "${block.language}". Valid: ${VALID_LANGUAGES.slice(0, 10).join(', ')}...`
    );
  }
}

console.log('\n🔗 Validating internal references...\n');

// Build list of all agent names
const allAgentNames = agents.map(a => a.name);

// Check internal references
for (const agent of agents) {
  const content = fs.readFileSync(agent.path, 'utf-8');
  const relativePath = `${agent.domain}/${agent.name}.md`;
  const refs = extractInternalRefs(content);

  for (const ref of refs) {
    // Skip external skill references
    if (['backend-developer', 'testing-process', 'devops', 'direction-technique', 'legacy-modernization', 'react-expert', 'nextjs-expert', 'frontend-developer'].includes(ref)) {
      continue;
    }

    test(
      `${relativePath} reference to "${ref}" is valid`,
      allAgentNames.includes(ref),
      `Unknown agent reference: "${ref}"`
    );
  }
}

console.log('\n📊 Validating SKILL.md structure...\n');

const skillPath = path.join(SKILL_DIR, 'SKILL.md');
const skillContent = fs.readFileSync(skillPath, 'utf-8');

// Check SKILL.md has required sections
const requiredSections = [
  'Philosophie',
  'Architecture du Skill',
  'Domaines et Agents',
  'Table de Routage',
  'Workflow Recommandé',
  'Livrables'
];

for (const section of requiredSections) {
  test(
    `SKILL.md has "${section}" section`,
    skillContent.includes(`## ${section}`) || skillContent.includes(`# ${section}`),
    `Missing section: "${section}"`
  );
}

// Summary
console.log('\n' + '='.repeat(50));
console.log(`\n📊 Content validation: ${passed} passed, ${failed} failed\n`);

if (failed > 0) {
  console.log('❌ Content validation failed\n');
  process.exit(1);
} else {
  console.log('✅ All content validations passed\n');
  process.exit(0);
}
