---
name: dspy-ruby
description: Use this skill when working with DSPy.rb, a Ruby framework for building type-safe, composable LLM applications. It is ideal for implementing predictable AI features, creating LLM signatures and modules, configuring language model providers, and testing LLM-powered functionality in Ruby applications.
---

# DSPy.rb Expert

## Overview

DSPy.rb is a Ruby framework that enables developers to **program LLMs, not prompt them**. Instead of manually crafting prompts, define application requirements through type-safe, composable modules that can be tested, optimized, and version-controlled like regular code.

This skill provides comprehensive guidance on:
- Creating type-safe signatures for LLM operations
- Building composable modules and workflows
- Configuring multiple LLM providers
- Implementing agents with tools
- Testing and optimizing LLM applications
- Production deployment patterns

## Core Capabilities

### 1. Type-Safe Signatures

Create input/output contracts for LLM operations with runtime type checking.

**When to use**: Defining any LLM task, from simple classification to complex analysis.

**Quick reference**:
```ruby
class EmailClassificationSignature < DSPy::Signature
  description "Classify customer support emails"

  input do
    const :email_subject, String
    const :email_body, String
  end

  output do
    const :category, T.enum(["Technical", "Billing", "General"])
    const :priority, T.enum(["Low", "Medium", "High"])
  end
end
```

**Templates**: See `assets/signature-template.rb` for comprehensive examples including:
- Basic signatures with multiple field types
- Vision signatures for multimodal tasks
- Sentiment analysis signatures
- Code generation signatures

**Best practices**:
- Always provide clear, specific descriptions
- Use enums for constrained outputs
- Include field descriptions with `desc:` parameter
- Prefer specific types over generic String when possible

**Full documentation**: See `references/core-concepts.md` sections on Signatures and Type Safety.

### 2. Composable Modules

Build reusable, chainable modules that encapsulate LLM operations.

**When to use**: Implementing any LLM-powered feature, especially complex multi-step workflows.

**Quick reference**:
```ruby
class EmailProcessor < DSPy::Module
  def initialize
    super
    @classifier = DSPy::Predict.new(EmailClassificationSignature)
  end
end
```