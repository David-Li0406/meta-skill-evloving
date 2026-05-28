# OpenAI Function Calling

## Basic Function Calling

### 1. Define Functions
```typescript
const tools: OpenAI.ChatCompletionTool[] = [
  {
    type: 'function',
    function: {
      name: 'search_textbook',
      description: 'Search the Physical AI textbook for specific topics or chapters',
      parameters: {
        type: 'object',
        properties: {
          query: {
            type: 'string',
            description: 'The search query or topic',
          },
          chapter: {
            type: 'string',
            description: 'Optional: specific chapter number (1-6)',
            enum: ['1', '2', '3', '4', '5', '6'],
          },
        },
        required: ['query'],
      },
    },
  },
  {
    type: 'function',
    function: {
      name: 'get_code_example',
      description: 'Get code examples for ROS 2, Python, or C++',
      parameters: {
        type: 'object',
        properties: {
          topic: {
            type: 'string',
            description: 'Programming topic (e.g., "publisher node", "URDF robot")',
          },
          language: {
            type: 'string',
            enum: ['python', 'cpp'],
          },
        },
        required: ['topic', 'language'],
      },
    },
  },
];
```

### 2. Chat with Tools
```typescript
const completion = await openai.chat.completions.create({
  model: 'gpt-4',
  messages: [
    { role: 'system', content: 'You are a Physical AI tutor.' },
    { role: 'user', content: 'How does ROS 2 pub/sub work?' },
  ],
  tools,
  tool_choice: 'auto', // Let GPT decide when to call functions
});
```

### 3. Handle Function Calls
```typescript
const responseMessage = completion.choices[0].message;

if (responseMessage.tool_calls) {
  // GPT wants to call a function
  const toolCalls = responseMessage.tool_calls;
  
  for (const toolCall of toolCalls) {
    const functionName = toolCall.function.name;
    const functionArgs = JSON.parse(toolCall.function.arguments);
    
    let functionResponse;
    
    if (functionName === 'search_textbook') {
      functionResponse = await searchTextbook(functionArgs.query, functionArgs.chapter);
    } else if (functionName === 'get_code_example') {
      functionResponse = await getCodeExample(functionArgs.topic, functionArgs.language);
    }
    
    // Add function result to conversation
    messages.push(responseMessage);
    messages.push({
      role: 'tool',
      tool_call_id: toolCall.id,
      content: JSON.stringify(functionResponse),
    });
  }
  
  // Get final response with function results
  const finalCompletion = await openai.chat.completions.create({
    model: 'gpt-4',
    messages,
  });
  
  return finalCompletion.choices[0].message.content;
}
```

## Real Implementation Example

```typescript
async function chatWithTools(userMessage: string, conversationHistory: any[]) {
  const messages = [
    { role: 'system', content: TUTOR_PROMPT },
    ...conversationHistory,
    { role: 'user', content: userMessage },
  ];
  
  const completion = await openai.chat.completions.create({
    model: 'gpt-4',
    messages,
    tools,
    tool_choice: 'auto',
  });
  
  const responseMessage = completion.choices[0].message;
  
  // Check for tool calls
  if (responseMessage.tool_calls) {
    messages.push(responseMessage);
    
    // Execute all tool calls
    for (const toolCall of responseMessage.tool_calls) {
      const { name, arguments: args } = toolCall.function;
      const parsedArgs = JSON.parse(args);
      
      const result = await executeTool(name, parsedArgs);
      
      messages.push({
        role: 'tool',
        tool_call_id: toolCall.id,
        content: JSON.stringify(result),
      });
    }
    
    // Get final answer
    const finalResponse = await openai.chat.completions.create({
      model: 'gpt-4',
      messages,
    });
    
    return finalResponse.choices[0].message.content;
  }
  
  return responseMessage.content;
}

async function executeTool(name: string, args: any) {
  switch (name) {
    case 'search_textbook':
      return await searchQdrant(args.query, args.chapter);
    case 'get_code_example':
      return await getCodeFromDatabase(args.topic, args.language);
    default:
      throw new Error(`Unknown tool: ${name}`);
  }
}
```

## Forcing Function Calls

```typescript
// Always call a specific function
const completion = await openai.chat.completions.create({
  model: 'gpt-4',
  messages,
  tools,
  tool_choice: {
    type: 'function',
    function: { name: 'search_textbook' },
  },
});
```

## Parallel Function Calling

GPT-4 can call multiple functions at once:

```typescript
// User: "Search for ROS 2 and get Python examples"
// GPT might call both functions simultaneously

if (responseMessage.tool_calls && responseMessage.tool_calls.length > 1) {
  // Execute in parallel
  const results = await Promise.all(
    responseMessage.tool_calls.map(async (toolCall) => {
      const result = await executeTool(
        toolCall.function.name,
        JSON.parse(toolCall.function.arguments)
      );
      
      return {
        role: 'tool',
        tool_call_id: toolCall.id,
        content: JSON.stringify(result),
      };
    })
  );
  
  messages.push(responseMessage, ...results);
}
```

## Best Practices

1. **Clear descriptions**: Help GPT know when to call functions
2. **Validate arguments**: Parse and validate before execution
3. **Handle errors**: Wrap in try/catch, send error as tool response
4. **Limit tools**: Don't overwhelm with too many functions (max 5-10)
5. **Use enums**: Constrain choices when possible
