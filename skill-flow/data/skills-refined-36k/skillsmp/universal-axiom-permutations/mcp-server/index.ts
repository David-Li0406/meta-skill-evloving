#!/usr/bin/env node

/**
 * MCP Server for The Universal Axiom
 *
 * Exposes The Universal Axiom framework as tools and resources
 * for AI assistants via the Model Context Protocol.
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListResourcesRequestSchema,
  ListToolsRequestSchema,
  ReadResourceRequestSchema,
  ListPromptsRequestSchema,
  GetPromptRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

import {
  UniversalAxiom,
  AxiomSimulator,
  AxiomState,
} from "./universal-axiom.js";

/**
 * Rate Limiting Module
 */
interface RateLimitConfig {
  maxRequestsPerMinute: number;
  maxRequestsPerHour: number;
}

class RateLimiter {
  private requestTimestamps: Map<string, number[]> = new Map();
  private config: RateLimitConfig;

  constructor(config: RateLimitConfig = {
    maxRequestsPerMinute: 60,
    maxRequestsPerHour: 1000,
  }) {
    this.config = config;
  }

  checkRateLimit(toolName: string): { allowed: boolean; reason?: string } {
    const now = Date.now();
    const timestamps = this.requestTimestamps.get(toolName) || [];

    // Remove timestamps older than 1 hour
    const recentTimestamps = timestamps.filter(ts => now - ts < 3600000);

    // Check hourly limit
    if (recentTimestamps.length >= this.config.maxRequestsPerHour) {
      return {
        allowed: false,
        reason: `Rate limit exceeded: Maximum ${this.config.maxRequestsPerHour} requests per hour for ${toolName}`,
      };
    }

    // Check per-minute limit
    const lastMinuteTimestamps = recentTimestamps.filter(ts => now - ts < 60000);
    if (lastMinuteTimestamps.length >= this.config.maxRequestsPerMinute) {
      return {
        allowed: false,
        reason: `Rate limit exceeded: Maximum ${this.config.maxRequestsPerMinute} requests per minute for ${toolName}`,
      };
    }

    // Record this request
    recentTimestamps.push(now);
    this.requestTimestamps.set(toolName, recentTimestamps);

    return { allowed: true };
  }

  getStats(toolName: string): {
    requestsLastMinute: number;
    requestsLastHour: number;
  } {
    const now = Date.now();
    const timestamps = this.requestTimestamps.get(toolName) || [];

    return {
      requestsLastMinute: timestamps.filter(ts => now - ts < 60000).length,
      requestsLastHour: timestamps.filter(ts => now - ts < 3600000).length,
    };
  }
}

const rateLimiter = new RateLimiter();

/**
 * Input Validation Module
 */
interface ValidationResult {
  valid: boolean;
  errors: string[];
}

function validateNumber(
  value: any,
  name: string,
  options: {
    required?: boolean;
    min?: number;
    max?: number;
    integer?: boolean;
  } = {}
): ValidationResult {
  const errors: string[] = [];

  // Check if value exists
  if (value === undefined || value === null) {
    if (options.required) {
      errors.push(`${name} is required`);
    }
    return { valid: errors.length === 0, errors };
  }

  // Check type
  if (typeof value !== "number") {
    errors.push(`${name} must be a number, got ${typeof value}`);
    return { valid: false, errors };
  }

  // Check for NaN and Infinity
  if (isNaN(value)) {
    errors.push(`${name} cannot be NaN`);
  }
  if (!isFinite(value)) {
    errors.push(`${name} must be finite (not Infinity or -Infinity)`);
  }

  // Check integer constraint
  if (options.integer && !Number.isInteger(value)) {
    errors.push(`${name} must be an integer, got ${value}`);
  }

  // Check range
  if (options.min !== undefined && value < options.min) {
    errors.push(`${name} must be >= ${options.min}, got ${value}`);
  }
  if (options.max !== undefined && value > options.max) {
    errors.push(`${name} must be <= ${options.max}, got ${value}`);
  }

  return { valid: errors.length === 0, errors };
}

function validateAxiomParams(params: any): ValidationResult {
  const allErrors: string[] = [];

  // Validate each parameter
  const validations = [
    validateNumber(params.impulses, "impulses", {}),
    validateNumber(params.elements, "elements", {}),
    validateNumber(params.pressure, "pressure", { min: 0.01 }),
    validateNumber(params.subjectivity, "subjectivity", { min: 0, max: 1 }),
    validateNumber(params.purpose, "purpose", { min: 0.01 }),
    validateNumber(params.time, "time", { min: 0 }),
    validateNumber(params.n, "n", { integer: true, min: 1 }),
  ];

  validations.forEach(v => {
    if (!v.valid) {
      allErrors.push(...v.errors);
    }
  });

  return { valid: allErrors.length === 0, errors: allErrors };
}

function validateState(state: any): ValidationResult {
  const errors: string[] = [];

  if (!state || typeof state !== "object") {
    errors.push("current_state must be a valid object");
    return { valid: false, errors };
  }

  // Check required properties
  if (!state.foundation || typeof state.foundation !== "object") {
    errors.push("current_state.foundation is required and must be an object");
  }
  if (!state.dynamic || typeof state.dynamic !== "object") {
    errors.push("current_state.dynamic is required and must be an object");
  }
  if (!state.cognitive || typeof state.cognitive !== "object") {
    errors.push("current_state.cognitive is required and must be an object");
  }
  if (typeof state.n !== "number") {
    errors.push("current_state.n is required and must be a number");
  }

  return { valid: errors.length === 0, errors };
}

function validateToolInput(toolName: string, args: any): ValidationResult {
  const allErrors: string[] = [];

  switch (toolName) {
    case "compute_intelligence":
    case "simulate_evolution":
    case "simulate_contradiction_resolution":
    case "analyze_permutation": {
      const validation = validateAxiomParams(args || {});
      if (!validation.valid) {
        allErrors.push(...validation.errors);
      }
      break;
    }

    case "evolve_system": {
      const stateValidation = validateState(args.current_state);
      if (!stateValidation.valid) {
        allErrors.push(...stateValidation.errors);
      }
      const stepsValidation = validateNumber(args.steps, "steps", {
        integer: true,
        min: 1,
        max: 1000,
      });
      if (!stepsValidation.valid) {
        allErrors.push(...stepsValidation.errors);
      }
      const deltaValidation = validateNumber(args.delta_time, "delta_time", {
        min: 0.001,
        max: 100,
      });
      if (!deltaValidation.valid) {
        allErrors.push(...deltaValidation.errors);
      }
      break;
    }

    case "apply_pressure": {
      const stateValidation = validateState(args.current_state);
      if (!stateValidation.valid) {
        allErrors.push(...stateValidation.errors);
      }
      const deltaValidation = validateNumber(args.pressure_delta, "pressure_delta", {
        required: true,
        min: -100,
        max: 100,
      });
      if (!deltaValidation.valid) {
        allErrors.push(...deltaValidation.errors);
      }
      break;
    }

    case "adjust_subjectivity": {
      const stateValidation = validateState(args.current_state);
      if (!stateValidation.valid) {
        allErrors.push(...stateValidation.errors);
      }
      const deltaValidation = validateNumber(args.subjectivity_delta, "subjectivity_delta", {
        required: true,
        min: -1,
        max: 1,
      });
      if (!deltaValidation.valid) {
        allErrors.push(...deltaValidation.errors);
      }
      break;
    }

    case "get_coherence_metric": {
      const stateValidation = validateState(args.current_state);
      if (!stateValidation.valid) {
        allErrors.push(...stateValidation.errors);
      }
      break;
    }

    case "compare_permutations": {
      if (!args.permutation_a || typeof args.permutation_a !== "object") {
        allErrors.push("permutation_a is required and must be an object");
      }
      if (!args.permutation_b || typeof args.permutation_b !== "object") {
        allErrors.push("permutation_b is required and must be an object");
      }
      break;
    }

    default:
      // Unknown tool - no specific validation
      break;
  }

  return { valid: allErrors.length === 0, errors: allErrors };
}

