# Extraction Decision Guide

Decision trees and criteria for determining when to extract logic to prompts, scripts, or keep inline.

## Decision Framework Overview

Three extraction options:
1. **Extract to reusable prompt** - Logic needs Claude's reasoning, will be reused
2. **Extract to script** - Logic is deterministic, algorithmic, testable
3. **Keep inline** - One-time use, context-specific, tightly coupled

## Decision Tree

```
START: Evaluating logic for extraction
│
├─ Is this logic reused across multiple contexts?
│  ├─ No → Keep inline (unless complex enough to warrant extraction for clarity)
│  └─ Yes → Continue evaluation
│
├─ Does the logic require Claude's reasoning/judgment?
│  ├─ Yes → Consider PROMPT extraction
│  │  └─ Evaluate prompt extraction criteria (6 factors below)
│  │
│  └─ No → Consider SCRIPT extraction
│     └─ Evaluate script extraction criteria (6 factors below)
│
└─ Is logic complex enough to warrant extraction?
   ├─ Yes → Extract based on above criteria
   └─ No → Keep inline even if reused (simple enough to repeat)
```

## Prompt Extraction Criteria

Extract to reusable prompt template if **3 or more** criteria met:

### Criterion 1: Reusability (Strong indicator)
**Score 1 if:**
- Logic used across 3+ different contexts/conversations
- Standard approach needed across team/project
- Multiple users will invoke this pattern

**Examples:**
- ✓ Code review workflow (used for every PR)
- ✓ Customer feedback analysis (used for every survey batch)
- ✓ Contract term extraction (used for each new contract)
- ✗ One-time data migration script
- ✗ Project-specific analysis for single client

### Criterion 2: Prompt Engineering Techniques Required
**Score 1 if:**
- Needs 3+ examples for consistency
- Requires structured chain-of-thought
- Benefits from XML tag organization
- Uses template variables for different inputs
- Needs specific response prefilling

**Examples:**
- ✓ Sentiment analysis with nuanced categories (needs examples)
- ✓ Multi-step reasoning for medical diagnosis (needs CoT)
- ✓ Structured data extraction from varied documents (needs XML + examples)
- ✗ Simple classification with obvious categories
- ✗ Straightforward question answering

### Criterion 3: Guardrails Needed
**Score 1 if:**
- Hallucination prevention required (quote-grounding, citations)
- Consistency enforcement critical (format specification, examples)
- Security measures needed (input screening, prompt leak protection)
- Character maintenance important (role boundaries, persona)

**Examples:**
- ✓ Financial analysis (hallucination prevention critical)
- ✓ Medical information assistant (guardrails essential)
- ✓ Legal document review (accuracy and citations required)
- ✗ Creative writing assistance (hallucinations acceptable)
- ✗ Brainstorming sessions (consistency less important)

### Criterion 4: Context Optimization Beneficial
**Score 1 if:**
- Would benefit from prompt caching (static content >1024 tokens)
- Needs document organization (20K+ token documents)
- Splitting into chained prompts would improve quality
- Quote-grounding would reduce context usage

**Examples:**
- ✓ Analysis with large knowledge base (cache KB, use repeatedly)
- ✓ Research synthesis from multiple long papers (document organization)
- ✓ Multi-phase workflow (extraction → analysis → recommendations)
- ✗ Simple queries with <1K context
- ✗ Single-step analysis of short inputs

### Criterion 5: Standardization Needed
**Score 1 if:**
- Team needs consistent approach
- Output format must be identical across uses
- Quality requirements uniform across contexts
- Reduces variation in how task is approached

**Examples:**
- ✓ Bug report triage (standardize priority assessment)
- ✓ Interview evaluation (consistent scoring criteria)
- ✓ Content moderation (uniform policy application)
- ✗ Ad-hoc analysis with varying requirements
- ✗ Exploratory tasks where variation is desired

### Criterion 6: Sufficient Complexity
**Score 1 if:**
- Instructions would be >200 tokens
- Requires multiple steps or phases
- Benefits from structured workflow
- Has multiple quality checkpoints

