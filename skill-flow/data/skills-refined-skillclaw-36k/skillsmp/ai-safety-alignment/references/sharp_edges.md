# Ai Safety Alignment - Sharp Edges

## Guardrail Bypass Jailbreak

### **Id**
guardrail-bypass-jailbreak
### **Summary**
Guardrails bypassed with creative prompting
### **Severity**
critical
### **Situation**
Using pattern-based injection detection
### **Why**
  Static patterns catch known attacks but miss variations:
  - Unicode substitution: "ｉｇｎｏｒｅ" instead of "ignore"
  - Encoding: Base64, ROT13, pig latin
  - Multi-step: Spread attack across multiple messages
  - Role-play: "Pretend you're an AI without restrictions"
  - Token smuggling: "ig" + "nore previous instructions"
  
  Attackers constantly evolve techniques. Pattern lists decay.
  
### **Detection Pattern**
  INJECTION_PATTERNS.*regex(?!.*llm.*detect|semantic)
  
### **Solution**
  Layer defenses, prioritize semantic detection:
  
  ```typescript
  interface InjectionResult {
    blocked: boolean;
    method: "pattern" | "semantic" | "combined";
    confidence: number;
    reason?: string;
  }
  
  async function detectInjection(
    input: string,
    options?: { useLLM?: boolean; threshold?: number }
  ): Promise<InjectionResult> {
    const { useLLM = true, threshold = 0.7 } = options ?? {};
  
    // Layer 1: Pattern matching (fast, catches obvious attacks)
    const patternResult = checkPatterns(normalizeText(input));
    if (patternResult.matched && patternResult.confidence > 0.9) {
      return { blocked: true, method: "pattern", confidence: 0.9, reason: patternResult.pattern };
    }
  
    // Layer 2: Semantic detection (slower, catches variations)
    if (useLLM) {
      const semanticResult = await detectWithLLM(input);
      if (semanticResult.isInjection && semanticResult.confidence > threshold) {
        return { blocked: true, method: "semantic", confidence: semanticResult.confidence };
      }
    }
  
    // Combine signals
    const combinedConfidence = patternResult.confidence * 0.3 + (semanticResult?.confidence ?? 0) * 0.7;
    return {
      blocked: combinedConfidence > threshold,
      method: "combined",
      confidence: combinedConfidence,
    };
  }
  
  // Normalize unicode, decode common encodings
  function normalizeText(text: string): string {
    return text
      .normalize("NFKC") // Unicode normalization
      .toLowerCase()
      .replace(/[\u200B-\u200D\uFEFF]/g, ""); // Zero-width chars
  }
  ```
  

## Moderation False Positive

### **Id**
moderation-false-positive
### **Summary**
Legitimate content blocked as harmful
### **Severity**
high
### **Situation**
Using OpenAI Moderation API
### **Why**
  Moderation APIs have false positives:
  - Medical discussions flagged as self-harm
  - Historical content flagged as hate
  - Security discussions flagged as violence
  - Literary quotes flagged incorrectly
  
  Blocking legitimate users damages trust and usability.
  
### **Detection Pattern**
  moderation.*flagged.*reject(?!.*review|appeal|context)
  
### **Solution**
  Add context and human review for edge cases:
  
  ```typescript
  interface ModerationResult {
    action: "allow" | "block" | "review";
    categories: string[];
    context?: string;
  }
  
  async function moderateWithContext(
    content: string,
    context: {
      domain: "medical" | "legal" | "educational" | "general";
      userTrust: number; // 0-1
    }
  ): Promise<ModerationResult> {
    const result = await openai.moderations.create({ input: content });
    const flagged = result.results[0];
  
    if (!flagged.flagged) {
      return { action: "allow", categories: [] };
    }
  
    // Check domain-specific exceptions
    const categories = Object.entries(flagged.categories)
      .filter(([_, v]) => v)
      .map(([k]) => k);
  
    // Medical domain: allow self-harm discussions in clinical context
    if (context.domain === "medical" && categories.includes("self-harm")) {
      const isClinical = await checkClinicalContext(content);
      if (isClinical) {
        return { action: "allow", categories, context: "clinical-exception" };
      }
    }
  
    // High-trust users get review instead of block
    if (context.userTrust > 0.8) {
      return { action: "review", categories };
    }
  
    // Educational content: allow historical discussions
    if (context.domain === "educational" && categories.includes("hate")) {
      return { action: "review", categories, context: "educational-review" };
    }
  
    return { action: "block", categories };
  }
  ```
  

