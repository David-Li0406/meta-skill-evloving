#!/usr/bin/env node
/**
 * Test: Validate Markdown Quality
 *
 * Validates markdown files for:
 * - Internal link integrity (references to other agents)
 * - Code block syntax validity
 * - Heading structure
 * - Table formatting
 *
 * @module tests/validate-markdown
 */

const path = require('path');
const {
  findMarkdownFiles,
  safeReadFile,
  directoryExists,
  fileExists,
  TestReporter
} = require('./utils');
const { SKILL_ROOT, DOMAINS } = require('./config');

const reporter = new TestReporter('validate-markdown');

/**
 * Extract internal links from markdown content
 * @param {string} content - Markdown content
 * @returns {string[]} Array of internal link targets
 */
function extractInternalLinks(content) {
  const links = [];
  const linkPattern = /\[([^\]]+)\]\(([^)]+)\)/g;
  let match;

  while ((match = linkPattern.exec(content)) !== null) {
    const target = match[2];
    if (!target.startsWith('http') && !target.startsWith('#') && !target.startsWith('mailto:')) {
      links.push(target);
    }
  }

  return links;
}

/**
 * Validate code blocks in content
 * @param {string} content - Markdown content
 * @returns {{ valid: number, invalid: string[] }}
 */
function validateCodeBlocks(content) {
  const valid = [];
  const invalid = [];

  const validLanguages = [
    'bash', 'sh', 'shell', 'zsh', 'shell-session',
    'javascript', 'js', 'typescript', 'ts', 'jsx', 'tsx',
    'python', 'py',
    'json', 'yaml', 'yml', 'xml', 'html', 'css', 'scss', 'sql',
    'markdown', 'md', 'mermaid',
    'php', 'ruby', 'go', 'rust', 'java', 'kotlin', 'swift',
    'objective-c', 'objc', 'c', 'cpp', 'c++', 'csharp', 'cs',
    'dockerfile', 'docker', 'nginx', 'apache', 'terraform', 'hcl',
    'graphql', 'prisma', 'makefile', 'make', 'promql',
    'diff', 'patch', 'text', 'txt', 'plain',
    '',
  ];

  // Pattern supports hyphenated languages like objective-c, shell-session
  const codeBlockPattern = /```([\w-]*)[ \t]*(?:\n|$)/g;
  let match;

  while ((match = codeBlockPattern.exec(content)) !== null) {
    const lang = match[1].toLowerCase();
    if (validLanguages.includes(lang)) {
      valid.push(lang || 'generic');
    } else {
      invalid.push(lang);
    }
  }

  const openBlocks = (content.match(/```/g) || []).length;
  if (openBlocks % 2 !== 0) {
    invalid.push('UNCLOSED_BLOCK');
  }

  return { valid: valid.length, invalid };
}

/**
 * Validate heading structure
 * @param {string} content - Markdown content
 * @returns {{ valid: boolean, issues: string[] }}
 */