// Server instance
const server = new Server(
  {
    name: "universal-axiom-server",
    version: "0.2.1",
  },
  {
    capabilities: {
      tools: {},
      resources: {},
      prompts: {},
    },
  }
);

/**
 * List available tools
 */
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "compute_intelligence",
        description:
          "Compute intelligence value using The Universal Axiom formula: Intelligence_n = E_n · (1 + F_n) · X · Y · Z · (A · B · C)",
        inputSchema: {
          type: "object",
          properties: {
            impulses: {
              type: "number",
              description: "A - Fundamental drives (can be positive or negative)",
              default: 1.0,
            },
            elements: {
              type: "number",
              description: "B - Core components (beneficial or detrimental)",
              default: 1.0,
            },
            pressure: {
              type: "number",
              description: "C - Constraints and forces (constructive or destructive)",
              default: 1.0,
            },
            subjectivity: {
              type: "number",
              description: "X - Subjectivity level (0 = objective, 1 = subjective)",
              minimum: 0,
              maximum: 1,
              default: 0.0,
            },
            purpose: {
              type: "number",
              description: "Y - Purpose-driven reasoning strength (0 = unclear, 1+ = clear)",
              default: 1.0,
            },
            time: {
              type: "number",
              description: "Z - Temporal continuity and irreversibility",
              default: 1.0,
            },
            n: {
              type: "number",
              description: "Iteration level (affects exponential and Fibonacci components)",
              default: 1,
            },
          },
          required: [],
        },
      },
      {
        name: "evolve_system",
        description:
          "Evolve a Universal Axiom system forward in time, updating temporal and dynamic components",
        inputSchema: {
          type: "object",
          properties: {
            current_state: {
              type: "object",
              description: "Current state of the axiom system",
            },
            steps: {
              type: "number",
              description: "Number of time steps to evolve",
              default: 1,
            },
            delta_time: {
              type: "number",
              description: "Time increment per step",
              default: 1.0,
            },
          },
          required: ["current_state"],
        },
      },
      {
        name: "apply_pressure",
        description:
          "Apply pressure changes to the system (e.g., from contradictions, constraints, or new information)",
        inputSchema: {
          type: "object",
          properties: {
            current_state: {
              type: "object",
              description: "Current state of the axiom system",
            },
            pressure_delta: {
              type: "number",
              description: "Change in pressure (positive increases, negative decreases)",
            },
          },
          required: ["current_state", "pressure_delta"],
        },
      },
      {
        name: "adjust_subjectivity",
        description:
          "Adjust the subjectivity level of the system (move toward objectivity or subjectivity)",
        inputSchema: {
          type: "object",
          properties: {
            current_state: {
              type: "object",
              description: "Current state of the axiom system",
            },
            subjectivity_delta: {
              type: "number",
              description: "Change in subjectivity (negative = more objective, positive = more subjective)",
            },
          },
          required: ["current_state", "subjectivity_delta"],
        },
      },
      {
        name: "simulate_evolution",
        description:
          "Simulate the evolution of a system over multiple time steps, tracking state changes",
        inputSchema: {
          type: "object",
          properties: {
            impulses: { type: "number", default: 1.0 },
            elements: { type: "number", default: 1.0 },
            pressure: { type: "number", default: 1.0 },
            subjectivity: { type: "number", minimum: 0, maximum: 1, default: 0.0 },
            purpose: { type: "number", default: 1.0 },
            time: { type: "number", default: 1.0 },
            n: { type: "number", default: 1 },
            steps: {
              type: "number",
              description: "Number of evolution steps to simulate",
              default: 10,
            },
            delta_time: { type: "number", default: 1.0 },
          },
          required: [],
        },
      },
      {
        name: "simulate_contradiction_resolution",
        description:
          "Simulate how the system resolves contradiction through pressure application and objectivity adjustment",
        inputSchema: {
          type: "object",
          properties: {
            impulses: { type: "number", default: 1.0 },
            elements: { type: "number", default: 1.0 },
            pressure: { type: "number", default: 1.0 },
            subjectivity: { type: "number", minimum: 0, maximum: 1, default: 0.5 },
            purpose: { type: "number", default: 1.0 },
            time: { type: "number", default: 1.0 },
            n: { type: "number", default: 1 },
            initial_pressure: {
              type: "number",
              description: "Initial pressure spike from contradiction",
              default: 2.0,
            },
            resolution_steps: {
              type: "number",
              description: "Number of steps to resolve the contradiction",
              default: 5,
            },
          },
          required: [],
        },
      },
      {
        name: "get_coherence_metric",
        description:
          "Calculate the coherence metric of a system based on objectivity, purpose, and pressure balance",
        inputSchema: {
          type: "object",
          properties: {
            current_state: {
              type: "object",
              description: "Current state of the axiom system",
            },
          },
          required: ["current_state"],
        },
      },
      {
        name: "analyze_permutation",
        description:
          "Analyze a specific permutation (configuration) of the Universal Axiom to diagnose which layers may need adjustment",
        inputSchema: {
          type: "object",
          properties: {
            impulses: { type: "number", default: 1.0 },
            elements: { type: "number", default: 1.0 },
            pressure: { type: "number", default: 1.0 },
            subjectivity: { type: "number", minimum: 0, maximum: 1, default: 0.0 },
            purpose: { type: "number", default: 1.0 },
            time: { type: "number", default: 1.0 },
            n: { type: "number", default: 1 },
          },
          required: [],
        },
      },
      {
        name: "compare_permutations",
        description:
          "Compare two different system permutations to see which has higher intelligence and better alignment",
        inputSchema: {
          type: "object",
          properties: {
            permutation_a: {
              type: "object",
              description: "First permutation to compare (with impulses, elements, pressure, etc.)",
            },
            permutation_b: {
              type: "object",
              description: "Second permutation to compare",
            },
            comparison_criteria: {
              type: "array",
              description: "Criteria to compare: intelligence, coherence, foundation, cognitive, dynamic",
              default: ["intelligence", "coherence"],
            },
          },
          required: ["permutation_a", "permutation_b"],
        },
      },
      {
        name: "optimize_system",
        description:
          "Suggest optimal adjustments to system variables to improve intelligence and coherence",
        inputSchema: {
          type: "object",
          properties: {
            current_state: {
              type: "object",
              description: "Current state of the system",
            },
            optimization_goal: {
              type: "string",
              description: "Goal: maximize_intelligence, maximize_coherence, balance, reduce_subjectivity",
              default: "maximize_intelligence",
            },
            constraints: {
              type: "object",
              description: "Constraints on adjustments (e.g., max_pressure: 5.0)",
              default: {},
            },
          },
          required: ["current_state"],
        },
      },
      {
        name: "predict_trajectory",
        description:
          "Predict the future trajectory of a system over multiple iterations",
        inputSchema: {
          type: "object",
          properties: {
            impulses: { type: "number", default: 1.0 },
            elements: { type: "number", default: 1.0 },
            pressure: { type: "number", default: 1.0 },
            subjectivity: { type: "number", minimum: 0, maximum: 1, default: 0.0 },
            purpose: { type: "number", default: 1.0 },
            time: { type: "number", default: 1.0 },
            n: { type: "number", default: 1 },
            future_steps: {
              type: "number",
              description: "Number of future steps to predict",
              default: 10,
            },
            environmental_changes: {
              type: "object",
              description: "Changes to apply per step (e.g., pressure_per_step: 0.1)",
              default: {},
            },
          },
          required: [],
        },
      },
      {
        name: "detect_collapse_risk",
        description:
          "Analyze a system for collapse risk indicators and warning signs",
        inputSchema: {
          type: "object",
          properties: {
            current_state: {
              type: "object",
              description: "Current state of the system to analyze",
            },
            trajectory_history: {
              type: "array",
              description: "Optional historical states to detect trends",
              default: [],
            },
          },
          required: ["current_state"],
        },
      },
    ],
  };
});

