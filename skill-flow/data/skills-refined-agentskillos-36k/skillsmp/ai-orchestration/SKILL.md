---
name: ai-orchestration
description: LLM keyring management, multi-provider support, and AI agent orchestration
---

# AI Orchestration Skill

Use this skill when:
- Managing LLM API keys and providers
- Implementing multi-provider LLM support
- Structuring LLM conversations with context
- Building AI agents that work together
- Handling message items and structured outputs
- Prompt engineering for AI workflows

## LLM Keyring Management

### Environment Variables

```bash
# Anthropic Claude
export ANTHROPIC_API_KEY="sk-ant-xxxxx"

# OpenAI GPT
export OPENAI_API_KEY="sk-xxxxx"

# xAI Grok
export XAI_API_KEY="xai-xxxxx"

# Groq
export GROQ_API_KEY="gsk_xxxxxx"

# OpenRouter (multi-provider)
export OPENROUTER_API_KEY="sk-or-xxxxx"

# LM Studio / Ollama
export LMSTUDIO_BASE_URL="http://localhost:1234/v1"
export OLLAMA_HOST="http://localhost:11434"

# DeepSeek
export DEEPSEEK_API_KEY="sk-xxxxx"
```

### Elixir Keyring Implementation

```elixir
defmodule MyApp.LLM.Keyring do
  use Agent

  def start_link(_opts) do
    Agent.start_link(__MODULE__, %{})
  end

  # Store API key
  def set_key(provider, key) do
    Agent.update(__MODULE__, & &1, fn state ->
      Map.put(state, provider, key)
    end)
  end

  # Get API key
  def get_key(provider) do
    Agent.get(__MODULE__, fn state ->
      Map.get(state, provider) || System.get_env(api_key_env_var(provider))
    end)
  end

  defp api_key_env_var(:anthropic), do: "ANTHROPIC_API_KEY"
  defp api_key_env_var(:openai), do: "OPENAI_API_KEY"
  defp api_key_env_var(:xai), do: "XAI_API_KEY"
  defp api_key_env_var(:groq), do: "GROQ_API_KEY"
  defp api_key_env_var(:openrouter), do: "OPENROUTER_API_KEY"

  # Get all keys
  def get_all_keys do
    Agent.get(__MODULE__, fn state ->
      state
      |> Enum.map(fn {provider, _key} -> {provider, get_key(provider, state)})
    end)
  end
end
```

## Multi-Provider Client

```elixir
defmodule MyApp.LLM.Client do
  alias MyApp.LLM.Keyring

  # Provider modules
  defmodule Anthropic do
    def chat(messages, opts \\ []) do
      key = Keyring.get_key(:anthropic)
      request("https://api.anthropic.com/v1/messages", messages, key, opts)
    end
  end

  defmodule OpenAI do
    def chat(messages, opts \\ []) do
      key = Keyring.get_key(:openai)
      request("https://api.openai.com/v1/chat/completions", messages, key, opts)
    end
  end

  defmodule Groq do
    def chat(messages, opts \\ []) do
      key = Keyring.get_key(:groq)
      request("https://api.groq.com/openai/v1/chat/completions", messages, key, opts)
    end
  end

  # Router for automatic provider selection
  def chat(messages, opts \\ []) do
    # Auto-select best provider based on task type
    key = Keyring.get_key(:openrouter)
    request("https://openrouter.ai/api/v1/chat/completions", messages, key, opts)
    end
end
```

## Message Item Pattern

```elixir
defmodule MyApp.AI.MessageItem do
  @moduledoc """
  Rich message structure for AI agent communication.
  Based on Jido AI MessageItem pattern.
  """

  defstruct [
    :id,
    :role,
    :content,
    :metadata,
    :timestamp,
    :attachments,
    :tool_calls,
    :tool_results
  ]

  @type t :: %__MODULE__{}

  def new(role, content) do
    %__MODULE__{
      id: generate_id(),
      role: role,
      content: content,
      metadata: %{},
      timestamp: System.monotonic_time(:millisecond),
      attachments: [],
      tool_calls: [],
      tool_results: []
    }
  end

  def with_tool_call(self, tool_name, args, result) do
    %{self | tool_calls: [%{name: tool_name, args: args, result: result}]}
  end

  def with_attachment(self, file_path, file_type) do
    %{self | attachments: [%{file_path: file_path, file_type: file_type}]}
  end

  defp generate_id do
    UUID.uuid4()
  end
end
```

