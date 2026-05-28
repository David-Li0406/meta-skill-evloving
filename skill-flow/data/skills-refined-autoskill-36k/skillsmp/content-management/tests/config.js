/**
 * Centralized configuration for content-management skill tests
 * @module tests/config
 */

const path = require('path');

/** @const {string} Base directory for the content-management skill */
const SKILL_ROOT = path.join(__dirname, '..');

/** @const {string} Directory containing agents */
const AGENTS_DIR = path.join(SKILL_ROOT, 'agents');

/** @const {string} Directory containing workflows */
const WORKFLOWS_DIR = path.join(SKILL_ROOT, 'workflows');

/** @const {string[]} Expected domains in content-management */
const EXPECTED_DOMAINS = [
  'editorial',
  'redaction',
  'assets',
  'localization'
];

/** @const {Object.<string, string[]>} Expected agents per domain */
const EXPECTED_AGENTS = {
  'editorial': [
    'orchestrator',
    'calendar-manager',
    'workflow-controller',
    'publication-scheduler'
  ],
  'redaction': [
    'orchestrator',
    'article-writer',
    'page-builder',
    'copywriter',
    'seo-optimizer'
  ],
  'assets': [
    'orchestrator',
    'media-manager',
    'image-optimizer',
    'video-handler'
  ],
  'localization': [
    'orchestrator',
    'translation-manager',
    'locale-adapter',
    'i18n-validator'
  ]
};

/** @const {string[]} Expected workflows */
const EXPECTED_WORKFLOWS = [
  'brief-to-article',
  'content-to-multilang',
  'media-to-cdn',
  'request-to-brief'
];

/**
 * Agent validation requirements
 * @const {Object}
 */
const AGENT_REQUIREMENTS = {
  /** Required frontmatter fields */
  frontmatter: ['name', 'description', 'version'],

  /** Required markdown sections for SRP agents */
  requiredSections: [
    'Ta Responsabilité Unique'
  ],

  /** Required sections for orchestrators */
  orchestratorSections: [
    'Workflow',
    'Agents'
  ],

  /** Minimum content length (characters) */
  minContentLength: 200
};

/**
 * Expected routing rules per domain orchestrator
 * @const {Object.<string, Object[]>}
 */
const EXPECTED_ROUTING = {
  'editorial': [
    { intent: 'calendrier', agent: 'calendar-manager' },
    { intent: 'workflow', agent: 'workflow-controller' },
    { intent: 'publication', agent: 'publication-scheduler' }
  ],
  'redaction': [
    { intent: 'article', agent: 'article-writer' },
    { intent: 'page', agent: 'page-builder' },
    { intent: 'copy', agent: 'copywriter' },
    { intent: 'seo', agent: 'seo-optimizer' }
  ],
  'assets': [
    { intent: 'média', agent: 'media-manager' },
    { intent: 'image', agent: 'image-optimizer' },
    { intent: 'vidéo', agent: 'video-handler' }
  ],
  'localization': [
    { intent: 'traduction', agent: 'translation-manager' },
    { intent: 'locale', agent: 'locale-adapter' },
    { intent: 'i18n', agent: 'i18n-validator' }
  ]
};

/**
 * Cross-references to other skills
 * @const {Object.<string, string[]>}
 */
const EXPECTED_CROSSREFS = {
  'marketing': [
    'seo-expert/strategie',
    'content-marketing/social-strategy',
    'direction-marketing/strategie'
  ]
};

module.exports = {
  SKILL_ROOT,
  AGENTS_DIR,
  WORKFLOWS_DIR,
  EXPECTED_DOMAINS,
  EXPECTED_AGENTS,
  EXPECTED_WORKFLOWS,
  AGENT_REQUIREMENTS,
  EXPECTED_ROUTING,
  EXPECTED_CROSSREFS
};
