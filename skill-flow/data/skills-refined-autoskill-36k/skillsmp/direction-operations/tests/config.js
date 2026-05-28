/**
 * Centralized configuration for direction-operations skill tests
 *
 * ## Naming Conventions
 *
 * - Domains: lowercase-kebab-case (e.g., `gouvernance`, `ressources`)
 * - Agents: lowercase-kebab-case (e.g., `vision-projet`, `allocation-strategique`)
 *
 * These conventions are enforced by validation tests.
 *
 * @module tests/config
 */

const path = require('path');

/** @const {string} Base directory for the skill */
const SKILL_ROOT = path.join(__dirname, '..');

/** @const {string[]} Operations domains */
const DOMAINS = [
  'gouvernance',
  'ressources',
  'pilotage',
  'qualite-delivery',
  'coordination'
];

/** @const {Object} Expected agents per domain */
const EXPECTED_AGENTS_PER_DOMAIN = {
  'gouvernance': [
    'orchestrator',
    'vision-projet',
    'comitologie',
    'regles-jeu',
    'escalade-strategique'
  ],
  'ressources': [
    'orchestrator',
    'capacite-equipe',
    'allocation-strategique',
    'competences',
    'staffing',
    'budget-ressources'
  ],
  'pilotage': [
    'orchestrator',
    'priorisation',
    'risques-portefeuille',
    'roadmap-strategique',
    'reporting-direction'
  ],
  'qualite-delivery': [
    'orchestrator',
    'standards-qualite',
    'sla-definition',
    'amelioration-continue',
    'metriques-operations',
    'audit-processus'
  ],
  'coordination': [
    'orchestrator',
    'synchro-equipes',
    'gestion-dependances',
    'communication-interne',
    'knowledge-management'
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

  /** Expected sections for operational agents */
  agentSections: ['Responsabilité', 'Inputs', 'Outputs']
};

/**
 * Domain keywords for routing validation
 * @const {Object}
 */
const DOMAIN_KEYWORDS = {
  'gouvernance': ['vision', 'objectif', 'OKR', 'comité', 'RACI', 'charte', 'escalade'],
  'ressources': ['capacité', 'charge', 'allocation', 'compétence', 'staffing', 'budget RH'],
  'pilotage': ['priorité', 'arbitrage', 'risque', 'roadmap', 'reporting', 'portefeuille'],
  'qualite-delivery': ['standard', 'qualité', 'SLA', 'amélioration', 'KPI', 'audit'],
  'coordination': ['synchro', 'dépendance', 'communication', 'knowledge', 'wiki']
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