/**
 * Handle tool execution
 */
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    // Check rate limit
    const rateLimitResult = rateLimiter.checkRateLimit(name);
    if (!rateLimitResult.allowed) {
      const stats = rateLimiter.getStats(name);
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(
              {
                error: "Rate limit exceeded",
                tool: name,
                reason: rateLimitResult.reason,
                stats: {
                  requestsLastMinute: stats.requestsLastMinute,
                  requestsLastHour: stats.requestsLastHour,
                },
                message: "Please wait before making additional requests",
              },
              null,
              2
            ),
          },
        ],
        isError: true,
      };
    }

    // Validate input parameters
    const validation = validateToolInput(name, args || {});
    if (!validation.valid) {
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(
              {
                error: "Input validation failed",
                tool: name,
                validationErrors: validation.errors,
                message: "Please check your input parameters and try again",
              },
              null,
              2
            ),
          },
        ],
        isError: true,
      };
    }

    switch (name) {
      case "compute_intelligence": {
        const axiom = new UniversalAxiom(args as any);
        const state = axiom.getState();

        return {
          content: [
            {
              type: "text",
              text: JSON.stringify(state, null, 2),
            },
          ],
        };
      }

      case "evolve_system": {
        const { current_state, steps = 1, delta_time = 1.0 } = args as any;
        const axiom = createAxiomFromState(current_state);

        const results: AxiomState[] = [];
        for (let i = 0; i < steps; i++) {
          axiom.evolve(delta_time);
          results.push(axiom.getState());
        }

        return {
          content: [
            {
              type: "text",
              text: JSON.stringify(
                {
                  steps: results.length,
                  evolution: results,
                  final_state: results[results.length - 1],
                },
                null,
                2
              ),
            },
          ],
        };
      }

      case "apply_pressure": {
        const { current_state, pressure_delta } = args as any;
        const axiom = createAxiomFromState(current_state);

        axiom.applyPressure(pressure_delta);
        const newState = axiom.getState();

        return {
          content: [
            {
              type: "text",
              text: JSON.stringify(
                {
                  pressure_applied: pressure_delta,
                  new_state: newState,
                },
                null,
                2
              ),
            },
          ],
        };
      }

      case "adjust_subjectivity": {
        const { current_state, subjectivity_delta } = args as any;
        const axiom = createAxiomFromState(current_state);

        axiom.adjustSubjectivity(subjectivity_delta);
        const newState = axiom.getState();

        return {
          content: [
            {
              type: "text",
              text: JSON.stringify(
                {
                  subjectivity_change: subjectivity_delta,
                  new_state: newState,
                },
                null,
                2
              ),
            },
          ],
        };
      }

      case "simulate_evolution": {
        const { steps = 10, delta_time = 1.0, ...params } = args as any;
        const axiom = new UniversalAxiom(params);
        const simulator = new AxiomSimulator(axiom);

        const history = simulator.simulateEvolution(steps, delta_time);

        return {
          content: [
            {
              type: "text",
              text: JSON.stringify(
                {
                  simulation_type: "evolution",
                  steps,
                  history,
                  final_intelligence: history[history.length - 1].intelligence,
                },
                null,
                2
              ),
            },
          ],
        };
      }

      case "simulate_contradiction_resolution": {
        const {
          initial_pressure = 2.0,
          resolution_steps = 5,
          ...params
        } = args as any;
        const axiom = new UniversalAxiom(params);
        const simulator = new AxiomSimulator(axiom);

        const history = simulator.simulateContradictionResolution(
          initial_pressure,
          resolution_steps
        );

        return {
          content: [
            {
              type: "text",
              text: JSON.stringify(
                {
                  simulation_type: "contradiction_resolution",
                  initial_pressure,
                  resolution_steps,
                  history,
                  coherence_improvement:
                    history[history.length - 1].cognitive.X_objectivity -
                    history[0].cognitive.X_objectivity,
                },
                null,
                2
              ),
            },
          ],
        };
      }

      case "get_coherence_metric": {
        const { current_state } = args as any;
        const axiom = createAxiomFromState(current_state);
        const simulator = new AxiomSimulator(axiom);

        const coherence = simulator.getCoherenceMetric();

        return {
          content: [
            {
              type: "text",
              text: JSON.stringify(
                {
                  coherence,
                  interpretation:
                    coherence > 0.7
                      ? "High coherence - system is well-aligned"
                      : coherence > 0.4
                      ? "Moderate coherence - some adjustment needed"
                      : "Low coherence - significant realignment required",
                  state: current_state,
                },
                null,
                2
              ),
            },
          ],
        };
      }

      case "analyze_permutation": {
        const axiom = new UniversalAxiom(args as any);
        const state = axiom.getState();
        const simulator = new AxiomSimulator(axiom);
        const coherence = simulator.getCoherenceMetric();

        // Diagnostic analysis
        const diagnostics = {
          foundation_layer: {
            status: state.foundation.product > 0 ? "positive" : "negative_or_zero",
            A_impulses: state.foundation.A_impulses,
            B_elements: state.foundation.B_elements,
            C_pressure: state.foundation.C_pressure,
            product: state.foundation.product,
            notes:
              state.foundation.product <= 0
                ? "⚠️ Foundation is weak or negative - check impulses, elements, and pressure"
                : state.foundation.C_pressure > 3
                ? "⚠️ High pressure detected - may indicate stress or contradiction"
                : "✓ Foundation is stable",
          },
          dynamic_layer: {
            E_n: state.dynamic.E_n,
            F_n: state.dynamic.F_n,
            product: state.dynamic.product,
            growth_rate: state.dynamic.E_n / (1 + state.dynamic.F_n),
            notes:
              state.n < 3
                ? "ℹ️ Early iteration - growth potential not yet fully realized"
                : "✓ Dynamic scaling active",
          },
          cognitive_layer: {
            objectivity: state.cognitive.X_objectivity,
            subjectivity: state.cognitive.X_subjectivity,
            purpose: state.cognitive.Y_purpose,
            time: state.cognitive.Z_time,
            product: state.cognitive.product,
            notes:
              state.cognitive.X_subjectivity > 0.7
                ? "⚠️ High subjectivity - increase objectivity for better coherence"
                : state.cognitive.Y_purpose < 0.3
                ? "⚠️ Low purpose alignment - clarify goals and direction"
                : "✓ Cognitive layer is balanced",
          },
          overall: {
            intelligence: state.intelligence,
            coherence,
            coherence_status:
              coherence > 0.7 ? "high" : coherence > 0.4 ? "moderate" : "low",
            recommendations: generateRecommendations(state, coherence),
          },
        };

        return {
          content: [
            {
              type: "text",
              text: JSON.stringify(diagnostics, null, 2),
            },
          ],
        };
      }

      case "compare_permutations": {
        const { permutation_a, permutation_b, comparison_criteria = ["intelligence", "coherence"] } = args as any;

        const axiomA = new UniversalAxiom(permutation_a);
        const axiomB = new UniversalAxiom(permutation_b);
        const stateA = axiomA.getState();
        const stateB = axiomB.getState();
        const simA = new AxiomSimulator(axiomA);
        const simB = new AxiomSimulator(axiomB);
        const coherenceA = simA.getCoherenceMetric();
        const coherenceB = simB.getCoherenceMetric();

        const comparison: any = {
          permutation_a: stateA,
          permutation_b: stateB,
          comparison: {},
          winner: {},
        };

        if (comparison_criteria.includes("intelligence")) {
          comparison.comparison.intelligence = {
            permutation_a: stateA.intelligence,
            permutation_b: stateB.intelligence,
            difference: stateA.intelligence - stateB.intelligence,
            winner: stateA.intelligence > stateB.intelligence ? "A" : stateB.intelligence > stateA.intelligence ? "B" : "TIE",
          };
        }

        if (comparison_criteria.includes("coherence")) {
          comparison.comparison.coherence = {
            permutation_a: coherenceA,
            permutation_b: coherenceB,
            difference: coherenceA - coherenceB,
            winner: coherenceA > coherenceB ? "A" : coherenceB > coherenceA ? "B" : "TIE",
          };
        }

        if (comparison_criteria.includes("foundation")) {
          comparison.comparison.foundation = {
            permutation_a: stateA.foundation.product,
            permutation_b: stateB.foundation.product,
            difference: stateA.foundation.product - stateB.foundation.product,
            winner: stateA.foundation.product > stateB.foundation.product ? "A" : stateB.foundation.product > stateA.foundation.product ? "B" : "TIE",
          };
        }

        if (comparison_criteria.includes("cognitive")) {
          comparison.comparison.cognitive = {
            permutation_a: stateA.cognitive.product,
            permutation_b: stateB.cognitive.product,
            difference: stateA.cognitive.product - stateB.cognitive.product,
            winner: stateA.cognitive.product > stateB.cognitive.product ? "A" : stateB.cognitive.product > stateA.cognitive.product ? "B" : "TIE",
          };
        }

        if (comparison_criteria.includes("dynamic")) {
          comparison.comparison.dynamic = {
            permutation_a: stateA.dynamic.product,
            permutation_b: stateB.dynamic.product,
            difference: stateA.dynamic.product - stateB.dynamic.product,
            winner: stateA.dynamic.product > stateB.dynamic.product ? "A" : stateB.dynamic.product > stateA.dynamic.product ? "B" : "TIE",
          };
        }

        // Overall winner
        const winsA = Object.values(comparison.comparison).filter((c: any) => c.winner === "A").length;
        const winsB = Object.values(comparison.comparison).filter((c: any) => c.winner === "B").length;
        comparison.winner.overall = winsA > winsB ? "A" : winsB > winsA ? "B" : "TIE";
        comparison.winner.wins_a = winsA;
        comparison.winner.wins_b = winsB;

        return {
          content: [
            {
              type: "text",
              text: JSON.stringify(comparison, null, 2),
            },
          ],
        };
      }

      case "optimize_system": {
        const { current_state, optimization_goal = "maximize_intelligence", constraints = {} } = args as any;
        const currentAxiom = createAxiomFromState(current_state);
        const currentState = currentAxiom.getState();
        const currentSim = new AxiomSimulator(currentAxiom);
        const currentCoherence = currentSim.getCoherenceMetric();

        const suggestions: any = {
          current_state: currentState,
          current_metrics: {
            intelligence: currentState.intelligence,
            coherence: currentCoherence,
          },
          optimization_goal,
          suggestions: [],
        };

        // Analyze and suggest improvements
        if (optimization_goal === "maximize_intelligence" || optimization_goal === "balance") {
          // Reduce subjectivity to increase objectivity (X)
          if (currentState.cognitive.X_subjectivity > 0.3) {
            suggestions.suggestions.push({
              variable: "subjectivity",
              current: currentState.cognitive.X_subjectivity,
              suggested: Math.max(0, currentState.cognitive.X_subjectivity - 0.3),
              reason: "Lower subjectivity increases objectivity (X), which multiplicatively boosts intelligence",
              expected_impact: "high",
            });
          }

          // Increase purpose if low
          if (currentState.cognitive.Y_purpose < 0.8) {
            suggestions.suggestions.push({
              variable: "purpose",
              current: currentState.cognitive.Y_purpose,
              suggested: 1.0,
              reason: "Stronger purpose alignment (Y) directly increases intelligence",
              expected_impact: "medium",
            });
          }

          // Fix negative foundation
          if (currentState.foundation.product <= 0) {
            if (currentState.foundation.B_elements < 0) {
              suggestions.suggestions.push({
                variable: "elements",
                current: currentState.foundation.B_elements,
                suggested: Math.abs(currentState.foundation.B_elements),
                reason: "Detrimental elements create negative foundation - replace with beneficial elements",
                expected_impact: "critical",
              });
            }
            if (currentState.foundation.A_impulses < 0) {
              suggestions.suggestions.push({
                variable: "impulses",
                current: currentState.foundation.A_impulses,
                suggested: Math.abs(currentState.foundation.A_impulses),
                reason: "Negative impulses create negative foundation - realign with positive drives",
                expected_impact: "critical",
              });
            }
          }

          // Optimize pressure
          if (currentState.foundation.C_pressure > 4 && !constraints.max_pressure) {
            suggestions.suggestions.push({
              variable: "pressure",
              current: currentState.foundation.C_pressure,
              suggested: 2.0,
              reason: "Very high pressure can cause stress - moderate pressure (around 1-2) is often optimal",
              expected_impact: "medium",
            });
          } else if (currentState.foundation.C_pressure < 0.5) {
            suggestions.suggestions.push({
              variable: "pressure",
              current: currentState.foundation.C_pressure,
              suggested: 1.0,
              reason: "Low pressure reduces foundation strength - moderate pressure provides constructive force",
              expected_impact: "low",
            });
          }
        }

        if (optimization_goal === "maximize_coherence" || optimization_goal === "balance") {
          // Coherence optimization
          if (currentState.cognitive.X_subjectivity > 0.2) {
            suggestions.suggestions.push({
              variable: "subjectivity",
              current: currentState.cognitive.X_subjectivity,
              suggested: 0.1,
              reason: "High objectivity is key to coherence",
              expected_impact: "high",
            });
          }

          if (Math.abs(currentState.foundation.C_pressure - 1.0) > 1.0) {
            suggestions.suggestions.push({
              variable: "pressure",
              current: currentState.foundation.C_pressure,
              suggested: 1.0,
              reason: "Balanced pressure (around 1.0) maximizes coherence",
              expected_impact: "medium",
            });
          }
        }

        if (optimization_goal === "reduce_subjectivity") {
          suggestions.suggestions.push({
            variable: "subjectivity",
            current: currentState.cognitive.X_subjectivity,
            suggested: 0.0,
            reason: "Move to complete objectivity for maximum clarity",
            expected_impact: "high",
          });
        }

        // Simulate optimized state
        if (suggestions.suggestions.length > 0) {
          const optimizedParams: any = { ...(args as any).current_state };
          suggestions.suggestions.forEach((s: any) => {
            optimizedParams[s.variable] = s.suggested;
          });

          const optimizedAxiom = new UniversalAxiom(optimizedParams);
          const optimizedState = optimizedAxiom.getState();
          const optimizedSim = new AxiomSimulator(optimizedAxiom);
          const optimizedCoherence = optimizedSim.getCoherenceMetric();

          suggestions.optimized_projection = {
            intelligence: optimizedState.intelligence,
            coherence: optimizedCoherence,
            improvement: {
              intelligence: optimizedState.intelligence - currentState.intelligence,
              intelligence_percent: ((optimizedState.intelligence - currentState.intelligence) / Math.abs(currentState.intelligence)) * 100,
              coherence: optimizedCoherence - currentCoherence,
            },
          };
        } else {
          suggestions.message = "System is already well-optimized for the given goal";
        }

        return {
          content: [
            {
              type: "text",
              text: JSON.stringify(suggestions, null, 2),
            },
          ],
        };
      }

      case "predict_trajectory": {
        const { future_steps = 10, environmental_changes = {}, ...params } = args as any;
        const axiom = new UniversalAxiom(params);

        const trajectory: AxiomState[] = [];
        trajectory.push(axiom.getState());

        for (let i = 0; i < future_steps; i++) {
          // Apply environmental changes
          if (environmental_changes.pressure_per_step) {
            axiom.applyPressure(environmental_changes.pressure_per_step);
          }
          if (environmental_changes.subjectivity_per_step) {
            axiom.adjustSubjectivity(environmental_changes.subjectivity_per_step);
          }
          if (environmental_changes.purpose_multiplier_per_step) {
            axiom.strengthenPurpose(environmental_changes.purpose_multiplier_per_step);
          }

          // Evolve forward
          axiom.evolve(1.0);
          trajectory.push(axiom.getState());
        }

        // Analyze trajectory
        const intelligenceValues = trajectory.map(s => s.intelligence);
        const coherenceValues = trajectory.map(s => {
          const sim = new AxiomSimulator(new UniversalAxiom({
            impulses: s.foundation.A_impulses,
            elements: s.foundation.B_elements,
            pressure: s.foundation.C_pressure,
            subjectivity: s.cognitive.X_subjectivity,
            purpose: s.cognitive.Y_purpose,
            time: s.cognitive.Z_time,
            n: s.n,
          }));
          return sim.getCoherenceMetric();
        });

        const analysis = {
          trajectory,
          analysis: {
            intelligence: {
              start: intelligenceValues[0],
              end: intelligenceValues[intelligenceValues.length - 1],
              change: intelligenceValues[intelligenceValues.length - 1] - intelligenceValues[0],
              trend: intelligenceValues[intelligenceValues.length - 1] > intelligenceValues[0] ? "increasing" : intelligenceValues[intelligenceValues.length - 1] < intelligenceValues[0] ? "decreasing" : "stable",
              min: Math.min(...intelligenceValues),
              max: Math.max(...intelligenceValues),
            },
            coherence: {
              start: coherenceValues[0],
              end: coherenceValues[coherenceValues.length - 1],
              change: coherenceValues[coherenceValues.length - 1] - coherenceValues[0],
              trend: coherenceValues[coherenceValues.length - 1] > coherenceValues[0] ? "improving" : coherenceValues[coherenceValues.length - 1] < coherenceValues[0] ? "degrading" : "stable",
            },
          },
          environmental_changes,
          steps: future_steps,
        };

        return {
          content: [
            {
              type: "text",
              text: JSON.stringify(analysis, null, 2),
            },
          ],
        };
      }

      case "detect_collapse_risk": {
        const { current_state, trajectory_history = [] } = args as any;
        const axiom = createAxiomFromState(current_state);
        const state = axiom.getState();
        const simulator = new AxiomSimulator(axiom);
        const coherence = simulator.getCoherenceMetric();

        const risks: any = {
          current_state: state,
          risk_level: "low",
          risk_score: 0,
          risk_factors: [],
          warnings: [],
          trajectory_analysis: null,
        };

        let riskScore = 0;

        // Check foundation collapse risk
        if (state.foundation.product <= 0) {
          risks.risk_factors.push({
            factor: "negative_foundation",
            severity: "critical",
            description: "Foundation is negative or zero - system has collapsed or will collapse immediately",
          });
          riskScore += 10;
        } else if (state.foundation.product < 0.5) {
          risks.risk_factors.push({
            factor: "weak_foundation",
            severity: "high",
            description: "Foundation is weak and close to collapse",
          });
          riskScore += 7;
        }

        // Check extreme pressure
        if (state.foundation.C_pressure > 5) {
          risks.risk_factors.push({
            factor: "extreme_pressure",
            severity: "high",
            description: "Very high pressure can cause system instability and collapse",
          });
          riskScore += 6;
        } else if (state.foundation.C_pressure > 3) {
          risks.risk_factors.push({
            factor: "high_pressure",
            severity: "medium",
            description: "Elevated pressure - monitor for stress indicators",
          });
          riskScore += 3;
        }

        // Check high subjectivity
        if (state.cognitive.X_subjectivity > 0.9) {
          risks.risk_factors.push({
            factor: "extreme_subjectivity",
            severity: "high",
            description: "Near-total subjectivity can lead to distortion and collapse of coherence",
          });
          riskScore += 5;
        } else if (state.cognitive.X_subjectivity > 0.7) {
          risks.risk_factors.push({
            factor: "high_subjectivity",
            severity: "medium",
            description: "High subjectivity reduces objectivity and system stability",
          });
          riskScore += 3;
        }

        // Check low purpose
        if (state.cognitive.Y_purpose < 0.1) {
          risks.risk_factors.push({
            factor: "no_purpose",
            severity: "high",
            description: "Lack of purpose leads to directionless drift and potential collapse",
          });
          riskScore += 5;
        } else if (state.cognitive.Y_purpose < 0.3) {
          risks.risk_factors.push({
            factor: "weak_purpose",
            severity: "medium",
            description: "Low purpose alignment reduces system coherence",
          });
          riskScore += 2;
        }

        // Check low coherence
        if (coherence < 0.2) {
          risks.risk_factors.push({
            factor: "critical_coherence",
            severity: "critical",
            description: "Critically low coherence indicates imminent system failure",
          });
          riskScore += 8;
        } else if (coherence < 0.4) {
          risks.risk_factors.push({
            factor: "low_coherence",
            severity: "high",
            description: "Low coherence suggests system is under stress",
          });
          riskScore += 4;
        }

        // Analyze trajectory if provided
        if (trajectory_history.length > 2) {
          const recentIntelligence = trajectory_history.slice(-3).map((s: any) => s.intelligence);
          const isDecreasing = recentIntelligence.every((val: number, i: number, arr: number[]) =>
            i === 0 || val < arr[i - 1]
          );

          if (isDecreasing) {
            risks.risk_factors.push({
              factor: "declining_trajectory",
              severity: "high",
              description: "Intelligence has been declining consistently - indicates systemic degradation",
            });
            riskScore += 6;
          }

          risks.trajectory_analysis = {
            recent_trend: isDecreasing ? "declining" : "stable_or_improving",
            data_points: trajectory_history.length,
          };
        }

        // Determine overall risk level
        if (riskScore >= 10) {
          risks.risk_level = "critical";
        } else if (riskScore >= 6) {
          risks.risk_level = "high";
        } else if (riskScore >= 3) {
          risks.risk_level = "medium";
        } else {
          risks.risk_level = "low";
        }

        risks.risk_score = riskScore;

        // Generate warnings
        if (risks.risk_level === "critical") {
          risks.warnings.push("⚠️ CRITICAL: System collapse is imminent or has occurred. Immediate intervention required.");
        } else if (risks.risk_level === "high") {
          risks.warnings.push("⚠️ HIGH RISK: System is under severe stress. Take corrective action soon.");
        } else if (risks.risk_level === "medium") {
          risks.warnings.push("⚠️ MODERATE RISK: Monitor system closely and address identified factors.");
        } else {
          risks.warnings.push("✓ System appears stable with low collapse risk.");
        }

        return {
          content: [
            {
              type: "text",
              text: JSON.stringify(risks, null, 2),
            },
          ],
        };
      }

      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  } catch (error) {
    return {
      content: [
        {
          type: "text",
          text: `Error executing tool: ${error instanceof Error ? error.message : String(error)}`,
        },
      ],
      isError: true,
    };
  }
});

