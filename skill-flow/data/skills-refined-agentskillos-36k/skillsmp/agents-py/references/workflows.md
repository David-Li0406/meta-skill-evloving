# Workflows reference

Build complex voice AI applications with multi-agent handoffs, tasks, and pipeline customization.

## Multi-agent handoffs

Switch between agents during a conversation:

```python
from livekit.agents import Agent, function_tool

class TriageAgent(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="You are a triage agent. Route users to the right department."
        )

    @function_tool()
    async def transfer_to_sales(self) -> Agent:
        """Transfer to the sales department."""
        await self.session.say("I'll connect you with our sales team.")
        return SalesAgent()

    @function_tool()
    async def transfer_to_support(self) -> Agent:
        """Transfer to technical support."""
        await self.session.say("Let me connect you with support.")
        return SupportAgent()

class SalesAgent(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="You are a sales representative."
        )

class SupportAgent(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="You are a technical support specialist."
        )
```

### Manual agent switching

```python
# Switch agent programmatically
session.update_agent(new_agent)
```

### Preserving context during handoffs

```python
class BaseAgent(Agent):
    async def on_enter(self) -> None:
        # Access previous chat context
        chat_ctx = self.chat_ctx.copy()
        
        # Add context from previous agent
        if self.session.userdata.get("prev_agent"):
            prev_items = self.session.userdata["prev_agent"].chat_ctx.items
            chat_ctx.items.extend(prev_items[-6:])  # Keep last 6 messages
        
        await self.update_chat_ctx(chat_ctx)
```

## Tasks

Tasks are focused units that perform a specific objective and return a typed result.

### Defining a task

```python
from livekit.agents import AgentTask, function_tool

class CollectEmailTask(AgentTask[str]):
    def __init__(self, chat_ctx=None):
        super().__init__(
            instructions="Collect and validate the user's email address.",
            chat_ctx=chat_ctx,
        )

    async def on_enter(self) -> None:
        await self.session.generate_reply(
            instructions="Ask the user for their email address."
        )

    @function_tool()
    async def confirm_email(self, email: str) -> None:
        """Confirm the user's email address."""
        self.complete(email)
```

### Running a task

```python
class MyAgent(Agent):
    async def on_enter(self) -> None:
        # Run task and get result
        email = await CollectEmailTask(chat_ctx=self.chat_ctx)
        
        # Use the result
        self.session.userdata["email"] = email
        
        await self.session.generate_reply(
            instructions=f"Thank the user and confirm their email: {email}"
        )
```

### Task with dataclass result

```python
from dataclasses import dataclass

@dataclass
class ContactInfo:
    name: str
    email: str
    phone: str

class CollectContactTask(AgentTask[ContactInfo]):
    def __init__(self):
        super().__init__(
            instructions="Collect the user's contact information."
        )
        self._data = {}

    @function_tool()
    async def record_name(self, name: str) -> None:
        """Record the user's name."""
        self._data["name"] = name
        self._check_complete()

    @function_tool()
    async def record_email(self, email: str) -> None:
        """Record the user's email."""
        self._data["email"] = email
        self._check_complete()

    @function_tool()
    async def record_phone(self, phone: str) -> None:
        """Record the user's phone number."""
        self._data["phone"] = phone
        self._check_complete()

    def _check_complete(self):
        if all(k in self._data for k in ["name", "email", "phone"]):
            self.complete(ContactInfo(**self._data))
```

## TaskGroups

Execute ordered sequences of tasks with regression support.

```python
from livekit.agents.beta.workflows import TaskGroup, GetEmailTask

# Create task group
task_group = TaskGroup()

# Add tasks in order
task_group.add(
    lambda: CollectNameTask(),
    id="collect_name",
    description="Collects the user's name"
)
task_group.add(
    lambda: GetEmailTask(),
    id="collect_email", 
    description="Collects the user's email"
)
task_group.add(
    lambda: ConfirmTask(),
    id="confirm",
    description="Confirms the collected information"
)

# Execute and get results
results = await task_group
print(results.task_results)
# {"collect_name": "John", "collect_email": GetEmailResult(...), ...}
```

## Prebuilt tasks

```python
from livekit.agents.beta.workflows import GetEmailTask, GetAddressTask, GetDtmfTask

# Collect email
email_result = await GetEmailTask(chat_ctx=self.chat_ctx)
print(email_result.email_address)

# Collect address
address_result = await GetAddressTask(chat_ctx=self.chat_ctx)
print(address_result.address)

# Collect DTMF input (for telephony)
dtmf_result = await GetDtmfTask(
    num_digits=10,
    chat_ctx=self.chat_ctx,
    ask_for_confirmation=True,
)
print(dtmf_result.user_input)
```

## Pipeline nodes

Customize the voice pipeline by overriding nodes in your Agent class.

### STT node

```python
class MyAgent(Agent):
    async def stt_node(self, audio, model_settings):
        """Customize speech-to-text processing."""
        # Pre-process audio
        async for event in Agent.default.stt_node(self, audio, model_settings):
            # Post-process transcription
            yield event
```

### LLM node

```python
class MyAgent(Agent):
    async def llm_node(self, chat_ctx, tools, model_settings):
        """Customize LLM inference."""
        # Modify chat context before inference
        async for chunk in Agent.default.llm_node(self, chat_ctx, tools, model_settings):
            # Filter or modify output
            yield chunk
```

### TTS node

```python
class MyAgent(Agent):
    async def tts_node(self, text, model_settings):
        """Customize text-to-speech."""
        # Pre-process text (e.g., pronunciation fixes)
        async def modified_text():
            async for t in text:
                yield t.replace("LiveKit", "Live Kit")
        
        async for frame in Agent.default.tts_node(self, modified_text(), model_settings):
            yield frame
```

### Transcription node

```python
class MyAgent(Agent):
    async def transcription_node(self, text, model_settings):
        """Customize transcription output."""
        async for delta in text:
            # Remove unwanted characters
            yield delta.replace("😘", "")
```

## Lifecycle hooks

```python
class MyAgent(Agent):
    async def on_enter(self) -> None:
        """Called when agent becomes active."""
        await self.session.generate_reply(
            instructions="Greet the user"
        )

    async def on_exit(self) -> None:
        """Called before handoff to another agent."""
        await self.session.say("Transferring you now...")

    async def on_user_turn_completed(self, turn_ctx, new_message) -> None:
        """Called when user finishes speaking, before agent responds."""
        # Inject RAG context
        rag_content = await my_rag_lookup(new_message.text_content())
        turn_ctx.add_message(role="assistant", content=rag_content)
```

## Best practices

1. **Use tasks for structured data collection** - They provide typed results and clear completion criteria
2. **Preserve context during handoffs** - Copy relevant chat history to the new agent
3. **Keep agents focused** - Each agent should have a clear responsibility
4. **Use lifecycle hooks** - `on_enter` and `on_exit` for proper setup and cleanup
5. **Test agent flows** - Use the testing framework to verify handoff behavior
