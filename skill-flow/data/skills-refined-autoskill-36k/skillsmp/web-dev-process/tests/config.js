/**
 * Centralized configuration for web-dev-process skill tests
 * @module tests/config
 */

const path = require('path');

/** @const {string} Base directory for the web-dev-process skill */
const SKILL_ROOT = path.join(__dirname, '..');

/** @const {string} Directory containing all agents */
const AGENTS_DIR = path.join(SKILL_ROOT, 'agents');

/** @const {string} Directory containing configs */
const CONFIGS_DIR = path.join(SKILL_ROOT, 'configs');

/** @const {string} Directory containing guides */
const GUIDES_DIR = path.join(SKILL_ROOT, 'guides');

/** @const {string} Directory containing templates */
const TEMPLATES_DIR = path.join(SKILL_ROOT, 'templates');

/** @const {string[]} The 7 development phases */
const PHASES = [
  'discovery',
  'design',
  'setup',
  'development',
  'testing',
  'deployment',
  'maintenance'
];

/** @const {Object} Expected agents per phase */
const EXPECTED_AGENTS_PER_PHASE = {
  'discovery': ['orchestrator', 'requirements', 'user-stories', 'scope-definition'],
  'design': ['orchestrator', 'architecture', 'data-modeling', 'api-design', 'ui-ux',
             'ux-principles', 'responsive-design', 'design-system', 'accessibility'],
  'setup': ['orchestrator', 'repository', 'git-config', 'branching-strategies',
            'branch-protection', 'pr-templates', 'environment', 'env-variables',
            'docker', 'secrets-management', 'cicd', 'ci-principles', 'cd-principles',
            'deployment-strategies', 'quality-tools', 'linting', 'formatting',
            'git-hooks', 'commit-conventions'],
  'development': ['orchestrator', 'coding-standards', 'code-review', 'git-workflow',
                  'documentation', 'readme', 'adr', 'runbooks'],
  'testing': ['orchestrator', 'unit-tests', 'integration-tests', 'e2e-tests',
              'performance', 'accessibility', 'security', 'dependency-audit',
              'security-headers'],
  'deployment': ['orchestrator', 'staging', 'production', 'rollback'],
  'maintenance': ['orchestrator', 'monitoring', 'metrics', 'logging', 'alerting',
                  'bug-tracking', 'updates']
};

/**
 * Agent validation requirements
 * @const {Object}
 */
const AGENT_REQUIREMENTS = {
  /** Required frontmatter fields */
  frontmatter: ['name', 'description'],

  /** Common sections for specialized agents */
  commonSections: [
    'Contexte',
    'Principes'
  ],

  /** Required sections for orchestrators */
  orchestratorSections: [
    'Agent',
    'Responsabilité'
  ],

  /** Minimum content length (characters) */
  minContentLength: 200
};

/**
 * Phase descriptions for validation
 * @const {Object}
 */
const PHASE_DESCRIPTIONS = {
  'discovery': 'Comprendre le besoin avant de coder',
  'design': 'Concevoir avant d\'implémenter',
  'setup': 'Préparer l\'environnement de travail',
  'development': 'Écrire du code maintenable',
  'testing': 'Valider la qualité',
  'deployment': 'Livrer en production',
  'maintenance': 'Maintenir et améliorer'
};

/**
 * Keywords for routing validation per phase
 * @const {Object}
 */
const PHASE_KEYWORDS = {
  'discovery': ['besoin', 'exigence', 'requirement', 'user story', 'scope', 'périmètre'],
  'design': ['architecture', 'schéma', 'modèle', 'API', 'UI', 'UX'],
  'setup': ['git', 'repo', 'branch', 'environnement', 'CI/CD', 'linter'],
  'development': ['code', 'convention', 'review', 'PR', 'commit', 'documentation'],
  'testing': ['test', 'unit', 'intégration', 'e2e', 'performance', 'sécurité'],
  'deployment': ['deploy', 'staging', 'production', 'release', 'rollback'],
  'maintenance': ['monitoring', 'log', 'alerte', 'bug', 'update']
};

/** @const {number} Number of development phases */
const PHASE_COUNT = PHASES.length;

module.exports = {
  SKILL_ROOT,
  AGENTS_DIR,
  CONFIGS_DIR,
  GUIDES_DIR,
  TEMPLATES_DIR,
  PHASES,
  PHASE_COUNT,
  EXPECTED_AGENTS_PER_PHASE,
  AGENT_REQUIREMENTS,
  PHASE_DESCRIPTIONS,
  PHASE_KEYWORDS
};
