# Analysis Patterns

Common prompt issues, evaluation examples, and quality assessment criteria.

## Common Prompt Issues

### Issue Category 1: Vague Objectives

**Symptoms:**
- Instructions like "analyze this" or "improve the code"
- No success criteria defined
- Output requirements unclear
- User doesn't know what they'll get

**Example - Poor prompt:**
```
Analyze this data and provide insights.

{{DATA}}
```

**Problems:**
- What kind of analysis? (Statistical, trends, anomalies, comparisons?)
- What insights? (Business recommendations, technical findings, data quality?)
- What format? (Report, bullet points, visualizations?)
- How deep? (High-level overview or detailed breakdown?)

**Evaluation checklist:**
- [ ] Clear objective stated
- [ ] Success criteria defined
- [ ] Output format specified
- [ ] Scope boundaries set

**Fix pattern:**
```
Analyze customer churn data to identify retention opportunities.

Objectives:
- Identify top 3 factors correlated with churn
- Segment customers by churn risk (high/medium/low)
- Recommend specific retention strategies for each segment

Output format:
1. Executive summary (3-5 sentences)
2. Statistical findings with confidence intervals
3. Customer segments with characteristics
4. Actionable recommendations prioritized by impact

{{DATA}}
```

---

### Issue Category 2: Missing Context

**Symptoms:**
- Claude makes incorrect assumptions about use case
- Output doesn't match intended audience or purpose
- Tone or detail level inappropriate

**Example - Poor prompt:**
```
Write a product description.

Product: CloudSync Pro
Features: File sync, encryption, team collaboration, 10GB storage
```

**Problems:**
- Who's the audience? (Technical users, business buyers, general consumers?)
- Where will this appear? (Website, app store, sales deck?)
- What action should it drive? (Purchase, trial signup, learn more?)
- What differentiates it? (Why choose this over competitors?)

**Evaluation checklist:**
- [ ] Target audience identified
- [ ] Use case/context provided
- [ ] Tone/style specified
- [ ] Key differentiators noted

**Fix pattern:**
```
Write a product description for our company website's pricing page.

Product: CloudSync Pro
Features: File sync, encryption, team collaboration, 10GB storage

Context:
- Audience: Small business owners (5-50 employees)
- Goal: Convert to paid subscription after trial
- Differentiator: Enterprise-grade security at SMB pricing
- Tone: Professional but approachable, emphasize reliability

Avoid technical jargon. Focus on business benefits over features. Include social
proof reference ("trusted by 10,000+ businesses").

Output: 100-150 words, 2-3 paragraphs
```

---

### Issue Category 3: No Examples (When Needed)

**Symptoms:**
- Inconsistent output format across runs
- Claude misinterprets desired structure
- Quality varies significantly

**Example - Poor prompt:**
```
Extract entities from the text and output as JSON.

{{TEXT}}
```

**Result:** Claude might output:
```json
{"entities": ["John", "Microsoft", "Seattle"]}
```
or:
```json
{"people": ["John"], "organizations": ["Microsoft"], "locations": ["Seattle"]}
```
or:
```json
[{"text": "John", "type": "PERSON"}, ...]
```

**All valid interpretations, but inconsistent!**

**Evaluation checklist:**
- [ ] Output structure has multiple valid interpretations?
- [ ] Task complexity warrants examples?
- [ ] Edge cases need demonstration?
- [ ] Format variations need clarification?

**Fix pattern:**
```
Extract entities from the text and output as JSON.

<examples>
<example>
<input>
"John Smith, CEO of Acme Corp, announced the merger yesterday in San Francisco."
</input>
<output>
{
  "people": [{"name": "John Smith", "title": "CEO"}],
  "organizations": ["Acme Corp"],
  "locations": ["San Francisco"],
  "events": ["merger"]
}
</output>
</example>

<example>
<input>
"The conference starts Monday. No speakers announced yet."
</input>
<output>
{
  "people": [],
  "organizations": [],
  "locations": [],
  "events": ["conference"]
}
</output>
</example>
</examples>

{{TEXT}}
```

