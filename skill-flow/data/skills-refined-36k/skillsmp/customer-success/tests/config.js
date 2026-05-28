/**
 * Configuration for customer-success skill tests
 * @module tests/config
 */

const path = require('path');

const SKILL_ROOT = path.join(__dirname, '..');

const DOMAINS = [
  'lifecycle',
  'loyalty',
  'churn',
  'success'
];

const EXPECTED_AGENTS_PER_DOMAIN = {
  'lifecycle': [
    'orchestrator',
    'onboarding',
    'activation',
    'engagement',
    'retention',
    'advocacy'
  ],
  'loyalty': [
    'orchestrator',
    'program-economics',
    'tier-design',
    'earn-mechanics',
    'burn-rewards',
    'gamification'
  ],
  'churn': [
    'orchestrator',
    'signal-detection',
    'scoring-model',
    'intervention-playbooks',
    'retention-offers',
    'dunning'
  ],
  'success': [
    'orchestrator',
    'health-score',
    'csm-operations',
    'qbr',
    'nps-csat',
    'voc'
  ]
};

const ROUTING_KEYWORDS = [
  'fidélisation',
  'rétention',
  'churn',
  'lifecycle',
  'loyalty',
  'NPS',
  'customer success'
];

module.exports = {
  SKILL_ROOT,
  DOMAINS,
  EXPECTED_AGENTS_PER_DOMAIN,
  ROUTING_KEYWORDS
};
