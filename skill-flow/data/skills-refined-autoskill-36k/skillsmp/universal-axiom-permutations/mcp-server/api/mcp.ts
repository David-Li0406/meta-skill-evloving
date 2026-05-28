/**
 * Universal Axiom MCP Server - Vercel Serverless HTTP Endpoint
 *
 * This adapts the MCP server to work as a stateless HTTP API for Vercel deployment.
 * Supports JSON-RPC 2.0 protocol used by MCP.
 */

// Vercel types - defined inline to avoid dependency issues
interface VercelRequest {
  method?: string;
  body?: unknown;
  query?: Record<string, string | string[]>;
  headers?: Record<string, string | string[] | undefined>;
}

interface VercelResponse {
  status(code: number): VercelResponse;
  json(body: unknown): void;
  end(): void;
  setHeader(name: string, value: string): VercelResponse;
}

// Import the Universal Axiom classes from the source
import {
  UniversalAxiom,
  AxiomSimulator,
  type AxiomState,
  type AxiomConfig,
} from '../lib/universal-axiom.js';

// Types for MCP protocol
interface JsonRpcRequest {
  jsonrpc: '2.0';
  id: string | number;
  method: string;
  params?: Record<string, unknown>;
}

interface JsonRpcResponse {
  jsonrpc: '2.0';
  id: string | number | null;
  result?: unknown;
  error?: {
    code: number;
    message: string;
    data?: unknown;
  };
}

// Server info
const SERVER_INFO = {
  name: 'universal-axiom-server',
  version: '0.2.0',
  protocolVersion: '2024-11-05',
};

