# Documentation Update Triggers

## When to Update CLAUDE.md

- New agent added to plugin
- New slash command created
- Architecture pattern changes
- Build process changes
- New testing patterns established

## When to Update Skill References

| Change | Update |
|--------|--------|
| API changes | board-sdk, unity-mcp-tools |
| New game rules interpretation | zero-day-rules |
| Layout constant changes | layout-sizing |
| Color palette updates | visual-style-guide |
| New code patterns | project-architecture |
| Test structure changes | unity-testing |

## When to Update SKILL.md

- After reference folder is complete
- When trigger phrases need adjustment
- When agent guidance changes
- After major workflow updates

## Project-Producer Responsibilities

The project-producer agent should:
1. Verify documentation matches implementation
2. Update references after significant code changes
3. Capture learnings from development sessions
4. Maintain CLAUDE.md accuracy

## Automation Hooks

Consider update triggers for:
- Post-commit documentation review
- Sprint/milestone documentation audit
- New feature documentation checklist
