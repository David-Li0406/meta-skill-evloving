#!/usr/bin/env node
/**
 * Test: Validate Markdown Syntax
 *
 * Validates basic markdown syntax:
 * - Valid YAML frontmatter
 * - Proper heading hierarchy
 * - No broken links (internal references)
 * - Code blocks have language specified
 *
 * @module tests/validate-markdown
 */

const path = require('path');
const {
  findMarkdownFiles,
  safeReadFile,
  parseFrontmatter,
  directoryExists,
  TestReporter
} = require('./utils');
const { SKILL_ROOT, DOMAINS } = require('./config');

const reporter = new TestReporter('validate-markdown');

/**
 * Validate markdown syntax in a file
 *
 * @param {string} filePath - Path to file
 * @returns {{ errors: string[], warnings: string[] }}
 */
function validateMarkdown(filePath) {
  const errors = [];
  const warnings = [];

  const { content, error } = safeReadFile(filePath);
  if (error) {
    return { errors: [error], warnings: [] };
  }

  // Check frontmatter
  const frontmatter = parseFrontmatter(content);
  if (!frontmatter) {
    errors.push('Invalid or missing YAML frontmatter');
  }

  // Check heading hierarchy (H1 should come first)
  const headingMatches = content.match(/^#+\s/gm);
  if (headingMatches && headingMatches.length > 0) {
    const firstHeading = headingMatches[0];
    if (!firstHeading.startsWith('# ')) {
      warnings.push('First heading should be H1');
    }
  }

  // Check for code blocks without language
  const codeBlockMatches = content.match(/```\n/g);
  if (codeBlockMatches && codeBlockMatches.length > 0) {
    warnings.push(`${codeBlockMatches.length} code block(s) without language specified`);
  }

  // Check for broken internal links
  const linkMatches = content.match(/\[([^\]]+)\]\(([^)]+)\)/g) || [];
  for (const link of linkMatches) {
    const match = link.match(/\[([^\]]+)\]\(([^)]+)\)/);
    if (match) {
      const href = match[2];
      // Check relative links
      if (href.startsWith('./') || href.startsWith('../')) {
        const targetPath = path.resolve(path.dirname(filePath), href);
        const { error: readError } = safeReadFile(targetPath);
        if (readError) {
          warnings.push(`Potentially broken link: ${href}`);
        }
      }
    }
  }

  return { errors, warnings };
}

reporter.header('Validating Markdown Syntax');

// Validate SKILL.md
const skillPath = path.join(SKILL_ROOT, 'SKILL.md');
const { errors: skillErrors, warnings: skillWarnings } = validateMarkdown(skillPath);
if (skillErrors.length === 0) {
  reporter.pass('SKILL.md');
} else {
  reporter.fail(`SKILL.md: ${skillErrors.join(', ')}`);
}

// Validate orchestrator.md
const orchestratorPath = path.join(SKILL_ROOT, 'orchestrator.md');
const { errors: orchErrors } = validateMarkdown(orchestratorPath);
if (orchErrors.length === 0) {
  reporter.pass('orchestrator.md');
} else {
  reporter.fail(`orchestrator.md: ${orchErrors.join(', ')}`);
}

// Validate domain agents
for (const domain of DOMAINS) {
  const domainDir = path.join(SKILL_ROOT, 'agents', domain);

  if (!directoryExists(domainDir)) {
    continue;
  }

  reporter.section(`Domain: ${domain}`);

  const files = findMarkdownFiles(domainDir);
  for (const file of files) {
    const relativePath = path.relative(SKILL_ROOT, file);
    const { errors, warnings } = validateMarkdown(file);

    if (errors.length === 0) {
      if (warnings.length === 0) {
        reporter.pass(relativePath);
      } else {
        reporter.pass(`${relativePath} (${warnings.length} warning${warnings.length > 1 ? 's' : ''})`);
      }
    } else {
      reporter.fail(`${relativePath}: ${errors.join(', ')}`);
    }
  }
}

reporter.summarize();
