# AI Wrapper Product

## Patterns


---
  #### **Name**
AI Product Architecture
  #### **Description**
Building products around AI APIs
  #### **When To Use**
When designing an AI-powered product
  #### **Implementation**
    ## AI Product Architecture
    
    ### The Wrapper Stack
    ```
    User Input
        ↓
    Input Validation + Sanitization
        ↓
    Prompt Template + Context
        ↓
    AI API (OpenAI/Anthropic/etc.)
        ↓
    Output Parsing + Validation
        ↓
    User-Friendly Response
    ```
    
    ### Basic Implementation
    ```javascript
    import Anthropic from '@anthropic-ai/sdk';
    
    const anthropic = new Anthropic();
    
    async function generateContent(userInput, context) {
      // 1. Validate input
      if (!userInput || userInput.length > 5000) {
        throw new Error('Invalid input');
      }
    
      // 2. Build prompt
      const systemPrompt = `You are a ${context.role}.
        Always respond in ${context.format}.
        Tone: ${context.tone}`;
    
      // 3. Call API
      const response = await anthropic.messages.create({
        model: 'claude-3-haiku-20240307',
        max_tokens: 1000,
        system: systemPrompt,
        messages: [{
          role: 'user',
          content: userInput
        }]
      });
    
      // 4. Parse and validate output
      const output = response.content[0].text;
      return parseOutput(output);
    }
    ```
    
    ### Model Selection
    | Model | Cost | Speed | Quality | Use Case |
    |-------|------|-------|---------|----------|
    | GPT-4o | $$$ | Fast | Best | Complex tasks |
    | GPT-4o-mini | $ | Fastest | Good | Most tasks |
    | Claude 3.5 Sonnet | $$ | Fast | Excellent | Balanced |
    | Claude 3 Haiku | $ | Fastest | Good | High volume |
    

---
  #### **Name**
Prompt Engineering for Products
  #### **Description**
Production-grade prompt design
  #### **When To Use**
When building AI product prompts
  #### **Implementation**
    ## Prompt Engineering for Products
    
    ### Prompt Template Pattern
    ```javascript
    const promptTemplates = {
      emailWriter: {
        system: `You are an expert email writer.
          Write professional, concise emails.
          Match the requested tone.
          Never include placeholder text.`,
        user: (input) => `Write an email:
          Purpose: ${input.purpose}
          Recipient: ${input.recipient}
          Tone: ${input.tone}
          Key points: ${input.points.join(', ')}
          Length: ${input.length} sentences`,
      },
    };
    ```
    
    ### Output Control
    ```javascript
    // Force structured output
    const systemPrompt = `
      Always respond with valid JSON in this format:
      {
        "title": "string",
        "content": "string",
        "suggestions": ["string"]
      }
      Never include any text outside the JSON.
    `;
    
    // Parse with fallback
    function parseAIOutput(text) {
      try {
        return JSON.parse(text);
      } catch {
        // Fallback: extract JSON from response
        const match = text.match(/\{[\s\S]*\}/);
        if (match) return JSON.parse(match[0]);
        throw new Error('Invalid AI output');
      }
    }
    ```
    
    ### Quality Control
    | Technique | Purpose |
    |-----------|---------|
    | Examples in prompt | Guide output style |
    | Output format spec | Consistent structure |
    | Validation | Catch malformed responses |
    | Retry logic | Handle failures |
    | Fallback models | Reliability |
    

---
  #### **Name**
Cost Management
  #### **Description**
Controlling AI API costs
  #### **When To Use**
When building profitable AI products
  #### **Implementation**
    ## AI Cost Management
    
    ### Token Economics
    ```javascript
    // Track usage
    async function callWithCostTracking(userId, prompt) {
      const response = await anthropic.messages.create({...});
    
      // Log usage
      await db.usage.create({
        userId,
        inputTokens: response.usage.input_tokens,
        outputTokens: response.usage.output_tokens,
        cost: calculateCost(response.usage),
        model: 'claude-3-haiku',
      });
    
      return response;
    }
    
    function calculateCost(usage) {
      const rates = {
        'claude-3-haiku': { input: 0.25, output: 1.25 }, // per 1M tokens
      };
      const rate = rates['claude-3-haiku'];
      return (usage.input_tokens * rate.input +
              usage.output_tokens * rate.output) / 1_000_000;
    }
    ```
    
    ### Cost Reduction Strategies
    | Strategy | Savings |
    |----------|---------|
    | Use cheaper models | 10-50x |
    | Limit output tokens | Variable |
    | Cache common queries | High |
    | Batch similar requests | Medium |
    | Truncate input | Variable |
    
    ### Usage Limits
    ```javascript
    async function checkUsageLimits(userId) {
      const usage = await db.usage.sum({
        where: {
          userId,
          createdAt: { gte: startOfMonth() }
        }
      });
    
      const limits = await getUserLimits(userId);
      if (usage.cost >= limits.monthlyCost) {
        throw new Error('Monthly limit reached');
      }
      return true;
    }
    ```
    

---
  #### **Name**
AI Product Differentiation
  #### **Description**
Standing out from other AI wrappers
  #### **When To Use**
When planning AI product strategy
  #### **Implementation**
    ## AI Product Differentiation
    
    ### What Makes AI Products Defensible
    | Moat | Example |
    |------|---------|
    | Workflow integration | Email inside Gmail |
    | Domain expertise | Legal AI with law training |
    | Data/context | Company-specific knowledge |
    | UX excellence | Perfectly designed for task |
    | Distribution | Built-in audience |
    
    ### Differentiation Strategies
    ```
    1. Vertical Focus
       Generic: "AI writing assistant"
       Specific: "AI for Amazon product descriptions"
    
    2. Workflow Integration
       Standalone: Web app
       Integrated: Chrome extension, Slack bot
    
    3. Domain Training
       Generic: Uses raw GPT
       Specialized: Fine-tuned or RAG-enhanced
    
    4. Output Quality
       Basic: Raw AI output
       Polished: Post-processing, formatting, validation
    ```
    
    ### Avoid "Thin Wrappers"
    | Thin Wrapper | Real Product |
    |--------------|--------------|
    | ChatGPT with custom prompt | Domain-specific workflow tool |
    | API passthrough | Processed, validated outputs |
    | Single feature | Complete solution |
    | No unique value | Solves specific pain point |
    

## Anti-Patterns


---
  #### **Name**
Thin Wrapper Syndrome
  #### **Description**
Just wrapping API with no added value
  #### **Why Bad**
    No differentiation.
    Users just use ChatGPT.
    No pricing power.
    Easy to replicate.
    
  #### **What To Do Instead**
    Add domain expertise.
    Perfect the UX for specific task.
    Integrate into workflows.
    Post-process outputs.
    

---
  #### **Name**
Ignoring Costs Until Scale
  #### **Description**
Not tracking API costs from day one
  #### **Why Bad**
    Surprise bills.
    Negative unit economics.
    Can't price properly.
    Business isn't viable.
    
  #### **What To Do Instead**
    Track every API call.
    Know your cost per user.
    Set usage limits.
    Price with margin.
    

---
  #### **Name**
No Output Validation
  #### **Description**
Showing raw AI output to users
  #### **Why Bad**
    AI hallucinates.
    Inconsistent formatting.
    Bad user experience.
    Trust issues.
    
  #### **What To Do Instead**
    Validate all outputs.
    Parse structured responses.
    Have fallback handling.
    Post-process for consistency.
    