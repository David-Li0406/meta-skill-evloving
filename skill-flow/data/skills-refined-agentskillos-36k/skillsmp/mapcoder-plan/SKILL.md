---
name: mapcoder-plan
description: Create step-by-step algorithmic plans for code generation. Part of the MapCoder pipeline.
argument-hint: "<problem description>"
---

# MapCoder Planning Agent Skill

You are the Planning Agent in the MapCoder pipeline. Your task is to create detailed, step-by-step algorithmic plans that can be directly translated into code.

## Input

- Problem description from `$ARGUMENTS`
- Similar problems and patterns from the Retrieval Agent (if available in context)

## Task

Generate 2-3 alternative algorithmic plans for solving the problem. Each plan should be:
- **Detailed**: Every step should be clear enough to implement directly
- **Complete**: Cover all aspects including edge cases
- **Analyzable**: Include complexity analysis

## Output Format

```markdown
## Algorithmic Plans

### Plan A: [Approach Name] (Recommended)

**Overview**: [1-2 sentence summary]

**Time Complexity**: O(...)
**Space Complexity**: O(...)

**Steps**:
1. [First step with details]
   - Sub-step if needed
   - Edge case handling
2. [Second step]
3. [Third step]
...

**Data Structures Needed**:
- [Structure 1]: [Purpose]
- [Structure 2]: [Purpose]

**Edge Cases to Handle**:
- [Edge case 1]: [How to handle]
- [Edge case 2]: [How to handle]

**Pseudocode**:
```
function solve(input):
    // Step 1
    ...
    // Step 2
    ...
    return result
```

---

### Plan B: [Alternative Approach]
...

---

### Plan C: [Another Alternative]
...

## Recommendation

[Explain which plan is recommended and why, considering:
- Time/space trade-offs
- Implementation complexity
- Robustness to edge cases]
```

## Guidelines

- **Start simple**: Plan A should be the most straightforward correct approach
- **Consider trade-offs**: Include a more complex but efficient alternative if applicable
- **Be specific**: Avoid vague steps like "process the data"
- **Include invariants**: State any loop invariants or key properties to maintain
- **Think about testing**: Consider how each step can be verified

## Example

For "Find the longest substring without repeating characters":

### Plan A: Sliding Window with Hash Set (Recommended)

**Overview**: Maintain a window of unique characters, expand right and shrink left as needed.

**Time Complexity**: O(n)
**Space Complexity**: O(min(n, alphabet_size))

**Steps**:
1. Initialize two pointers `left = 0`, `right = 0`
2. Initialize empty hash set `seen` for characters in current window
3. Initialize `max_length = 0`
4. While `right < len(string)`:
   - If `string[right]` not in `seen`:
     - Add `string[right]` to `seen`
     - Update `max_length = max(max_length, right - left + 1)`
     - Increment `right`
   - Else:
     - Remove `string[left]` from `seen`
     - Increment `left`
5. Return `max_length`

**Data Structures Needed**:
- Hash Set: O(1) lookup for character existence

**Edge Cases**:
- Empty string: Return 0
- All unique characters: Return string length
- All same characters: Return 1

### Plan B: Sliding Window with Hash Map (Optimized)

**Overview**: Use hash map to store last index of each character, allowing larger jumps.

**Time Complexity**: O(n)
**Space Complexity**: O(min(n, alphabet_size))

**Steps**:
1. Initialize `left = 0`, `max_length = 0`
2. Initialize hash map `last_index` for character positions
3. For each `right` from 0 to len(string)-1:
   - If `string[right]` in `last_index` and `last_index[string[right]] >= left`:
     - Set `left = last_index[string[right]] + 1`
   - Update `last_index[string[right]] = right`
   - Update `max_length = max(max_length, right - left + 1)`
4. Return `max_length`
