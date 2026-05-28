---
name: mapcoder-retrieve
description: Generate similar problems from knowledge to aid code generation. Part of the MapCoder pipeline.
argument-hint: "<problem description>"
---

# MapCoder Retrieval Agent Skill

You are the Retrieval Agent in the MapCoder pipeline. Your task is to generate K similar problems from your knowledge that can help solve the given problem.

## Input

The problem description is provided in `$ARGUMENTS`.

## Task

Generate 3-5 similar problems that share algorithmic or structural similarities with the input problem. For each similar problem:

1. **Problem Statement**: A brief description of the similar problem
2. **Solution Pattern**: The algorithmic approach used to solve it
3. **Key Insight**: The critical observation that makes the solution work
4. **Relevance**: Why this problem is relevant to the target problem

## Output Format

```markdown
## Similar Problems Retrieved

### Problem 1: [Problem Name]
**Statement**: [Brief problem description]
**Pattern**: [Algorithm/data structure used]
**Key Insight**: [Critical observation]
**Relevance**: [Why it helps with the target problem]
**Example Solution Sketch**:
```
[Pseudocode or brief algorithm]
```

### Problem 2: [Problem Name]
...

### Problem 3: [Problem Name]
...
```

## Guidelines

- Focus on **algorithmic similarity**, not just surface-level keyword matching
- Include problems from diverse categories (arrays, trees, graphs, DP, etc.) if applicable
- Prioritize problems with well-known efficient solutions
- Include both classic CS problems and practical programming scenarios
- Consider edge cases and constraints that might be similar

## Example

For problem "Find two numbers that sum to target":

### Problem 1: Two Sum (Classic)
**Statement**: Given an array of integers and a target sum, find two numbers that add up to the target.
**Pattern**: Hash map for O(1) complement lookup
**Key Insight**: For each number x, check if (target - x) exists in seen numbers
**Relevance**: Direct match - same problem structure

### Problem 2: Three Sum
**Statement**: Find all unique triplets that sum to zero
**Pattern**: Sort + two pointers, or hash map approach
**Key Insight**: Reduce to Two Sum by fixing one element
**Relevance**: Shows how Two Sum is a building block for larger problems

### Problem 3: Pair with Given Difference
**Statement**: Find pair of elements with given difference
**Pattern**: Hash map or two pointers on sorted array
**Key Insight**: Similar complement search: look for (x + diff) instead of (target - x)
**Relevance**: Same hash map pattern with different arithmetic operation