---

### Issue Category 4: No Chain-of-Thought (When Needed)

**Symptoms:**
- Errors in multi-step reasoning
- Logical gaps in analysis
- Can't debug why Claude reached conclusion

**Example - Poor prompt:**
```
Is this code secure? Identify any vulnerabilities.

{{CODE}}
```

**Problem:** Claude jumps straight to answer without showing reasoning, potentially missing issues.

**Evaluation checklist:**
- [ ] Task requires multi-step analysis?
- [ ] Judgment and tradeoffs involved?
- [ ] Need to verify reasoning process?
- [ ] Debugging might be necessary?

**Fix pattern:**
```
Analyze this code for security vulnerabilities.

<thinking>
Systematic security review:

1. Input validation:
   - Where does user input enter?
   - Is it sanitized/validated?
   - Could it be exploited?

2. Authentication/Authorization:
   - Are access controls present?
   - Are they sufficient?
   - Privilege escalation risks?

3. Data handling:
   - Is sensitive data protected?
   - Encryption used appropriately?
   - Data leakage risks?

4. Common vulnerabilities:
   - SQL injection possible?
   - XSS vectors present?
   - CSRF protections in place?

For each area: [your detailed analysis]
</thinking>

<vulnerabilities>
[List identified issues with severity and remediation]
</vulnerabilities>

{{CODE}}
```

---

### Issue Category 5: Poor XML Structure

**Symptoms:**
- Claude confuses different prompt sections
- Instructions mixed with data
- Hard to reference specific components

**Example - Poor prompt:**
```
Analyze the contract below and compare it to industry standards. The contract
is from TechCorp dated 2024-01-15. Industry standards say payment terms should
be Net 30, liability caps should be 2x annual contract value, and termination
notice should be 60 days.

CONTRACT TEXT:
[Large contract text]

Make sure to check payment terms, liability, and termination carefully.
```

**Problems:**
- Contract text not clearly separated
- Industry standards embedded in prose (hard to reference)
- Instructions scattered (beginning and end)
- No clear structure for Claude to follow

**Evaluation checklist:**
- [ ] Multiple distinct components (data, instructions, examples)?
- [ ] Large documents need clear boundaries?
- [ ] Instructions reference specific sections?
- [ ] Output has multiple parts?

**Fix pattern:**
```
<role>
You are a contract analyst comparing agreements to industry standards.
</role>

<industry_standards>
  <standard category="payment">
    <best_practice>Net 30 payment terms</best_practice>
    <rationale>Standard B2B practice for cash flow management</rationale>
  </standard>
  <standard category="liability">
    <best_practice>Liability cap at 2x annual contract value</best_practice>
    <rationale>Balances risk protection with business viability</rationale>
  </standard>
  <standard category="termination">
    <best_practice>60 days notice required</best_practice>
    <rationale>Sufficient time for transition planning</rationale>
  </standard>
</industry_standards>

<instructions>
Compare the contract against industry standards above.

For each standard:
1. Locate relevant contract language
2. Compare to best practice
3. Assess deviation severity (none|minor|moderate|major)
4. Recommend action (accept|negotiate|reject)

<comparison_output>
  <standard_comparison>
    <category>[Category name]</category>
    <contract_terms>[What contract says]</contract_terms>
    <standard_terms>[What standard recommends]</standard_terms>
    <deviation_severity>[Level]</deviation_severity>
    <recommendation>[Action]</recommendation>
    <rationale>[Why]</rationale>
  </standard_comparison>
</comparison_output>
</instructions>

<contract>
  <metadata>
    <party>TechCorp</party>
    <date>2024-01-15</date>
  </metadata>
  <contract_text>
[Contract text here]
  </contract_text>
</contract>
```

---

### Issue Category 6: No Guardrails (When Needed)

**Symptoms:**
- Hallucinated facts or figures
- Inconsistent outputs across similar inputs
- Security/safety issues

