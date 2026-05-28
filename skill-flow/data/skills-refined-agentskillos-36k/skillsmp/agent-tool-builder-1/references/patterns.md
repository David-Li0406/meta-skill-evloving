# Agent Tool Builder

## Patterns


---
  #### **Name**
Tool Schema Design
  #### **Description**
Creating clear, unambiguous JSON Schema for tools
  #### **When**
Defining any new tool for an agent
  #### **Example**
    # TOOL SCHEMA BEST PRACTICES:
    
    ## 1. Detailed Descriptions (Most Important)
    """
    BAD - Too vague:
    {
      "name": "get_stock_price",
      "description": "Gets stock price",
      "input_schema": {
        "type": "object",
        "properties": {
          "ticker": {"type": "string"}
        }
      }
    }
    
    GOOD - Comprehensive:
    {
      "name": "get_stock_price",
      "description": "Retrieves the current stock price for a given ticker
        symbol. The ticker symbol must be a valid symbol for a publicly
        traded company on a major US stock exchange like NYSE or NASDAQ.
        Returns the latest trade price in USD. Use when the user asks
        about current or recent stock prices. Does NOT provide historical
        data, company info, or predictions.",
      "input_schema": {
        "type": "object",
        "properties": {
          "ticker": {
            "type": "string",
            "description": "The stock ticker symbol, e.g. AAPL for Apple Inc."
          }
        },
        "required": ["ticker"]
      }
    }
    """
    
    ## 2. Parameter Descriptions
    """
    Every parameter needs:
    - What it is
    - Format expected
    - Example value
    - Edge cases/limitations
    
    {
      "location": {
        "type": "string",
        "description": "City and state/country. Format: 'City, State' for US
          (e.g., 'San Francisco, CA') or 'City, Country' for international
          (e.g., 'Tokyo, Japan'). Do not use ZIP codes or coordinates."
      },
      "unit": {
        "type": "string",
        "enum": ["celsius", "fahrenheit"],
        "description": "Temperature unit. Defaults to user's locale if not
          specified. Use 'fahrenheit' for US users, 'celsius' for others."
      }
    }
    """
    
    ## 3. Use Enums When Possible
    """
    Enums constrain the LLM to valid values:
    
    "priority": {
      "type": "string",
      "enum": ["low", "medium", "high", "critical"],
      "description": "Task priority level"
    }
    
    "action": {
      "type": "string",
      "enum": ["create", "read", "update", "delete"],
      "description": "The CRUD operation to perform"
    }
    """
    
    ## 4. Required vs Optional
    """
    Be explicit about what's required:
    
    {
      "type": "object",
      "properties": {
        "query": {...},      // Required
        "limit": {...},      // Optional with default
        "offset": {...}      // Optional
      },
      "required": ["query"],
      "additionalProperties": false  // Strict mode
    }
    """
    

---
  #### **Name**
Tool with Input Examples
  #### **Description**
Using examples to guide LLM tool usage
  #### **When**
Complex tools with nested objects or format-sensitive inputs
  #### **Example**
    # TOOL USE EXAMPLES (Anthropic Beta Feature):
    
    """
    Examples show Claude concrete patterns that schemas can't express.
    Improves accuracy from 72% to 90% on complex operations.
    """
    
    {
      "name": "create_calendar_event",
      "description": "Creates a calendar event with optional attendees and reminders",
      "input_schema": {
        "type": "object",
        "properties": {
          "title": {"type": "string", "description": "Event title"},
          "start_time": {
            "type": "string",
            "description": "ISO 8601 datetime, e.g. 2024-03-15T14:00:00Z"
          },
          "duration_minutes": {"type": "integer", "description": "Event duration"},
          "attendees": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Email addresses of attendees"
          }
        },
        "required": ["title", "start_time", "duration_minutes"]
      },
      "input_examples": [
        {
          "title": "Team Standup",
          "start_time": "2024-03-15T09:00:00Z",
          "duration_minutes": 30,
          "attendees": ["alice@company.com", "bob@company.com"]
        },
        {
          "title": "Quick Chat",
          "start_time": "2024-03-15T14:00:00Z",
          "duration_minutes": 15
        },
        {
          "title": "Project Review",
          "start_time": "2024-03-15T16:00:00-05:00",
          "duration_minutes": 60,
          "attendees": ["team@company.com"]
        }
      ]
    }
    
    # EXAMPLE DESIGN PRINCIPLES:
    # - Use realistic data, not placeholders
    # - Show minimal, partial, and full specification patterns
    # - Keep concise: 1-5 examples per tool
    # - Focus on ambiguous cases
    

