# Function tools reference

Function tools let your agent call external functions during conversations.

## Basic function tool

```python
from livekit.agents import Agent, function_tool, RunContext

class MyAgent(Agent):
    def __init__(self) -> None:
        super().__init__(instructions="You are a helpful assistant.")

    @function_tool()
    async def get_weather(self, context: RunContext, location: str) -> str:
        """Get the current weather for a location.
        
        Args:
            location: The city name to get weather for
        """
        # Your implementation here
        return f"The weather in {location} is sunny and 72°F"
```

## RunContext

Access session data and perform actions within tools:

```python
from livekit.agents import function_tool, RunContext

@function_tool()
async def save_note(self, context: RunContext, note: str) -> str:
    """Save a note for the user."""
    # Access user data
    context.userdata["notes"] = context.userdata.get("notes", [])
    context.userdata["notes"].append(note)
    
    # Access the session
    session = context.session
    
    # Access the room
    room = context.session.room
    
    return "Note saved!"
```

## Tool with complex parameters

```python
from typing import Literal
from livekit.agents import function_tool, RunContext

@function_tool()
async def book_appointment(
    self,
    context: RunContext,
    date: str,
    time: str,
    service: Literal["haircut", "coloring", "styling"],
    notes: str = "",
) -> str:
    """Book an appointment.
    
    Args:
        date: The date in YYYY-MM-DD format
        time: The time in HH:MM format
        service: Type of service requested
        notes: Optional additional notes
    """
    return f"Booked {service} for {date} at {time}"
```

## Tool returning an Agent (handoff)

Return an Agent instance to hand off control. You can also return a tuple with the agent and a message for the LLM:

```python
from livekit.agents import function_tool, RunContext, Agent

@function_tool()
async def transfer_to_billing(self, context: RunContext) -> Agent:
    """Transfer the call to the billing department."""
    await self.session.say("I'll transfer you to our billing team.")
    return BillingAgent()

# Or return with a message for the LLM
@function_tool()
async def transfer_to_sales(self, context: RunContext) -> tuple[Agent, str]:
    """Transfer the call to the sales department."""
    return SalesAgent(), "Transferring the user to SalesAgent"
```

## Tool with speech during execution

```python
from livekit.agents import function_tool, RunContext

@function_tool()
async def long_running_task(self, context: RunContext, query: str) -> str:
    """Perform a long-running search."""
    # Speak while processing
    await self.session.say("Let me look that up for you...")
    
    # Do the work
    result = await search_database(query)
    
    return result
```

## Provider tools

Use tools specific to model providers:

```python
from livekit.plugins.google import GeminiFileSearch

class MyAgent(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="You are a helpful assistant.",
            tools=[
                GeminiFileSearch(corpus_name="my-corpus"),
            ],
        )
```

## Standalone tool definitions

Define tools outside of an agent class:

```python
from livekit.agents import Agent, function_tool, RunContext

@function_tool()
async def calculate_tip(context: RunContext, amount: float, percentage: float = 18.0) -> str:
    """Calculate the tip for a bill.
    
    Args:
        amount: The bill amount
        percentage: Tip percentage (default 18%)
    """
    tip = amount * (percentage / 100)
    return f"Tip: ${tip:.2f}, Total: ${amount + tip:.2f}"

class MyAgent(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="You are a helpful assistant.",
            tools=[calculate_tip],
        )
```

## Tool interruptions

Handle interruptions during long-running tools:

```python
import asyncio
from livekit.agents import function_tool, RunContext

@function_tool()
async def search_database(self, context: RunContext, query: str) -> str:
    """Search the database."""
    # For non-interruptible tools, call this at the start:
    # context.disallow_interruptions()
    
    wait_for_result = asyncio.ensure_future(perform_search(query))
    await context.speech_handle.wait_if_not_interrupted([wait_for_result])
    
    if context.speech_handle.interrupted:
        # Tool was interrupted, clean up
        wait_for_result.cancel()
        return None  # Return value is ignored when interrupted
    
    return wait_for_result.result()
```

## Error handling

Use `ToolError` to return errors to the LLM:

```python
from livekit.agents import function_tool, RunContext, ToolError

@function_tool()
async def lookup_weather(self, context: RunContext, location: str) -> str:
    """Look up weather for a location."""
    if location == "mars":
        raise ToolError("This location is not supported yet.")
    return f"Weather in {location}: Sunny, 72°F"
```

## Best practices

1. **Write clear docstrings** - The LLM uses them to understand when to call the tool
2. **Use type hints** - They define the parameter schema for the LLM
3. **Return strings** - Results are added to the conversation context
4. **Handle errors gracefully** - Return error messages the LLM can understand
5. **Keep tools focused** - One tool should do one thing well
