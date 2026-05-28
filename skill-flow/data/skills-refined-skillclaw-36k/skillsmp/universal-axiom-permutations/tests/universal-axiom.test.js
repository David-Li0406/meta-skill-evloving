/**
 * Test suite for The Universal Axiom (JavaScript)
 * Tests the core formula: Intelligence_n = E_n⋅(1+F_n)⋅X⋅Y⋅Z⋅(A⋅B⋅C)
 * Based on PROMPT.md principles and The Epiphany Engine specifications
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

import { UniversalAxiom, AxiomSimulator, MathSolutions, fibonacciSequence } from '../dist/javascript/universal-axiom.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

describe('Foundation Layer (A·B·C)', () => {
  test('initializes with correct values', () => {
    const axiom = new UniversalAxiom({ impulses: 2.0, elements: 3.0, pressure: 1.5 });
    const state = axiom.getState();

    expect(state.foundation.A_impulses).toBe(2.0);
    expect(state.foundation.B_elements).toBe(3.0);
    expect(state.foundation.C_pressure).toBe(1.5);
  });

  test('computes A·B·C product correctly', () => {
    const axiom = new UniversalAxiom({ impulses: 2.0, elements: 3.0, pressure: 1.5 });
    const state = axiom.getState();

    expect(state.foundation.product).toBe(2.0 * 3.0 * 1.5);
  });
});

describe('Dynamic Layer (E_n·(1+F_n))', () => {
  test('generates Fibonacci sequence per PROMPT.md', () => {
    const sequence = fibonacciSequence(12);
    const expected = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144];

    expect(sequence).toEqual(expected);
  });

  test('computes Fibonacci at specific n values', () => {
    const axiom1 = new UniversalAxiom({ n: 1 });
    const axiom10 = new UniversalAxiom({ n: 10 });

    expect(axiom1.getState().dynamic.F_n).toBe(1);
    expect(axiom10.getState().dynamic.F_n).toBe(89);
  });

  test('computes exponential growth E_n', () => {
    const axiom = new UniversalAxiom({ n: 1 });
    const state = axiom.getState();

    expect(state.dynamic.E_n).toBe(5);
  });

  test('computes E_n·(1+F_n) product', () => {
    const axiom = new UniversalAxiom({ n: 1 });
    const state = axiom.getState();

    const E_n = 5;
    const F_n = 1;
    const expected = E_n * (1 + F_n);

    expect(state.dynamic.product).toBeCloseTo(expected, 6);
  });
});

describe('Cognitive Layer (X·Y·Z)', () => {
  test('relates subjectivity and objectivity per PROMPT.md', () => {
    const axiom = new UniversalAxiom({ subjectivity: 0.3 });
    const state = axiom.getState();

    expect(state.cognitive.X_subjectivity).toBe(0.3);
    expect(state.cognitive.X_objectivity).toBe(0.7);
  });

  test('computes X·Y·Z product', () => {
    const axiom = new UniversalAxiom({ subjectivity: 0.2, purpose: 1.5, time: 2.0 });
    const state = axiom.getState();

    const expected = 0.8 * 1.5 * 2.0; // objectivity * purpose * time
    expect(state.cognitive.product).toBe(expected);
  });
});

describe('Universal Axiom Core Formula', () => {
  test('initializes with all layers', () => {
    const axiom = new UniversalAxiom();
    const state = axiom.getState();

    expect(state.foundation).toBeDefined();
    expect(state.dynamic).toBeDefined();
    expect(state.cognitive).toBeDefined();
    expect(state.n).toBe(1);
  });

  test('computes Intelligence_n = E_n⋅(1+F_n)⋅X⋅Y⋅Z⋅(A⋅B⋅C)', () => {
    const axiom = new UniversalAxiom({ impulses: 1.0, elements: 1.0, pressure: 1.0, n: 1 });

    // Manual calculation per PROMPT.md
    const A_B_C = 1.0 * 1.0 * 1.0;
    const E_n = 5;
    const F_n = 1;
    const E_F = E_n * (1 + F_n);
    const X_Y_Z = 1.0 * 1.0 * 1.0;
    const expected = E_F * X_Y_Z * A_B_C;

    const intelligence = axiom.computeIntelligence();
    expect(intelligence).toBeCloseTo(expected, 6);
  });

  test('matches TEST_RESULTS.md value at n=1', () => {
    const axiom = new UniversalAxiom({ n: 1 });
    const intelligence = axiom.computeIntelligence();

    expect(intelligence).toBeCloseTo(10.0, 3);
  });

  test('matches TEST_RESULTS.md value at n=10', () => {
    const axiom = new UniversalAxiom({ n: 1 });
    for (let i = 0; i < 9; i++) {
      axiom.evolve();
    }

    const intelligence = axiom.computeIntelligence();
    expect(intelligence).toBe(106287300);
  });

  test('evolution increases intelligence per PROMPT.md', () => {
    const axiom = new UniversalAxiom({ n: 1 });
    const intelligenceBefore = axiom.computeIntelligence();

    axiom.evolve();
    const intelligenceAfter = axiom.computeIntelligence();

    expect(intelligenceAfter).toBeGreaterThan(intelligenceBefore);
  });

  test('pressure application affects foundation layer', () => {
    const axiom = new UniversalAxiom({ pressure: 1.0 });
    const intelligenceBefore = axiom.computeIntelligence();

    axiom.applyPressure(1.0);
    const intelligenceAfter = axiom.computeIntelligence();

    expect(intelligenceAfter).toBeGreaterThan(intelligenceBefore);
  });

  test('pressure is clamped to minimum 0.01', () => {
    const axiom = new UniversalAxiom({ pressure: 1.0 });
    axiom.applyPressure(-10.0);

    const state = axiom.getState();
    expect(state.foundation.C_pressure).toBe(0.01);
  });

  test('adjusting subjectivity changes objectivity', () => {
    const axiom = new UniversalAxiom({ subjectivity: 0.5 });
    const intelligenceBefore = axiom.computeIntelligence();

    axiom.adjustSubjectivity(-0.2);
    const intelligenceAfter = axiom.computeIntelligence();
    const state = axiom.getState();

    expect(intelligenceAfter).toBeGreaterThan(intelligenceBefore);
    expect(state.cognitive.X_subjectivity).toBe(0.3);
  });

  test('subjectivity is clamped to [0.0, 1.0]', () => {
    const axiom = new UniversalAxiom({ subjectivity: 0.5 });

    axiom.adjustSubjectivity(1.0);
    expect(axiom.getState().cognitive.X_subjectivity).toBe(1.0);

    axiom.adjustSubjectivity(-2.0);
    expect(axiom.getState().cognitive.X_subjectivity).toBe(0.0);
  });

  test('strengthening purpose uses multiplier', () => {
    const axiom = new UniversalAxiom({ purpose: 1.0 });
    const intelligenceBefore = axiom.computeIntelligence();

    axiom.strengthenPurpose(1.5);
    const state = axiom.getState();
    const intelligenceAfter = axiom.computeIntelligence();

    expect(state.cognitive.Y_purpose).toBe(1.5);
    expect(intelligenceAfter).toBeGreaterThan(intelligenceBefore);
  });

  test('negative impulses produce negative intelligence', () => {
    const axiom = new UniversalAxiom({ impulses: -1.0 });
    const intelligence = axiom.computeIntelligence();

    expect(intelligence).toBeLessThan(0);
  });

  test('extreme subjectivity produces zero intelligence', () => {
    const axiom = new UniversalAxiom({ subjectivity: 1.0 });
    const intelligence = axiom.computeIntelligence();

    expect(intelligence).toBe(0.0);
  });

  test('extreme objectivity produces positive intelligence', () => {
    const axiom = new UniversalAxiom({ subjectivity: 0.0 });
    const intelligence = axiom.computeIntelligence();

    expect(intelligence).toBeGreaterThan(0);
  });
});

describe('AxiomSimulator', () => {
  test('initializes with axiom', () => {
    const axiom = new UniversalAxiom();
    const simulator = new AxiomSimulator(axiom);

    expect(simulator.axiom).toBe(axiom);
  });

  test('tracks evolution history', () => {
    const axiom = new UniversalAxiom({ n: 1 });
    const simulator = new AxiomSimulator(axiom);
    const history = simulator.simulateEvolution(5);

    expect(history.length).toBe(6); // initial + 5 steps
    expect(history[0].n).toBe(1);
    expect(history[5].n).toBe(6);
  });

  test('contradiction resolution reduces subjectivity per PROMPT.md', () => {
    const axiom = new UniversalAxiom({ subjectivity: 0.5, pressure: 1.0 });
    const simulator = new AxiomSimulator(axiom);

    const initialSubjectivity = axiom.cognitive.subjectivity;
    const history = simulator.simulateContradictionResolution(2.0, 5);

    const finalSubjectivity = history[history.length - 1].cognitive.X_subjectivity;
    expect(finalSubjectivity).toBeLessThan(initialSubjectivity);
  });

  test('high objectivity produces high coherence', () => {
    const axiom = new UniversalAxiom({ subjectivity: 0.1, purpose: 2.0, pressure: 1.0 });
    const simulator = new AxiomSimulator(axiom);
    const coherence = simulator.getCoherenceMetric();

    expect(coherence).toBeGreaterThan(0.8);
  });

  test('coherence decreases with subjectivity', () => {
    const axiomObjective = new UniversalAxiom({ subjectivity: 0.1 });
    const coherenceObjective = new AxiomSimulator(axiomObjective).getCoherenceMetric();

    const axiomSubjective = new UniversalAxiom({ subjectivity: 0.8 });
    const coherenceSubjective = new AxiomSimulator(axiomSubjective).getCoherenceMetric();

    expect(coherenceObjective).toBeGreaterThan(coherenceSubjective);
  });

  test('no stagnation with evolution', () => {
    const axiom = new UniversalAxiom({ n: 1 });
    const simulator = new AxiomSimulator(axiom);
    const history = simulator.simulateEvolution(10);

    const intelligences = history.map(state => state.intelligence);

    // Verify monotonic increase
    for (let i = 1; i < intelligences.length; i++) {
      expect(intelligences[i]).toBeGreaterThan(intelligences[i - 1]);
    }
  });
});

describe('Golden Cases Parity', () => {
  test('matches expected intelligence values', () => {
    const goldenPath = path.join(__dirname, 'golden_cases.csv');
    const lines = fs.readFileSync(goldenPath, 'utf-8').trim().split('\n');
    const [, ...rows] = lines;

    rows.forEach((row) => {
      const [
        name,
        impulses,
        elements,
        pressure,
        subjectivity,
        purpose,
        time,
        n,
        expectedIntelligence
      ] = row.split(',');

      const axiom = new UniversalAxiom({
        impulses: Number(impulses),
        elements: Number(elements),
        pressure: Number(pressure),
        subjectivity: Number(subjectivity),
        purpose: Number(purpose),
        time: Number(time),
        n: Number(n)
      });

      const actual = axiom.computeIntelligence();
      expect(actual).toBeCloseTo(Number(expectedIntelligence), 6);
      expect(actual).not.toBeNaN();
      expect(name).toBeTruthy();
    });
  });
});

describe('PROMPT.md Compliance', () => {
  test('axiom is deterministic - mirrors physics laws', () => {
    const axiom1 = new UniversalAxiom({ n: 5, impulses: 1.0, elements: 1.0 });
    const axiom2 = new UniversalAxiom({ n: 5, impulses: 1.0, elements: 1.0 });

    expect(axiom1.computeIntelligence()).toBe(axiom2.computeIntelligence());
  });

  test('Fibonacci sequence regulates system dynamics', () => {
    const axiom = new UniversalAxiom({ n: 1 });
    const simulator = new AxiomSimulator(axiom);
    const history = simulator.simulateEvolution(10);

    // Extract first 10 fibonacci values from evolution history
    const fibValues = history.slice(0, 10).map(state => state.dynamic.F_n);
    const expected = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89];

    expect(fibValues).toEqual(expected);
  });

  test('pressure reveals contradictions', () => {
    const axiom = new UniversalAxiom({ subjectivity: 0.5, pressure: 1.0 });

    axiom.applyPressure(2.0);
    const state = axiom.getState();

    expect(state.foundation.C_pressure).toBe(3.0);
  });

  test('TimeSphere advances over time', () => {
    const axiom = new UniversalAxiom({ time: 1.0 });
    const simulator = new AxiomSimulator(axiom);
    const history = simulator.simulateEvolution(5);

    const times = history.map(state => state.cognitive.Z_time);
    expect(times).toEqual([1.0, 2.0, 3.0, 4.0, 5.0, 6.0]);
  });

  test('Foundation Layer ABC variables per PROMPT.md', () => {
    const axiom = new UniversalAxiom({ impulses: 2.0, elements: 3.0, pressure: 1.5 });
    const state = axiom.getState();

    // A = Impulses (Current)
    expect(state.foundation.A_impulses).toBe(2.0);

    // B = Elements (Energy, Matter, State)
    expect(state.foundation.B_elements).toBe(3.0);

    // C = Pressure (Direction, Momentum, Integrity)
    expect(state.foundation.C_pressure).toBe(1.5);

    // Product = A·B·C
    expect(state.foundation.product).toBe(2.0 * 3.0 * 1.5);
  });

  test('Cognitive Layer XYZ variables per PROMPT.md', () => {
    const axiom = new UniversalAxiom({ subjectivity: 0.3, purpose: 1.5, time: 2.0 });
    const state = axiom.getState();

    // X = subjectivity scaling aggregate
    expect(state.cognitive.X_subjectivity).toBe(0.3);
    expect(state.cognitive.X_objectivity).toBe(0.7);

    // Y = The Why Axis scale (purpose)
    expect(state.cognitive.Y_purpose).toBe(1.5);

    // Z = flux of Time (TimeSphere)
    expect(state.cognitive.Z_time).toBe(2.0);
  });

  test('handles large n values with Fibonacci regulation', () => {
    const axiom = new UniversalAxiom({ n: 1 });
    for (let i = 0; i < 19; i++) {
      axiom.evolve();
    }

    const intelligence = axiom.computeIntelligence();
    expect(intelligence).toBeGreaterThan(0);
    expect(isFinite(intelligence)).toBe(true);
  });
});

describe('MathSolutions (Erdos problems)', () => {
  test('seeded Erdos problem is available', () => {
    const solutions = MathSolutions.erdosSeed();
    const expected = {
      'erdos-straus': 'open',
      'erdos-distinct-distances': 'solved',
      'erdos-moser': 'partial',
      'erdos-ko-rado': 'solved',
      'erdos-szekeres': 'partial',
      'erdos-faber-lovasz': 'solved',
      'erdos-ginzburg-ziv': 'solved',
      'erdos-heilbronn': 'solved',
      'erdos-discrepancy': 'solved',
    };

    expect(solutions.listProblems()).toHaveLength(Object.keys(expected).length);

    Object.entries(expected).forEach(([identifier, status]) => {
      const problem = solutions.getProblem(identifier);
      expect(problem.status).toBe(status);
      expect(problem.proofSteps).toHaveLength(5);
    });
  });

  test('adds proof steps with axiom insights', () => {
    const solutions = MathSolutions.erdosSeed();
    solutions.addProofStep(
      'erdos-straus',
      'Normalize the equation to isolate reciprocal structure.',
      "Use the axiom's foundation layer (A·B·C) to align constraints."
    );

    const problem = solutions.getProblem('erdos-straus');
    expect(problem.proofSteps).toHaveLength(6);
    expect(problem.proofSteps[5].statement).toContain('Normalize the equation');
  });
});
