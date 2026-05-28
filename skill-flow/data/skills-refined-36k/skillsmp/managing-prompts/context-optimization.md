# Context Optimization

Strategies for token efficiency, prompt caching, document organization, and splitting decisions.

## Token Management

### Token Counting

**Estimation rule of thumb:**
- English: ~4 characters per token (including spaces)
- Code: ~3-3.5 characters per token (varies by language)
- JSON/XML: ~3.5-4 characters per token

**Precise counting:**
Use Claude API token counter or tokenizer libraries.

```python
import anthropic

client = anthropic.Anthropic(api_key="...")

# Count tokens for message content
token_count = client.messages.count_tokens(
    model="claude-sonnet-4-5-20250929",
    messages=[
        {"role": "user", "content": "Your prompt content here"}
    ]
)

print(f"Tokens: {token_count}")
```

### Context Window Limits

**Current limits:**
- Standard models: 200,000 tokens (input + output)
- Claude Sonnet 4/4.5: Up to 1,000,000 tokens (beta, tier 4+)
- Pricing premium: 2x input, 1.5x output for requests >200K tokens

**Planning considerations:**
- Leave buffer for output (estimate max completion tokens needed)
- Account for conversation history accumulation
- Monitor remaining capacity in multi-turn interactions

**Claude 4.5 context awareness:**
- Model knows its remaining token budget
- Explicitly informed of context window size
- Can plan accordingly for extended tasks
- No silent truncation - validation errors if exceeded

## Prompt Caching

### When to Use Caching

**Cost-benefit analysis:**

Cache when:
- Static content ≥1024 tokens (≥4096 for Haiku 4.5)
- Content reused across multiple requests
- Cache hit savings > cache write overhead

**Example scenarios:**
- Large system prompts with examples (5K+ tokens)
- Documentation or knowledge bases (10K-100K+ tokens)
- Tool definitions for agents (2K-10K tokens)
- Conversation history in multi-turn chats

**Pricing (Claude Sonnet 4.5):**
- Cache writes: $3.75 per 1M tokens (1.25x base rate of $3)
- Cache reads: $0.30 per 1M tokens (0.1x base rate)
- Regular input: $3 per 1M tokens

**Break-even calculation:**
- Cache write cost = 1.25x regular
- Cache read cost = 0.1x regular
- Savings per read = 0.9x regular
- Break-even after 2 cache hits (1.25 / 0.9 ≈ 1.4 reads)

### Cache Structure

**Placement rules:**
1. Cacheable content must be at beginning of prompt
2. Order: tools → system → messages
3. Mark end of cacheable section with `cache_control` parameter
4. System automatically finds longest matching cached prefix

**Basic example:**
```python
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    system=[
        {
            "type": "text",
            "text": "Large system prompt with examples and guidelines...",
            "cache_control": {"type": "ephemeral"}
        }
    ],
    messages=[
        {"role": "user", "content": "User query"}
    ]
)
```

**Multi-section caching:**
```python
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    system=[
        {
            "type": "text",
            "text": "Core instructions (rarely change)...",
            "cache_control": {"type": "ephemeral"}
        },
        {
            "type": "text",
            "text": "Domain knowledge base (occasionally updates)...",
            "cache_control": {"type": "ephemeral"}
        }
    ],
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Recent conversation history...",
                    "cache_control": {"type": "ephemeral"}
                },
                {
                    "type": "text",
                    "text": "Current user query"
                }
            ]
        }
    ]
)
```

**Maximum: 4 cache control breakpoints per request**

### Cache Minimum Thresholds

**Cacheability requirements (minimum tokens to cache):**

| Model | Minimum Tokens | Notes |
|-------|----------------|-------|
| Claude Opus 4.5 | 4,096 tokens | Higher threshold |
| Claude Sonnet 4.5 | 1,024 tokens | Standard |
| Claude Haiku 4.5 | 4,096 tokens | Higher threshold |
| Claude Haiku 3.5 | 2,048 tokens | Mid-range |
| Claude Opus 4.1 | 1,024 tokens | Standard |

