---
id: prompt-engineering
name: "Prompt Engineering"
domain: ML
skill: faion-ml-engineer
category: "ml-engineering"
---

# Prompt Engineering

## Overview

Prompt engineering is the practice of designing effective inputs for LLMs to achieve desired outputs. Good prompts improve accuracy, consistency, and efficiency while reducing costs and errors.

## When to Use

- Any LLM application
- Before considering fine-tuning
- When outputs are inconsistent
- To improve task accuracy
- To control output format
- To reduce hallucinations

## Key Concepts

### Prompt Components

```
┌─────────────────────────────────────────┐
│           SYSTEM PROMPT                  │
│  - Role definition                       │
│  - Behavioral constraints               │
│  - Output format rules                  │
└─────────────────────────────────────────┘
                   │
┌─────────────────▼───────────────────────┐
│           USER PROMPT                    │
│  - Context/Background                    │
│  - Task description                     │
│  - Examples (few-shot)                  │
│  - Input data                           │
│  - Output instructions                  │
└─────────────────────────────────────────┘
```

### Prompt Patterns

| Pattern | Use Case | Example |
|---------|----------|---------|
| Zero-shot | Simple tasks | "Translate to Spanish: Hello" |
| Few-shot | Pattern learning | Examples + task |
| Chain-of-Thought | Complex reasoning | "Let's think step by step" |
| Self-consistency | Reliability | Multiple samples, vote |
| ReAct | Tool use | Reason + Act pattern |

## Implementation

### Basic Prompting Patterns

```python
from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class PromptTemplate:
    """Reusable prompt template."""
    system: str
    user_template: str
    examples: List[Dict] = None

    def format(self, **kwargs) -> List[Dict]:
        """Format prompt with variables."""
        messages = [{"role": "system", "content": self.system}]

        # Add examples if few-shot
        if self.examples:
            for ex in self.examples:
                messages.append({"role": "user", "content": ex["input"]})
                messages.append({"role": "assistant", "content": ex["output"]})

        # Add user message
        messages.append({
            "role": "user",
            "content": self.user_template.format(**kwargs)
        })

        return messages

# Zero-shot template
CLASSIFICATION_PROMPT = PromptTemplate(
    system="""You are a sentiment classifier. Classify text as:
- positive
- negative
- neutral

Respond with only the classification.""",
    user_template="Classify: {text}"
)

# Few-shot template
FEW_SHOT_CLASSIFICATION = PromptTemplate(
    system="You are a sentiment classifier. Respond with only: positive, negative, or neutral.",
    user_template="Classify: {text}",
    examples=[
        {"input": "Classify: I love this product!", "output": "positive"},
        {"input": "Classify: This is terrible.", "output": "negative"},
        {"input": "Classify: The product arrived on time.", "output": "neutral"}
    ]
)

# Usage
messages = FEW_SHOT_CLASSIFICATION.format(text="This exceeded my expectations!")
```

### System Prompt Patterns

```python
SYSTEM_PROMPTS = {
    "assistant": """You are a helpful, harmless, and honest AI assistant.

Guidelines:
- Be concise and direct
- Acknowledge uncertainty
- Ask clarifying questions when needed
- Never make up information""",

    "code_expert": """You are an expert software developer with deep knowledge of:
- Python, JavaScript, TypeScript
- System design and architecture
- Testing and debugging

When writing code:
- Include type hints
- Add docstrings
- Handle errors appropriately
- Follow best practices""",

    "data_analyst": """You are a data analyst expert.

When analyzing data:
- Start with summary statistics
- Identify patterns and anomalies
- Provide actionable insights
- Support claims with data
- Use visualizations when helpful""",

    "editor": """You are a professional editor.

When editing text:
- Fix grammar and spelling
- Improve clarity and flow
- Maintain the author's voice
- Suggest structural improvements
- Be constructive, not critical"""
}

def create_system_prompt(
    role: str,
    constraints: List[str] = None,
    output_format: str = None
) -> str:
    """Create a structured system prompt."""
    prompt_parts = [f"You are {role}."]

    if constraints:
        prompt_parts.append("\nConstraints:")
        for c in constraints:
            prompt_parts.append(f"- {c}")

    if output_format:
        prompt_parts.append(f"\nOutput format:\n{output_format}")

    return "\n".join(prompt_parts)

# Example
system = create_system_prompt(
    role="a helpful customer support agent for TechCorp",
    constraints=[
        "Always be polite and professional",
        "If you don't know, say so",
        "Offer to escalate complex issues",
        "Never share internal information"
    ],
    output_format="Respond in a friendly, concise manner. Include relevant links when available."
)
```

### Role-Based Prompting

