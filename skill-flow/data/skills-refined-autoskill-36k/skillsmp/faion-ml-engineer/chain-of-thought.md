---
id: chain-of-thought
name: "Chain-of-Thought"
domain: ML
skill: faion-ml-engineer
category: "ml-engineering"
---

# Chain-of-Thought

## Overview

Chain-of-Thought (CoT) prompting enables LLMs to break down complex problems into intermediate reasoning steps. This technique dramatically improves performance on tasks requiring multi-step reasoning, math, logic, and complex analysis.

## When to Use

- Mathematical calculations
- Multi-step reasoning problems
- Logic puzzles
- Code debugging
- Complex analysis tasks
- Decision making with multiple factors

## Key Concepts

### CoT Techniques

| Technique | Description | Trigger |
|-----------|-------------|---------|
| Zero-shot CoT | Add "think step by step" | Single phrase |
| Few-shot CoT | Examples with reasoning | Demonstrated steps |
| Self-consistency | Multiple paths, vote | Sample + aggregate |
| Tree of Thoughts | Explore multiple branches | Structured exploration |
| Least-to-Most | Break into subproblems | Decomposition |

### How CoT Works

```
Without CoT:
Q: If John has 5 apples and gives 2 to Mary, then buys 3 more, how many does he have?
A: 6 ← (May be wrong, no reasoning shown)

With CoT:
Q: If John has 5 apples and gives 2 to Mary, then buys 3 more, how many does he have?
A: Let me think step by step:
   1. John starts with 5 apples
   2. He gives 2 to Mary: 5 - 2 = 3 apples
   3. He buys 3 more: 3 + 3 = 6 apples
   Therefore, John has 6 apples.
```

## Implementation

### Zero-Shot Chain-of-Thought

```python
def zero_shot_cot(
    client,
    problem: str,
    model: str = "gpt-4o"
) -> str:
    """Simple zero-shot CoT with magic phrase."""
    messages = [
        {
            "role": "user",
            "content": f"{problem}\n\nLet's think step by step."
        }
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages
    )

    return response.choices[0].message.content

# Variations of the magic phrase
COT_TRIGGERS = [
    "Let's think step by step.",
    "Let's work through this systematically.",
    "Let me break this down:",
    "Let's analyze this carefully:",
    "Let's solve this step by step:",
    "First, let me understand the problem, then solve it methodically."
]
```

### Few-Shot Chain-of-Thought

```python
def few_shot_cot(
    client,
    problem: str,
    examples: list[dict],
    model: str = "gpt-4o"
) -> str:
    """Few-shot CoT with reasoning examples."""
    messages = []

    # Add examples with reasoning
    for ex in examples:
        messages.append({"role": "user", "content": ex["question"]})
        messages.append({"role": "assistant", "content": ex["reasoning"]})

    # Add the actual problem
    messages.append({"role": "user", "content": problem})

    response = client.chat.completions.create(
        model=model,
        messages=messages
    )

    return response.choices[0].message.content

# Example reasoning chains
MATH_COT_EXAMPLES = [
    {
        "question": "Roger has 5 tennis balls. He buys 2 more cans of tennis balls. Each can has 3 tennis balls. How many tennis balls does he have now?",
        "reasoning": """Let me solve this step by step:
1. Roger starts with 5 tennis balls
2. He buys 2 cans, each with 3 balls
3. New balls from cans: 2 × 3 = 6 balls
4. Total balls: 5 + 6 = 11 balls

Therefore, Roger has 11 tennis balls."""
    },
    {
        "question": "A store had 40 apples. If they sold 15 in the morning and 18 in the afternoon, how many are left?",
        "reasoning": """Let me work through this:
1. Starting apples: 40
2. Sold in morning: 15
3. After morning: 40 - 15 = 25 apples
4. Sold in afternoon: 18
5. After afternoon: 25 - 18 = 7 apples

Therefore, 7 apples are left."""
    }
]
```

### Self-Consistency

```python
import random
from collections import Counter
from typing import List, Tuple

def self_consistency_cot(
    client,
    problem: str,
    num_samples: int = 5,
    temperature: float = 0.7,
    model: str = "gpt-4o"
) -> Tuple[str, float]:
    """
    Generate multiple reasoning paths and vote on the answer.
    Returns most common answer and confidence.
    """
    answers = []

    for _ in range(num_samples):
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": f"{problem}\n\nLet's think step by step. End with 'The answer is: [answer]'"
                }
            ],
            temperature=temperature
        )

        # Extract answer
        text = response.choices[0].message.content
        if "The answer is:" in text:
            answer = text.split("The answer is:")[-1].strip().rstrip(".")
            answers.append(answer)

    if not answers:
        return None, 0.0

    # Vote on most common answer
    counter = Counter(answers)
    most_common = counter.most_common(1)[0]

    return most_common[0], most_common[1] / len(answers)

# Usage
problem = "If a shirt costs $25 and is 20% off, what is the final price?"
answer, confidence = self_consistency_cot(client, problem, num_samples=5)
print(f"Answer: {answer} (confidence: {confidence:.0%})")
```