**Example - Poor prompt:**
```
Summarize the key findings from the research paper.

{{RESEARCH_PAPER}}
```

**Problems:**
- No requirement to ground in actual paper text
- No handling of missing/unclear information
- No citation requirements
- Claude might infer beyond what paper states

**Evaluation checklist:**
- [ ] Factual accuracy critical?
- [ ] Consistency requirements high?
- [ ] Security/safety concerns present?
- [ ] Character maintenance needed?

**Fix pattern:**
```
Summarize the key findings from the research paper.

Accuracy requirements:
- Extract exact quotes for each key finding before summarizing
- Every claim must be traceable to specific paper section
- If paper doesn't clearly state something, note: "Paper does not explicitly address [topic]"
- Do not infer findings beyond what paper directly states

Process:
<quotes>
[Extract relevant quotes with page numbers]
</quotes>

<summary>
[Summary based solely on extracted quotes]
</summary>

{{RESEARCH_PAPER}}
```

---

## Quality Assessment Criteria

### Criterion 1: Clarity (0-10 scale)

**10 - Excellent clarity:**
- Objective crystal clear
- Instructions explicit and unambiguous
- No room for misinterpretation
- Colleague test passes easily

**7 - Good clarity:**
- Objective clear
- Most instructions explicit
- Minor ambiguities possible
- Colleague would mostly understand

**4 - Poor clarity:**
- Objective vague
- Instructions require interpretation
- Multiple valid interpretations exist
- Colleague would have questions

**1 - Very poor clarity:**
- Objective unclear
- Instructions confusing or contradictory
- Colleague completely confused

**Assessment questions:**
- Can you explain the objective in one sentence?
- Would a colleague understand without context?
- Are there multiple ways to interpret instructions?
- Is output format unambiguous?

---

### Criterion 2: Completeness (0-10 scale)

**10 - Fully complete:**
- All necessary context provided
- Success criteria defined
- Edge cases covered
- Output format specified
- Constraints stated

**7 - Mostly complete:**
- Core information present
- Success criteria implied or basic
- Main scenarios covered
- Output format mostly clear

**4 - Incomplete:**
- Missing important context
- No success criteria
- Edge cases ignored
- Output format vague

**1 - Very incomplete:**
- Critical information missing
- No guidance on success
- Major gaps in requirements

**Assessment questions:**
- Does Claude have everything needed?
- Are success criteria measurable?
- Are edge cases handled?
- Is output format fully specified?

---

### Criterion 3: Efficiency (0-10 scale)

**10 - Highly efficient:**
- No redundant information
- Minimal token usage for value delivered
- Caching implemented where beneficial
- Progressive disclosure used appropriately

**7 - Good efficiency:**
- Mostly concise
- Some optimization opportunities exist
- Reasonable token usage

**4 - Poor efficiency:**
- Verbose and redundant
- Significant token waste
- No optimization attempts

**1 - Very inefficient:**
- Extremely verbose
- Massive redundancy
- Obvious optimization opportunities ignored

**Assessment questions:**
- Could anything be said more concisely?
- Is there redundant information?
- Are caching opportunities identified?
- Is token usage justified?

---

### Criterion 4: Technique Application (0-10 scale)

**10 - Excellent technique application:**
- Examples provided (3-5 for complex tasks)
- Chain-of-thought where reasoning needed
- XML tags for clear structure
- Guardrails appropriate to risk level
- Template variables for reusability

**7 - Good technique application:**
- Most appropriate techniques present
- Some techniques could be better applied
- Generally follows best practices

**4 - Poor technique application:**
- Missing key techniques
- Techniques poorly applied
- Doesn't follow best practices

**1 - No technique application:**
- No examples where needed
- No structure
- No guardrails
- No optimization

**Assessment questions:**
- Are examples provided for complex tasks?
- Is chain-of-thought enabled for reasoning?
- Are XML tags used for structure?
- Are guardrails appropriate?

---

