/**
 * Centralized configuration for Legacy Modernization skill tests
 *
 * @module tests/config
 */

const path = require('path');

const SKILL_ROOT = path.join(__dirname, '..');

const DOMAINS = [
  'assessment',
  'strategies',
  'migration',
  'refactoring',
  'testing'
];

const EXPECTED_AGENTS_PER_DOMAIN = {
  'assessment': [
    'orchestrator',
    'audit'
  ],
  'strategies': [
    'orchestrator',
    'strangler'
  ],
  'migration': [
    'orchestrator',
    'data'
  ],
  'refactoring': [
    'orchestrator',
    'incremental'
  ],
  'testing': [
    'orchestrator',
    'characterization'
  ]
};

const AGENT_REQUIREMENTS = {
  frontmatter: ['name', 'description'],
  minOrchestratorLength: 500,
  minAgentLength: 400,
  minContentLength: 400
};

const DOMAIN_KEYWORDS = {
  'assessment': ['audit', 'debt', 'risk', 'evaluation', 'dependencies'],
  'strategies': ['strangler', 'bubble', 'abstraction', 'feature flag', 'parallel'],
  'migration': ['ETL', 'data', 'CDC', 'sync', 'rollback', 'Debezium'],
  'refactoring': ['incremental', 'extract', 'seams', 'contracts'],
  'testing': ['characterization', 'golden master', 'approval', 'regression']
};

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
