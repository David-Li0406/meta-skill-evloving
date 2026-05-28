# Source References

Official Anthropic documentation and resources for Claude prompting best practices.

## Primary Sources

### Claude 4 Best Practices

https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-4-best-practices

Core prompting guidance for Claude 4.x models including Opus 4.5. Covers:

- Explicit instruction requirements
- Context and motivation
- System prompt sensitivity
- "Think" word sensitivity
- Extended thinking recommendations
- Formatting guidance

### Migrating to Claude 4

https://platform.claude.com/docs/en/about-claude/models/migrating-to-claude-4

Migration guidance from Claude 3.x to Claude 4.x models. Covers:

- Behavioral differences
- Breaking changes
- Platform-specific model strings
- Prompt adjustment strategies

### Claude Code Best Practices

https://www.anthropic.com/engineering/claude-code-best-practices

Engineering blog post on effective Claude Code usage. Covers:

- Being specific vs vague
- Research and planning before implementation
- Using CLAUDE.md files
- Visual and tangible targets
- Workflow patterns

### Effective Context Engineering for AI Agents

https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents

Guidance on managing context for agentic applications. Covers:

- Finding high-signal tokens
- System prompt "Goldilocks zone"
- Avoiding hardcoded logic vs vague guidance
- Structured formats for state management

## Official Plugins and Skills

### Opus 4.5 Migration Plugin

https://github.com/anthropics/claude-code/tree/main/plugins/claude-opus-4-5-migration

Official Anthropic plugin for migrating to Opus 4.5. Contains:

- Model string updates
- Beta header removal
- Prompt adjustment snippets

### Opus 4.5 Prompt Snippets

https://github.com/anthropics/claude-code/blob/main/plugins/claude-opus-4-5-migration/skills/claude-opus-4-5-migration/references/prompt-snippets.md

Battle-tested prompt snippets for Opus 4.5 behavioral issues:

1. Tool overtriggering
2. Over-engineering prevention
3. Code exploration
4. Frontend design quality
5. Thinking sensitivity

## Model Announcements

### Introducing Claude Opus 4.5

https://www.anthropic.com/news/claude-opus-4-5

Official announcement covering:

- Model capabilities
- Vision improvements
- Coding performance
- Pricing

### Claude Opus 4.5 Product Page

https://www.anthropic.com/claude/opus

Product overview with capability highlights.

## Additional Resources

### Prompt Improver

https://www.anthropic.com/news/prompt-improver

Tool for automatically refining prompts using prompt engineering techniques.

### Prompt Generator

https://www.anthropic.com/news/prompt-generator

Generate production-ready prompt templates in the Anthropic Console.

### Anthropic Academy

https://www.anthropic.com/learn/build-with-claude

Learning resources for building with Claude.

## Key Takeaways by Source

### From Claude 4 Best Practices

- Claude 4.x requires more explicit direction than earlier models
- Provide context explaining _why_ behavior matters
- Opus 4.5 is more responsive to system prompts (may overtrigger)
- Replace "think" with "consider", "evaluate", "believe"
- Extended thinking improves complex reasoning but impacts caching

### From Claude Code Best Practices

- Specificity reduces course corrections
- "Include as many relevant features as possible" beats "Create a dashboard"
- Lead with research and planning before coding
- Provide visual targets (screenshots, test cases, mocks)

### From Context Engineering

- Find smallest set of high-signal tokens
- System prompts need the right "altitude" (not too rigid, not too vague)
- Use structured formats (JSON, prose) for state tracking
- Prompt chaining improves accuracy for multi-step tasks

### From Opus 4.5 Migration Plugin

- Replace emphatic language (MUST → should, ALWAYS → typically)
- Add over-engineering prevention snippet when needed
- Add code exploration directive if model skips reading files
- Replace "think" variants throughout prompts
