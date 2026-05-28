# Ai Observability - Sharp Edges

## Langfuse Flush Not Called

### **Id**
langfuse-flush-not-called
### **Summary**
Traces don't appear in Langfuse dashboard
### **Severity**
high
### **Situation**
Using Langfuse SDK but traces are missing
### **Why**
  Langfuse batches traces for performance. If your function returns
  before the batch is flushed, traces are lost. Common in:
  - Serverless functions (Lambda, Vercel Edge)
  - Short-lived scripts
  - API routes that return quickly
  
  Without explicit flush, traces vanish silently.
  
### **Detection Pattern**
  langfuse\.trace|langfuse\.generation(?!.*flush|shutdown)
  
### **Solution**
  Always flush before function returns:
  
  ```typescript
  import { Langfuse } from "langfuse";
  
  const langfuse = new Langfuse({
    publicKey: process.env.LANGFUSE_PUBLIC_KEY!,
    secretKey: process.env.LANGFUSE_SECRET_KEY!,
    flushAt: 1, // Flush after every event in serverless
  });
  
  export async function handler(req: Request) {
    try {
      const trace = langfuse.trace({ name: "api-call" });
      // ... your logic
      return response;
    } finally {
      // CRITICAL: Always flush before returning
      await langfuse.flushAsync();
    }
  }
  
  // Or use shutdown on process exit
  process.on("beforeExit", async () => {
    await langfuse.shutdownAsync();
  });
  ```
  

## Prompt Cache Miss Cost

### **Id**
prompt-cache-miss-cost
### **Summary**
Cache writes cost more than regular tokens
### **Severity**
medium
### **Situation**
Using Anthropic prompt caching
### **Why**
  Anthropic charges 25% MORE for cache writes (first request).
  If your cache TTL expires before reuse, you pay premium for
  nothing. Break-even is 3-5 requests within 5-minute window.
  
  Caching small prompts or infrequent patterns wastes money.
  
### **Detection Pattern**
  cache_control.*ephemeral(?!.*frequent|repeated)
  
### **Solution**
  Only cache when break-even is likely:
  
  ```typescript
  // Calculate if caching is worthwhile
  function shouldCache(options: {
    promptTokens: number;
    expectedRequestsInTTL: number;
    ttlMinutes?: number;
  }): boolean {
    const { promptTokens, expectedRequestsInTTL, ttlMinutes = 5 } = options;
  
    // Minimum 1024 tokens for caching
    if (promptTokens < 1024) return false;
  
    // Break-even analysis
    // Cache write: 1.25x cost
    // Cache read: 0.1x cost
    // Regular: 1x cost per request
  
    const regularCost = promptTokens * expectedRequestsInTTL;
    const cachedCost = promptTokens * 1.25 + // Write
      promptTokens * 0.1 * (expectedRequestsInTTL - 1); // Reads
  
    return cachedCost < regularCost && expectedRequestsInTTL >= 3;
  }
  
  // Use conditionally
  const systemContent = shouldCache({
    promptTokens: estimateTokens(systemPrompt),
    expectedRequestsInTTL: requestsPerMinute * 5,
  })
    ? [{ type: "text", text: systemPrompt, cache_control: { type: "ephemeral" } }]
    : [{ type: "text", text: systemPrompt }];
  ```
  

## Helicone Proxy Latency

### **Id**
helicone-proxy-latency
### **Summary**
Helicone proxy adds latency
### **Severity**
medium
### **Situation**
Using Helicone for observability
### **Why**
  Helicone routes requests through their proxy. This adds
  10-50ms latency per request. For latency-critical apps
  (real-time chat, streaming), this may be unacceptable.
  
  Also: if Helicone has an outage, your LLM calls fail.
  
### **Detection Pattern**
  baseURL.*helicone(?!.*fallback|direct)
  
### **Solution**
  Implement fallback to direct API:
  
  ```typescript
  import OpenAI from "openai";
  
  // Primary: via Helicone
  const heliconeClient = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY!,
    baseURL: "https://oai.helicone.ai/v1",
    defaultHeaders: {
      "Helicone-Auth": `Bearer ${process.env.HELICONE_API_KEY}`,
    },
  });
  
  // Fallback: direct to OpenAI
  const directClient = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY!,
  });
  
  async function robustCompletion(
    options: OpenAI.ChatCompletionCreateParamsNonStreaming,
    useHelicone: boolean = true
  ) {
    if (!useHelicone) {
      return directClient.chat.completions.create(options);
    }
  
    try {
      const timeoutPromise = new Promise((_, reject) =>
        setTimeout(() => reject(new Error("Helicone timeout")), 5000)
      );
  
      return await Promise.race([
        heliconeClient.chat.completions.create(options),
        timeoutPromise,
      ]) as OpenAI.ChatCompletion;
    } catch (error) {
      console.warn("Helicone failed, falling back to direct:", error);
      return directClient.chat.completions.create(options);
    }
  }
  ```
  

