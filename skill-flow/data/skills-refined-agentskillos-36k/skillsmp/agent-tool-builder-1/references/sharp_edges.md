# Agent Tool Builder - Sharp Edges

## Tool Description Under 3 Sentences

### **Id**
description-too-short
### **Severity**
high
### **Situation**
Defining a new tool with minimal description
### **Symptom**
  LLM picks wrong tool. Parameters are malformed. Agent asks user
  to clarify things the tool already handles. Tool works in tests
  but fails with real user queries.
  
### **Why**
  The LLM never sees your code - only the schema and description.
  Short descriptions leave the LLM guessing. It doesn't know edge
  cases, format expectations, or when NOT to use the tool. Every
  ambiguity becomes a potential failure.
  
### **Solution**
  Write comprehensive descriptions:
  - What the tool does (1-2 sentences)
  - When to use it (1 sentence)
  - When NOT to use it (1 sentence)
  - What it returns (1 sentence)
  - Parameter format examples in descriptions
  
  Minimum 3-4 sentences for simple tools, more for complex ones.
  
### **Detection Pattern**
  - "description":\s*"[^"]{1,50}"
  - description:\s*[^\n]{1,50}$

## Tool Results in Wrong Format for Provider

### **Id**
tool-result-format-mismatch
### **Severity**
critical
### **Situation**
Returning tool results to Claude or OpenAI
### **Symptom**
  400 errors. "tool_use ids were found without tool_result blocks."
  Agent can't parse results. Conversation breaks after tool use.
  
### **Why**
  Each LLM provider has specific format requirements for tool results.
  Anthropic needs tool_result blocks with matching tool_use_id.
  OpenAI needs function results in specific format. Missing is_error
  flags cause retries instead of error handling.
  
### **Solution**
  # Anthropic format:
  {
    "type": "tool_result",
    "tool_use_id": "toolu_01xxx",  # Must match exactly
    "content": "Result string or JSON",
    "is_error": true  # Include for errors
  }
  
  # OpenAI format:
  {
    "role": "tool",
    "tool_call_id": "call_xxx",
    "content": "Result string"
  }
  
  Always match IDs exactly. Always use strings for content.
  
### **Detection Pattern**
  - tool_result
  - tool_call_id

## Parallel Tool Results in Separate Messages

### **Id**
parallel-results-wrong-format
### **Severity**
critical
### **Situation**
Handling multiple tool calls from one response
### **Symptom**
  First tool works. Subsequent tools ignored or error.
  "tool_use ids were found without tool_result blocks immediately after."
  Parallel tool calling stops working.
  
### **Why**
  When Claude makes parallel tool calls, ALL results must be in a
  single user message. Sending separate messages for each result
  breaks the format and "teaches" Claude to avoid parallel calls.
  
### **Solution**
  # WRONG - separate messages:
  messages.append({"role": "user", "content": [result_1]})
  messages.append({"role": "user", "content": [result_2]})
  
  # CORRECT - all results in one message:
  messages.append({
      "role": "user",
      "content": [result_1, result_2, result_3]
  })
  
  # Also WRONG - text before tool results:
  messages.append({
      "role": "user",
      "content": [
          {"type": "text", "text": "Here are results:"},  # NO!
          result_1, result_2
      ]
  })
  
  # Tool results must come FIRST, text AFTER.
  
### **Detection Pattern**
  - tool_result
  - append.*tool

## Missing Strict Mode on Tool Schemas

### **Id**
no-strict-mode
### **Severity**
high
### **Situation**
Using OpenAI function calling
### **Symptom**
  LLM sends unexpected parameters. Type mismatches. Missing required
  fields that should have been enforced. Schema violations that
  cause runtime errors.
  
### **Why**
  Without strict mode, OpenAI models can deviate from the schema.
  They might add extra fields, use wrong types, or omit required
  parameters. The model tries to be helpful but breaks your code.
  
### **Solution**
  # Enable strict mode:
  {
    "name": "get_weather",
    "strict": true,  # Add this
    "parameters": {
      "type": "object",
      "properties": {...},
      "required": ["location"],
      "additionalProperties": false  # Required for strict
    }
  }
  
  # With strict mode:
  # - All parameters validated against schema
  # - Extra properties rejected
  # - Type checking enforced
  # - Required fields guaranteed
  
### **Detection Pattern**
  - "strict":\s*false
  - tools.*function

## Returning Objects Instead of Strings

### **Id**
return-object-not-string
### **Severity**
high
### **Situation**
Implementing tool handler functions
### **Symptom**
  Tool result shows "[object Object]" or repr() output.
  LLM can't parse the result. Follow-up responses reference
  wrong data. JSON parsing errors in next turn.
  
### **Why**
  LLMs process text. When you return a Python dict or JS object,
  it gets converted to string unpredictably. Some frameworks use
  repr(), others use JSON, others fail silently. The LLM sees
  garbage and hallucinates a reasonable-seeming interpretation.
  
