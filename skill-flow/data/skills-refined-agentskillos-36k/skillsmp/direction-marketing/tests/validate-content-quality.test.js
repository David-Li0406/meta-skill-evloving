#!/usr/bin/env node
/**
 * Validates content quality of direction-marketing agents
 *
 * Checks:
 * - Minimum line count (50 lines)
 * - Required sections present
 * - YAML frontmatter complete
 *
 * @see docs/agent-template-standards.md for standards reference
 */

const fs = require('fs');
const path = require('path');
const { SKILL_ROOT, DOMAINS } = require('./config');

// Configuration - aligned with docs/agent-template-standards.md
const MIN_AGENT_LINES = 100;
const MIN_ENRICHED_AGENT_LINES = 200;

const REQUIRED_SECTIONS = [
  'Responsabilité',  // "Ta Responsabilité Unique" or "Ta Responsabilité"
  'Inputs',          // "Inputs Acceptés" or similar
  'Livrables'        // Output section
];

const RECOMMENDED_SECTIONS = [
  'Tu NE fais PAS',
  'Template de Sortie',
  'Bonnes Pratiques',
  'Pièges à Éviter'
];

const REQUIRED_YAML_FIELDS = ['name', 'description', 'domain'];

// Enriched agents that should have more content
const ENRICHED_AGENTS = [
  'strategie/competitor-analysis',
  'strategie/swot-marketing',
  'strategie/roadmap-marketing',
  'mesure/attribution-model',
  'positionnement/persona-builder'
];

let errors = 0;
let warnings = 0;
const issues = [];

console.log('🔍 Validating content quality of direction-marketing agents...\n');

/**
 * Parse YAML frontmatter from markdown content
 */
function parseYamlFrontmatter(content) {
  const match = content.match(/^---\n([\s\S]*?)\n---/);
  if (!match) return null;

  const yaml = {};
  const lines = match[1].split('\n');
  for (const line of lines) {
    const colonIndex = line.indexOf(':');
    if (colonIndex > 0) {
      const key = line.slice(0, colonIndex).trim();
      const value = line.slice(colonIndex + 1).trim();
      yaml[key] = value;
    }
  }
  return yaml;
}

/**
 * Check if content contains a section (case-insensitive partial match)
 */
function hasSection(content, sectionName) {
  const regex = new RegExp(`^##\\s+.*${sectionName}`, 'im');
  return regex.test(content);
}

/**
 * Validate a single agent file
 */
function validateAgent(agentPath, domain, agentName) {
  const relativePath = `${domain}/${agentName}`;
  const content = fs.readFileSync(agentPath, 'utf8');
  const lines = content.split('\n').length;

  const agentIssues = [];

  // 1. Check line count
  const isEnriched = ENRICHED_AGENTS.includes(relativePath);
  const minLines = isEnriched ? MIN_ENRICHED_AGENT_LINES : MIN_AGENT_LINES;

  if (lines < minLines) {
    agentIssues.push({
      type: 'error',
      message: `Only ${lines} lines (minimum: ${minLines})`
    });
  }

  // 2. Check YAML frontmatter
  const yaml = parseYamlFrontmatter(content);
  if (!yaml) {
    agentIssues.push({
      type: 'error',
      message: 'Missing YAML frontmatter'
    });
  } else {
    for (const field of REQUIRED_YAML_FIELDS) {
      if (!yaml[field]) {
        agentIssues.push({
          type: 'error',
          message: `Missing YAML field: ${field}`
        });
      }
    }

    // Check domain matches directory
    if (yaml.domain && yaml.domain !== domain) {
      agentIssues.push({
        type: 'warning',
        message: `YAML domain '${yaml.domain}' doesn't match directory '${domain}'`
      });
    }
  }

  // 3. Check required sections
  for (const section of REQUIRED_SECTIONS) {
    if (!hasSection(content, section)) {
      agentIssues.push({
        type: 'error',
        message: `Missing required section: ${section}`
      });
    }
  }

  // 4. Check recommended sections (warnings only)
  for (const section of RECOMMENDED_SECTIONS) {
    if (!hasSection(content, section)) {
      agentIssues.push({
        type: 'warning',
        message: `Missing recommended section: ${section}`
      });
    }
  }

  return agentIssues;
}

// Validate all agents
for (const domain of DOMAINS) {
  const domainPath = path.join(SKILL_ROOT, 'agents', domain);

  if (!fs.existsSync(domainPath)) {
    continue;
  }

  const agents = fs.readdirSync(domainPath)
    .filter(f => f.endsWith('.md'));

  for (const agentFile of agents) {
    const agentPath = path.join(domainPath, agentFile);
    const agentName = agentFile.replace('.md', '');
    const relativePath = `${domain}/${agentName}`;

    const agentIssues = validateAgent(agentPath, domain, agentName);

    if (agentIssues.length > 0) {
      const agentErrors = agentIssues.filter(i => i.type === 'error');
      const agentWarnings = agentIssues.filter(i => i.type === 'warning');

      if (agentErrors.length > 0) {
        console.log(`❌ ${relativePath}`);
        for (const issue of agentErrors) {
          console.log(`   └─ ${issue.message}`);
        }
        errors += agentErrors.length;
      }

      if (agentWarnings.length > 0) {
        if (agentErrors.length === 0) {
          console.log(`⚠️  ${relativePath}`);
        }
        for (const issue of agentWarnings) {
          console.log(`   └─ ⚠️  ${issue.message}`);
        }
        warnings += agentWarnings.length;
      }

      issues.push({ agent: relativePath, issues: agentIssues });
    } else {
      console.log(`✅ ${relativePath}`);
    }
  }
}

// Summary
console.log('\n================================');
console.log('📊 Content Quality Summary');
console.log('================================');
console.log(`Minimum lines (standard): ${MIN_AGENT_LINES}`);
console.log(`Minimum lines (enriched): ${MIN_ENRICHED_AGENT_LINES}`);
console.log(`Required sections: ${REQUIRED_SECTIONS.join(', ')}`);
console.log(`Recommended sections: ${RECOMMENDED_SECTIONS.join(', ')}`);
console.log('');

if (errors > 0) {
  console.log(`❌ ${errors} error(s), ${warnings} warning(s)`);
  console.log('\nRun with --fix to see suggestions for fixing issues.');
  process.exit(1);
} else if (warnings > 0) {
  console.log(`✅ No errors, but ${warnings} warning(s) to review`);
  process.exit(0);
} else {
  console.log('✅ All content quality checks passed!');
  process.exit(0);
}
