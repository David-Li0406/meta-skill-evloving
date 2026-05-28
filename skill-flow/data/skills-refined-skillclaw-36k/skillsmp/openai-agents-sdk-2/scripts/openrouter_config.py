#!/usr/bin/env python3
"""
OpenRouter Configuration Template

This script provides a template for configuring agents with OpenRouter models.
It demonstrates various OpenRouter configurations and best practices.

Usage:
    python openrouter_config.py
"""

import asyncio
import os
import sys
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    from agents import Agent, Runner, function_tool
    from agents.extensions.models.litellm_model import LitellmModel
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please install required packages:")
    print("  pip install 'openai-agents[litellm]' python-dotenv")
    sys.exit(1)

# Function tools for demonstration
@function_tool
def get_current_time() -> str:
    """Get the current time."""
    from datetime import datetime
    return f"The current time is {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

@function_tool
def simple_calculator(a: float, b: float, operation: str) -> float:
    """
    Perform simple arithmetic operations.

    Args:
        a: First number
        b: Second number
        operation: Operation to perform (add, subtract, multiply, divide)

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
        raise ValueError(f"Unknown operation: {operation}")

    return operations[operation](a, b)

class OpenRouterConfig:
    """
    Configuration manager for OpenRouter agents.
    Provides pre-configured agents for different OpenRouter models.
    """

    # Model configurations for different use cases
    MODEL_CONFIGS: Dict[str, Dict[str, Any]] = {
        "fast": {
            "model": "openrouter/anthropic/claude-3-haiku",
            "temperature": 0.3,
            "max_tokens": 500,
            "description": "Fast, cost-effective model for simple tasks"
        },
        "balanced": {
            "model": "openrouter/openai/gpt-4-turbo",
            "temperature": 0.7,
            "max_tokens": 1000,
            "description": "Balanced model for general-purpose tasks"
        },
        "creative": {
            "model": "openrouter/google/gemini-2.0-pro-exp",
            "temperature": 0.9,
            "max_tokens": 1500,
            "description": "Creative model for brainstorming and ideation"
        },
        "analytical": {
            "model": "openrouter/anthropic/claude-3-5-sonnet",
            "temperature": 0.5,
            "max_tokens": 2000,
            "description": "Analytical model for complex reasoning"
        }
    }

    @classmethod
    def get_api_key(cls) -> str:
        """
        Get OpenRouter API key from environment.

        Returns:
            API key string

        Raises:
            ValueError: If API key is not set
        """
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENROUTER_API_KEY environment variable not set.\n"
                "Set it with: export OPENROUTER_API_KEY='your-key'\n"
                "Or add it to your .env file"
            )
        return api_key

    @classmethod
    def create_agent(
        cls,
        config_name: str = "balanced",
        tools: Optional[list] = None,
        custom_name: Optional[str] = None,
        custom_instructions: Optional[str] = None
    ) -> Agent:
        """
        Create an agent with OpenRouter configuration.

        Args:
            config_name: Name of configuration preset (fast, balanced, creative, analytical)
            tools: List of function tools for the agent
            custom_name: Custom name for the agent
            custom_instructions: Custom instructions for the agent

        Returns:
            Configured Agent instance
        """
        if config_name not in cls.MODEL_CONFIGS:
            raise ValueError(
                f"Unknown config: {config_name}. "
                f"Available: {list(cls.MODEL_CONFIGS.keys())}"
            )

        config = cls.MODEL_CONFIGS[config_name]
        api_key = cls.get_api_key()

        # Default agent name and instructions
        agent_name = custom_name or f"{config_name.capitalize()} Agent"
        instructions = custom_instructions or f"""
        You are a helpful assistant powered by {config['model']}.
        You have access to tools that can help answer questions.
        Be concise and helpful in your responses.
        """

        return Agent(
            name=agent_name,
            instructions=instructions,
            model=LitellmModel(
                model=config["model"],
                api_key=api_key,
                temperature=config["temperature"],
                max_tokens=config["max_tokens"],
                base_url="https://openrouter.ai/api/v1"
            ),
            tools=tools or [],
            max_steps=15,
            allow_delegation=False
        )

    @classmethod
    def list_available_models(cls):
        """List all available OpenRouter model configurations."""
        print("📋 Available OpenRouter Model Configurations:")
        print("=" * 60)
        for name, config in cls.MODEL_CONFIGS.items():
            print(f"\n{name.upper()}:")
            print(f"  Model: {config['model']}")
            print(f"  Temperature: {config['temperature']}")
            print(f"  Max Tokens: {config['max_tokens']}")
            print(f"  Description: {config['description']}")
        print("\n" + "=" * 60)

async def test_openrouter_configuration():
    """
    Test OpenRouter configuration with different model presets.
    """
    print("🧪 Testing OpenRouter Configuration")
    print("=" * 50)

    try:
        # Test each configuration
        for config_name in ["fast", "balanced", "creative", "analytical"]:
            print(f"\n🔧 Testing {config_name} configuration...")

            agent = OpenRouterConfig.create_agent(
                config_name=config_name,
                tools=[get_current_time, simple_calculator],
                custom_name=f"Test {config_name.capitalize()} Agent"
            )

            # Test a simple query
            test_query = "What's 15 multiplied by 7? Use the calculator tool."
            print(f"   Query: {test_query}")

            try:
                result = await Runner.run(agent, test_query)
                print(f"   ✅ Response: {result.final_output[:100]}...")
            except Exception as e:
                print(f"   ❌ Error: {e}")

        print("\n✅ All configurations tested successfully!")

    except ValueError as e:
        print(f"\n❌ Configuration error: {e}")
        print("\n💡 Solution: Set your OpenRouter API key:")
        print("   export OPENROUTER_API_KEY='your-api-key'")
        print("   Or create a .env file with OPENROUTER_API_KEY=your-key")
        return False

    return True

async def create_custom_agent():
    """
    Create a custom agent with specific configuration.
    """
    print("\n🎛️  Creating Custom OpenRouter Agent")
    print("=" * 50)

    # Show available configurations
    OpenRouterConfig.list_available_models()

    try:
        # Create agent with specific configuration
        agent = OpenRouterConfig.create_agent(
            config_name="balanced",
            tools=[get_current_time, simple_calculator],
            custom_name="Math Time Assistant",
            custom_instructions="""
            You are a specialized assistant that helps with mathematical calculations
            and time-related queries. You have access to:
            1. A calculator tool for arithmetic operations
            2. A time tool to get current time

            Always use the appropriate tool for the task.
            If asked for calculations, use the calculator tool.
            If asked for time, use the time tool.
            """
        )

        print(f"\n🤖 Agent created: {agent.name}")
        print(f"   Model: {agent.model.model}")
        print(f"   Tools: {[tool.__name__ for tool in agent.tools]}")

        # Test the agent
        test_queries = [
            "What's 42 divided by 6?",
            "What time is it now?",
            "Calculate 123 + 456 and tell me the current time"
        ]

        for query in test_queries:
            print(f"\n📝 Query: {query}")
            result = await Runner.run(agent, query)
            print(f"   🤖 Response: {result.final_output}")

    except Exception as e:
        print(f"\n❌ Error creating agent: {e}")
        return False

    return True

def setup_environment():
    """
    Set up environment variables for OpenRouter.
    """
    print("🔧 Environment Setup Guide")
    print("=" * 50)

    # Check if .env file exists
    env_file = ".env"
    if os.path.exists(env_file):
        print(f"✅ Found .env file at: {os.path.abspath(env_file)}")
    else:
        print("❌ No .env file found.")

    # Check for API key
    api_key = os.getenv("OPENROUTER_API_KEY")
    if api_key:
        print(f"✅ OPENROUTER_API_KEY is set (first 10 chars: {api_key[:10]}...)")
    else:
        print("❌ OPENROUTER_API_KEY is not set")
        print("\n💡 To set it up:")
        print("   1. Get your API key from https://openrouter.ai")
        print("   2. Create a .env file with:")
        print('      OPENROUTER_API_KEY="your-api-key-here"')
        print("   3. Or set it as an environment variable:")
        print('      export OPENROUTER_API_KEY="your-api-key-here"')

    print("\n📦 Required packages:")
    print("   pip install 'openai-agents[litellm]' python-dotenv")

def main():
    """
    Main entry point for the OpenRouter configuration script.
    """
    import argparse

    parser = argparse.ArgumentParser(description="OpenRouter Configuration Manager")
    parser.add_argument(
        "--setup",
        action="store_true",
        help="Show environment setup instructions"
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Test OpenRouter configurations"
    )
    parser.add_argument(
        "--custom",
        action="store_true",
        help="Create and test a custom agent"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run all tests and setup"
    )

    args = parser.parse_args()

    # If no arguments, show help
    if not any(vars(args).values()):
        parser.print_help()
        return

    try:
        if args.setup or args.all:
            setup_environment()

        if args.test or args.all:
            success = asyncio.run(test_openrouter_configuration())
            if not success:
                return

        if args.custom or args.all:
            success = asyncio.run(create_custom_agent())
            if not success:
                return

        if args.all:
            print("\n" + "=" * 50)
            print("✅ All operations completed successfully!")
            print("\n📚 Next steps:")
            print("   1. Review the scripts/ directory for more examples")
            print("   2. Check references/openrouter-integration.md for detailed guide")
            print("   3. Modify basic_agent.py for your specific use case")

    except KeyboardInterrupt:
        print("\n\n👋 Operation cancelled by user.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()