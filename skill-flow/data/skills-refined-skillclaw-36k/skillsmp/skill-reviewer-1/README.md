# Skill Reviewer

Reviews Claude Code skills against official best practices and quality standards from Anthropic's skill authoring guide.

## Features

- Validates YAML frontmatter (name, description, allowed-tools)
- Checks SKILL.md length (target: under 500 lines)
- Verifies progressive disclosure patterns
- Assesses description specificity and quality
- Reviews scripts for security and best practices
- Provides structured feedback with severity levels

## Files

- `SKILL.md` - Main skill definition and workflow
- `REFERENCE.md` - Detailed technical specifications and official checklist

## Usage

Invoke when reviewing SKILL.md files, auditing skill quality, or validating against official best practices.

## Acknowledgments

Originally from [caoer](https://github.com/caoer).