function validateHeadings(content) {
  const issues = [];

  if (!content.match(/^#\s+.+$/m)) {
    issues.push('Missing H1 heading');
  }

  const h1Count = (content.match(/^#\s+.+$/gm) || []).length;
  if (h1Count > 1) {
    issues.push(`Multiple H1 headings (${h1Count})`);
  }

  const headings = content.match(/^#{1,6}\s+.+$/gm) || [];
  let prevLevel = 0;

  for (const heading of headings) {
    const level = heading.match(/^(#+)/)[1].length;
    if (prevLevel > 0 && level > prevLevel + 1) {
      issues.push(`Heading level skip: H${prevLevel} → H${level}`);
      break;
    }
    prevLevel = level;
  }

  return { valid: issues.length === 0, issues };
}

/**
 * Validate table formatting
 * @param {string} content - Markdown content
 * @returns {{ count: number, malformed: number }}
 */
function validateTables(content) {
  let count = 0;
  let malformed = 0;

  const lines = content.split('\n');
  let inTable = false;
  let tableColumns = 0;

  for (const line of lines) {
    const trimmed = line.trim();

    if (trimmed.startsWith('|') && trimmed.endsWith('|')) {
      if (!inTable) {
        inTable = true;
        count++;
        tableColumns = (trimmed.match(/\|/g) || []).length - 1;
      } else {
        const cols = (trimmed.match(/\|/g) || []).length - 1;
        if (cols !== tableColumns && !trimmed.match(/^[\|\s:-]+$/)) {
          malformed++;
        }
      }
    } else if (inTable && trimmed !== '') {
      inTable = false;
      tableColumns = 0;
    }
  }

  return { count, malformed };
}

// Main execution
reporter.header('Validating Markdown Quality');

// Collect all files
const allFiles = [];
for (const domain of DOMAINS) {
  const domainDir = path.join(SKILL_ROOT, 'agents', domain);
  if (directoryExists(domainDir)) {
    allFiles.push(...findMarkdownFiles(domainDir));
  }
}

const skillMdPath = path.join(SKILL_ROOT, 'SKILL.md');
if (fileExists(skillMdPath)) {
  allFiles.push(skillMdPath);
}

reporter.section('Markdown File Validation');
reporter.info(`Found ${allFiles.length} markdown files to validate`);

let filesWithIssues = 0;

for (const file of allFiles) {
  const relativePath = path.relative(SKILL_ROOT, file);
  const { content, error } = safeReadFile(file);

  if (error) {
    reporter.fail(`${relativePath}: ${error}`, { file: relativePath, path: file });
    continue;
  }

  const fileIssues = [];

  const headingResult = validateHeadings(content);
  if (!headingResult.valid) {
    fileIssues.push(...headingResult.issues);
  }

  const codeResult = validateCodeBlocks(content);
  if (codeResult.invalid.length > 0) {
    for (const lang of codeResult.invalid) {
      if (lang === 'UNCLOSED_BLOCK') {
        fileIssues.push('Unclosed code block');
      } else {
        fileIssues.push(`Unknown code language: ${lang}`);
      }
    }
  }

  const tableResult = validateTables(content);
  if (tableResult.malformed > 0) {
    fileIssues.push(`${tableResult.malformed} malformed table(s)`);
  }

  if (fileIssues.length === 0) {
    reporter.pass(relativePath, { file: relativePath });
  } else {
    filesWithIssues++;
    reporter.warn(`${relativePath}: ${fileIssues.join(', ')}`);
  }
}

// 2. Validate internal links
reporter.section('Internal Link Validation');

let brokenLinks = [];
let totalLinks = 0;

for (const file of allFiles) {
  const { content } = safeReadFile(file);
  if (!content) continue;

  const links = extractInternalLinks(content);
  totalLinks += links.length;

  const fileDir = path.dirname(file);

  for (const link of links) {
    const targetPath = link.startsWith('/')
      ? path.join(SKILL_ROOT, link)
      : path.join(fileDir, link);

    const cleanPath = targetPath.split('#')[0];

    if (cleanPath && !fileExists(cleanPath) && !directoryExists(cleanPath)) {
      brokenLinks.push({
        from: path.relative(SKILL_ROOT, file),
        to: link
      });
    }
  }
}

if (brokenLinks.length === 0) {
  reporter.pass(`All ${totalLinks} internal links valid`, { totalLinks });
} else {
  reporter.warn(`${brokenLinks.length} potentially broken links`);
}

// 3. Code block statistics
reporter.section('Statistics');

const langCounts = new Map();
let totalCodeBlocks = 0;

for (const file of allFiles) {
  const { content } = safeReadFile(file);
  if (!content) continue;

  const codeBlockPattern = /```([\w-]*)[ \t]*(?:\n|$)/g;
  let match;

  while ((match = codeBlockPattern.exec(content)) !== null) {
    const lang = match[1] || 'generic';
    langCounts.set(lang, (langCounts.get(lang) || 0) + 1);
    totalCodeBlocks++;
  }
}

reporter.info(`${totalCodeBlocks} code blocks, ${allFiles.length} files checked`);

reporter.summarize();
