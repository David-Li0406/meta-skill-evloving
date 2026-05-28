/**
 * Centralized configuration for technical skill tests
 *
 * ## Naming Conventions
 *
 * - Domains: lowercase-kebab-case (e.g., `avant-projet`, `qualite`)
 * - Agents: lowercase-kebab-case (e.g., `audit-existant`, `code-review`)
 * - Numbers allowed in agent names (e.g., `adr-001` if needed)
 *
 * These conventions are enforced by validation tests.
 *
 * @module tests/config
 */

const path = require('path');

/** @const {string} Base directory for the skill */
const SKILL_ROOT = path.join(__dirname, '..');

/** @const {string[]} Technical domains */
const DOMAINS = [
  'avant-projet',
  'specification',
  'architecture',
  'estimation',
  'qualite',
  'securite',
  'performance',
  'infrastructure',
  'communication',
  'support',
  'strategy'
];

/** @const {Object} Expected agents per domain */
const EXPECTED_AGENTS_PER_DOMAIN = {
  'avant-projet': [
    'orchestrator',
    'selection-stack',
    'audit-existant',
    'etude-faisabilite',
    'poc-spike'
  ],
  'specification': [
    'orchestrator',
    'cadrage-technique',
    'specification-technique',
    'modelisation-donnees',
    'specification-api'
  ],
  'architecture': [
    'orchestrator',
    'architecture-systeme',
    'architecture-applicative',
    'patterns-design',
    'review-architecture',
    'adr'
  ],
  'estimation': [
    'orchestrator',
    'estimation-macro',
    'estimation-detaillee',
    'decoupe-taches',
    'analyse-risques'
  ],
  'qualite': [
    'orchestrator',
    'conventions-code',
    'code-review',
    'metriques-qualite',
    'dette-technique',
    'definition-of-done'
  ],
  'securite': [
    'orchestrator',
    'audit-securite',
    'securite-applicative',
    'gestion-secrets',
    'conformite-rgpd'
  ],
  'performance': [
    'orchestrator',
    'audit-performance',
    'optimisation-frontend',
    'optimisation-backend',
    'monitoring-perf'
  ],
  'infrastructure': [
    'orchestrator',
    'architecture-infra',
    'strategie-cicd',
    'environnements',
    'strategie-deploiement'
  ],
  'communication': [
    'orchestrator',
    'handoff-developpeur',
    'documentation-technique',
    'onboarding-technique',
    'reporting-technique'
  ],
  'support': [
    'orchestrator',
    'troubleshooting',
    'gestion-incidents',
    'post-mortem',
    'veille-technologique'
  ],
  'strategy': [
    'orchestrator',
    'benchmark-concurrentiel',
    'strategie-digitale',
    'recommandations',
    'kpis-business'
  ]
};

/**
 * Agent validation requirements
 *
 * ## Content Length Thresholds
 * These thresholds ensure meaningful content:
 * - 500 chars ≈ ~100 words (minimum for a useful agent with examples)
 * - 800 chars ≈ ~150 words (orchestrators need routing tables + decision trees)
 *
 * If agents regularly fail these checks, consider:
 * 1. Adding more examples or code blocks
 * 2. Expanding decision criteria
 * 3. OR adjusting thresholds if content is intentionally concise
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
  minOrchestratorLength: 800,

  /**
   * Minimum content length for specialized agents (characters)
   * Lower threshold: focused content with code examples
   */
  minAgentLength: 500,

  /** Legacy threshold for backwards compatibility */
  minContentLength: 500,

  /** Expected sections for orchestrators */
  orchestratorSections: ['Règles de Routage', 'Arbre de Décision'],

  /** Expected sections for technical agents */
  agentSections: ['Mission', 'Points d\'Escalade']
};

/**
 * Domain keywords for routing validation
 *
 * NOTE: Case Handling
 * - Keywords are normalized to lowercase during matching
 * - Both "POC" and "poc" will match the same keyword
 * - SKILL.md and orchestrator content is also lowercased for comparison
 * - This ensures case-insensitive routing in production
 *
 * @const {Object}
 */
const DOMAIN_KEYWORDS = {
  'avant-projet': ['stack', 'framework', 'POC', 'spike', 'audit', 'faisabilité'],
  'specification': ['spec', 'API', 'modèle', 'données', 'schéma'],
  'architecture': ['architecture', 'pattern', 'ADR', 'design'],
  'estimation': ['estimation', 'chiffrage', 'risque', 'tâche'],
  'qualite': ['qualité', 'review', 'test', 'dette', 'DoD', 'convention'],
  'securite': ['sécurité', 'OWASP', 'RGPD', 'secret', 'audit'],
  'performance': ['performance', 'latence', 'Core Web Vitals', 'monitoring'],
  'infrastructure': ['CI/CD', 'pipeline', 'déploiement', 'Kubernetes', 'Terraform'],
  'communication': ['handoff', 'documentation', 'onboarding', 'reporting'],
  'support': ['incident', 'post-mortem', 'troubleshooting', 'veille'],
  'strategy': ['benchmark', 'stratégie digitale', 'KPIs', 'roadmap', 'recommandation', 'concurrentiel']
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