// Tool definitions
const TOOLS = [
  {
    name: 'compute_intelligence',
    description: 'Compute intelligence value using The Universal Axiom formula: Intelligence_n = E_n · (1 + F_n) · X · Y · Z · (A · B · C)',
    inputSchema: {
      type: 'object',
      properties: {
        impulses: { type: 'number', description: 'A - Fundamental drives', default: 1.0 },
        elements: { type: 'number', description: 'B - Core components', default: 1.0 },
        pressure: { type: 'number', description: 'C - Constraints and forces', default: 1.0 },
        subjectivity: { type: 'number', description: 'X - Subjectivity level (0-1)', minimum: 0, maximum: 1, default: 0.0 },
        purpose: { type: 'number', description: 'Y - Purpose-driven reasoning strength', default: 1.0 },
        time: { type: 'number', description: 'Z - Temporal continuity', default: 1.0 },
        n: { type: 'number', description: 'Iteration level', default: 1 },
      },
      required: [],
    },
  },
  {
    name: 'evolve_system',
    description: 'Evolve a Universal Axiom system forward in time, updating temporal and dynamic components',
    inputSchema: {
      type: 'object',
      properties: {
        current_state: { type: 'object', description: 'Current state of the axiom system' },
        steps: { type: 'number', description: 'Number of time steps to evolve', default: 1 },
        delta_time: { type: 'number', description: 'Time increment per step', default: 1.0 },
      },
      required: ['current_state'],
    },
  },
  {
    name: 'apply_pressure',
    description: 'Apply pressure changes to the system (e.g., from contradictions, constraints, or new information)',
    inputSchema: {
      type: 'object',
      properties: {
        current_state: { type: 'object', description: 'Current state of the axiom system' },
        pressure_delta: { type: 'number', description: 'Change in pressure' },
      },
      required: ['current_state', 'pressure_delta'],
    },
  },
  {
    name: 'adjust_subjectivity',
    description: 'Adjust the subjectivity level of the system (move toward objectivity or subjectivity)',
    inputSchema: {
      type: 'object',
      properties: {
        current_state: { type: 'object', description: 'Current state of the axiom system' },
        subjectivity_delta: { type: 'number', description: 'Change in subjectivity' },
      },
      required: ['current_state', 'subjectivity_delta'],
    },
  },
  {
    name: 'simulate_evolution',
    description: 'Simulate the evolution of a system over multiple time steps, tracking state changes',
    inputSchema: {
      type: 'object',
      properties: {
        impulses: { type: 'number', default: 1.0 },
        elements: { type: 'number', default: 1.0 },
        pressure: { type: 'number', default: 1.0 },
        subjectivity: { type: 'number', minimum: 0, maximum: 1, default: 0.0 },
        purpose: { type: 'number', default: 1.0 },
        time: { type: 'number', default: 1.0 },
        n: { type: 'number', default: 1 },
        steps: { type: 'number', description: 'Number of evolution steps', default: 10 },
        delta_time: { type: 'number', default: 1.0 },
      },
      required: [],
    },
  },
  {
    name: 'simulate_contradiction_resolution',
    description: 'Simulate how the system resolves contradiction through pressure application and objectivity adjustment',
    inputSchema: {
      type: 'object',
      properties: {
        impulses: { type: 'number', default: 1.0 },
        elements: { type: 'number', default: 1.0 },
        pressure: { type: 'number', default: 1.0 },
        subjectivity: { type: 'number', minimum: 0, maximum: 1, default: 0.5 },
        purpose: { type: 'number', default: 1.0 },
        time: { type: 'number', default: 1.0 },
        n: { type: 'number', default: 1 },
        initial_pressure: { type: 'number', description: 'Initial pressure spike', default: 2.0 },
        resolution_steps: { type: 'number', description: 'Steps to resolve', default: 5 },
      },
      required: [],
    },
  },
  {
    name: 'get_coherence_metric',
    description: 'Calculate the coherence metric of a system based on objectivity, purpose, and pressure balance',
    inputSchema: {
      type: 'object',
      properties: {
        current_state: { type: 'object', description: 'Current state of the axiom system' },
      },
      required: ['current_state'],
    },
  },
  {
    name: 'analyze_permutation',
    description: 'Analyze a specific permutation of the Universal Axiom to diagnose which layers may need adjustment',
    inputSchema: {
      type: 'object',
      properties: {
        impulses: { type: 'number', default: 1.0 },
        elements: { type: 'number', default: 1.0 },
        pressure: { type: 'number', default: 1.0 },
        subjectivity: { type: 'number', minimum: 0, maximum: 1, default: 0.0 },
        purpose: { type: 'number', default: 1.0 },
        time: { type: 'number', default: 1.0 },
        n: { type: 'number', default: 1 },
      },
      required: [],
    },
  },
  {
    name: 'compare_permutations',
    description: 'Compare two different system permutations to see which has higher intelligence and better alignment',
    inputSchema: {
      type: 'object',
      properties: {
        permutation_a: { type: 'object', description: 'First permutation to compare' },
        permutation_b: { type: 'object', description: 'Second permutation to compare' },
        comparison_criteria: { type: 'array', description: 'Criteria to compare', default: ['intelligence', 'coherence'] },
      },
      required: ['permutation_a', 'permutation_b'],
    },
  },
  {
    name: 'optimize_system',
    description: 'Suggest optimal adjustments to system variables to improve intelligence and coherence',
    inputSchema: {
      type: 'object',
      properties: {
        current_state: { type: 'object', description: 'Current state of the system' },
        optimization_goal: { type: 'string', description: 'Goal: maximize_intelligence, maximize_coherence, balance, reduce_subjectivity', default: 'maximize_intelligence' },
        constraints: { type: 'object', description: 'Constraints on adjustments', default: {} },
      },
      required: ['current_state'],
    },
  },
  {
    name: 'predict_trajectory',
    description: 'Predict the future trajectory of a system over multiple iterations',
    inputSchema: {
      type: 'object',
      properties: {
        impulses: { type: 'number', default: 1.0 },
        elements: { type: 'number', default: 1.0 },
        pressure: { type: 'number', default: 1.0 },
        subjectivity: { type: 'number', minimum: 0, maximum: 1, default: 0.0 },
        purpose: { type: 'number', default: 1.0 },
        time: { type: 'number', default: 1.0 },
        n: { type: 'number', default: 1 },
        future_steps: { type: 'number', description: 'Number of future steps to predict', default: 10 },
        environmental_changes: { type: 'object', description: 'Changes to apply per step', default: {} },
      },
      required: [],
    },
  },
  {
    name: 'detect_collapse_risk',
    description: 'Analyze a system for collapse risk indicators and warning signs',
    inputSchema: {
      type: 'object',
      properties: {
        current_state: { type: 'object', description: 'Current state to analyze' },
        trajectory_history: { type: 'array', description: 'Optional historical states', default: [] },
      },
      required: ['current_state'],
    },
  },
];

