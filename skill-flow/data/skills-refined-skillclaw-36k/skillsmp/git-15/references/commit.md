# Git Commit

Analyzes changes and creates a commit with a Conventional Commits format message.

## Parameters

`$ARGUMENTS`: Optional commit message. Uses provided message if given, auto-generates if not.

## Workflow

### 1. Collect Changes (without staging)

```bash
git status
git diff --cached  # Check already staged files
git diff           # Changes not yet staged
git branch --show-current
```

### 2. Branch Processing

**A) Already staged files exist** → Commit only those files (skip split analysis, go to step 5)

**B) No staged files** → Proceed to step 3

### 3. Logical Change Analysis

Core summary from collected information:
- Which files were changed?
- What kind of changes? (add/modify/delete)
- What is the purpose of the changes?
- **Check if changes with multiple purposes are mixed**
  - Detect when different features/bugs/refactoring are mixed
  - Example: feat + fix, refactor + feat, etc.

### 4. Suggest Split When Needed

When 2 or more logical changes detected, suggest split commit to user (AskUserQuestion):

```json
{
  "questions": [{
    "header": "Commit Split",
    "question": "2 logical changes detected:\n1. ✨ feat: Add login form\n2. 🐛 fix: Session expiry bug\n\nSplit into separate commits?",
    "multiSelect": false,
    "options": [
      { "label": "Split", "description": "Separate into 2 commits" },
      { "label": "Combine", "description": "Keep as single commit" }
    ]
  }]
}
```

### 5. Determine Commit Message

**If $ARGUMENTS provided**: Use that message as description

**If $ARGUMENTS not provided**: Auto-generate message based on changes

### 6. Type & Emoji Inference

See [commit-prefix-rules.md](commit-prefix-rules.md)

Inference priority:
1. Branch name (feature/*, fix/*, hotfix/*, docs/*, etc.)
2. Changed file paths/extensions
3. Diff content analysis
4. Default: `feat`

### 7. Stage & Execute Commit

**Split Y** → Selective git add per file + commit each (repeat)

```bash
# First change
git add src/login.tsx src/auth.ts
git commit -m "<emoji> <type>: message"

# Second change
git add src/session.ts
git commit -m "<emoji> <type>: message"
```

**Split N** → git add . + single commit

```bash
git add .
git commit -m "<emoji> <type>: message subject

- detailed change 1
- detailed change 2"
```

## Commit Message Format (Conventional Commits)

```
<emoji> <type>[scope][!]: <description>

- [detailed change 1]
- [detailed change 2]
```

### Type & Emoji Map

| Type | Emoji |
|------|-------|
| `feat` | ✨ |
| `fix` | 🐛 |
| `docs` | 📝 |
| `style` | 💄 |
| `refactor` | ♻️ |
| `perf` | ⚡ |
| `test` | ✅ |
| `chore` | 🔧 |
| `ci` | 🚀 |
| `build` | 📦 |
| `revert` | ⏪ |

## Examples

### When $ARGUMENTS provided

Input: `Fix login bug`

Output:
```
🐛 fix: Fix login bug

- Fix session expiry handling logic
- Improve error messages
```

### When $ARGUMENTS not provided

Change: New file `src/components/Header.tsx` added

Output:
```
✨ feat: Add Header component

- Implement responsive navigation
- Render logo and menu items
```

### Example with Scope

Input: `Fix auth token refresh error`

Output:
```
🐛 fix(auth): Fix auth token refresh error

- Adjust token refresh timing
- Improve error handling
```

### Breaking Change Example

Input: `Change API response structure (Breaking)`

Output:
```
✨ feat(api)!: Change API response structure

- response.data → response.items
- Add pagination metadata

BREAKING CHANGE: Existing API clients need modification
```

## Commit Message Rules

### Length Limits

- **Subject (first line)**: Under 72 characters (including emoji + type + scope)
- Body: 72 characters per line recommended

### Tone

- Use **imperative mood** (present tense, start with verb)
- ✅ "Add", "Fix", "Delete", "Improve", "Refactor"
- ❌ "Added", "Fixed", "Deleted"

### Atomic Commit Principle

- **Single purpose**: One commit contains only one logical change
- Split unrelated changes into separate commits
- Example: feat + fix mixed → Split into 2 commits

## Cautions

- Don't commit if no changes exist
- Warn if sensitive files (.env, credentials, etc.) are included
- Write commit messages in Korean
- Never add `Co-Authored-By` pattern
