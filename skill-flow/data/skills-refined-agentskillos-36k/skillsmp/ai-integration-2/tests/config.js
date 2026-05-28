/**
 * Centralized configuration for AI Integration skill tests
 *
 * @module tests/config
 */

const path = require('path');

/** @const {string} Base directory for the skill */
const SKILL_ROOT = path.join(__dirname, '..');

/** @const {string[]} AI Integration domains */
const DOMAINS = [
  'llm',
  'rag',
  'vectors',
  'prompting',
  'agents',
  'mlops'
];

/** @const {Object} Expected agents per domain */
const EXPECTED_AGENTS_PER_DOMAIN = {
  'llm': [
    'orchestrator',
    'openai',
    'claude',
    'langchain'
  ],
  'rag': [
    'orchestrator',
    'architecture'
  ],
  'vectors': [
    'orchestrator',
    'pgvector'
  ],
  'prompting': [
    'orchestrator',
    'patterns'
  ],
  'agents': [
    'orchestrator'
  ],
  'mlops': [
    'orchestrator'
  ]
};

/**
 * Agent validation requirements
 */
const AGENT_REQUIREMENTS = {
  frontmatter: ['name', 'description'],
  minOrchestratorLength: 500,
  minAgentLength: 400,
  minContentLength: 400,
  orchestratorSections: ['Agents', 'Routage'],
  agentSections: []
};

/**
 * Domain keywords for routing validation
 */
const DOMAIN_KEYWORDS = {
  'llm': ['OpenAI', 'Claude', 'GPT', 'LLM', 'API', 'chat', 'completion'],
  'rag': ['RAG', 'retrieval', 'augmented', 'chunking', 'embedding', 'vector'],
  'vectors': ['pgvector', 'Pinecone', 'Weaviate', 'embedding', 'similarity'],
  'prompting': ['prompt', 'few-shot', 'chain-of-thought', 'template'],
  'agents': ['agent', 'tool', 'function calling', 'memory'],
  'mlops': ['deployment', 'fine-tuning', 'monitoring', 'MLflow']
};

/**
 * Get total expected agent count
 * @returns {number}
 */
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
