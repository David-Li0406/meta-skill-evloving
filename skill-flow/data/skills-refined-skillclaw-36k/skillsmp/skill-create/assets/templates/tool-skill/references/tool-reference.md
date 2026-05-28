# Tool Skill Reference

Guidance for skills that manipulate files, formats, or APIs.

## Design Principles
- Make scripts deterministic and idempotent
- Keep SKILL.md brief; place format details here
- Document required inputs (paths, credentials, flags)
- Provide sample commands and expected outputs

## Template Sections
- Supported inputs/outputs
- Pre-flight checks
- Processing steps (link to scripts)
- Validation commands
- Error handling and recovery steps

## Example Triggers
- "This skill should be used when cleaning or splitting PDF files"
- "Use when normalizing JSON exports from Service X"
- "Invoke when calling the internal API for batch updates"

## Checklist
- [ ] Scripts cover the repeated operations
- [ ] Validation commands are runnable
- [ ] Third-person description includes trigger words
- [ ] Edge cases documented (unsupported formats, size limits)

## Anti-Patterns
- Manual steps repeated each time (automate via scripts)
- Missing validation for produced artifacts
- Ambiguous description that doesn't mention the tool or format
