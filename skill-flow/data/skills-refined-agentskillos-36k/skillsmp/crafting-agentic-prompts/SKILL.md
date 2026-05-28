---
name: crafting-agentic-prompts
description: Provides prompt engineering best practices for agentic workflows with modern language models. This skill should be used when users need help writing system prompts, improving agent behavior, controlling output formatting, optimizing tool usage patterns, or setting up long-horizon reasoning tasks. Triggers on requests like "write a prompt", "improve agent behavior", "make agent more proactive", "control verbosity", or "setup agentic workflow".
---

# Agentic Prompting

## Overview

This skill provides comprehensive guidance for writing effective prompts for agentic workflows using modern language models. Apply these principles when crafting system prompts, improving agent behavior, or optimizing agentic applications.

## When to Use This Skill

Use this skill when the user requests help with:

- Writing or improving system prompts for agentic workflows
- Making agents more or less proactive about taking action
- Controlling agent verbosity and output formatting
- Optimizing parallel tool calling behavior
- Setting up long-horizon reasoning tasks
- Improving research and information gathering capabilities
- Enhancing subagent orchestration
- Creating prompts for document creation, coding, or frontend generation
- Reducing hallucinations or improving accuracy
- Any other agent behavior modification

## Core Principles

### 1. Be Explicit with Instructions

Modern language models respond well to clear, explicit instructions. Specify exactly what behavior is desired rather than leaving it implicit.

**Example:** Instead of "Create an analytics dashboard", use "Create an analytics dashboard. Include as many relevant features and interactions as possible. Go beyond the basics to create a fully-featured implementation."

### 2. Add Context to Improve Performance

Provide context or motivation behind instructions. Explain WHY a behavior is important to help the model understand goals and deliver targeted responses.

**Example:** Instead of "NEVER use ellipses", use "The response will be read aloud by a text-to-speech engine, so never use ellipses since the text-to-speech engine will not know how to pronounce them."

### 3. Be Vigilant with Examples & Details

Language models pay close attention to details and examples. Ensure examples align with desired behaviors and minimize undesired behaviors.

### 4. Tell the Model What TO Do, Not What NOT To Do

Frame instructions positively:
- Instead of: "Do not use markdown"
- Use: "Write in smoothly flowing prose paragraphs"

## Workflow

When helping users craft agentic prompts:

1. **Understand the Use Case**
   - What type of agent is being built? (research, coding, document creation, etc.)
   - What specific behaviors does the user want to encourage or discourage?
   - What are the user's main pain points with current agent behavior?

2. **Identify Relevant Patterns**
   - Consult `references/prompt-templates.md` for categorized prompt snippets
   - For comprehensive guidance, refer to `references/agentic-best-practices.md`
   - Match user needs to relevant templates and patterns

3. **Compose the Prompt**
   - Start with core instructions using explicit, directive language
   - Add context and motivation where it improves understanding
   - Include relevant prompt snippets from templates
   - Use XML tags to structure complex multi-part prompts
   - Frame instructions positively (what TO do vs what NOT to do)

4. **Test and Iterate**
   - Recommend the user test the prompt with real scenarios
   - Suggest adjustments based on observed behavior
   - Remind users that prompts can be iteratively refined

## Common Scenarios

This skill includes detailed prompt templates for common scenarios in `references/prompt-templates.md`:

- **Proactive Action**: Make agents more or less proactive about tool use
- **Verbosity Control**: Control output formatting and reduce excessive markdown
- **Parallel Tool Calls**: Optimize simultaneous operations
- **Long-Horizon Tasks**: Setup multi-context-window workflows
- **Research & Search**: Improve information gathering and synthesis
- **Subagent Orchestration**: Delegate work to specialized subagents
- **Document Creation**: Enhance presentations and visual documents
- **Coding & Frontend**: Generate high-quality, visually distinctive UIs
- **Hallucination Reduction**: Minimize speculation and improve accuracy
- **State Management**: Track progress across long tasks

For comprehensive reference material covering all prompt engineering best practices, see `references/agentic-best-practices.md`.

## Resources

### references/

**prompt-templates.md** - Categorized collection of proven prompt snippets organized by scenario. Load this when the user needs specific prompt patterns for common use cases.

**agentic-best-practices.md** - Comprehensive reference material covering all prompt engineering principles and advanced techniques for agentic workflows. Load this for deep dives or complex scenarios.

## Best Practices

- **Use XML tags for structure**: Wrap complex instructions in XML tags (e.g., `<use_parallel_tool_calls>...</use_parallel_tool_calls>`)
- **Provide context, not just rules**: Explain WHY a behavior is important
- **Match prompt style to output style**: If minimal markdown is desired, use minimal markdown in the prompt
- **Be specific about model identity**: Include model information when needed if relevant to the system
- **Test iteratively**: Encourage users to test and refine prompts based on real usage
