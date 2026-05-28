# Prompt Engineer - Sharp Edges

## Vague Instructions

### **Id**
vague-instructions
### **Summary**
Using imprecise language in prompts
### **Severity**
high
### **Situation**
Instructions like 'be helpful' or 'do a good job'
### **Why**
  LLMs interpret vague instructions differently than humans expect.
  "Be concise" means different things to different models and contexts.
  Without specific criteria, output varies unpredictably.
  
### **Solution**
  Be explicit:
  - "Respond in 2-3 sentences"
  - "List exactly 5 items"
  - "Use only information from the provided context"
  - Test how model interprets your instructions
  
### **Symptoms**
  - Output varies between runs
  - Model doesn't do what you meant
  - Works sometimes, fails sometimes
### **Detection Pattern**
  #### **Language**
generic
  #### **Pattern**
be helpful|do your best|as needed|when appropriate|if necessary

## No Output Format

### **Id**
no-output-format
### **Summary**
Expecting specific format without specifying it
### **Severity**
high
### **Situation**
Wanting JSON but not requiring it in prompt
### **Why**
  Models default to natural language. Without explicit format requirements,
  you get inconsistent structures that break parsing. Even with format
  instructions, examples are more reliable than descriptions.
  
### **Solution**
  Specify format explicitly:
  - Include output schema or example
  - Use JSON mode when available
  - Show exact format in examples
  - Validate output programmatically
  
### **Symptoms**
  - Parse errors on model output
  - Inconsistent JSON structure
  - Model adds explanatory text
### **Detection Pattern**
  #### **Language**
generic
  #### **Pattern**
json\.loads\(|parse.*response(?!.*format|.*schema)

## No Negative Instructions

### **Id**
no-negative-instructions
### **Summary**
Only saying what to do, not what to avoid
### **Severity**
medium
### **Situation**
Prompts without explicit don'ts
### **Why**
  Models make predictable mistakes you could prevent. Without negative
  instructions, they hallucinate, add unwanted content, or format
  incorrectly. Don'ts are as important as dos.
  
### **Solution**
  Include explicit don'ts:
  - "Do NOT make up information"
  - "Do NOT include explanatory text"
  - "NEVER mention that you're an AI"
  - Test for common failure modes
  
### **Symptoms**
  - Model adds unwanted content
  - Predictable but undesired behaviors
  - Same mistakes repeatedly
### **Detection Pattern**
  #### **Language**
generic
  #### **Pattern**
system.*prompt(?!.*not|.*never|.*don't|.*avoid)

## Prompt Guessing

### **Id**
prompt-guessing
### **Summary**
Changing prompts without measuring impact
### **Severity**
medium
### **Situation**
Tweaking prompts based on intuition alone
### **Why**
  Prompt changes have non-obvious effects. A 'better' prompt by intuition
  might actually hurt performance. Without measurement, you're guessing
  and may be making things worse.
  
### **Solution**
  Systematic evaluation:
  - Create test set with expected outputs
  - Measure before and after changes
  - Track metrics over time
  - A/B test significant changes
  
### **Symptoms**
  - Performance regresses unexpectedly
  - No idea if changes help
  - Endless prompt tweaking
### **Detection Pattern**
  #### **Language**
generic
  #### **Pattern**
prompt.*=|system_prompt.*=(?!.*evaluate|.*test|.*benchmark)

## Context Overload

### **Id**
context-overload
### **Summary**
Including irrelevant context 'just in case'
### **Severity**
medium
### **Situation**
Stuffing all available information into prompt
### **Why**
  More context can dilute important information, confuse the model,
  and increase costs. Models have attention limits - irrelevant content
  competes with relevant content.
  
### **Solution**
  Curate context:
  - Include only relevant information
  - Use retrieval for large docs
  - Order context by importance
  - Set relevance thresholds
  
### **Symptoms**
  - Model ignores key information
  - High token costs
  - Answers drift with more context
### **Detection Pattern**
  #### **Language**
generic
  #### **Pattern**
context.*=.*all|include.*everything|full.*document

## Few Shot Bias

### **Id**
few-shot-bias
### **Summary**
Biased or unrepresentative examples
### **Severity**
medium
### **Situation**
Examples that don't represent expected inputs
### **Why**
  Models learn patterns from examples. If examples are biased toward
  certain cases, the model performs poorly on others. Examples should
  cover the expected distribution.
  
### **Solution**
  Diverse examples:
  - Include edge cases
  - Cover expected input distribution
  - Balance example types
  - Include negative examples when helpful
  
### **Symptoms**
  - Works on examples, fails on real inputs
  - Biased toward certain outputs
  - Narrow success patterns
### **Detection Pattern**
  #### **Language**
generic
  #### **Pattern**
examples.*=.*\[(?!.*edge|.*different|.*varied)

## Temperature Ignorance

### **Id**
temperature-ignorance
### **Summary**
Using default temperature for all tasks
### **Severity**
medium
### **Situation**
Not adjusting temperature for task type
### **Why**
  Temperature affects output determinism. High temperature for factual
  tasks causes errors. Low temperature for creative tasks causes
  repetitive, boring outputs.
  
### **Solution**
  Task-appropriate temperature:
  - 0-0.3 for factual/structured tasks
  - 0.5-0.7 for balanced tasks
  - 0.8-1.0 for creative tasks
  - Test different values
  
### **Symptoms**
  - Factual errors from high temperature
  - Boring outputs from low temperature
  - Inconsistent creative quality
### **Detection Pattern**
  #### **Language**
generic
  #### **Pattern**
temperature.*=.*1\.0|temperature.*=.*0(?!.*creative|.*factual)

## Prompt Injection Naive

### **Id**
prompt-injection-naive
### **Summary**
Not considering prompt injection in user input
### **Severity**
high
### **Situation**
Concatenating user input directly into prompt
### **Why**
  User input can contain instructions that override your prompt. This
  is prompt injection - users can make the model ignore your instructions
  and follow theirs instead.
  
### **Solution**
  Defend against injection:
  - Clearly delimit user input
  - Use XML tags or quotes
  - Instruction hierarchy (system > user)
  - Validate/sanitize user input
  
### **Symptoms**
  - Model follows user instructions over yours
  - Unexpected behaviors with certain inputs
  - Security issues in production
### **Detection Pattern**
  #### **Language**
generic
  #### **Pattern**
prompt.*\+.*user_input|f".*\{user|concat.*input