// Resources
const RESOURCES = [
  {
    uri: 'axiom://framework/overview',
    name: 'Universal Axiom Framework Overview',
    description: 'Complete overview of The Universal Axiom framework',
    mimeType: 'text/markdown',
  },
  {
    uri: 'axiom://framework/formula',
    name: 'The Intelligence Formula',
    description: 'Detailed explanation of the intelligence formula',
    mimeType: 'text/markdown',
  },
  {
    uri: 'axiom://framework/layers',
    name: 'The Three Layers',
    description: 'Foundation, Dynamic, and Cognitive layers explained',
    mimeType: 'text/markdown',
  },
];

// Resource content
const RESOURCE_CONTENT: Record<string, string> = {
  'axiom://framework/overview': `# The Universal Axiom Framework

The Universal Axiom is a mathematical framework that models intelligence through immutable natural laws.

## The Formula

\`\`\`
Intelligence_n = E_n · (1 + F_n) · X · Y · Z · (A · B · C)
\`\`\`

## The Three Layers

1. **Foundation Layer (A · B · C)** - Physical Reality
2. **Dynamic Layer (E_n · (1 + F_n))** - Growth & Regulation
3. **Cognitive Layer (X · Y · Z)** - Alignment & Evolution`,

  'axiom://framework/formula': `# The Intelligence Formula

\`\`\`
Intelligence_n = E_n · (1 + F_n) · X · Y · Z · (A · B · C)
\`\`\`

**Foundation**: A (Impulses) · B (Elements) · C (Pressure)
**Dynamic**: E_n (Exponential) · (1 + F_n) (Fibonacci regulation)
**Cognitive**: X (Objectivity) · Y (Purpose) · Z (Time)`,

  'axiom://framework/layers': `# The Three Layers

## Foundation Layer (A · B · C)
- A: Impulses - fundamental drives
- B: Elements - core components
- C: Pressure - constraints and forces

## Dynamic Layer (E_n · (1 + F_n))
- E_n: Exponential growth potential
- F_n: Fibonacci regulation

## Cognitive Layer (X · Y · Z)
- X: Objectivity (1 - subjectivity)
- Y: Purpose alignment
- Z: Temporal continuity`,
};

// Helper functions
function createAxiomFromState(state: Record<string, unknown>): UniversalAxiom {
  const foundation = state.foundation as Record<string, number> | undefined;
  const cognitive = state.cognitive as Record<string, number> | undefined;

  return new UniversalAxiom({
    impulses: foundation?.A_impulses ?? 1.0,
    elements: foundation?.B_elements ?? 1.0,
    pressure: foundation?.C_pressure ?? 1.0,
    subjectivity: cognitive?.X_subjectivity ?? 0.0,
    purpose: cognitive?.Y_purpose ?? 1.0,
    time: cognitive?.Z_time ?? 1.0,
    n: (state.n as number) ?? 1,
  });
}

function generateRecommendations(state: AxiomState, coherence: number): string[] {
  const recommendations: string[] = [];

  if (state.foundation.product <= 0) {
    recommendations.push('❗ Critical: Foundation is negative or zero. Address impulses, elements, or pressure immediately.');
  } else if (state.foundation.C_pressure > 3) {
    recommendations.push('⚠️ High pressure detected. Consider reducing constraints or resolving contradictions.');
  }

  if (state.cognitive.X_subjectivity > 0.7) {
    recommendations.push('📊 High subjectivity. Increase objectivity by gathering data and reducing bias.');
  }

  if (state.cognitive.Y_purpose < 0.3) {
    recommendations.push('🎯 Low purpose alignment. Clarify goals and direction before proceeding.');
  }

  if (coherence < 0.4) {
    recommendations.push('🔧 Low coherence. System needs realignment across multiple dimensions.');
  } else if (coherence > 0.7) {
    recommendations.push('✅ High coherence. System is well-aligned and stable.');
  }

  if (recommendations.length === 0) {
    recommendations.push('✓ System appears balanced. Consider evolution or exploration.');
  }

  return recommendations;
}

