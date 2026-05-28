---
name: example-skill
description: An example skill demonstrating the agentskills.io format with all optional sections included
license: MIT
compatibility: Works with any environment that supports markdown files
metadata:
  author: Menlo Project
  version: 1.0.0
  category: example
---

# Example Skill

This is an example skill that demonstrates the proper structure and format for agentskills.io compatible skills.

## Purpose

Use this skill as a template when creating new skills. It shows:

- Required YAML frontmatter with name and description
- Optional frontmatter fields (license, compatibility, metadata)
- Proper markdown structure in the body
- How to reference scripts, assets, and documentation

## Usage

When creating a new skill:

1. **Copy this directory structure**:
   ```
   skill-name/
   ├── SKILL.md
   ├── scripts/       (optional)
   ├── references/    (optional)
   └── assets/        (optional)
   ```

2. **Update the YAML frontmatter** with your skill's name and description

3. **Write clear instructions** in the body explaining:
   - What the skill does
   - When to use it
   - Step-by-step instructions
   - Examples
   - Edge cases or limitations

4. **Add supporting materials** (optional):
   - Put executable code in `scripts/`
   - Put detailed documentation in `references/`
   - Put templates or resources in `assets/`

## Examples

### Input
A task that matches the skill's description

### Output
Expected result after following the skill's instructions

### Edge Cases
- What happens if X occurs
- How to handle Y situation
- Limitations or constraints

## Best Practices

- Keep the description field clear and specific so agents know when to use this skill
- Keep SKILL.md under 5000 tokens for optimal performance
- Use progressive disclosure: put detailed docs in references/ instead of the main file
- Provide concrete examples
- List any dependencies or requirements in the compatibility field

## References

For detailed information, see:
- `references/detailed-guide.md` - In-depth documentation
- `scripts/example.sh` - Example script
- `assets/template.txt` - Template file

## Notes

This is a meta-skill used only for demonstration. Delete this folder when you create your first real skill, or keep it as a reference.
