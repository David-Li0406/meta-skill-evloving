# How to Use the Git Batch Commit Skill

Hey Claude—I just added the "git-batch-commit" skill. Can you analyze my git staging area and create appropriate batch commits?

## Example Invocations

### Example 1: Basic Batch Commit Analysis

**Request:**
```
Hey Claude—I just added the "git-batch-commit" skill. Can you analyze my repository and tell me if I should batch these commits?
```

**What Claude Will Do:**
- Check git status (staged, modified, untracked files)
- Count total files
- Compare against threshold (default: 10 files)
- Recommend batching strategy if needed
- Show preview of proposed batches

---

### Example 2: Create Batch Commits in English

**Request:**
```
Hey Claude—I just added the "git-batch-commit" skill. Can you create batch commits for all my staged files with English commit messages?
```

**What Claude Will Do:**
- Analyze all staged files
- Group files by feature/functionality (auth, api, docs, etc.)
- Generate Conventional Commit messages (feat/fix/docs/etc.)
- Create commits in English
- Provide execution summary

---

### Example 3: Create Batch Commits in Chinese

**Request:**
```
Hey Claude—I just added the "git-batch-commit" skill. Can you create batch commits in Chinese for these changes?
```

**What Claude Will Do:**
- Same analysis and grouping
- Generate commit messages in Chinese
- Example output: `feat(auth): 新增OAuth2认证功能`
- Maintain Conventional Commits format with Chinese descriptions

---

### Example 4: Custom Threshold

**Request:**
```
Hey Claude—I just added the "git-batch-commit" skill. Can you use a threshold of 15 files and batch my commits?
```

**What Claude Will Do:**
- Use custom threshold (15 instead of default 10)
- Only recommend batching if > 15 files
- Adjust batch sizes accordingly

---

### Example 5: Dry Run Preview

**Request:**
```
Hey Claude—I just added the "git-batch-commit" skill. Can you preview what batch commits would be created without actually committing?
```

**What Claude Will Do:**
- Analyze repository state
- Generate batch plans
- Show detailed preview of each batch
- Display commit messages
- No actual commits created (dry run mode)

---

### Example 6: Specific Commit Types

**Request:**
```
Hey Claude—I just added the "git-batch-commit" skill. Can you group these changes using 'feat' and 'refactor' commit types only?
```

**What Claude Will Do:**
- Filter files to match requested commit types
- Group accordingly
- Focus on feature additions and refactorings
- Separate other changes if needed

---

## What to Provide

**Required:**
- Git repository with staged/modified/untracked files

**Optional:**
- Language preference (en, zh, es, ja, etc.)
- Custom threshold value
- Specific commit types to use
- Scope preferences

**Examples of Providing Context:**
```
"Use Chinese for commit messages"
"Set threshold to 8 files"
"Focus on feat and fix commits"
"Use scopes: auth, api, database"
```

---

## What You'll Get

### Analysis Report
```json
{
  "total_files": 18,
  "threshold": 10,
  "requires_batching": true,
  "recommended_batches": 7
}
```

### Batch Plans
```
Batch 1: feat(auth) - 3 files
  - src/auth/login.py
  - src/auth/oauth.py
  - src/api/auth_endpoints.py

Commit Message:
feat(auth): add OAuth2 authentication functionality
```

### Execution Summary
```
✓ Completed 7/7 commits
  - 4 feat commits
  - 1 docs commit
  - 1 chore commit
  - 1 test commit
```

---

## Conventional Commit Types Explained

| Type | When to Use | Example |
|------|-------------|---------|
| **feat** | New features or functionality | `feat(auth): add OAuth2 login support` |
| **fix** | Bug fixes | `fix(api): resolve null pointer exception` |
| **docs** | Documentation changes only | `docs(readme): update installation guide` |
| **refactor** | Code restructuring without features | `refactor(database): optimize query logic` |
| **chore** | Maintenance (deps, configs) | `chore(deps): update dependencies` |
| **style** | Code formatting/style | `style(ui): format component styles` |
| **test** | Adding or updating tests | `test(auth): add OAuth unit tests` |
| **perf** | Performance improvements | `perf(api): optimize response caching` |

---

## Best Practices

### 1. Review Before Committing
Always review the proposed batches and commit messages before execution. Use dry-run mode first:
```
"Preview batch commits without executing"
```

### 2. Use Meaningful Scopes
Ensure scopes match your project structure:
- `auth` - Authentication/authorization
- `api` - API endpoints
- `ui` - User interface
- `database` - Database/models
- `core` - Core functionality

### 3. Keep Language Consistent
Choose one language for commit messages per project:
- Team projects: Usually English
- Personal projects: Your preference
- Open source: English recommended

### 4. Adjust Threshold for Project Size
- Small projects: 5-8 files
- Medium projects: 10-15 files
- Large projects: 15-20 files

### 5. Atomic Commits
Each batch should represent one cohesive change:
- ✅ All auth-related changes in one commit
- ✅ All documentation updates in one commit
- ❌ Random mix of unrelated files

---

## Troubleshooting

### Issue: Too Many Batches Created
**Solution:** Increase threshold
```
"Use threshold of 20 files"
```

### Issue: Files Grouped Incorrectly
**Solution:** Specify scopes manually
```
"Group files by: auth, api, frontend, backend"
```

### Issue: Wrong Commit Type Detected
**Solution:** Override commit type
```
"Use 'refactor' type for database changes"
```

### Issue: Commit Messages Too Generic
**Solution:** Provide context about changes
```
"These changes add OAuth2 support with Google provider integration"
```

---

## Configuration File (Optional)

Create `git_batch_config.json` in your repository:

```json
{
  "threshold": 12,
  "default_language": "en",
  "preferred_scopes": ["auth", "api", "ui", "database"],
  "commit_types": ["feat", "fix", "docs", "refactor", "chore"],
  "auto_execute": false
}
```

**Settings Explained:**
- `threshold`: Max files before batching recommended
- `default_language`: Commit message language
- `preferred_scopes`: Project-specific scopes
- `commit_types`: Allowed commit types
- `auto_execute`: Auto-commit without preview (use with caution!)

---

## Advanced Usage

### Combine with Git Hooks
Use with pre-commit hooks for validation:
```
"Create batch commits and run pre-commit checks"
```

### Multi-Language Teams
Alternate languages by developer:
```
"Create commits in Chinese for Chinese developers, English for others"
```

### Custom Grouping Logic
Override default grouping:
```
"Group all frontend files together regardless of feature"
```

---

## Safety Features

✅ **Dry-run mode** - Preview before committing
✅ **Rollback support** - Can amend or reset if needed
✅ **Conflict detection** - Warns about file dependencies
✅ **Validation** - Checks for unstaged critical files
✅ **Review required** - Never auto-commits without confirmation

---

**Need Help?**
Ask Claude specific questions about batch commits:
- "What commit type should I use for database migrations?"
- "How do I customize scopes for my project?"
- "Can you explain why files were grouped this way?"
