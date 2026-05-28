// Type definitions for Universal Axiom (imported from parent project)

export interface FoundationState {
  impulses: number;
  elements: number;
  pressure: number;
}

export interface DynamicState {
  n: number;
  baseExponential: number;
}

export interface CognitiveState {
  subjectivity: number;
  purpose: number;
  time: number;
}

export interface AxiomState {
  n: number;
  foundation: {
    A_impulses: number;
    B_elements: number;
    C_pressure: number;
    product: number;
  };
  dynamic: {
    E_n: number;
    F_n: number;
    product: number;
  };
  cognitive: {
    X_subjectivity: number;
    X_objectivity: number;
    Y_purpose: number;
    Z_time: number;
    product: number;
  };
  intelligence: number;
}

export class FoundationLayer {
  constructor(impulses: number, elements: number, pressure: number);
  impulses: number;
  elements: number;
  pressure: number;
  compute(): number;
}

export class DynamicLayer {
  constructor(n: number, baseExponential?: number);
  n: number;
  baseExponential: number;
  exponentialGrowth(): number;
  fibonacci(): number;
  compute(): number;
}

export class CognitiveLayer {
  constructor(subjectivity: number, purpose: number, time: number);
  subjectivity: number;
  purpose: number;
  time: number;
  compute(): number;
}

export class UniversalAxiom {
  constructor(params?: Partial<FoundationState & CognitiveState & { n: number }>);
  foundation: FoundationLayer;
  dynamic: DynamicLayer;
  cognitive: CognitiveLayer;
  n: number;
  computeIntelligence(): number;
  evolve(deltaTime?: number): number;
  applyPressure(pressureDelta: number): number;
  adjustSubjectivity(subjectivityDelta: number): number;
  strengthenPurpose(purposeMultiplier: number): number;
  getState(): AxiomState;
  toString(): string;
}

export class AxiomSimulator {
  constructor(axiom: UniversalAxiom);
  recordState(): void;
  simulateEvolution(steps?: number, deltaTime?: number): AxiomState[];
  simulateContradictionResolution(initialPressure?: number, resolutionSteps?: number): AxiomState[];
  getCoherenceMetric(): number;
  getHistory(): AxiomState[];
}

export function fibonacciSequence(n: number): number[];
