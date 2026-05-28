/**
 * Configuration for direction-artistique skill tests
 * @module tests/config
 */

const path = require('path');

const SKILL_ROOT = path.join(__dirname, '..');

const DOMAINS = [
  'branding',
  'ux-strategy',
  'design-strategy',
  'guidelines',
  'orchestration'
];

const EXPECTED_AGENTS_PER_DOMAIN = {
  'branding': [
    'orchestrator',
    'brand-identity',
    'visual-language',
    'tone-of-voice',
    'brand-audit',
    'brand-guidelines'
  ],
  'ux-strategy': [
    'orchestrator',
    'ux-research-strategy',
    'user-journey-strategy',
    'ux-principles',
    'accessibility-strategy'
  ],
  'design-strategy': [
    'orchestrator',
    'design-vision',
    'design-principles',
    'design-system-strategy',
    'innovation-design'
  ],
  'guidelines': [
    'orchestrator',
    'style-guide',
    'component-standards',
    'documentation-design',
    'quality-criteria'
  ],
  'orchestration': [
    'orchestrator',
    'brief-creatif',
    'delegation-design',
    'validation-creative'
  ]
};

const TOTAL_EXPECTED_AGENTS = 25;

const ROUTING_KEYWORDS = [
  'direction artistique',
  'DA',
  'identité visuelle',
  'branding',
  'UX strategy',
  'design vision',
  'guidelines',
  'charte graphique'
];

module.exports = {
  SKILL_ROOT,
  DOMAINS,
  EXPECTED_AGENTS_PER_DOMAIN,
  TOTAL_EXPECTED_AGENTS,
  ROUTING_KEYWORDS
};