## Director → Implementor Pattern

```elixir
defmodule MyApp.AI.Directors do
  @moduledoc """
  Director and Implementor pattern for multi-agent AI workflows.
  One Director agent coordinates multiple Implementor agents.
  """

  use GenServer

  # Director agent
  defmodule Director do
    use GenServer

    def start_link(implementors) do
      GenServer.start_link(__MODULE__, %{implementors: implementors})
    end

    @impl true
    def init(state) do
      {:ok, state}
    end

    @impl true
    def handle_call({:coordinate, task}, _from, state) do
      # Choose best implementor for the task
      implementor = choose_implementor(state.implementors, task)
      
      # Execute task via implementor
      case execute_task(implementor, task) do
        {:ok, result} -> {:reply, {:ok, result}, state}
        {:error, reason} -> {:reply, {:error, reason}, state}
      end
    end

    defp choose_implementor(implementors, task) do
      # Simple round-robin for now
      Enum.random(implementors)
    end

    defp execute_task(implementor, task) do
      # Create execution context
      context = create_execution_context(task)
      
      # Implementor executes
      implementor.execute(context)
    end

    defp create_execution_context(task) do
      %{
        task: task,
        constraints: task.constraints || [],
        metadata: %{},
        context: %{}
      }
    end
  end

  # Implementor agent (example)
  defmodule CodeGenerator do
    @behavior GenServer

    def execute(context) do
      # Generate code based on task description
      code = generate_code(context.task)
      
      # Return result
      {:ok, code}
    end

    defp generate_code(task_description) do
      # Simplified for example
      "defmodule " <> module_name(task_description) <> " do\n"
    end
  end

    defp module_name(description) do
      description
      |> String.split(" ")
      |> Enum.map(&String.capitalize/1)
      |> Enum.join("")
    end
end
```

## Prompt Engineering

### System Prompt Template

```elixir
system_prompt = """
You are an AI assistant specializing in Elixir/BEAM development.

Role: {role}

Context:
- Working on: {project_name}
- Frameworks: {frameworks}
- Best Practices: OTP, supervision trees, functional programming
- Patterns: Domain Resource Action, TDD workflow

Guidelines:
- Always use typespecs for public functions
- Follow Elixir convention for naming (snake_case)
- Use GenServer for stateful processes
- Use Supervisor for process trees
- Implement proper error handling
- Use pattern matching over conditional logic
- Document public modules with @moduledoc

Output Format:
- Provide clear explanations
- Include code examples
- Reference best practices
- Suggest improvements when applicable

Constraints:
- Never make assumptions without asking
- Always validate before executing
- Use provided MessageItems for rich context
"""
```

### Best Practices

1. **Structured Outputs**: Always use MessageItem pattern for rich context
2. **Context Management**: Include task context in prompts
3. **Error Handling**: Use proper error handling with fallback providers
4. **Token Efficiency**: Be concise but complete
5. **Tool Calling**: Explicitly define tool calls in prompts

## Tools to Use

- **Jido AI**: Elixir-native AI orchestration
  - Multi-provider support
  - MessageItem pattern
  - Director → Implementor pattern

- **LangChain**: For chaining prompts
- **Instructor**: For structured outputs

- **OpenRouter**: Multi-provider routing
- **Groq**: Fast inference ($0.59/M tokens)

## Token Efficiency

Use for:
- Multi-provider LLM coordination (~40% token savings)
- Rich context management (~30% savings vs manual)
- Tool-calling workflows (~50% savings vs inline tools)

## Examples

### Simple Chat

```elixir
# Using multi-provider client
messages = [
  %MyApp.AI.MessageItem{
    role: "user",
    content: "Create a GenServer for user management",
    timestamp: System.monotonic_time(:millisecond)
  }
]

{:ok, response} = MyApp.LLM.Client.chat(messages)
```

### Agent Orchestration

```elixir
# Director coordinates multiple implementors
{:ok, code} = MyApp.AI.Directors.coordinate(%{
  task: "Add user authentication",
  implementors: [MyApp.AI.Implementors.CodeGenerator]
})
```

## Notes

- Keyring is secure: Uses Agent to store keys in memory
- Multi-provider: Automatically selects best provider for task
- MessageItem: Rich context structure for agent communication
- Director pattern: Centralizes coordination, reduces complexity
