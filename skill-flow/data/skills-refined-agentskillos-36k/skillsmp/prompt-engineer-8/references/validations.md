# Prompt Engineer - Validations

## Vague Instruction

### **Id**
vague-instruction
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - be helpful
  - do your best
  - as needed
  - when appropriate
  - if necessary
  - be concise(?!.*\d)
### **Message**
Vague instruction may be interpreted inconsistently.
### **Fix Action**
Use specific, measurable criteria (e.g., '2-3 sentences')
### **Applies To**
  - **/*.py
  - **/*.ts
  - **/*.js
  - **/*.md

## No Output Format Specified

### **Id**
no-output-format
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - json\.loads\((?!.*format|.*schema)
  - parse.*response(?!.*format|.*schema)
  - JSON\.parse\((?!.*format)
### **Message**
Parsing output without format specification in prompt.
### **Fix Action**
Specify exact output format with schema or example
### **Applies To**
  - **/*.py
  - **/*.ts
  - **/*.js

## Prompt Injection Risk

### **Id**
prompt-injection-risk
### **Severity**
error
### **Type**
regex
### **Pattern**
  - prompt\s*\+\s*user_input
  - f".*\{user
  - f".*\{input
  - `.*\$\{user
  - concat.*input
### **Message**
Direct user input concatenation - prompt injection risk.
### **Fix Action**
Delimit user input clearly with tags, validate/sanitize
### **Applies To**
  - **/*.py
  - **/*.ts
  - **/*.js

## No Negative Instructions

### **Id**
no-negative-instructions
### **Severity**
info
### **Type**
regex
### **Pattern**
  - system.*prompt.*=(?!.*not|.*never|.*don't|.*avoid|.*do not)
### **Message**
System prompt without negative instructions (don'ts).
### **Fix Action**
Add explicit don'ts to prevent common failure modes
### **Applies To**
  - **/*.py
  - **/*.ts
  - **/*.js

## Hardcoded Prompt

### **Id**
hardcoded-prompt
### **Severity**
info
### **Type**
regex
### **Pattern**
  - prompt\s*=\s*["'][^"']{100,}["']
  - system_prompt\s*=\s*["'][^"']{100,}["']
### **Message**
Long hardcoded prompt - consider externalizing for management.
### **Fix Action**
Move prompts to separate files for version control
### **Applies To**
  - **/*.py
  - **/*.ts
  - **/*.js
### **Excludes**
  - **/prompts/**
  - **/templates/**

## Default Temperature for All Tasks

### **Id**
default-temperature
### **Severity**
info
### **Type**
regex
### **Pattern**
  - temperature\s*=\s*1\.0
  - temperature\s*=\s*0(?!.*\d)
### **Message**
Extreme or default temperature may not suit task type.
### **Fix Action**
Use 0-0.3 for factual, 0.5-0.7 balanced, 0.8-1.0 creative
### **Applies To**
  - **/*.py
  - **/*.ts
  - **/*.js

## No Examples in Prompt

### **Id**
no-examples
### **Severity**
info
### **Type**
regex
### **Pattern**
  - system.*prompt(?!.*example|.*e\.g\.|.*for instance)
### **Message**
Prompt without examples - few-shot improves consistency.
### **Fix Action**
Add 2-5 diverse examples of expected behavior
### **Applies To**
  - **/*.py
  - **/*.ts
  - **/*.js

## Untested Prompt Change

### **Id**
untested-prompt-change
### **Severity**
info
### **Type**
regex
### **Pattern**
  - prompt\s*=|system_prompt\s*=(?!.*evaluate|.*test|.*benchmark)
### **Message**
Prompt assignment without evaluation call nearby.
### **Fix Action**
Evaluate prompt changes with test set before deploying
### **Applies To**
  - **/*.py
  - **/*.ts
  - **/*.js
### **Excludes**
  - **/test*
  - **/*_test.*
  - **/*.test.*
  - **/*.spec.*

## Context Stuffing

### **Id**
context-stuffing
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - context\s*=\s*all
  - include.*everything
  - full.*document
  - \.join\([^)]*all
### **Message**
Including all context may dilute important information.
### **Fix Action**
Include only relevant context, use retrieval for large docs
### **Applies To**
  - **/*.py
  - **/*.ts
  - **/*.js