**Key point:** Requests below minimum aren't cached, even if marked with `cache_control`. Always check response `cache_creation_input_tokens` to confirm caching occurred.

### Cache Lifetime Options

**Default: 5-minute TTL (ephemeral, auto-refresh)**
- Lifetime: 5 minutes from creation or last use
- Refreshes automatically when cache hit occurs (no additional cost)
- Good for: Regular cadence usage (prompts used more frequently than every 5 minutes)
- Cost multipliers: 1.25x write, 0.1x read

**Extended: 1-hour TTL (ephemeral, extended lifetime)**
- Lifetime: 1 hour from creation (no auto-refresh on hit)
- Higher write cost but longer persistence
- Best for specific scenarios (see below)
- Cost multipliers: 2x write, 0.1x read

#### Pricing Comparison (Claude Sonnet 4.5)

| Operation | 5-Minute TTL | 1-Hour TTL | Regular Input |
|-----------|-------------|------------|---------------|
| Cache writes | $3.75/MTok (1.25x) | $6/MTok (2x) | $3/MTok (1x) |
| Cache reads | $0.30/MTok (0.1x) | $0.30/MTok (0.1x) | $3/MTok (1x) |
| Break-even | ~2 cache hits | ~3 cache hits | N/A |

**Other models:** Same multipliers apply (1.25x/2x for writes, 0.1x for reads)

#### When to Use 1-Hour TTL

