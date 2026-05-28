# Targeted Research Workflow

For when you already know exactly what dimensions to research.

<when_to_use>
- User specifies exact topics to cover
- Follow-up research on known gaps
- Structured comparison requests
</when_to_use>

<process>
1. **User-Defined Topics**
   - Skip brief generation
   - Use user's specified dimensions directly
   - Spawn one worker per dimension

2. **Standard Synthesis**
   - Merge findings normally
   - Optional gap detection (ask user)

3. **Structured Output**
   - Organized by user's dimensions
   - Direct answers to each specified area
</process>

<example>
User: "Compare these three approaches: X, Y, Z"

Workers:
1. Research approach X
2. Research approach Y
3. Research approach Z

Output:
| Aspect | X | Y | Z |
|--------|---|---|---|
| [Comparison points] |
</example>