---
  #### **Name**
Tool Error Handling
  #### **Description**
Returning errors that help the LLM recover
  #### **When**
Any tool that can fail
  #### **Example**
    # ERROR HANDLING BEST PRACTICES:
    
    ## Return Informative Errors
    """
    BAD:
    {"error": "Failed"}
    {"error": true}
    
    GOOD:
    {
      "error": true,
      "error_type": "not_found",
      "message": "Location 'Atlantis' not found in weather database.
        Please provide a real city name like 'San Francisco, CA'.",
      "suggestions": ["San Francisco, CA", "Los Angeles, CA"]
    }
    """
    
    ## Anthropic Tool Result with Error
    """
    {
      "type": "tool_result",
      "tool_use_id": "toolu_01A09q90qw90lq917835lq9",
      "content": "Error: Location 'Atlantis' not found in weather database.
        Please provide a real city name like 'San Francisco, CA'.",
      "is_error": true
    }
    """
    
    ## Error Categories to Handle
    """
    1. Input Validation Errors
       - Missing required parameters
       - Invalid format
       - Out of range values
    
    2. External Service Errors
       - API unavailable
       - Rate limited
       - Timeout
    
    3. Business Logic Errors
       - Resource not found
       - Permission denied
       - Conflict/duplicate
    
    4. Internal Errors
       - Unexpected exceptions
       - Data corruption
    """
    
    ## Implementation Pattern
    """
    from dataclasses import dataclass
    from typing import Union
    
    @dataclass
    class ToolResult:
        success: bool
        content: str
        error_type: str = None
        suggestions: list[str] = None
    
        def to_response(self) -> dict:
            if self.success:
                return {"content": self.content}
            return {
                "content": f"Error ({self.error_type}): {self.content}",
                "is_error": True
            }
    
    def get_weather(location: str) -> ToolResult:
        # Validate input
        if not location or len(location) < 2:
            return ToolResult(
                success=False,
                content="Location must be at least 2 characters",
                error_type="validation_error"
            )
    
        try:
            data = weather_api.fetch(location)
            return ToolResult(
                success=True,
                content=f"Temperature: {data.temp}°F, Conditions: {data.conditions}"
            )
        except LocationNotFound:
            return ToolResult(
                success=False,
                content=f"Location '{location}' not found",
                error_type="not_found",
                suggestions=weather_api.suggest_locations(location)
            )
        except RateLimitError:
            return ToolResult(
                success=False,
                content="Weather service rate limit exceeded. Try again in 60 seconds.",
                error_type="rate_limit"
            )
        except Exception as e:
            return ToolResult(
                success=False,
                content=f"Unexpected error: {str(e)}",
                error_type="internal_error"
            )
    """
    

---
  #### **Name**
MCP Tool Pattern
  #### **Description**
Building tools using Model Context Protocol
  #### **When**
Creating reusable, cross-platform tools
  #### **Example**
    # MCP TOOL IMPLEMENTATION:
    
    """
    MCP (Model Context Protocol) is Anthropic's open standard for
    connecting AI agents to external systems. Build once, use everywhere.
    """
    
    ## Basic MCP Server (TypeScript)
    """
    import { Server } from "@modelcontextprotocol/sdk/server";
    import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio";
    
    const server = new Server({
      name: "weather-server",
      version: "1.0.0"
    });
    
    // Define tools
    server.setRequestHandler("tools/list", async () => ({
      tools: [
        {
          name: "get_weather",
          description: "Get current weather for a location. Returns
            temperature, conditions, and humidity. Use for weather
            queries about specific cities.",
          inputSchema: {
            type: "object",
            properties: {
              location: {
                type: "string",
                description: "City and state, e.g. 'San Francisco, CA'"
              },
              unit: {
                type: "string",
                enum: ["celsius", "fahrenheit"],
                default: "fahrenheit"
              }
            },
            required: ["location"]
          }
        }
      ]
    }));
    
    // Handle tool calls
    server.setRequestHandler("tools/call", async (request) => {
      const { name, arguments: args } = request.params;
    
      if (name === "get_weather") {
        try {
          const weather = await fetchWeather(args.location, args.unit);
          return {
            content: [
              {
                type: "text",
                text: JSON.stringify(weather)
              }
            ]
          };
        } catch (error) {
          return {
            content: [
              {
                type: "text",
                text: `Error: ${error.message}`
              }
            ],
            isError: true
          };
        }
      }
    
      throw new Error(`Unknown tool: ${name}`);
    });
    
    // Start server
    const transport = new StdioServerTransport();
    await server.connect(transport);
    """
    
    ## MCP Benefits
    """
    - Universal compatibility across LLM providers
    - Reusable tool libraries
    - Streaming and SSE transport support
    - Built-in observability
    - Tool access controls
    """
    