## Moderation False Negative

### **Id**
moderation-false-negative
### **Summary**
Harmful content passes moderation
### **Severity**
critical
### **Situation**
Relying solely on moderation API
### **Why**
  Moderation APIs miss:
  - Subtle harassment and microaggressions
  - Domain-specific harmful advice
  - Context-dependent harm
  - Novel attack patterns
  - Non-English content (weaker coverage)
  
  A single layer creates single point of failure.
  
### **Detection Pattern**
  moderation.*create(?!.*&&|additional|layer)
  
### **Solution**
  Layer multiple moderation approaches:
  
  ```typescript
  interface MultiLayerResult {
    safe: boolean;
    layers: {
      openai: boolean;
      custom: boolean;
      domain: boolean;
    };
    reason?: string;
  }
  
  async function multiLayerModeration(
    content: string,
    domain?: string
  ): Promise<MultiLayerResult> {
    const [openaiResult, customResult, domainResult] = await Promise.all([
      // Layer 1: OpenAI Moderation (general harm)
      openai.moderations.create({ input: content }),
  
      // Layer 2: Custom patterns (business-specific)
      checkCustomPatterns(content),
  
      // Layer 3: Domain-specific rules
      domain ? checkDomainRules(content, domain) : Promise.resolve({ safe: true }),
    ]);
  
    const layers = {
      openai: !openaiResult.results[0].flagged,
      custom: customResult.safe,
      domain: domainResult.safe,
    };
  
    // All layers must pass
    const safe = Object.values(layers).every(Boolean);
  
    return {
      safe,
      layers,
      reason: safe ? undefined : Object.entries(layers).find(([_, v]) => !v)?.[0],
    };
  }
  ```
  

## Pii Detection Incomplete

### **Id**
pii-detection-incomplete
### **Summary**
PII leaks through detection gaps
### **Severity**
high
### **Situation**
Using regex-based PII detection
### **Why**
  Regex patterns miss:
  - International phone formats (+44, +91, etc.)
  - Non-US ID numbers (NHS, national IDs)
  - Names (infinite variations)
  - Addresses (many formats)
  - Context-dependent PII (employee IDs, account numbers)
  
  Partial protection creates false confidence.
  
### **Detection Pattern**
  PII_PATTERNS.*regex(?!.*spacy|presidio|comprehend)
  
### **Solution**
  Use ML-based PII detection:
  
  ```typescript
  import { AnalyzeAction, PresidioAnalyzer } from "presidio-analyzer";
  
  // Or use AWS Comprehend for managed service
  import { ComprehendClient, DetectPiiEntitiesCommand } from "@aws-sdk/client-comprehend";
  
  interface PIIResult {
    found: boolean;
    entities: Array<{
      type: string;
      text: string;
      start: number;
      end: number;
      confidence: number;
    }>;
    redacted: string;
  }
  
  async function detectPIIWithML(text: string): Promise<PIIResult> {
    const client = new ComprehendClient({ region: "us-east-1" });
  
    const command = new DetectPiiEntitiesCommand({
      Text: text,
      LanguageCode: "en",
    });
  
    const response = await client.send(command);
  
    const entities = (response.Entities ?? []).map((e) => ({
      type: e.Type!,
      text: text.slice(e.BeginOffset!, e.EndOffset!),
      start: e.BeginOffset!,
      end: e.EndOffset!,
      confidence: e.Score!,
    }));
  
    // Redact detected PII
    let redacted = text;
    for (const entity of entities.sort((a, b) => b.start - a.start)) {
      redacted = redacted.slice(0, entity.start) + `[${entity.type}]` + redacted.slice(entity.end);
    }
  
    return {
      found: entities.length > 0,
      entities,
      redacted,
    };
  }
  ```
  

## Output Filter Bypass

### **Id**
output-filter-bypass
### **Summary**
Harmful content in LLM output bypasses filters
### **Severity**
high
### **Situation**
Only filtering input, not output
### **Why**
  LLMs can generate harmful content even with safe inputs:
  - Jailbroken base model
  - Training data contamination
  - Prompt injection in retrieved context (RAG)
  - Model hallucinating harmful content
  
  Input filtering alone is insufficient.
  
### **Detection Pattern**
  validateInput(?!.*validateOutput|filterOutput)
  
