---
name: health-context
description: Retrieve health history for informed decisions. Use when discussing medications, supplements, skincare, diet, fitness, or any health-related product evaluation.
allowed-tools: mcp__aiii__recall_memories
---

# Health Context

Retrieve relevant health history before providing health-related advice or evaluations.

## When to Use

- User asks about medications or supplements
- User is evaluating health/skincare products
- User mentions diet or fitness questions
- User asks about potential interactions
- Any health-related decision that could benefit from personal context

## Important Disclaimer

Always remind users that this is contextual information from their own records, not medical advice. Recommend consulting healthcare professionals for medical decisions.

## Instructions

1. **Identify the health topic**:
   - Medications and supplements
   - Allergies and sensitivities
   - Skin conditions or concerns
   - Dietary preferences or restrictions
   - Fitness goals or limitations

2. **Query Health space**:

   ```json
   {
     "query": "relevant health terms",
     "space_id": "health_space_id",
     "limit": 10
   }
   ```

3. **Look for relevant context**:
   - Known allergies or sensitivities
   - Current medications/supplements
   - Past discussions about similar topics
   - Stated preferences or concerns
   - Previous reactions or experiences

4. **Present context before advice**:

   ```
   Based on your health notes:
   - You mentioned sensitive skin (Nov 2025)
   - You're currently taking vitamin D (Dec 2025)
   - You had a reaction to retinol previously (Oct 2025)

   With this in mind...
   ```

5. **Flag potential concerns**:
   - Possible interactions
   - Contradictions with stated preferences
   - Similar products that caused issues

6. **Provide informed response**:
   - Reference the relevant context
   - Explain how it affects the recommendation
   - Suggest alternatives if concerns found

## Example Interaction

**User:** "Is this retinol serum safe for me?"

**Claude:**

1. Identifies: skincare, retinol
2. Queries Health space for: retinol, skin, sensitivity, allergies
3. Finds: "User mentioned sensitive skin", "Had reaction to retinol before"
4. Presents context:
   > "Based on your health notes, you mentioned having sensitive skin and a previous reaction to retinol (Oct 2025). Given this history, I'd recommend..."
5. Provides cautious recommendation with alternatives

## No Health Context

If no relevant health memories found:

1. State that no relevant health history was found
2. Ask clarifying questions about relevant health factors
3. Provide general guidance with appropriate caveats
4. Suggest saving the discussion to Health space for future reference
