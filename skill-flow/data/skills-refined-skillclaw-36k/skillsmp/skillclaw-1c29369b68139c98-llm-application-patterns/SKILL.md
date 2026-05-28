---
name: llm-application-patterns
description: Use this skill when building production LLM applications in any language, focusing on structured interfaces, type-safe contracts, and modular workflows.
---

# LLM Application Patterns

## Overview

Build production LLM applications using structured, testable patterns. Instead of manually crafting prompts, define application requirements through type-safe, composable modules that can be tested, optimized, and version-controlled like regular code.

**Core principle: Program LLMs, don't prompt them.**

This skill provides language-agnostic guidance on:
- Creating type-safe signatures for LLM operations
- Building composable modules and workflows
- Configuring multiple LLM providers
- Implementing agents with tools
- Testing and optimizing LLM applications
- Production deployment patterns

## Core Concepts

### 1. Type-Safe Signatures

Define input/output contracts for LLM operations with runtime type checking.

**When to use**: Any LLM task, from simple classification to complex analysis.

**Pattern** (pseudo-code):
```
Signature: EmailClassification
  Description: "Classify customer support emails"

  Inputs:
    email_subject: String (required)
    email_body: String (required)

  Outputs:
    category: Enum["Technical", "Billing", "General"]
    priority: Enum["Low", "Medium", "High"]
    confidence: Float (0.0 to 1.0)
```

**Best practices**:
- Always provide clear, specific descriptions
- Use enums for constrained outputs
- Include field descriptions
- Prefer specific types over generic strings
- Define confidence scores when useful

### 2. Composable Modules

Build reusable, chainable modules that encapsulate LLM operations.

**Pattern** (pseudo-code):
```
Module: EmailProcessor
  Initialize:
    classifier = Predict(EmailClassificationSignature)

  Forward(email_subject, email_body):
    return classifier.forward(email_subject, email_body)
```

**Module composition** - chain modules for complex workflows:
```
Module: CustomerServicePipeline
  Initialize:
    classifier = EmailClassifier()
    router = TicketRouter()
    responder = AutoResponder()
```