/**
 * Configuration for paid-media skill tests
 * @module tests/config
 */

const path = require('path');

const SKILL_ROOT = path.join(__dirname, '..');

const DOMAINS = [
  'sea',
  'social-ads',
  'display',
  'video'
];

const EXPECTED_AGENTS_PER_DOMAIN = {
  'sea': [
    'orchestrator',
    'campaign-structure',
    'keyword-strategy',
    'bidding-optimization',
    'quality-score',
    'ad-copy',
    'extensions'
  ],
  'social-ads': [
    'orchestrator',
    'audience-targeting',
    'creative-strategy',
    'campaign-objectives',
    'placement-optimization',
    'retargeting'
  ],
  'display': [
    'orchestrator',
    'programmatic-buying',
    'dsp-management',
    'audience-segments',
    'brand-safety'
  ],
  'video': [
    'orchestrator',
    'youtube-ads',
    'video-formats',
    'ctv-ott'
  ]
};

const ROUTING_KEYWORDS = [
  'Google Ads',
  'SEA',
  'Meta Ads',
  'Facebook Ads',
  'Social Ads',
  'Display',
  'Programmatic',
  'YouTube Ads'
];

module.exports = {
  SKILL_ROOT,
  DOMAINS,
  EXPECTED_AGENTS_PER_DOMAIN,
  ROUTING_KEYWORDS
};
