/**
 * Centralized configuration for lead-dev skill tests
 * @module tests/config
 */

const path = require('path');

/** @const {string} Base directory for the skill */
const SKILL_ROOT = path.join(__dirname, '..');

/** @const {string[]} Lead Dev domains */
const DOMAINS = [
  'code-review',
  'team-coordination',
  'technical-decisions',
  'mentoring',
  'delivery'
];

/** @const {Object} Expected agents per domain */
const EXPECTED_AGENTS_PER_DOMAIN = {
  'code-review': [
    'orchestrator',
    'pr-review',
    'architecture-check',
    'quality-gate',
    'security-review',
    'performance-review'
  ],
  'team-coordination': [
    'orchestrator',
    'task-delegation',
    'standup-prep',
    'blocker-resolution',
    'sprint-support'
  ],
  'technical-decisions': [
    'orchestrator',
    'library-selection',
    'pattern-choice',
    'refactoring-plan',
    'tech-debt-prioritization'
  ],
  'mentoring': [
    'orchestrator',
    'code-feedback',
    'best-practices',
    'onboarding-dev',
    'skill-assessment'
  ],
  'delivery': [
    'orchestrator',
    'release-planning',
    'merge-strategy',
    'deployment-check',
    'hotfix-coordination',
    'release-notes'
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
  minOrchestratorLength: 800,

  /** Minimum content length for specialized agents (characters) */
  minAgentLength: 500,

  /** Expected sections for orchestrators */
  orchestratorSections: ['Arbre de Décision'],

  /** Expected sections for agents */
  agentSections: ['Ta Responsabilité Unique', 'Tu NE fais PAS']
};

/**
 * Domain keywords for routing validation
 * @const {Object}
 */
const DOMAIN_KEYWORDS = {
  'code-review': ['PR', 'pull request', 'review', 'qualité code', 'sécurité code'],
  'team-coordination': ['tâche', 'daily', 'standup', 'blocage', 'sprint'],
  'technical-decisions': ['librairie', 'pattern', 'refactoring', 'dette technique'],
  'mentoring': ['feedback', 'onboarding', 'formation', 'progression'],
  'delivery': ['release', 'deploy', 'hotfix', 'merge', 'changelog']
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