```python
def create_expert_prompt(
    expertise: str,
    task: str,
    context: str = ""
) -> List[Dict]:
    """Create a prompt with expert persona."""
    system = f"""You are a world-class expert in {expertise}.

Your expertise includes:
- Deep theoretical knowledge
- Practical experience
- Awareness of common pitfalls
- Knowledge of best practices

Provide thorough, accurate, and actionable advice."""

    user = f"Task: {task}"
    if context:
        user = f"Context: {context}\n\n{user}"

    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user}
    ]

# Usage
messages = create_expert_prompt(
    expertise="Python performance optimization",
    task="Review this code for performance issues and suggest improvements",
    context="This function is called 10,000 times per second in production"
)
```

### Structured Output Prompting

```python
import json
from typing import Type
from pydantic import BaseModel

def create_structured_prompt(
    task: str,
    output_schema: Type[BaseModel],
    examples: List[Dict] = None
) -> str:
    """Create prompt for structured JSON output."""
    schema_str = json.dumps(output_schema.model_json_schema(), indent=2)

    prompt = f"""Task: {task}

Output must be valid JSON matching this schema:
```json
{schema_str}
```
"""

    if examples:
        prompt += "\n\nExamples:\n"
        for ex in examples:
            prompt += f"Input: {ex['input']}\nOutput: {json.dumps(ex['output'])}\n\n"

    return prompt

# Example usage
from pydantic import BaseModel, Field
from typing import List

class ProductReview(BaseModel):
    sentiment: str = Field(..., description="positive, negative, or neutral")
    score: float = Field(..., ge=0, le=1, description="Confidence score")
    key_points: List[str] = Field(..., description="Main points from review")
    summary: str = Field(..., description="One sentence summary")

prompt = create_structured_prompt(
    task="Analyze this product review and extract structured information",
    output_schema=ProductReview,
    examples=[
        {
            "input": "Great product! Fast delivery.",
            "output": {
                "sentiment": "positive",
                "score": 0.95,
                "key_points": ["Product quality", "Fast delivery"],
                "summary": "Customer satisfied with product and delivery speed."
            }
        }
    ]
)
```

### Delimiting and Formatting

```python
def format_with_delimiters(
    instruction: str,
    content: str,
    delimiter: str = "```"
) -> str:
    """Format prompt with clear delimiters."""
    return f"""{instruction}

{delimiter}
{content}
{delimiter}"""

def format_with_xml_tags(
    instruction: str,
    **sections
) -> str:
    """Format prompt with XML-style tags."""
    prompt = instruction + "\n\n"

    for tag, content in sections.items():
        prompt += f"<{tag}>\n{content}\n</{tag}>\n\n"

    return prompt

# Example
prompt = format_with_xml_tags(
    "Summarize the document and answer the question.",
    document="This is a long document about AI...",
    question="What are the main benefits of AI?",
    format="Provide a 2-3 sentence summary followed by a direct answer."
)

# Output:
# Summarize the document and answer the question.
#
# <document>
# This is a long document about AI...
# </document>
#
# <question>
# What are the main benefits of AI?
# </question>
#
# <format>
# Provide a 2-3 sentence summary followed by a direct answer.
# </format>
```

### Meta-Prompting

```python
def generate_prompt(
    task_description: str,
    client,  # OpenAI client
    model: str = "gpt-4o"
) -> str:
    """Use LLM to generate an effective prompt."""
    meta_prompt = """You are a prompt engineering expert. Create an effective prompt for the following task.

The prompt should:
1. Be clear and specific
2. Include relevant context
3. Specify output format
4. Include examples if helpful
5. Handle edge cases

Task: {task}

Generate only the prompt, no explanation."""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": meta_prompt.format(task=task_description)}
        ]
    )

    return response.choices[0].message.content

def optimize_prompt(
    original_prompt: str,
    failure_cases: List[Dict],
    client,
    model: str = "gpt-4o"
) -> str:
    """Improve prompt based on failure cases."""
    meta_prompt = f"""Analyze this prompt and its failure cases, then create an improved version.

Original prompt:
{original_prompt}

Failure cases:
{json.dumps(failure_cases, indent=2)}

Create an improved prompt that addresses these failures while maintaining the original intent."""

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": meta_prompt}]
    )

    return response.choices[0].message.content
```

### Prompt Chaining

```python
from typing import List, Callable

class PromptChain:
    """Chain multiple prompts together."""

    def __init__(self, client, model: str = "gpt-4o"):
        self.client = client
        self.model = model
        self.steps: List[Callable] = []

    def add_step(self, prompt_func: Callable):
        """Add a step to the chain."""
        self.steps.append(prompt_func)
        return self

    def run(self, initial_input: str) -> Dict:
        """Execute the chain."""
        current_input = initial_input
        results = {"steps": []}

        for i, step_func in enumerate(self.steps):
            prompt = step_func(current_input)

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )

            output = response.choices[0].message.content

            results["steps"].append({
                "step": i + 1,
                "input": current_input[:100],
                "output": output
            })

            current_input = output

        results["final_output"] = current_input
        return results

# Usage
def step1_extract(text):
    return f"Extract the main entities from this text: {text}"

def step2_categorize(entities):
    return f"Categorize these entities by type: {entities}"

def step3_summarize(categories):
    return f"Create a brief summary of these categorized entities: {categories}"

