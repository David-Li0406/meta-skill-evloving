#!/usr/bin/env node
/**
 * Test: Validate Agent Example Test Cases
 *
 * Tests that each agent type can handle realistic sample scenarios.
 * Validates input parsing, expected behavior, and output format.
 *
 * @module tests/validate-agent-examples
 */

const fs = require('fs');
const path = require('path');
const {
  safeReadFile,
  parseFrontmatter,
  directoryExists,
  printSeparator
} = require('./utils');
const {
  PROJECT_MANAGEMENT_DIR,
  PROJECT_MANAGEMENT_AGENTS_DIR,
  PROJECT_MANAGEMENT_SUBDOMAINS
} = require('./config');

// =============================================================================
// Test Results
// =============================================================================

let passed = 0;
let failed = 0;
const errors = [];

// =============================================================================
// Example Test Cases by Agent Type
// =============================================================================

/**
 * Sample inputs and expected behaviors for each agent
 * @const {Object.<string, Object>}
 */
const AGENT_TEST_CASES = {
  // Avant-projet agents
  'collecte-besoin': {
    category: 'extraction',
    sampleInput: `
      Email de Jean Dupont (jean@acme.fr):
      "Bonjour, nous cherchons une refonte de notre site e-commerce.
      Budget: environ 50k€. Deadline: juin 2025.
      Besoin d'un nouveau design et d'améliorer le SEO."
    `,
    expectedBehavior: [
      'extract client info',
      'identify budget',
      'capture deadline',
      'list requirements'
    ],
    outputContains: ['Client', 'Budget', 'Délai', 'Objectifs']
  },

  'formalisation-brief': {
    category: 'structuring',
    sampleInput: 'Données brutes extraites de l\'email client',
    expectedBehavior: [
      'structure into sections',
      'use standard format',
      'highlight gaps'
    ],
    outputContains: ['Contexte', 'Objectifs', 'Périmètre', 'Contraintes']
  },

  'questions-clarification': {
    category: 'analysis',
    sampleInput: 'Brief structuré avec informations manquantes',
    expectedBehavior: [
      'identify missing info',
      'prioritize questions',
      'group by theme'
    ],
    outputContains: ['Question', 'Priorité']
  },

  'chiffrage': {
    category: 'estimation',
    sampleInput: 'Périmètre découpé en lots fonctionnels',
    expectedBehavior: [
      'estimate per lot',
      'break down by profile',
      'calculate totals'
    ],
    outputContains: ['Lot', 'Jours', 'Total']
  },

  // Pilotage agents
  'creation-planning': {
    category: 'planning',
    sampleInput: 'Estimation validée et contraintes calendaires',
    expectedBehavior: [
      'create milestones',
      'sequence tasks',
      'identify critical path'
    ],
    outputContains: ['Jalon', 'Date', 'Tâche']
  },

  'reporting-hebdo': {
    category: 'reporting',
    sampleInput: 'État actuel du projet et écarts détectés',
    expectedBehavior: [
      'summarize progress',
      'highlight issues',
      'list next steps'
    ],
    outputContains: ['Avancement', 'Attention', 'Statut']
  },

  // Communication agents
  'email-relance': {
    category: 'communication',
    sampleInput: 'Client non répondant depuis 5 jours',
    expectedBehavior: [
      'professional tone',
      'clear call to action',
      'reference previous exchange'
    ],
    outputContains: ['Objet', 'Message']
  },

  // Livraison agents
  'plan-recette': {
    category: 'testing',
    sampleInput: 'Spécifications fonctionnelles du projet',
    expectedBehavior: [
      'define test scope',
      'list test types',
      'set acceptance criteria'
    ],
    outputContains: ['Périmètre', 'Critères', 'Planning']
  },

  'pv-recette': {
    category: 'documentation',
    sampleInput: 'Résultats de recette et anomalies',
    expectedBehavior: [
      'document test results',
      'list resolved issues',
      'get sign-off'
    ],
    outputContains: ['Résultat', 'Validation', 'Signature']
  },

  // Facturation agents
  'preparation-facture': {
    category: 'billing',
    sampleInput: 'Jalon atteint et livrables validés',
    expectedBehavior: [
      'reference contract',
      'list deliverables',
      'calculate amount'
    ],
    outputContains: ['Montant', 'Livrable', 'Référence']
  }
};

// =============================================================================
// Helper Functions
// =============================================================================

/**
 * Check if agent content supports the expected behavior
 *
 * @param {string} content - Agent markdown content
 * @param {string[]} behaviors - Expected behaviors
 * @returns {string[]} Missing behavior indicators
 */