### **Solution**
  Filter both input AND output:
  
  ```typescript
  interface SafeCompletionResult {
    content: string;
    filtered: boolean;
    inputBlocked: boolean;
    outputFiltered: boolean;
  }
  
  async function safeCompletion(
    messages: Array<{ role: string; content: string }>,
    options?: { strictOutput?: boolean }
  ): Promise<SafeCompletionResult> {
    // 1. Validate input
    const lastUserMessage = messages.findLast((m) => m.role === "user");
    if (lastUserMessage) {
      const inputCheck = await validateInput(lastUserMessage.content);
      if (!inputCheck.allowed) {
        return {
          content: "I can't help with that request.",
          filtered: true,
          inputBlocked: true,
          outputFiltered: false,
        };
      }
    }
  
    // 2. Generate response
    const response = await openai.chat.completions.create({
      model: "gpt-4o",
      messages,
    });
  
    const rawOutput = response.choices[0].message.content ?? "";
  
    // 3. Filter output
    const outputCheck = await moderateOutput(rawOutput);
    if (outputCheck.flagged) {
      if (options?.strictOutput) {
        return {
          content: "I generated a response that didn't meet safety guidelines.",
          filtered: true,
          inputBlocked: false,
          outputFiltered: true,
        };
      }
  
      // Attempt to sanitize
      return {
        content: outputCheck.sanitized ?? rawOutput,
        filtered: true,
        inputBlocked: false,
        outputFiltered: true,
      };
    }
  
    return {
      content: rawOutput,
      filtered: false,
      inputBlocked: false,
      outputFiltered: false,
    };
  }
  ```
  

## Rate Limit Bypass

### **Id**
rate-limit-bypass
### **Summary**
Attackers bypass safety via high-volume requests
### **Severity**
medium
### **Situation**
Safety checks without rate limiting
### **Why**
  Attackers can:
  - Probe for bypass patterns with many attempts
  - Overwhelm moderation API quotas
  - Find edge cases through fuzzing
  - Exhaust your safety budget
  
  Safety without rate limiting is incomplete.
  
### **Detection Pattern**
  validateInput|moderation(?!.*rateLimit|throttle)
  
### **Solution**
  Rate limit by user and implement escalating blocks:
  
  ```typescript
  import { Ratelimit } from "@upstash/ratelimit";
  import { Redis } from "@upstash/redis";
  
  const redis = new Redis({
    url: process.env.UPSTASH_REDIS_URL!,
    token: process.env.UPSTASH_REDIS_TOKEN!,
  });
  
  const ratelimit = new Ratelimit({
    redis,
    limiter: Ratelimit.slidingWindow(10, "1m"),
    analytics: true,
  });
  
  // Track safety violations
  async function checkSafetyWithRateLimit(
    userId: string,
    input: string
  ): Promise<{ allowed: boolean; reason?: string }> {
    // Check rate limit
    const { success, remaining } = await ratelimit.limit(userId);
    if (!success) {
      return { allowed: false, reason: "rate_limited" };
    }
  
    // Check violation history
    const violations = await redis.get<number>(`violations:${userId}`) ?? 0;
    if (violations >= 5) {
      return { allowed: false, reason: "too_many_violations" };
    }
  
    // Perform safety check
    const safetyResult = await validateInput(input);
  
    if (!safetyResult.allowed) {
      // Increment violations
      await redis.incr(`violations:${userId}`);
      await redis.expire(`violations:${userId}`, 86400); // 24h
  
      // Escalating response
      if (violations >= 3) {
        // Notify admin for review
        await notifyAdmin(userId, input, safetyResult);
      }
    }
  
    return safetyResult;
  }
  ```
  

## Context Window Injection

### **Id**
context-window-injection
### **Summary**
Injection via long context overwhelms safety
### **Severity**
high
### **Situation**
RAG or long-context applications
### **Why**
  Long contexts can hide attacks:
  - Instructions buried in retrieved documents
  - "Lost in the middle" - model ignores safety in long contexts
  - Context poisoning via vector DB
  - Injection in structured data (JSON, XML)
  
  Safety checks on truncated input miss full attack.
  
### **Detection Pattern**
  retrieve.*context(?!.*sanitize|validate)
  