### **Solution**
  # WRONG:
  def get_weather(location):
      return {"temp": 72, "conditions": "sunny"}  # Object!
  
  # CORRECT:
  def get_weather(location):
      result = {"temp": 72, "conditions": "sunny"}
      return json.dumps(result)  # String!
  
  # Or for simple results:
  def get_stock_price(ticker):
      price = fetch_price(ticker)
      return f"The current price of {ticker} is ${price}"  # String!
  
  # Always serialize to string before returning.
  
### **Detection Pattern**
  - return\s*\{
  - return\s*dict

## Error Results Without is_error Flag

### **Id**
missing-error-is-error-flag
### **Severity**
medium
### **Situation**
Returning error from tool execution
### **Symptom**
  LLM treats error message as success. Continues with bad data.
  Doesn't retry or ask for clarification. User sees error message
  presented as if it were a valid result.
  
### **Why**
  Without is_error flag, the LLM has no way to know the tool
  failed. It processes the error message as valid output and
  continues. "Error: Not found" becomes part of the answer.
  
### **Solution**
  # WRONG:
  return {"content": "Error: Location not found"}
  
  # CORRECT (Anthropic):
  return {
      "type": "tool_result",
      "tool_use_id": tool_id,
      "content": "Error: Location 'Atlantis' not found. Please provide
        a valid city name like 'San Francisco, CA'.",
      "is_error": true  # Critical!
  }
  
  # This tells Claude:
  # 1. The tool failed
  # 2. It should handle the error (retry, ask user, explain)
  # 3. Don't use this as valid data
  
### **Detection Pattern**
  - content.*[Ee]rror
  - return.*error

## Tool Name Collisions Across MCP Servers

### **Id**
tool-collision-mcp
### **Severity**
medium
### **Situation**
Connecting to multiple MCP servers
### **Symptom**
  Wrong tool gets called. Results from unexpected server.
  "Tool not found" errors for tools that exist. Unpredictable
  behavior depending on connection order.
  
### **Why**
  When multiple MCP servers define tools with the same name,
  which one gets called is undefined. The LLM sees all tools
  in a flat namespace and picks based on description match.
  
### **Solution**
  1. Use namespaced tool names:
     - weather_server:get_current
     - calendar_server:get_events
     - NOT: get_current, get_events
  
  2. Or prefix all tools:
     - weather_get_current
     - calendar_get_events
  
  3. Check for collisions at startup:
     all_tools = []
     for server in servers:
         tools = server.list_tools()
         for tool in tools:
             if tool.name in [t.name for t in all_tools]:
                 raise ToolCollisionError(f"Duplicate: {tool.name}")
             all_tools.append(tool)
  
### **Detection Pattern**
  - mcp.*server
  - connect.*server

## Executing Tools Without Input Validation

### **Id**
no-input-validation
### **Severity**
critical
### **Situation**
Processing LLM-provided parameters
### **Symptom**
  SQL injection. Command injection. Path traversal. Type errors
  crashing the tool. Malformed requests to external APIs.
  
### **Why**
  LLMs can hallucinate dangerous inputs. A confused model might
  send "'; DROP TABLE users; --" as a search query. Without
  validation, your tool executes whatever the LLM sends.
  
### **Solution**
  # ALWAYS validate before execution:
  
  def search_database(query: str) -> str:
      # Type validation
      if not isinstance(query, str):
          return error_result("Query must be a string")
  
      # Length validation
      if len(query) > 1000:
          return error_result("Query too long (max 1000 chars)")
  
      # Character validation
      if re.search(r'[;\'"\\]', query):
          return error_result("Query contains invalid characters")
  
      # Sanitization
      safe_query = sanitize_sql(query)
  
      # Now safe to execute
      return execute_query(safe_query)
  
  # For file operations:
  def read_file(path: str) -> str:
      # Path traversal prevention
      safe_path = os.path.abspath(path)
      if not safe_path.startswith(ALLOWED_DIR):
          return error_result("Path outside allowed directory")
      # ...
  
### **Detection Pattern**
  - def.*tool
  - execute
  - query

## Providing More Than 20 Tools

### **Id**
too-many-tools
### **Severity**
high
### **Situation**
Building an agent with many capabilities
### **Symptom**
  Wrong tool selection. Hallucinated tools. Slow responses.
  High token costs. Agent seems confused about capabilities.
  
### **Why**
  With 30+ tools, the LLM must parse all descriptions to decide
  which to use. Context gets crowded. Token costs increase.
  Probability of picking wrong tool increases with options.
  
### **Solution**
  1. Use dynamic tool loading (Tool Search):
     # Load only frequently-used tools
     # Fetch others on demand based on query
  
  2. Group related operations:
     # Instead of: create_user, read_user, update_user, delete_user
     # Use: manage_user(action: "create"|"read"|"update"|"delete")
  
  3. Remove rarely-used tools:
     # Track tool usage
     # Remove tools with <1% usage
  
  4. Use hierarchical tools:
     # High-level: "manage_calendar"
     # Internally routes to specific operations
  
### **Detection Pattern**
  - tools.*\[.*,.*,.*,.*,.*,.*,.*,.*,.*,.*,.*,.*,.*,.*,.*,.*,.*,.*,.*,.*,