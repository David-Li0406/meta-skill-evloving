/**
 * Configuration for marketing-ops skill tests
 * @module tests/config
 */

const path = require('path');

const SKILL_ROOT = path.join(__dirname, '..');

const DOMAINS = [
  'campagnes',
  'automation',
  'performance',
  'acquisition'
];

const EXPECTED_AGENTS_PER_DOMAIN = {
  'campagnes': [
    'orchestrator',
    'planning-campagne',
    'coordination-canaux',
    'budget-allocation',
    'suivi-performance'
  ],
  'automation': [
    'orchestrator',
    'workflow-builder',
    'triggers-actions',
    'lead-scoring',
    'multi-touch-sequences'
  ],
  'performance': [
    'orchestrator',
    'funnel-optimization',
    'conversion-optimization',
    'experimentation',
    'personalization'
  ],
  'acquisition': [
    'orchestrator',
    'growth-hacking',
    'email-marketing'
  ]
};

const ROUTING_KEYWORDS = [
  'campagne',
  'automation',
  'email marketing',
  'workflow',
  'lead scoring',
  'funnel',
  'conversion'
];

module.exports = {
  SKILL_ROOT,
  DOMAINS,
  EXPECTED_AGENTS_PER_DOMAIN,
  ROUTING_KEYWORDS
};
