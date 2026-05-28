# Detailed Guide

This is a reference document that provides in-depth information about the skill.

## Why Use References?

Reference files allow you to:
- Keep SKILL.md concise and focused
- Provide detailed documentation that loads only when needed
- Organize information into logical sections
- Reduce initial context load

## When to Use References

Use reference files when:
- You have detailed technical documentation
- You need to explain complex concepts
- You want to provide extensive examples
- The information is only needed occasionally

## Progressive Disclosure

The agentskills.io approach uses progressive disclosure:

1. **First**: Agent sees skill name + description (~100 tokens)
2. **Then**: Agent reads SKILL.md when task matches (~1000-5000 tokens)
3. **Finally**: Agent loads reference files only if specifically needed

This keeps context usage efficient while providing comprehensive documentation when required.

## Best Practices

- Keep SKILL.md focused on "how to use this skill"
- Put background information, theory, or extensive details here
- Link to reference files from SKILL.md
- Organize references by topic (e.g., `api-reference.md`, `troubleshooting.md`)