---
  #### **Name**
Tool Runner Pattern
  #### **Description**
Using SDK tool runners for automatic handling
  #### **When**
Building tool loops without manual management
  #### **Example**
    # TOOL RUNNER (Anthropic SDK Beta):
    
    """
    The tool runner handles the tool call loop automatically:
    - Executes tools when Claude calls them
    - Manages conversation state
    - Handles error retries
    - Provides streaming support
    """
    
    ## Python Example
    """
    import anthropic
    from anthropic import beta_tool
    
    client = anthropic.Anthropic()
    
    @beta_tool
    def get_weather(location: str, unit: str = "fahrenheit") -> str:
        '''Get the current weather in a given location.
    
        Args:
            location: The city and state, e.g. San Francisco, CA
            unit: Temperature unit, either 'celsius' or 'fahrenheit'
        '''
        # Implementation
        return json.dumps({"temperature": "72°F", "conditions": "Sunny"})
    
    @beta_tool
    def search_web(query: str) -> str:
        '''Search the web for information.
    
        Args:
            query: The search query
        '''
        # Implementation
        return json.dumps({"results": [...]})
    
    # Tool runner handles the loop
    runner = client.beta.messages.tool_runner(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        tools=[get_weather, search_web],
        messages=[
            {"role": "user", "content": "What's the weather in Paris?"}
        ]
    )
    
    # Process each message
    for message in runner:
        print(message.content[0].text)
    
    # Or just get final result
    final = runner.until_done()
    """
    
    ## TypeScript with Zod
    """
    import { Anthropic } from '@anthropic-ai/sdk';
    import { betaZodTool } from '@anthropic-ai/sdk/helpers/beta/zod';
    import { z } from 'zod';
    
    const anthropic = new Anthropic();
    
    const getWeatherTool = betaZodTool({
      name: 'get_weather',
      description: 'Get the current weather in a given location',
      inputSchema: z.object({
        location: z.string().describe('City and state, e.g. San Francisco, CA'),
        unit: z.enum(['celsius', 'fahrenheit']).default('fahrenheit')
      }),
      run: async (input) => {
        // Type-safe input!
        return JSON.stringify({temperature: '72°F'});
      }
    });
    
    const runner = anthropic.beta.messages.toolRunner({
      model: 'claude-sonnet-4-5',
      max_tokens: 1024,
      tools: [getWeatherTool],
      messages: [{ role: 'user', content: "What's the weather in Paris?" }]
    });
    
    for await (const message of runner) {
      console.log(message.content[0].text);
    }
    """
    

---
  #### **Name**
Parallel Tool Execution
  #### **Description**
Running multiple tools simultaneously
  #### **When**
