# Agent Strategy Plugin Development

Agent Strategy plugins implement custom reasoning strategies for Dify agents (e.g., Function Calling, ReAct).

## File Structure

```
my-agent-strategy/
├── manifest.yaml                # Plugin manifest
├── main.py                      # Entry point
├── pyproject.toml               # Dependencies (uv)
├── README.md                    # Documentation
├── _assets/
│   └── icon.svg                 # Plugin icon
├── provider/
│   └── {provider_name}.yaml     # Provider config
└── strategies/
    ├── {strategy_name}.yaml     # Strategy definition (parameters)
    └── {strategy_name}.py       # Strategy implementation
```

## manifest.yaml

```yaml
version: 0.0.1
type: plugin
author: your-name
name: my_agent_strategy
label:
  en_US: My Agent Strategy
  zh_Hans: 我的 Agent 策略
description:
  en_US: Custom agent reasoning strategies
icon: icon.svg

meta:
  version: 0.0.1
  arch: [amd64, arm64]
  runner:
    language: python
    version: "3.12"
    entrypoint: main
  minimum_dify_version: "1.7.0"

plugins:
  agent_strategies:              # Note: agent_strategies
    - provider/my_agent.yaml

resource:
  memory: 1048576
  permission:
    tool:
      enabled: true              # Agent needs tool access
    model:
      enabled: true              # Agent needs model access
      llm: true
```

## provider.yaml

```yaml
identity:
  author: your-name
  name: my_agent
  label:
    en_US: My Agent
    zh_Hans: 我的 Agent
  description:
    en_US: Custom agent reasoning strategies
  icon: icon.svg

strategies:
  - strategies/function_calling.yaml
  - strategies/react.yaml

extra:
  python:
    source: provider/my_agent.py
```

## strategy.yaml

```yaml
identity:
  name: function_calling
  author: your-name
  label:
    en_US: Function Calling
    zh_Hans: 函数调用

description:
  en_US: Agent strategy using model's native function calling capability
  zh_Hans: 使用模型原生函数调用能力的 Agent 策略

features:
  - agent-loop-status            # Shows agent loop progress in UI

parameters:
  - name: model
    type: model-selector
    scope: tool-call             # Model must support tool calling
    required: true
    label:
      en_US: Model
      zh_Hans: 模型

  - name: tools
    type: array[tools]
    required: true
    label:
      en_US: Tool list
      zh_Hans: 工具列表

  - name: instruction
    type: string
    required: true
    label:
      en_US: Instruction
      zh_Hans: 指令
    auto_generate:
      type: prompt_instruction
    template:
      enabled: true

  - name: query
    type: string
    required: true
    label:
      en_US: Query
      zh_Hans: 查询

  - name: maximum_iterations
    type: number
    required: true
    default: 3
    min: 1
    max: 30
    label:
      en_US: Maximum Iterations
      zh_Hans: 最大迭代次数

  - name: context
    type: any
    scope: array[object]
    required: false
    label:
      en_US: Context
      zh_Hans: 上下文

extra:
  python:
    source: strategies/function_calling.py
```

## Provider Implementation

```python
from dify_plugin.interfaces.agent import AgentProvider

class MyAgentProvider(AgentProvider):
    """Agent Provider - usually empty implementation"""
    pass
```

## Strategy Implementation

```python
from typing import Any, Generator
from dify_plugin.interfaces.agent import AgentStrategy, AgentModelConfig, ToolEntity
from dify_plugin.entities.agent import AgentInvokeMessage
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.entities.model.llm import LLMUsage
from dify_plugin.entities.model.message import (
    AssistantPromptMessage,
    PromptMessage,
    SystemPromptMessage,
    ToolPromptMessage,
    UserPromptMessage,
)

class FunctionCallingStrategy(AgentStrategy):
    def _invoke(
        self, parameters: dict[str, Any]
    ) -> Generator[AgentInvokeMessage, None, None]:
        """Core execution method"""
        # Extract parameters
        query = parameters.get("query", "")
        instruction = parameters.get("instruction", "")
        model_config: AgentModelConfig = parameters.get("model")
        tools: list[ToolEntity] = parameters.get("tools", [])
        max_iterations = parameters.get("maximum_iterations", 3)

        # Initialize tools
        tools = self._init_prompt_tools(tools)

        # Build prompt messages
        messages = self._build_messages(instruction, query)

        # Start iteration log
        iteration_log = self.create_log_message(
            label="Agent Loop",
            data={},
            status=ToolInvokeMessage.LogMessage.LogStatus.START
        )
        yield iteration_log

        # Agent loop
        llm_usage = {"usage": LLMUsage.empty_usage()}
        iteration = 0

        while iteration < max_iterations:
            iteration += 1

            # Call LLM
            llm_result = self._invoke_llm(
                model_config=model_config,
                messages=messages,
                tools=tools
            )

            # Process response
            assistant_message = llm_result.message
            messages.append(assistant_message)

            # Update usage
            if llm_result.usage:
                self.increase_usage(llm_usage, llm_result.usage)

            # Check for tool calls
            tool_calls = assistant_message.tool_calls
            if not tool_calls:
                # No more tool calls, output final response
                yield self.create_text_message(assistant_message.content or "")
                break

            # Execute tool calls
            for tool_call in tool_calls:
                tool_result = self._execute_tool(tool_call, tools)
                messages.append(ToolPromptMessage(
                    content=tool_result,
                    tool_call_id=tool_call.id,
                    name=tool_call.function.name
                ))

        # Finish iteration log
        yield self.finish_log_message(
            log=iteration_log,
            data={"iterations": iteration},
            metadata={"usage": llm_usage["usage"]}
        )

    def _build_messages(
        self, instruction: str, query: str
    ) -> list[PromptMessage]:
        """Build initial prompt messages"""
        messages = []

        if instruction:
            messages.append(SystemPromptMessage(content=instruction))

        messages.append(UserPromptMessage(content=query))

        return messages

    def _invoke_llm(
        self,
        model_config: AgentModelConfig,
        messages: list[PromptMessage],
        tools: list[ToolEntity]
    ):
        """Invoke LLM with tools"""
        return self.session.model.llm.invoke(
            model_config=model_config,
            prompt_messages=messages,
            tools=tools,
            stream=False
        )

    def _execute_tool(
        self, tool_call, tools: list[ToolEntity]
    ) -> str:
        """Execute a tool call"""
        tool_name = tool_call.function.name
        tool_args = tool_call.function.arguments

        # Find and invoke tool
        result = self.session.tool.invoke(
            provider_type=ToolProviderType.BUILT_IN,
            provider=tool_name.split("/")[0],
            tool_name=tool_name.split("/")[-1],
            parameters=tool_args
        )

        return str(result)
```

