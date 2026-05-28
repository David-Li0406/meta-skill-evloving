"""
Agent with MCP Server Integration Template

An agent that connects to an MCP server to access tools.
Uses Gemini via direct AsyncOpenAI integration.

Requirements:
    pip install openai-agents python-dotenv

Environment:
    GOOGLE_API_KEY=your-gemini-api-key
    MCP_SERVER_URL=http://localhost:8000/api/mcp (optional)

Usage:
    # Start MCP server first, then:
    python agent_mcp.py
"""

import asyncio
import os
from agents import AsyncOpenAI, OpenAIChatCompletionsModel, Agent, Runner
from agents.mcp import MCPServerStreamableHttp
from agents.run import RunConfig
from agents.extensions.handoff_prompt import prompt_with_handoff_instructions
from dotenv import load_dotenv

load_dotenv()


# ============================================================================
# Configuration
# ============================================================================

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:8000/api/mcp")

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable not set")

# Setup Gemini client and model
external_provider = AsyncOpenAI(
    api_key=GOOGLE_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai",
)

model = OpenAIChatCompletionsModel(
    openai_client=external_provider,
    model="gemini-2.0-flash-exp",
)

# Create run configuration
run_config = RunConfig(
    model=model,
    model_provider=external_provider,
    tracing_disabled=True
)


# ============================================================================
# Agent Instructions
# ============================================================================

AGENT_INSTRUCTIONS = prompt_with_handoff_instructions("""
You are a helpful assistant with access to MCP tools.

## Guidelines
1. Use the available MCP tools to help users
2. Always confirm actions after performing them
3. Be concise but friendly
4. Ask for clarification if needed

## Available Tools
The MCP server provides tools for your use. Check what's available
and use them appropriately based on user requests.
""")


# ============================================================================
# Agent Factory
# ============================================================================

def create_agent(mcp_server) -> Agent:
    """Create an agent with MCP server access."""
    return Agent(
        name="MCP Assistant",
        instructions=AGENT_INSTRUCTIONS,
        mcp_servers=[mcp_server],
    )


# ============================================================================
# Chat Functions
# ============================================================================

async def single_query(agent: Agent, query: str) -> str:
    """Run a single query and return the response."""
    result = await Runner.run(agent, query, config=run_config)
    return result.final_output


async def chat_loop(agent: Agent):
    """Interactive chat loop."""
    print("\nMCP Agent - Interactive Mode")
    print("Type 'quit' to exit\n")

    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["quit", "exit", "q"]:
                break

            result = await Runner.run(agent, user_input, config=run_config)
            print(f"Assistant: {result.final_output}\n")

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}\n")

    print("Goodbye!")


# ============================================================================
# Main Entry Point
# ============================================================================

async def main():
    """Main entry point with MCP connection."""
    print(f"Connecting to MCP server at {MCP_SERVER_URL}...")

    try:
        async with MCPServerStreamableHttp(
            name="MCP Server",
            params={
                "url": MCP_SERVER_URL,
                "timeout": 30,
            },
            cache_tools_list=True,
            max_retry_attempts=3,
        ) as mcp_server:
            # List available tools
            tools = await mcp_server.list_tools()
            print(f"Connected! Available tools: {[t.name for t in tools]}\n")

            # Create agent
            agent = create_agent(mcp_server)

            # Run interactive loop
            await chat_loop(agent)

    except ConnectionError as e:
        print(f"Connection error: {e}")
        print(f"Make sure the MCP server is running at {MCP_SERVER_URL}")
    except Exception as e:
        print(f"Error: {e}")


async def demo():
    """Run demo queries."""
    print(f"Connecting to MCP server at {MCP_SERVER_URL}...")

    async with MCPServerStreamableHttp(
        name="MCP Server",
        params={"url": MCP_SERVER_URL, "timeout": 30},
        cache_tools_list=True,
    ) as mcp_server:
        tools = await mcp_server.list_tools()
        print(f"Available tools: {[t.name for t in tools]}")

        agent = create_agent(mcp_server)

        # Demo queries - customize based on your MCP tools
        queries = [
            "What tools do you have available?",
            "Help me with a task",
        ]

        print("\nMCP Agent Demo")
        print("=" * 50)

        for query in queries:
            print(f"\nUser: {query}")
            result = await Runner.run(agent, query, config=run_config)
            print(f"Assistant: {result.final_output}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        asyncio.run(demo())
    else:
        asyncio.run(main())
