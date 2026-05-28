# Parallel Agent Workflow

Coordinate multiple agents working in parallel using git worktrees to avoid file conflicts.

## Features

- Split work across N agents, each in isolated git worktree
- Agents work independently on different components/files
- Staged merge strategy (N agents → M groups → 1 final)
- Automatic conflict resolution with surfacing
- Template agent prompts for consistent execution

## Use Cases

- Multi-component refactoring
- Parallel feature development
- Large-scale codebase changes

## Files

- `SKILL.md` - Main skill definition and workflow

## Acknowledgments

Originally from [caoer](https://github.com/caoer).
