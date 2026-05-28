/**
 * Centralized configuration for UX/UI Design skill tests
 *
 * ## Naming Conventions
 *
 * - Domains: lowercase-kebab-case (e.g., `research`, `branding`)
 * - Agents: lowercase-kebab-case (e.g., `persona-builder`, `motion-design`)
 *
 * These conventions are enforced by validation tests.
 *
 * @module tests/config
 */

const path = require('path');

/** @const {string} Base directory for the skill */
const SKILL_ROOT = path.join(__dirname, '..');

/** @const {string[]} UX/UI domains */
const DOMAINS = [
  'research',
  'wireframe',
  'visual',
  'prototype',
  'testing',
  'branding'
];

/** @const {Object} Expected agents per domain */
const EXPECTED_AGENTS_PER_DOMAIN = {
  'research': [
    'orchestrator',
    'persona-builder',
    'journey-mapper',
    'interview-guide',
    'competitor-analyzer'
  ],
  'wireframe': [
    'orchestrator',
    'sitemap-designer',
    'zoning-creator',
    'wireframe-generator'
  ],
  'visual': [
    'orchestrator',
    'ui-designer',
    'mockup-creator',
    'style-guide-creator',
    'asset-exporter'
  ],
  'prototype': [
    'orchestrator',
    'prototype-builder',
    'interaction-designer',
    'animation-designer'
  ],
  'testing': [
    'orchestrator',
    'usability-tester',
    'ab-tester',
    'feedback-analyzer'
  ],
  'branding': [
    'orchestrator',
    'direction-artistique',
    'brand-identity',
    'motion-design',
    'assets-creator'
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
   * Note: UX/UI orchestrators are more concise than technical ones
   */
  minOrchestratorLength: 700,

  /**
   * Minimum content length for specialized agents (characters)
   */
  minAgentLength: 500,

  /** Legacy threshold for backwards compatibility */
  minContentLength: 500,

  /** Expected sections for orchestrators */
  orchestratorSections: ['Règles de Routage', 'Arbre de Décision'],

  /** Expected sections for UX/UI agents */
  agentSections: ['Mission', 'Points d\'Escalade']
};

/**
 * Domain keywords for routing validation
 *
 * @const {Object}
 */
const DOMAIN_KEYWORDS = {
  'research': ['persona', 'interview', 'parcours', 'comportement', 'user research', 'analyse'],
  'wireframe': ['wireframe', 'zoning', 'arborescence', 'sitemap', 'architecture information'],
  'visual': ['maquette', 'UI', 'couleur', 'typographie', 'style guide', 'design visuel'],
  'prototype': ['prototype', 'interaction', 'animation', 'micro-interaction', 'cliquable'],
  'testing': ['test utilisateur', 'A/B', 'heatmap', 'feedback', 'usability'],
  'branding': ['direction artistique', 'identité visuelle', 'logo', 'charte graphique', 'motion design', 'moodboard']
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
