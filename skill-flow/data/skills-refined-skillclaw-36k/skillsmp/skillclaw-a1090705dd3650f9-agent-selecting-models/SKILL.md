---
name: agent-selecting-models
description: Use this skill when selecting the appropriate AI model based on task complexity, reasoning requirements, and performance needs, particularly when implementing agents or justifying model selection.
---

# Selecting AI Models for Agents

Guidelines for choosing between sonnet and haiku models based on agent capabilities and task requirements.

## When This Skill Loads

This Skill auto-loads when implementing agents or documenting model selection rationale.

## Available Models

### Sonnet (claude-sonnet-4-5)

**Characteristics**:

- Advanced reasoning capabilities
- Complex decision-making
- Deep pattern recognition
- Sophisticated analysis
- Multi-step orchestration
- Higher cost, slower performance

**Use for**: Complex, reasoning-intensive tasks

### Haiku (claude-haiku-3-5)

**Characteristics**:

- Fast execution
- Straightforward tasks
- Pattern matching
- Simple decision-making
- Cost-effective
- Lower cost, faster performance

**Use for**: Simple, well-defined tasks

## Decision Framework

### Use Sonnet When Task Requires

✅ **Advanced Reasoning**

- Analyzing technical claims for subtle contradictions
- Distinguishing objective errors from subjective improvements
- Detecting false positives in validation findings
- Context-dependent decision-making
- Inferring user intent from ambiguous requests

✅ **Complex Pattern Recognition**

- Cross-referencing multiple documentation files
- Identifying conceptual duplications (not just verbatim)
- Detecting inconsistencies across architectural layers
- Understanding domain-specific patterns
- Recognizing semantic similarities

✅ **Sophisticated Analysis**

- Verifying factual accuracy against authoritative sources
- Assessing confidence levels (HIGH/MEDIUM/FALSE_POSITIVE)
- Evaluating code quality and architectural decisions
- Analyzing narrative flow and pedagogical structure
- Determining fix safety and impact

✅ **Multi-Step Orchestration**

- Coordinating complex validation workflows
- Managing dependencies between validation steps
- Iterative refinement processes
- Dynamic workflow adaptation
- Error recovery and retry logic

✅ **Deep Web Research**

- Finding and evaluating authoritative sources
- Comparing claims against official documentation
- Version verification across multiple registries
- API correctness validation
- Detecting outdated information

### Use Haiku When Task Is

✅ **Pattern Matching**

- Extracting URLs from markdown files
- Finding code blocks by language
- Matching simple patterns in data
- Performing straightforward data retrieval tasks