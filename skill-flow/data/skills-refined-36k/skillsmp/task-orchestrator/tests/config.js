/**
 * Centralized configuration for task-orchestrator skill tests
 * @module tests/config
 */

const fs = require('fs');
const path = require('path');

/** @const {string} Base directory for the task-orchestrator skill */
const SKILL_ROOT = path.join(__dirname, '..');

/** @const {string} Directory containing agents */
const AGENTS_DIR = path.join(SKILL_ROOT, 'agents');

/** @const {string[]} Expected domains in task-orchestrator */
const EXPECTED_DOMAINS = [
  'queue',
  'state-machine',
  'execution',
  'tracking'
];

/** @const {Object.<string, string[]>} Expected agents per domain */
const EXPECTED_AGENTS = {
  'queue': [
    'orchestrator',
    'queue-manager',
    'priority-adjuster',
    'capacity-monitor',
    'sla-tracker'
  ],
  'state-machine': [
    'orchestrator',
    'state-controller',
    'workflow-engine',
    'blocker-handler',
    'rollback-manager'
  ],
  'execution': [
    'orchestrator',
    'task-dispatcher',
    'parallel-executor',
    'result-collector',
    'error-handler'
  ],
  'tracking': [
    'orchestrator',
    'progress-tracker',
    'metrics-collector',
    'report-generator',
    'audit-logger'
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
 * State machine states
 * @const {string[]}
 */
const TASK_STATES = [
  'CREATED',
  'QUEUED',
  'SCHEDULED',
  'IN_PROGRESS',
  'BLOCKED',
  'COMPLETED',
  'FAILED',
  'CANCELLED'
];

/**
 * Expected routing rules per domain orchestrator
 * @const {Object.<string, Object[]>}
 */
const EXPECTED_ROUTING = {
  'queue': [
    { intent: 'ajouter tâche', agent: 'queue-manager' },
    { intent: 'priorité', agent: 'priority-adjuster' },
    { intent: 'capacité', agent: 'capacity-monitor' },
    { intent: 'SLA', agent: 'sla-tracker' }
  ],
  'state-machine': [
    { intent: 'état', agent: 'state-controller' },
    { intent: 'workflow', agent: 'workflow-engine' },
    { intent: 'blocage', agent: 'blocker-handler' },
    { intent: 'annulation', agent: 'rollback-manager' }
  ],
  'execution': [
    { intent: 'dispatch', agent: 'task-dispatcher' },
    { intent: 'parallèle', agent: 'parallel-executor' },
    { intent: 'résultat', agent: 'result-collector' },
    { intent: 'erreur', agent: 'error-handler' }
  ],
  'tracking': [
    { intent: 'avancement', agent: 'progress-tracker' },
    { intent: 'métriques', agent: 'metrics-collector' },
    { intent: 'rapport', agent: 'report-generator' },
    { intent: 'audit', agent: 'audit-logger' }
  ]
};

module.exports = {
  SKILL_ROOT,
  AGENTS_DIR,
  EXPECTED_DOMAINS,
  EXPECTED_AGENTS,
  AGENT_REQUIREMENTS,
  TASK_STATES,
  EXPECTED_ROUTING
};
