/**
 * Configuration for seo-expert skill tests
 * @module tests/config
 */

const path = require('path');

const SKILL_ROOT = path.join(__dirname, '..');

const DOMAINS = [
  'technique',
  'contenu',
  'netlinking',
  'local',
  'international',
  'strategie',
  'pilotage'
];

const EXPECTED_AGENTS_PER_DOMAIN = {
  'technique': [
    'orchestrator',
    'core-web-vitals',
    'crawl-indexation',
    'architecture-site',
    'javascript-seo',
    'migration-seo'
  ],
  'contenu': [
    'orchestrator',
    'recherche-mots-cles',
    'brief-redactionnel',
    'semantique-seo',
    'optimisation-onpage'
  ],
  'netlinking': [
    'orchestrator',
    'strategie-backlinks',
    'prospection-liens',
    'outreach-partenariats',
    'analyse-profil-liens'
  ],
  'local': [
    'orchestrator',
    'google-business',
    'citations-nap',
    'avis-reputation',
    'local-content'
  ],
  'international': [
    'orchestrator',
    'hreflang',
    'geotargeting',
    'localisation-contenu',
    'strategie-structure'
  ],
  'strategie': [
    'orchestrator',
    'audit-global',
    'roadmap-seo',
    'opportunites-keywords'
  ],
  'pilotage': [
    'orchestrator',
    'reporting-seo',
    'analytics-seo',
    'suivi-positions',
    'veille-algorithmes'
  ]
};

const ROUTING_KEYWORDS = [
  'SEO',
  'référencement',
  'mots-clés',
  'backlinks',
  'Core Web Vitals',
  'indexation',
  'netlinking',
  'SEO local'
];

module.exports = {
  SKILL_ROOT,
  DOMAINS,
  EXPECTED_AGENTS_PER_DOMAIN,
  ROUTING_KEYWORDS
};