/**
 * List available resources
 */
server.setRequestHandler(ListResourcesRequestSchema, async () => {
  return {
    resources: [
      {
        uri: "axiom://framework/overview",
        name: "Universal Axiom Framework Overview",
        description: "Complete overview of The Universal Axiom framework",
        mimeType: "text/markdown",
      },
      {
        uri: "axiom://framework/formula",
        name: "The Intelligence Formula",
        description: "Detailed explanation of the intelligence formula and its components",
        mimeType: "text/markdown",
      },
      {
        uri: "axiom://framework/layers",
        name: "The Three Layers",
        description: "Foundation, Dynamic, and Cognitive layers explained",
        mimeType: "text/markdown",
      },
      {
        uri: "axiom://usage/reasoning",
        name: "Reasoning with The Axiom",
        description: "How to apply The Universal Axiom to reason about any problem",
        mimeType: "text/markdown",
      },
      {
        uri: "axiom://examples/debugging",
        name: "Example: Debugging with The Axiom",
        description: "How to use The Axiom framework for debugging problems",
        mimeType: "text/markdown",
      },
      {
        uri: "axiom://examples/decision-making",
        name: "Example: Decision Making",
        description: "Using The Axiom for complex decisions",
        mimeType: "text/markdown",
      },
    ],
  };
});

