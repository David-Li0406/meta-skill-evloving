---
name: google-adk
description: Use this skill for developing agentic software and multi-agent systems using Google's Agent Development Kit (ADK) in Python.
---

# Google Agent Development Kit (ADK) Skill

## Purpose

Provide specialized guidance for developing agentic applications and multi-agent systems using Google's Agent Development Kit (ADK). Enable AI assistants to design agents, build tools, orchestrate multi-agent workflows, implement memory/state management, and deploy agent-based applications following code-first development patterns.

## When to Use This Skill

Invoke this skill when:

- Building conversational AI agents with tool integration
- Creating multi-agent orchestration systems
- Developing workflow agents (sequential, parallel, iterative)
- Implementing custom tools for agents
- Designing agent architectures for complex tasks
- Deploying agent applications to production
- Evaluating agent performance and behavior
- Implementing human-in-the-loop patterns

Do NOT use this skill for:

- Generic Python development (use Python-specific skills)
- Simple REST API development (ADK is for agentic systems)
- Frontend development (ADK is backend agent framework)
- Direct LLM API usage without agent orchestration (use LLM provider SDKs)
- Non-Python agent frameworks (LangChain, CrewAI, AutoGPT - different patterns)

## Core ADK Concepts

### Platform Architecture

**Framework Philosophy:**
- **Code-first approach** - Define agents in Python code (not YAML/JSON configs)
- **Model-agnostic** - Optimized for Gemini but supports other LLMs
- **Composable** - Build complex systems from simple agent primitives
- **Observable** - Built-in integration with tracing and monitoring tools

**Supported Languages:**
- **Python** (primary, most mature) - `google-adk` package
- **Go** (available) - `adk-go` repository
- **Java** (available) - `adk-java` repository

**Runtime Environment:**
- Python 3.9+ required
- Agent Engine for deployment (containerized execution)
- Web UI for development/testing (Angular + FastAPI)
- CLI for evaluation and deployment operations

### Agent Types and Hierarchy

**1. LlmAgent** (Dynamic, model-driven)

*Use for:*
- Conversational interfaces
- Decision-making with uncertainty
- Natural language understanding
- Creative tasks (content generation)
- Contextual reasoning

*Characteristics:*
- Uses LLM for decision-making
- Non-deterministic execution
- Tool selection driven by model
- Handles ambiguous inputs

**2. Workflow Agents** (Deterministic, programmatic)

*Sequential Agent:*
- Executes tools in fixed order
- Use for: Multi-step processes with dependencies
- Example: Data pipeline (fetch → transform → load)

*Parallel Agent:*
- Executes multiple tools concurrently
- Use for: Independent operations requiring aggregation
- Example: Multi-source data gathering

*Loop Agent:*
- Repeats execution until condition met
- Use for: Iterative refinement, convergence tasks
- Example: Generator-critic pattern

**3. Custom Agents** (User-defined logic)

*Use for:*
- Domain-specific orchestration
- Complex state machines
- Integration with existing systems
- Specialized execution patterns

**Agent Composition:**
- Agents can contain sub-agents (hierarchical)
- Parent agent coordinates child agents
- Supports multi-level nesting

### Tool Ecosystem

**Tool Categories:**

1. **Built-in Tools**:
   - **Search** - Web search via Google Search API
   - **Code Execution** - Python code interpreter (sandboxed)
   - **Google Cloud tools** - Vertex AI, BigQuery, Cloud Storage

2. **Custom Function Tools**:
   - Python functions wrapped as tools
   - Automatic schema generation from type hints
   - Supports async functions

3. **OpenAPI Tools**:
   - Auto-generate from OpenAPI/Swagger specs
   - HTTP-based service integration

4. **MCP (Model Context Protocol) Tools**:
   - Integration with MCP servers
   - Cross-framework tool sharing

**Tool Attributes:**
- **Name** - Unique identifier
- **Description** - Natural language explanation for LLM
- **Parameters** - JSON schema defining inputs
- **Function** - Execution logic
- **Confirmation** - Optional human-in-the-loop approval

### Memory and State Management

**Session Management:**
- Agent maintains conversation history
- Automatic context window management
- Configurable history retention

**State Persistence:**
- Custom state objects per agent
- Serialization support (JSON, pickle)
- Database integration for long-term storage

**Context Caching:**
- Reduces token usage for repeated context
- Automatic cache invalidation
- Configurable cache TTL

## Agent Development Methodology

### Planning Phase

**Step 1: Define Agent Purpose**
- Primary objective (single responsibility)
- Input/output format
- Success criteria
- Failure modes

**Step 2: Identify Required Tools**

Decision criteria:
- Use **built-in tools** when available (Search, Code Execution)
- Create **custom functions** for simple operations (<100 lines)
- Use **OpenAPI tools** for existing REST APIs
- Use **MCP tools** for cross-framework compatibility

