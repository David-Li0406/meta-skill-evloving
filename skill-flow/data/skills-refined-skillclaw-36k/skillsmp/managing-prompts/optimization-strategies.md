# Optimization Strategies

Before/after examples for each optimization type with specific transformations.

## Context Reduction Optimization

### Optimization 1: Removing Claude's Existing Knowledge

**Before (285 tokens):**
```
Python is a high-level, interpreted programming language known for its clear syntax
and readability. It supports multiple programming paradigms including procedural,
object-oriented, and functional programming. Python has a comprehensive standard
library that provides tools for various tasks.

When working with files in Python, the built-in open() function is used. This
function is part of Python's I/O system and returns a file object. File objects
have methods like read(), write(), and close() for interacting with files.

For working with CSV (Comma-Separated Values) files, Python provides the csv module
in its standard library. CSV is a simple file format used to store tabular data.
Each line in a CSV file represents a row, and values within rows are separated by
commas.

Your task: Write a Python script to read a CSV file named 'data.csv', filter rows
where the 'age' column is greater than 30, and write the filtered results to
'output.csv'.
```

**After (45 tokens):**
```
Task: Python script to process 'data.csv'

Requirements:
- Read CSV file
- Filter rows: age > 30
- Write to 'output.csv'
- Handle errors: missing file, invalid data
```

**Reduction:** 285 → 45 tokens (84% reduction)

**What was removed:** Background about Python, file I/O, CSV format - all known to Claude.

---

### Optimization 2: Compressing Verbose Instructions

**Before (320 tokens):**
```
You are tasked with analyzing customer feedback data. This feedback comes from
various sources including email, chat, and surveys. Each piece of feedback contains
text written by customers describing their experience.

For each piece of feedback, you need to perform several analysis steps. First,
you should determine the overall sentiment. Sentiment can be positive, negative,
or neutral. Positive sentiment means the customer is happy or satisfied. Negative
sentiment means they are unhappy or dissatisfied. Neutral sentiment means the
feedback doesn't express strong feelings either way.

Second, you need to identify the main topic or subject that the feedback is about.
Topics might include things like product quality, customer service, shipping and
delivery, pricing, website usability, or other relevant categories.

Third, extract any specific issues or problems mentioned. These are concrete things
that went wrong or could be improved. For example, "website was slow" or "product
arrived damaged" would be specific issues.

Fourth, note any feature requests. These are suggestions from customers about new
features or improvements they'd like to see.

Finally, assign a priority level based on urgency and impact. Use critical for
severe issues affecting many customers, high for important problems, medium for
moderate concerns, and low for minor feedback.
```

**After (85 tokens):**
```
Analyze customer feedback and extract:

1. **Sentiment**: positive | negative | neutral
2. **Topic**: product_quality | support | shipping | pricing | website | other
3. **Issues**: Specific problems mentioned
4. **Feature requests**: Suggested improvements
5. **Priority**: critical | high | medium | low
   - critical: severe, widespread impact
   - high: important problems
   - medium/low: moderate/minor concerns

Output as JSON matching this structure.
```

**Reduction:** 320 → 85 tokens (73% reduction)

**Techniques applied:**
- Numbered list instead of prose
- Enum values instead of descriptions
- Table format for priority definitions
- Removed examples (obvious from context)

---

### Optimization 3: Consolidating Redundant Sections

**Before (510 tokens):**
```
<instructions>
When analyzing code, look for potential bugs. Bugs are errors in the code that
cause it to malfunction or produce incorrect results. Common bugs include off-by-one
errors, null pointer exceptions, and logic errors.

Also check for security vulnerabilities. Security vulnerabilities are weaknesses
that could be exploited by attackers. Examples include SQL injection, cross-site
scripting (XSS), and insecure authentication.

Additionally, assess code quality. Code quality refers to how well the code is
written, including readability, maintainability, and adherence to best practices.
Poor code quality makes the codebase harder to understand and modify.

Finally, evaluate performance issues. Performance issues are areas where the code
runs slower than necessary or uses more resources than needed. Common performance
problems include inefficient algorithms, unnecessary database queries, and memory
leaks.
</instructions>

<guidelines>
For bugs: identify the error, explain the impact, and suggest a fix.
For security vulnerabilities: note the vulnerability type, describe the risk, and
provide a secure alternative.
For code quality: point out the quality issue, explain why it matters, and recommend
improvements.
For performance: identify the inefficiency, estimate the impact, and suggest
optimizations.
</guidelines>
```

