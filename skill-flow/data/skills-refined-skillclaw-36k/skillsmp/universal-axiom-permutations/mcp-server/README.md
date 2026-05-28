# Universal Axiom MCP Server

A Model Context Protocol (MCP) server that exposes The Universal Axiom framework as tools and resources for AI assistants.

## What is This?

This MCP server allows AI assistants (like Claude) to:
- **Use The Universal Axiom** to reason about any problem
- **Compute intelligence values** using the axiom formula
- **Simulate system evolution** and contradiction resolution
- **Access framework documentation** and examples
- **Apply multiplicative reasoning** instead of traditional additive logic

## Features

### Tools (12 Total)

The server provides these tools for AI assistants:

#### Core Intelligence Tools
1. **`compute_intelligence`** - Calculate intelligence using the formula: `Intelligence_n = E_n · (1 + F_n) · X · Y · Z · (A · B · C)`
2. **`evolve_system`** - Evolve a system forward in time
3. **`apply_pressure`** - Apply pressure changes (contradictions, constraints)
4. **`adjust_subjectivity`** - Move toward objectivity or subjectivity

#### Simulation Tools
5. **`simulate_evolution`** - Simulate evolution over multiple steps
6. **`simulate_contradiction_resolution`** - See how contradictions resolve through the axiom
7. **`predict_trajectory`** - 🆕 Forecast future system evolution with environmental changes

#### Analysis Tools
8. **`analyze_permutation`** - Get diagnostic analysis and recommendations
9. **`get_coherence_metric`** - Measure system coherence
10. **`compare_permutations`** - 🆕 Compare two systems across multiple criteria
11. **`detect_collapse_risk`** - 🆕 Analyze collapse risk with severity assessment

#### Optimization Tools
12. **`optimize_system`** - 🆕 Get intelligent suggestions for improving system variables

### Resources

Documentation and examples accessible via MCP:

- Framework overview and formula
- Layer explanations (Foundation, Dynamic, Cognitive)
- Reasoning guides
- Examples: debugging, decision-making, and more

### Prompts

Pre-built prompts for common reasoning patterns:

- **`analyze_problem`** - Analyze any problem using the framework
- **`reason_with_axiom`** - Apply axiom reasoning for novel insights

## Installation

### Prerequisites

- Node.js 16 or higher
- npm or yarn

### Setup

1. **Navigate to the MCP server directory**:
   ```bash
   cd mcp-server
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Build the server**:
   ```bash
   npm run build
   ```

## Usage

### With Claude Desktop

Add this to your Claude Desktop configuration (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "universal-axiom": {
      "command": "node",
      "args": ["/absolute/path/to/pointy-stick/mcp-server/build/mcp-server/index.js"]
    }
  }
}
```

**Configuration file locations:**
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

### With Other MCP Clients

The server uses stdio transport and follows the MCP specification. Run it with:

```bash
npm start
```

Or execute directly:

```bash
node build/index.js
```

## Example Usage

Once connected to an MCP client, you can use tools like:

```typescript
// Compute intelligence for a given permutation
compute_intelligence({
  impulses: 1.5,
  elements: 2.0,
  pressure: 1.2,
  subjectivity: 0.3,
  purpose: 1.0,
  time: 2.0,
  n: 5
})

// Analyze a permutation with diagnostics
analyze_permutation({
  impulses: 1.0,
  elements: -0.5,  // Detrimental element
  pressure: 3.0,   // High pressure
  subjectivity: 0.8,  // High subjectivity
  purpose: 0.4,
  time: 1.0,
  n: 3
})

// Simulate contradiction resolution
simulate_contradiction_resolution({
  subjectivity: 0.7,
  initial_pressure: 2.5,
  resolution_steps: 5
})
```

## The Universal Axiom Framework

### The Formula

```
Intelligence_n = E_n · (1 + F_n) · X · Y · Z · (A · B · C)
```

### The Three Layers

1. **Foundation Layer (A · B · C)** - Physical Reality
   - **A (Impulses)**: Fundamental drives (can be ±)
   - **B (Elements)**: Core components (beneficial/detrimental)
   - **C (Pressure)**: Constraints and forces (constructive/destructive)

2. **Dynamic Layer (E_n · (1 + F_n))** - Growth & Regulation
   - **E_n**: Exponential growth `(2 × 3^n) - 1`
   - **F_n**: Fibonacci regulation (natural constraint)

3. **Cognitive Layer (X · Y · Z)** - Alignment & Evolution
   - **X**: Objectivity `(1 - subjectivity)`
   - **Y**: Purpose alignment
   - **Z**: Temporal continuity

### Key Principles

- **Multiplicative, not additive**: Any zero collapses the system
- **Emergence over construction**: Conditions create solutions
- **Contradictions as fuel**: Pressure reveals misalignment
- **Time is irreversible**: Systems evolve, cannot stagnate

## Development

### Build

```bash
npm run build
```

### Watch mode

```bash
npm run dev
```

### Project Structure

```
mcp-server/
├── index.ts           # Main server implementation
├── package.json       # Package configuration
├── tsconfig.json      # TypeScript configuration
├── build/             # Compiled output (generated)
└── README.md          # This file
```

## How It Works

The MCP server:

1. **Exposes tools** that AI assistants can call
2. **Provides resources** (documentation, examples)
3. **Offers prompts** for common reasoning patterns
4. **Uses stdio transport** for communication

When an AI assistant needs to:
- Reason about a complex problem
- Analyze system dynamics
- Resolve contradictions
- Make decisions with multiplicative thinking

It can use these tools to apply The Universal Axiom framework.

## Why MCP?

The Model Context Protocol allows:
- **Standardized integration** with AI assistants
- **Tool exposure** without custom APIs
- **Resource sharing** (documentation, examples)
- **Prompt templates** for common patterns
- **Local execution** (no cloud dependencies)

## Learn More

- **Main Repository**: [github.com/TheUniversalAxiom/pointy-stick](https://github.com/TheUniversalAxiom/pointy-stick)
- **Website**: [www.epiphanyengine.ai](https://www.epiphanyengine.ai)
- **MCP Documentation**: [modelcontextprotocol.io](https://modelcontextprotocol.io)

## License

MIT - See LICENSE file in the root repository

---

**The Axiom doesn't answer questions. It generates the conditions from which answers must emerge.**
