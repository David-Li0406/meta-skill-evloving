# Todo Agent with MCP Integration

A complete example of an AI agent for task management using Gemini via LiteLLM and MCP tools.

## Full Implementation

```python
"""
Todo AI Agent with MCP Server Integration

This agent connects to an MCP server to manage tasks using natural language.
Uses Gemini via LiteLLM for the language model.

Requirements:
    pip install "openai-agents[litellm]"

Environment:
    GOOGLE_API_KEY=your-gemini-api-key

Usage:
    python todo_agent.py
"""

import asyncio
import os
from agents import Agent, Runner, set_tracing_disabled
from agents.mcp import MCPServerStreamableHttp
from agents.extensions.models.litellm_model import LitellmModel
from agents.extensions.handoff_prompt import prompt_with_handoff_instructions

# Disable OpenAI tracing (not needed for Gemini)
set_tracing_disabled(disabled=True)


# ============================================================================
# Configuration
# ============================================================================

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:8000/api/mcp")
USER_ID = "demo-user"  # In production, get from auth


# ============================================================================
# Agent Instructions
# ============================================================================

TASK_AGENT_INSTRUCTIONS = prompt_with_handoff_instructions("""
You are a helpful task management assistant.

## Your Capabilities
You can help users manage their tasks using these MCP tools:

- **add_task**: Create new tasks
  - Required: user_id, title
  - Optional: description, priority (low/medium/high), due_date (YYYY-MM-DD)

- **list_tasks**: View existing tasks
  - Required: user_id
  - Optional: status (pending/in_progress/completed/all), priority (low/medium/high/all)

- **complete_task**: Mark a task as completed
  - Required: user_id, task_id

- **delete_task**: Remove a task
  - Required: user_id, task_id

- **update_task**: Modify task details
  - Required: user_id, task_id
  - Optional: title, description, status, priority, due_date

## Guidelines
1. Always use user_id="{user_id}" when calling tools
2. Confirm actions with the user after performing them
3. When listing tasks, format them nicely for readability
4. Suggest organizing tasks by priority when appropriate
5. Be concise but friendly

## Response Format
- Use bullet points for task lists
- Include task IDs when relevant
- Summarize changes after actions
""".format(user_id=USER_ID))


HELP_AGENT_INSTRUCTIONS = prompt_with_handoff_instructions("""
You provide help about using the todo application.

## Topics You Cover
- How to create tasks with priorities
- How to organize tasks effectively
- Best practices for task management
- Productivity tips

## Guidelines
- Be helpful and encouraging
- Give practical examples
- Keep explanations concise
""")


# ============================================================================
# Agent Setup
# ============================================================================

async def create_agents(mcp_server):
    """Create the agent hierarchy."""

    model = LitellmModel(
        model="gemini/gemini-2.0-flash",
        api_key=GOOGLE_API_KEY,
    )

    # Task management agent (has MCP tools)
    task_agent = Agent(
        name="Task Agent",
        instructions=TASK_AGENT_INSTRUCTIONS,
        model=model,
        mcp_servers=[mcp_server],
    )

    # Help agent (no tools, just answers questions)
    help_agent = Agent(
        name="Help Agent",
        instructions=HELP_AGENT_INSTRUCTIONS,
        model=model,
    )

    # Main triage agent
    main_agent = Agent(
        name="Todo Assistant",
        instructions=prompt_with_handoff_instructions(f"""
You are the main todo application assistant.

## Routing Rules
- **Task Agent**: Any task-related requests
  - Creating, viewing, updating, deleting tasks
  - Marking tasks complete
  - Questions about specific tasks

- **Help Agent**: Questions about how to use the app
  - "How do I..." questions
  - Feature explanations
  - Productivity tips

## For Simple Interactions
- Greetings: Respond directly with a friendly greeting
- Thanks: Respond directly with "You're welcome!"

Current user ID: {USER_ID}
"""),
        model=model,
        handoffs=[task_agent, help_agent],
    )

    return main_agent


# ============================================================================
# Chat Loop
# ============================================================================

async def chat_loop(agent):
    """Interactive chat loop."""
    print("\n" + "=" * 50)
    print("Todo AI Assistant")
    print("=" * 50)
    print("Type 'quit' to exit\n")

    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ["quit", "exit", "q"]:
                print("\nGoodbye!")
                break

            # Run agent
            result = await Runner.run(agent, user_input)

            # Print response
            print(f"\nAssistant ({result.current_agent.name}): {result.final_output}\n")

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}\n")


# ============================================================================
# Main Entry Point
# ============================================================================

async def main():
    """Main entry point."""
    if not GOOGLE_API_KEY:
        print("Error: GOOGLE_API_KEY environment variable not set")
        return

    print(f"Connecting to MCP server at {MCP_SERVER_URL}...")

    try:
        async with MCPServerStreamableHttp(
            name="Todo MCP Server",
            params={
                "url": MCP_SERVER_URL,
                "timeout": 30,
            },
            cache_tools_list=True,
        ) as mcp_server:
            print("Connected to MCP server")

            # List available tools
            tools = await mcp_server.list_tools()
            print(f"Available tools: {[t.name for t in tools]}")

            # Create agents
            agent = await create_agents(mcp_server)

            # Start chat loop
            await chat_loop(agent)

    except ConnectionError:
        print(f"Error: Could not connect to MCP server at {MCP_SERVER_URL}")
        print("Make sure the backend server is running.")


if __name__ == "__main__":
    asyncio.run(main())
```

## Example Conversation

```
Todo AI Assistant
==================================================
Type 'quit' to exit

You: Show me my tasks

Assistant (Task Agent): Here are your current tasks:

**Pending Tasks:**
• [ID: 1] Review quarterly report - Priority: High
• [ID: 3] Buy groceries - Priority: Low

**Completed Tasks:**
• [ID: 2] Send email to team - Priority: Medium

Total: 3 tasks (2 pending, 1 completed)

You: Create a high priority task to prepare for tomorrow's meeting

Assistant (Task Agent): I've created your task:

✅ **Task Created**
- **Title:** Prepare for tomorrow's meeting
- **Priority:** High
- **Status:** Pending
- **ID:** 4

Would you like to add a description or due date?

You: Mark task 1 as complete

Assistant (Task Agent): ✅ Task "Review quarterly report" has been marked as completed!

You now have 2 pending tasks remaining.

You: How do I organize my tasks better?

Assistant (Help Agent): Great question! Here are some tips for organizing your tasks:

**Priority System**
- Use **High** for urgent/important tasks
- Use **Medium** for important but not urgent
- Use **Low** for "nice to have" items

**Best Practices**
- Review tasks daily
- Complete high-priority items first
- Break large tasks into smaller ones
- Set realistic due dates

Would you like me to help reorganize your current tasks?

You: quit

Goodbye!
```

## Running the Agent

1. Start the MCP server (backend):
```bash
cd backend
uvicorn main:app --reload --port 8000
```

2. Run the agent:
```bash
export GOOGLE_API_KEY=your-api-key
python todo_agent.py
```

## Integration with FastAPI Chat Endpoint

See the chatkit-python skill for integrating this agent with a FastAPI `/api/chat` endpoint.