**Step 3: Select Agent Type**

```
START: What's the agent's decision pattern?
  │
  ├─> Requires natural language reasoning? ─Yes─> LlmAgent ★
  │
  ├─> Fixed sequence of steps?
  │   └─> Sequential Workflow Agent ★
  │
  ├─> Independent parallel operations?
  │   └─> Parallel Workflow Agent ★
  │
  ├─> Iterative refinement needed?
  │   └─> Loop Workflow Agent ★
  │
  └─> Custom orchestration logic?
      └─> Custom Agent ★
```

**Step 4: Design Multi-Agent Architecture** (if needed)

Patterns:
- **Coordinator/Dispatcher** - Central agent routes to specialists
- **Sequential Pipeline** - Output of Agent A → Input of Agent B
- **Parallel Fan-Out/Gather** - Distribute work, aggregate results
- **Hierarchical Decomposition** - Break complex task into subtasks

### Implementation Phase

**Agent Implementation Examples:**

Key agent patterns demonstrated:
- **LlmAgent** - Conversational agent with custom tools
- **SequentialAgent** - Ordered execution (fetch → transform → save)
- **ParallelAgent** - Concurrent tool execution
- **LoopAgent** - Iterative refinement with break conditions
- **Session Management** - Multi-turn conversation with history

### Testing Phase

**Web UI Testing:**

```bash
# Start API server
adk api_server --port 8000

# Start web UI (separate terminal)
cd adk-web
npm install
npm start
# Access: http://localhost:4200
```

**Programmatic Testing:**

```python
# Unit test for agent
def test_weather_agent():
    agent = create_weather_agent()
    response = agent.run("Weather in NYC?")
    assert "weather" in response.content.lower()
    assert response.success is True

# Integration test with mock tools
def test_pipeline_agent():
    agent = create_pipeline_agent(mock_tools=True)
    result = agent.run({"input": "test_data"})
    assert result["status"] == "completed"
```

## Deployment Options

### Agent Engine (Managed Service)

**Deployment Commands:**
```bash
pip install google-adk[cli]
adk auth login
adk deploy --agent-file agent.py --agent-name my_agent --project-id my-gcp-project --region us-central1
```

### Cloud Run Deployment

**Components:**
- FastAPI server with agent endpoints
- Dockerfile for containerization
- Health check and error handling
- Environment configuration

### Docker Containerization

**Self-Hosted Options:**
- Docker Compose with Redis
- Single container deployment
- Environment variable configuration

### Resource Requirements

| Agent Complexity | CPU | RAM | Concurrent Requests |
|------------------|-----|-----|---------------------|
| Simple LlmAgent | 1 core | 512MB | 10 |
| Workflow Agent | 2 cores | 1GB | 20 |
| Multi-Agent (3-5 agents) | 4 cores | 2GB | 10 |
| Complex Multi-Agent (>5) | 8 cores | 4GB | 5 |

## Evaluation and Testing

### Criteria-Based Evaluation

**Pattern:**
- Define custom evaluation criteria (accuracy, helpfulness, etc.)
- Run test cases against agent
- Analyze pass rate and scores

## Best Practices

### Agent Instruction Writing

**Effective Patterns:**
- Clear role and responsibilities
- Structured format with constraints
- Specific tool usage guidance
- Example interactions

### Tool Design Principles

**Key Principles:**
1. **Single Responsibility** - One clear purpose per tool
2. **Descriptive Naming** - Clear action and object naming
3. **Type Hints** - Complete type annotations for all parameters

### Error Handling

**Strategies:**
- **Graceful Degradation** - Return error messages instead of raising exceptions
- **Retry Logic** - Automatic retry with exponential backoff
- **Input Validation** - Validate and sanitize all inputs

### Security and Safety

**Implementation:**
- **Input Validation** - Email format validation, length limits
- **Rate Limiting** - Decorator-based request throttling
- **Sanitization** - Remove dangerous HTML/script content

### Performance Optimization

**Async Tools:**
- Automatic parallel execution for async functions
- Improved throughput for I/O-bound operations

## References

### Official Documentation
- **Main docs:** https://google.github.io/adk-docs/
- **Python SDK:** https://github.com/google/adk-python
- **Examples:** https://github.com/google/adk-samples
- **Web UI:** https://github.com/google/adk-web

### Community Resources
- **GitHub Discussions:** https://github.com/google/adk-python/discussions
- **Issue Tracker:** https://github.com/google/adk-python/issues

---

**Version:** 1.0.0
**Last Updated:** 2025-11-13
**Complexity Rating:** 3 (Moderate - requires agent architecture knowledge)
**Estimated Learning Time:** 10-15 hours for proficiency