Independent tool calls that can run in parallel
  #### **Example**
    # PARALLEL TOOL EXECUTION:
    
    """
    By default, Claude can call multiple tools in one response.
    This dramatically reduces latency for independent operations.
    """
    
    ## Handling Parallel Results
    """
    # Claude returns multiple tool_use blocks:
    response.content = [
        {"type": "text", "text": "I'll check both locations..."},
        {"type": "tool_use", "id": "toolu_01", "name": "get_weather",
         "input": {"location": "San Francisco, CA"}},
        {"type": "tool_use", "id": "toolu_02", "name": "get_weather",
         "input": {"location": "New York, NY"}},
        {"type": "tool_use", "id": "toolu_03", "name": "get_time",
         "input": {"timezone": "America/Los_Angeles"}},
        {"type": "tool_use", "id": "toolu_04", "name": "get_time",
         "input": {"timezone": "America/New_York"}}
    ]
    
    # Execute in parallel
    import asyncio
    
    async def execute_tools_parallel(tool_uses):
        tasks = [execute_tool(t) for t in tool_uses]
        return await asyncio.gather(*tasks)
    
    results = await execute_tools_parallel(tool_uses)
    
    # Return ALL results in SINGLE user message (critical!)
    tool_results = [
        {"type": "tool_result", "tool_use_id": "toolu_01", "content": "72°F, Sunny"},
        {"type": "tool_result", "tool_use_id": "toolu_02", "content": "45°F, Cloudy"},
        {"type": "tool_result", "tool_use_id": "toolu_03", "content": "2:30 PM PST"},
        {"type": "tool_result", "tool_use_id": "toolu_04", "content": "5:30 PM EST"}
    ]
    
    # CORRECT: All results in one message
    messages.append({"role": "user", "content": tool_results})
    
    # WRONG: Separate messages (breaks parallel execution pattern)
    # messages.append({"role": "user", "content": [tool_results[0]]})
    # messages.append({"role": "user", "content": [tool_results[1]]})
    """
    
    ## Encouraging Parallel Tool Use
    """
    Add to system prompt:
    "For maximum efficiency, whenever you need to perform multiple
    independent operations, invoke all relevant tools simultaneously
    rather than sequentially."
    """
    
    ## Disabling Parallel (When Needed)
    """
    response = client.messages.create(
        model="claude-sonnet-4-5",
        tools=tools,
        tool_choice={"type": "auto", "disable_parallel_tool_use": True},
        messages=messages
    )
    """
    

## Anti-Patterns


---
  #### **Name**
Vague Descriptions
  #### **Description**
Tool descriptions that don't explain when/how to use the tool
  #### **Why**
    LLMs only see the schema and description. A vague description means the
    LLM has to guess when to use the tool, what format to use, and what to
    expect. This leads to wrong tool selection, bad parameters, and wasted
    tokens on retries.
    
  #### **Instead**
    Write 3-4 sentences minimum. Include: what it does, when to use it,
    when NOT to use it, parameter format expectations, and what it returns.
    

---
  #### **Name**
Silent Failures
  #### **Description**
Tools that return empty or unclear results on error
  #### **Why**
    When a tool fails silently, the agent continues with bad data or
    hallucinates missing information. The user sees wrong results with
    no indication anything went wrong. Debugging becomes impossible.
    
  #### **Instead**
    Always return explicit error messages with is_error: true.
    Include error type, human-readable message, and suggestions for fixing.
    

---
  #### **Name**
Too Many Tools
  #### **Description**
Providing 20+ tools to an agent
  #### **Why**
    More tools = more confusion. The LLM has to parse all tool descriptions
    to decide which to use. With 30 tools, it's more likely to pick wrong
    or hallucinate a tool that doesn't exist. Token costs increase too.
    
  #### **Instead**
    Aim for <20 tools. Use tool search (dynamic loading) for large
    libraries. Group related operations into fewer, smarter tools.
    

---
  #### **Name**
Object Returns
  #### **Description**
Returning Python objects or complex structures instead of strings
  #### **Why**
    LLMs process text. Returning a Python dict doesn't automatically
    serialize to something useful. The LLM may see repr() output or
    get type errors. Inconsistent return formats cause parsing issues.
    
  #### **Instead**
    Always return strings. For structured data, return JSON.stringify().
    For simple results, return plain text. Be consistent.
    

---
  #### **Name**
Missing Validation
  #### **Description**
Trusting LLM inputs without validation
  #### **Why**
    LLMs can send malformed, out-of-range, or even malicious inputs.
    SQL injection through tool parameters is possible. Without validation,
    you're one hallucination away from a security incident or crash.
    
  #### **Instead**
    Validate all inputs before execution. Check types, ranges, formats.
    Sanitize strings that will be used in queries or commands.
    Return validation errors, don't throw exceptions.
    

---
  #### **Name**
No Examples
  #### **Description**
Complex tools without usage examples
  #### **Why**
    JSON Schema can express structure but not intent. For tools with
    nested objects, optional parameters, or format-sensitive inputs,
    the LLM needs to see concrete examples to understand the pattern.
    
  #### **Instead**
    Use input_examples for complex tools. Show minimal, partial, and
    full parameter patterns. Use realistic data, not placeholders.
    