---
name: semantic-commit
description: Use this skill to create semantic commits by logically splitting large changes into meaningful units and generating appropriate commit messages according to Conventional Commits.
---

# Semantic Commit Skill

This skill allows you to split large changes into meaningful units and generate semantic commit messages. It analyzes changes, classifies them, and automatically determines if they should be split into multiple commits.

## Detection Criteria for Large Changes

A change is detected as large if it meets any of the following criteria:

1. Number of changed files: 5 or more
2. Number of changed lines: 100 or more
3. Changes span multiple functionalities
4. Mixed patterns: combinations of feat, fix, and docs

```bash
# Analyze the scale of changes
CHANGED_FILES=$(git diff HEAD --name-only | wc -l)
CHANGED_LINES=$(git diff HEAD --stat | tail -1 | grep -o '[0-9]\+ insertions\|[0-9]\+ deletions' | awk '{sum+=$1} END {print sum}')

if [ $CHANGED_FILES -ge 5 ] || [ $CHANGED_LINES -ge 100 ]; then
  echo "Large change detected: splitting recommended"
fi
```

## Commit Creation Flow

### 1. Check Changes

```bash
git status
git diff
git diff --staged
git log --oneline -5
```

- Review changed files and diffs
- Refer to recent commit styles

### 2. Classification and Splitting Decision

Commits should be split if:

- Changes involve different functionalities
- Mixed types (e.g., feat and fix)
- Changes can be independently reverted
- The diff is too large (e.g., over 300 lines)

### 3. Generate Commit Messages

Follow the conventions outlined in the project guidelines to generate commit messages. The basic format is:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### 4. User Confirmation

If splitting is necessary, present the reasons and proposed splits to the user for confirmation. If no split is needed, proceed without confirmation.

### 5. Execute Commits

After confirmation, use `git add` and `git commit` to execute the commits. If splitting is required, stage and commit each logical group sequentially.

## Logical Grouping Criteria

1. **Functional Units**: Related files within the same functionality
2. **Change Types**: Group by type (e.g., test files, documentation)
3. **Dependencies**: Related files based on import relationships
4. **Change Scale**: Maintain appropriate commit sizes (e.g., no more than 10 files per commit)

## Example of Commit Splitting

### Before (Single Large Commit)

```
feat: implement complete user authentication system with login, registration, password reset, API routes, database models, tests and documentation
```

### After (Meaningful Splits)

1. `feat(db): add user model and authentication schema`
2. `feat(auth): implement core authentication functionality`
3. `feat(api): add authentication API routes`
4. `test(auth): add comprehensive authentication tests`
5. `docs(auth): add authentication documentation and configuration`

## Troubleshooting

### Commit Failures

- Check pre-commit hooks
- Resolve dependencies
- Retry on individual files

### Inappropriate Splitting

- Use manual `edit` mode
- Adjust with `--max-commits` option
- Re-run with finer granularity

## Best Practices

1. **Respect Project Guidelines**: Follow existing settings and patterns
2. **Small Change Units**: Each commit should represent a single logical change
3. **Clear Messages**: Ensure commit messages clearly describe changes
4. **Relevance**: Group functionally related files together
5. **Separate Tests**: Keep test files in separate commits

## Additional Resources

- Detailed implementation examples and Bash scripts: [reference.md](reference.md)
- Before/After splitting examples: [examples.md](examples.md)

## Note

- No automatic push: `git push` must be executed manually after commits.
- No branch creation: Commits are made on the current branch.
- Backup recommended: Use `git stash` for important changes before proceeding.