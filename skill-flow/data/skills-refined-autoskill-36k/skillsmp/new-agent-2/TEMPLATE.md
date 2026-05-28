# Agent Template

Use this template when creating a new agent.

## File: `Backend/src/agents/{name}_agent.py`

```python
"""
{Name} Agent - {Brief description of what this agent does}.

This agent handles {domain} tasks by interfacing with the {Service} MCP server.
"""

import os
from typing import Any

from anthropic import AsyncAnthropic

from src.agents.base import AgentContext, AgentResult, BaseAgent
from src.services.agent_execution_service import AgentExecutionService


# =============================================================================
# Tool Definitions
# =============================================================================

TOOL_DEFINITIONS = [
    {
        "name": "example_tool",
        "description": "Brief description of what this tool does. Be specific so Claude knows when to use it.",
        "input_schema": {
            "type": "object",
            "properties": {
                "param1": {
                    "type": "string",
                    "description": "Description of this parameter",
                },
                "param2": {
                    "type": "integer",
                    "description": "Description of this parameter",
                    "minimum": 1,
                    "maximum": 100,
                },
            },
            "required": ["param1"],
        },
    },
]


# =============================================================================
# System Prompt
# =============================================================================

SYSTEM_PROMPT = """You are the {Name} Agent, a specialized assistant for {domain} tasks.

## Available Tools

You have access to the following tools:

### example_tool
{Detailed description of when and how to use this tool}

## Guidelines

1. {Guideline 1}
2. {Guideline 2}
3. Always confirm destructive actions before executing

## Response Format

- Be concise and actionable
- Include relevant details from tool responses
- If an error occurs, explain what went wrong and suggest next steps
"""


# =============================================================================
# Agent Implementation
# =============================================================================

class {Name}Agent(BaseAgent):
    """
    {Name} Agent - handles {domain} tasks.

    Available tools:
        - example_tool: Brief description
    """

    name = "{name}_agent"
    description = "Handles {domain} tasks including {list of capabilities}"

    def __init__(
        self,
        db_session_factory,
        anthropic_api_key: str,
        mcp_base_url: str | None = None,
    ):
        super().__init__(db_session_factory)
        self.client = AsyncAnthropic(api_key=anthropic_api_key)
        self.mcp_base_url = mcp_base_url or os.getenv(
            "{NAME}_MCP_URL", "http://localhost:808X"
        )
        self.model = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-20250514")

    async def _execute(self, context: AgentContext) -> AgentResult:
        """Execute the agent's main logic."""
        execution_service = AgentExecutionService(context.session)

        # Create execution record
        execution = await execution_service.create_execution(
            agent_name=self.name,
            chat_id=context.chat_id,
            input_text=context.task,
            parent_execution_id=context.parent_execution_id,
        )

        try:
            result = await self._run_tool_loop(context, execution_service, execution)
            await execution_service.complete_execution(
                execution.id,
                output_text=result.message,
                success=result.success,
            )
            return result
        except Exception as e:
            await execution_service.complete_execution(
                execution.id,
                output_text=str(e),
                success=False,
                error=str(e),
            )
            return AgentResult(
                success=False,
                message=f"Error executing {self.name}: {e}",
                error=str(e),
            )

    async def _run_tool_loop(
        self,
        context: AgentContext,
        execution_service: AgentExecutionService,
        execution,
    ) -> AgentResult:
        """Run the tool calling loop until Claude returns a final response."""
        messages = [{"role": "user", "content": context.task}]

        while True:
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                system=SYSTEM_PROMPT,
                tools=TOOL_DEFINITIONS,
                messages=messages,
            )

            # Log token usage
            await execution_service.log_tokens(
                execution.id,
                input_tokens=response.usage.input_tokens,
                output_tokens=response.usage.output_tokens,
            )

            # Check for tool use
            tool_uses = [b for b in response.content if b.type == "tool_use"]

            if not tool_uses:
                # No more tools, extract final response
                text_content = next(
                    (b.text for b in response.content if b.type == "text"), ""
                )
                return AgentResult(success=True, message=text_content)

            # Process tool calls
            messages.append({"role": "assistant", "content": response.content})

            tool_results = []
            for tool_use in tool_uses:
                result = await self._handle_tool(
                    tool_use.name,
                    tool_use.input,
                    execution_service,
                    execution.id,
                )
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": tool_use.id,
                    "content": str(result),
                })

            messages.append({"role": "user", "content": tool_results})

    async def _handle_tool(
        self,
        tool_name: str,
        tool_input: dict[str, Any],
        execution_service: AgentExecutionService,
        execution_id,
    ) -> dict[str, Any]:
        """Handle a tool call and return the result."""
        try:
            match tool_name:
                case "example_tool":
                    result = await self._example_tool(**tool_input)
                case _:
                    result = {"error": f"Unknown tool: {tool_name}"}

            # Log tool call (use input_data/output_data, NOT tool_input/tool_output)
            await execution_service.log_tool_call(
                execution_id,
                tool_name=tool_name,
                input_data=tool_input,
                output_data=result,
            )

            return result

        except Exception as e:
            error_result = {"error": str(e)}
            await execution_service.log_tool_call(
                execution_id,
                tool_name=tool_name,
                input_data=tool_input,
                output_data=error_result,
            )
            return error_result

    # =========================================================================
    # Tool Implementations
    # =========================================================================

    async def _example_tool(self, param1: str, param2: int = 10) -> dict[str, Any]:
        """
        Example tool implementation.

        Args:
            param1: Description
            param2: Description with default

        Returns:
            Result dictionary
        """
        # If using MCP server:
        # async with httpx.AsyncClient() as client:
        #     response = await client.post(
        #         f"{self.mcp_base_url}/tools/example_tool",
        #         json={"param1": param1, "param2": param2},
        #         timeout=30.0,
        #     )
        #     response.raise_for_status()
        #     return response.json()

        return {
            "success": True,
            "param1": param1,
            "param2": param2,
        }
```

## Registration in `main.py`

```python
from src.agents.{name}_agent import {Name}Agent

# In lifespan():
registry.register({Name}Agent(
    db_session_factory=db_session_factory,
    anthropic_api_key=anthropic_api_key,
    mcp_base_url=f"http://{os.getenv('{NAME}_MCP_HOST', 'localhost')}:{os.getenv('{NAME}_MCP_PORT', '808X')}"
))
```

## Orchestrator Update

Add to the orchestrator's system prompt in `Backend/src/agents/orchestrator.py`:

```
X. **{Name} Operations** → Delegate to `{name}` agent (when available)
   - {Capability 1}
   - {Capability 2}
   - {Capability 3}
```

## Database Routing Table (CRITICAL!)

Insert into `routing.agents` table for hybrid router to work:

```sql
INSERT INTO routing.agents (name, display_name, description, keywords, regex_patterns, enabled, priority)
VALUES (
    '{name}',
    '{Name} Agent',
    '{Description - be specific about when to use this agent. Include action words.}',
    ARRAY['{keyword1}', '{keyword2}', '{keyword3}', '{keyword4}'],
    ARRAY[
        '\b({name}|{alias})\b',
        '\b({action1}|{action2}).*(noun)\b'
    ],
    true,
    {priority}  -- github=10, todo=20, email=30, calendar=40, motion=50, google_drive=60, resume=70
);
```

## Generate Embeddings

After database insert, restart backend or call:

```bash
curl -X POST http://localhost:8000/api/router/generate-embeddings
```

Verify with logs: `Router service initialized with X agents, X embeddings` - numbers should match.