// Tool execution
function executeTool(name: string, args: Record<string, unknown> = {}): unknown {
  switch (name) {
    case 'compute_intelligence': {
      const axiom = new UniversalAxiom(args as AxiomConfig);
      return axiom.getState();
    }

    case 'evolve_system': {
      const { current_state, steps = 1, delta_time = 1.0 } = args;
      const axiom = createAxiomFromState(current_state as Record<string, unknown>);
      const results: AxiomState[] = [];

      for (let i = 0; i < (steps as number); i++) {
        axiom.evolve(delta_time as number);
        results.push(axiom.getState());
      }

      return {
        steps: results.length,
        evolution: results,
        final_state: results[results.length - 1],
      };
    }

    case 'apply_pressure': {
      const { current_state, pressure_delta } = args;
      const axiom = createAxiomFromState(current_state as Record<string, unknown>);
      axiom.applyPressure(pressure_delta as number);

      return {
        pressure_applied: pressure_delta,
        new_state: axiom.getState(),
      };
    }

    case 'adjust_subjectivity': {
      const { current_state, subjectivity_delta } = args;
      const axiom = createAxiomFromState(current_state as Record<string, unknown>);
      axiom.adjustSubjectivity(subjectivity_delta as number);

      return {
        subjectivity_change: subjectivity_delta,
        new_state: axiom.getState(),
      };
    }

    case 'simulate_evolution': {
      const { steps = 10, delta_time = 1.0, ...params } = args;
      const axiom = new UniversalAxiom(params as AxiomConfig);
      const simulator = new AxiomSimulator(axiom);
      const history = simulator.simulateEvolution(steps as number, delta_time as number);

      return {
        simulation_type: 'evolution',
        steps,
        history,
        final_intelligence: history[history.length - 1].intelligence,
      };
    }

    case 'simulate_contradiction_resolution': {
      const { initial_pressure = 2.0, resolution_steps = 5, ...params } = args;
      const axiom = new UniversalAxiom(params as AxiomConfig);
      const simulator = new AxiomSimulator(axiom);
      const history = simulator.simulateContradictionResolution(
        initial_pressure as number,
        resolution_steps as number
      );

      return {
        simulation_type: 'contradiction_resolution',
        initial_pressure,
        resolution_steps,
        history,
        coherence_improvement:
          history[history.length - 1].cognitive.X_objectivity - history[0].cognitive.X_objectivity,
      };
    }

    case 'get_coherence_metric': {
      const { current_state } = args;
      const axiom = createAxiomFromState(current_state as Record<string, unknown>);
      const simulator = new AxiomSimulator(axiom);
      const coherence = simulator.getCoherenceMetric();

      return {
        coherence,
        interpretation:
          coherence > 0.7
            ? 'High coherence - system is well-aligned'
            : coherence > 0.4
            ? 'Moderate coherence - some adjustment needed'
            : 'Low coherence - significant realignment required',
        state: current_state,
      };
    }

    case 'analyze_permutation': {
      const axiom = new UniversalAxiom(args as AxiomConfig);
      const state = axiom.getState();
      const simulator = new AxiomSimulator(axiom);
      const coherence = simulator.getCoherenceMetric();

      return {
        foundation_layer: {
          status: state.foundation.product > 0 ? 'positive' : 'negative_or_zero',
          A_impulses: state.foundation.A_impulses,
          B_elements: state.foundation.B_elements,
          C_pressure: state.foundation.C_pressure,
          product: state.foundation.product,
        },
        dynamic_layer: {
          E_n: state.dynamic.E_n,
          F_n: state.dynamic.F_n,
          product: state.dynamic.product,
        },
        cognitive_layer: {
          objectivity: state.cognitive.X_objectivity,
          subjectivity: state.cognitive.X_subjectivity,
          purpose: state.cognitive.Y_purpose,
          time: state.cognitive.Z_time,
          product: state.cognitive.product,
        },
        overall: {
          intelligence: state.intelligence,
          coherence,
          recommendations: generateRecommendations(state, coherence),
        },
      };
    }

    case 'compare_permutations': {
      const { permutation_a, permutation_b, comparison_criteria = ['intelligence', 'coherence'] } = args;

      const axiomA = new UniversalAxiom(permutation_a as AxiomConfig);
      const axiomB = new UniversalAxiom(permutation_b as AxiomConfig);
      const stateA = axiomA.getState();
      const stateB = axiomB.getState();
      const simA = new AxiomSimulator(axiomA);
      const simB = new AxiomSimulator(axiomB);
      const coherenceA = simA.getCoherenceMetric();
      const coherenceB = simB.getCoherenceMetric();

      const comparison: Record<string, unknown> = {};
      const criteria = comparison_criteria as string[];

      if (criteria.includes('intelligence')) {
        comparison.intelligence = {
          permutation_a: stateA.intelligence,
          permutation_b: stateB.intelligence,
          winner: stateA.intelligence > stateB.intelligence ? 'A' : stateB.intelligence > stateA.intelligence ? 'B' : 'TIE',
        };
      }

      if (criteria.includes('coherence')) {
        comparison.coherence = {
          permutation_a: coherenceA,
          permutation_b: coherenceB,
          winner: coherenceA > coherenceB ? 'A' : coherenceB > coherenceA ? 'B' : 'TIE',
        };
      }

      return {
        permutation_a: stateA,
        permutation_b: stateB,
        comparison,
      };
    }

    case 'optimize_system': {
      const { current_state, optimization_goal = 'maximize_intelligence' } = args;
      const currentAxiom = createAxiomFromState(current_state as Record<string, unknown>);
      const currentState = currentAxiom.getState();
      const currentSim = new AxiomSimulator(currentAxiom);
      const currentCoherence = currentSim.getCoherenceMetric();

      const suggestions: Array<Record<string, unknown>> = [];

      if (currentState.cognitive.X_subjectivity > 0.3) {
        suggestions.push({
          variable: 'subjectivity',
          current: currentState.cognitive.X_subjectivity,
          suggested: Math.max(0, currentState.cognitive.X_subjectivity - 0.3),
          reason: 'Lower subjectivity increases objectivity',
        });
      }

      if (currentState.cognitive.Y_purpose < 0.8) {
        suggestions.push({
          variable: 'purpose',
          current: currentState.cognitive.Y_purpose,
          suggested: 1.0,
          reason: 'Stronger purpose alignment increases intelligence',
        });
      }

      return {
        current_metrics: {
          intelligence: currentState.intelligence,
          coherence: currentCoherence,
        },
        optimization_goal,
        suggestions,
      };
    }

    case 'predict_trajectory': {
      const { future_steps = 10, environmental_changes = {}, ...params } = args;
      const axiom = new UniversalAxiom(params as AxiomConfig);
      const envChanges = environmental_changes as Record<string, number>;

      const trajectory: AxiomState[] = [];
      trajectory.push(axiom.getState());

      for (let i = 0; i < (future_steps as number); i++) {
        if (envChanges.pressure_per_step) {
          axiom.applyPressure(envChanges.pressure_per_step);
        }
        if (envChanges.subjectivity_per_step) {
          axiom.adjustSubjectivity(envChanges.subjectivity_per_step);
        }
        axiom.evolve(1.0);
        trajectory.push(axiom.getState());
      }

      return {
        trajectory,
        steps: future_steps,
        environmental_changes,
      };
    }

    case 'detect_collapse_risk': {
      const { current_state } = args;
      const axiom = createAxiomFromState(current_state as Record<string, unknown>);
      const state = axiom.getState();
      const simulator = new AxiomSimulator(axiom);
      const coherence = simulator.getCoherenceMetric();

      const riskFactors: Array<Record<string, string>> = [];
      let riskScore = 0;

      if (state.foundation.product <= 0) {
        riskFactors.push({ factor: 'negative_foundation', severity: 'critical' });
        riskScore += 10;
      }

      if (state.foundation.C_pressure > 5) {
        riskFactors.push({ factor: 'extreme_pressure', severity: 'high' });
        riskScore += 6;
      }

      if (state.cognitive.X_subjectivity > 0.9) {
        riskFactors.push({ factor: 'extreme_subjectivity', severity: 'high' });
        riskScore += 5;
      }

      if (coherence < 0.2) {
        riskFactors.push({ factor: 'critical_coherence', severity: 'critical' });
        riskScore += 8;
      }

      return {
        risk_level: riskScore >= 10 ? 'critical' : riskScore >= 6 ? 'high' : riskScore >= 3 ? 'medium' : 'low',
        risk_score: riskScore,
        risk_factors: riskFactors,
        current_state: state,
      };
    }

    default:
      throw new Error(`Unknown tool: ${name}`);
  }
}

