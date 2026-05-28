/**
 * Centralized configuration for frontend-developer skill tests
 *
 * @module tests/config
 */

const path = require('path');

/** @const {string} Base directory for the skill */
const SKILL_ROOT = path.join(__dirname, '..');

/** @const {string[]} Frontend domains */
const DOMAINS = [
  'foundations',
  'javascript',
  'frameworks',
  'styling',
  'state-management',
  'testing',
  'performance',
  'tooling'
];

/** @const {Object} Expected agents per domain */
const EXPECTED_AGENTS_PER_DOMAIN = {
  'foundations': [
    'orchestrator',
    'html-semantique',
    'css-moderne',
    'accessibilite',
    'responsive-design'
  ],
  'javascript': [
    'orchestrator',
    'javascript-moderne',
    'typescript',
    'dom-manipulation',
    'api-integration'
  ],
  'frameworks': [
    'orchestrator',
    'react-expert',
    'vue-expert',
    'nextjs-expert',
    'wordpress-expert',
    'component-patterns'
  ],
  'styling': [
    'orchestrator',
    'tailwind-expert',
    'css-in-js',
    'animations'
  ],
  'state-management': [
    'orchestrator',
    'react-state',
    'server-state'
  ],
  'testing': [
    'orchestrator',
    'unit-testing',
    'component-testing',
    'e2e-testing'
  ],
  'performance': [
    'orchestrator',
    'core-web-vitals',
    'bundle-optimization'
  ],
  'tooling': [
    'orchestrator',
    'build-tools',
    'linting-formatting'
  ]
};

/**
 * Agent validation requirements
 * @const {Object}
 */
const AGENT_REQUIREMENTS = {
  frontmatter: ['name', 'description'],
  minOrchestratorLength: 500,
  minAgentLength: 300,
  minContentLength: 300,
  orchestratorSections: ['Règles de Routage'],
  agentSections: ['Rôle']
};

/**
 * Domain keywords for routing validation
 * @const {Object}
 */
const DOMAIN_KEYWORDS = {
  'foundations': ['html', 'css', 'accessibilité', 'a11y', 'responsive', 'sémantique'],
  'javascript': ['javascript', 'typescript', 'ES6', 'DOM', 'API', 'fetch', 'async'],
  'frameworks': ['react', 'vue', 'next', 'nuxt', 'wordpress', 'gutenberg', 'composant', 'component'],
  'styling': ['tailwind', 'styled', 'emotion', 'animation', 'CSS-in-JS'],
  'state-management': ['state', 'context', 'zustand', 'redux', 'react-query'],
  'testing': ['test', 'vitest', 'jest', 'playwright', 'cypress', 'RTL'],
  'performance': ['performance', 'Core Web Vitals', 'LCP', 'bundle', 'lighthouse'],
  'tooling': ['vite', 'webpack', 'eslint', 'prettier', 'build']
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