**Examples:**
- ✓ Comprehensive code review (multiple checks, Structured Outputs)
- ✓ Research paper analysis (multi-phase: extract → analyze → synthesize)
- ✓ Customer support ticket routing (categorization + prioritization + response drafting)
- ✗ Simple sentiment classification
- ✗ Single-field data extraction

### Scoring & Decision

**Count criteria met (0-6):**
- 0-2: Keep inline or use simple prompt pattern
- 3-4: Extract to reusable prompt template
- 5-6: Strongly recommended for extraction

## Script Extraction Criteria

Extract to separate script if **3 or more** criteria met:

### Criterion 1: Deterministic Logic
**Score 1 if:**
- Same input always produces same output
- No judgment or reasoning required
- Algorithmic or rule-based processing
- No context-dependent decisions

**Examples:**
- ✓ Email address validation (regex pattern matching)
- ✓ Date format conversion (algorithmic)
- ✓ JSON schema validation (rule-based)
- ✗ Sentiment analysis (requires judgment)
- ✗ Content quality assessment (subjective)

### Criterion 2: Computation-Heavy
**Score 1 if:**
- Involves calculations or data processing
- Performance-critical operations
- Large dataset manipulation
- Iterative algorithms

**Examples:**
- ✓ Statistical analysis on dataset
- ✓ Image resizing and compression
- ✓ Sorting and filtering large data
- ✗ Text generation
- ✗ Conceptual analysis

### Criterion 3: Testable with Unit Tests
**Score 1 if:**
- Can write comprehensive unit tests
- Test cases have clear pass/fail criteria
- Edge cases identifiable and testable
- No subjective evaluation needed

**Examples:**
- ✓ URL parser (clear test cases)
- ✓ Data validation function (definite rules)
- ✓ Format converter (deterministic outputs)
- ✗ Creative content generation (subjective quality)
- ✗ Nuanced classification (fuzzy boundaries)

### Criterion 4: Reusable Across Prompts
**Score 1 if:**
- Multiple different prompts would use this logic
- Not specific to single use case
- Provides utility function others can leverage
- Reduces duplication across prompt templates

**Examples:**
- ✓ Citation formatter (used by multiple analysis prompts)
- ✓ Data sanitizer (preprocessing for various prompts)
- ✓ Output validator (post-processing for multiple workflows)
- ✗ Prompt-specific calculation
- ✗ One-time data transformation

### Criterion 5: No Reasoning Required
**Score 1 if:**
- No "understanding" needed
- No context interpretation required
- No judgment calls
- Pure mechanical processing

**Examples:**
- ✓ Text tokenization (mechanical)
- ✓ File path manipulation (rule-based)
- ✓ Character encoding conversion (deterministic)
- ✗ Intent classification (needs understanding)
- ✗ Relevance filtering (needs judgment)

### Criterion 6: Format Conversion or Validation
**Score 1 if:**
- Converting between data formats
- Validating structure or content
- Parsing structured data
- Schema enforcement

**Examples:**
- ✓ Markdown to HTML converter
- ✓ JSON schema validator
- ✓ CSV parser
- ✗ Natural language generation
- ✗ Content summarization

### Scoring & Decision

**Count criteria met (0-6):**
- 0-2: Keep logic in prompt or inline
- 3-4: Extract to script
- 5-6: Strongly recommended for script extraction

## Keep Inline Criteria

Keep logic inline if **ANY** of these apply:

### One-Time Use
- Logic specific to single unique situation
- Not reusable in any other context
- Effort to extract > effort to keep inline

### Tightly Coupled to Context
- Depends heavily on current conversation state
- References information only available in this session
- Loses meaning when separated from context

### Requires Real-Time Interaction
- User provides input during execution
- Decisions require clarification questions
- Iterative refinement based on feedback

### Simple Enough to Repeat
- <100 tokens of instructions
- Obvious pattern that's quick to write out
- Extraction overhead not worth minimal reuse benefit

