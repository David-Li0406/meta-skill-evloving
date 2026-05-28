# Optimization Patterns

Improve LLM application accuracy, speed, and cost through systematic optimization.

## Prompt Optimization

### Clear Instructions

```
Bad:
  "Classify this email"

Good:
  "Classify the following customer support email into exactly
   one category: technical, billing, or general.

   Consider:
   - Technical: login issues, bugs, feature questions
   - Billing: payments, subscriptions, refunds
   - General: everything else

   Return only the category name."
```

### Output Format Specification

```
Bad:
  "Analyze this text and give me the sentiment"

Good:
  "Analyze the sentiment of the following text.

   Return a JSON object with:
   - sentiment: 'positive', 'negative', or 'neutral'
   - confidence: number from 0.0 to 1.0
   - key_phrases: list of phrases that influenced the decision

   Example output:
   {
     'sentiment': 'positive',
     'confidence': 0.85,
     'key_phrases': ['great service', 'highly recommend']
   }"
```

### Few-Shot Examples

```
Prompt:
  "Classify customer emails. Examples:

   Email: 'I can't log in to my account'
   Category: technical

   Email: 'When will I be charged?'
   Category: billing

   Email: 'Thanks for the help!'
   Category: general

   Now classify:
   Email: '{user_email}'
   Category:"
```

## Structured Output Optimization

### Use Type Constraints

```
Instead of:
  "Return the category as a string"

Use:
  Output:
    category: Enum["technical", "billing", "general"]
```

### Reduce Output Tokens

```
Instead of:
  "Explain your reasoning in detail, then provide the answer"

Use:
  "Provide only the classification. No explanation needed."

# When you DO need reasoning:
  Output:
    reasoning: String (max 100 chars)
    answer: String
```

## Context Optimization

### Relevance Filtering

```
Bad:
  # Stuffing entire document into context
  context = full_document  # 50,000 tokens

Good:
  # Extract relevant sections first
  relevant_sections = search(document, query)  # 2,000 tokens
  context = relevant_sections
```

### Context Compression

```
For long contexts:
  1. Summarize older messages in conversation
  2. Keep recent messages verbatim
  3. Extract key facts from documents

Context structure:
  [Summary of conversation history]
  [Key facts from documents]
  [Recent 5 messages verbatim]
  [Current query]
```

## Chain of Thought Optimization

### When to Use CoT

Use Chain of Thought for:
- Math problems
- Multi-step reasoning
- Complex analysis
- Decisions requiring justification

Skip CoT for:
- Simple classification
- Entity extraction
- Formatting tasks

### Efficient CoT

```
Bad:
  "Think step by step about every aspect of this problem..."
  # Produces verbose, expensive output

Good:
  "Briefly note key considerations, then answer.
   Keep reasoning under 50 words."
```

## Few-Shot Learning

### Example Selection

```
Dynamic few-shot:
  1. Embed the input query
  2. Find most similar examples from training set
  3. Include top 3-5 as few-shot examples

# More relevant examples = better performance
```

### Example Ordering

```
Research shows:
  - Put most similar example last (recency bias)
  - Include diverse examples (cover edge cases)
  - 3-5 examples usually sufficient
  - More examples = more tokens = higher cost
```

## Model Selection Optimization

### Task-Model Matching

```
Simple tasks (classification, extraction):
  → gpt-4o-mini, claude-3-haiku, gemini-flash
  → Fast, cheap, sufficient quality

Complex tasks (reasoning, analysis):
  → gpt-4o, claude-3-5-sonnet, gemini-pro
  → Better quality worth the cost

Code tasks:
  → claude-3-5-sonnet (strong at code)
  → gpt-4o (good alternative)
```

### Dynamic Model Selection

```
Router:
  estimate_complexity(input)

  if complexity == "simple":
    use: cheap_fast_model
  elif complexity == "medium":
    use: balanced_model
  else:
    use: best_model
```

## Caching Strategies

### Response Caching

```
Cache:
  key: hash(prompt + inputs)
  value: llm_response
  ttl: 1 hour (or based on use case)

Lookup:
  if cache.has(key):
    return cache.get(key)  # Free, instant
  else:
    response = llm.predict(...)
    cache.set(key, response)
    return response
```

### Semantic Caching

```
# For similar (not identical) queries
Semantic Cache:
  1. Embed the query
  2. Search for similar cached queries
  3. If similarity > threshold:
     return cached response
  4. Else:
     call LLM, cache result
```

## Batching

### Request Batching

```
Instead of:
  for item in items:
    result = llm.predict(item)  # N API calls

Use:
  results = llm.batch_predict(items)  # 1 API call
  # Lower latency, sometimes lower cost
```

### Prompt Batching

```
Instead of:
  prompt1 = "Classify: email1"
  prompt2 = "Classify: email2"
  # 2 separate calls

Use:
  prompt = """
  Classify each email:

  1. {email1}
  2. {email2}

  Return classifications as JSON array.
  """
  # 1 call, process multiple items
```

## Latency Optimization

### Streaming

```
For user-facing applications:
  Use streaming responses
  - Show output as it generates
  - Better perceived performance
  - Same total time, better UX
```

### Parallel Requests

```
When possible:
  # Instead of sequential
  result1 = llm.predict(input1)
  result2 = llm.predict(input2)

  # Run in parallel
  results = parallel([
    llm.predict(input1),
    llm.predict(input2)
  ])
```

### Precomputation

```
For predictable queries:
  # Precompute during off-peak hours
  common_queries = get_common_queries()
  for query in common_queries:
    cache.set(query, llm.predict(query))
```

## Evaluation and Iteration

### Metrics to Track

```
Quality:
  - Accuracy on golden set
  - User satisfaction ratings
  - Error rate

Cost:
  - Tokens per request (input/output)
  - Cost per request
  - Daily/monthly spend

Performance:
  - Latency (p50, p95, p99)
  - Throughput (requests/sec)
```

### A/B Testing

```
Experiment:
  control: current_prompt
  treatment: new_prompt

  Split traffic 50/50
  Measure:
    - Accuracy
    - Latency
    - Cost
    - User engagement

  Statistical significance before deciding
```

### Continuous Improvement

```
Optimization Loop:
  1. Measure current performance
  2. Identify bottleneck (accuracy, cost, latency)
  3. Form hypothesis
  4. Test change
  5. Measure improvement
  6. Deploy if better
  7. Repeat
```

## Fine-Tuning Considerations

### When to Fine-Tune

Consider fine-tuning when:
- Have 1000+ high-quality examples
- Need consistent style/format
- Cost of prompting is high
- Latency is critical

Don't fine-tune when:
- Task changes frequently
- Have few examples
- Prompt engineering works well enough

### Fine-Tuning Process

```
1. Collect training data
   - Input/output pairs
   - High quality, diverse
   - 1000+ examples

2. Format for provider
   - OpenAI: JSONL format
   - Anthropic: Constitutional AI
   - Open source: Various formats

3. Train model
   - Upload data
   - Start training job
   - Monitor metrics

4. Evaluate
   - Test on held-out set
   - Compare to base model
   - Check for regressions

5. Deploy
   - Replace model in config
   - Monitor production metrics
```
