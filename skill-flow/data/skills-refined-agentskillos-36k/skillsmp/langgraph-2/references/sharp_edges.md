# Langgraph - Sharp Edges

## Reducer Overwrites State

### **Id**
reducer-overwrites-state
### **Summary**
State updates overwrite instead of merge
### **Severity**
high
### **Situation**
Data disappears after node execution
### **Why**
  Without reducers, updates replace entire field.
  Messages get overwritten instead of appended.
  Previous state lost silently.
  
### **Solution**
  from typing import Annotated
  from operator import add
  from langgraph.graph.message import add_messages
  
  # WRONG - no reducer, overwrites
  class BadState(TypedDict):
      messages: list  # Each update replaces list!
  
  # First node returns: {"messages": ["msg1"]}
  # Second node returns: {"messages": ["msg2"]}
  # Result: {"messages": ["msg2"]}  # msg1 is gone!
  
  # CORRECT - with reducer
  class GoodState(TypedDict):
      messages: Annotated[list, add_messages]  # Appends
  
  # Result: {"messages": ["msg1", "msg2"]}
  
  # Common reducers:
  from operator import add
  
  class State(TypedDict):
      # Messages: use add_messages (handles AIMessage, etc.)
      messages: Annotated[list, add_messages]
  
      # Lists: use operator.add
      items: Annotated[list[str], add]
  
      # Numbers: custom reducer
      count: Annotated[int, lambda a, b: a + b]
  
      # Dicts: merge reducer
      data: Annotated[dict, lambda a, b: {**a, **b}]
  
      # Overwrite (no reducer) - for single values
      current_step: str
  
### **Symptoms**
  - Messages disappear
  - Only last value remains
  - State smaller than expected
### **Detection Pattern**
TypedDict.*\n.*messages:\s*list[^\[]

## Conditional Edge Typos

### **Id**
conditional-edge-typos
### **Summary**
Route function returns wrong node name
### **Severity**
high
### **Situation**
Graph throws error or routes incorrectly
### **Why**
  Route function must return exact node names.
  Typos cause KeyError or wrong routing.
  No compile-time validation.
  
### **Solution**
  from langgraph.graph import StateGraph, END
  
  graph = StateGraph(State)
  graph.add_node("agent", agent_node)
  graph.add_node("tools", tool_node)
  
  # WRONG - typo in return value
  def bad_router(state):
      if should_use_tools(state):
          return "tool"  # Wrong! Node is "tools"
      return "end"  # Wrong! Should be END constant
  
  # CORRECT - exact names
  def good_router(state):
      if should_use_tools(state):
          return "tools"  # Matches add_node name
      return END  # Use constant, not string
  
  # BETTER - use Literal types
  from typing import Literal
  
  def typed_router(state) -> Literal["tools", "agent", "__end__"]:
      if should_use_tools(state):
          return "tools"
      return END
  
  # Add conditional edges with explicit mapping
  graph.add_conditional_edges(
      "agent",
      good_router,
      {
          "tools": "tools",
          END: END
      }
  )
  
  # The mapping validates at compile time
  
### **Symptoms**
  - KeyError on node name
  - Unexpected routing
  - Graph never reaches END
### **Detection Pattern**
return.*"end"|return.*"END"

## Missing Checkpointer Threads

### **Id**
missing-checkpointer-threads
### **Summary**
Thread ID not provided for stateful agents
### **Severity**
high
### **Situation**
Each invocation starts fresh, no memory
### **Why**
  Checkpointer saves state by thread_id.
  Without config, each call is new thread.
  Conversation history not loaded.
  
### **Solution**
  from langgraph.checkpoint.sqlite import SqliteSaver
  
  memory = SqliteSaver.from_conn_string(":memory:")
  app = graph.compile(checkpointer=memory)
  
  # WRONG - no config
  result1 = app.invoke({"messages": [("user", "Hi, I'm Bob")]})
  result2 = app.invoke({"messages": [("user", "What's my name?")]})
  # Agent doesn't know name - new thread each time!
  
  # CORRECT - with thread_id
  config = {"configurable": {"thread_id": "user-bob-session-1"}}
  
  result1 = app.invoke(
      {"messages": [("user", "Hi, I'm Bob")]},
      config=config
  )
  result2 = app.invoke(
      {"messages": [("user", "What's my name?")]},
      config=config
  )
  # Agent remembers: "Your name is Bob"
  
  # For new conversation, new thread_id
  new_config = {"configurable": {"thread_id": "user-bob-session-2"}}
  
  # Thread ID strategies:
  # - Per user: f"user-{user_id}"
  # - Per session: f"user-{user_id}-{session_id}"
  # - Per conversation: f"conv-{uuid4()}"
  
### **Symptoms**
  - Agent forgets previous messages
  - Each call seems independent
  - "I don't have context" responses
### **Detection Pattern**
app\.invoke\([^,]+\)[^,]*$|invoke.*\{[^}]*\}[^,]*\)