### Exploratory/Experimental
- Still figuring out the right approach
- Likely to change significantly
- Not ready for standardization

## Decision Examples

### Example 1: Code Review Workflow

**Context:** Need to review code for quality, security, performance, and tests.

**Evaluation:**

Prompt extraction criteria:
- [x] Reusability - Used for every PR (many contexts)
- [x] Prompt techniques - Needs examples for consistency, structured CoT
- [x] Guardrails - Consistency in reviews important
- [x] Context optimization - Could cache review guidelines
- [x] Standardization - Team needs uniform review standards
- [x] Complexity - Multi-phase: scan → analyze → recommend

**Score: 6/6**

Script extraction criteria:
- [ ] Deterministic - Requires judgment
- [ ] Computation-heavy - Mostly reasoning, not computation
- [ ] Testable - Subjective quality assessment
- [ ] Reusable across prompts - Specific to code review
- [ ] No reasoning - Definitely requires reasoning
- [ ] Format conversion - Not applicable

**Score: 0/6**

**Decision: Extract to prompt template** ✓

---

### Example 2: Email Validation

**Context:** Need to validate email addresses match proper format.

**Evaluation:**

Prompt extraction criteria:
- [ ] Reusability - Yes, but simple enough for script
- [ ] Prompt techniques - No examples needed, simple pattern
- [ ] Guardrails - Not needed for format validation
- [ ] Context optimization - Not applicable, tiny input
- [ ] Standardization - Standard regex handles this
- [ ] Complexity - Very simple, single step

**Score: 0/6**

Script extraction criteria:
- [x] Deterministic - Same email always validates same way
- [ ] Computation-heavy - Simple regex matching
- [x] Testable - Clear pass/fail criteria
- [x] Reusable across prompts - Many prompts need email validation
- [x] No reasoning - Pure pattern matching
- [x] Format conversion - Validation is format checking

**Score: 5/6**

**Decision: Extract to script** ✓

---

### Example 3: Customer Sentiment Analysis

**Context:** Classify customer feedback as positive/negative/neutral with confidence.

**Evaluation:**

Prompt extraction criteria:
- [x] Reusability - Used for all customer feedback
- [x] Prompt techniques - Needs 3-5 examples for edge cases
- [x] Guardrails - Consistency across all analyses important
- [ ] Context optimization - Small inputs, no optimization needed
- [x] Standardization - Team needs consistent classification
- [ ] Complexity - Relatively simple classification

**Score: 4/6**

Script extraction criteria:
- [ ] Deterministic - Requires judgment and context
- [ ] Computation-heavy - Text understanding, not computation
- [ ] Testable - Fuzzy boundaries (is "it's okay" neutral or slightly positive?)
- [ ] Reusable across prompts - Specific to sentiment
- [ ] No reasoning - Definitely requires reasoning
- [ ] Format conversion - Not applicable

**Score: 0/6**

**Decision: Extract to prompt template** ✓

---

### Example 4: One-Time Data Migration

**Context:** Need to transform old database records to new schema for migration.

**Evaluation:**

Prompt extraction criteria:
- [ ] Reusability - One-time migration
- [ ] Prompt techniques - Straightforward transformation
- [ ] Guardrails - Not needed for one-time use
- [ ] Context optimization - N/A
- [ ] Standardization - Not needed for one-time task
- [ ] Complexity - Migration logic is simple

**Score: 0/6**

Script extraction criteria:
- [x] Deterministic - Clear field mapping rules
- [x] Computation-heavy - Processing thousands of records
- [x] Testable - Can test transformation logic
- [ ] Reusable across prompts - One-time migration
- [x] No reasoning - Mechanical field mapping
- [x] Format conversion - Schema transformation

**Score: 5/6** - But wait...

**Override consideration:** Despite high script score, this is ONE-TIME USE.

**Decision: Keep inline or use simple script** - Effort to create robust, reusable script not worth it for one-time task. Simple inline Python or one-off script is fine.

---

### Example 5: Creative Writing Assistant

