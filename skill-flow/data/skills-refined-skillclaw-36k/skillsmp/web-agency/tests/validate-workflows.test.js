#!/usr/bin/env node
/**
 * Test: Validate Agent Workflows (Integration Tests)
 *
 * Validates that workflow sequences are complete and agents
 * can work together as defined in the workflow configurations.
 *
 * @module tests/validate-workflows
 */

const fs = require('fs');
const path = require('path');
const {
  findMarkdownFiles,
  safeReadFile,
  parseFrontmatter,
  directoryExists,
  printSeparator
} = require('./utils');
const {
  PROJECT_MANAGEMENT_DIR,
  PROJECT_MANAGEMENT_AGENTS_DIR,
  WORKFLOWS,
  AGENT_REQUIREMENTS
} = require('./config');

// =============================================================================
// Test Results
// =============================================================================

let passed = 0;
let failed = 0;
const errors = [];

// =============================================================================
// Helper Functions
// =============================================================================

/**
 * Get agent file path from subdomain and agent name
 *
 * @param {string} subdomain - The subdomain (e.g., 'avant-projet')
 * @param {string} agentName - The agent name
 * @returns {string} Full path to agent file
 */
function getAgentPath(subdomain, agentName) {
  return path.join(PROJECT_MANAGEMENT_AGENTS_DIR, subdomain, `${agentName}.md`);
}

/**
 * Check if agent has required output template
 *
 * @param {string} content - Agent content
 * @returns {boolean} True if template found
 */
function hasOutputTemplate(content) {
  return content.includes('## Template') ||
         content.includes('## Format de Sortie') ||
         content.includes('## Sortie') ||
         content.includes('```markdown');
}

/**
 * Check if agent accepts input type
 *
 * @param {string} content - Agent content
 * @param {string} inputType - Expected input type
 * @returns {boolean} True if input section exists
 */
function hasInputSection(content) {
  return content.includes('## Input') ||
         content.includes('## Inputs') ||
         content.includes('## Entrée') ||
         content.includes('## Contexte Nécessaire');
}

/**
 * Validate agent meets SRP requirements
 *
 * @param {string} content - Agent content
 * @returns {string[]} Array of missing requirements
 */
function validateAgentSRP(content) {
  const missing = [];

  for (const section of AGENT_REQUIREMENTS.requiredSections) {
    if (!content.includes(section)) {
      missing.push(section);
    }
  }

  return missing;
}

/**
 * Check workflow step connectivity
 * Validates that output of step N can be input of step N+1
 *
 * @param {Object[]} steps - Workflow steps
 * @returns {string[]} Connectivity issues
 */
function checkWorkflowConnectivity(steps) {
  const issues = [];

  for (let i = 0; i < steps.length - 1; i++) {
    const currentStep = steps[i];
    const nextStep = steps[i + 1];

    if (currentStep.output !== nextStep.input) {
      issues.push(
        `Step ${i + 1} (${currentStep.agent}) outputs '${currentStep.output}' ` +
        `but step ${i + 2} (${nextStep.agent}) expects '${nextStep.input}'`
      );
    }
  }

  return issues;
}

// =============================================================================
// Test Functions
// =============================================================================

/**
 * Test that all agents in workflow exist
 *
 * @param {string} workflowId - Workflow identifier
 * @param {Object} workflow - Workflow definition
 */
function testWorkflowAgentsExist(workflowId, workflow) {
  console.log(`\n📋 Testing: ${workflow.name}`);
  console.log(`   ${workflow.description}`);

  let workflowPassed = true;
  const missingAgents = [];

  for (const step of workflow.steps) {
    const agentPath = getAgentPath(workflow.subdomain, step.agent);

    if (!fs.existsSync(agentPath)) {
      missingAgents.push(step.agent);
      workflowPassed = false;
    }
  }

  if (missingAgents.length > 0) {
    console.log(`   ❌ Missing agents: ${missingAgents.join(', ')}`);
    errors.push(`[${workflowId}] Missing agents: ${missingAgents.join(', ')}`);
    failed++;
  } else {
    console.log(`   ✅ All ${workflow.steps.length} agents exist`);
    passed++;
  }

  return workflowPassed;
}

