/**
 * Centralized configuration for wordpress-gutenberg-expert skill tests
 * @module tests/config
 */

const path = require('path');

/** @const {string} Base directory for the skill */
const SKILL_ROOT = path.join(__dirname, '..');

/** @const {string} Directory containing all agents */
const AGENTS_DIR = path.join(SKILL_ROOT, 'agents');

/** @const {string} Directory containing docs */
const DOCS_DIR = path.join(SKILL_ROOT, 'docs');

/** @const {string} Directory containing references */
const REFERENCES_DIR = path.join(SKILL_ROOT, 'references');

/** @const {string[]} WordPress domains */
const DOMAINS = [
  'wp-core',
  'gutenberg-blocks',
  'theme',
  'tooling',
  'testing',
  'design'
];

/** @const {string[]} Standalone expert agents */
const STANDALONE_AGENTS = [
  'wp-rest-api-expert',
  'gdpr-consent-api',
  'i18n-localization',
  'seo-expert',
  'accessibility-expert'
];

/** @const {Object} Expected agents per domain */
const EXPECTED_AGENTS_PER_DOMAIN = {
  'wp-core': ['orchestrator', 'custom-post-types', 'custom-taxonomies',
              'custom-roles', 'custom-meta', 'hooks-filters', 'security-validation'],
  'gutenberg-blocks': ['orchestrator', 'custom-blocks', 'block-variations',
                       'block-styles', 'data-stores'],
  'theme': ['orchestrator', 'block-theme', 'templates-patterns',
            'style-engine', 'interactivity-api'],
  'tooling': ['orchestrator', 'wp-cli-commands', 'project-init',
              'environment-config', 'local-dev', 'staging-setup',
              'build-tooling', 'repository-setup', 'cicd-pipelines',
              'gitlab-ci', 'deployment-ssh', 'issue-management', 'quality-check'],
  'testing': ['orchestrator', 'php-unit-tests', 'js-unit-tests', 'e2e-tests'],
  'design': ['orchestrator', 'design-tokens', 'visual-review']
};

/**
 * Agent validation requirements
 * @const {Object}
 */
const AGENT_REQUIREMENTS = {
  /** Required frontmatter fields */
  frontmatter: ['name', 'description'],

  /** Minimum content length (characters) */
  minContentLength: 300,

  /** Expected sections for WP agents */
  expectedSections: ['Sources', 'Contexte']
};

/**
 * WordPress-specific keywords for routing validation
 * @const {Object}
 */
const DOMAIN_KEYWORDS = {
  'wp-core': ['CPT', 'taxonomy', 'role', 'meta', 'hook', 'action', 'filter', 'nonce'],
  'gutenberg-blocks': ['block', 'variation', 'style', 'registerBlockType', 'useSelect'],
  'theme': ['theme.json', 'block theme', 'template', 'pattern', 'FSE'],
  'tooling': ['WP-CLI', 'wp-env', 'docker', 'CI/CD', 'deploy'],
  'testing': ['PHPUnit', 'Jest', 'Playwright', 'e2e'],
  'design': ['token', 'Figma', 'maquette', 'design system']
};

module.exports = {
  SKILL_ROOT,
  AGENTS_DIR,
  DOCS_DIR,
  REFERENCES_DIR,
  DOMAINS,
  STANDALONE_AGENTS,
  EXPECTED_AGENTS_PER_DOMAIN,
  AGENT_REQUIREMENTS,
  DOMAIN_KEYWORDS
};
