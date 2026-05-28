#!/usr/bin/env node

/**
 * Claude Code Skill Validator
 *
 * Validates skill structure according to Claude Code documentation:
 * - YAML frontmatter format and required fields
 * - File structure and /reference/ folder requirements
 * - Token budget estimates for metadata and body
 * - Path format validation (forward slashes)
 * - Description specificity checks
 *
 * Usage: node validate-skill.js <path-to-skill-directory>
 */

const fs = require('fs');
const path = require('path');
const yaml = require('yaml');

// ANSI color codes for terminal output
const colors = {
  reset: '\x1b[0m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  cyan: '\x1b[36m',
};

class SkillValidator {
  constructor(skillPath) {
    this.skillPath = path.resolve(skillPath);
    this.errors = [];
    this.warnings = [];
    this.info = [];
    this.skillMdPath = path.join(this.skillPath, 'SKILL.md');
  }

  // Color helper methods
  error(msg) {
    this.errors.push(msg);
    console.error(`${colors.red}✗ ERROR: ${msg}${colors.reset}`);
  }

  warn(msg) {
    this.warnings.push(msg);
    console.warn(`${colors.yellow}⚠ WARNING: ${msg}${colors.reset}`);
  }

  success(msg) {
    console.log(`${colors.green}✓ ${msg}${colors.reset}`);
  }

  log(msg) {
    this.info.push(msg);
    console.log(`${colors.cyan}ℹ ${msg}${colors.reset}`);
  }

  // Token estimation (rough approximation: ~4 chars per token)
  estimateTokens(text) {
    return Math.ceil(text.length / 4);
  }

  // Validate skill directory exists
  validateDirectory() {
    if (!fs.existsSync(this.skillPath)) {
      this.error(`Skill directory not found: ${this.skillPath}`);
      return false;
    }
    if (!fs.statSync(this.skillPath).isDirectory()) {
      this.error(`Path is not a directory: ${this.skillPath}`);
      return false;
    }
    this.success('Skill directory exists');
    return true;
  }

  // Validate SKILL.md exists
  validateSkillMdExists() {
    if (!fs.existsSync(this.skillMdPath)) {
      this.error('SKILL.md not found in skill directory');
      return false;
    }
    this.success('SKILL.md exists');
    return true;
  }

  // Parse and validate YAML frontmatter
  validateFrontmatter(content) {
    // Check for frontmatter delimiters
    if (!content.startsWith('---\n') && !content.startsWith('---\r\n')) {
      this.error('SKILL.md must start with "---" on line 1');
      return null;
    }

    const lines = content.split('\n');
    let closingIndex = -1;

    for (let i = 1; i < lines.length; i++) {
      if (lines[i].trim() === '---') {
        closingIndex = i;
        break;
      }
    }

    if (closingIndex === -1) {
      this.error('SKILL.md frontmatter missing closing "---"');
      return null;
    }

    this.success('Valid YAML frontmatter delimiters found');

    // Extract and parse YAML
    const yamlContent = lines.slice(1, closingIndex).join('\n');
    let metadata;

    try {
      metadata = yaml.parse(yamlContent);
    } catch (e) {
      this.error(`Invalid YAML syntax: ${e.message}`);
      return null;
    }

    this.success('YAML syntax is valid');
    return { metadata, bodyStartLine: closingIndex + 1 };
  }

  // Validate required frontmatter fields
  validateRequiredFields(metadata) {
    const required = ['name', 'description'];
    let allPresent = true;

    required.forEach(field => {
      if (!metadata[field]) {
        this.error(`Required frontmatter field missing: "${field}"`);
        allPresent = false;
      } else {
        this.success(`Required field present: ${field}`);
      }
    });

    return allPresent;
  }

  // Validate description specificity
  validateDescription(description) {
    if (!description) return false;

    const tokens = this.estimateTokens(description);
    this.log(`Description length: ${description.length} chars (~${tokens} tokens)`);

    // Check for vague terms
    const vagueTerms = ['helps', 'assists', 'provides', 'enables', 'allows'];
    const foundVague = vagueTerms.filter(term =>
      description.toLowerCase().includes(term)
    );

    if (foundVague.length > 2) {
      this.warn(`Description may be too vague. Contains: ${foundVague.join(', ')}`);
      this.warn('Consider adding specific triggers or use cases');
    }

    // Check for "when to use" indicators
    const hasWhenIndicators = /when|use when|trigger|for \w+ing/i.test(description);
    if (!hasWhenIndicators) {
      this.warn('Description should include "when to use" indicators');
    } else {
      this.success('Description includes usage triggers');
    }

    // Check length
    if (tokens > 150) {
      this.warn(`Description is long (~${tokens} tokens). Consider keeping under 150 tokens`);
    } else if (tokens < 20) {
      this.warn(`Description is short (~${tokens} tokens). Add more specificity about when to use`);
    } else {
      this.success(`Description length is good (~${tokens} tokens)`);
    }

    return true;
  }

  // Validate allowed-tools field if present
  validateAllowedTools(metadata) {
    if (!metadata['allowed-tools']) {
      this.log('No allowed-tools restriction (skill has access to all tools)');
      return true;
    }

    const allowedTools = metadata['allowed-tools'];
    if (typeof allowedTools === 'string') {
      const tools = allowedTools.split(',').map(t => t.trim());
      this.success(`Tool restrictions defined: ${tools.join(', ')}`);
    } else {
      this.warn('allowed-tools should be a comma-separated string');
    }

    return true;
  }

  // Validate markdown body
  validateBody(content, bodyStartLine) {
    const lines = content.split('\n');
    const bodyContent = lines.slice(bodyStartLine).join('\n').trim();

    if (!bodyContent) {
      this.error('SKILL.md body is empty');
      return false;
    }

    const tokens = this.estimateTokens(bodyContent);
    this.log(`Body length: ${bodyContent.length} chars (~${tokens} tokens)`);

    if (tokens > 5000) {
      this.error(`Body exceeds 5k tokens (~${tokens} tokens). Move content to /reference/ files`);
    } else if (tokens > 2000) {
      this.warn(`Body is over 2k tokens (~${tokens} tokens). Consider moving details to /reference/`);
    } else {
      this.success(`Body token count is optimal (~${tokens} tokens, under 2k recommended)`);
    }

    return true;
  }

  // Validate file structure
  validateFileStructure() {
    const files = fs.readdirSync(this.skillPath);

    // Check for markdown files in root (only SKILL.md allowed)
    const rootMdFiles = files.filter(f =>
      f.endsWith('.md') && f !== 'SKILL.md'
    );

    if (rootMdFiles.length > 0) {
      this.error(`Markdown files found in root (should be in /reference/): ${rootMdFiles.join(', ')}`);
      this.error('Move these files to /reference/ folder');
    } else {
      this.success('No stray markdown files in root directory');
    }

    // Check for /reference/ folder
    const referencePath = path.join(this.skillPath, 'reference');
    if (fs.existsSync(referencePath) && fs.statSync(referencePath).isDirectory()) {
      const referenceFiles = fs.readdirSync(referencePath);
      const mdFiles = referenceFiles.filter(f => f.endsWith('.md'));

      if (mdFiles.length > 0) {
        this.success(`/reference/ folder exists with ${mdFiles.length} file(s): ${mdFiles.join(', ')}`);
      } else {
        this.warn('/reference/ folder exists but contains no markdown files');
      }
    } else {
      this.warn('/reference/ folder not found (optional, but recommended for detailed docs)');
    }

    // Check for scripts folder
    const scriptsPath = path.join(this.skillPath, 'scripts');
    if (fs.existsSync(scriptsPath)) {
      const scriptFiles = fs.readdirSync(scriptsPath);
      this.log(`/scripts/ folder exists with ${scriptFiles.length} file(s)`);
    }

    return rootMdFiles.length === 0;
  }

  // Validate paths in content (should use forward slashes)
  validatePaths(content) {
    const backslashPaths = content.match(/\]\([^)]*\\/g);

    if (backslashPaths && backslashPaths.length > 0) {
      this.warn('Found paths with backslashes. Use forward slashes for cross-platform compatibility');
      backslashPaths.forEach(match => {
        this.warn(`  Found: ${match}`);
      });
    } else {
      this.success('All paths use forward slashes');
    }

    // Check for reference links
    const referenceLinks = content.match(/\[.*?\]\(\.\/reference\/.*?\.md\)/g);
    if (referenceLinks && referenceLinks.length > 0) {
      this.success(`Found ${referenceLinks.length} links to /reference/ files`);

      // Validate that referenced files exist
      referenceLinks.forEach(link => {
        const match = link.match(/\(\.\/reference\/(.*?\.md)\)/);
        if (match) {
          const filename = match[1];
          const filepath = path.join(this.skillPath, 'reference', filename);
          if (!fs.existsSync(filepath)) {
            this.error(`Referenced file does not exist: ./reference/${filename}`);
          } else {
            this.success(`  ✓ ./reference/${filename} exists`);
          }
        }
      });
    }

    return true;
  }

  // Validate metadata token budget (~100 tokens)
  validateMetadataTokens(metadata) {
    const metadataStr = yaml.stringify(metadata);
    const tokens = this.estimateTokens(metadataStr);

    this.log(`Metadata token estimate: ~${tokens} tokens`);

    if (tokens > 150) {
      this.warn(`Metadata is large (~${tokens} tokens). Aim for ~100 tokens`);
    } else if (tokens > 100) {
      this.log('Metadata is slightly over 100 tokens but acceptable');
    } else {
      this.success(`Metadata token budget is optimal (~${tokens} tokens)`);
    }

    return true;
  }

  // Run all validations
  async validate() {
    console.log(`\n${colors.blue}╔════════════════════════════════════════════╗${colors.reset}`);
    console.log(`${colors.blue}║   Claude Code Skill Validator v1.0.0      ║${colors.reset}`);
    console.log(`${colors.blue}╚════════════════════════════════════════════╝${colors.reset}\n`);

    console.log(`Validating skill at: ${colors.cyan}${this.skillPath}${colors.reset}\n`);

    // Step 1: Directory validation
    console.log(`${colors.blue}[1/8]${colors.reset} Validating directory...`);
    if (!this.validateDirectory()) return this.generateReport();

    // Step 2: SKILL.md existence
    console.log(`\n${colors.blue}[2/8]${colors.reset} Checking for SKILL.md...`);
    if (!this.validateSkillMdExists()) return this.generateReport();

    // Read SKILL.md
    const content = fs.readFileSync(this.skillMdPath, 'utf-8');

    // Step 3: Frontmatter parsing
    console.log(`\n${colors.blue}[3/8]${colors.reset} Validating YAML frontmatter...`);
    const parsed = this.validateFrontmatter(content);
    if (!parsed) return this.generateReport();

    const { metadata, bodyStartLine } = parsed;

    // Step 4: Required fields
    console.log(`\n${colors.blue}[4/8]${colors.reset} Checking required fields...`);
    this.validateRequiredFields(metadata);

    // Step 5: Description quality
    console.log(`\n${colors.blue}[5/8]${colors.reset} Validating description...`);
    this.validateDescription(metadata.description);

    // Step 6: Optional fields
    console.log(`\n${colors.blue}[6/8]${colors.reset} Checking optional fields...`);
    this.validateAllowedTools(metadata);
    this.validateMetadataTokens(metadata);

    // Step 7: Body validation
    console.log(`\n${colors.blue}[7/8]${colors.reset} Validating body content...`);
    this.validateBody(content, bodyStartLine);

    // Step 8: File structure
    console.log(`\n${colors.blue}[8/8]${colors.reset} Validating file structure...`);
    this.validateFileStructure();
    this.validatePaths(content);

    return this.generateReport();
  }

  // Generate final report
  generateReport() {
    console.log(`\n${colors.blue}═══════════════════════════════════════════${colors.reset}`);
    console.log(`${colors.blue}VALIDATION REPORT${colors.reset}`);
    console.log(`${colors.blue}═══════════════════════════════════════════${colors.reset}\n`);

    if (this.errors.length === 0 && this.warnings.length === 0) {
      console.log(`${colors.green}✓ All validations passed! Skill structure is excellent.${colors.reset}\n`);
      return 0;
    }

    if (this.errors.length > 0) {
      console.log(`${colors.red}Errors: ${this.errors.length}${colors.reset}`);
      this.errors.forEach((err, i) => {
        console.log(`  ${i + 1}. ${err}`);
      });
      console.log('');
    }

    if (this.warnings.length > 0) {
      console.log(`${colors.yellow}Warnings: ${this.warnings.length}${colors.reset}`);
      this.warnings.forEach((warn, i) => {
        console.log(`  ${i + 1}. ${warn}`);
      });
      console.log('');
    }

    if (this.errors.length > 0) {
      console.log(`${colors.red}✗ Validation failed. Please fix errors before deploying.${colors.reset}\n`);
      return 1;
    } else {
      console.log(`${colors.yellow}⚠ Validation passed with warnings. Consider addressing warnings for best practices.${colors.reset}\n`);
      return 0;
    }
  }
}

