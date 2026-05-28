# Few-Shot

Pattern learning through examples. Use 2-8 consistent examples.

## Template

```markdown
Task: [What to do]

<examples>
Input: [Example 1 input]
Output: [Example 1 output]

Input: [Example 2 input]
Output: [Example 2 output]

Input: [Example 3 input]
Output: [Example 3 output]
</examples>

Your turn:
Input: [Actual input]
Output:
```

## Critical Rules

1. **All examples must be identical in structure**
2. Use 2-8 examples (3 is usually enough)
3. Cover edge cases in examples
4. Examples should be realistic, not trivial

## Example

```markdown
Task: Extract company funding info as JSON

<examples>
Input: "Acme Corp raised $50M Series B from Sequoia"
Output: {"company": "Acme Corp", "amount": 50000000, "round": "Series B", "investor": "Sequoia"}

Input: "London startup TechFlow secured £30M from Balderton"
Output: {"company": "TechFlow", "amount": 30000000, "round": null, "investor": "Balderton"}

Input: "Stealth AI company got $15M seed, investors undisclosed"
Output: {"company": null, "amount": 15000000, "round": "seed", "investor": null}
</examples>

Your turn:
Input: [press release text]
Output:
```

## When NOT to Use

- Simple direct task → Use Zero-shot
- Need to show reasoning → Use CoT
- No good examples available → Use Role-based
