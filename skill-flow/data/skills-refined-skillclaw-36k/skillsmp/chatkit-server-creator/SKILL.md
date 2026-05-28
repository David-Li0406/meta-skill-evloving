---
name: chatkit-server-creator
description: This skill helps create ChatKit server implementations that integrate with databases and openai-agents, following best practices for conversation management and message persistence.
---

# ChatKit Server Creator

This skill helps create ChatKit server implementations that integrate with databases and openai-agents, following best practices for conversation management and message persistence.

## Usage Instructions

When a user needs to create a ChatKit server with database integration and agent processing, use this skill to generate:

1. Custom ChatKit server class extending the base ChatKitServer
2. Proper initialization with agent and store dependencies
3. Message processing flow with database persistence
4. Thread management and conversation history handling
5. Response streaming with proper ID management

## Best Practices to Follow

- Extend the base `ChatKitServer` class to create custom implementations
- Pass the stores implementation to the parent constructor: `super().__init__(store=stores)`
- Include an agent instance for message processing
- Use `ThreadItemConverter` to convert between ChatKit items and agent input
- Implement async methods for proper database operations
- Handle ID mapping to prevent collisions from external services (LiteLLM/Gemini)
- Create proper logging for debugging and monitoring
- Use type hints for all method parameters and return values
- Implement proper error handling for database and agent operations

## Template Structure

### Basic ChatKit Server:
```python
from collections.abc import AsyncIterator
from chatkit.server import ChatKitServer
from agents import Agent, Runner
from .stores import YourStores  # Import your stores implementation
import logging
from pydantic import BaseModel
from typing import Optional
from chatkit.types import AssistantMessageItem, ThreadMetadata, UserMessageItem
from chatkit.agents import AgentContext, stream_agent_response, ThreadItemConverter

# Set up logging
logger = logging.getLogger(__name__)

class CustomChatKitServer(ChatKitServer):
    """
    Custom ChatKit server implementation extending the base ChatKitServer class.
    """

    def __init__(self, agent: Agent, stores: YourStores):
        """
        Initialize the custom ChatKit server with the provided agent and stores.

        Args:
            agent: The OpenAI Agent to use for processing messages
            stores: The stores implementation for message persistence
        """
        super().__init__(store=stores)
        self.agent = agent
        self.converter = ThreadItemConverter()
        logger.info("CustomChatKitServer initialized")

    async def respond(self, thread: ThreadMetadata, input_user_message: UserMessageItem | None, context: dict) -> AsyncIterator:
        """
        Process a user message and generate an agent response with database persistence.
        """
        agent_context = AgentContext(
            thread=thread,
            store=self.store,
            request_context=context,
        )

        # Load all thread items from the database
        page = await self.store.load_thread_items(thread.id, None, 100, "asc", context)
        all_items = list(page.data)

        # Add current input to the list if provided
        if input_user_message:
            all_items.append(input_user_message)

        # Convert thread items to agent input format
        agent_input = await self.converter.to_agent_input(all_items) if all_items else []

        # Run the agent with streaming
        result = Runner.run_streamed(
            self.agent,
            agent_input,
            context=agent_context,
        )

        # Track ID mappings to ensure unique IDs (LiteLLM/Gemini may reuse IDs)
        id_mapping: dict[str, str] = {}

        async for event in stream_agent_response(agent_context, result):
            # Handle ID mapping for uniqueness
            if event.type == "thread.item.added":
                if isinstance(event.item, AssistantMessageItem):
                    old_id = event.item.id
                    # Generate unique ID if we haven't seen this response ID before
                    if old_id not in id_mapping:
                        new_id = self.store.generate_item_id("message", thread, context)
                        id_mapping[old_id] = new_id
                    event.item.id = id_mapping[old_id]
            elif event.type == "thread.item.done":
                if isinstance(event.item, AssistantMessageItem):
                    old_id = event.item.id
                    if old_id in id_mapping:
                        event.item.id = id_mapping[old_id]
            elif event.type == "thread.item.updated":
                if event.item_id in id_mapping:
                    event.item_id = id_mapping[event.item_id]

            yield event
```

## Key Integration Points

- **Database Integration**: Uses the store parameter for loading/saving conversation history
- **Agent Integration**: Uses the openai-agents Runner to execute agents with streaming
- **Thread Management**: Maintains conversation history by loading all items before agent processing
- **Response Streaming**: Streams agent responses back to clients with proper event handling
- **ID Management**: Handles potential ID collisions from external AI services

## Common Server Customizations

- Adding authentication and authorization checks
- Implementing rate limiting
- Adding custom logging and analytics
- Extending with additional business logic
- Adding custom error handling and recovery

## Output Requirements

1. Generate complete, working ChatKit server implementations
2. Include proper database integration with the stores interface
3. Add agent processing with streaming responses
4. Include proper ID management to prevent collisions
5. Follow the exact patterns shown in the template
