# Final Checklist Before Distribution

Verify all items before sharing a skill.

## Core Quality

- [ ] Name is ≤ 64 characters, lowercase + hyphens only
- [ ] Description is specific and includes key terms
- [ ] Description includes both what the Skill does AND when to use it
- [ ] Description uses third person ("Processes..." not "I process...")
- [ ] SKILL.md body is under **500 lines**
- [ ] Additional details are in separate reference files
- [ ] No time-sensitive information (or in "old patterns" section)
- [ ] Consistent terminology throughout
- [ ] Examples are concrete, not abstract
- [ ] File references are **one level deep** from SKILL.md
- [ ] Progressive disclosure used appropriately
- [ ] Workflows have clear steps
- [ ] Skill Chaining section documented (if interacts with others)

## Folder Structure

- [ ] SKILL.md exists at root
- [ ] `scripts/` contains executable code only
- [ ] `references/` contains documentation for context loading
- [ ] `assets/` contains output resources (templates, images)
- [ ] No extraneous files (README.md, CHANGELOG.md, etc.)
- [ ] All paths use forward slashes (not Windows backslashes)

## Code and Scripts

- [ ] Scripts solve problems rather than punt to Claude
- [ ] Error handling is explicit and helpful
- [ ] No "voodoo constants" (all values documented)
- [ ] Required packages listed in instructions
- [ ] Scripts tested and working
- [ ] MCP tools use fully qualified names (`Server:tool_name`)

## Reference Files

- [ ] Files > 100 lines have table of contents at top
- [ ] No nested references (all link directly from SKILL.md)
- [ ] Each reference file clearly referenced from SKILL.md
- [ ] Content not duplicated between SKILL.md and references

## Testing

- [ ] At least three evaluation scenarios created
- [ ] Tested with real usage scenarios
- [ ] Tested with target models (Haiku/Sonnet/Opus if multi-model)
- [ ] Team feedback incorporated (if applicable)

## Quality Score

Calculate average across 9 dimensions:

| Dimension | Score (1-5) |
|-----------|-------------|
| Clarity | |
| Completeness | |
| Discoverability | |
| Context Efficiency | |
| Actionability | |
| Resource Organization | |
| Examples | |
| Skill Chaining | |
| Error Handling | |
| **Average** | |

**Minimum for production**: 3.5/5
**Excellence target**: 4.5/5

## Package Command

Once all checks pass:

```bash
scripts/package_skill.py <path/to/skill-folder>
```