**Use 1-hour cache when:**
- Prompts used less frequently than every 5 minutes but more than hourly
- Agentic side-agents taking longer than 5 minutes to complete
- Long chat conversations with delayed user responses (user may not reply within 5 minutes)
- Latency-critical applications where performance matters beyond 5-minute window
- Rate limit optimization (cache hits don't count against rate limits)

**Use 5-minute cache when:**
- Regular cadence usage (interactive sessions, continuous API calls)
- Prompts used more frequently than every 5 minutes (auto-refresh is free)
- Short-lived sessions (under 5 minutes total)
- Cost optimization (lower write cost, frequent hits)

**Avoid caching when:**
- Prompts used more than 1 hour apart (cache expired, recreate each time)
- Content changes frequently (cache invalidation overhead)
- Content below minimum threshold (1024-4096 tokens depending on model)

#### Implementation with TTL Parameter

**5-minute cache (default):**
```python
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    system=[
        {
            "type": "text",
            "text": "Large system prompt...",
            "cache_control": {"type": "ephemeral", "ttl": "5m"}
        }
    ],
    messages=[{"role": "user", "content": "Query"}]
)
```

**1-hour cache:**
```python
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    system=[
        {
            "type": "text",
            "text": "Large system prompt for long-running agent...",
            "cache_control": {"type": "ephemeral", "ttl": "1h"}
        }
    ],
    messages=[{"role": "user", "content": "Query"}]
)
```

**Note:** If `ttl` is omitted, defaults to `"5m"`

#### Mixing TTLs in Single Request

You can use both 1-hour and 5-minute caches in the same request, with a constraint:

**Rule: 1-hour cache entries must appear BEFORE 5-minute entries**

**Valid example:**
```python
system=[
    {
        "type": "text",
        "text": "Rarely changing knowledge base...",
        "cache_control": {"type": "ephemeral", "ttl": "1h"}  # First
    },
    {
        "type": "text",
        "text": "Frequently updated context...",
        "cache_control": {"type": "ephemeral", "ttl": "5m"}  # Second
    }
]
```

**Invalid example (will fail):**
```python
system=[
    {
        "type": "text",
        "text": "...",
        "cache_control": {"type": "ephemeral", "ttl": "5m"}  # Cannot be before 1h
    },
    {
        "type": "text",
        "text": "...",
        "cache_control": {"type": "ephemeral", "ttl": "1h"}  # Error: must come first
    }
]
```

#### TTL Mixing Billing

When mixing TTLs, billing is calculated at three positions:

**Position A:** Highest cache hit (tokens read from cache)
**Position B:** Highest 1-hour `cache_control` block after A
**Position C:** Last `cache_control` block (any TTL)

**Charges:**
- Cache read tokens: A
- 1-hour cache write tokens: (B - A)
- 5-minute cache write tokens: (C - B)

**Example response with mixed TTLs:**
```python
{
    "usage": {
        "input_tokens": 50,
        "cache_read_input_tokens": 10000,
        "cache_creation_input_tokens": 5000,
        "output_tokens": 200,
        "cache_creation": {
            "ephemeral_1h_input_tokens": 3000,
            "ephemeral_5m_input_tokens": 2000
        }
    }
}
```

**Cost calculation (Sonnet 4.5):**
- Cache reads: 10,000 tokens × $0.30/MTok = $0.003
- 1h cache writes: 3,000 tokens × $6/MTok = $0.018
- 5m cache writes: 2,000 tokens × $3.75/MTok = $0.0075
- Regular input: 50 tokens × $3/MTok = $0.00015
- **Total input cost:** $0.02865

#### Cache Lifetime and Invalidation

**Cache invalidation:**
- Content hash changes → new cache created
- Lifetime expires (5m or 1h) → automatic cleanup
- Manual invalidation not supported (change content to force new cache)

**Refresh behavior:**
- **5-minute TTL:** Refreshed on each cache hit (extends lifetime by 5 minutes, no cost)
- **1-hour TTL:** Not refreshed on hit (fixed 1-hour lifetime from creation)

**Latency:**
- Both 5m and 1h TTLs have same latency characteristics
- Improved time-to-first-token for long documents (both TTLs)

#### Decision Flow for TTL Selection

```
How frequently is this prompt used?
├─ More than every 5 minutes
│  └─ Use 5-minute TTL (auto-refresh free)
│
├─ Between 5 minutes and 1 hour
│  └─ Is rate limit optimization important?
│     ├─ YES → Use 1-hour TTL (cache hits don't count against limits)
│     └─ NO → Compare costs:
│              1h write cost vs multiple 5m writes + recreations
│
└─ More than 1 hour apart
   └─ Use 5-minute TTL (cache will expire anyway, lower write cost)
```

### Optimizing Cache Hits

**Strategy 1: Position editable content last**

Bad - cache broken by minor changes:
```python
system = [
    {"type": "text", "text": f"Today is {date}"},  # Changes daily
    {"type": "text", "text": large_knowledge_base},  # Static
    {"type": "text", "text": "Guidelines...", "cache_control": {"type": "ephemeral"}}
]
```

Good - static content cached despite date changes:
```python
system = [
    {"type": "text", "text": large_knowledge_base},  # Static, cached
    {"type": "text", "text": "Guidelines...", "cache_control": {"type": "ephemeral"}},
    {"type": "text", "text": f"Today is {date}"}  # Changes daily, not cached
]
```

**Strategy 2: Intermediate breakpoints for long prompts**

If >20 content blocks before cache point, earlier content not cacheable. Add intermediate breakpoints:

```python
system = [
    {"type": "text", "text": "Block 1"},
    {"type": "text", "text": "Block 2"},
    # ... 18 more blocks ...
    {"type": "text", "text": "Block 20", "cache_control": {"type": "ephemeral"}},
    {"type": "text", "text": "Block 21"},
    # ... more blocks ...
    {"type": "text", "text": "Block 40", "cache_control": {"type": "ephemeral"}},
]
```

**Strategy 3: Normalize content for consistent hashing**

Ensure identical content has identical hash:
- Consistent whitespace formatting
- Stable ordering (don't randomize examples)
- Deterministic template rendering
- No timestamps or random elements in cached sections

### Cache Invalidation Patterns

**What invalidates cache at each level:**

| Change Type | Tools Cache | System Cache | Messages Cache | Impact |
|-------------|------------|-------------|----------------|--------|
| Tool definitions | ✘ | ✘ | ✘ | Entire cache invalidated |
| Web search toggle | ✓ | ✘ | ✘ | System + messages re-cached |
| Citations toggle | ✓ | ✘ | ✘ | System + messages re-cached |
| Tool choice param | ✓ | ✓ | ✘ | Only messages level affected |
| Image addition/removal | ✓ | ✓ | ✘ | Messages level affected |
| Thinking settings | ✓ | ✓ | ✘ | Messages level affected |
| Non-tool results + thinking | ✓ | ✓ | ✘ | Previous thinking blocks stripped |

**Strategy:** Place editable content (date, context updates) AFTER cache breakpoint to preserve cache on other changes.

### Measuring Cache Performance

**Check response headers:**
```python
response = client.messages.create(...)

usage = response.usage
print(f"Input tokens: {usage.input_tokens}")
print(f"Cache creation tokens: {usage.cache_creation_input_tokens}")
print(f"Cache read tokens: {usage.cache_read_input_tokens}")

# Calculate total
total = usage.input_tokens + usage.cache_creation_input_tokens + usage.cache_read_input_tokens
print(f"Total input tokens: {total}")
```

**Calculate cache effectiveness:**
```python
cache_hit_rate = usage.cache_read_input_tokens / (
    usage.cache_read_input_tokens + usage.cache_creation_input_tokens
)
print(f"Cache hit rate: {cache_hit_rate:.1%}")
```

**Optimization targets:**
- High cache read ratio (>80% of input from cache on subsequent requests)
- Minimal cache creation overhead (<200 tokens per request type)
- 2+ requests per cache (break-even), ideally 5+ for ROI
- Cache hits on >70% of requests in session

**Performance fields in response:**
- `cache_creation_input_tokens`: Tokens written to cache (1.25x-2x cost)
- `cache_read_input_tokens`: Tokens from cache (0.1x cost)
- `input_tokens`: Tokens after cache breakpoint (full cost)
- For 1h cache: Split into `ephemeral_5m_input_tokens` and `ephemeral_1h_input_tokens`

## Document Organization

### Long Document Placement

**Key principle: Place 20K+ token documents near beginning**

Research shows 30% quality improvement for complex multi-document tasks.

**Optimal structure:**
```xml
<documents>
  <document index="1">
    <source>large_report.pdf</source>
    <document_content>
      [20K+ tokens of content]
    </document_content>
  </document>

  <document index="2">
    <source>specifications.txt</source>
    <document_content>
      [Another large document]
    </document_content>
  </document>
</documents>

<instructions>
Analyze the documents above and answer the following question:
{{QUESTION}}
</instructions>
```

**Rationale:**
- Claude's attention mechanisms favor earlier content
- Long documents early = better context for subsequent processing
- Instructions referencing documents work better when documents precede them

### Document Structuring

**XML metadata structure:**
```xml
<documents>
  <document index="1">
    <source>Q4_2024_Financial_Report.pdf</source>
    <doc_type>financial_report</doc_type>
    <date>2024-12-31</date>
    <page_count>87</page_count>
    <document_content>
      [Actual content]
    </document_content>
  </document>

  <document index="2">
    <source>Q3_2024_Financial_Report.pdf</source>
    <doc_type>financial_report</doc_type>
    <date>2024-09-30</date>
    <page_count>82</page_count>
    <document_content>
      [Actual content]
    </document_content>
  </document>
</documents>
```

**Benefits:**
- Clear boundaries between documents
- Metadata enables selective processing
- Hierarchical structure improves parsing
- Easy citation format: [Document 1, p.23]

### Quote-Grounding for Noise Filtering

**Problem:** Large documents (50K+ tokens) contain much irrelevant information.

**Solution:** Two-phase approach extracts relevant sections first.

**Phase 1: Quote extraction**
```xml
<instructions>
Read the research papers below and extract quotes relevant to: {{RESEARCH_QUESTION}}

For each relevant finding:
<quote>
  <text>"[Exact quote from source]"</text>
  <source>Document {{N}}, page {{P}}</source>
  <relevance>Brief note on why this quote matters</relevance>
</quote>

Focus on extracting 10-20 highly relevant quotes rather than including everything. This filters the 50K+ token corpus down to the essential information.
</instructions>

<documents>
  {{LARGE_DOCUMENT_CORPUS}}
</documents>
```

**Phase 2: Analysis based on quotes**
```xml
<instructions>
Using only the quotes extracted above, synthesize an answer to: {{RESEARCH_QUESTION}}

Ground each claim in your synthesis with reference to specific quote numbers.
</instructions>
```

**Benefits:**
- Reduces effective context from 50K+ to 2-5K tokens
- Improves accuracy by focusing on relevant content
- Enables better reasoning on filtered information
- Claude explicitly identifies what matters

## Context Reduction Strategies

### Strategy 1: Remove Redundant Information

**Identify and eliminate:**
- Information Claude already knows (standard libraries, common patterns)
- Repeated explanations across sections
- Verbose examples when concise ones suffice
- Background that doesn't inform the task

**Example - Before (verbose):**
```
Python is a popular programming language known for its readability and extensive
standard library. When working with files in Python, you can use the built-in
'open' function which is part of Python's standard library. The open function
returns a file object that has methods for reading and writing.

Your task is to write a Python script that reads a CSV file and processes each row.
The CSV (Comma-Separated Values) format is a common way to store tabular data.
You should use Python's csv module, which is part of the standard library and
provides functionality for reading and writing CSV files.

Here's what you need to do:
1. Import the csv module
2. Open the file
3. Create a CSV reader
4. Process each row
5. Close the file when done

[Additional verbose instructions...]
```

**Example - After (concise):**
```
Write a Python script to process CSV file: {{FILENAME}}

Requirements:
- Read each row
- Extract columns: {{COLUMNS}}
- Filter rows where {{CONDITION}}
- Output results to {{OUTPUT_FORMAT}}

Handle errors: missing file, malformed CSV, empty data.
```

Token reduction: ~250 tokens → ~50 tokens (80% reduction)

### Strategy 2: Template Variables for Repetition

**Pattern: Multiple similar prompts with different inputs**

Before - separate full prompts:
```
Prompt 1: [500 tokens of instructions] + Input A
Prompt 2: [500 tokens of identical instructions] + Input B
Prompt 3: [500 tokens of identical instructions] + Input C
Total: 1500 tokens
```

After - template with variables:
```
Template: [500 tokens of instructions] + {{INPUT}}
Instance 1: Load template + Input A
Instance 2: Load template + Input B (from cache!)
Instance 3: Load template + Input C (from cache!)
Total: 500 tokens + cache overhead
```

**Implementation:**
```xml
<instructions cache_control="ephemeral">
[Reusable instructions with {{VARIABLES}}]
</instructions>

<current_input>
{{VARIABLE_VALUES}}
</current_input>
```

### Strategy 3: Progressive Disclosure in Prompts

**Problem:** Single 2000-line prompt with rarely-needed details

**Solution:** Split into core + referenced sections

**Core prompt (500 tokens):**
```xml
<instructions>
You are a code reviewer. For each submission:

1. Check code quality (load quality-criteria.md if needed)
2. Verify security (load security-checklist.md if needed)
3. Assess performance (load performance-guidelines.md if needed)
4. Review tests (load testing-standards.md if needed)

Provide concise feedback with severity levels: critical, major, minor.
</instructions>
```

**Referenced files (only loaded when needed):**
- quality-criteria.md (300 tokens)
- security-checklist.md (400 tokens)
- performance-guidelines.md (350 tokens)
- testing-standards.md (250 tokens)

**Benefit:** Core prompt always loaded (500 tokens), details loaded on-demand (300-400 tokens each) rather than all details always (2000 tokens).

### Strategy 4: Summarization Chains

**Use case:** Need to process 200K tokens of source material but only need summary insights.

**Approach: Chain summarization prompts**

**Prompt 1: Initial summarization**
```xml
<instructions>
Summarize each document into 500-word structured summary capturing:
- Main topics
- Key findings
- Important data points
- Conclusions
</instructions>

<documents>
{{DOCUMENTS_1_TO_50}}  // 200K tokens
</documents>
```
Output: 5K tokens

**Prompt 2: Synthesis from summaries**
```xml
<instructions>
Using the document summaries below, synthesize answer to: {{QUESTION}}
</instructions>

<summaries>
{{SUMMARIES_FROM_PROMPT_1}}  // 5K tokens
</summaries>
```

**Token savings:** 200K → 5K for synthesis (97.5% reduction)

**Tradeoff:** Two prompts vs one, potential information loss in summarization

**When to use:** Information need < detail level in sources

## Prompt Splitting Strategies

### When to Split Prompts

**Split into chained prompts when:**
- Task has 3+ distinct subtasks with different objectives
- Each subtask needs full attention without distraction
- Debugging requires isolating steps
- Intermediate outputs need validation
- Total complexity would produce 1000+ token instructions

**Examples:**
- Legal contract review: extract terms → analyze risks → recommend changes
- Content pipeline: research → outline → draft → edit → format
- Data pipeline: extract → transform → analyze → visualize

**Keep as single prompt when:**
- Subtasks are tightly coupled
- Context loss between prompts would hurt quality
- Task is simple despite multiple steps
- Total instructions <500 tokens

### Chaining Pattern

**Prompt 1: Extraction**
```xml
<objective>
Extract key terms from the contract for analysis.
</objective>

<instructions>
Read the contract and extract:

<extracted_terms>
  <term category="payment">
    <description>[Term description]</description>
    <location>[Section, page]</location>
  </term>
  [Repeat for each term]
</extracted_terms>

Categories: payment, termination, liability, intellectual_property, confidentiality
</instructions>

<contract>
{{CONTRACT}}
</contract>
```

**Prompt 2: Analysis (using output from Prompt 1)**
```xml
<objective>
Analyze extracted contract terms for risks.
</objective>

<instructions>
For each term below, assess:
- Risk level: low, medium, high, critical
- Rationale: why this risk level
- Recommendation: accept, negotiate, reject

<risk_analysis>
  <term_analysis>
    <term_reference>[From extraction]</term_reference>
    <risk_level>[Level]</risk_level>
    <rationale>[Why]</rationale>
    <recommendation>[Action]</recommendation>
  </term_analysis>
</risk_analysis>
</instructions>

<extracted_terms>
{{OUTPUT_FROM_PROMPT_1}}
</extracted_terms>
```

**Benefits:**
- Each prompt focused on single objective
- Clear handoff via XML structure
- Easy to debug (isolate which step has issues)
- Can update one step without affecting others

### Parallel Splitting

**Use case:** Independent analyses that can run simultaneously

**Example: Multi-document comparison**

Run these in parallel:
```python
# Prompt A: Analyze Document 1
response_a = analyze_document(doc1)

# Prompt B: Analyze Document 2
response_b = analyze_document(doc2)

# Prompt C: Analyze Document 3
response_c = analyze_document(doc3)

# Prompt D: Synthesize all analyses
synthesis = synthesize(response_a, response_b, response_c)
```

**Benefits:**
- Faster (parallel execution)
- Each document gets full attention
- Avoids context overload from 3 large documents simultaneously

## Information Density Optimization

### Compression Techniques

**Technique 1: Bullet points over prose**

Before:
```
The system should validate user input to ensure data quality. This means checking
that all required fields are present and that the data types are correct. For
example, email addresses should match the email format pattern, and dates should
be valid calendar dates. Additionally, the system should check for SQL injection
attempts and cross-site scripting patterns to prevent security vulnerabilities.
```

After:
```
Input validation requirements:
- Required fields presence check
- Data type verification (email format, valid dates)
- Security scanning (SQL injection, XSS patterns)
```

Token reduction: ~70 tokens → ~25 tokens

**Technique 2: Tables over text**

Before:
```
For API endpoint /users, use GET method to retrieve users, POST to create users,
PUT to update users, and DELETE to remove users. For /products, GET retrieves
products, POST creates products, PUT updates products, and DELETE removes products.
```

After:
```
| Endpoint  | GET      | POST   | PUT    | DELETE |
|-----------|----------|--------|--------|--------|
| /users    | Retrieve | Create | Update | Remove |
| /products | Retrieve | Create | Update | Remove |
```

**Technique 3: Code over description**

Before:
```
The function should take two parameters: a list of numbers and a target sum.
It should iterate through the list and find pairs of numbers that add up to
the target sum. For each pair found, it should store them in a results list.
At the end, return the results list containing all pairs.
```

After:
```python
def find_pairs(numbers: list[int], target: int) -> list[tuple]:
    """Find all pairs summing to target."""
    # Implement this
```

### Minimizing Examples

**Principle: Use minimum number of examples to convey pattern**

Over-specified (5 examples for simple pattern):
```xml
<examples>
<example><input>{"name": "John"}</input><output>Hello, John!</output></example>
<example><input>{"name": "Jane"}</input><output>Hello, Jane!</output></example>
<example><input>{"name": "Bob"}</input><output>Hello, Bob!</output></example>
<example><input>{"name": "Alice"}</input><output>Hello, Alice!</output></example>
<example><input>{"name": "Eve"}</input><output>Hello, Eve!</output></example>
</examples>
```

Optimized (1 example + template):
```xml
<example>
<input>{"name": "John"}</input>
<output>Hello, John!</output>
</example>

Pattern: Hello, {name}!
```

**When to use multiple examples:**
- Complex patterns requiring 3-5 examples for coverage
- Edge cases that aren't obvious
- Format variations that need demonstration

**When 1 example sufficient:**
- Simple, obvious patterns
- Format can be specified in text
- Transformations are straightforward

## Optimization Decision Framework

### Decision Tree

```
Token usage analysis:
├─ Total tokens < 50K
│  ├─ No optimization needed
│  └─ Consider caching if reused
│
├─ Total tokens 50K-100K
│  ├─ Remove redundancy
│  ├─ Implement caching for static content
│  └─ Use quote-grounding if large documents
│
├─ Total tokens 100K-200K
│  ├─ All above optimizations
│  ├─ Consider prompt chaining if 3+ distinct subtasks
│  └─ Progressive disclosure for rarely-needed details
│
└─ Total tokens > 200K
   ├─ Required: Split into chained prompts
   ├─ Use summarization chains for large corpora
   ├─ Parallel splitting for independent analyses
   └─ Aggressive information density optimization
```

### Optimization Checklist

For any prompt over 10K tokens, evaluate:

- [ ] Remove information Claude already knows
- [ ] Eliminate redundant explanations
- [ ] Convert prose to bullets/tables/code where possible
- [ ] Minimize examples to essential set
- [ ] Identify static content ≥1024 tokens for caching
- [ ] Check if 20K+ documents should move to beginning
- [ ] Use quote-grounding for large documents
- [ ] Evaluate if prompt splitting appropriate (3+ subtasks)
- [ ] Consider template variables for repeated patterns
- [ ] Move rarely-needed details to referenced files

### Measuring Success

**Metrics to track:**
- Token count before/after optimization
- Cache hit rate (target >80%)
- Response quality (maintain or improve)
- Cost per request (should decrease)
- Latency (may increase with chaining, decrease with caching)

**Example success:**
```
Before optimization:
- Total tokens: 85K
- Cost per request: $0.255
- Response time: 12s

After optimization:
- Total tokens: 25K (70% reduction)
- Cached tokens: 20K (80% cache hit rate)
- Cost per request: $0.021 (92% reduction)
- Response time: 8s (33% improvement)
```

---

## 1M Context Window (Beta)

**Availability:**
- Claude Sonnet 4 and 4.5 only
- Beta feature: Usage tier 4+ and custom rate limit organizations
- Available on: Claude API, Microsoft Foundry, Amazon Bedrock, Google Vertex AI
- Beta header required: `context-1m-2025-08-07`

**Implementation:**
```python
response = client.beta.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Process this large document..."}
    ],
    betas=["context-1m-2025-08-07"]
)
```

**Pricing & Constraints:**
- **Cost:** Requests >200K tokens charged at premium rates (2x input, 1.5x output)
- **Rate limits:** Dedicated rate limits for long-context requests
- **Multimodal:** Large numbers of images/PDFs count toward token limit
- **Validation:** No silent truncation; validation error if exceeding limit

**Use Cases:**
- Process entire codebases (500K+ tokens)
- Analyze comprehensive datasets or research corpora
- Extended multi-turn conversations with full history preservation
- Complex document analysis with all context accessible

**Context Awareness in 1M Window:**
- Claude 4.5/Haiku 4.5 receive remaining context budget information
- Models understand token capacity and can manage work accordingly
- Enables multi-context-window workflows (See: architecture-patterns.md#multi-context-workflows)

---

## Thinking Block Handling with Extended Thinking

**Automatic Stripping Behavior:**

When using extended thinking, thinking blocks are automatically stripped from context calculations:

```
Turn 1:
- Input: User message
- Output: [thinking block] + text response
- Thinking tokens: NOT carried forward

Turn 2:
- Input: Previous messages (thinking stripped)
- Output: [new thinking block] + text response
- Effective context: (input - previous_thinking) + current_turn
```

**With Tool Use:**

```
Turn 1:
- Output: [thinking block] + tool_call
- Thinking is kept in context (MUST be passed back)

Turn 2:
- Input: [thinking block] + tool_result
- Important: Preserve thinking block exactly (cryptographically signed)

Turn 3+ (after tool cycle):
- Previous thinking blocks can be dropped or auto-stripped
- System removes them from context calculation
```

**Implementation Notes:**
- Don't manually strip thinking blocks during tool use (API handles verification)
- Modifying thinking blocks breaks reasoning continuity (API error)
- Thinking tokens billed as output tokens only once (during generation)
- Token calculation: `context = input_tokens + current_turn_tokens`

**Token Efficiency:**
- Thinking blocks allow extensive reasoning without wasting context
- API automatically excludes thinking from subsequent input calculations
- Particularly valuable for multi-turn reasoning tasks
- Combined with caching for significant token savings

---

## Context Awareness (Claude 4.5 & Haiku 4.5)

**How It Works:**

Models receive explicit budget information:

```xml
<budget:token_budget>200000</budget:token_budget>
<!-- Or 500K for Claude.ai Enterprise -->
<!-- Or 1M for beta users -->
```

**Benefits:**
- Claude understands remaining capacity explicitly
- Makes smarter decisions about work allocation
- Enables effective multi-context-window task execution
- Like a cooking show WITH a clock (vs without)

**Usage Pattern:**

```
Start: Receive budget (200K, 500K, or 1M)
After each tool call: Updated remaining capacity notification
Claude uses this to: Plan phases, manage state, wrap up appropriately
```

**Practical Application:**

Without context awareness:
```
Claude must guess how many tokens remain
→ May stop early or attempt too much
→ Inefficient execution
```

With context awareness:
```
Claude knows exact remaining budget
→ Plans accordingly
→ Completes work up to limit
→ Can prepare for next context window
```
