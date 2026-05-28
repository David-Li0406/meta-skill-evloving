# AI Product Development

## Patterns


---
  #### **Name**
Structured Output with Validation
  #### **Description**
Use function calling or JSON mode with schema validation
  #### **When**
LLM output will be used programmatically
  #### **Example**
    import { z } from 'zod';
    
    const schema = z.object({
      category: z.enum(['bug', 'feature', 'question']),
      priority: z.number().min(1).max(5),
      summary: z.string().max(200)
    });
    
    const response = await openai.chat.completions.create({
      model: 'gpt-4',
      messages: [{ role: 'user', content: prompt }],
      response_format: { type: 'json_object' }
    });
    
    const parsed = schema.parse(JSON.parse(response.content));
    

---
  #### **Name**
Streaming with Progress
  #### **Description**
Stream LLM responses to show progress and reduce perceived latency
  #### **When**
User-facing chat or generation features
  #### **Example**
    const stream = await openai.chat.completions.create({
      model: 'gpt-4',
      messages,
      stream: true
    });
    
    for await (const chunk of stream) {
      const content = chunk.choices[0]?.delta?.content;
      if (content) {
        yield content; // Stream to client
      }
    }
    

---
  #### **Name**
Prompt Versioning and Testing
  #### **Description**
Version prompts in code and test with regression suite
  #### **When**
Any production prompt
  #### **Example**
    // prompts/categorize-ticket.ts
    export const CATEGORIZE_TICKET_V2 = {
      version: '2.0',
      system: 'You are a support ticket categorizer...',
      test_cases: [
        { input: 'Login broken', expected: { category: 'bug' } },
        { input: 'Want dark mode', expected: { category: 'feature' } }
      ]
    };
    
    // Test in CI
    const result = await llm.generate(prompt, test_case.input);
    assert.equal(result.category, test_case.expected.category);
    

---
  #### **Name**
Caching Expensive Operations
  #### **Description**
Cache embeddings and deterministic LLM responses
  #### **When**
Same queries processed repeatedly
  #### **Example**
    // Cache embeddings (expensive to compute)
    const cacheKey = `embedding:${hash(text)}`;
    let embedding = await cache.get(cacheKey);
    
    if (!embedding) {
      embedding = await openai.embeddings.create({
        model: 'text-embedding-3-small',
        input: text
      });
      await cache.set(cacheKey, embedding, '30d');
    }
    

---
  #### **Name**
Circuit Breaker for LLM Failures
  #### **Description**
Graceful degradation when LLM API fails or returns garbage
  #### **When**
Any LLM integration in critical path
  #### **Example**
    const circuitBreaker = new CircuitBreaker(callLLM, {
      threshold: 5, // failures
      timeout: 30000, // ms
      resetTimeout: 60000 // ms
    });
    
    try {
      const response = await circuitBreaker.fire(prompt);
      return response;
    } catch (error) {
      // Fallback: rule-based system, cached response, or human queue
      return fallbackHandler(prompt);
    }
    

---
  #### **Name**
RAG with Hybrid Search
  #### **Description**
Combine semantic search with keyword matching for better retrieval
  #### **When**
Implementing RAG systems
  #### **Example**
    // 1. Semantic search (vector similarity)
    const embedding = await embed(query);
    const semanticResults = await vectorDB.search(embedding, topK: 20);
    
    // 2. Keyword search (BM25)
    const keywordResults = await fullTextSearch(query, topK: 20);
    
    // 3. Rerank combined results
    const combined = rerank([...semanticResults, ...keywordResults]);
    const topChunks = combined.slice(0, 5);
    
    // 4. Add to prompt
    const context = topChunks.map(c => c.text).join('\n\n');
    

## Anti-Patterns


---
  #### **Name**
Demo-ware
  #### **Description**
AI features that work in demos but fail in production
  #### **Example**
    Works with perfect input, falls apart with typos, edge cases,
    adversarial input, or high volume
    
  #### **Why Bad**
Demos deceive. Production reveals truth. Users lose trust fast.
  #### **Fix**
Test with real messy data. Add validation. Handle failures gracefully.

---
  #### **Name**
Context window stuffing
  #### **Description**
Cramming everything into the context window
  #### **Example**
    Entire codebase in context, all docs in prompt, no retrieval
    
  #### **Why Bad**
Expensive, slow, hits limits. Dilutes relevant context with noise.
  #### **Fix**
Smart retrieval (RAG). Only include relevant context. Summarize.

---
  #### **Name**
Unstructured output parsing
  #### **Description**
Parsing free-form text instead of structured output
  #### **Example**
    Asking for JSON in the prompt, parsing response with regex
    
  #### **Why Bad**
Breaks randomly. Inconsistent formats. Injection risks.
  #### **Fix**
Use function calling / tool use. Validate with Zod. Retry on failure.

---
  #### **Name**
No fallback strategy
  #### **Description**
App breaks when LLM fails or returns garbage
  #### **Example**
No error handling, no human fallback, no graceful degradation
  #### **Why Bad**
APIs fail. Rate limits hit. Garbage in = garbage out.
  #### **Fix**
Circuit breakers. Fallback to rules. Human-in-the-loop for critical paths.

---
  #### **Name**
Ignoring safety
  #### **Description**
No guardrails for harmful or incorrect output
  #### **Example**
    LLM outputs go directly to users, no content filtering, no fact checking
    
  #### **Why Bad**
Hallucinations, inappropriate content, liability. Brand damage.
  #### **Fix**
Content filters. Confidence thresholds. Human review for high-stakes.

---
  #### **Name**
No Output Validation
  #### **Description**
Using LLM output directly without validation
  #### **Why**
LLMs hallucinate, format responses incorrectly, return garbage
  #### **Instead**
    Parse with schema validation (Zod).
    Retry with clarified prompt on parse failure.
    Fallback to safe default if validation fails multiple times.
    

---
  #### **Name**
Synchronous LLM Calls in Request Path
  #### **Description**
Waiting for LLM response before returning to user
  #### **Why**
Slow, blocks user, fails if API timeout
  #### **Instead**
    Stream response for perceived speed.
    Or: queue job, return immediately, notify on completion.
    Show loading state with estimated time.
    

---
  #### **Name**
Prompt Injection Ignorance
  #### **Description**
Not sanitizing user input in prompts
  #### **Why**
Users can manipulate LLM to ignore instructions or leak data
  #### **Instead**
    Clearly separate instructions from user input:
    System: You are a customer service agent...
    User input (untrusted): {userMessage}
    
    Validate output matches expected behavior.
    

---
  #### **Name**
Single Model for Everything
  #### **Description**
Using GPT-4 for all tasks regardless of complexity
  #### **Why**
Expensive, slow for simple tasks
  #### **Instead**
    Simple classification → GPT-3.5-turbo
    Code generation → GPT-4
    Embeddings → text-embedding-3-small
    Measure cost per task and optimize.
    

---
  #### **Name**
No Monitoring or Observability
  #### **Description**
Shipping LLM features without tracking performance
  #### **Why**
Cannot debug failures, optimize costs, or measure quality
  #### **Instead**
    Log: prompt, response, latency, cost, validation failures
    Monitor: success rate, latency p95, cost per day
    Alert: on quality degradation or cost spikes
    

---
  #### **Name**
Treating Prompts as Magic
  #### **Description**
Not understanding why prompt works, just that it does
  #### **Why**
Breaks on edge cases, cannot debug, cannot improve systematically
  #### **Instead**
    Document why each instruction is needed.
    Test with edge cases and adversarial inputs.
    A/B test prompt changes with metrics.
    