## Ragas Eval Cost

### **Id**
ragas-eval-cost
### **Summary**
RAGAS evaluation costs more than the original call
### **Severity**
medium
### **Situation**
Running RAGAS evals on every production request
### **Why**
  RAGAS uses LLM-as-judge, meaning each eval makes multiple LLM calls:
  - Faithfulness: Extract claims + verify each claim
  - Answer relevancy: Generate reverse questions + compare
  - Context precision: Score each context chunk
  
  Running on 100% of traffic can cost 3-5x your actual LLM spend.
  
### **Detection Pattern**
  evaluateRAGAS|ragas.*evaluate(?!.*sample|batch|schedule)
  
### **Solution**
  Sample and batch evaluations:
  
  ```typescript
  import { db } from "./db";
  
  // Sample 5% of production traffic for evaluation
  async function maybeEvaluate(sample: RAGSample): Promise<void> {
    const shouldEval = Math.random() < 0.05; // 5% sample
  
    if (shouldEval) {
      // Queue for batch evaluation
      await db.evalQueue.create({
        data: {
          sample: JSON.stringify(sample),
          status: "pending",
          createdAt: new Date(),
        },
      });
    }
  }
  
  // Batch process evaluations off-peak
  // Run via cron at 3 AM
  async function processEvalBatch() {
    const pending = await db.evalQueue.findMany({
      where: { status: "pending" },
      take: 100, // Limit batch size
    });
  
    for (const item of pending) {
      const sample = JSON.parse(item.sample) as RAGSample;
      const scores = await evaluateRAGAS(sample);
  
      await db.evalQueue.update({
        where: { id: item.id },
        data: { status: "completed", scores: JSON.stringify(scores) },
      });
  
      // Rate limit to avoid cost spikes
      await new Promise((r) => setTimeout(r, 1000));
    }
  }
  ```
  

## Cost Tracking Lag

### **Id**
cost-tracking-lag
### **Summary**
Usage API data is delayed
### **Severity**
medium
### **Situation**
Real-time budget enforcement
### **Why**
  Provider usage APIs have delays:
  - OpenAI: Up to 48 hours for detailed usage
  - Anthropic: Up to 24 hours for billing data
  - Langfuse: Near real-time but may lag during high load
  
  Real-time budget enforcement using delayed data allows overspend.
  
### **Detection Pattern**
  checkBudget.*usage.*api(?!.*local|track|record)
  
### **Solution**
  Track locally, reconcile with provider:
  
  ```typescript
  // Local tracking (real-time)
  async function trackUsage(usage: {
    userId: string;
    tokens: number;
    cost: number;
  }) {
    // Increment in Redis for real-time limits
    await redis.incrbyfloat(`usage:${usage.userId}:month`, usage.cost);
    await redis.incrbyfloat(`usage:${usage.userId}:today`, usage.cost);
  
    // Also store in DB for history
    await db.tokenUsage.create({ data: usage });
  }
  
  // Check local budget (real-time)
  async function checkLocalBudget(userId: string): Promise<{
    allowed: boolean;
    used: number;
    limit: number;
  }> {
    const used = parseFloat(
      (await redis.get(`usage:${userId}:month`)) || "0"
    );
    const user = await db.user.findUnique({ where: { id: userId } });
    const limit = user?.monthlyBudget || 10;
  
    return {
      allowed: used < limit,
      used,
      limit,
    };
  }
  
  // Reconcile with provider (daily)
  async function reconcileWithProvider() {
    const providerUsage = await fetchProviderUsage(); // API call
    const localUsage = await db.tokenUsage.aggregate({...});
  
    const discrepancy = Math.abs(providerUsage.cost - localUsage.cost);
    if (discrepancy > 1) { // More than $1 difference
      await alertOps("Cost tracking discrepancy", { providerUsage, localUsage });
    }
  }
  ```
  

## Trace Data Pii

### **Id**
trace-data-pii
### **Summary**
Traces contain user PII
### **Severity**
high
### **Situation**
Tracing user prompts and responses
### **Why**
  Traces capture full prompts and responses. If users include:
  - Names, emails, phone numbers
  - Health information
  - Financial data
  - Passwords (users do paste them)
  
  You're storing PII in a third-party service. GDPR, HIPAA implications.
  
### **Detection Pattern**
  trace.*input|generation.*output(?!.*sanitize|redact)
  
