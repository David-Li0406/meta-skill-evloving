# Claude 3 → Claude 4.5 Migration Guide

Update patterns for migrating prompts from Claude 3 to Claude 4.5 models.

## Key Behavioral Differences

### Claude 4.5 Characteristics

**More explicit instruction following:**
- Examines details closely
- Follows instructions precisely (including unintended patterns in examples)
- Requires more specificity than Claude 3
- Less likely to "read between the lines"

**Better at:**
- Long-horizon reasoning and state tracking
- Recognizing delegation opportunities
- Parallel tool execution
- Multi-window workflows with file-based state

**Different defaults:**
- More concise, fact-based communication
- Less verbose without explicit requests
- Won't provide summaries unless asked
- More direct, fewer preambles

**New capabilities:**
- Context awareness (knows remaining token budget)
- Extended thinking support
- Better subagent orchestration

## Migration Patterns

### Pattern 1: Increase Instruction Specificity

**Claude 3 prompt (worked with implicit expectations):**
```
Analyze this code and improve it.

{{CODE}}
```

**Claude 4.5 prompt (needs explicit requirements):**
```
Analyze this code and improve it.

Specific improvements to make:
1. Performance optimization (identify O(n²) or worse, suggest better algorithms)
2. Readability (clear variable names, appropriate comments, logical structure)
3. Error handling (catch edge cases, validate inputs, handle failures gracefully)
4. Security (check for SQL injection, XSS, input validation issues)

For each improvement:
- Explain what's suboptimal and why
- Provide specific improved code
- Describe the benefit of the change

{{CODE}}
```

**Rationale:** Claude 4.5 needs explicit scope. "Improve it" is too vague.

---

### Pattern 2: Add Contextual Motivation

**Claude 3 prompt:**
```
Extract email addresses from the text and output as JSON array.

{{TEXT}}
```

**Claude 4.5 prompt:**
```
Extract email addresses from the text and output as JSON array.

Context: These emails will be added to a mailing list for product updates. Accuracy
is critical - false positives waste sending resources, false negatives miss potential
customers. Err on the side of precision (only include valid emails) over recall.

{{TEXT}}
```

**Rationale:** Claude 4.5 generalizes better when it understands *why* requirements matter.

---

### Pattern 3: Ensure Example Quality Alignment

**Claude 3 prompt (examples with inconsistent details):**
```
<examples>
<example>
Input: "Great product!"
Output: {"sentiment": "positive", "confidence": "high"}
</example>
<example>
Input: "It's okay I guess"
Output: {"sentiment": "neutral", "confidence": "medium", "note": "Lukewarm response"}
</example>
</examples>
```

**Problem for Claude 4.5:** Second example has "note" field, first doesn't. Claude 4.5 examines examples closely and might add "note" inconsistently.

**Claude 4.5 prompt (consistent examples):**
```
<examples>
<example>
Input: "Great product!"
Output: {"sentiment": "positive", "confidence": "high"}
</example>
<example>
Input: "It's okay I guess"
Output: {"sentiment": "neutral", "confidence": "medium"}
</example>
<example>
Input: "Terrible experience, very disappointed"
Output: {"sentiment": "negative", "confidence": "high"}
</example>
</examples>
```

**Rationale:** Claude 4.5 closely examines example details. Ensure all examples follow identical structure.

---

### Pattern 4: Request Summaries Explicitly

**Claude 3 prompt (got verbose updates automatically):**
```
Research the following topic and compile findings:
{{RESEARCH_TOPIC}}
```

Claude 3 output included:
- "Let me start by searching for information about X..."
- "I've found several relevant sources. Now I'll analyze..."
- "Based on my research, here are the key findings..."

**Claude 4.5 prompt (needs explicit request for progress updates):**
```
Research the following topic and compile findings:
{{RESEARCH_TOPIC}}

Process:
1. Search for relevant sources (summarize what you find before proceeding)
2. Analyze the information (explain your analytical approach)
3. Synthesize key findings (provide final summary)

For each step, explain what you're doing before moving to the next step. This helps
track progress and ensures thoroughness.
```

**Rationale:** Claude 4.5 defaults to more concise output. Request summaries explicitly.

---

### Pattern 5: Use Action Framing Over Suggestion Framing

**Claude 3 prompt (suggestion framing worked):**
```
Can you help me improve this function's performance?

{{CODE}}
```

Claude 3 understood this as "please improve the code."

