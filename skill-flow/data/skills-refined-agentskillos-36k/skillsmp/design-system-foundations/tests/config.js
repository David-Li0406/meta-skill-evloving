/**
 * Centralized configuration for design-system-foundations skill tests
 * @module tests/config
 */

const path = require('path');

/** @const {string} Base directory for the design-system-foundations skill */
const SKILL_ROOT = path.join(__dirname, '..');

/** @const {string} Directory containing all agents */
const AGENTS_DIR = path.join(SKILL_ROOT, 'agents');

/** @const {string} Directory containing documentation */
const DOCS_DIR = path.join(SKILL_ROOT, 'docs');

/** @const {string} Directory containing references */
const REFERENCES_DIR = path.join(SKILL_ROOT, 'references');

/** @const {string[]} The 4 Atomic Design levels */
const LEVELS = [
  'foundations',
  'atoms',
  'molecules',
  'templates'
];

/** @const {Object} Expected agents per Atomic Design level */
const EXPECTED_AGENTS_PER_LEVEL = {
  'foundations': ['orchestrator', 'colors', 'typography', 'spacing', 'shadows'],
  'atoms': ['orchestrator', 'buttons', 'inputs', 'labels', 'icons', 'badges'],
  'molecules': ['orchestrator', 'forms', 'cards', 'navigation', 'modals', 'alerts'],
  'templates': ['orchestrator', 'hero-sections', 'layouts', 'pages']
};

/** @const {string[]} Expected documentation files */
const EXPECTED_DOCS = [
  'getting-started.md',
  'naming-conventions.md',
  'animation-performance.md',
  'testing-guide.md',
  'dark-mode.md',
  'bundle-optimization.md',
  'accessibility-checklist.md'
];

/**
 * Agent validation requirements
 * @const {Object}
 */
const AGENT_REQUIREMENTS = {
  /** Required frontmatter fields */
  frontmatter: ['name', 'description'],

  /** Common sections for foundation agents */
  foundationSections: [
    'CSS Custom Properties',
    'Tokens'
  ],

  /** Common sections for component agents (atoms, molecules) */
  componentSections: [
    'CSS',
    'Variants'
  ],

  /** Required sections for orchestrators */
  orchestratorSections: [
    'Agent',
    'Routing'
  ],

  /** Minimum content length (characters) */
  minContentLength: 500
};

/**
 * CSS token patterns to validate
 * @const {Object}
 */
const TOKEN_PATTERNS = {
  colors: /--color-[a-z]+-[0-9]+/,
  spacing: /--space-[0-9]+/,
  typography: /--font-(size|weight|family|leading)/,
  shadows: /--shadow-(sm|md|lg|xl)/,
  radius: /--radius-(sm|md|lg|xl|full)/
};

/**
 * Level descriptions for validation
 * @const {Object}
 */
const LEVEL_DESCRIPTIONS = {
  'foundations': 'Design tokens: colors, typography, spacing, shadows',
  'atoms': 'Smallest UI elements: buttons, inputs, labels, icons, badges',
  'molecules': 'Composed components: forms, cards, navigation, modals, alerts',
  'templates': 'Page structures: hero sections, layouts, pages'
};

/**
 * Keywords for routing validation per level
 * @const {Object}
 */
const LEVEL_KEYWORDS = {
  'foundations': ['color', 'palette', 'font', 'typography', 'spacing', 'shadow', 'elevation', 'token'],
  'atoms': ['button', 'input', 'label', 'icon', 'badge', 'tag', 'chip'],
  'molecules': ['form', 'card', 'nav', 'modal', 'dialog', 'alert', 'toast'],
  'templates': ['hero', 'layout', 'page', 'section', 'dashboard', 'landing']
};

/** @const {number} Number of Atomic Design levels */
const LEVEL_COUNT = LEVELS.length;

/**
 * @const {number} Total number of agents across all levels (computed)
 * Includes 4 orchestrators (one per level) + 17 specialized agents = 21 total
 */
const TOTAL_AGENT_COUNT = Object.values(EXPECTED_AGENTS_PER_LEVEL)
  .reduce((sum, agents) => sum + agents.length, 0);

module.exports = {
  SKILL_ROOT,
  AGENTS_DIR,
  DOCS_DIR,
  REFERENCES_DIR,
  LEVELS,
  LEVEL_COUNT,
  TOTAL_AGENT_COUNT,
  EXPECTED_AGENTS_PER_LEVEL,
  EXPECTED_DOCS,
  AGENT_REQUIREMENTS,
  TOKEN_PATTERNS,
  LEVEL_DESCRIPTIONS,
  LEVEL_KEYWORDS
};
