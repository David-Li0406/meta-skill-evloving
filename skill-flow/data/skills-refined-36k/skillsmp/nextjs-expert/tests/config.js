/**
 * Configuration des tests pour nextjs-expert
 */

export const SKILL_CONFIG = {
  name: 'nextjs-expert',
  version: '1.0.0',
  basePath: '..',

  // Domaines attendus
  domains: [
    'app-router',
    'server-components',
    'data',
    'rendering',
    'optimization',
    'deployment',
    'testing'
  ],

  // Agents par domaine
  expectedAgents: {
    'app-router': [
      'orchestrator',
      'routing',
      'layouts',
      'navigation',
      'error-handling'
    ],
    'server-components': [
      'orchestrator',
      'server-vs-client',
      'async-components',
      'streaming',
      'composition'
    ],
    'data': [
      'orchestrator',
      'data-fetching',
      'server-actions',
      'revalidation',
      'client-fetching'
    ],
    'rendering': [
      'orchestrator',
      'ssr-ssg',
      'isr',
      'middleware',
      'edge-runtime'
    ],
    'optimization': [
      'orchestrator',
      'images',
      'fonts',
      'bundle',
      'caching'
    ],
    'deployment': [
      'orchestrator',
      'vercel',
      'docker',
      'environment',
      'ci-cd'
    ],
    'testing': [
      'orchestrator',
      'unit-testing',
      'integration-testing',
      'e2e-testing',
      'mocking'
    ]
  },

  // Fichiers requis à la racine
  requiredRootFiles: [
    'SKILL.md',
    'orchestrator.md'
  ],

  // Total attendu
  totalAgents: 35
};