// MCP method handlers
function handleInitialize(): unknown {
  return {
    protocolVersion: SERVER_INFO.protocolVersion,
    capabilities: {
      tools: {},
      resources: {},
    },
    serverInfo: {
      name: SERVER_INFO.name,
      version: SERVER_INFO.version,
    },
  };
}

function handleListTools(): unknown {
  return { tools: TOOLS };
}

function handleCallTool(params: Record<string, unknown>): unknown {
  const { name, arguments: args } = params;
  const result = executeTool(name as string, (args as Record<string, unknown>) || {});

  return {
    content: [
      {
        type: 'text',
        text: JSON.stringify(result, null, 2),
      },
    ],
  };
}

function handleListResources(): unknown {
  return { resources: RESOURCES };
}

function handleReadResource(params: Record<string, unknown>): unknown {
  const { uri } = params;
  const content = RESOURCE_CONTENT[uri as string];

  if (!content) {
    throw new Error(`Resource not found: ${uri}`);
  }

  return {
    contents: [
      {
        uri,
        mimeType: 'text/markdown',
        text: content,
      },
    ],
  };
}

// Main request handler
function handleRequest(request: JsonRpcRequest): JsonRpcResponse {
  try {
    let result: unknown;

    switch (request.method) {
      case 'initialize':
        result = handleInitialize();
        break;
      case 'tools/list':
        result = handleListTools();
        break;
      case 'tools/call':
        result = handleCallTool(request.params || {});
        break;
      case 'resources/list':
        result = handleListResources();
        break;
      case 'resources/read':
        result = handleReadResource(request.params || {});
        break;
      case 'ping':
        result = {};
        break;
      default:
        return {
          jsonrpc: '2.0',
          id: request.id,
          error: {
            code: -32601,
            message: `Method not found: ${request.method}`,
          },
        };
    }

    return {
      jsonrpc: '2.0',
      id: request.id,
      result,
    };
  } catch (error) {
    return {
      jsonrpc: '2.0',
      id: request.id,
      error: {
        code: -32603,
        message: error instanceof Error ? error.message : String(error),
      },
    };
  }
}

// Vercel serverless handler
export default async function handler(
  req: VercelRequest,
  res: VercelResponse
): Promise<void> {
  // Enable CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  // Handle preflight
  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  // Health check endpoint
  if (req.method === 'GET') {
    res.status(200).json({
      name: SERVER_INFO.name,
      version: SERVER_INFO.version,
      status: 'healthy',
      endpoints: {
        mcp: 'POST /api/mcp',
        health: 'GET /api/mcp',
      },
    });
    return;
  }

  // MCP requests must be POST
  if (req.method !== 'POST') {
    res.status(405).json({ error: 'Method not allowed' });
    return;
  }

  try {
    const body = req.body as JsonRpcRequest | JsonRpcRequest[];

    // Handle batch requests
    if (Array.isArray(body)) {
      const responses = body.map(handleRequest);
      res.status(200).json(responses);
      return;
    }

    // Handle single request
    const response = handleRequest(body);
    res.status(200).json(response);
  } catch (error) {
    res.status(400).json({
      jsonrpc: '2.0',
      id: null,
      error: {
        code: -32700,
        message: 'Parse error',
        data: error instanceof Error ? error.message : String(error),
      },
    });
  }
}