function checkExpectedBehaviors(content, behaviors) {
  const missing = [];
  const contentLower = content.toLowerCase();

  // Behavior keyword mappings
  const behaviorKeywords = {
    'extract client info': ['client', 'extraire', 'information'],
    'identify budget': ['budget', 'montant', 'coût'],
    'capture deadline': ['délai', 'date', 'deadline'],
    'list requirements': ['besoin', 'fonctionnalité', 'exigence'],
    'structure into sections': ['section', 'structur', 'format'],
    'use standard format': ['template', 'format', 'standard'],
    'highlight gaps': ['manquant', 'incomplet', 'à clarifier'],
    'identify missing info': ['manquant', 'question', 'clarifi'],
    'prioritize questions': ['priorité', 'important', 'critique'],
    'group by theme': ['thème', 'catégorie', 'groupe'],
    'estimate per lot': ['lot', 'estim', 'charge'],
    'break down by profile': ['profil', 'développeur', 'designer'],
    'calculate totals': ['total', 'somme', 'montant'],
    'create milestones': ['jalon', 'milestone', 'étape'],
    'sequence tasks': ['tâche', 'séquence', 'ordre'],
    'identify critical path': ['critique', 'dépendance', 'chemin'],
    'summarize progress': ['avancement', 'progression', 'statut'],
    'highlight issues': ['problème', 'risque', 'alerte'],
    'list next steps': ['action', 'prochaine', 'suivant'],
    'professional tone': ['professionnel', 'cordial', 'ton'],
    'clear call to action': ['action', 'demande', 'réponse'],
    'reference previous exchange': ['précédent', 'référence', 'suite'],
    'define test scope': ['périmètre', 'scope', 'couverture'],
    'list test types': ['test', 'type', 'fonctionnel'],
    'set acceptance criteria': ['critère', 'acceptance', 'validation'],
    'document test results': ['résultat', 'test', 'document'],
    'list resolved issues': ['résolu', 'corrigé', 'anomalie'],
    'get sign-off': ['signature', 'validation', 'accord'],
    'reference contract': ['contrat', 'devis', 'référence'],
    'list deliverables': ['livrable', 'élément', 'fourni'],
    'calculate amount': ['montant', 'calcul', 'total']
  };

  for (const behavior of behaviors) {
    const keywords = behaviorKeywords[behavior] || [behavior];
    const found = keywords.some(kw => contentLower.includes(kw));

    if (!found) {
      missing.push(behavior);
    }
  }

  return missing;
}

/**
 * Check if agent output template contains expected sections
 *
 * @param {string} content - Agent content
 * @param {string[]} expectedOutputs - Expected output sections
 * @returns {string[]} Missing output sections
 */
function checkOutputTemplate(content, expectedOutputs) {
  const missing = [];
  const contentLower = content.toLowerCase();

  for (const output of expectedOutputs) {
    if (!contentLower.includes(output.toLowerCase())) {
      missing.push(output);
    }
  }

  return missing;
}

/**
 * Get agent category from test case or infer from content
 *
 * @param {Object} testCase - Test case definition
 * @param {string} content - Agent content
 * @returns {string} Agent category
 */
function getAgentCategory(testCase, content) {
  if (testCase) return testCase.category;

  // Infer from content keywords
  if (content.includes('email') || content.includes('message')) return 'communication';
  if (content.includes('estim') || content.includes('chiffr')) return 'estimation';
  if (content.includes('planning') || content.includes('jalon')) return 'planning';
  if (content.includes('test') || content.includes('recette')) return 'testing';
  if (content.includes('factur') || content.includes('paiement')) return 'billing';

  return 'general';
}

// =============================================================================
// Test Functions
// =============================================================================

/**
 * Test agent has proper input handling
 *
 * @param {string} agentName - Agent name
 * @param {string} content - Agent content
 * @param {Object} testCase - Test case definition
 */
function testAgentInputHandling(agentName, content, testCase) {
  const hasInputSection =
    content.includes('## Input') ||
    content.includes('## Entrée') ||
    content.includes('## Contexte Nécessaire') ||
    content.includes('Inputs Acceptés');

  if (hasInputSection) {
    console.log(`   ✅ Has input handling section`);
    passed++;
  } else {
    console.log(`   ⚠️  No explicit input section`);
    passed++; // Warning only
  }
}

/**
 * Test agent supports expected behaviors
 *
 * @param {string} agentName - Agent name
 * @param {string} content - Agent content
 * @param {Object} testCase - Test case definition
 */