### **Solution**
  Validate retrieved context before injection:
  
  ```typescript
  interface RetrievedChunk {
    content: string;
    source: string;
    score: number;
  }
  
  async function safeRAGContext(
    chunks: RetrievedChunk[],
    options?: { maxTokens?: number }
  ): Promise<RetrievedChunk[]> {
    const validatedChunks: RetrievedChunk[] = [];
  
    for (const chunk of chunks) {
      // Check for injection patterns in retrieved content
      const injectionCheck = await detectInjection(chunk.content, { useLLM: false });
      if (injectionCheck.blocked) {
        console.warn(`Blocked suspicious chunk from ${chunk.source}`);
        continue;
      }
  
      // Check for prompt-like instructions
      if (containsInstructions(chunk.content)) {
        console.warn(`Chunk contains instructions: ${chunk.source}`);
        // Wrap in quotes to de-emphasize
        chunk.content = `Retrieved content: "${chunk.content}"`;
      }
  
      validatedChunks.push(chunk);
    }
  
    return validatedChunks;
  }
  
  function containsInstructions(text: string): boolean {
    const instructionPatterns = [
      /\b(you must|you should|always|never|ignore|forget)\b/i,
      /\b(instructions?|commands?|directives?)\s*:/i,
      /\bsystem\s*prompt/i,
    ];
  
    return instructionPatterns.some((p) => p.test(text));
  }
  ```
  

## Guardrails Latency

### **Id**
guardrails-latency
### **Summary**
Safety checks add significant latency
### **Severity**
medium
### **Situation**
Multiple safety layers in production
### **Why**
  Each safety layer adds latency:
  - OpenAI Moderation: 50-200ms
  - LLM-based detection: 500-2000ms
  - PII detection: 100-500ms
  
  Stacking layers can add 1-3 seconds to every request.
  
### **Detection Pattern**
  await.*moderation.*await.*detect.*await(?!.*parallel|Promise\.all)
  
### **Solution**
  Run safety checks in parallel, cache results:
  
  ```typescript
  interface SafetyCheckResult {
    safe: boolean;
    latencyMs: number;
    checks: Record<string, boolean>;
  }
  
  async function parallelSafetyCheck(
    input: string,
    userId: string
  ): Promise<SafetyCheckResult> {
    const start = Date.now();
  
    // Check cache first
    const cacheKey = `safety:${hashInput(input)}`;
    const cached = await redis.get<SafetyCheckResult>(cacheKey);
    if (cached) {
      return { ...cached, latencyMs: Date.now() - start };
    }
  
    // Run all checks in parallel
    const [moderation, injection, pii] = await Promise.all([
      openai.moderations.create({ input }).catch(() => ({ results: [{ flagged: false }] })),
      detectInjection(input, { useLLM: false }), // Fast pattern-only
      detectPII(input),
    ]);
  
    const checks = {
      moderation: !moderation.results[0].flagged,
      injection: !injection.blocked,
      pii: !pii.found,
    };
  
    const safe = Object.values(checks).every(Boolean);
  
    const result: SafetyCheckResult = {
      safe,
      latencyMs: Date.now() - start,
      checks,
    };
  
    // Cache for 5 minutes
    await redis.setex(cacheKey, 300, result);
  
    return result;
  }
  ```
  

## Multilingual Safety Gap

### **Id**
multilingual-safety-gap
### **Summary**
Non-English content bypasses safety
### **Severity**
high
### **Situation**
Moderation API with non-English users
### **Why**
  Most safety tools are English-centric:
  - OpenAI Moderation: Best in English, weaker in other languages
  - Pattern matching: Only covers one language
  - PII patterns: Format varies by country
  
  Attackers use non-English to bypass filters.
  
### **Detection Pattern**
  moderation|validateInput(?!.*language|translate|multilingual)
  
### **Solution**
  Detect language and apply appropriate safety:
  
  ```typescript
  import { franc } from "franc";
  
  async function multilingualSafetyCheck(
    input: string
  ): Promise<{ safe: boolean; language: string; method: string }> {
    // Detect language
    const language = franc(input);
  
    // English: Use full safety stack
    if (language === "eng") {
      const result = await fullSafetyCheck(input);
      return { ...result, language: "en", method: "full" };
    }
  
    // Supported languages: Translate then check
    const supportedLanguages = ["spa", "fra", "deu", "por", "ita"];
    if (supportedLanguages.includes(language)) {
      const translated = await translateToEnglish(input);
      const result = await fullSafetyCheck(translated);
      return { ...result, language, method: "translated" };
    }
  
    // Unsupported: Use stricter threshold + basic moderation
    const moderation = await openai.moderations.create({ input });
    const flagged = moderation.results[0];
  
    // Lower threshold for unsupported languages
    const scores = Object.values(flagged.category_scores);
    const maxScore = Math.max(...scores);
  
    return {
      safe: maxScore < 0.3, // Stricter than default 0.5
      language,
      method: "strict-threshold",
    };
  }
  ```
  