### Criterion 5: Claude 4.5 Optimization (0-10 scale)

**10 - Fully optimized for Claude 4.5:**
- Explicit, specific instructions
- Contextual motivation provided
- Example quality high (no unintended patterns)
- Action framing (not suggestion)
- Summary requests explicit
- Quality modifiers for creative tasks
- Parallel execution guidance
- Context awareness leveraged

**7 - Good Claude 4.5 alignment:**
- Mostly explicit instructions
- Some contextual motivation
- Examples decent quality
- Most Claude 4.5 features considered

**4 - Poor Claude 4.5 alignment:**
- Vague instructions (Claude 3 style)
- Missing contextual motivation
- Example quality issues
- Suggestion framing instead of action

**1 - Not optimized for Claude 4.5:**
- Written for Claude 3
- No Claude 4.5 features leveraged
- Would require migration

**Assessment questions:**
- Are instructions explicit enough for Claude 4.5?
- Is contextual motivation provided?
- Are examples high quality and consistent?
- Are Claude 4.5 capabilities leveraged?

---

## Analysis Template

When analyzing a prompt, use this structure:

```xml
<prompt_analysis>
  <summary>
[Brief description of prompt purpose and current state]
  </summary>

  <scores>
    <clarity>X/10 - [Brief reasoning]</clarity>
    <completeness>X/10 - [Brief reasoning]</completeness>
    <efficiency>X/10 - [Brief reasoning]</efficiency>
    <technique_application>X/10 - [Brief reasoning]</technique_application>
    <claude_45_optimization>X/10 - [Brief reasoning]</claude_45_optimization>
    <overall>X/10 - [Average or weighted]</overall>
  </scores>

  <strengths>
    - [What the prompt does well]
    - [Another strength]
  </strengths>

  <issues>
    <critical>
      - [Issue that severely impacts functionality]
    </critical>
    <major>
      - [Issue that significantly impacts quality]
    </major>
    <minor>
      - [Issue that could be improved but not essential]
    </minor>
  </issues>

  <recommendations>
    <recommendation priority="critical|major|minor">
      <change>[Specific modification to make]</change>
      <rationale>[Why this improves the prompt]</rationale>
      <implementation>[How to apply the change]</implementation>
      <before>[Current problematic pattern]</before>
      <after>[Improved pattern]</after>
    </recommendation>
  </recommendations>

  <optimization_opportunities>
    <context_optimization>
      - [Token reduction strategies]
      - [Caching opportunities]
    </context_optimization>
    <quality_improvements>
      - [Technique additions]
      - [Guardrail implementations]
    </quality_improvements>
  </optimization_opportunities>
</prompt_analysis>
```

## Example Full Analysis

**Prompt to analyze:**
```
Analyze customer reviews and tell me what people think about the product.

Reviews:
[20 customer reviews, ~5K tokens]
```

**Analysis:**

