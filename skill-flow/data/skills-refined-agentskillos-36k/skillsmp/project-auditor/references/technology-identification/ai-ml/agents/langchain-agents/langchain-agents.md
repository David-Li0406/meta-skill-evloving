# LangChain Agents

**Category**: ai-ml/agents
**Description**: LangChain Agent implementations - autonomous AI agents that use tools and reasoning

## Package Detection

### NPM
- `langchain`
- `@langchain/core`
- `@langchain/langgraph`

### PYPI
- `langchain`
- `langchain-core`
- `langgraph`
- `langchain-experimental`

## Agent Pattern Detection

### Python Agent Patterns
File extensions: .py

**Pattern**: `from langchain\.agents import|from langchain_core\.agents import`
- LangChain agent imports
- Example: `from langchain.agents import AgentExecutor, create_openai_functions_agent`

**Pattern**: `AgentExecutor\(`
- Agent executor instantiation
- Example: `agent_executor = AgentExecutor(agent=agent, tools=tools)`

**Pattern**: `create_.*_agent\(`
- Agent factory functions
- Example: `create_openai_functions_agent`, `create_react_agent`, `create_tool_calling_agent`

**Pattern**: `@tool|from langchain\.tools import`
- Tool definitions for agents
- Example: `@tool\ndef search(query: str):`

**Pattern**: `BaseTool|StructuredTool`
- Custom tool implementations
- Example: `class MyTool(BaseTool):`

**Pattern**: `AgentType\.|agent_types`
- Agent type specifications
- Example: `AgentType.OPENAI_FUNCTIONS`

### JavaScript Agent Patterns
File extensions: .js, .ts

**Pattern**: `from ['"]@langchain/langgraph['"]`
- LangGraph agent orchestration
- Example: `import { StateGraph } from "@langchain/langgraph";`

**Pattern**: `AgentExecutor|createAgent`
- Agent creation in JavaScript
- Example: `const executor = AgentExecutor.fromAgentAndTools({ agent, tools })`

**Pattern**: `DynamicTool|DynamicStructuredTool`
- Dynamic tool creation
- Example: `new DynamicTool({ name: "search", func: async (input) => {...} })`

## LangGraph Patterns (Agentic Workflows)

**Pattern**: `StateGraph\(|from langgraph|import.*langgraph`
- LangGraph workflow definitions
- Example: `workflow = StateGraph(AgentState)`

**Pattern**: `\.add_node\(|\.add_edge\(`
- Graph node/edge definitions
- Example: `workflow.add_node("agent", agent_node)`

**Pattern**: `CompiledGraph|graph\.compile\(`
- Compiled graph execution
- Example: `app = workflow.compile()`

## Usage Classification

### Agent Types
- **ReAct Agents**: Reasoning + Acting pattern
- **Function Calling Agents**: OpenAI/Claude function calling
- **Tool Calling Agents**: Generic tool use
- **Plan and Execute**: Multi-step planning
- **LangGraph Agents**: Custom stateful workflows

### Risk Indicators
- **Autonomous Execution**: `AgentExecutor` with unrestricted tools
- **External API Calls**: Tools that access external services
- **File System Access**: Tools with read/write capabilities
- **Code Execution**: Tools that execute arbitrary code

## Detection Confidence

- **Agent Import Detection**: 95% (HIGH)
- **Tool Detection**: 90% (HIGH)
- **LangGraph Detection**: 95% (HIGH)
- **Usage Pattern Analysis**: 80% (MEDIUM)

## Security Considerations

- Agent tools may have access to sensitive resources
- Autonomous agents can make unexpected API calls
- Tool permissions should be scoped and reviewed
- Agent outputs should be validated before action
