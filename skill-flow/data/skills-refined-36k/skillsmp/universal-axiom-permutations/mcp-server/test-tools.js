#!/usr/bin/env node

/**
 * Test script for MCP Server Tools
 *
 * Tests each tool exposed by the MCP server to ensure they work correctly.
 */

import { UniversalAxiom, AxiomSimulator } from './build/mcp-server/universal-axiom.js';

const GREEN = '\x1b[32m';
const RED = '\x1b[31m';
const RESET = '\x1b[0m';
const BLUE = '\x1b[34m';

let passCount = 0;
let failCount = 0;

function assert(condition, testName) {
  if (condition) {
    console.log(`${GREEN}✓${RESET} ${testName}`);
    passCount++;
  } else {
    console.log(`${RED}✗${RESET} ${testName}`);
    failCount++;
  }
}

function testSection(name) {
  console.log(`\n${BLUE}=== ${name} ===${RESET}`);
}

// Test 1: UniversalAxiom can be instantiated
testSection('Core Functionality Tests');

try {
  const axiom = new UniversalAxiom({
    impulses: 1.0,
    elements: 1.0,
    pressure: 1.0,
    subjectivity: 0.0,
    purpose: 1.0,
    time: 1.0,
    n: 1
  });
  assert(axiom !== null, 'UniversalAxiom instantiation');

  const intelligence = axiom.computeIntelligence();
  assert(intelligence === 10.0, `compute_intelligence (expected 10.0, got ${intelligence})`);

  const state = axiom.getState();
  assert(state.intelligence === 10.0, 'getState returns correct intelligence');
  assert(state.foundation.product === 1.0, 'Foundation layer computed correctly');
  assert(state.cognitive.X_objectivity === 1.0, 'Cognitive layer computed correctly');
} catch (error) {
  console.error(`${RED}✗${RESET} Core functionality failed:`, error.message);
  failCount++;
}

// Test 2: Evolution
testSection('Evolution Tests');

try {
  const axiom = new UniversalAxiom({ n: 1 });
  axiom.evolve();
  const state = axiom.getState();
  assert(state.n === 2, 'evolve_system increments n');
  assert(state.cognitive.Z_time === 2.0, 'evolve_system updates time');
  assert(state.intelligence > 10.0, 'evolve_system increases intelligence');
} catch (error) {
  console.error(`${RED}✗${RESET} Evolution failed:`, error.message);
  failCount++;
}

// Test 3: Pressure application
testSection('Pressure Tests');

try {
  const axiom = new UniversalAxiom({ pressure: 1.0 });
  const initialPressure = axiom.foundation.pressure;
  axiom.applyPressure(2.0);
  assert(axiom.foundation.pressure > initialPressure, 'apply_pressure increases pressure');
} catch (error) {
  console.error(`${RED}✗${RESET} Pressure application failed:`, error.message);
  failCount++;
}

// Test 4: Subjectivity adjustment
testSection('Subjectivity Tests');

try {
  const axiom = new UniversalAxiom({ subjectivity: 0.5 });
  axiom.adjustSubjectivity(-0.2);
  const state = axiom.getState();
  assert(state.cognitive.X_subjectivity === 0.3, 'adjust_subjectivity changes subjectivity');
  assert(state.cognitive.X_objectivity === 0.7, 'objectivity changes inversely');
} catch (error) {
  console.error(`${RED}✗${RESET} Subjectivity adjustment failed:`, error.message);
  failCount++;
}

// Test 5: Simulator
testSection('Simulator Tests');

try {
  const axiom = new UniversalAxiom({
    impulses: 1.0,
    elements: 1.0,
    pressure: 1.0,
    subjectivity: 0.3,
    purpose: 1.0,
    time: 1.0,
    n: 1
  });
  const simulator = new AxiomSimulator(axiom);

  assert(simulator !== null, 'AxiomSimulator instantiation');

  const history = simulator.simulateEvolution(5);
  assert(history.length === 6, `simulate_evolution returns correct history length (expected 6, got ${history.length})`);
  assert(history[0].n === 1, 'History starts at n=1');
  assert(history[5].n === 6, 'History ends at n=6');

  const coherence = simulator.getCoherenceMetric();
  assert(coherence > 0 && coherence <= 1, `get_coherence_metric returns valid value (${coherence})`);
} catch (error) {
  console.error(`${RED}✗${RESET} Simulator failed:`, error.message);
  failCount++;
}

// Test 6: Contradiction resolution
testSection('Contradiction Resolution Tests');