```xml
<prompt_analysis>
  <summary>
Simple customer review analysis prompt. Very vague with minimal structure.
Lacks context, examples, output format, and any guardrails. Approximately 5K
tokens with no optimization.
  </summary>

  <scores>
    <clarity>2/10 - Objective extremely vague ("what people think" is not specific)</clarity>
    <completeness>1/10 - Missing context, output format, success criteria</completeness>
    <efficiency>5/10 - Token usage reasonable for data size, but no structure</efficiency>
    <technique_application>1/10 - No examples, no CoT, no XML structure, no guardrails</technique_application>
    <claude_45_optimization>2/10 - Vague instructions problematic for Claude 4.5</claude_45_optimization>
    <overall>2.2/10 - Needs substantial improvement</overall>
  </scores>

  <strengths>
    - Includes the actual data to analyze
    - Token usage not excessive for task
  </strengths>

  <issues>
    <critical>
      - No clear objective (what aspects to analyze?)
      - No output format specified (Claude will guess)
      - No success criteria defined
    </critical>
    <major>
      - No examples (output structure will be inconsistent)
      - Missing context (who's the audience? what decisions depend on this?)
      - No sentiment categorization guidance
      - No handling of edge cases (sarcasm, mixed sentiment)
    </major>
    <minor>
      - Could benefit from XML structure for multiple reviews
      - No chain-of-thought for reasoning visibility
    </minor>
  </issues>

  <recommendations>
    <recommendation priority="critical">
      <change>Define specific analysis objectives and output format</change>
      <rationale>Claude needs explicit guidance on what insights to extract</rationale>
      <implementation>Add objectives section with specific analysis categories and JSON output schema</implementation>
      <before>
"Analyze customer reviews and tell me what people think about the product."
      </before>
      <after>
"Analyze customer reviews to identify actionable product improvement opportunities.

Extract for each review:
1. Overall sentiment (positive/neutral/negative)
2. Specific aspects mentioned (quality, price, features, support)
3. Key issues or praise points
4. Suggested improvements

Output format:
{
  \"summary\": {
    \"positive_count\": N,
    \"neutral_count\": N,
    \"negative_count\": N,
    \"top_themes\": [\"theme1\", \"theme2\"]
  },
  \"reviews\": [
    {
      \"id\": N,
      \"sentiment\": \"positive|neutral|negative\",
      \"aspects\": {\"quality\": \"positive\", \"price\": \"negative\"},
      \"key_points\": [\"...\", \"...\"],
      \"suggested_improvements\": [\"...\"]
    }
  ],
  \"recommendations\": [\"Most impactful improvements based on frequency and sentiment\"]
}"
      </after>
    </recommendation>

    <recommendation priority="major">
      <change>Add 3 diverse examples showing edge cases</change>
      <rationale>Ensures consistent output structure and handling of mixed/sarcastic reviews</rationale>
      <implementation>Add examples block with positive, negative, and mixed sentiment reviews</implementation>
      <before>
[No examples]
      </before>
      <after>
<examples>
<example>
<input>"Great product! Love the new features. A bit pricey though."</input>
<output>
{
  \"sentiment\": \"positive\",
  \"aspects\": {\"features\": \"positive\", \"price\": \"negative\"},
  \"key_points\": [\"Appreciates new features\", \"Price concern\"],
  \"suggested_improvements\": [\"Consider pricing adjustment or value communication\"]
}
</output>
</example>
[2 more examples: clearly negative, neutral/sarcastic]
</examples>
      </after>
    </recommendation>

    <recommendation priority="major">
      <change>Add context about use case and decision impact</change>
      <rationale>Helps Claude prioritize insights and tailor analysis depth</rationale>
      <implementation>Add context section explaining how analysis will be used</implementation>
      <before>
[No context]
      </before>
      <after>
Context: Analysis informs product roadmap priorities for Q2. Product team needs
specific, actionable insights on what to improve. Focus on recurring themes
affecting multiple customers over isolated issues.
      </after>
    </recommendation>

    <recommendation priority="minor">
      <change>Structure reviews with XML for clarity</change>
      <rationale>Clearer boundaries between reviews, easier to reference specific items</rationale>
      <implementation>Wrap each review in XML structure</implementation>
      <before>
Reviews:
[Review 1 text]
[Review 2 text]
      </before>
      <after>
<reviews>
  <review id="1">[Review 1 text]</review>
  <review id="2">[Review 2 text]</review>
</reviews>
      </after>
    </recommendation>
  </recommendations>

  <optimization_opportunities>
    <context_optimization>
      - Current: ~5K tokens (reviews)
      - Could structure reviews more efficiently with XML (minor savings)
      - If analyzing multiple batches, cache analysis instructions (~500 tokens)
    </context_optimization>
    <quality_improvements>
      - Add chain-of-thought for complex sentiment analysis
      - Implement consistency guardrail (examples + format spec)
      - Add handling for sarcasm/mixed sentiment explicitly
    </quality_improvements>
  </optimization_opportunities>
</prompt_analysis>
```

Use this template and criteria for systematic prompt analysis.