**Claude 4.5 prompt (action framing clearer):**
```
Improve this function's performance.

Optimize for:
- Time complexity (target O(n) or better)
- Memory efficiency
- Readability maintenance

Provide the optimized code with explanation of improvements.

{{CODE}}
```

**Rationale:** Claude 4.5 interprets "Can you help" literally (might suggest approaches rather than implementing). Use imperative voice for implementation requests.

---

### Pattern 6: Add Quality Modifiers for Creative Tasks

**Claude 3 prompt:**
```
Design a landing page for a SaaS product.

Features:
- Hero section
- Feature showcase
- Pricing
- Call-to-action

{{PRODUCT_DETAILS}}
```

**Claude 4.5 prompt:**
```
Design a landing page for a SaaS product. Don't hold back - give it your all.

Requirements:
- Hero section with compelling headline and visual
- Feature showcase highlighting key benefits
- Pricing table with clear tiers
- Strong call-to-action

Design direction:
- Modern, clean aesthetic
- Professional but approachable
- Use color palette: [specify colors]
- Include micro-interactions and subtle animations
- Mobile-responsive layout

Create a polished, production-ready design that showcases the product beautifully.

{{PRODUCT_DETAILS}}
```

**Rationale:** Claude 4.5 needs explicit encouragement for "above and beyond" quality.

---

### Pattern 7: Guide Parallel Tool Execution

**Claude 3 prompt (parallel execution happened implicitly):**
```
Search for information about [Topic A], [Topic B], and [Topic C], then synthesize
findings.
```

**Claude 4.5 prompt (explicit parallel guidance):**
```
Search for information about [Topic A], [Topic B], and [Topic C], then synthesize
findings.

Tool usage optimization: Run searches in parallel rather than sequentially. Execute
all three searches simultaneously using multiple tool calls in one message for faster
results.

After all searches complete, synthesize the findings.
```

**Rationale:** Claude 4.5 supports parallel execution but benefits from explicit guidance.

---

### Pattern 8: Leverage Context Awareness

**Claude 3 prompt (no context budget guidance):**
```
Analyze these documents and extract key information:
{{LARGE_DOCUMENTS}}
```

**Claude 4.5 prompt (leverages context awareness):**
```
Analyze these documents and extract key information.

Note: You have access to {{CONTEXT_SIZE}} tokens. Use the full context window
effectively - don't stop prematurely due to perceived space constraints. Track your
progress and utilize available capacity completely.

If approaching limits, note what remains and we can continue in a follow-up session.

{{LARGE_DOCUMENTS}}
```

**Rationale:** Claude 4.5 knows its remaining token budget. Reference this to prevent premature stopping.

---

### Pattern 9: Enable Multi-Window Workflows

**Claude 3 prompt (single-window assumption):**
```
Implement comprehensive test coverage for this module.

{{MODULE_CODE}}
```

**Claude 4.5 initial prompt (multi-window strategy):**
```
Implement comprehensive test coverage for this module. This is a multi-session task.

Session 1 objectives:
1. Analyze module structure and identify testable components
2. Create test plan with priorities
3. Begin implementing high-priority tests
4. Save progress to test-progress.json before session ends

State management:
- Create/update test-progress.json with:
  - Components analyzed
  - Tests implemented
  - Coverage percentage
  - Next steps
- We'll continue in subsequent sessions using the state file

Focus on thorough testing, not rushing. Use full context window available.

{{MODULE_CODE}}
```

**Claude 4.5 continuation prompt:**
```
Continue implementing test coverage from previous session.

1. Load test-progress.json
2. Review completed tests and remaining work
3. Implement next priority test files
4. Update progress file with new state

{{MODULE_CODE}}
```

**Rationale:** Claude 4.5 excels at multi-window workflows with file-based state persistence.

---

### Pattern 10: Subagent Delegation Guidance

**Claude 3 prompt (no subagent concept):**
```
You are a lead agent coordinating research. When you need information, use available
tools to gather it yourself.
```

**Claude 4.5 prompt (leverages delegation recognition):**
```
You are a lead agent coordinating research. Your role is strategic coordination and
synthesis, not direct information gathering.

Subagent orchestration:
- You have access to specialized research subagents via the delegate_research tool
- When you need information gathered, invoke subagents with clear objectives
- Run multiple subagents in parallel for independent research threads
- Your focus: breaking down questions, coordinating work, synthesizing results

Don't try to do all research yourself. Delegate effectively and focus on high-level
coordination and synthesis.
```

