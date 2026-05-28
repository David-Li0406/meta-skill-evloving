/**
 * Centralized configuration for Testing Process skill tests
 *
 * ## Naming Conventions
 *
 * - Domains: lowercase-kebab-case (e.g., `strategy`, `quality`)
 * - Agents: lowercase-kebab-case (e.g., `tdd-bdd`, `frontend-perf`)
 *
 * These conventions are enforced by validation tests.
 *
 * @module tests/config
 */

const path = require('path');

/** @const {string} Base directory for the skill */
const SKILL_ROOT = path.join(__dirname, '..');

/** @const {string[]} Testing Process domains */
const DOMAINS = [
  'strategy',
  'types',
  'quality',
  'performance',
  'security',
  'accessibility'
];

/** @const {Object} Expected agents per domain */
const EXPECTED_AGENTS_PER_DOMAIN = {
  'strategy': [
    'orchestrator',
    'pyramide',
    'tdd-bdd',
    'planning',
    'documentation'
  ],
  'types': [
    'orchestrator',
    'unit',
    'integration',
    'e2e',
    'component'
  ],
  'quality': [
    'orchestrator',
    'coverage',
    'mutation',
    'flaky'
  ],
  'performance': [
    'orchestrator',
    'load',
    'frontend-perf',
    'profiling'
  ],
  'security': [
    'orchestrator',
    'owasp',
    'dependencies',
    'headers'
  ],
  'accessibility': [
    'orchestrator',
    'wcag',
    'audit'
  ]
};

/**
 * Agent validation requirements
 *
 * @const {Object}
 */
const AGENT_REQUIREMENTS = {
  /** Required frontmatter fields */
  frontmatter: ['name', 'description'],

  /**
   * Minimum content length for orchestrators (characters)
   * Higher threshold: needs routing table + decision tree + examples
   */
  minOrchestratorLength: 500,

  /**
   * Minimum content length for specialized agents (characters)
   * Lower threshold: focused content with methodology
   */
  minAgentLength: 400,

  /** Legacy threshold for backwards compatibility */
  minContentLength: 400,

  /** Expected sections for orchestrators */
  orchestratorSections: ['Agents', 'Routage'],

  /** Expected sections for methodology agents */
  agentSections: ['Mission', 'Livrables']
};

/**
 * Domain keywords for routing validation
 *
 * @const {Object}
 */
const DOMAIN_KEYWORDS = {
  'strategy': ['pyramide', 'TDD', 'BDD', 'planning', 'strategie', 'ratio'],
  'types': ['unit', 'integration', 'e2e', 'end-to-end', 'component', 'mock'],
  'quality': ['coverage', 'couverture', 'mutation', 'flaky', 'instable'],
  'performance': ['load', 'charge', 'performance', 'Core Web Vitals', 'profiling'],
  'security': ['OWASP', 'securite', 'XSS', 'injection', 'CVE', 'vulnerabilite'],
  'accessibility': ['WCAG', 'accessibilite', 'a11y', 'axe-core', 'Pa11y', 'ARIA']
};

/**
 * Get total expected agent count
 * @returns {number} Total agents across all domains
 */
function getTotalExpectedAgents() {
  return Object.values(EXPECTED_AGENTS_PER_DOMAIN)
    .reduce((sum, agents) => sum + agents.length, 0);
}

module.exports = {
  SKILL_ROOT,
  DOMAINS,
  EXPECTED_AGENTS_PER_DOMAIN,
  AGENT_REQUIREMENTS,
  DOMAIN_KEYWORDS,
  getTotalExpectedAgents
};