## Tool Node Error Handling

### **Id**
tool-node-error-handling
### **Summary**
Tool errors crash the agent
### **Severity**
medium
### **Situation**
One tool failure stops entire agent
### **Why**
  Default ToolNode doesn't catch exceptions.
  Tool error propagates up.
  Agent can't recover.
  
### **Solution**
  from langgraph.prebuilt import ToolNode
  from langchain_core.tools import ToolException
  
  # Option 1: Use handle_tool_errors
  tool_node = ToolNode(
      tools,
      handle_tool_errors=True  # Converts errors to messages
  )
  
  # Option 2: Custom error handling in tools
  @tool
  def risky_search(query: str) -> str:
      """Search with error handling."""
      try:
          result = external_api.search(query)
          return result
      except Exception as e:
          # Return error message, don't raise
          return f"Search failed: {str(e)}. Please try a different query."
  
  # Option 3: Wrap ToolNode
  def safe_tool_node(state):
      try:
          return tool_node.invoke(state)
      except Exception as e:
          # Return error as message
          return {
              "messages": [
                  AIMessage(content=f"Tool error: {e}. Trying alternative...")
              ]
          }
  
  # Option 4: Use ToolException for handled errors
  @tool
  def validated_tool(input: str) -> str:
      """Tool with validation."""
      if not input:
          raise ToolException("Input required")  # Handled gracefully
      return process(input)
  
### **Symptoms**
  - Agent crashes on tool failure
  - Unhandled exception errors
  - Partial execution
### **Detection Pattern**
ToolNode\([^)]*\)(?!.*handle_tool_errors)

## Async Sync Mismatch

### **Id**
async-sync-mismatch
### **Summary**
Mixing async and sync incorrectly
### **Severity**
medium
### **Situation**
"Event loop" errors or blocking
### **Why**
  LangGraph supports both sync and async.
  Mixing them causes problems.
  Can't await in sync context.
  
### **Solution**
  # SYNC version - all sync
  def sync_agent(state):
      response = llm.invoke(state["messages"])  # sync
      return {"messages": [response]}
  
  result = app.invoke(input)  # sync invoke
  
  # ASYNC version - all async
  async def async_agent(state):
      response = await llm.ainvoke(state["messages"])  # async
      return {"messages": [response]}
  
  result = await app.ainvoke(input)  # async invoke
  
  # WRONG - async in sync context
  def broken_agent(state):
      response = await llm.ainvoke(...)  # Can't await here!
  
  # WRONG - sync in async causing blocking
  async def slow_agent(state):
      response = llm.invoke(...)  # Blocks event loop!
  
  # If you need sync in async, use run_in_executor
  import asyncio
  
  async def mixed_agent(state):
      loop = asyncio.get_event_loop()
      response = await loop.run_in_executor(
          None,
          lambda: sync_llm.invoke(state["messages"])
      )
      return {"messages": [response]}
  
  # Streaming also has sync/async versions
  for chunk in app.stream(input):  # sync
      print(chunk)
  
  async for chunk in app.astream(input):  # async
      print(chunk)
  
### **Symptoms**
  - cannot be used in 'await' expression
  - Event loop blocked
  - Slow performance
### **Detection Pattern**
async def.*\n.*[^a]invoke\(|def [^a].*\n.*await

## Graph Not Compiled

### **Id**
graph-not-compiled
### **Summary**
Using graph without compile()
### **Severity**
high
### **Situation**
AttributeError when invoking
### **Why**
  StateGraph is builder, not executor.
  Must call compile() to get runnable.
  Common when refactoring.
  
### **Solution**
  from langgraph.graph import StateGraph
  
  graph = StateGraph(State)
  graph.add_node("agent", agent)
  # ... add edges
  
  # WRONG - using graph directly
  result = graph.invoke(input)  # AttributeError!
  
  # CORRECT - compile first
  app = graph.compile()
  result = app.invoke(input)
  
  # With checkpointer
  app = graph.compile(checkpointer=memory)
  
  # With interrupt points
  app = graph.compile(
      checkpointer=memory,
      interrupt_before=["dangerous_action"]
  )
  
  # Common pattern - module level
  # graph.py
  graph = StateGraph(State)
  # ... build graph
  app = graph.compile()  # Export the compiled version
  
  # main.py
  from graph import app
  result = app.invoke(input)
  
### **Symptoms**
  - AttributeError: 'StateGraph' has no attribute 'invoke'
  - Missing methods on graph object
### **Detection Pattern**
StateGraph\([^)]*\)\.invoke|graph\.invoke