### Tree of Thoughts

```python
from typing import List, Dict
import json

class TreeOfThoughts:
    """
    Explore multiple reasoning paths and evaluate them.
    """

    def __init__(self, client, model: str = "gpt-4o"):
        self.client = client
        self.model = model

    def solve(
        self,
        problem: str,
        num_branches: int = 3,
        max_depth: int = 3
    ) -> Dict:
        """Solve problem using tree of thoughts."""
        # Generate initial thoughts
        initial_thoughts = self._generate_thoughts(problem, num_branches)

        # Evaluate and select best thoughts
        evaluated = self._evaluate_thoughts(problem, initial_thoughts)

        # Expand best thought
        best_thought = max(evaluated, key=lambda x: x["score"])

        # Continue reasoning from best thought
        final_answer = self._complete_reasoning(problem, best_thought["thought"])

        return {
            "problem": problem,
            "explored_thoughts": evaluated,
            "selected_path": best_thought,
            "final_answer": final_answer
        }

    def _generate_thoughts(self, problem: str, num_thoughts: int) -> List[str]:
        """Generate initial reasoning approaches."""
        prompt = f"""Problem: {problem}

Generate {num_thoughts} different approaches to solve this problem.
Each approach should be a first step in the reasoning process.
Format: Return JSON array of strings."""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )

        result = json.loads(response.choices[0].message.content)
        return result.get("approaches", [])

    def _evaluate_thoughts(
        self,
        problem: str,
        thoughts: List[str]
    ) -> List[Dict]:
        """Evaluate how promising each thought is."""
        evaluated = []

        for thought in thoughts:
            prompt = f"""Problem: {problem}

Proposed first step: {thought}

Evaluate this approach on a scale of 1-10:
- Is it relevant to the problem?
- Does it lead toward a solution?
- Is it logically sound?

Return JSON: {{"score": N, "reason": "..."}}"""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )

            result = json.loads(response.choices[0].message.content)
            evaluated.append({
                "thought": thought,
                "score": result.get("score", 0),
                "reason": result.get("reason", "")
            })

        return evaluated

    def _complete_reasoning(self, problem: str, starting_thought: str) -> str:
        """Complete the reasoning from a starting point."""
        prompt = f"""Problem: {problem}

Starting approach: {starting_thought}

Continue this reasoning to reach the final answer.
Show each step clearly and end with the final answer."""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content
```

### Least-to-Most Prompting

```python
def least_to_most(
    client,
    problem: str,
    model: str = "gpt-4o"
) -> Dict:
    """
    Decompose into subproblems and solve from simplest to most complex.
    """
    # Step 1: Decompose the problem
    decompose_prompt = f"""Problem: {problem}

Break this problem down into simpler subproblems.
List them from simplest to most complex.
Return JSON: {{"subproblems": ["...", "..."]}}"""

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": decompose_prompt}],
        response_format={"type": "json_object"}
    )

    result = json.loads(response.choices[0].message.content)
    subproblems = result.get("subproblems", [])

    # Step 2: Solve each subproblem
    solutions = []
    context = ""

    for subproblem in subproblems:
        solve_prompt = f"""Original problem: {problem}

Previous solutions:
{context}

Current subproblem: {subproblem}

Solve this subproblem step by step."""

        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": solve_prompt}]
        )

        solution = response.choices[0].message.content
        solutions.append({
            "subproblem": subproblem,
            "solution": solution
        })

        context += f"\nSubproblem: {subproblem}\nSolution: {solution}\n"

    # Step 3: Synthesize final answer
    synthesize_prompt = f"""Original problem: {problem}

Subproblem solutions:
{context}

Using all the above solutions, provide the final answer to the original problem."""

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": synthesize_prompt}]
    )

    return {
        "problem": problem,
        "subproblems": solutions,
        "final_answer": response.choices[0].message.content
    }
```

### Structured CoT for Specific Domains

```python
def code_debugging_cot(
    client,
    code: str,
    error: str,
    model: str = "gpt-4o"
) -> str:
    """Chain-of-thought for debugging code."""
    prompt = f"""Debug this code that produces an error.

Code:
```
{code}
```

Error:
```
{error}
```

Analyze step by step:
1. What does the code intend to do?
2. Where exactly does the error occur?
3. What is the root cause?
4. What is the fix?

Then provide the corrected code."""

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

def decision_making_cot(
    client,
    decision: str,
    options: List[str],
    criteria: List[str],
    model: str = "gpt-4o"
) -> str:
    """Chain-of-thought for decision making."""
    options_text = "\n".join([f"- {opt}" for opt in options])
    criteria_text = "\n".join([f"- {crit}" for crit in criteria])

    prompt = f"""Help make this decision:

Decision: {decision}

Options:
{options_text}

Evaluation criteria:
{criteria_text}

Analyze step by step:
1. List pros and cons for each option
2. Evaluate each option against each criterion
3. Identify potential risks and mitigations
4. Consider trade-offs
5. Make a recommendation with reasoning

Provide a structured analysis and final recommendation."""

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

def math_problem_cot(
    client,
    problem: str,
    model: str = "gpt-4o"
) -> Dict:
    """Structured math problem solving."""
    prompt = f"""Solve this math problem with detailed steps:

{problem}

Follow this structure:
1. **Given**: What information is provided?
2. **Find**: What are we solving for?
3. **Approach**: What method will we use?
4. **Solution**: Step-by-step calculation
5. **Verification**: Check the answer
6. **Answer**: Final answer with units

Return your analysis in JSON format with these sections."""

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )

    return json.loads(response.choices[0].message.content)
```

