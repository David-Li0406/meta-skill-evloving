#!/usr/bin/env node

/**
 * SonarCloud Security Issues Fetcher
 *
 * Fetches all security vulnerabilities and hotspots from SonarCloud
 * for a given organization and exports to CSV.
 *
 * Usage: node fetch-security-issues.mjs <organization> [output-file.csv]
 *
 * Environment: SONARCLOUD_TOKEN (required)
 *
 * Security:
 *   - API token sourced from environment variable (never hardcoded)
 *   - Token validated at startup before any API calls
 *   - Token never logged or exposed in error messages
 *   - Used only in Authorization headers for SonarCloud API
 */

import { writeFileSync } from 'fs';

const SONARCLOUD_BASE_URL = 'https://sonarcloud.io/api';
const SONARCLOUD_TOKEN = process.env.SONARCLOUD_TOKEN;

// Parse command line arguments
const args = process.argv.slice(2);
if (args.length === 0) {
  console.error('❌ Error: Organization key is required');
  console.error('Usage: node fetch-security-issues.mjs <organization> [output-file.csv]');
  process.exit(1);
}

const organization = args[0];
const outputFile = args[1] || `sonarcloud-security-issues-${Date.now()}.csv`;

// Validate token
if (!SONARCLOUD_TOKEN) {
  console.error('❌ Error: SONARCLOUD_TOKEN environment variable is not set');
  console.error('Generate a token at: https://sonarcloud.io/account/security');
  console.error('Then set it: export SONARCLOUD_TOKEN=your_token_here');
  process.exit(1);
}

/**
 * Make authenticated request to SonarCloud API with retry logic
 */
async function fetchSonarCloud(endpoint, params = {}) {
  const url = new URL(`${SONARCLOUD_BASE_URL}${endpoint}`);
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null) {
      url.searchParams.append(key, value);
    }
  });

  const maxRetries = 3;
  let attempt = 0;

  while (attempt < maxRetries) {
    try {
      const response = await fetch(url.toString(), {
        headers: {
          'Authorization': `Bearer ${SONARCLOUD_TOKEN}`,
          'Accept': 'application/json'
        }
      });

      // Handle rate limiting
      if (response.status === 429) {
        console.warn('⚠️  Rate limit hit, waiting 60 seconds...');
        await sleep(60000);
        attempt++;
        continue;
      }

      // Handle authentication errors
      if (response.status === 401) {
        console.error('❌ Authentication failed. Check your SONARCLOUD_TOKEN.');
        process.exit(1);
      }

      // Handle other errors
      if (!response.ok) {
        const text = await response.text();
        throw new Error(`HTTP ${response.status}: ${text}`);
      }

      return await response.json();
    } catch (error) {
      attempt++;
      if (attempt >= maxRetries) {
        throw error;
      }
      console.warn(`⚠️  Request failed (attempt ${attempt}/${maxRetries}), retrying...`);
      await sleep(2000 * attempt); // Exponential backoff
    }
  }
}

/**
 * Sleep for specified milliseconds
 */
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Fetch all projects in the organization with pagination
 */
async function fetchAllProjects(organization) {
  console.log(`📋 Fetching projects for organization: ${organization}`);

  const projects = [];
  let page = 1;
  const pageSize = 500; // Max allowed by API
  let hasMore = true;

  while (hasMore) {
    const data = await fetchSonarCloud('/projects/search', {
      organization,
      p: page,
      ps: pageSize
    });

    projects.push(...data.components);
    console.log(`   Found ${data.components.length} projects (page ${page})`);

    hasMore = data.paging.total > page * pageSize;
    page++;
  }

  console.log(`✅ Total projects: ${projects.length}\n`);
  return projects;
}

/**
 * Fetch all vulnerabilities for a project with pagination
 */
async function fetchVulnerabilities(organization, projectKey) {
  const issues = [];
  let page = 1;
  const pageSize = 500;
  let hasMore = true;

  while (hasMore) {
    const data = await fetchSonarCloud('/issues/search', {
      organization,
      componentKeys: projectKey,
      types: 'VULNERABILITY',
      p: page,
      ps: pageSize
    });

    issues.push(...data.issues);

    hasMore = data.paging.total > page * pageSize;
    page++;
  }

  return issues;
}

/**
 * Fetch all security hotspots for a project with pagination
 */
async function fetchHotspots(organization, projectKey) {
  const hotspots = [];
  let page = 1;
  const pageSize = 500;
  let hasMore = true;

  while (hasMore) {
    try {
      const data = await fetchSonarCloud('/hotspots/search', {
        projectKey,
        p: page,
        ps: pageSize
      });

      hotspots.push(...data.hotspots);

      hasMore = data.paging.total > page * pageSize;
      page++;
    } catch (error) {
      // Some projects may not support hotspots API
      console.warn(`   ⚠️  Could not fetch hotspots: ${error.message}`);
      break;
    }
  }

  return hotspots;
}

