# OpenAI Agents SDK Setup Guide

## Complete Installation and Configuration

### Prerequisites
- Python 3.8+
- Virtual environment (recommended)
- OpenAI Agents SDK Python package
- OpenRouter API key (for OpenRouter models)

### Installation Steps

```bash
# Create and activate virtual environment
python -m venv .venv

# On macOS/Linux:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate

# Install OpenAI Agents SDK with all optional dependencies
pip install "openai-agents[all]"

# Or install specific components
pip install "openai-agents[litellm]"    # For OpenRouter and other model providers
pip install "openai-agents[voice]"      # For voice capabilities
pip install "openai-agents[redis]"      # For session storage
```

### Environment Configuration

```bash
# Set OpenRouter API key
export OPENROUTER_API_KEY="your-api-key-here"

# Or create a .env file
echo "OPENROUTER_API_KEY=your-api-key-here" > .env
```

### Basic Agent Setup

```python
from agents import Agent, Runner, function_tool
import asyncio

@function_tool
def get_weather(city: str) -> str:
    """Get weather information for a city."""
    return f"The weather in {city} is sunny."

# Create agent
agent = Agent(
    name="Weather Assistant",
    instructions="You are a helpful weather assistant.",
    model="gpt-4o",  # Use OpenAI model
    tools=[get_weather],
)

async def main():
    result = await Runner.run(agent, "What's the weather in Tokyo?")
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
```

### Configuration Files

#### requirements.txt
```
openai-agents[litellm]>=0.2.0
python-dotenv>=1.0.0
```

#### .env.example
```env
# OpenRouter Configuration
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1

# OpenAI Configuration (if using OpenAI models)
OPENAI_API_KEY=your_openai_api_key_here

# Other environment variables
LOG_LEVEL=INFO
DEBUG=false
```

### Project Structure

```
your_project/
├── .env                    # Environment variables
├── .env.example           # Example environment variables
├── requirements.txt       # Python dependencies
├── src/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── weather_agent.py
│   │   ├── math_agent.py
│   │   └── research_agent.py
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── weather_tools.py
│   │   ├── calculation_tools.py
│   │   └── web_tools.py
│   └── main.py
└── tests/
    ├── test_agents.py
    └── test_tools.py
```

### Common Issues and Solutions

#### 1. ModuleNotFoundError
```bash
# If you get: ModuleNotFoundError: No module named 'agents'
pip install openai-agents
```

#### 2. LiteLLM Import Error
```bash
# If you get: ImportError: cannot import name 'LitellmModel'
pip install "openai-agents[litellm]"
```

#### 3. API Key Issues
```python
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check if API key is set
api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    raise ValueError("OPENROUTER_API_KEY environment variable not set")
```

#### 4. Async/Await Pattern
```python
# Correct way to run agents
async def run_agent():
    result = await Runner.run(agent, "Your prompt")
    return result.final_output

# Run from main
if __name__ == "__main__":
    import asyncio
    asyncio.run(run_agent())
```

### Testing Your Setup

Create a test script to verify installation:

```python
# test_setup.py
import asyncio
import os
from agents import Agent, Runner, function_tool
from agents.extensions.models.litellm_model import LitellmModel
from dotenv import load_dotenv

load_dotenv()

@function_tool
def test_tool(message: str) -> str:
    """Test tool that echoes back the message."""
    return f"Echo: {message}"

async def test_basic_agent():
    """Test basic agent with OpenAI model."""
    agent = Agent(
        name="Test Agent",
        instructions="You are a test agent.",
        model="gpt-4o",
        tools=[test_tool],
    )

    result = await Runner.run(agent, "Say hello and use the test tool")
    print(f"Basic Agent Test: {result.final_output}")
    return True

async def test_openrouter_agent():
    """Test agent with OpenRouter model."""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("Skipping OpenRouter test - API key not set")
        return False

    agent = Agent(
        name="OpenRouter Test Agent",
        instructions="You are a test agent using OpenRouter.",
        model=LitellmModel(
            model="openrouter/openai/gpt-4-turbo",
            api_key=api_key
        ),
        tools=[test_tool],
    )

    result = await Runner.run(agent, "Say hello from OpenRouter")
    print(f"OpenRouter Agent Test: {result.final_output}")
    return True

async def main():
    print("Testing OpenAI Agents SDK Setup...")

    # Test basic agent
    basic_success = await test_basic_agent()

    # Test OpenRouter agent
    openrouter_success = await test_openrouter_agent()

    if basic_success:
        print("✓ Basic agent test passed")
    else:
        print("✗ Basic agent test failed")

    if openrouter_success:
        print("✓ OpenRouter agent test passed")
    else:
        print("✗ OpenRouter agent test skipped or failed")

    print("\nSetup test completed!")

if __name__ == "__main__":
    asyncio.run(main())
```

### Next Steps

After successful setup:
1. Explore function tools in [tool-definition.md](tool-definition.md)
2. Learn about multi-agent systems in [multi-agent-patterns.md](multi-agent-patterns.md)
3. Configure OpenRouter models in [openrouter-integration.md](openrouter-integration.md)
4. Check the example scripts in the `scripts/` directory