### **Solution**
  Sanitize before tracing:
  
  ```typescript
  // PII patterns
  const PII_PATTERNS = [
    { pattern: /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/g, replacement: "[EMAIL]" },
    { pattern: /\b\d{3}[-.]?\d{3}[-.]?\d{4}\b/g, replacement: "[PHONE]" },
    { pattern: /\b\d{3}-\d{2}-\d{4}\b/g, replacement: "[SSN]" },
    { pattern: /\b\d{16}\b/g, replacement: "[CARD]" },
    { pattern: /password[:\s]+"[^"]+"/gi, replacement: 'password: "[REDACTED]"' },
  ];
  
  function sanitizeForTracing(text: string): string {
    let sanitized = text;
    for (const { pattern, replacement } of PII_PATTERNS) {
      sanitized = sanitized.replace(pattern, replacement);
    }
    return sanitized;
  }
  
  // Use when tracing
  const trace = langfuse.trace({
    name: "chat",
    input: sanitizeForTracing(userMessage),
  });
  
  generation.end({
    output: sanitizeForTracing(response),
  });
  ```
  

## Llm As Judge Bias

### **Id**
llm-as-judge-bias
### **Summary**
LLM judges favor their own outputs
### **Severity**
medium
### **Situation**
Using same model for generation and evaluation
### **Why**
  LLMs have self-preference bias. GPT-4 rates GPT-4 outputs higher.
  Claude rates Claude outputs higher. Using the same model to
  evaluate its own outputs gives inflated scores.
  
  Studies show 10-20% score inflation with same-model evaluation.
  
### **Detection Pattern**
  evaluate.*model.*same|generate.*evaluate.*model(?!.*different)
  
### **Solution**
  Use different models for generation and evaluation:
  
  ```typescript
  // Generation with Claude
  const generatedResponse = await anthropic.messages.create({
    model: "claude-sonnet-4-20250514",
    messages: [{ role: "user", content: userQuery }],
  });
  
  // Evaluation with GPT-4
  const evaluation = await openai.chat.completions.create({
    model: "gpt-4o",
    messages: [
      {
        role: "user",
        content: `Evaluate this response for quality: ${generatedResponse}`,
      },
    ],
  });
  
  // Or use smaller, specialized evaluation models
  // - Prometheus-2 for open-ended evaluation
  // - TruLens evaluation models
  ```
  

## Streaming Cost Tracking

### **Id**
streaming-cost-tracking
### **Summary**
Can't track tokens from streaming responses
### **Severity**
medium
### **Situation**
Using streaming with cost tracking
### **Why**
  Streaming responses don't include usage in the stream.
  You only get token counts at the end (or not at all).
  Cost tracking breaks if you only listen to stream events.
  
### **Detection Pattern**
  stream.*true(?!.*usage|finalize)
  
### **Solution**
  Capture final usage from stream:
  
  ```typescript
  import OpenAI from "openai";
  
  async function streamWithCostTracking(
    options: Omit<OpenAI.ChatCompletionCreateParamsStreaming, "stream">
  ) {
    const stream = await openai.chat.completions.create({
      ...options,
      stream: true,
      stream_options: { include_usage: true }, // Critical!
    });
  
    let content = "";
    let usage = { prompt_tokens: 0, completion_tokens: 0 };
  
    for await (const chunk of stream) {
      // Collect content
      const delta = chunk.choices[0]?.delta?.content || "";
      content += delta;
  
      // Capture usage from final chunk
      if (chunk.usage) {
        usage = {
          prompt_tokens: chunk.usage.prompt_tokens,
          completion_tokens: chunk.usage.completion_tokens,
        };
      }
    }
  
    // Now track costs
    const cost = calculateCost(options.model, usage.prompt_tokens, usage.completion_tokens);
    await trackUsage({ tokens: usage.prompt_tokens + usage.completion_tokens, cost });
  
    return { content, usage, cost };
  }
  ```
  

## Metric Aggregation Wrong

### **Id**
metric-aggregation-wrong
### **Summary**
Average latency hides P99 spikes
### **Severity**
medium
### **Situation**
Monitoring LLM latency
### **Why**
  Average latency of 500ms sounds fine. But if P99 is 5 seconds,
  1% of users have terrible experience. Token counts vary wildly,
  so variance is huge. Averages mislead.
  
### **Detection Pattern**
  avg.*latency|mean.*response(?!.*percentile|p95|p99)
  
### **Solution**
  Track percentiles, not averages:
  
  ```typescript
  import { Histogram } from "prom-client";
  
  const llmLatency = new Histogram({
    name: "llm_latency_seconds",
    help: "LLM response latency",
    labelNames: ["model", "operation"],
    buckets: [0.1, 0.25, 0.5, 1, 2.5, 5, 10, 30], // Seconds
  });
  
  async function trackedCompletion(options: CompletionOptions) {
    const end = llmLatency.startTimer({ model: options.model, operation: "chat" });
  
    try {
      const response = await openai.chat.completions.create(options);
      return response;
    } finally {
      end();
    }
  }
  
  // Query percentiles in Prometheus/Grafana:
  // histogram_quantile(0.99, llm_latency_seconds_bucket)
  // histogram_quantile(0.95, llm_latency_seconds_bucket)
  // histogram_quantile(0.50, llm_latency_seconds_bucket)
  ```
  