# Chain-of-Thought (CoT)

Explicit step-by-step reasoning. Shows logical process.

## Template

```markdown
Task: [What to do]

Think step by step:
<thinking>
Step 1: [Analysis]
Step 2: [Reasoning]
Step 3: [Conclusion]
</thinking>

<answer>
[Final result]
</answer>
```

## Example

```markdown
Task: Should we approve this loan application?

Applicant:
- Income: $75,000/year
- Debt: $15,000
- Credit score: 720
- Loan requested: $25,000

Think step by step:
<thinking>
Step 1: Calculate debt-to-income ratio
- Current debt: $15,000
- Annual income: $75,000
- DTI: 15,000 / 75,000 = 20%

Step 2: Assess credit worthiness
- Score 720 is "Good" (670-739 range)
- Above minimum threshold of 650

Step 3: Evaluate loan impact
- New total debt: $15,000 + $25,000 = $40,000
- New DTI: 40,000 / 75,000 = 53%
- This exceeds 43% guideline

Step 4: Make decision
- Credit score acceptable
- But new DTI too high
- Risk: borrower may struggle with payments
</thinking>

<answer>
DECLINE. While credit score is acceptable (720), the post-loan debt-to-income ratio of 53% exceeds our 43% threshold. Recommend applicant reduce existing debt or request smaller loan amount.
</answer>
```

## When to Use

- Math problems
- Logical deductions
- Multi-step analysis
- Debugging
- Decision-making with criteria

## When NOT to Use

- Simple lookups (overkill)
- Creative tasks (constrains creativity)
- o1/o3 models (they have built-in reasoning)
