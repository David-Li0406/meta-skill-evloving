# PromptL Skill

A Claude Code skill that helps LLMs write PromptL prompts for the [Latitude](https://latitude.so) platform.

## What is PromptL?

PromptL is a versatile, human-readable language that simplifies defining and managing dynamic prompts for LLMs. It offers:

- **Readable syntax** - Easy to write and maintain
- **Dynamic flexibility** - Variables, conditionals, and loops
- **Powerful logic** - Chains, agents, and tool integrations

## Installation

Copy the skill to your Claude Code skills directory:

```bash
# Clone the repository
git clone https://github.com/latitude-dev/promptl-skill.git

# Copy to Claude Code skills directory
cp -r promptl-skill ~/.claude/skills/promptl
```

Or manually create the directory and copy the files:

```bash
mkdir -p ~/.claude/skills/promptl
cp SKILL.md AGENTS.md ~/.claude/skills/promptl/
```

## Usage

Once installed, the skill will automatically activate when you're working on tasks involving:

- Writing PromptL prompts
- Configuring LLM parameters
- Using variables, conditionals, or loops
- Creating multi-step chains
- Defining tools or agents
- Working with structured JSON output

You can also explicitly invoke it with `/promptl`.

## What's Included

### SKILL.md

Quick reference guide with:
- Syntax categories overview
- Quick reference for all features
- When to apply the skill

### AGENTS.md

Comprehensive documentation covering:

1. **Prompt Structure** - Config section and message content
2. **Configuration** - YAML frontmatter options
3. **Messages** - System, user, assistant, and tool tags
4. **Variables** - Dynamic content with `{{ }}`
5. **Conditionals** - `if`/`else`/`endif` blocks
6. **Loops** - `for`/`endfor` iteration
7. **Chains and Steps** - Multi-step workflows
8. **Tools** - Function calling definitions
9. **Agents** - Autonomous AI workflows
10. **Prompt References** - Reusable snippets
11. **Content Types** - Images, files, and more
12. **Mocking** - Testing and development
13. **Structured Output** - JSON schema validation
14. **Best Practices** - Do's and don'ts

## Example

Here's a simple PromptL prompt:

```
---
provider: OpenAI
model: gpt-4o
temperature: 0.7
---

You are a helpful assistant.

<user>
  Tell me a joke about {{ topic }}.
</user>
```

And a more advanced agent:

```yaml
---
provider: OpenAI
model: gpt-4o
type: agent
maxSteps: 40
tools:
  - latitude/search
schema:
  type: object
  properties:
    summary:
      type: string
    key_points:
      type: array
      items:
        type: string
  required:
    - summary
    - key_points
---

Research {{ topic }} and provide a structured summary.
```

## Resources

- [Latitude Documentation](https://docs.latitude.so)
- [PromptL Syntax Guide](https://docs.latitude.so/promptl/syntax)
- [Claude Code](https://docs.anthropic.com/claude-code)

## License

MIT License - see [LICENSE](LICENSE) for details.
