/**
 * Centralized configuration for client-intake skill tests
 * @module tests/config
 */

const fs = require('fs');
const path = require('path');

/** @const {string} Base directory for the client-intake skill */
const SKILL_ROOT = path.join(__dirname, '..');

/** @const {string} Directory containing agents */
const AGENTS_DIR = path.join(SKILL_ROOT, 'agents');

/** @const {string[]} Expected domains in client-intake */
const EXPECTED_DOMAINS = [
  'reception',
  'qualification',
  'extraction',
  'response',
  'routing'
];

/** @const {Object.<string, string[]>} Expected agents per domain */
const EXPECTED_AGENTS = {
  'reception': [
    'orchestrator',
    'email-parser',
    'form-handler',
    'chat-handler',
    'webhook-receiver',
    'attachment-processor'
  ],
  'qualification': [
    'orchestrator',
    'intent-classifier',
    'complexity-assessor',
    'urgency-detector',
    'budget-estimator',
    'feasibility-checker'
  ],
  'extraction': [
    'orchestrator',
    'requirements-extractor',
    'stakeholder-identifier',
    'timeline-parser',
    'tech-stack-detector',
    'constraints-mapper'
  ],
  'response': [
    'orchestrator',
    'acknowledgment-sender',
    'clarification-requester',
    'status-notifier',
    'rejection-handler'
  ],
  'routing': [
    'orchestrator',
    'skill-matcher',
    'priority-ranker',
    'workload-balancer',
    'dependency-resolver'
  ]
};

/**
 * Agent validation requirements
 * @const {Object}
 */
const AGENT_REQUIREMENTS = {
  /** Required frontmatter fields */
  frontmatter: ['name', 'description', 'version'],

  /** Required markdown sections for SRP agents */
  requiredSections: [
    'Ta Responsabilité Unique'
  ],

  /** Required sections for orchestrators */
  orchestratorSections: [
    'Workflow',
    'Agents'
  ],

  /** Minimum content length (characters) */
  minContentLength: 200
};

/**
 * Expected routing rules per domain orchestrator
 * @const {Object.<string, Object[]>}
 */
const EXPECTED_ROUTING = {
  'reception': [
    { intent: 'email', agent: 'email-parser' },
    { intent: 'formulaire', agent: 'form-handler' },
    { intent: 'chat', agent: 'chat-handler' },
    { intent: 'webhook', agent: 'webhook-receiver' },
    { intent: 'pièce jointe', agent: 'attachment-processor' }
  ],
  'qualification': [
    { intent: 'type de demande', agent: 'intent-classifier' },
    { intent: 'complexité', agent: 'complexity-assessor' },
    { intent: 'urgence', agent: 'urgency-detector' },
    { intent: 'budget', agent: 'budget-estimator' },
    { intent: 'faisabilité', agent: 'feasibility-checker' }
  ],
  'extraction': [
    { intent: 'exigences', agent: 'requirements-extractor' },
    { intent: 'interlocuteurs', agent: 'stakeholder-identifier' },
    { intent: 'dates', agent: 'timeline-parser' },
    { intent: 'technologies', agent: 'tech-stack-detector' },
    { intent: 'contraintes', agent: 'constraints-mapper' }
  ],
  'response': [
    { intent: 'accusé réception', agent: 'acknowledgment-sender' },
    { intent: 'clarification', agent: 'clarification-requester' },
    { intent: 'statut', agent: 'status-notifier' },
    { intent: 'refus', agent: 'rejection-handler' }
  ],
  'routing': [
    { intent: 'skill cible', agent: 'skill-matcher' },
    { intent: 'priorité', agent: 'priority-ranker' },
    { intent: 'charge', agent: 'workload-balancer' },
    { intent: 'dépendances', agent: 'dependency-resolver' }
  ]
};

module.exports = {
  SKILL_ROOT,
  AGENTS_DIR,
  EXPECTED_DOMAINS,
  EXPECTED_AGENTS,
  AGENT_REQUIREMENTS,
  EXPECTED_ROUTING
};
