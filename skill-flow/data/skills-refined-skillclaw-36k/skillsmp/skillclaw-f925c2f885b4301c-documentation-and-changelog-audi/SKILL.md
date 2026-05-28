---
name: documentation-and-changelog-auditor
description: Use this skill to audit project documentation, including CHANGELOG.md, to ensure it accurately reflects code changes and is user-focused.
---

# Skill body

## Overview

This skill audits project documentation, including `CHANGELOG.md`, to identify and propose updates based on code changes. It ensures that documentation is user-focused and accurately reflects the current state of the codebase.

## Steps for Auditing Documentation

1. **Detect Changes**
   - Use `git diff --name-only` to identify changed files.

2. **Identify Related Documentation**
   - Based on the paths of changed files, determine which documentation needs to be audited.
   - If a project-specific configuration file `.claude/doc-audit.json` exists, use its settings to prioritize documents.

3. **Check Consistency**
   - Compare the content of the documentation with the actual code/configuration.
   - Ensure that:
     - New features are documented.
     - Deleted features are removed from documentation.
     - API changes are reflected in the documentation.

4. **Propose Updates**
   - For documents that require updates, provide specific suggestions:
     - Format: 
       ```markdown
       ## Documentation Audit Results

       ### Documents Needing Updates

       1. **CHANGELOG.md**
          - Reason: New features added that need to be documented.
          - Suggestion: Update the changelog to reflect these changes.

       2. **README.md**
          - Reason: New CLI options have been added.
          - Suggestion: Add to the "Usage" section.
       ```

5. **Execute Updates**
   - After user approval, implement the proposed updates to the documentation.

## Important Formatting and Content Rules for CHANGELOG.md

- Follow the [Keep a Changelog](https://keepachangelog.com/ja/1.0.0/) format.
- Document changes from the user's perspective, focusing on how changes affect their experience.
- Use links for PR or Issue numbers in the format `[#123](github.com/your-repo/issues/123)`.
- Clearly state the nature of changes, including any breaking changes and their implications.
- For bug fixes, describe the issues that were present and how they were resolved.
- Use Fully Qualified Class Names (FQCN) for class names, even if verbose.

## Tools Required
- Read
- Glob
- Grep
- Edit
- Write
- Bash