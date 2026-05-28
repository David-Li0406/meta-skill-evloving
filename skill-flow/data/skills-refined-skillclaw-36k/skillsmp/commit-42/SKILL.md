---
name: commit
description: Create a git commit following the project's gitmoji workflow with verification. Use when (1) user wants to commit staged changes, (2) user invokes /commit command, (3) user asks to create a commit. Triggers on "commit", "git commit", "create commit", "stage and commit".
---

# Commit Skill

Goal: Analyze staged git changes and generate a commit message following the pattern: `<gitmoji> <short description>`

The user input to you can be provided directly by the agent or as a command argument - you **MUST** consider it before proceeding with the prompt (if not empty).

You **MUST** always use the text form for the emojis in the commit message (e.g., `:sparkles:` instead of the Unicode character emoji ✨).

Always use the users' GPG key for signing commits. If this fails, ask the user to provide the GPG key and unlock it so that the commit can be signed.

You **MUST** never use the `--no-gpg-sign` without user confirmation.

User input:

$ARGUMENTS

# Argument Parsing

Parse the following optional flags from $ARGUMENTS:

- `--no-verify` or `-n`: Skip pre-commit hooks when creating the commit
- `--emoji <emoji>` or `-e <emoji>`: Use specific gitmoji (e.g., `--emoji ✨` or `--emoji :sparkles:`)

Examples:
- `/commit` - Normal commit with hooks
- `/commit --no-verify` - Skip hooks
- `/commit --emoji 🐛` - Use specific emoji
- `/commit --emoji ♻️ --no-verify` - Specific emoji and skip hooks

Any remaining text after flags is treated as additional context for the commit message.

# Configuration

## Step 0: Load Configuration

The PostToolUse hook **injects validated config into your context** via `additionalContext`. The config summary looks like:

```
Gitmoji: true/false (N custom)    # "(N custom)" only if custom emojis defined
Run hooks by default: true/false
Co-author attribution: true/false
Message template: {pattern}        # only if configured
Body template: configured          # only if configured
```

**DISPLAY REQUIREMENT:** When you receive the injected config, you MUST immediately display it to the user with this format:

**Active Commit Config:**
```
<paste the exact config here>
```

This gives users visibility into their active configuration before proceeding. If no config appears, use default values.

**Config structure:**
```yaml
gitmoji:
  enabled: true  # Use gitmoji in commit messages
  custom:        # Optional: extend built-in emoji list
    - emoji: "🎯"
      code: ":dart:"
      description: "Focus on goal"

hooks:
  runByDefault: true  # Run pre-commit hooks by default

format:
  coAuthor: false  # Add co-authored-by attribution
  messageTemplate: "{emoji} {type}({scope}): {description}"  # Optional pattern
  bodyTemplate: |  # Optional multiline body
    {body}
    BREAKING CHANGE: {breaking}
    Closes: {issues}
```

**Behavior based on config:**
- If `gitmoji.enabled: false` - Skip Step 2 (Determine Gitmoji) entirely, proceed without gitmoji
- If `gitmoji.custom` defined - Include custom emojis in the selection options
- If `hooks.runByDefault: false` - Treat as if `--no-verify` flag was passed
- If `format.coAuthor: true` - Add co-authored-by attribution to commit message
- If `format.messageTemplate` defined - Use template for message format
- If `format.bodyTemplate` defined - Ask for body content in Step 4
- If config file is missing - Use defaults (gitmoji enabled, hooks enabled, no co-author)

**Override rules:**
- Command-line flags (`--no-verify`, `--emoji`) always override config
- Config overrides defaults
- Defaults are: gitmoji enabled, hooks enabled, no co-author, no template

# Execution steps:

## Step 1: Analyze the changes

- Run `git status` to verify there are staged changes
- Run `git diff --cached` to see the actual staged changes
- If no changes are staged, inform the user and stop
- Review the staged changes to understand what was modified
- Identify the primary type of change (feature, bugfix, refactor, etc.)
- Are there multiple logical changes that should be separate commits?
- If `--emoji` flag was provided, use that gitmoji; otherwise determine the most appropriate one


## Step 2: Determine Gitmoji

**If gitmoji is disabled (`gitmoji.enabled: false` in config):**
- Skip this step entirely
- Proceed to Step 3 without gitmoji

**If `--emoji` flag was provided:**
- Use the specified emoji directly
- Skip to Step 3

**If no `--emoji` flag and gitmoji is enabled:**
- Analyze the changes and determine 2-3 most suitable gitmojis
- Include custom emojis from config if "(N custom)" appears in config summary
- Use AskUserQuestion to let the user select their preferred gitmoji