// CLI entry point
async function main() {
  const args = process.argv.slice(2);

  if (args.length === 0 || args.includes('--help') || args.includes('-h')) {
    console.log(`
${colors.cyan}Claude Code Skill Validator${colors.reset}

${colors.blue}Usage:${colors.reset}
  node validate-skill.js <path-to-skill-directory>

${colors.blue}Examples:${colors.reset}
  node validate-skill.js ./my-skill
  node validate-skill.js ~/.claude/skills/my-skill
  node validate-skill.js .  (validate current directory)

${colors.blue}What it validates:${colors.reset}
  ✓ YAML frontmatter format (opening/closing ---)
  ✓ Required fields: name, description
  ✓ Description specificity and triggers
  ✓ Token budgets (metadata ~100, body <2k recommended)
  ✓ File structure (/reference/ folder for docs)
  ✓ No stray .md files in root (except SKILL.md)
  ✓ Path format (forward slashes)
  ✓ Referenced files exist
`);
    process.exit(0);
  }

  const skillPath = args[0];
  const validator = new SkillValidator(skillPath);
  const exitCode = await validator.validate();
  process.exit(exitCode);
}

// Run if called directly
if (require.main === module) {
  main().catch(err => {
    console.error(`${colors.red}Fatal error: ${err.message}${colors.reset}`);
    process.exit(1);
  });
}

module.exports = { SkillValidator };