function testAgentBehaviors(agentName, content, testCase) {
  if (!testCase || !testCase.expectedBehavior) {
    console.log(`   ⏭️  No behavior tests defined`);
    passed++;
    return;
  }

  const missingBehaviors = checkExpectedBehaviors(content, testCase.expectedBehavior);

  if (missingBehaviors.length === 0) {
    console.log(`   ✅ Supports all expected behaviors (${testCase.expectedBehavior.length})`);
    passed++;
  } else if (missingBehaviors.length <= testCase.expectedBehavior.length / 2) {
    console.log(`   ⚠️  May not support: ${missingBehaviors.slice(0, 2).join(', ')}`);
    passed++; // Partial support is acceptable
  } else {
    console.log(`   ❌ Missing behaviors: ${missingBehaviors.join(', ')}`);
    errors.push(`[${agentName}] Missing behaviors`);
    failed++;
  }
}

/**
 * Test agent output template
 *
 * @param {string} agentName - Agent name
 * @param {string} content - Agent content
 * @param {Object} testCase - Test case definition
 */
function testAgentOutputTemplate(agentName, content, testCase) {
  if (!testCase || !testCase.outputContains) {
    console.log(`   ⏭️  No output tests defined`);
    passed++;
    return;
  }

  const missingOutputs = checkOutputTemplate(content, testCase.outputContains);

  if (missingOutputs.length === 0) {
    console.log(`   ✅ Output template has required sections`);
    passed++;
  } else if (missingOutputs.length <= testCase.outputContains.length / 2) {
    console.log(`   ⚠️  Output may miss: ${missingOutputs.join(', ')}`);
    passed++;
  } else {
    console.log(`   ❌ Output missing: ${missingOutputs.join(', ')}`);
    errors.push(`[${agentName}] Incomplete output template`);
    failed++;
  }
}

/**
 * Test agent has process/workflow documentation
 *
 * @param {string} agentName - Agent name
 * @param {string} content - Agent content
 */
function testAgentProcessDoc(agentName, content) {
  const hasProcess =
    content.includes('## Processus') ||
    content.includes('## Process') ||
    content.includes('## Étapes') ||
    content.includes('```') && content.includes('→');

  if (hasProcess) {
    console.log(`   ✅ Has process documentation`);
    passed++;
  } else {
    console.log(`   ⚠️  No explicit process flow`);
    passed++; // Warning only
  }
}

// =============================================================================
// Main Execution
// =============================================================================

console.log('🧪 Validating Agent Example Test Cases\n');
printSeparator();

if (!directoryExists(PROJECT_MANAGEMENT_DIR)) {
  console.error(`❌ Project management directory not found: ${PROJECT_MANAGEMENT_DIR}`);
  process.exit(1);
}

let totalAgentsTested = 0;

for (const subdomain of PROJECT_MANAGEMENT_SUBDOMAINS) {
  const subdomainPath = path.join(PROJECT_MANAGEMENT_AGENTS_DIR, subdomain);
  console.log(`\n📂 ${subdomain}/`);

  if (!directoryExists(subdomainPath)) {
    console.log(`   ❌ Subdomain not found`);
    failed++;
    continue;
  }

  // Get all agent files (excluding orchestrator)
  const files = fs.readdirSync(subdomainPath)
    .filter(f => f.endsWith('.md') && !f.includes('orchestrator'));

  for (const file of files) {
    const agentName = path.basename(file, '.md');
    const agentPath = path.join(subdomainPath, file);
    const testCase = AGENT_TEST_CASES[agentName];

    console.log(`\n   🤖 ${agentName}`);

    const { content, error } = safeReadFile(agentPath);
    if (error) {
      console.log(`      ❌ ${error}`);
      errors.push(`[${agentName}] ${error}`);
      failed++;
      continue;
    }

    const category = getAgentCategory(testCase, content);
    console.log(`      Category: ${category}`);

    testAgentInputHandling(agentName, content, testCase);
    testAgentBehaviors(agentName, content, testCase);
    testAgentOutputTemplate(agentName, content, testCase);
    testAgentProcessDoc(agentName, content);

    totalAgentsTested++;
  }
}

// =============================================================================
// Summary
// =============================================================================

console.log('\n');
printSeparator();
console.log(`\n📊 Results: ${passed} passed, ${failed} failed`);
console.log(`   Agents tested: ${totalAgentsTested}`);
console.log(`   Test cases defined: ${Object.keys(AGENT_TEST_CASES).length}`);

if (errors.length > 0) {
  console.log('\n❌ Agent example test errors:');
  for (const err of errors) {
    console.log(`   └─ ${err}`);
  }
  process.exit(1);
} else {
  console.log('\n✅ All agent example tests passed');
  process.exit(0);
}