**Built-in gitmojis:**
- ✨ `:sparkles:` - New feature (type: feat)
- 🐛 `:bug:` - Bug fix (type: fix)
- 🔧 `:wrench:` - Configuration changes (type: chore)
- ♻️ `:recycle:` - Code refactoring (type: refactor)
- ✅ `:white_check_mark:` - Add/update tests (type: test)
- 📝 `:memo:` - Documentation (type: docs)
- 🎨 `:art:` - Code style/formatting (type: style)
- ⚡ `:zap:` - Performance improvements (type: perf)
- 🔥 `:fire:` - Remove code/files (type: chore)

**Custom gitmojis (from config):**
If the config summary shows custom emojis (e.g., "2 custom"), include them in the selection options alongside the built-in ones. The custom emojis were defined by the user in their `.claude/commit.yaml`.

## Step 3: Suggest Commit Message

Based on the changes and config settings, suggest a commit message.

**If message template is configured (`Message template:` in config summary):**
1. Parse the template placeholders: `{emoji}`, `{type}`, `{scope}`, `{description}`
2. For `{type}`: Infer from the selected gitmoji (see emoji-to-type mapping in Step 2)
3. For `{scope}`: Infer from the changed files/directories, or ask if ambiguous
4. Assemble message by replacing placeholders

**Template examples with `{emoji} {type}({scope}): {description}`:**
- `✨ feat(auth): add user authentication endpoint`
- `🐛 fix(api): resolve null pointer in message handler`
- `♻️ refactor(dlq): migrate DLQ service to use Avro schema`

**If no message template (default behavior):**

With gitmoji enabled:
```
<gitmoji> <short description>
```
Examples: `✨ add user authentication endpoint`, `🐛 fix null pointer`

Without gitmoji:
```
<short description>
```
Examples: `add user authentication endpoint`, `fix null pointer`

## Step 4: Body Template (Optional)

**Skip this step if no body template is configured** (no `Body template: configured` in summary).

**If body template is configured:**
1. Ask user if they want to add a commit body using AskUserQuestion:
   - "Yes, add body" - collect body information
   - "No, skip" - proceed without body

2. If adding body, collect information for placeholders:
   - `{body}`: Main body text describing the change in more detail
   - `{breaking}`: Breaking change description (or empty if none)
   - `{issues}`: Issue numbers this commit addresses (e.g., #123, #456)

3. Assemble body by replacing placeholders, omitting empty sections

## Step 5: Confirm and Create Commit

**Present the proposed commit:**
1. Show the complete commit message (subject line + body if configured)
2. Show summary of files being committed
3. Note whether hooks will run or be skipped

**Use AskUserQuestion for confirmation with these options:**
- "Yes, create commit" - Proceed with commit
- "No, cancel" - Abort the commit
- "Edit message" - Let user modify the message before committing

**Option handling:**
- **"Yes, create commit"**: Proceed to create the commit
- **"No, cancel"**: Inform user commit was cancelled
- **"Edit message"**: Ask what to change, apply changes, then ask for confirmation again

**Determine if hooks should run:**
- If `--no-verify` flag was provided: Skip hooks
- Else if `hooks.runByDefault: false` in config: Skip hooks
- Otherwise: Run hooks

**Create the commit:**
1. Verify files are staged (they should be from Step 1)
2. Create the commit using the approved message
3. Add `--no-verify` flag if hooks should be skipped
4. Add co-authored-by attribution if `format.coAuthor: true` in config
5. Show the commit hash and summary

**Co-authored-by format** (only if `format.coAuthor: true`):
```
<commit message>

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

**Commit command format:**

To reduce context window usage, capture output to temp file and only show if commit fails:

```bash
# Normal commit - capture output, only show on failure
TMPFILE=$(mktemp) && git commit -m "<message>" > "$TMPFILE" 2>&1 && echo "✓ Commit successful (hook output suppressed)" || (echo "✗ Commit failed, showing output:" && cat "$TMPFILE"); rm -f "$TMPFILE"

# Skip hooks
git commit -m "<message>" --no-verify
```

## Step 6: Handle Hook Failures

If the pre-commit hook fails, provide a clean summary:

**Summarize the failure:**
Parse the hook output and identify:
- ESLint errors: Count of files with issues, sample error message
- Prettier errors: Files that need formatting
- Test failures: Which test suites/tests failed
- Other errors: General error message

**Present clean summary:**
```
Pre-commit hook failed:
- ESLint: 3 files with errors (src/auth.ts, src/api.ts, src/utils.ts)
- First error: 'foo' is defined but never used (no-unused-vars)
```

**Offer options via AskUserQuestion:**
- "Fix issues" - Analyze errors and suggest/apply fixes
- "Show full output" - Display the complete hook output
- "Skip hooks (--no-verify)" - Retry the commit without hooks
- "Cancel" - Abort and let user fix manually

**If user chooses "Fix issues":**
1. Review the specific errors
2. Apply fixes to the affected files
3. Re-stage the fixed files with `git add`
4. Retry the commit automatically
