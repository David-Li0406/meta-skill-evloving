/**
 * Configuration for direction-marketing skill tests
 * @module tests/config
 */

const path = require('path');

const SKILL_ROOT = path.join(__dirname, '..');

const DOMAINS = [
  'strategie',
  'positionnement',
  'acquisition',
  'mesure',
  'orchestration'
];

const EXPECTED_AGENTS_PER_DOMAIN = {
  'strategie': [
    'orchestrator',
    'audit-marche',
    'market-analysis',
    'competitor-analysis',
    'swot-marketing',
    'objectifs-marketing',
    'roadmap-marketing',
    'budget-strategy'
  ],
  'positionnement': [
    'orchestrator',
    'discovery',
    'persona-builder',
    'brand-positioning',
    'value-proposition',
    'differentiation'
  ],
  'acquisition': [
    'orchestrator',
    'channel-strategy',
    'funnel-design',
    'budget-allocation',
    'growth-strategy'
  ],
  'mesure': [
    'orchestrator',
    'kpis-definition',
    'objectives-okr',
    'attribution-model',
    'roi-framework'
  ],
  'orchestration': [
    'orchestrator',
    'brief-marketing',
    'delegation-marketing',
    'validation-strategy'
  ]
};

const TOTAL_EXPECTED_AGENTS = 28;

const ROUTING_KEYWORDS = [
  'stratégie marketing',
  'positionnement',
  'persona',
  'acquisition',
  'KPIs marketing',
  'ROI',
  'funnel',
  'growth'
];

// Content quality standards
// @see docs/agent-template-standards.md
const CONTENT_QUALITY = {
  minLines: {
    standard: 100,
    enriched: 200
  },
  requiredSections: [
    'Responsabilité',
    'Inputs',
    'Livrables'
  ],
  recommendedSections: [
    'Tu NE fais PAS',
    'Template de Sortie',
    'Bonnes Pratiques',
    'Pièges à Éviter'
  ],
  requiredYamlFields: ['name', 'description', 'domain'],
  enrichedAgents: [
    'strategie/competitor-analysis',
    'strategie/swot-marketing',
    'strategie/roadmap-marketing',
    'mesure/attribution-model',
    'positionnement/persona-builder'
  ]
};

// Triptyque validation configuration
// Section headers must match actual deliverable templates exactly
const TRIPTYQUE = {
  files: {
    problemDefinition: '.project/strategy/problem-definition.md',
    offerDefinition: '.project/strategy/offer-definition.md',
    persona: '.project/marketing/persona.md',
  },
  contentValidation: {
    // Match actual templates in .web-agency/deliverables/by-category/
    problemDefinition: [
      '## 1. Le Problème en Une Phrase',
      '## 2. Contexte du Problème',
      '## 3. Manifestations du Problème',
      '## 4. Quantification du Problème',
    ],
    offerDefinition: [
      '## 1. Vue d\'Ensemble des Offres',
      '## 2. Offre Principale',
      '## 5. Proposition de Valeur',
      '## 6. Preuves et Crédibilité',
    ],
    persona: [
      '## Photo & Identité',
      '## Objectifs & Motivations',
      '## Comportement Digital',
      '## Parcours d\'Achat',
    ],
  },
  workflow: {
    order: ['discovery', 'persona-builder', 'brand-positioning'],
    maxIterations: 3,
    escalationThresholdDays: 5,
  },
};

module.exports = {
  SKILL_ROOT,
  DOMAINS,
  EXPECTED_AGENTS_PER_DOMAIN,
  TOTAL_EXPECTED_AGENTS,
  ROUTING_KEYWORDS,
  CONTENT_QUALITY,
  TRIPTYQUE
};
