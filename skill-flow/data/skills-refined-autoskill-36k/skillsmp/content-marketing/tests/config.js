/**
 * Configuration for content-marketing skill tests
 * @module tests/config
 */

const path = require('path');

const SKILL_ROOT = path.join(__dirname, '..');

const DOMAINS = [
  'content',
  'social-strategy'
];

const EXPECTED_AGENTS_PER_DOMAIN = {
  'content': [
    'orchestrator',
    'ligne-editoriale',
    'arborescence',
    'copywriting',
    'blog-articles',
    'social-media-content',
    'landing-pages'
  ],
  'social-strategy': [
    'orchestrator',
    'platform-strategy',
    'engagement-strategy',
    'community-management',
    'social-listening'
  ]
};

const ROUTING_KEYWORDS = [
  'contenu',
  'copywriting',
  'ligne éditoriale',
  'social media',
  'community management',
  'blog',
  'landing page'
];

module.exports = {
  SKILL_ROOT,
  DOMAINS,
  EXPECTED_AGENTS_PER_DOMAIN,
  ROUTING_KEYWORDS
};