## ReAct Strategy Pattern

```python
class ReActStrategy(AgentStrategy):
    """ReAct: Thought-Action-Observation pattern"""

    REACT_PROMPT = """Answer the following questions as best you can.
You have access to the following tools:
{tools}

Use the following format:
Question: the input question
Thought: think about what to do
Action: the action to take, one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (repeat Thought/Action/Observation)
Thought: I now know the final answer
Final Answer: the final answer

Begin!
Question: {query}
Thought:"""

    def _invoke(self, parameters: dict[str, Any]) -> Generator[AgentInvokeMessage, None, None]:
        query = parameters.get("query")
        tools = parameters.get("tools", [])
        max_iterations = parameters.get("maximum_iterations", 5)

        # Build initial prompt
        prompt = self._build_react_prompt(query, tools)
        scratchpad = ""

        for i in range(max_iterations):
            # Call LLM with stop tokens
            response = self._invoke_llm_with_stop(
                prompt + scratchpad,
                stop=["Observation:"]
            )

            # Parse thought and action
            thought, action, action_input = self._parse_response(response)

            yield self.create_log_message(
                label=f"Thought {i+1}",
                data={"thought": thought, "action": action}
            )

            if action == "Final Answer":
                yield self.create_text_message(action_input)
                return

            # Execute action
            observation = self._execute_tool(action, action_input, tools)

            # Add to scratchpad
            scratchpad += f"{response}\nObservation: {observation}\nThought:"

        yield self.create_text_message("Max iterations reached")
```

## Parameter Types

| Type | Description | Example |
|------|-------------|---------|
| `model-selector` | Model picker with scope | LLM selection |
| `array[tools]` | Tool list selector (Agent-specific) | Available tools |
| `string` | Text input | Query, instruction |
| `number` | Numeric with min/max | max_iterations |
| `boolean` | True/false | enable_streaming |
| `select` | Dropdown selection | strategy_mode |
| `secret-input` | Encrypted input | api_key |
| `file` | Single file | context_file |
| `files` | Multiple files | reference_docs |
| `app-selector` | Dify app picker | app reference |
| `any` | Flexible type with scope | Context data |

**Note**: `array[tools]` is unique to Agent Strategy plugins, allowing selection of available tools for the agent loop.

## Message Types

```python
# Log message (for agent loop tracking)
yield self.create_log_message(
    label="Step 1",
    data={"action": "search"},
    status=ToolInvokeMessage.LogMessage.LogStatus.START
)

# Finish log message
yield self.finish_log_message(
    log=log_message,
    data={"result": "success"},
    metadata={"usage": llm_usage}
)

# Text response
yield self.create_text_message("Final answer")

# JSON response
yield self.create_json_message({"status": "complete"})

# Retriever resource (for RAG)
yield self.create_retriever_resource_message(
    retriever_resources=resources,
    context="Context text"
)
```

## Key Interfaces

```python
from dify_plugin.interfaces.agent import (
    AgentStrategy,        # Base class for strategies
    AgentProvider,        # Base class for provider
    AgentModelConfig,     # Model configuration
    ToolEntity,           # Tool definition
)

from dify_plugin.entities.agent import AgentInvokeMessage
from dify_plugin.entities.tool import ToolInvokeMessage, ToolProviderType
from dify_plugin.entities.model.llm import LLMUsage
```

## Session Access

```python
# Invoke LLM
result = self.session.model.llm.invoke(
    model_config=model_config,
    prompt_messages=messages,
    tools=tools,
    stream=True  # or False
)

# Invoke tool
result = self.session.tool.invoke(
    provider_type=ToolProviderType.BUILT_IN,
    provider="google",
    tool_name="google_search",
    parameters={"query": "search term"}
)
```

## Strategy Features

```yaml
features:
  - agent-loop-status   # Shows agent loop progress in UI
```

## Best Practices

1. **Use logging** - Create log messages for each iteration step
2. **Track usage** - Accumulate LLM token usage with `increase_usage()`
3. **Handle iterations** - Implement proper loop termination conditions
4. **Initialize tools** - Call `_init_prompt_tools()` before using tools
5. **Stream responses** - Use generators for real-time output
6. **Parse carefully** - Handle malformed LLM outputs gracefully
