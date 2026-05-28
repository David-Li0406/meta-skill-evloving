# Prompt Engineer

## Patterns


---
  #### **Name**
Structured System Prompt
  #### **Description**
Well-organized system prompt with clear sections
  #### **When**
Designing any LLM application
  #### **Implementation**
    - Role: who the model is
    - Context: relevant background
    - Instructions: what to do
    - Constraints: what NOT to do
    - Output format: expected structure
    - Examples: demonstration of correct behavior
    

---
  #### **Name**
Few-Shot Examples
  #### **Description**
Include examples of desired behavior
  #### **When**
Task is complex or has specific format
  #### **Implementation**
    - Show 2-5 diverse examples
    - Include edge cases in examples
    - Match example difficulty to expected inputs
    - Use consistent formatting across examples
    - Include negative examples when helpful
    

---
  #### **Name**
Chain-of-Thought
  #### **Description**
Request step-by-step reasoning
  #### **When**
Complex reasoning or multi-step problems
  #### **Implementation**
    - Ask model to think step by step
    - Provide reasoning structure
    - Request explicit intermediate steps
    - Parse reasoning separately from answer
    - Use for debugging model failures
    

---
  #### **Name**
Output Schema
  #### **Description**
Specify exact output format
  #### **When**
Need parseable, structured output
  #### **Implementation**
    - Use JSON schema or XML tags
    - Provide output example
    - Include all required fields
    - Specify types and constraints
    - Validate output programmatically
    

---
  #### **Name**
Prompt Decomposition
  #### **Description**
Break complex tasks into smaller prompts
  #### **When**
Single prompt fails or is unreliable
  #### **Implementation**
    - Identify distinct subtasks
    - Create focused prompt per subtask
    - Chain outputs as inputs
    - Parallelize independent subtasks
    - Aggregate results appropriately
    

---
  #### **Name**
Evaluation Framework
  #### **Description**
Systematically test prompt changes
  #### **When**
Optimizing prompt performance
  #### **Implementation**
    - Create golden test set with expected outputs
    - Define evaluation metrics (accuracy, format, etc.)
    - Run A/B tests on prompt variations
    - Track metrics over time
    - Version control prompts like code
    

## Anti-Patterns


---
  #### **Name**
Vague Instructions
  #### **Description**
Using imprecise language in prompts
  #### **Problem**
Model interprets differently than intended
  #### **Solution**
Be specific, use concrete examples, test interpretations

---
  #### **Name**
Kitchen Sink Prompt
  #### **Description**
Cramming everything into one prompt
  #### **Problem**
Model loses focus, ignores parts, inconsistent
  #### **Solution**
Decompose into focused prompts, chain if needed

---
  #### **Name**
No Negative Instructions
  #### **Description**
Only saying what to do, not what to avoid
  #### **Problem**
Model makes predictable errors you could prevent
  #### **Solution**
Include explicit don'ts and edge cases to avoid

---
  #### **Name**
Prompt Guessing
  #### **Description**
Changing prompts without measuring impact
  #### **Problem**
No idea if changes help or hurt
  #### **Solution**
Evaluate before and after, use test suites

---
  #### **Name**
Context Overload
  #### **Description**
Including irrelevant context to be safe
  #### **Problem**
Dilutes important info, wastes tokens, confuses model
  #### **Solution**
Include only relevant context, use retrieval for large docs

---
  #### **Name**
Format Ambiguity
  #### **Description**
Expecting specific format without specifying it
  #### **Problem**
Inconsistent outputs, parsing failures
  #### **Solution**
Explicit format spec with schema and example