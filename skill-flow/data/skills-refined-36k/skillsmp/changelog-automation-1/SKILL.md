---
name: changelog-automation
description: Use this skill immediately AFTER a successful git commit to update the project CHANGELOG.md.
---

# Changelog Automation Protocol

## 1. Trigger
- This skill should be invoked after you receive confirmation that a commit was successful.

## 2. Formatting
- Open (or create) `CHANGELOG.md` in the project root.
- Add a new entry under the `## [Unreleased]` header or the current date.
- Use the format: `- <type>: <description> (commit_hash)`

## 3. Automation
- You may update the `CHANGELOG.md` file automatically, but you must inform the user: "Updated CHANGELOG.md with the latest changes."
- **Note:** Do not create a new commit for the changelog update unless the user asks; typically, this is staged for the *next* release cycle or amended to the current one.