/**
 * Convert vulnerability to CSV row
 */
function vulnerabilityToRow(issue, projectKey) {
  return {
    project: projectKey,
    type: 'VULNERABILITY',
    severity: issue.severity || '',
    status: issue.status || '',
    rule: issue.rule || '',
    message: (issue.message || '').replace(/"/g, '""'), // Escape quotes
    component: issue.component || '',
    line: issue.line || '',
    created: issue.creationDate || '',
    url: `https://sonarcloud.io/project/issues?open=${issue.key}&id=${projectKey}`
  };
}

/**
 * Convert security hotspot to CSV row
 */
function hotspotToRow(hotspot, projectKey) {
  return {
    project: projectKey,
    type: 'SECURITY_HOTSPOT',
    severity: '', // Hotspots don't have severity
    status: hotspot.status || '',
    rule: hotspot.rule || '',
    message: (hotspot.message || '').replace(/"/g, '""'), // Escape quotes
    component: hotspot.component || '',
    line: hotspot.line || '',
    created: hotspot.creationDate || '',
    url: `https://sonarcloud.io/project/security_hotspots?id=${projectKey}&hotspots=${hotspot.key}`
  };
}

/**
 * Export issues to CSV
 */
function exportToCSV(rows, filename) {
  const headers = [
    'Project',
    'Type',
    'Severity',
    'Status',
    'Rule',
    'Message',
    'Component',
    'Line',
    'Created',
    'URL'
  ];

  const csvLines = [
    headers.join(','),
    ...rows.map(row => [
      row.project,
      row.type,
      row.severity,
      row.status,
      row.rule,
      `"${row.message}"`,
      row.component,
      row.line,
      row.created,
      row.url
    ].join(','))
  ];

  writeFileSync(filename, csvLines.join('\n'), 'utf-8');
}

/**
 * Main execution
 */
async function main() {
  console.log('🔍 SonarCloud Security Audit\n');
  console.log(`Organization: ${organization}`);
  console.log(`Output file: ${outputFile}\n`);

  try {
    // Fetch all projects
    const projects = await fetchAllProjects(organization);

    if (projects.length === 0) {
      console.warn('⚠️  No projects found in organization');
      process.exit(0);
    }

    // Fetch security issues for each project
    const allRows = [];
    let totalVulnerabilities = 0;
    let totalHotspots = 0;

    for (let i = 0; i < projects.length; i++) {
      const project = projects[i];
      const projectKey = project.key;

      console.log(`[${i + 1}/${projects.length}] Processing: ${projectKey}`);

      // Fetch vulnerabilities
      const vulnerabilities = await fetchVulnerabilities(organization, projectKey);
      totalVulnerabilities += vulnerabilities.length;
      console.log(`   📊 Vulnerabilities: ${vulnerabilities.length}`);

      vulnerabilities.forEach(vuln => {
        allRows.push(vulnerabilityToRow(vuln, projectKey));
      });

      // Fetch security hotspots
      const hotspots = await fetchHotspots(organization, projectKey);
      totalHotspots += hotspots.length;
      console.log(`   🔥 Security Hotspots: ${hotspots.length}`);

      hotspots.forEach(hotspot => {
        allRows.push(hotspotToRow(hotspot, projectKey));
      });

      // Small delay to be nice to the API
      await sleep(500);
    }

    // Export to CSV
    console.log('\n📝 Exporting to CSV...');
    exportToCSV(allRows, outputFile);

    // Summary
    console.log('\n✅ Security audit complete!\n');
    console.log(`📊 Summary:`);
    console.log(`   Projects scanned: ${projects.length}`);
    console.log(`   Vulnerabilities: ${totalVulnerabilities}`);
    console.log(`   Security Hotspots: ${totalHotspots}`);
    console.log(`   Total issues: ${allRows.length}`);
    console.log(`\n📄 Output file: ${outputFile}`);

    // Triage suggestions
    if (allRows.length > 0) {
      console.log('\n💡 Triage suggestions:');
      console.log('   1. Sort by Severity (BLOCKER, CRITICAL first)');
      console.log('   2. Filter by Status (OPEN, CONFIRMED)');
      console.log('   3. Group by Rule for bulk remediation');

      const blockerCount = allRows.filter(r => r.severity === 'BLOCKER').length;
      const criticalCount = allRows.filter(r => r.severity === 'CRITICAL').length;

      if (blockerCount > 0 || criticalCount > 0) {
        console.log(`\n⚠️  High priority: ${blockerCount} BLOCKER + ${criticalCount} CRITICAL issues`);
      }
    }

  } catch (error) {
    console.error(`\n❌ Error: ${error.message}`);
    console.error(error.stack);
    process.exit(1);
  }
}

// Run the script
main();
