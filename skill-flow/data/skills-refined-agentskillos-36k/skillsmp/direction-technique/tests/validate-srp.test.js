#!/usr/bin/env node
/**
 * SRP Validation Tests
 *
 * Validates that POURQUOI-level agents (direction-technique)
 * do NOT contain implementation code.
 *
 * Per ADR-005: POURQUOI level should only contain:
 * - Policies and objectives
 * - Decision criteria
 * - Checklists (without code)
 * - Questions for clarification
 * - References to QUOI/COMMENT levels
 *
 * @module tests/validate-srp
 */

const fs = require('fs');
const path = require('path');
const { directoryExists, fileExists } = require('./utils');

const SKILL_ROOT = path.resolve(__dirname, '..');

// Code block patterns that should NOT appear in POURQUOI-level agents
const FORBIDDEN_CODE_PATTERNS = [
  /```typescript/gi,
  /```javascript/gi,
  /```php/gi,
  /```python/gi,
  /```ruby/gi,
  /```go/gi,
  /```rust/gi,
  /```java/gi,
  /```sql/gi,
  /```yaml\s*\n\s*(version:|apiVersion:|services:|kind:)/gi, // Docker/K8s YAML
  /```dockerfile/gi,
  /```nginx/gi,
  /```bash\s*\n\s*(npm|yarn|docker|kubectl|git|curl|wget)/gi, // Command examples
];

// Allowed code patterns (diagrams, ASCII art, templates)
const ALLOWED_PATTERNS = [
  /```\s*\n\s*[┌└├│─▼▲►◄→←↓↑]/m, // ASCII diagrams
  /```markdown/gi, // Markdown templates
  /```\s*\n\s*#.*Template/i, // Templates
  /```\s*\n\s*Internet\s*\n\s*│/m, // Network diagrams
];

// Domains to validate (POURQUOI level)
const POURQUOI_DOMAINS = [
  'avant-projet',
  'specification',
  'architecture',
  'estimation',
  'qualite',
  'securite',
  'performance',
  'infrastructure',
];

/**
 * Get all agent files in a domain directory
 * @param {string} domain - Domain name
 * @returns {string[]} Array of file paths
 */
function getAgentFiles(domain) {
  const domainPath = path.join(SKILL_ROOT, 'agents', domain);

  if (!directoryExists(domainPath)) {
    return [];
  }

  try {
    const entries = fs.readdirSync(domainPath, { withFileTypes: true });
    return entries
      .filter(entry => entry.isFile() && entry.name.endsWith('.md') && entry.name !== 'orchestrator.md')
      .map(entry => path.join(domainPath, entry.name));
  } catch (err) {
    console.error(`Warning: Cannot read directory ${domainPath}: ${err.message}`);
    return [];
  }
}

/**
 * Check if a code block match is allowed (ASCII diagrams, templates, etc.)
 * @param {string} content - File content
 * @param {number} matchIndex - Index of the match
 * @param {string} matchText - Matched text
 * @returns {boolean} True if allowed
 */
function isAllowedCodeBlock(content, matchIndex, matchText) {
  // Find the code block boundaries
  const codeBlockStart = content.lastIndexOf('```', matchIndex);
  const codeBlockEnd = content.indexOf('```', matchIndex + matchText.length);

  if (codeBlockStart === -1 || codeBlockEnd === -1) return false;

  const codeBlock = content.substring(codeBlockStart, codeBlockEnd + 3);

  return ALLOWED_PATTERNS.some(pattern => pattern.test(codeBlock));
}

/**
 * Validate a file for SRP violations using matchAll
 * @param {string} filePath - Path to file
 * @returns {Object[]} Array of violations
 */
function validateFile(filePath) {
  let content;
  try {
    content = fs.readFileSync(filePath, 'utf-8');
  } catch (err) {
    console.error(`Warning: Cannot read file ${filePath}: ${err.message}`);
    return [];
  }

  const fileName = path.basename(filePath);
  const violations = [];

  for (const pattern of FORBIDDEN_CODE_PATTERNS) {
    // Use matchAll for cleaner iteration (reset not needed)
    const matches = content.matchAll(new RegExp(pattern.source, pattern.flags));

    for (const match of matches) {
      // Check if this is an allowed pattern
      if (!isAllowedCodeBlock(content, match.index, match[0])) {
        const lineNumber = content.substring(0, match.index).split('\n').length;
        violations.push({
          file: fileName,
          line: lineNumber,
          pattern: pattern.source,
          match: match[0].substring(0, 50),
        });
      }
    }
  }

  return violations;
}

// Run tests
console.log('\n🧪 Validating SRP - No Code in POURQUOI Level Agents\n');
console.log('==================================================\n');

let totalPassed = 0;
let totalFailed = 0;
const allViolations = [];

for (const domain of POURQUOI_DOMAINS) {
  console.log(`📁 Domain: ${domain}`);
  const files = getAgentFiles(domain);

  if (files.length === 0) {
    console.log(`  ⚠️  No agent files found\n`);
    continue;
  }

  let domainPassed = 0;
  let domainFailed = 0;

  for (const file of files) {
    const violations = validateFile(file);
    const fileName = path.basename(file);

    if (violations.length === 0) {
      console.log(`  ✅ ${fileName}`);
      domainPassed++;
    } else {
      console.log(`  ❌ ${fileName}`);
      violations.forEach(v => {
        console.log(`     Line ${v.line}: Found code block (${v.match}...)`);
        allViolations.push({ ...v, domain });
      });
      domainFailed++;
    }
  }

  totalPassed += domainPassed;
  totalFailed += domainFailed;
  console.log();
}

console.log('==================================================\n');
console.log(`📊 Results: ${totalPassed} passed, ${totalFailed} failed\n`);

if (allViolations.length > 0) {
  console.log('❌ SRP Violations Found:\n');
  console.log('The following files contain code that should be moved to QUOI or COMMENT level:\n');

  allViolations.forEach(v => {
    console.log(`  - ${v.domain}/${v.file}:${v.line}`);
  });

  console.log('\nRecommendation:');
  console.log('  1. Remove implementation code from these files');
  console.log('  2. Keep only policies, objectives, and decision criteria');
  console.log('  3. Add references to QUOI/COMMENT level agents for implementation\n');

  process.exit(1);
} else {
  console.log('✅ All POURQUOI-level agents comply with SRP\n');
  console.log('No implementation code found in direction-technique agents.\n');
  process.exit(0);
}