**Rationale:** Claude 4.5 recognizes delegation opportunities. Encourage this behavior explicitly.

## Comprehensive Migration Checklist

When migrating a Claude 3 prompt to Claude 4.5, evaluate:

### Specificity
- [ ] Instructions explicit enough? (Add concrete requirements)
- [ ] Success criteria defined? (State what "good" looks like)
- [ ] Output format specified precisely? (Don't assume implied structure)
- [ ] Edge cases covered? (Claude 4.5 follows instructions literally)

### Context & Motivation
- [ ] Added reasoning for why requirements matter?
- [ ] Explained use case and impact?
- [ ] Provided background that aids generalization?

### Examples
- [ ] All examples structurally identical?
- [ ] Cover diverse scenarios?
- [ ] No unintended patterns Claude might follow?
- [ ] Quality appropriate for task complexity?

### Communication Style
- [ ] Using action framing for implementation requests?
- [ ] Added explicit requests for summaries/progress updates?
- [ ] Included quality modifiers for creative tasks?
- [ ] Specified desired verbosity level?

### Advanced Capabilities
- [ ] Leveraging context awareness? (Reference token budget)
- [ ] Guiding parallel tool execution where applicable?
- [ ] Using multi-window workflow if task >100K tokens?
- [ ] Encouraging subagent delegation for agent prompts?

### Examples
- [ ] Structurally consistent?
- [ ] Adequate diversity (3-5 for complex tasks)?
- [ ] No unintended details Claude might copy?

## Common Issues After Migration

### Issue 1: Output Too Concise

**Symptom:** Claude 4.5 provides minimal explanation where Claude 3 was verbose.

**Solution:**
```
Add to prompt:
"Provide detailed explanations for your recommendations. For each suggestion, explain:
- What the issue is
- Why it matters
- How your solution addresses it
- What the impact of the change will be"
```

---

### Issue 2: Stops Too Early in Long Tasks

**Symptom:** Claude 4.5 completes less work than Claude 3 did.

**Solution:**
```
Add to prompt:
"You have access to [X] tokens in this context window. Use the full capacity
available - don't stop prematurely. If approaching limits, save state and indicate
what remains for continuation."
```

---

### Issue 3: Follows Examples Too Literally

**Symptom:** Copies specific details from examples that shouldn't be replicated.

**Solution:** Audit examples for:
- Inconsistent fields between examples
- Placeholder values that should vary
- Specific numbers/dates that are example-specific
- Format variations across examples

Ensure all examples follow identical structure with appropriate variation only in content.

---

### Issue 4: Doesn't Implement, Just Suggests

**Symptom:** Claude 4.5 provides recommendations rather than implementing changes.

**Solution:** Change framing:
- Before: "Can you improve this code?"
- After: "Improve this code by [specific optimizations]. Provide the complete optimized implementation."

---

### Issue 5: Less Creative Than Expected

**Symptom:** Outputs are functional but lack polish or creativity.

**Solution:**
```
Add quality modifiers:
"Don't hold back - give it your all. Create a polished, production-ready [output]
that showcases [quality attributes]. Be creative and thorough."
```

## Testing Migration Success

After migrating a prompt, test with:

1. **Original test cases:** Ensure outputs still meet requirements
2. **Edge cases:** Verify Claude 4.5 handles unusual inputs appropriately
3. **Multiple runs:** Check consistency across iterations
4. **Quality comparison:** Assess if outputs match or exceed Claude 3 quality
5. **Token efficiency:** Measure if changes reduced unnecessary tokens

**Success criteria:**
- Quality maintained or improved ✓
- Consistency equal or better ✓
- Handles edge cases appropriately ✓
- Leverages Claude 4.5 capabilities ✓
- No unintended behavioral changes ✓

## Quick Migration Template

```
Claude 3 prompt:
[Original prompt]

Migration checklist:
□ Made instructions more explicit
□ Added contextual motivation
□ Ensured example consistency
□ Added summary requests if needed
□ Changed suggestion → action framing
□ Added quality modifiers for creative tasks
□ Added parallel execution guidance if applicable
□ Leveraged context awareness if applicable
□ Enabled multi-window workflow if needed
□ Added subagent delegation guidance if applicable

Claude 4.5 prompt:
[Migrated prompt]

Testing notes:
- Test case 1: [Result]
- Test case 2: [Result]
- Edge case handling: [Assessment]
- Quality comparison: [Assessment]
```

Use this template to systematically migrate and validate prompts.