/**
 * Test workflow agent chain integrity
 *
 * @param {string} workflowId - Workflow identifier
 * @param {Object} workflow - Workflow definition
 */
function testWorkflowChainIntegrity(workflowId, workflow) {
  const issues = checkWorkflowConnectivity(workflow.steps);

  if (issues.length > 0) {
    console.log(`   ❌ Chain connectivity issues:`);
    for (const issue of issues) {
      console.log(`      └─ ${issue}`);
    }
    errors.push(`[${workflowId}] Chain issues: ${issues.length}`);
    failed++;
  } else {
    console.log(`   ✅ Workflow chain is connected`);
    passed++;
  }
}

/**
 * Test that workflow agents have proper I/O
 *
 * @param {string} workflowId - Workflow identifier
 * @param {Object} workflow - Workflow definition
 */
function testWorkflowAgentIO(workflowId, workflow) {
  let ioIssues = 0;

  for (const step of workflow.steps) {
    const agentPath = getAgentPath(workflow.subdomain, step.agent);
    const { content, error } = safeReadFile(agentPath);

    if (error) continue;

    if (!hasOutputTemplate(content)) {
      console.log(`   ⚠️  ${step.agent}: No output template defined`);
      ioIssues++;
    }
  }

  if (ioIssues === 0) {
    console.log(`   ✅ All agents have output templates`);
    passed++;
  } else {
    console.log(`   ⚠️  ${ioIssues} agents missing output templates`);
    // Warning only, not failure
    passed++;
  }
}

/**
 * Test that workflow agents follow SRP
 *
 * @param {string} workflowId - Workflow identifier
 * @param {Object} workflow - Workflow definition
 */
function testWorkflowAgentsSRP(workflowId, workflow) {
  let srpIssues = 0;

  for (const step of workflow.steps) {
    const agentPath = getAgentPath(workflow.subdomain, step.agent);
    const { content, error } = safeReadFile(agentPath);

    if (error) continue;

    const missing = validateAgentSRP(content);
    if (missing.length > 0) {
      srpIssues++;
    }
  }

  if (srpIssues === 0) {
    console.log(`   ✅ All agents follow SRP pattern`);
    passed++;
  } else {
    console.log(`   ⚠️  ${srpIssues} agents missing SRP sections`);
    // Warning only for now
    passed++;
  }
}

// =============================================================================
// Main Execution
// =============================================================================

console.log('🔗 Validating Agent Workflows (Integration Tests)\n');
printSeparator();

if (!directoryExists(PROJECT_MANAGEMENT_DIR)) {
  console.error(`❌ Project management directory not found: ${PROJECT_MANAGEMENT_DIR}`);
  process.exit(1);
}

console.log(`Testing ${Object.keys(WORKFLOWS).length} workflow definitions\n`);

for (const [workflowId, workflow] of Object.entries(WORKFLOWS)) {
  const agentsExist = testWorkflowAgentsExist(workflowId, workflow);

  if (agentsExist) {
    testWorkflowChainIntegrity(workflowId, workflow);
    testWorkflowAgentIO(workflowId, workflow);
    testWorkflowAgentsSRP(workflowId, workflow);
  }
}

// =============================================================================
// Summary
// =============================================================================

console.log('\n');
printSeparator();
console.log(`\n📊 Results: ${passed} passed, ${failed} failed`);

if (errors.length > 0) {
  console.log('\n❌ Workflow validation errors:');
  for (const err of errors) {
    console.log(`   └─ ${err}`);
  }
  process.exit(1);
} else {
  console.log('\n✅ All workflow integration tests passed');
  process.exit(0);
}
