#!/usr/bin/env node
/**
 * create-issue.mjs
 *
 * Helper script for creating GitHub issues in NASA-PDS repositories.
 * Formats issue body according to template structure and creates via gh CLI.
 *
 * Usage:
 *   node scripts/create-issue.mjs <type> <repo> <title> <data.json>
 *
 * Arguments:
 *   type       Template type: bug, feature, task, vulnerability, theme
 *   repo       Repository name (without NASA-PDS/ prefix)
 *   title      Issue title
 *   data.json  JSON file with template field data
 *
 * Example:
 *   node scripts/create-issue.mjs bug pds-registry "Validator fails on nested tables" bug-data.json
 */

import { execSync } from 'child_process';
import { readFileSync } from 'fs';

const TEMPLATE_CONFIGS = {
  bug: {
    labels: 'bug,needs:triage',
    assignee: 'jordanpadams',
    formatBody: formatBugBody
  },
  feature: {
    labels: 'needs:triage,requirement',
    assignee: 'jordanpadams',
    formatBody: formatFeatureBody
  },
  task: {
    labels: 'task,i&t.skip',
    assignee: null,
    formatBody: formatTaskBody
  },
  vulnerability: {
    labels: 'security,bug,needs:triage',
    assignee: 'jordanpadams',
    formatBody: formatVulnerabilityBody
  },
  theme: {
    labels: 'theme,Epic,i&t.skip',
    assignee: null,
    formatBody: formatThemeBody
  }
};

/**
 * Format bug report body
 */
function formatBugBody(data) {
  return `## Checked for duplicates
${data.checkedDuplicates || "Yes - I've already checked"}

## 🐛 Describe the bug
${data.description}

## 🕵️ Expected behavior
${data.expectedBehavior}

## 📜 To Reproduce
${formatList(data.reproductionSteps)}

## 🖥 Environment Info
${formatList(data.environment)}

## 📚 Version of Software Used
${data.version || 'N/A'}

## 🩺 Test Data / Additional context
${data.testData || 'N/A'}

## 🦄 Related requirements
${data.relatedRequirements || 'N/A'}

---
## For Internal Dev Team To Complete

## ⚙️ Engineering Details
_To be filled by engineering team_

## 🎉 Integration & Test
_To be filled by engineering team_`;
}

/**
 * Format feature request body
 */
function formatFeatureBody(data) {
  return `## Checked for duplicates
${data.checkedDuplicates || "Yes - I've already checked"}

## 🧑‍🔬 User Persona(s)
${data.personas || 'N/A'}

## 💪 Motivation
...so that I can ${data.motivation}

## 📖 Additional Details
${data.additionalDetails || 'N/A'}

---
## For Internal Dev Team To Complete

## Acceptance Criteria
**Given** <!-- a condition -->
**When I perform** <!-- an action -->
**Then I expect** <!-- the result -->

## ⚙️ Engineering Details
_To be filled by engineering team_

## 🎉 I&T
_To be filled by engineering team_`;
}

/**
 * Format task body
 */
function formatTaskBody(data) {
  return `## Are you sure this is not a new requirement or bug?
${data.notRequirementOrBug || 'Yes'}

## Task Type
${data.taskType || 'Sub-task'}

## 💡 Description
${data.description}`;
}

/**
 * Format vulnerability body
 */
function formatVulnerabilityBody(data) {
  return `## Checked for duplicates
${data.checkedDuplicates || "Yes - I've already checked"}

## 🐛 Describe the vulnerability
${data.description}

## 🕵️ Expected behavior
${data.expectedBehavior}

## 📜 To Reproduce
${formatList(data.reproductionSteps)}

## 🖥 Environment Info
${formatList(data.environment)}

## 📚 Version of Software Used
${data.version || 'N/A'}

## 🩺 Test Data / Additional context
${data.testData || 'N/A'}

## 🦄 Related requirements
${data.relatedRequirements || 'N/A'}

---
## For Internal Dev Team To Complete

## ⚙️ Engineering Details
_To be filled by engineering team_`;
}

/**
 * Format release theme body
 */
function formatThemeBody(data) {
  return `## Are you sure this is not a new requirement or bug?
${data.notRequirementOrBug || 'Yes'}

## 💡 Description
${data.description}`;
}

/**
 * Format array as numbered or bulleted list
 */
function formatList(items) {
  if (typeof items === 'string') {
    return items;
  }

  if (!Array.isArray(items)) {
    return 'N/A';
  }

  return items.map((item, index) => `${index + 1}. ${item}`).join('\n');
}

/**
 * Create GitHub issue
 */
function createIssue(type, repo, title, bodyData) {
  const config = TEMPLATE_CONFIGS[type];

  if (!config) {
    throw new Error(`Invalid template type: ${type}`);
  }

  // Format body according to template
  const body = config.formatBody(bodyData);

  // Build gh command
  let command = `gh issue create --repo NASA-PDS/${repo}`;
  command += ` --title "${title.replace(/"/g, '\\"')}"`;
  command += ` --label "${config.labels}"`;

  if (config.assignee) {
    command += ` --assignee ${config.assignee}`;
  }

  // Write body to temp file to avoid command-line length limits
  const bodyFile = `/tmp/gh-issue-body-${Date.now()}.md`;
  writeFileSync(bodyFile, body, 'utf8');
  command += ` --body-file "${bodyFile}"`;

  console.log(`Creating ${type} issue in NASA-PDS/${repo}...`);
  console.log(`Title: ${title}`);
  console.log(`Labels: ${config.labels}`);

  try {
    const result = execSync(command, { encoding: 'utf8' });
    console.log('\nIssue created successfully!');
    console.log(result.trim());

    // Clean up temp file
    execSync(`rm "${bodyFile}"`);

    return result.trim();
  } catch (error) {
    console.error('\nError creating issue:');
    console.error(error.message);
    process.exit(1);
  }
}

// Parse arguments
const [type, repo, title, dataFile] = process.argv.slice(2);

if (!type || !repo || !title || !dataFile) {
  console.error('Usage: node create-issue.mjs <type> <repo> <title> <data.json>');
  console.error('Types: bug, feature, task, vulnerability, theme');
  process.exit(1);
}

// Load data
let bodyData;
try {
  bodyData = JSON.parse(readFileSync(dataFile, 'utf8'));
} catch (error) {
  console.error(`Error reading data file: ${error.message}`);
  process.exit(1);
}

// Import writeFileSync
import { writeFileSync } from 'fs';

// Create issue
createIssue(type, repo, title, bodyData);
