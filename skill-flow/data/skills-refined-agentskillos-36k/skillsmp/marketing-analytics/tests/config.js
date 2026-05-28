/**
 * Configuration for marketing-analytics skill tests
 * @module tests/config
 */

const path = require('path');

const SKILL_ROOT = path.join(__dirname, '..');

const DOMAINS = [
  'tracking',
  'attribution',
  'reporting',
  'testing',
  'insights',
  'analytics'
];

const EXPECTED_AGENTS_PER_DOMAIN = {
  'tracking': [
    'orchestrator',
    'gtm-setup',
    'pixel-implementation',
    'data-layer',
    'server-side',
    'consent-management'
  ],
  'attribution': [
    'orchestrator',
    'attribution-models',
    'customer-journey',
    'touchpoint-analysis',
    'cross-device'
  ],
  'reporting': [
    'orchestrator',
    'dashboard-design',
    'kpi-framework',
    'data-visualization',
    'automated-reporting'
  ],
  'testing': [
    'orchestrator',
    'experiment-design',
    'statistical-analysis',
    'hypothesis-testing',
    'multivariate-testing'
  ],
  'insights': [
    'orchestrator',
    'funnel-analysis',
    'cohort-analysis',
    'predictive-analytics',
    'customer-segmentation'
  ],
  'analytics': [
    'orchestrator',
    'kpi-tracking',
    'ab-testing',
    'attribution',
    'reporting'
  ]
};

const ROUTING_KEYWORDS = [
  'tracking',
  'GA4',
  'GTM',
  'attribution',
  'analytics',
  'A/B testing',
  'dashboard',
  'KPI'
];

module.exports = {
  SKILL_ROOT,
  DOMAINS,
  EXPECTED_AGENTS_PER_DOMAIN,
  ROUTING_KEYWORDS
};
