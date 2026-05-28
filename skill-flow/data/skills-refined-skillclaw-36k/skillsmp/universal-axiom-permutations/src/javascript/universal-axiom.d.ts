/**
 * The Universal Axiom - Core Implementation (TypeScript)
 *
 * Intelligence_n = E_n · (1 + F_n) · X · Y · Z · (A · B · C)
 *
 * Foundation Layer: Impulses (A), Elements (B), Pressure (C)
 * Dynamic Layer: Exponential Growth (E_n), Fibonacci Sequence (F_n)
 * Cognitive Layer: Subjectivity Scale (X), Why Axis (Y), TimeSphere (Z)
 */
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
/**
 * Foundation Layer: A · B · C
 */
export declare class FoundationLayer {
    impulses: number;
    elements: number;
    pressure: number;
    constructor(impulses: number, elements: number, pressure: number);
    compute(): number;
}
/**
 * Dynamic Layer: E_n · (1 + F_n)
 */
export declare class DynamicLayer {
    n: number;
    baseExponential: number;
    constructor(n: number, baseExponential?: number);
    exponentialGrowth(): number;
    fibonacci(): number;
    compute(): number;
}
/**
 * Cognitive Layer: X · Y · Z
 */
export declare class CognitiveLayer {
    subjectivity: number;
    purpose: number;
    time: number;
    constructor(subjectivity: number, // 0-1 scale
    purpose: number, time: number);
    compute(): number;
}
/**
 * The Universal Axiom - Complete Intelligence Model
 *
 * Intelligence_n = E_n · (1 + F_n) · X · Y · Z · (A · B · C)
 */
export declare class UniversalAxiom {
    foundation: FoundationLayer;
    dynamic: DynamicLayer;
    cognitive: CognitiveLayer;
    n: number;
    constructor({ impulses, elements, pressure, subjectivity, purpose, time, n }?: Partial<FoundationState & CognitiveState & {
        n: number;
    }>);
    /**
     * Compute Intelligence_n = E_n · (1 + F_n) · X · Y · Z · (A · B · C)
     */
    computeIntelligence(): number;
    /**
     * Evolve the system forward in time
     */
    evolve(deltaTime?: number): number;
    /**
     * Apply pressure change (e.g., from contradictions or constraints)
     */
    applyPressure(pressureDelta: number): number;
    /**
     * Adjust subjectivity level (moving toward objectivity or away)
     */
    adjustSubjectivity(subjectivityDelta: number): number;
    /**
     * Strengthen or weaken purpose alignment
     */
    strengthenPurpose(purposeMultiplier: number): number;
    /**
     * Get current state of all variables
     */
    getState(): AxiomState;
    toString(): string;
}
/**
 * Simulator for running Universal Axiom scenarios
 */
export declare class AxiomSimulator {
    private axiom;
    private history;
    constructor(axiom: UniversalAxiom);
    recordState(): void;
    /**
     * Simulate evolution over multiple time steps
     */
    simulateEvolution(steps?: number, deltaTime?: number): AxiomState[];
    /**
     * Simulate how the system handles contradiction
     */
    simulateContradictionResolution(initialPressure?: number, resolutionSteps?: number): AxiomState[];
    /**
     * Calculate coherence metric based on balance of components
     */
    getCoherenceMetric(): number;
    getHistory(): AxiomState[];
}
/**
 * Generate Fibonacci sequence up to n terms
 */
export declare function fibonacciSequence(n: number): number[];
export type ProblemStatus = 'open' | 'solved' | 'partial';
export declare class ProofStep {
    statement: string;
    axiomInsight: string;
    constructor(statement: string, axiomInsight: string);
    toJSON(): {
        statement: string;
        axiom_insight: string;
    };
}
export declare class ErdosProblem {
    identifier: string;
    title: string;
    statement: string;
    status: ProblemStatus;
    axiomInsight: string;
    proofSteps: ProofStep[];
    constructor(identifier: string, title: string, statement: string, status: ProblemStatus, axiomInsight: string, proofSteps?: ProofStep[]);
    addProofStep(statement: string, axiomInsight: string): void;
    addProofSteps(steps: ProofStep[]): void;
    toJSON(): {
        identifier: string;
        title: string;
        statement: string;
        status: ProblemStatus;
        axiom_insight: string;
        proof_steps: {
            statement: string;
            axiom_insight: string;
        }[];
    };
}
export declare class MathSolutions {
    private problems;
    constructor(problems?: ErdosProblem[]);
    static erdosSeed(): MathSolutions;
    addProblem(problem: ErdosProblem): void;
    getProblem(identifier: string): ErdosProblem;
    listProblems(): ErdosProblem[];
    addProofStep(identifier: string, statement: string, axiomInsight: string): void;
    summaries(): {
        identifier: string;
        title: string;
        status: ProblemStatus;
    }[];
}
//# sourceMappingURL=universal-axiom.d.ts.map
