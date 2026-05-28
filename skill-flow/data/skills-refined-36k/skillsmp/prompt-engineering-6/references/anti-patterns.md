# Prompt Anti-Patterns

Common mistakes and how to fix them. Load this file when debugging prompts.

## 1. Vague Instructions

**Bad:**
```
Write a good summary
```

**Why it fails:** "Good" is subjective. Claude interprets differently each time.

**Good:**
```
Write a 3-paragraph summary (150-200 words) covering:
1. Main findings
2. Methodology
3. Implications
```

**Fix pattern:** Replace adjectives with measurable criteria.

---

## 2. Missing Format Specification

**Bad:**
```
List the results
```

**Why it fails:** Could be bullets, numbered list, table, JSON, prose.

**Good:**
```
List results in JSON format:
{
  "id": number,
  "name": string,
  "status": "active" | "inactive"
}
```

**Fix pattern:** Always specify exact output structure with example.

---

## 3. Ambiguous Constraints

**Bad:**
```
Be creative but professional
```

**Why it fails:** These terms mean different things to different people.

**Good:**
```
Use creative analogies to explain complex concepts.
Maintain professional language:
- No slang or colloquialisms
- Proper grammar and punctuation
- Cite sources when making claims
```

**Fix pattern:** Define each constraint with specific behaviors.

---

## 4. Over-Engineering Simple Tasks

**Bad:**
```
Using Tree-of-Thoughts pattern to list files in a directory
```

**Why it fails:** Adds latency and complexity for no benefit.

**Good:**
```
Use bash to list all .py files in /src/
```

**Fix pattern:** Match technique complexity to task complexity.

| Task Complexity | Appropriate Technique |
|-----------------|----------------------|
| Simple lookup | Zero-shot |
| Pattern matching | Few-shot (2-3 examples) |
| Reasoning needed | CoT |
| Exploration needed | ToT |

---

## 5. Underspecifying Complex Tasks

**Bad:**
```
Analyze this codebase for issues
```

**Why it fails:** No structure for systematic analysis.

**Good:**
```
Analyze this codebase using this checklist:

<thinking>
1. Security: Check for OWASP Top 10
2. Performance: Identify O(n²) or worse algorithms
3. Maintainability: Find code duplication > 10 lines
4. Testing: Calculate coverage gaps
</thinking>

For each issue found:
- File:line reference
- Severity (Critical/High/Medium/Low)
- Specific remediation
```

**Fix pattern:** Add CoT structure with explicit checklist.

---

## 6. Inconsistent Few-Shot Examples

**Bad:**
```
Example 1: "The movie was great" -> Positive
Example 2: Input: "I hated it" Output: negative
Example 3: Text="Meh" | Sentiment=Neutral
```

**Why it fails:** Claude learns the pattern, but pattern is inconsistent.

**Good:**
```
Example 1:
Input: "The movie was great"
Output: Positive

Example 2:
Input: "I hated it"
Output: Negative

Example 3:
Input: "Meh"
Output: Neutral
```

**Fix pattern:** All examples must have identical structure.

---

## 7. No Length Boundaries

**Bad:**
```
Explain this concept
```

**Why it fails:** Claude can be verbose. You might get 500 words when you wanted 50.

**Good:**
```
Explain this concept in exactly 5 bullet points, each under 20 words
```

**Fix pattern:** Always specify: word count, bullet count, paragraph count, or character limit.

| Boundary Type | Example |
|---------------|---------|
| Word count | "maximum 200 words" |
| Bullet count | "exactly 5 bullet points" |
| Paragraph count | "in 2-3 paragraphs" |
| Character limit | "under 280 characters" |

---

## 8. Assuming Context Awareness

**Bad:**
```
Fix the bug
```

**Why it fails:** Which bug? In which file? What's the expected behavior?

**Good:**
```
Fix the bug in `calculate_total()` at src/billing.py:42
Issue: Division by zero when cart is empty
Expected: Return 0 when cart has no items
```

**Fix pattern:** Be explicit about: location, current behavior, expected behavior.

---

## 9. No Validation Mechanism

**Bad:**
```
Generate code for the feature
```

**Why it fails:** No quality check. Errors propagate.

**Good:**
```
Generate code for the feature, then:
1. Verify it compiles/runs without errors
2. Check it handles these edge cases: [list]
3. Confirm it follows our style guide: [link]
4. List any assumptions you made
```

**Fix pattern:** Add explicit validation steps to the prompt.

---

## 10. Same Prompt for All Models

**Bad:**
Using XML-heavy prompts for GPT-4, or CoT for o1.

**Why it fails:** Each model has different optimal patterns.

**Model-Specific Guidance:**

| Model | Optimization |
|-------|--------------|
| Claude | XML tags, explicit structure, be very literal |
| GPT-4 | Bookend critical instructions (start + end) |
| GPT-4.1 | Even more literal than 4, repeat constraints |
| o1/o3 | NO CoT (built-in reasoning), just state problem |
| Gemini | Numbered steps, explicit formatting |

**Fix pattern:** Know your model's preferences.

---

## 11. Agent Ignores Constraints

**Bad:**
```
Don't include code examples.
[long instructions]
```

**Why it fails:** Constraint buried, easily forgotten.

**Good:**
```
IMPORTANT: Do NOT include any code examples.

[long instructions]

Remember: No code examples in your response.
```

Plus use XML:
```xml
<constraints>
- No code examples
- Maximum 500 words
- Professional tone only
</constraints>
```

**Fix pattern:** Bookend + XML tags + repeat critical constraints.

---

## 12. Agent Hallucinates Facts

**Bad:**
```
What are the revenue figures for Company X?
```

**Why it fails:** No grounding. Claude may invent numbers.

**Good:**
```
Based ONLY on the document below, what are the revenue figures?
If the information is not in the document, respond "Not found in source."

<document>
[actual document content]
</document>
```

**Fix pattern:**
1. Provide source material
2. Explicit instruction to use only provided info
3. Define fallback for missing info

---

## Troubleshooting Quick Reference

| Symptom | Likely Cause | Quick Fix |
|---------|--------------|-----------|
| Inconsistent output | Vague instructions | Add explicit format + example |
| Too verbose | No length limit | Add "exactly X bullets" |
| Misses requirements | Instructions buried | Bookend critical points |
| Unclear reasoning | No CoT structure | Add `<thinking>` tags |
| Few-shot ignored | Inconsistent examples | Standardize all examples |
| Wrong decisions | Unclear boundaries | Add "Can/Cannot decide" lists |
| Ignores constraints | Not explicit enough | Bookend + XML + repeat |
| Makes up facts | No grounding | Provide source + "only use this" |
| Over-complicated | Wrong technique | Match technique to task complexity |
| Under-analyzed | No structure | Add CoT or checklist |
