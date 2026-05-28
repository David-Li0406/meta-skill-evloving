---
title: Handle High-Level Run Item Events
impact: LOW-MEDIUM
impactDescription: Meaningful progress updates without token-level detail
tags: streaming, events, run-item, progress
---

## Handle High-Level Run Item Events

**Impact: LOW-MEDIUM (meaningful progress updates without token-level detail)**

Use `run_item_stream_event` for high-level progress updates like "tool called", "message generated", instead of raw tokens.

**Raw events vs item events:**

```python
from agents import Agent, Runner, ItemHelpers

agent = Agent(name="Agent", tools=[some_tool])
result = Runner.run_streamed(agent, "Do something")

async for event in result.stream_events():
    # Skip raw token events
    if event.type == "raw_response_event":
        continue
        
    # Handle high-level events
    if event.type == "agent_updated_stream_event":
        print(f"Now talking to: {event.new_agent.name}")
        
    elif event.type == "run_item_stream_event":
        item = event.item
        
        if item.type == "tool_call_item":
            print(f"Calling tool: {item.raw_item.name}")
            
        elif item.type == "tool_call_output_item":
            print(f"Tool result: {item.output[:100]}...")
            
        elif item.type == "message_output_item":
            text = ItemHelpers.text_message_output(item)
            print(f"Response: {text}")
            
        elif item.type == "handoff_call_item":
            print(f"Handing off to another agent...")
            
        elif item.type == "handoff_output_item":
            print(f"Handoff complete")
```

**Build a progress indicator:**

```python
from agents import Agent, Runner

async def run_with_progress(agent: Agent, input: str):
    result = Runner.run_streamed(agent, input)
    
    steps = []
    async for event in result.stream_events():
        if event.type == "run_item_stream_event":
            item = event.item
            
            if item.type == "tool_call_item":
                steps.append(f"🔧 Calling {item.raw_item.name}")
            elif item.type == "tool_call_output_item":
                steps.append(f"✅ Got result from tool")
            elif item.type == "message_output_item":
                steps.append(f"💬 Generated response")
                
        elif event.type == "agent_updated_stream_event":
            steps.append(f"🔄 Switched to {event.new_agent.name}")
    
    print("Steps taken:")
    for step in steps:
        print(f"  {step}")
    
    return result.final_output
```

**Item types:**

| Item type | Meaning |
|-----------|---------|
| `tool_call_item` | LLM decided to call a tool |
| `tool_call_output_item` | Tool returned a result |
| `message_output_item` | LLM generated text output |
| `handoff_call_item` | LLM initiated a handoff |
| `handoff_output_item` | Handoff completed |

Reference: [Streaming Documentation](https://openai.github.io/openai-agents-python/streaming/)
