"""
Basic Gemini Agent Template

A simple agent using Gemini via direct AsyncOpenAI integration with function tools.

Requirements:
    pip install openai-agents python-dotenv

Environment:
    GOOGLE_API_KEY=your-gemini-api-key

Usage:
    python agent_gemini.py
"""

import asyncio
import os
from agents import AsyncOpenAI, OpenAIChatCompletionsModel, Agent, Runner, function_tool
from agents.run import RunConfig
from dotenv import load_dotenv

load_dotenv()


# ============================================================================
# Configuration
# ============================================================================

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

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
# Function Tools
# ============================================================================

@function_tool
def greet(name: str) -> str:
    """Greet someone by name.

    Args:
        name: The name of the person to greet
    """
    return f"Hello, {name}! Nice to meet you."


@function_tool
def calculate(operation: str, a: float, b: float) -> dict:
    """Perform a calculation.

    Args:
        operation: The operation (add, subtract, multiply, divide)
        a: First number
        b: Second number
    """
    operations = {
        "add": lambda x, y: x + y,
        "subtract": lambda x, y: x - y,
        "multiply": lambda x, y: x * y,
        "divide": lambda x, y: x / y if y != 0 else "Cannot divide by zero",
    }

    if operation not in operations:
        return {"error": f"Unknown operation: {operation}"}

    result = operations[operation](a, b)
    return {
        "operation": operation,
        "a": a,
        "b": b,
        "result": result,
    }


@function_tool
def get_current_time() -> str:
    """Get the current date and time."""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ============================================================================
# Agent Setup
# ============================================================================

def create_agent() -> Agent:
    """Create the Gemini agent."""
    return Agent(
        name="Gemini Assistant",
        instructions="""You are a helpful assistant powered by Gemini.

Available tools:
- greet: Say hello to someone
- calculate: Do math (add, subtract, multiply, divide)
- get_current_time: Get the current time

Be helpful, friendly, and concise in your responses.""",
        tools=[greet, calculate, get_current_time],
    )


# ============================================================================
# Main Entry Point
# ============================================================================

async def main():
    """Run the agent with sample queries."""
    agent = create_agent()

    # Test queries
    queries = [
        "Hello! My name is Alice.",
        "What's 25 multiplied by 4?",
        "What time is it?",
        "Can you add 100 and 250, then tell me the result?",
    ]

    print("Gemini Agent Demo")
    print("=" * 50)

    for query in queries:
        print(f"\nUser: {query}")
        result = await Runner.run(agent, query, config=run_config)
        print(f"Assistant: {result.final_output}")

    print("\n" + "=" * 50)
    print("Demo complete!")


async def interactive():
    """Run interactive chat loop."""
    agent = create_agent()

    print("\nGemini Agent - Interactive Mode")
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

    print("Goodbye!")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        asyncio.run(interactive())
    else:
        asyncio.run(main())