**After (125 tokens):**
```
<instructions>
Analyze code for issues in four categories. For each issue found:
- Identify and categorize
- Explain impact/risk
- Provide fix/improvement

**Categories:**
1. **Bugs**: Errors causing malfunction (off-by-one, null pointer, logic errors)
2. **Security**: Exploitable weaknesses (SQL injection, XSS, auth flaws)
3. **Quality**: Readability, maintainability, best practices
4. **Performance**: Inefficient algorithms, excess queries, memory leaks
</instructions>
```

**Reduction:** 510 → 125 tokens (75% reduction)

**What changed:**
- Merged instructions and guidelines (redundant separation)
- Single format applies to all categories (don't repeat)
- Examples in parentheses instead of separate sentences

## Quality Improvement Optimization

### Optimization 4: Adding Examples for Consistency

**Before (no examples, 120 tokens):**
```
Extract structured data from the product description.

Output format:
{
  "name": "string",
  "category": "string",
  "price": "number",
  "features": ["array", "of", "strings"],
  "availability": "string"
}

{{PRODUCT_DESCRIPTION}}
```

**After (with examples, 340 tokens):**
```
Extract structured data from the product description.

<examples>
<example>
<input>
"UltraBook Pro 15 - Premium laptop with 16GB RAM, 512GB SSD, and stunning 4K display.
Perfect for professionals. Only 3 left in stock! $1,299.99"
</input>
<output>
{
  "name": "UltraBook Pro 15",
  "category": "laptops",
  "price": 1299.99,
  "features": ["16GB RAM", "512GB SSD", "4K display"],
  "availability": "low_stock"
}
</output>
</example>

<example>
<input>
"Wireless Bluetooth Headphones - Noise cancelling, 30hr battery, comfortable fit.
Currently unavailable."
</input>
<output>
{
  "name": "Wireless Bluetooth Headphones",
  "category": "audio",
  "price": null,
  "features": ["noise cancelling", "30hr battery", "comfortable fit"],
  "availability": "out_of_stock"
}
</output>
</example>

<example>
<input>
"SmartWatch X - Fitness tracking, heart rate monitor, waterproof. In stock. $199"
</input>
<output>
{
  "name": "SmartWatch X",
  "category": "wearables",
  "price": 199.00,
  "features": ["fitness tracking", "heart rate monitor", "waterproof"],
  "availability": "in_stock"
}
</output>
</example>
</examples>

{{PRODUCT_DESCRIPTION}}
```

**Addition:** 120 → 340 tokens (220 token increase, 183% of original)

**Quality improvement:**
- Shows how to handle missing data (price: null)
- Demonstrates category inference
- Illustrates availability normalization
- Provides feature extraction pattern

**When worth it:** Inconsistent outputs costing more in retries than 220 tokens cost upfront.

---

### Optimization 5: Adding Structured Chain-of-Thought

**Before (no CoT, 95 tokens):**
```
Analyze whether the product review is genuine or potentially fake.

Consider factors like writing style, specificity, balance, and suspicious patterns.

Output: genuine | suspicious | fake
Confidence: high | medium | low
Reasoning: Brief explanation

{{REVIEW}}
```

**After (with structured CoT, 185 tokens):**
```
Analyze whether the product review is genuine or potentially fake.

<thinking>
Evaluate each factor:

1. **Writing style**: Natural vs formulaic, personal vs generic
2. **Specificity**: Concrete details vs vague praise/criticism
3. **Balance**: Mentions positives and negatives vs one-sided
4. **Suspicious patterns**: Excessive exclamation, promotional language, competitor mentions
5. **Reviewer behavior**: (if available) Review history, timing patterns

For each factor: [your assessment]

Overall assessment: [synthesis]
</thinking>

<judgment>
Classification: genuine | suspicious | fake
Confidence: high | medium | low
Reasoning: [Key factors that led to classification]
</judgment>

{{REVIEW}}
```

**Addition:** 95 → 185 tokens (95% increase)

**Quality improvement:**
- Explicit reasoning process reduces errors
- Structured evaluation ensures all factors considered
- Confidence calibration more accurate with reasoning
- Easier to debug when classification wrong

## Hallucination Reduction Optimization

### Optimization 6: Adding Quote-Grounding

**Before (no quote requirement, 110 tokens):**
```
Answer the user's question about the research paper.

Provide accurate information based on the paper's findings.

<paper>
{{RESEARCH_PAPER}}
</paper>

<question>
{{USER_QUESTION}}
</question>
```

**After (with quote-grounding, 210 tokens):**
```
Answer the user's question about the research paper using a two-step process.

Step 1: Extract relevant quotes
<quotes>
For each relevant finding:
- "[Exact quote]" [Section, page]
</quotes>

Step 2: Answer based on quotes
<answer>
[Your answer with references to quote numbers]
</answer>

Critical rule: Every factual claim must trace to a specific quote. If you find
yourself making a claim without a quote, either find the quote or don't make the claim.

If the paper doesn't address the question, state: "The paper does not provide
information about [topic]."

<paper>
{{RESEARCH_PAPER}}
</paper>

<question>
{{USER_QUESTION}}
</question>
```

**Addition:** 110 → 210 tokens (91% increase)

**Quality improvement:**
- Hallucination rate drops significantly
- Claims become verifiable
- Makes Claude identify what's actually present vs inferred

---

### Optimization 7: Adding Uncertainty Permission

**Before (no uncertainty guidance, 75 tokens):**
```
Based on the financial data provided, answer questions about the company's performance.

<data>
{{FINANCIAL_DATA}}
</data>

<question>
{{QUESTION}}
</question>
```

**After (with uncertainty permission, 155 tokens):**
```
Based on the financial data provided, answer questions about the company's performance.

**Critical: Epistemic honesty**
If the data doesn't contain information needed to answer fully, explicitly state:
"The data doesn't provide [specific information]. Available data shows: [what is present]."

Do NOT:
- Infer missing data points
- Calculate metrics not present in the data
- Extrapolate trends beyond the data period
- Present assumptions as facts

It's better to admit limitations than to speculate.

<data>
{{FINANCIAL_DATA}}
</data>

<question>
{{QUESTION}}
</question>
```

**Addition:** 75 → 155 tokens (107% increase)

**Quality improvement:**
- Prevents fabricated financial figures
- User knows what's based on data vs speculation
- Reduces liability for incorrect information

## Caching Implementation Optimization

### Optimization 8: Restructuring for Cache Efficiency

**Before (poor caching structure, breaks cache frequently):**
```python
system_prompt = f"""
Current date: {datetime.now().strftime('%Y-%m-%d')}
Session ID: {session_id}

You are a technical support agent for CloudCorp. Here are the extensive product
documentation and guidelines:

{large_documentation}  # 50K tokens

{support_guidelines}   # 10K tokens

Current system status: {fetch_system_status()}
"""
```

**Problem:** Date and session_id change every request, breaking cache for entire 60K token block.

**After (optimized caching structure):**
```python
messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": large_documentation,  # 50K tokens - static
                "cache_control": {"type": "ephemeral"}
            },
            {
                "type": "text",
                "text": support_guidelines,  # 10K tokens - static
                "cache_control": {"type": "ephemeral"}
            },
            {
                "type": "text",
                "text": f"""Current date: {datetime.now().strftime('%Y-%m-%d')}
Session ID: {session_id}
Current system status: {fetch_system_status()}"""  # Dynamic - not cached
            },
            {
                "type": "text",
                "text": user_query
            }
        ]
    }
]
```

**Improvement:**
- Before: 0% cache hit rate (always breaking)
- After: 60K/60K tokens cached = 100% cache hit on static content
- Cost reduction: ~95% on cached portion after initial write

---

### Optimization 9: Multi-Level Caching for Mixed Update Frequencies

**Before (single cache block, breaks when any part updates):**
```python
system = [{
    "type": "text",
    "text": f"{core_instructions}\n\n{knowledge_base}\n\n{recent_updates}",
    "cache_control": {"type": "ephemeral"}
}]
```

**Update frequency:**
- core_instructions: Never changes
- knowledge_base: Updated weekly
- recent_updates: Updated daily

**Problem:** Daily updates break cache for entire block (including weekly and static content).

**After (multi-level caching):**
```python
system = [
    {
        "type": "text",
        "text": core_instructions,  # Static - Level 1 cache
        "cache_control": {"type": "ephemeral"}
    },
    {
        "type": "text",
        "text": knowledge_base,  # Weekly updates - Level 2 cache
        "cache_control": {"type": "ephemeral"}
    },
    {
        "type": "text",
        "text": recent_updates  # Daily updates - not cached
    }
]
```

**Improvement:**
- Core instructions always cached (100% hit rate)
- Knowledge base cached 6/7 days (86% hit rate)
- Only recent_updates recalculated daily
- Effective cache rate increases from ~0% to ~90%+

## Prompt Splitting Optimization

### Optimization 10: Chaining for Focused Attention

**Before (single complex prompt, 650 tokens):**
```xml
<instructions>
You will review a legal contract and perform comprehensive analysis.

Step 1: Read the entire contract carefully and identify all key terms in these
categories: payment terms, termination clauses, liability limitations, intellectual
property rights, confidentiality obligations, dispute resolution mechanisms, and
any unusual or non-standard provisions.

Step 2: For each identified term, analyze the risks from the client's perspective.
Consider factors like financial exposure, operational constraints, legal liability,
and competitive implications. Rate each risk as low, medium, high, or critical.

Step 3: Based on the risk analysis, develop specific recommendations. For high and
critical risks, suggest alternative language or negotiation points. For medium risks,
note areas requiring client decision. For low risks, document for completeness.

Step 4: Compile everything into a comprehensive report with executive summary,
detailed findings, risk matrix, and actionable recommendations prioritized by urgency.

Provide thorough analysis addressing all aspects of the contract.
</instructions>

<contract>
{{CONTRACT}}  # 30K tokens
</contract>
```

**Problem:** Trying to do extraction, analysis, and recommendation generation simultaneously leads to:
- Missed terms (attention divided)
- Inconsistent risk assessment
- Recommendations not well-grounded in analysis

**After (chained prompts with focused objectives):**

**Prompt 1: Term Extraction (200 tokens + contract)**
```xml
<objective>Extract and categorize key contract terms.</objective>

<instructions>
Read the contract and extract terms in these categories:
- payment
- termination
- liability
- intellectual_property
- confidentiality
- dispute_resolution
- unusual_provisions

<extracted_terms>
  <term category="[category]">
    <description>[What the term says]</description>
    <location>[Section, page]</location>
  </term>
</extracted_terms>

Focus solely on accurate, complete extraction. Analysis comes in next step.
</instructions>

<contract>{{CONTRACT}}</contract>
```

**Prompt 2: Risk Analysis (180 tokens + extracted terms)**
```xml
<objective>Analyze risks for each extracted term.</objective>

<instructions>
For each term below, assess risk from client perspective:

<risk_assessment>
  <term_risk>
    <term_reference>[From extraction]</term_reference>
    <risk_level>low|medium|high|critical</risk_level>
    <risk_factors>
      <financial>[Exposure]</financial>
      <operational>[Constraints]</operational>
      <legal>[Liability]</legal>
      <competitive>[Implications]</competitive>
    </risk_factors>
  </term_risk>
</risk_assessment>

Focus solely on thorough risk assessment. Recommendations come in next step.
</instructions>

<extracted_terms>{{TERMS_FROM_PROMPT_1}}</extracted_terms>
```

**Prompt 3: Recommendations (170 tokens + risk assessment)**
```xml
<objective>Generate actionable recommendations based on risk analysis.</objective>

<instructions>
For each medium+ risk, provide:

<recommendations>
  <recommendation>
    <term_reference>[From analysis]</term_reference>
    <priority>critical|high|medium</priority>
    <action>negotiate|modify|accept_with_conditions</action>
    <suggested_language>[Alternative wording]</suggested_language>
    <negotiation_points>[Key arguments]</negotiation_points>
  </recommendation>
</recommendations>

For low risks: <low_risks_summary>[Brief note]</low_risks_summary>
</instructions>

<risk_assessment>{{RISKS_FROM_PROMPT_2}}</risk_assessment>
```

**Improvement:**
- Each prompt has single clear objective
- Extraction more complete (full attention)
- Risk analysis more consistent (focused evaluation)
- Recommendations better grounded (based on structured analysis)
- Easier to debug (isolate which step has issues)
- Can improve individual steps without affecting others

**Token comparison:**
- Before: 650 instructions + 30K contract = 30,650 tokens
- After: 200 + 30K + 180 + extracted_terms + 170 + risks = ~31,500 tokens
- Slight increase (2.8%) but significant quality improvement

## Combined Optimization Example

### Optimization 11: Full Optimization Stack

**Before (inefficient prompt, 125K tokens total):**

```python
prompt = f"""
You are an AI assistant helping analyze customer support tickets. Customer support
is an important function that helps users resolve issues with products and services.
Good customer support improves satisfaction and retention.

When analyzing tickets, you need to understand the customer's issue, determine the
appropriate team to handle it, and assess the urgency. Issues can range from simple
questions to critical system outages.

Support tickets come in via email, chat, and phone. Each channel has different
expectations for response time. Email tickets should be responded to within 24 hours,
chat within 5 minutes, and phone calls should be handled immediately.

Here is our complete product knowledge base:
{entire_knowledge_base}  # 100K tokens - rarely needed, could use selective retrieval

Current date and time: {datetime.now()}
Operator ID: {operator_id}
System status: All systems operational

For each ticket, output the following information:
- Category: The type of issue
- Priority: How urgent the issue is
- Assigned team: Which team should handle it
- Suggested response: A draft response to the customer
- Related articles: Links to knowledge base articles

Ticket to analyze:
{ticket_content}
"""
```

**Problems:**
1. Verbose unnecessary background (250 tokens wasted)
2. Entire knowledge base embedded (100K tokens, only ~1K relevant per ticket)
3. No caching despite repetitive structure
4. No examples leading to inconsistent categorization
5. Single complex task (could split routing from response drafting)

**After (fully optimized):**

```python
# Cacheable system prompt (5K tokens after removing KB)
system_prompt = [
    {
        "type": "text",
        "text": """Analyze support tickets for routing and response.

Output format:
{
  "category": "billing|technical|account|general",
  "priority": "critical|high|medium|low",
  "team": "billing|engineering|account_management|tier1_support",
  "response_draft": "...",
  "kb_articles": ["article_id1", "article_id2"]
}

Priority guidelines:
- critical: System down, data loss, security breach
- high: Major feature broken, blocking work
- medium: Partial functionality issue
- low: Questions, minor bugs, feature requests""",
        "cache_control": {"type": "ephemeral"}
    },
    {
        "type": "text",
        "text": """Examples:

<example>
<input>
Channel: email
Issue: "I was charged twice for my subscription this month. Can you refund the duplicate charge?"
</input>
<output>
{
  "category": "billing",
  "priority": "high",
  "team": "billing",
  "response_draft": "I apologize for the duplicate charge. I've escalated this to our billing team who will process your refund within 2-3 business days. You'll receive a confirmation email once completed.",
  "kb_articles": ["refund-policy", "billing-issues"]
}
</output>
</example>

[2 more examples covering technical and account categories]""",
        "cache_control": {"type": "ephemeral"}
    }
]

# Retrieve only relevant KB articles (RAG approach)
relevant_kb = retrieve_relevant_articles(ticket_content)  # ~1K tokens instead of 100K

# Dynamic content (not cached)
user_message = f"""
Context:
- Date: {datetime.now().strftime('%Y-%m-%d')}
- Operator: {operator_id}
- Channel: {ticket_channel}

Relevant KB articles:
{relevant_kb}

Ticket:
{ticket_content}
"""

# Make request
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    system=system_prompt,
    messages=[{"role": "user", "content": user_message}],
    max_tokens=1000
)
```

**Improvements:**
1. **Token reduction:** 125K → 7K (94% reduction)
   - Removed verbose background: 250 → 0 tokens
   - RAG instead of full KB: 100K → 1K tokens
   - Concise instructions: 400 → 150 tokens

2. **Caching implemented:** 5K tokens cached
   - Cache hit rate: ~95% (only first request pays write cost)
   - Cost reduction: ~90% after initial request

3. **Quality improvements:**
   - Added 3 examples for consistency
   - Structured output format
   - Clear priority guidelines

4. **Cost comparison:**
   - Before: 125K tokens × $3/1M = $0.375 per request
   - After first request: 7K tokens × $3/1M = $0.021 per request
   - After cache hits: (2K + 5K cached) × ($3 + $0.30)/1M = $0.0076 per request
   - **98% cost reduction at scale**

5. **Quality maintained/improved:**
   - Faster (less tokens to process)
   - More consistent (examples added)
   - More accurate (relevant KB only)

This demonstrates combining multiple optimization strategies for maximum impact.