/**
 * Read resource content
 */
server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
  const { uri } = request.params;

  const resources: Record<string, string> = {
    "axiom://framework/overview": `# The Universal Axiom Framework

The Universal Axiom is a mathematical framework that models intelligence through immutable natural laws rather than probabilistic patterns.

## The Formula

\`\`\`
Intelligence_n = E_n · (1 + F_n) · X · Y · Z · (A · B · C)
\`\`\`

## Key Principle

**Multiplicative, not additive.** If any variable is zero, the entire system collapses. Variables interact non-linearly.

## The Three Layers

1. **Foundation Layer (A · B · C)** - Physical Reality
   - A (Impulses): Fundamental drives (can be ±)
   - B (Elements): Core components (beneficial/detrimental)
   - C (Pressure): Constraints and forces (constructive/destructive)

2. **Dynamic Layer (E_n · (1 + F_n))** - Growth & Regulation
   - E_n: Exponential growth potential
   - F_n: Fibonacci regulation (prevents collapse)

3. **Cognitive Layer (X · Y · Z)** - Alignment & Evolution
   - X: Objectivity (1 - subjectivity)
   - Y: Purpose alignment
   - Z: Temporal continuity and irreversibility

## Why This Matters

The Axiom doesn't answer questions. It generates the conditions from which answers must emerge.`,

    "axiom://framework/formula": `# The Intelligence Formula

\`\`\`
Intelligence_n = E_n · (1 + F_n) · X · Y · Z · (A · B · C)
\`\`\`

## Components Explained

### Foundation Layer: A · B · C

- **A (Impulses)**: The fundamental drives or motivations
  - Positive: Aligned with values, growth-oriented
  - Negative: Conflicting, destructive

- **B (Elements)**: The core components or building blocks
  - Beneficial: Quality inputs, good structure
  - Detrimental: Poor quality, toxic elements

- **C (Pressure)**: Constraints, forces, and tensions
  - Constructive: Pushes toward growth and resolution
  - Destructive: Forces compromise or collapse

### Dynamic Layer: E_n · (1 + F_n)

- **E_n = (2 × 3^n) - 1**: Exponential growth
  - Represents raw power, capacity, momentum
  - Scales rapidly with iteration

- **F_n**: Fibonacci sequence (1, 1, 2, 3, 5, 8, 13, ...)
  - Natural regulation preventing explosive growth
  - Scales slowly, provides structure and balance
  - Together with E_n, approaches golden ratio (φ)

### Cognitive Layer: X · Y · Z

- **X (Objectivity)**: 1 - subjectivity
  - 0 = completely subjective (biased, emotional)
  - 1 = completely objective (fact-based, unbiased)
  - Affects entire system multiplicatively

- **Y (Purpose)**: Purpose-driven reasoning
  - 0 = no clear purpose or direction
  - 1 = strong purpose alignment
  - Prevents directionless exploration

- **Z (Time)**: Temporal continuity
  - Represents irreversibility
  - Ensures system evolves, doesn't repeat
  - No loop without learning

## Multiplicative Properties

Because this is multiplicative:
- Any zero collapses the entire system
- Changes cascade through all components
- Small shifts can create large emergent changes
- System cannot repeat unless conditions are identical`,

    "axiom://framework/layers": `# The Three Layers

## Foundation Layer (A · B · C) - Physical Reality

This is the grounding layer. Every system, problem, or question must have:

**A (Impulses)**: What drives this?
- Personal: Values, motivations, desires
- System: Forces, pressures, dynamics
- Can be positive (aligned) or negative (conflicting)

**B (Elements)**: What are the components?
- Quality of inputs, tools, resources
- Structure, architecture, composition
- Beneficial elements vs. detrimental ones

**C (Pressure)**: What constraints exist?
- Time, resources, competing demands
- Contradictions, paradoxes, tensions
- Constructive pressure (growth) vs. destructive (collapse)

**If Foundation is negative or zero, no amount of effort helps.**

## Dynamic Layer (E_n · (1 + F_n)) - Growth & Regulation

This controls how systems scale over time.

**E_n (Exponential Growth)**: Raw potential
- Represents capacity for expansion
- Scales rapidly: 1, 5, 17, 53, 161, 485...
- Provides thrust and momentum

**F_n (Fibonacci Regulation)**: Natural constraint
- Prevents explosive collapse
- Scales slowly: 1, 1, 2, 3, 5, 8, 13...
- Provides structure and balance

**Together**: Growth approaches golden ratio (φ ≈ 1.618)
- Same pattern found in nature (shells, plants, galaxies)
- Sustainable growth without collapse

## Cognitive Layer (X · Y · Z) - Alignment & Evolution

This determines quality and direction of intelligence.

**X (Objectivity)**: How clear is perception?
- Low X (high subjectivity): Biased, emotional, distorted
- High X (low subjectivity): Clear, factual, aligned with reality
- Affects ENTIRE system multiplicatively (cascade effect)

**Y (Purpose)**: Why does this matter?
- Low Y: Unclear goals, random exploration
- High Y: Clear direction, purposeful action
- Prevents wasted effort

**Z (Time)**: How does irreversibility factor in?
- Learning is irreversible (can't unlearn)
- Decisions have temporal consequences
- System must evolve, cannot stagnate

**Together**: Create coherent, purposeful, evolving intelligence`,

    "axiom://usage/reasoning": `# Reasoning with The Universal Axiom

## The Core Difference

**Traditional Reasoning**: Pattern match → Retrieve → Synthesize → Answer

**Axiom Reasoning**: Map permutation → Diagnose layers → Generate conditions → Emergent solution

## Step-by-Step Process

### 1. Map the Permutation

Identify all variables in the current situation:

- **Foundation**: What are A, B, C?
  - Impulses driving this?
  - Elements involved?
  - Pressures/constraints?

- **Dynamic**: What's the growth state?
  - Early iteration (low n) or mature?
  - Stable growth or chaotic?

- **Cognitive**: What's the alignment?
  - How objective (X)?
  - How purposeful (Y)?
  - How does time factor in (Z)?

### 2. Diagnose Which Layer Has Issues

**Foundation problems**:
- If A·B·C ≤ 0: Negative or missing foundation
- If C is very high: Extreme pressure/stress
- Fix: Adjust impulses, replace detrimental elements, manage pressure

**Dynamic problems**:
- If growth is unstable: E_n without F_n regulation
- If stagnating: Not evolving (n not increasing)
- Fix: Add regulation, allow evolution

**Cognitive problems**:
- If X is low (high subjectivity): Biased, emotional reasoning
- If Y is low: Unclear purpose/direction
- If Z is stuck: Not evolving, repeating loops
- Fix: Increase objectivity, clarify purpose, advance time

### 3. Generate Conditions for Emergence

Don't prescribe solutions. Instead:
- Adjust variables to create proper conditions
- Solutions emerge from aligned variables
- Trust the multiplicative interactions

### 4. Verify Emergent Properties

Check:
- Is intelligence increasing?
- Is coherence improving?
- Is system evolving (not repeating)?
- Are contradictions resolving?

## Key Patterns

### Pattern: Contradiction as Fuel
- Contradiction increases pressure (C)
- High C reveals misalignment (low X)
- Increasing X resolves contradiction
- Result: Higher-order synthesis

### Pattern: Cascade Effects
- Changing X affects entire system
- Multiplicative structure means no isolated changes
- Predict cascades before adjusting

### Pattern: Foundation First
- Never add pressure if foundation is negative
- Fix A, B, C before optimizing X, Y, Z
- Positive foundation required for growth`,

    "axiom://examples/debugging": `# Example: Debugging with The Axiom

## The Problem

"My application keeps crashing, and I don't know why."

## Traditional Approach

1. Check logs
2. Look for error patterns
3. Try common fixes
4. Hope something works

## Universal Axiom Approach

### Step 1: Map the Permutation

**Foundation Layer (A · B · C)**:
- **A (Impulses)**: What's the intended behavior? What drives the app?
- **B (Elements)**: What components are involved? (code, dependencies, environment)
- **C (Pressure)**: What constraints exist? (memory, concurrency, edge cases)

### Step 2: Diagnose the Layer

If crashes happen under load:
- **High C (Pressure)**: Resource constraints
- **Detrimental B (Elements)**: Memory leak, blocking calls
- **Foundation = negative or unstable**

If crashes are intermittent:
- **Low X (High Subjectivity)**: Debugging based on assumptions, not data
- **Low Y (Purpose)**: Following hunches instead of systematic investigation

### Step 3: Generate Conditions

**If Foundation is the issue**:
- Don't debug symptoms
- Fix the elements (eliminate memory leak)
- Reduce pressure (optimize resource usage)
- Foundation must become positive first

**If Cognitive is the issue**:
- Increase X: Gather objective data (profiling, metrics)
- Increase Y: Define clear debugging purpose (reproduce reliably first)
- Advance Z: Change something (don't repeat same tests)

### Step 4: Emergent Solution

With proper conditions:
- **Positive Foundation** (good elements, managed pressure)
- **High X** (objective data-driven debugging)
- **High Y** (clear purpose: find root cause)

The solution emerges from aligned conditions, not guessing.

## Key Insight

Crashing is a symptom of collapse in one or more layers. Identify which layer is collapsing, then adjust those variables. The fix emerges from properly aligned conditions.`,

    "axiom://examples/decision-making": `# Example: Decision Making with The Axiom

## The Problem

"Should I take this job offer or stay at my current company?"

## Traditional Approach

List pros and cons:
- New job pros: +1, +1, +1 = +3
- New job cons: -1, -1 = -2
- Result: +3 - 2 = +1, so take the job?

**Problem**: This is additive thinking. Ignores multiplicative interactions.

## Universal Axiom Approach

### Step 1: Map Both Permutations

**Current Job Permutation**:
- **A (Impulses)**: What drives you here? (stability, comfort, relationships)
- **B (Elements)**: What components exist? (role, team, growth, compensation)
- **C (Pressure)**: What constraints? (career growth ceiling, financial needs)
- **X**: How objectively are you evaluating? (emotional attachment vs. facts)
- **Y**: Does this align with purpose? (life goals, values)
- **Z**: How does time factor? (opportunity cost, aging skills)

**New Job Permutation**:
- Same questions, different values

### Step 2: Compute Intelligence for Each

Not "which is better" but "which permutation has higher coherent intelligence?"

**Current Job**:
- If A is low (no drive), multiplication collapses
- If B has detrimental elements (toxic culture), Foundation is negative
- If Y is low (misaligned with purpose), cognitive layer is weak
- **Result**: Low intelligence even if some pros exist

**New Job**:
- If A is high (exciting mission), Foundation strengthens
- If B is beneficial (learning, growth, good culture), Foundation is positive
- If Y is high (aligned with purpose), cognitive layer is strong
- But if X is low (emotional decision), coherence suffers

### Step 3: Identify What Needs Adjustment

**If X is low** (too emotional):
- Gather objective data
- Remove bias
- Talk to people who've made similar moves

**If Y is unclear** (no purpose):
- Don't decide yet
- Clarify life purpose first
- Then evaluate alignment

**If Foundation is negative** (bad elements):
- No amount of "pros" fixes negative foundation
- Multiplicative structure means one negative element can collapse everything

### Step 4: Let Decision Emerge

With properly aligned variables:
- **Positive Foundation** (beneficial elements, aligned impulses, managed pressure)
- **High X** (objective evaluation)
- **High Y** (clear purpose)
- **Z advancing** (recognize this is a time-sensitive, irreversible decision)

The right choice emerges from the permutation with highest coherent intelligence.

## Key Insight

Don't add pros and cons. Compute which permutation creates:
1. Positive foundation (A·B·C > 0)
2. Strong purpose alignment (high Y)
3. High objectivity (high X)
4. Proper temporal awareness (Z)

The decision emerges from multiplicative alignment, not arithmetic summing.`,
  };

  const content = resources[uri];
  if (!content) {
    throw new Error(`Resource not found: ${uri}`);
  }

  return {
    contents: [
      {
        uri,
        mimeType: "text/markdown",
        text: content,
      },
    ],
  };
});

