#!/usr/bin/env node
/**
 * cache-templates.mjs
 *
 * Fetches and caches NASA-PDS issue templates from the .github repository.
 * Templates are stored locally to avoid repeated GitHub API calls.
 *
 * Usage:
 *   node scripts/cache-templates.mjs [--force]
 *
 * Options:
 *   --force    Force refresh even if cache is recent
 */

import { execSync } from 'child_process';
import { writeFileSync, readFileSync, existsSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const CACHE_DIR = join(__dirname, '../resources/templates');
const TIMESTAMP_FILE = join(CACHE_DIR, '.cache-timestamp');
const CACHE_MAX_AGE_DAYS = 7;

const TEMPLATES = [
  '-bug_report.yml',
  'i-t-bug-report.yml',
  '-feature_request.yml',
  '-vulnerability-issue.yml',
  'task.yml',
  'release-theme.yml',
  'config.yml'
];

/**
 * Check if cache is fresh (less than CACHE_MAX_AGE_DAYS old)
 */
function isCacheFresh() {
  if (!existsSync(TIMESTAMP_FILE)) {
    return false;
  }

  const timestamp = parseInt(readFileSync(TIMESTAMP_FILE, 'utf8'));
  const ageMs = Date.now() - timestamp;
  const ageDays = ageMs / (1000 * 60 * 60 * 24);

  return ageDays < CACHE_MAX_AGE_DAYS;
}

/**
 * Fetch a template file from GitHub
 */
function fetchTemplate(templateName) {
  console.log(`Fetching ${templateName}...`);

  try {
    const downloadUrl = execSync(
      `gh api repos/NASA-PDS/.github/contents/.github/ISSUE_TEMPLATE/${templateName} --jq '.download_url'`,
      { encoding: 'utf8' }
    ).trim();

    const content = execSync(`curl -sL "${downloadUrl}"`, { encoding: 'utf8' });

    return content;
  } catch (error) {
    console.error(`Error fetching ${templateName}:`, error.message);
    return null;
  }
}

/**
 * Main caching function
 */
function cacheTemplates(force = false) {
  // Check if we need to refresh
  if (!force && isCacheFresh()) {
    console.log('Template cache is fresh. Use --force to refresh.');
    console.log(`Cache location: ${CACHE_DIR}`);
    return;
  }

  console.log('Caching NASA-PDS issue templates...');

  // Create cache directory if it doesn't exist
  if (!existsSync(CACHE_DIR)) {
    mkdirSync(CACHE_DIR, { recursive: true });
  }

  // Fetch and cache each template
  let successCount = 0;
  for (const template of TEMPLATES) {
    const content = fetchTemplate(template);

    if (content) {
      const outputPath = join(CACHE_DIR, template);
      writeFileSync(outputPath, content, 'utf8');
      successCount++;
    }
  }

  // Update timestamp
  writeFileSync(TIMESTAMP_FILE, Date.now().toString(), 'utf8');

  console.log(`\nSuccessfully cached ${successCount}/${TEMPLATES.length} templates`);
  console.log(`Cache location: ${CACHE_DIR}`);
  console.log(`Cache will expire in ${CACHE_MAX_AGE_DAYS} days`);
}

// Parse command-line arguments
const args = process.argv.slice(2);
const force = args.includes('--force');

// Run
try {
  // Verify gh CLI is available
  execSync('gh --version', { stdio: 'ignore' });
  cacheTemplates(force);
} catch (error) {
  console.error('Error: GitHub CLI (gh) is not installed or not authenticated.');
  console.error('Install: https://cli.github.com/');
  console.error('Authenticate: gh auth login');
  process.exit(1);
}
