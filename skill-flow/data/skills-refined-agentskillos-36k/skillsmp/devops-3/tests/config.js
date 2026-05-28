/**
 * Centralized configuration for DevOps skill tests
 *
 * ## Naming Conventions
 *
 * - Domains: lowercase-kebab-case (e.g., `cicd`, `kubernetes`)
 * - Agents: lowercase-kebab-case (e.g., `github-actions`, `docker-compose`)
 *
 * These conventions are enforced by validation tests.
 *
 * @module tests/config
 */

const path = require('path');

/** @const {string} Base directory for the skill */
const SKILL_ROOT = path.join(__dirname, '..');

/** @const {string[]} DevOps domains */
const DOMAINS = [
  'cicd',
  'containers',
  'kubernetes',
  'infrastructure',
  'monitoring',
  'deployment'
];

/** @const {Object} Expected agents per domain */
const EXPECTED_AGENTS_PER_DOMAIN = {
  'cicd': [
    'orchestrator',
    'github-actions',
    'gitlab-ci',
    'pipelines',
    'quality-gates',
    'artifacts'
  ],
  'containers': [
    'orchestrator',
    'docker',
    'docker-compose',
    'registries',
    'security'
  ],
  'kubernetes': [
    'orchestrator',
    'deployments',
    'services',
    'helm',
    'scaling',
    'config'
  ],
  'infrastructure': [
    'orchestrator',
    'terraform',
    'aws',
    'gcp',
    'networking'
  ],
  'monitoring': [
    'orchestrator',
    'prometheus',
    'grafana',
    'logging',
    'alerting'
  ],
  'deployment': [
    'orchestrator',
    'strategies',
    'rollback'
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
   * Lower threshold: focused content with code examples
   */
  minAgentLength: 400,

  /** Legacy threshold for backwards compatibility */
  minContentLength: 400,

  /** Expected sections for orchestrators */
  orchestratorSections: ['Agents', 'Routage'],

  /** Expected sections for technical agents */
  agentSections: ['Responsabilités']
};

/**
 * Domain keywords for routing validation
 *
 * @const {Object}
 */
const DOMAIN_KEYWORDS = {
  'cicd': ['CI/CD', 'pipeline', 'GitHub Actions', 'GitLab CI', 'workflow'],
  'containers': ['Docker', 'container', 'image', 'Dockerfile', 'registry'],
  'kubernetes': ['Kubernetes', 'K8s', 'pod', 'deployment', 'Helm', 'kubectl'],
  'infrastructure': ['Terraform', 'AWS', 'GCP', 'VPC', 'IaC'],
  'monitoring': ['Prometheus', 'Grafana', 'logs', 'alerting', 'metrics'],
  'deployment': ['Blue-Green', 'Canary', 'rollback', 'release']
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
