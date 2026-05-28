/**
 * Centralized configuration for Security Expert skill tests
 *
 * @module tests/config
 */

const path = require('path');

const SKILL_ROOT = path.join(__dirname, '..');

const DOMAINS = [
  'appsec',
  'secure-coding',
  'threat-modeling',
  'penetration',
  'compliance'
];

const EXPECTED_AGENTS_PER_DOMAIN = {
  'appsec': [
    'orchestrator',
    'sast',
    'dast',
    'iast',
    'sca'
  ],
  'secure-coding': [
    'orchestrator',
    'validation',
    'authentication',
    'authorization',
    'cryptography'
  ],
  'threat-modeling': [
    'orchestrator',
    'stride',
    'attack-trees',
    'risk-assessment'
  ],
  'penetration': [
    'orchestrator',
    'owasp-top10',
    'api-security',
    'web-vulnerabilities',
    'reporting'
  ],
  'compliance': [
    'orchestrator',
    'rgpd',
    'soc2',
    'iso27001',
    'pci-dss'
  ]
};

const AGENT_REQUIREMENTS = {
  frontmatter: ['name', 'description'],
  minOrchestratorLength: 500,
  minAgentLength: 400,
  minContentLength: 400
};

const DOMAIN_KEYWORDS = {
  'appsec': ['SAST', 'DAST', 'IAST', 'SCA', 'scanning', 'vulnerability'],
  'secure-coding': ['validation', 'authentication', 'authorization', 'cryptography', 'Zod'],
  'threat-modeling': ['STRIDE', 'attack', 'threat', 'risk', 'CVSS'],
  'penetration': ['OWASP', 'injection', 'XSS', 'pentest', 'vulnerability'],
  'compliance': ['RGPD', 'SOC2', 'ISO27001', 'PCI DSS', 'compliance']
};

function getTotalExpectedAgents() {
  return Object.values(EXPECTED_AGENTS_PER_DOMAIN)
    .reduce((sum, agents) => sum + agents.length, 0);
}

module.exports = {
  SKILL_ROOT,
  DOMAINS,
  EXPECTED_AGENTS_PER_DOMAIN,
  AGENT_REQUIREMENTS,
  DOMAIN_KEYWORDS,
  getTotalExpectedAgents
};
