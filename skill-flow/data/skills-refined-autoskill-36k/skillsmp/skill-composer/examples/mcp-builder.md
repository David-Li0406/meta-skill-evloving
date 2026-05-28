# Example: MCP Builder

**Source**: https://github.com/anthropics/skills/tree/main/mcp-builder
**Pattern**: Comprehensive four-phase framework with external references
**Use case**: Creating Model Context Protocol servers for LLM integration

## Key Sections from SKILL.md

### High-Level Workflow (4 Phases)

**Phase 1: Deep Research and Planning**
- 1.1 Understand agent-centric design principles
- 1.3 Study MCP protocol documentation (WebFetch from URL)
- 1.4 Study framework documentation
- 1.5 Exhaustively study API documentation
- 1.6 Create comprehensive implementation plan

**Phase 2: Implementation**
- 2.1 Set up project structure
- 2.2 Implement core infrastructure first
- 2.3 Implement tools systematically
- 2.4 Follow language-specific best practices

**Phase 3: Review and Refine**
- 3.1 Code quality review
- 3.2 Test and build
- 3.3 Use quality checklist

**Phase 4: Create Evaluations**
- 4.1 Understand evaluation purpose
- 4.2 Create 10 evaluation questions
- 4.3 Evaluation requirements
- 4.4 Output format (XML)

### Agent-Centric Design Principles (Quoted)

**"Build for Workflows, Not Just API Endpoints":**
Consolidate related operations into cohesive tools. Don't expose raw API endpoints.

**"Optimize for Limited Context":**
Agents have constrained context windows - make every token count.

**"Design Actionable Error Messages":**
Guide agents toward correct usage patterns. Suggest specific next steps.

**"Follow Natural Task Subdivisions":**
Tool names should reflect how humans think about tasks.

### External Documentation Loading

**WebFetch instructions**:
```markdown
Use WebFetch to load: `https://modelcontextprotocol.io/llms-full.txt`
```

**Reference files** (loaded during specific phases in original skill):
- Best Practices guide
- Python Implementation Guide
- TypeScript Implementation Guide
- Evaluation Guide

Note: These reference files exist in the original anthropics/skills repository, not in this example.

### Testing Warning

```markdown
**Important:** MCP servers are long-running processes that wait for
requests over stdio/stdin or sse/http. Running them directly in your main
process (e.g., `python server.py`) will cause your process to hang
indefinitely.

**Safe ways to test the server:**
- Use the evaluation harness (recommended)
- Run the server in tmux
- Use a timeout: `timeout 5s python server.py`
```

### 10 Evaluation Questions

Phase 4 requires creating 10 complex, realistic questions. Each must be:
- Independent
- Read-only
- Complex (requiring multiple tool calls)
- Realistic
- Verifiable (single, clear answer)
- Stable (answer won't change over time)

### Documentation Library Section

Lists all resources to load during development with clear phase guidance:
- Core MCP Documentation (Load First)
- SDK Documentation (Load During Phase 1/2)
- Language-Specific Guides (Load During Phase 2)
- Evaluation Guide (Load During Phase 4)

## Analysis

**What makes this work**:

1. **Four-phase structure**: Clear gates with deliverables
2. **Quoted design principles**: Core tenets as section headers
3. **External documentation integration**: WebFetch instructions
4. **Progressive file loading**: Load references during specific phases
5. **Multi-language support**: Python and TypeScript paths
6. **Evaluation framework**: 10 questions validate effectiveness
7. **Testing gotchas**: Explicit warning about hanging processes

## Unique Features

**Quoted Design Principles**:
Uses quoted headers like **"Build for Workflows, Not Just API Endpoints"** for emphasis and easy reference.

**WebFetch Integration**:
Explicitly instructs to use WebFetch tool to load external documentation:
- MCP protocol specification
- Python SDK README
- TypeScript SDK README

**Progressive Reference Loading**:
Tells when to load each reference file:
- Phase 1: mcp_best_practices.md
- Phase 2: python_mcp_server.md or node_mcp_server.md
- Phase 4: evaluation.md

**Testing Gotcha Section**:
Warns about hanging processes and provides three safe testing approaches.

**10 Evaluation Questions**:
Requires creating comprehensive evaluation with specific criteria for each question.

**Documentation Library**:
Comprehensive list of all references with emojis and phase guidance.

## Pattern Type

**Comprehensive framework guide** with:
- Four phases with deliverables
- External documentation integration
- Progressive reference loading
- Multi-language support
- Evaluation framework

## Key Takeaways

1. **Phase-based development** - Clear deliverables at each phase
2. **Quoted principles** - Design tenets as emphasized headers
3. **External documentation via WebFetch** - Load specs and SDKs dynamically
4. **Progressive disclosure** - Load references during specific phases
5. **Multi-language paths** - Python and TypeScript guidance
6. **Evaluation-driven development** - 10 questions validate effectiveness
7. **Testing gotchas** - Explicit warnings about common failures
8. **Agent-centric design** - Optimize for LLM usage, not human