try {
  const axiom = new UniversalAxiom({
    subjectivity: 0.8,
    pressure: 3.0,
    n: 1
  });
  const simulator = new AxiomSimulator(axiom);

  const resolution = simulator.simulateContradictionResolution(2.0, 5);
  const finalState = resolution[resolution.length - 1];

  assert(resolution.length >= 5, 'Contradiction resolution returns history');
  assert(finalState.cognitive.X_subjectivity < 0.8, 'Contradiction resolution reduces subjectivity');
} catch (error) {
  console.error(`${RED}✗${RESET} Contradiction resolution failed:`, error.message);
  failCount++;
}

// Test 7: Multiple permutations
testSection('Permutation Comparison Tests');

try {
  const axiom1 = new UniversalAxiom({ impulses: 1.0, elements: 1.0, n: 1 });
  const axiom2 = new UniversalAxiom({ impulses: 2.0, elements: 1.5, n: 1 });

  const intel1 = axiom1.computeIntelligence();
  const intel2 = axiom2.computeIntelligence();

  assert(intel2 > intel1, `compare_permutations: Higher foundation produces higher intelligence (${intel2} > ${intel1})`);
} catch (error) {
  console.error(`${RED}✗${RESET} Permutation comparison failed:`, error.message);
  failCount++;
}

// Test 8: Edge cases
testSection('Edge Case Tests');

try {
  // Zero foundation should produce zero intelligence
  const zeroAxiom = new UniversalAxiom({ impulses: 0, n: 1 });
  assert(zeroAxiom.computeIntelligence() === 0, 'Zero impulses produces zero intelligence');

  // Negative impulses should produce negative intelligence
  const negativeAxiom = new UniversalAxiom({ impulses: -1.0, n: 1 });
  assert(negativeAxiom.computeIntelligence() < 0, 'Negative impulses produces negative intelligence');

  // Complete subjectivity should produce zero intelligence
  const subjectiveAxiom = new UniversalAxiom({ subjectivity: 1.0, n: 1 });
  assert(subjectiveAxiom.computeIntelligence() === 0, 'Complete subjectivity (X=0) produces zero intelligence');
} catch (error) {
  console.error(`${RED}✗${RESET} Edge case tests failed:`, error.message);
  failCount++;
}

// Test 9: Large n values
testSection('Scaling Tests');

try {
  const axiom = new UniversalAxiom({ n: 10 });
  const intelligence = axiom.computeIntelligence();

  assert(intelligence > 0, `Large n values work correctly (n=10, intelligence=${intelligence})`);
  assert(Number.isFinite(intelligence), 'Intelligence remains finite at n=10');
} catch (error) {
  console.error(`${RED}✗${RESET} Scaling tests failed:`, error.message);
  failCount++;
}

// Test 10: Validation and clamping
testSection('Validation Tests');

try {
  // Test subjectivity clamping via adjustSubjectivity method
  const axiom = new UniversalAxiom({ subjectivity: 0.8, n: 1 });
  axiom.adjustSubjectivity(0.5); // Try to set to 1.3
  const state = axiom.getState();
  assert(state.cognitive.X_subjectivity <= 1.0, 'Subjectivity is clamped to max 1.0');

  const axiom2 = new UniversalAxiom({ subjectivity: 0.2, n: 1 });
  axiom2.adjustSubjectivity(-0.5); // Try to set to -0.3
  const state2 = axiom2.getState();
  assert(state2.cognitive.X_subjectivity >= 0.0, 'Subjectivity is clamped to min 0.0');

  const axiom3 = new UniversalAxiom({ pressure: 1.0, n: 1 });
  axiom3.applyPressure(-5.0); // Try to set to -4.0
  assert(axiom3.foundation.pressure >= 0.01, 'Pressure is clamped to minimum 0.01');
} catch (error) {
  console.error(`${RED}✗${RESET} Validation tests failed:`, error.message);
  failCount++;
}

// Summary
console.log(`\n${BLUE}=== Test Summary ===${RESET}`);
console.log(`${GREEN}Passed: ${passCount}${RESET}`);
console.log(`${RED}Failed: ${failCount}${RESET}`);
console.log(`Total: ${passCount + failCount}`);

if (failCount === 0) {
  console.log(`\n${GREEN}✓ All MCP server tools are working correctly!${RESET}`);
  process.exit(0);
} else {
  console.log(`\n${RED}✗ Some tests failed. Please review the implementation.${RESET}`);
  process.exit(1);
}
