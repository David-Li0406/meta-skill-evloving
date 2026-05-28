---
name: auto-sync-and-refactor
description: Use this skill when you need to perform batch updates or refactorings across multiple repositories based on detected patterns.
---

# Skill body

## When to Use

This skill is applicable when you encounter recurring patterns in multiple repositories, such as batch updates or refactoring tasks. It helps streamline operations by providing a common implementation approach.

## Implementation

1. **Identify the Pattern**: Determine the specific pattern that has been detected across repositories (e.g., "Auto-sync: batch update" or "refactor: Migrate CLAUDE.md to inheritance model").
2. **Gather Context**: Review the repositories where the pattern was found to understand the context and variations.
3. **Plan the Update/Refactor**:
   - For batch updates, outline the changes needed across all identified repositories.
   - For refactoring, define the new structure or model to be implemented.
4. **Execute Changes**: Apply the updates or refactorings consistently across all repositories.
5. **Test and Validate**: Ensure that the changes work as intended in each repository and do not introduce errors.

## Examples

*Examples extracted from commit history:*

```
Pattern: Auto-sync: batch update 2026-01-14
Repos: OGManufacturing, achantas-media, acma-projects, ai-native-traditional-eng, assethold, assetutilities, client_projects, doris, energy, frontierdeepwater, hobbies, investments, pdf-large-reader, pyproject-starter, rock-oil-field, sabithaandkrishnaestates, saipem, sd-work, seanation, teamresumes

Pattern: refactor: Migrate CLAUDE.md to inheritance model
Repos: OGManufacturing, aceengineer-admin, aceengineer-website, achantas-media, ai-native-traditional-eng, assethold, client_projects, energy, frontierdeepwater, hobbies, pyproject-starter, rock-oil-field, sabithaandkrishnaestates, saipem, sd-work, seanation, teamresumes
```