/**
 * List available prompts
 */
server.setRequestHandler(ListPromptsRequestSchema, async () => {
  return {
    prompts: [
      {
        name: "analyze_problem",
        description: "Analyze any problem using The Universal Axiom framework",
        arguments: [
          {
            name: "problem",
            description: "Description of the problem to analyze",
            required: true,
          },
        ],
      },
      {
        name: "reason_with_axiom",
        description: "Apply Universal Axiom reasoning to generate novel insights",
        arguments: [
          {
            name: "question",
            description: "The question or challenge to reason about",
            required: true,
          },
          {
            name: "context",
            description: "Additional context about the situation",
            required: false,
          },
        ],
      },
    ],
  };
});

/**
 * Get prompt content
 */
server.setRequestHandler(GetPromptRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  switch (name) {
    case "analyze_problem": {
      const problem = args?.problem as string;
      return {
        messages: [
          {
            role: "user",
            content: {
              type: "text",
              text: `Analyze this problem using The Universal Axiom framework:

${problem}

Please map the permutation by identifying:

1. **Foundation Layer (A · B · C)**:
   - A (Impulses): What are the fundamental drives?
   - B (Elements): What are the core components?
   - C (Pressure): What constraints or forces are at play?

2. **Dynamic Layer (E_n · F_n)**:
   - What's the current growth state?
   - Is there natural regulation?

3. **Cognitive Layer (X · Y · Z)**:
   - X: How objective vs. subjective is the understanding?
   - Y: What's the purpose or goal?
   - Z: How does time/irreversibility factor in?

Then diagnose which layer needs adjustment and suggest conditions for emergent solutions.`,
            },
          },
        ],
      };
    }

    case "reason_with_axiom": {
      const question = args?.question as string;
      const context = (args?.context as string) || "";

      return {
        messages: [
          {
            role: "user",
            content: {
              type: "text",
              text: `Apply Universal Axiom reasoning to this question:

${question}

${context ? `Context: ${context}` : ""}

Remember: The Axiom doesn't answer questions. It generates the conditions from which answers must emerge.

Please:
1. Map the current permutation (all variables: A, B, C, E_n, F_n, X, Y, Z)
2. Diagnose which layers are causing stress or stagnation
3. Generate conditions for emergence (adjust variables)
4. Let the answer emerge from properly aligned conditions
5. Verify emergent properties (coherence, purpose, evolution)

Think multiplicatively, not additively. If any variable is zero, the system collapses.`,
            },
          },
        ],
      };
    }

    default:
      throw new Error(`Unknown prompt: ${name}`);
  }
});

