# Prompting Skill

> **Install:** `npx skills add diskd-ai/prompting` | [skills.sh](https://skills.sh)

Prompt engineering guidance for writing and improving LLM prompts.

---

## Scope & Purpose

This skill provides guidance for crafting effective prompts for any LLM (Claude, GPT, Gemini, Llama, etc.), covering:

* Writing new prompts from scratch
* Reviewing and improving existing prompts
* Designing system prompts for AI assistants
* Structuring prompts for specific output formats (JSON, XML, markdown)
* Applying prompt engineering techniques

---

## When to Use This Skill

**Triggers:**
* Asked to write a prompt for a specific task
* Need to review or improve an existing prompt
* Designing system prompts for AI assistants
* Structuring prompts for specific output formats
* Applying techniques like few-shot, chain-of-thought, or role prompting

---

## Quick Reference: Techniques

| Technique | When to Use |
|-----------|-------------|
| Few-shot | Specific format/style needed |
| Chain-of-thought | Complex reasoning, math, analysis |
| Role prompting | Domain expertise, specific tone |
| Task decomposition | Multi-step workflows |
| Constraints | Precise requirements |

---

## Quick Reference: Output Formats

| Format | When to Use |
|--------|-------------|
| XML tags | Complex prompts, clear section boundaries |
| JSON | Programmatic parsing, structured data |
| Markdown | Human-readable reports, documentation |

---

## Prompt Template

```
[Context/Role - optional]
[Task - required]
[Constraints/Requirements - as needed]
[Output format - as needed]
[Examples - for complex tasks]
```

---

## Skill Structure

```
prompting/
  SKILL.md          # Full prompt engineering guide
  README.md         # This file (overview)
  references/       # Supporting documentation
    techniques.md   # Detailed technique patterns
    structured.md   # Output format patterns
    system-prompts.md # System prompt design
```

---

## Resources

* **Full skill reference**: [SKILL.md](SKILL.md)
* **Techniques guide**: [references/techniques.md](references/techniques.md)
* **Structured outputs**: [references/structured.md](references/structured.md)
* **System prompts**: [references/system-prompts.md](references/system-prompts.md)

---

## License

MIT