### Production CoT Service

```python
from dataclasses import dataclass
from typing import Optional, Callable
from enum import Enum
import logging

class CoTStrategy(Enum):
    ZERO_SHOT = "zero_shot"
    FEW_SHOT = "few_shot"
    SELF_CONSISTENCY = "self_consistency"
    TREE_OF_THOUGHTS = "tree_of_thoughts"
    LEAST_TO_MOST = "least_to_most"

@dataclass
class CoTConfig:
    strategy: CoTStrategy = CoTStrategy.ZERO_SHOT
    num_samples: int = 5  # For self-consistency
    temperature: float = 0.7
    examples: list = None  # For few-shot

class ChainOfThoughtService:
    """Production CoT reasoning service."""

    def __init__(self, client, model: str = "gpt-4o"):
        self.client = client
        self.model = model
        self.logger = logging.getLogger(__name__)

    def reason(
        self,
        problem: str,
        config: Optional[CoTConfig] = None
    ) -> Dict:
        """Apply chain-of-thought reasoning to a problem."""
        config = config or CoTConfig()

        try:
            if config.strategy == CoTStrategy.ZERO_SHOT:
                result = self._zero_shot(problem)
            elif config.strategy == CoTStrategy.FEW_SHOT:
                result = self._few_shot(problem, config.examples or [])
            elif config.strategy == CoTStrategy.SELF_CONSISTENCY:
                result = self._self_consistency(problem, config.num_samples, config.temperature)
            elif config.strategy == CoTStrategy.TREE_OF_THOUGHTS:
                tot = TreeOfThoughts(self.client, self.model)
                result = tot.solve(problem)
            elif config.strategy == CoTStrategy.LEAST_TO_MOST:
                result = least_to_most(self.client, problem, self.model)
            else:
                result = self._zero_shot(problem)

            return {
                "success": True,
                "strategy": config.strategy.value,
                "result": result
            }

        except Exception as e:
            self.logger.error(f"CoT reasoning failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def _zero_shot(self, problem: str) -> str:
        """Zero-shot CoT."""
        return zero_shot_cot(self.client, problem, self.model)

    def _few_shot(self, problem: str, examples: list) -> str:
        """Few-shot CoT."""
        return few_shot_cot(self.client, problem, examples, self.model)

    def _self_consistency(
        self,
        problem: str,
        num_samples: int,
        temperature: float
    ) -> Dict:
        """Self-consistency CoT."""
        answer, confidence = self_consistency_cot(
            self.client, problem, num_samples, temperature, self.model
        )
        return {
            "answer": answer,
            "confidence": confidence
        }
```

## Best Practices

1. **Choose Right Strategy**
   - Zero-shot for simple problems
   - Few-shot for pattern-dependent tasks
   - Self-consistency for critical decisions

2. **Provide Clear Examples**
   - Show complete reasoning
   - Cover different problem types
   - Include edge cases

3. **Structure the Output**
   - Request step-by-step format
   - Ask for explicit answer marker
   - Use structured formats when possible

4. **Verify Reasoning**
   - Check intermediate steps
   - Use self-consistency for validation
   - Ask for verification step

5. **Handle Complexity**
   - Decompose complex problems
   - Use tree of thoughts for branching logic
   - Apply least-to-most for sequential dependencies

## Common Pitfalls

1. **Expecting Perfection** - CoT improves but doesn't guarantee correctness
2. **Wrong Problem Type** - CoT helps with reasoning, not all tasks
3. **Weak Examples** - Poor few-shot examples lead to poor reasoning
4. **Ignoring Confidence** - Not using self-consistency when accuracy matters
5. **Overly Complex** - Using ToT when zero-shot suffices
6. **No Verification** - Not checking reasoning steps

## References

- [Chain-of-Thought Paper](https://arxiv.org/abs/2201.11903)
- [Self-Consistency Paper](https://arxiv.org/abs/2203.11171)
- [Tree of Thoughts Paper](https://arxiv.org/abs/2305.10601)
- [Least-to-Most Paper](https://arxiv.org/abs/2205.10625)
