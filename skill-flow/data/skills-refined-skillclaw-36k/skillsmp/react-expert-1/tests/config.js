/**
 * Centralized configuration for react-expert skill tests
 *
 * @module tests/config
 */

const path = require('path');

/** @const {string} Base directory for the skill */
const SKILL_ROOT = path.join(__dirname, '..');

/** @const {string[]} React domains */
const DOMAINS = [
  'hooks',
  'components',
  'state',
  'data',
  'testing',
  'styling',
  'performance'
];

/** @const {Object} Expected agents per domain */
const EXPECTED_AGENTS_PER_DOMAIN = {
  'hooks': [
    'orchestrator',
    'state-hooks',
    'effect-hooks',
    'ref-hooks',
    'custom-hooks'
  ],
  'components': [
    'orchestrator',
    'functional',
    'composition',
    'forms',
    'error-boundaries'
  ],
  'state': [
    'orchestrator',
    'context',
    'zustand',
    'redux-toolkit'
  ],
  'data': [
    'orchestrator',
    'react-query',
    'swr',
    'suspense'
  ],
  'testing': [
    'orchestrator',
    'rtl',
    'hooks-testing',
    'mocking'
  ],
  'styling': [
    'orchestrator',
    'tailwind-react',
    'css-in-js'
  ],
  'performance': [
    'orchestrator',
    'memoization',
    'code-splitting'
  ]
};

/**
 * Agent validation requirements
 * @const {Object}
 */
const AGENT_REQUIREMENTS = {
  frontmatter: ['name', 'description'],
  minOrchestratorLength: 400,
  minAgentLength: 500,
  minContentLength: 500,
  orchestratorSections: ['Règles de Routage', 'Agents Disponibles'],
  agentSections: ['Rôle']
};

/**
 * Domain keywords for routing validation
 * @const {Object}
 */
const DOMAIN_KEYWORDS = {
  'hooks': ['useState', 'useEffect', 'useRef', 'useReducer', 'useCallback', 'useMemo', 'custom hook'],
  'components': ['composant', 'props', 'children', 'compound', 'render props', 'HOC', 'form'],
  'state': ['context', 'provider', 'zustand', 'redux', 'store', 'slice'],
  'data': ['react-query', 'useQuery', 'useMutation', 'swr', 'suspense', 'fetch'],
  'testing': ['test', 'render', 'screen', 'userEvent', 'mock', 'RTL', 'vitest'],
  'styling': ['tailwind', 'styled', 'emotion', 'CSS-in-JS', 'cn', 'cva'],
  'performance': ['memo', 'useMemo', 'useCallback', 'lazy', 'code splitting']
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
