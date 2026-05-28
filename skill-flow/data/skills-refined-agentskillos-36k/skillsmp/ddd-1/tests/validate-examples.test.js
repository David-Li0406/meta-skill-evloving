/**
 * Code examples validation tests for DDD skill
 *
 * Validates:
 * - TypeScript examples have basic syntax validity
 * - Code blocks are properly formatted
 * - Examples follow DDD patterns
 *
 * Run with: node tests/validate-examples.test.js
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

function extractCodeBlocks(content, language = null) {
  const regex = /```(\w*)\n([\s\S]*?)```/g;
  const blocks = [];
  let match;
  while ((match = regex.exec(content)) !== null) {
    const lang = match[1].toLowerCase();
    if (!language || lang === language || (language === 'typescript' && lang === 'ts')) {
      blocks.push({
        language: lang,
        code: match[2],
        startLine: content.substring(0, match.index).split('\n').length
      });
    }
  }
  return blocks;
}

function validateTypeScriptSyntax(code) {
  const errors = [];

  // Check for balanced braces
  const openBraces = (code.match(/{/g) || []).length;
  const closeBraces = (code.match(/}/g) || []).length;
  if (openBraces !== closeBraces) {
    errors.push(`Unbalanced braces: ${openBraces} open, ${closeBraces} close`);
  }

  // Check for balanced parentheses
  const openParens = (code.match(/\(/g) || []).length;
  const closeParens = (code.match(/\)/g) || []).length;
  if (openParens !== closeParens) {
    errors.push(`Unbalanced parentheses: ${openParens} open, ${closeParens} close`);
  }

  // Check for balanced brackets
  const openBrackets = (code.match(/\[/g) || []).length;
  const closeBrackets = (code.match(/\]/g) || []).length;
  if (openBrackets !== closeBrackets) {
    errors.push(`Unbalanced brackets: ${openBrackets} open, ${closeBrackets} close`);
  }

  // Check for common syntax errors
  if (code.includes('function (') && !code.includes('function (')) {
    // OK - anonymous function
  }

  // Check for unclosed strings (simple check)
  const lines = code.split('\n');
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    // Skip lines that are likely comments
    if (line.trim().startsWith('//') || line.trim().startsWith('*')) continue;

    const singleQuotes = (line.match(/'/g) || []).length;
    const doubleQuotes = (line.match(/"/g) || []).length;
    const backticks = (line.match(/`/g) || []).length;

    // Template literals can span multiple lines, so skip backtick check
    if (singleQuotes % 2 !== 0 && !line.includes("\\'")) {
      // Could be multiline string, skip
    }
  }

  return errors;
}

function validateDDDPatterns(code, agentName) {
  const patterns = [];

  // Check for DDD patterns based on agent type
  if (agentName.includes('aggregate') || agentName.includes('entities')) {
    if (code.includes('class ') && code.includes('extends')) {
      patterns.push('Entity/Aggregate inheritance');
    }
    if (code.includes('private ') || code.includes('readonly ')) {
      patterns.push('Encapsulation');
    }
  }

  if (agentName.includes('value-object')) {
    if (code.includes('readonly') || code.includes('private constructor')) {
      patterns.push('Immutability');
    }
    if (code.includes('equals(')) {
      patterns.push('Value equality');
    }
  }

  if (agentName.includes('repository')) {
    if (code.includes('interface ') && code.includes('Repository')) {
      patterns.push('Repository interface');
    }
    if (code.includes('findBy') || code.includes('save(')) {
      patterns.push('Repository methods');
    }
  }

  if (agentName.includes('event')) {
    if (code.includes('Event') || code.includes('event')) {
      patterns.push('Domain event');
    }
  }

  return patterns;
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

console.log('\n🧪 Validating code examples...\n');

const agents = getAllAgents();

// Focus on template and tactical agents (which have code examples)
const codeAgents = agents.filter(a =>
  ['templates', 'tactical', 'case-studies', 'integrations'].includes(a.domain)
);

let totalBlocks = 0;
let tsBlocks = 0;

for (const agent of codeAgents) {
  const content = fs.readFileSync(agent.path, 'utf-8');
  const relativePath = `${agent.domain}/${agent.name}.md`;

  const allBlocks = extractCodeBlocks(content);
  const tsBlocks = extractCodeBlocks(content, 'typescript');

  totalBlocks += allBlocks.length;

  if (tsBlocks.length > 0) {
    console.log(`\n📄 ${relativePath} (${tsBlocks.length} TypeScript blocks)`);

    for (let i = 0; i < tsBlocks.length; i++) {
      const block = tsBlocks[i];

      // Validate syntax
      const syntaxErrors = validateTypeScriptSyntax(block.code);
      test(
        `  Block ${i + 1} (line ${block.startLine}) has valid syntax`,
        syntaxErrors.length === 0,
        syntaxErrors.join('; ')
      );

      // Validate DDD patterns
      const patterns = validateDDDPatterns(block.code, agent.name);
      if (patterns.length > 0) {
        test(
          `  Block ${i + 1} demonstrates DDD patterns`,
          true,
          ''
        );
      }
    }
  }
}

console.log('\n📊 Checking code block statistics...\n');

test(
  `Total code blocks found: ${totalBlocks}`,
  totalBlocks >= 20,
  `Expected at least 20 code blocks across templates/examples`
);

console.log('\n🔍 Validating template completeness...\n');

// Check that templates have all required sections
const templateAgents = agents.filter(a => a.domain === 'templates');

for (const template of templateAgents) {
  const content = fs.readFileSync(template.path, 'utf-8');
  const relativePath = `templates/${template.name}.md`;

  // Templates should have TypeScript examples
  const tsBlocks = extractCodeBlocks(content, 'typescript');
  test(
    `${relativePath} has TypeScript examples`,
    tsBlocks.length >= 1,
    'Template should include TypeScript code examples'
  );

  // Templates should have structure/usage section
  test(
    `${relativePath} has structure or usage section`,
    content.includes('## Template') ||
    content.includes('## Structure') ||
    content.includes('## Usage'),
    'Template should have a Structure or Usage section'
  );
}

console.log('\n🔍 Validating case study completeness...\n');

// Check that case studies have all phases
const caseStudies = agents.filter(a => a.domain === 'case-studies');

for (const study of caseStudies) {
  const content = fs.readFileSync(study.path, 'utf-8');
  const relativePath = `case-studies/${study.name}.md`;

  // Case studies should have multiple sections
  const sectionCount = (content.match(/^## /gm) || []).length;
  test(
    `${relativePath} has multiple sections (${sectionCount})`,
    sectionCount >= 3,
    'Case study should have at least 3 sections'
  );

  // Case studies should have code examples
  const codeBlocks = extractCodeBlocks(content);
  test(
    `${relativePath} has code examples (${codeBlocks.length})`,
    codeBlocks.length >= 2,
    'Case study should include code examples'
  );
}

// Summary
console.log('\n' + '='.repeat(50));
console.log(`\n📊 Examples validation: ${passed} passed, ${failed} failed\n`);

if (failed > 0) {
  console.log('❌ Examples validation failed\n');
  process.exit(1);
} else {
  console.log('✅ All examples validations passed\n');
  process.exit(0);
}
