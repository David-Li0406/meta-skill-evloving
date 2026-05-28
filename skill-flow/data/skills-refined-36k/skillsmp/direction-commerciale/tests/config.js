/**
 * Centralized configuration for direction-commerciale skill tests
 *
 * ## Naming Conventions
 *
 * - Domains: lowercase-kebab-case (e.g., `pricing`, `rentabilite`)
 * - Agents: lowercase-kebab-case (e.g., `modeles-pricing`, `analyse-rentabilite`)
 *
 * These conventions are enforced by validation tests.
 *
 * @module tests/config
 */

const path = require('path');

/** @const {string} Base directory for the skill */
const SKILL_ROOT = path.join(__dirname, '..');

/** @const {string[]} Commercial domains */
const DOMAINS = [
  'strategie-commerciale',
  'pricing',
  'partenariats',
  'rentabilite',
  'relation-client'
];

/** @const {Object} Expected agents per domain */
const EXPECTED_AGENTS_PER_DOMAIN = {
  'strategie-commerciale': [
    'orchestrator',
    'vision-commerciale',
    'objectifs-ca',
    'segmentation-marche',
    'go-to-market',
    'veille-concurrentielle'
  ],
  'pricing': [
    'orchestrator',
    'modeles-pricing',
    'valorisation-services',
    'pricing-projets',
    'negociation-strategy'
  ],
  'partenariats': [
    'orchestrator',
    'strategie-partenariats',
    'evaluation-partenaires',
    'modeles-collaboration',
    'suivi-partenariats'
  ],
  'rentabilite': [
    'orchestrator',
    'analyse-rentabilite',
    'objectifs-marge',
    'arbitrage-investissement',
    'optimisation-couts',
    'forecast-financier'
  ],
  'relation-client': [
    'orchestrator',
    'strategie-comptes-cles',
    'satisfaction-strategique',
    'developpement-compte',
    'retention-strategique'
  ]
};

/**
 * Agent validation requirements
 * @const {Object}
 */
const AGENT_REQUIREMENTS = {
  /** Required frontmatter fields */
  frontmatter: ['name', 'description'],

  /** Minimum content length for orchestrators (characters) */
  minOrchestratorLength: 600,

  /** Minimum content length for specialized agents (characters) */
  minAgentLength: 400,

  /** Legacy threshold for backwards compatibility */
  minContentLength: 400,

  /** Expected sections for orchestrators */
  orchestratorSections: ['Agents Disponibles', 'Routage'],

  /** Expected sections for commercial agents */
  agentSections: ['Responsabilité', 'Inputs', 'Outputs']
};

/**
 * Domain keywords for routing validation
 * @const {Object}
 */
const DOMAIN_KEYWORDS = {
  'strategie-commerciale': ['vision commerciale', 'objectif CA', 'segment', 'go-to-market', 'concurrence'],
  'pricing': ['pricing', 'tarif', 'prix', 'grille', 'négociation', 'remise'],
  'partenariats': ['partenariat', 'partenaire', 'alliance', 'collaboration'],
  'rentabilite': ['rentabilité', 'marge', 'ROI', 'investissement', 'coût', 'forecast'],
  'relation-client': ['grand compte', 'compte clé', 'NPS', 'upsell', 'rétention', 'churn']
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