**Context:** Help user brainstorm and develop creative story ideas.

**Evaluation:**

Prompt extraction criteria:
- [ ] Reusability - Each story is unique, prompts would vary
- [ ] Prompt techniques - Freeform, doesn't need structured examples
- [ ] Guardrails - Creative freedom desired, not restricted
- [ ] Context optimization - N/A
- [ ] Standardization - Anti-goal (want variety and creativity)
- [ ] Complexity - Conversational, exploratory

**Score: 0/6**

Script extraction criteria:
- [ ] Deterministic - Highly creative and variable
- [ ] Computation-heavy - Conceptual ideation
- [ ] Testable - Subjective creative quality
- [ ] Reusable across prompts - Each story different
- [ ] No reasoning - Requires deep creative reasoning
- [ ] Format conversion - Not applicable

**Score: 0/6**

**Decision: Keep inline** ✓ - Conversational, exploratory, benefits from context and iteration.

## Combined Extraction Strategy

Sometimes logic has both prompt and script components.

**Example: Contract Analysis System**

**Workflow:**
1. Extract terms from contract (prompt - requires understanding)
2. Validate extracted terms against schema (script - deterministic)
3. Analyze risks for each term (prompt - requires judgment)
4. Format analysis into report (script - template rendering)

**Implementation:**
- Prompt template 1: Term extraction with examples
- Python script: Schema validation
- Prompt template 2: Risk analysis with CoT
- Python script: Report formatter

**Benefit:** Each component uses appropriate tool (Claude for reasoning, script for mechanics).

## Quick Reference Decision Chart

| Characteristic | Extract to Prompt | Extract to Script | Keep Inline |
|----------------|-------------------|-------------------|-------------|
| Reusable across contexts | ✓ | ✓ | ✗ |
| Requires judgment/reasoning | ✓ | ✗ | Either |
| Deterministic/algorithmic | ✗ | ✓ | Either |
| Needs examples for quality | ✓ | ✗ | ✗ |
| Computation-heavy | ✗ | ✓ | ✗ |
| Has unit test cases | ✗ | ✓ | ✗ |
| Needs guardrails | ✓ | ✗ | ✗ |
| Context optimization needed | ✓ | ✗ | ✗ |
| One-time use | ✗ | ✗ | ✓ |
| Tightly coupled to current context | ✗ | ✗ | ✓ |
| Exploratory/experimental | ✗ | ✗ | ✓ |

## Extraction Process

### For Prompt Extraction:

1. **Identify reusable pattern** - What varies vs what's constant?
2. **Define template variables** - Mark dynamic inputs with {{VARIABLE}}
3. **Create core instructions** - Write reusable instruction set
4. **Add examples** - Include 3-5 diverse, high-quality examples
5. **Implement guardrails** - Add appropriate safeguards
6. **Optimize context** - Implement caching if applicable
7. **Document usage** - Clear examples of how to use template
8. **Test across contexts** - Verify works in different scenarios

### For Script Extraction:

1. **Define interface** - Clear inputs and outputs
2. **Implement logic** - Write deterministic algorithm
3. **Add error handling** - Handle edge cases and failures
4. **Write unit tests** - Comprehensive test coverage
5. **Document API** - Docstrings and usage examples
6. **Optimize performance** - If computation-heavy
7. **Make reusable** - Generic enough for multiple contexts
8. **Integration points** - How prompts will call this script

## When to Refactor Existing Inline Logic

Refactor from inline to extracted when:

**For prompts:**
- Used same logic 3+ times across conversations
- Team members duplicating similar prompts
- Quality inconsistent without structured template
- Context optimization would save significant tokens

**For scripts:**
- Same calculation repeated in multiple prompts
- Inline logic causing prompt bloat (>200 tokens)
- Testing needed but prompts not easily testable
- Performance issues with prompt-based processing

**Don't refactor if:**
- Used <3 times and unlikely to be reused more
- Extraction effort > maintenance effort of inline
- Logic still evolving and extraction would add rigidity
- Context-specific and loses meaning when extracted
