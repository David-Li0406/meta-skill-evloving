#!/usr/bin/env python3
"""
Basic Agent Template for OpenAI Agents SDK

This script provides a template for creating basic agents with function tools.
Use this as a starting point for building your own agents.

Usage:
    python basic_agent.py
"""

import asyncio
import os
from typing import Annotated
from dotenv import load_dotenv
from agents import Agent, Runner, function_tool

# Load environment variables
load_dotenv()

# Basic function tool example
@function_tool
def get_weather(city: str) -> str:
    """
    Get weather information for a city.

    Args:
        city: Name of the city to get weather for

    Returns:
        Weather information string
    """
    return f"The weather in {city} is sunny with a temperature of 22°C."

@function_tool
def calculator(
    a: Annotated[float, "First number"],
    b: Annotated[float, "Second number"],
    operation: Annotated[str, "Operation: add, subtract, multiply, or divide"]
) -> float:
    """
    Perform basic arithmetic operations.

    Args:
        a: First number
        b: Second number
        operation: Mathematical operation to perform

    Returns:
        Result of the calculation
    """
    operations = {
        "add": lambda x, y: x + y,
        "subtract": lambda x, y: x - y,
        "multiply": lambda x, y: x * y,
        "divide": lambda x, y: x / y if y != 0 else float('inf')
    }

    if operation not in operations:
        raise ValueError(f"Unknown operation: {operation}. Use add, subtract, multiply, or divide.")

    return operations[operation](a, b)

async def create_basic_agent(model: str = "gpt-4o") -> Agent:
    """
    Create a basic agent with weather and calculator tools.

    Args:
        model: Model to use for the agent

    Returns:
        Configured Agent instance
    """
    agent = Agent(
        name="Basic Assistant",
        instructions="""
        You are a helpful assistant that can:
        1. Provide weather information using the get_weather tool
        2. Perform calculations using the calculator tool
        3. Answer general questions

        Always be polite and helpful. If you're asked to perform a calculation,
        use the calculator tool. If asked about weather, use the get_weather tool.
        """,
        model=model,
        tools=[get_weather, calculator],
        max_steps=10,  # Limit to prevent infinite loops
        allow_delegation=False,  # This is a basic agent, no delegation
    )

    return agent

async def run_demo():
    """
    Run a demonstration of the basic agent.
    """
    print("🤖 Creating basic agent...")
    agent = await create_basic_agent()

    # Test questions
    test_queries = [
        "What's the weather in Tokyo?",
        "Calculate 15 multiplied by 23",
        "Tell me about artificial intelligence",
    ]

    for query in test_queries:
        print(f"\n📝 Query: {query}")
        print("⏳ Processing...")

        try:
            result = await Runner.run(agent, query)
            print(f"✅ Response: {result.final_output}")
        except Exception as e:
            print(f"❌ Error: {e}")

async def interactive_mode():
    """
    Run the agent in interactive mode.
    """
    print("🤖 Interactive Basic Agent")
    print("=" * 50)
    print("Type 'quit' or 'exit' to end the session")
    print("=" * 50)

    agent = await create_basic_agent()

    while True:
        try:
            query = input("\n💭 Your question: ").strip()

            if query.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break

            if not query:
                continue

            print("⏳ Processing...")
            result = await Runner.run(agent, query)
            print(f"🤖 Response: {result.final_output}")

        except KeyboardInterrupt:
            print("\n\n👋 Session interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def main():
    """
    Main entry point for the script.
    """
    import argparse

    parser = argparse.ArgumentParser(description="Basic Agent Template")
    parser.add_argument(
        "--mode",
        choices=["demo", "interactive"],
        default="demo",
        help="Run mode: demo (default) or interactive"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="gpt-4o",
        help="Model to use for the agent (default: gpt-4o)"
    )

    args = parser.parse_args()

    # Check for API key if using OpenAI models
    if not os.getenv("OPENAI_API_KEY") and args.model.startswith("gpt-"):
        print("⚠️  Warning: OPENAI_API_KEY environment variable not set")
        print("   Set it with: export OPENAI_API_KEY='your-key'")
        print("   Or add it to your .env file")
        print()

    if args.mode == "demo":
        asyncio.run(run_demo())
    else:
        asyncio.run(interactive_mode())

if __name__ == "__main__":
    main()