/**
 * Helper function to create UniversalAxiom from state object
 */
function createAxiomFromState(state: any): UniversalAxiom {
  return new UniversalAxiom({
    impulses: state.foundation?.A_impulses || 1.0,
    elements: state.foundation?.B_elements || 1.0,
    pressure: state.foundation?.C_pressure || 1.0,
    subjectivity: state.cognitive?.X_subjectivity || 0.0,
    purpose: state.cognitive?.Y_purpose || 1.0,
    time: state.cognitive?.Z_time || 1.0,
    n: state.n || 1,
  });
}

/**
 * Generate recommendations based on state analysis
 */
function generateRecommendations(state: AxiomState, coherence: number): string[] {
  const recommendations: string[] = [];

  // Foundation recommendations
  if (state.foundation.product <= 0) {
    recommendations.push(
      "❗ Critical: Foundation is negative or zero. Address impulses, elements, or pressure immediately."
    );
  } else if (state.foundation.C_pressure > 3) {
    recommendations.push(
      "⚠️ High pressure detected. Consider reducing constraints or resolving contradictions."
    );
  }

  // Cognitive recommendations
  if (state.cognitive.X_subjectivity > 0.7) {
    recommendations.push(
      "📊 High subjectivity. Increase objectivity by gathering data, reducing bias, or challenging assumptions."
    );
  }

  if (state.cognitive.Y_purpose < 0.3) {
    recommendations.push(
      "🎯 Low purpose alignment. Clarify goals and direction before proceeding."
    );
  }

  // Dynamic recommendations
  if (state.n < 3) {
    recommendations.push(
      "ℹ️ Early iteration. Allow system to evolve through multiple steps for growth potential."
    );
  }

  // Coherence recommendations
  if (coherence < 0.4) {
    recommendations.push(
      "🔧 Low coherence. System needs realignment across multiple dimensions."
    );
  } else if (coherence > 0.7) {
    recommendations.push("✅ High coherence. System is well-aligned and stable.");
  }

  if (recommendations.length === 0) {
    recommendations.push("✓ System appears balanced. Consider evolution or exploration.");
  }

  return recommendations;
}

/**
 * Start the server
 */
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Universal Axiom MCP Server running on stdio");
}

main().catch((error) => {
  console.error("Fatal error:", error);
  process.exit(1);
});