chain = PromptChain(client, "gpt-4o")
chain.add_step(step1_extract)
chain.add_step(step2_categorize)
chain.add_step(step3_summarize)

result = chain.run("Apple announced a new iPhone with advanced AI features...")
```

### Prompt Library

```python
from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Optional

class PromptCategory(Enum):
    CLASSIFICATION = "classification"
    GENERATION = "generation"
    EXTRACTION = "extraction"
    TRANSFORMATION = "transformation"
    ANALYSIS = "analysis"

@dataclass
class ManagedPrompt:
    name: str
    category: PromptCategory
    system: str
    template: str
    examples: Optional[List[Dict]] = None
    version: str = "1.0"
    description: str = ""

class PromptLibrary:
    """Centralized prompt management."""

    def __init__(self):
        self.prompts: Dict[str, ManagedPrompt] = {}

    def register(self, prompt: ManagedPrompt):
        """Register a prompt."""
        self.prompts[prompt.name] = prompt

    def get(self, name: str) -> ManagedPrompt:
        """Retrieve a prompt."""
        if name not in self.prompts:
            raise KeyError(f"Prompt '{name}' not found")
        return self.prompts[name]

    def format(self, name: str, **kwargs) -> List[Dict]:
        """Format a prompt with variables."""
        prompt = self.get(name)
        messages = [{"role": "system", "content": prompt.system}]

        if prompt.examples:
            for ex in prompt.examples:
                messages.append({"role": "user", "content": ex["input"]})
                messages.append({"role": "assistant", "content": ex["output"]})

        messages.append({
            "role": "user",
            "content": prompt.template.format(**kwargs)
        })

        return messages

# Initialize library
library = PromptLibrary()

# Register prompts
library.register(ManagedPrompt(
    name="sentiment_analysis",
    category=PromptCategory.CLASSIFICATION,
    system="You are a sentiment analysis expert. Respond with only: positive, negative, or neutral.",
    template="Analyze the sentiment: {text}",
    examples=[
        {"input": "Analyze the sentiment: I love it!", "output": "positive"},
        {"input": "Analyze the sentiment: This is awful.", "output": "negative"}
    ],
    version="1.2",
    description="Classify text sentiment into three categories"
))

# Usage
messages = library.format("sentiment_analysis", text="The product works as expected.")
```

### Prompt Testing

```python
from typing import List, Dict, Callable
import json

class PromptTester:
    """Test prompts against expected outputs."""

    def __init__(self, client, model: str = "gpt-4o"):
        self.client = client
        self.model = model

    def test_prompt(
        self,
        prompt_messages: List[Dict],
        test_cases: List[Dict],
        evaluator: Callable[[str, str], bool] = None
    ) -> Dict:
        """Test a prompt against multiple cases."""
        results = {
            "passed": 0,
            "failed": 0,
            "cases": []
        }

        for case in test_cases:
            # Build messages with test input
            messages = prompt_messages.copy()
            messages[-1]["content"] = messages[-1]["content"].format(**case["input"])

            # Get response
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            actual = response.choices[0].message.content

            # Evaluate
            expected = case["expected"]
            if evaluator:
                passed = evaluator(actual, expected)
            else:
                passed = expected.lower() in actual.lower()

            if passed:
                results["passed"] += 1
            else:
                results["failed"] += 1

            results["cases"].append({
                "input": case["input"],
                "expected": expected,
                "actual": actual,
                "passed": passed
            })

        results["accuracy"] = results["passed"] / len(test_cases)
        return results

# Usage
tester = PromptTester(client)
messages = library.format("sentiment_analysis", text="{text}")

test_cases = [
    {"input": {"text": "I absolutely love this!"}, "expected": "positive"},
    {"input": {"text": "This is the worst."}, "expected": "negative"},
    {"input": {"text": "It arrived on Tuesday."}, "expected": "neutral"},
]

results = tester.test_prompt(messages, test_cases)
print(f"Accuracy: {results['accuracy']:.2%}")
```

## Best Practices

1. **Be Specific**
   - Clear task description
   - Explicit output format
   - Include constraints

2. **Use Examples**
   - Show desired output format
   - Cover edge cases
   - Quality over quantity

3. **Structure Matters**
   - Use delimiters for clarity
   - Separate instruction from content
   - Organize complex prompts

4. **Iterate and Test**
   - Start simple, add complexity
   - Test with diverse inputs
   - Track prompt versions

5. **Manage Prompts**
   - Version control prompts
   - Document purpose and usage
   - Create reusable templates

## Common Pitfalls

1. **Vague Instructions** - Ambiguous tasks lead to inconsistent outputs
2. **No Output Format** - Model guesses desired format
3. **Too Many Examples** - Confuses more than helps
4. **Implicit Assumptions** - Model may not share your assumptions
5. **No Edge Cases** - Fails on unusual inputs
6. **Prompt Injection** - User input manipulates behavior

## References

- [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
- [Anthropic Prompt Engineering](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)
