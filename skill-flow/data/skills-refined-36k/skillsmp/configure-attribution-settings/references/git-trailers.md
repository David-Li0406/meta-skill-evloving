# Git Trailers Reference

Technical reference for git trailers used in commit attribution.

## What Are Git Trailers?

Git trailers are key-value pairs that appear at the end of commit messages, following RFC 822 message header format. They provide structured metadata about commits.

### Official Documentation

From `git-interpret-trailers(1)`:

> Trailers are lines that look similar to RFC 822 e-mail headers, at the end of the
> otherwise free-form part of a commit message. For example:
>
> ```
> Signed-off-by: Alice <alice@example.com>
> Reviewed-by: Bob <bob@example.com>
> ```

## Standard Format

### Basic Syntax

```
Trailer-Key: Value
```

**Rules:**
- Key followed by colon and space
- Value on same line or continuation lines
- Multiple trailers allowed
- Must be at end of commit message
- Separated from message body by blank line

### Example Commit

```
Add user authentication feature

Implement OAuth2 flow with JWT tokens and refresh
token rotation. Added middleware for protected routes.

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
Signed-off-by: John Doe <john@example.com>
```

## Common Git Trailers

### Co-Authored-By

Acknowledges co-authors of a commit.

**Format:**
```
Co-Authored-By: Name <email@example.com>
```

**Usage:**
- Pair programming
- AI assistance
- Mentoring situations
- Team collaboration

**Platform support:**
- ✅ GitHub: Shows co-authors, credits in contribution graphs
- ✅ GitLab: Shows co-authors on commit page
- ⚠️ Bitbucket: Displays but doesn't parse specially

### Signed-off-by

Developer Certificate of Origin (DCO) signature.

**Format:**
```
Signed-off-by: Developer Name <developer@example.com>
```

**Usage:**
- Open source projects requiring DCO
- Legal compliance
- Contribution tracking

**Add automatically:**
```bash
git commit -s
```

### Reviewed-by

Acknowledges code reviewers.

**Format:**
```
Reviewed-by: Reviewer Name <reviewer@example.com>
```

**Usage:**
- Code review acknowledgment
- Quality assurance tracking
- Approval documentation

### Tested-by

Acknowledges testers.

**Format:**
```
Tested-by: Tester Name <tester@example.com>
```

**Usage:**
- QA acknowledgment
- Testing validation
- Certification tracking

### Bug / Issue / Closes

Links commits to issue tracking systems.

**Format:**
```
Fixes: #123
Closes: #456
Resolves: JIRA-789
```

**Usage:**
- Issue tracking integration
- Automatic issue closing
- Release note generation

## Working with Trailers

### Manual Addition

Add trailers manually in commit message:

```bash
git commit -m "Add feature" -m "" -m "Co-Authored-By: Name <email>"
```

Blank line (`-m ""`) separates message body from trailers.

### Using git-interpret-trailers

Git provides `git interpret-trailers` command for programmatic manipulation:

**Add trailer:**
```bash
echo "commit message" | git interpret-trailers --trailer "Co-Authored-By: Name <email>"
```

**Add multiple:**
```bash
git interpret-trailers \
  --trailer "Co-Authored-By: Alice <alice@example.com>" \
  --trailer "Reviewed-by: Bob <bob@example.com>" \
  message.txt
```

**Configure defaults:**
```bash
git config trailer.coauthoredby.key "Co-Authored-By"
```

### Commit Template

Configure git to use commit template with trailers:

**Create template (~/.gitmessage):**
```


Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

**Configure git:**
```bash
git config --global commit.template ~/.gitmessage
```

### Git Hooks

Add trailers automatically with prepare-commit-msg hook:

**~/.git/hooks/prepare-commit-msg:**
```bash
#!/bin/bash

# Add Co-Authored-By trailer if not present
if ! grep -q "Co-Authored-By:" "$1"; then
  echo "" >> "$1"
  echo "Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>" >> "$1"
fi
```

Make executable:
```bash
chmod +x .git/hooks/prepare-commit-msg
```

## Email Format in Trailers

### Standard Format

Git trailers use RFC 822 email format:

```
Name <email@example.com>
```

**Components:**
- Display name (optional)
- Email in angle brackets (required for GitHub/GitLab recognition)

### Examples

**With name:**
```
Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

**Name only (no email):**
```
Co-Authored-By: Claude Sonnet 4.5
```

**Email only:**
```
Co-Authored-By: <noreply@anthropic.com>
```

**Multiple addresses (not standard):**
```
Co-Authored-By: Team <team@example.com>, Bot <bot@example.com>
```

### Email Requirements

For GitHub/GitLab co-author recognition:
- ✅ Email must be in angle brackets: `<email@example.com>`
- ✅ Email should be registered with platform account
- ✅ Email must be valid format
- ⚠️ noreply addresses work but don't link to accounts

## Multi-line Trailers

### Continuation Lines

Trailers can span multiple lines with indentation:

```
Co-Authored-By: Claude Sonnet 4.5
  <noreply@anthropic.com>
```

**Rules:**
- Continuation lines start with whitespace
- Whitespace is part of the value
- Not commonly used

### Multiple Trailers

Each trailer on separate line:

```
Co-Authored-By: Alice <alice@example.com>
Co-Authored-By: Bob <bob@example.com>
Reviewed-by: Charlie <charlie@example.com>
```

## Parsing Trailers

### With git

**Extract all trailers:**
```bash
git log -1 --pretty=format:%B | git interpret-trailers --parse
```

**Output:**
```
Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
Signed-off-by: John Doe <john@example.com>
```

**Get specific trailer:**
```bash
git log -1 --pretty="%(trailers:key=Co-Authored-By)"
```

### With grep

**Find commits with trailers:**
```bash
git log --grep="Co-Authored-By:"
```

**Extract trailer from commit:**
```bash
git log -1 --pretty=%B | grep "Co-Authored-By:"
```

### Manual Parsing

Trailers are at end of commit message, after blank line:

**Algorithm:**
1. Read commit message
2. Find last blank line
3. Lines after blank line are potential trailers
4. Parse lines matching `Key: Value` format

**Example (bash):**
```bash
#!/bin/bash
# Get commit message
MESSAGE=$(git log -1 --pretty=%B)

# Extract trailers (lines after last blank line matching trailer format)
echo "$MESSAGE" | awk '
  /^$/ { blank=NR; next }
  NR > blank && /^[A-Z][a-zA-Z-]+: / { print }
'
```

## Platform-Specific Behavior

### GitHub

**Co-Authored-By Recognition:**
- Parses `Co-Authored-By: Name <email>` format
- Shows co-authors on commit page
- Credits co-authors in contribution graphs
- Links email to GitHub account if registered
- Requires email to match GitHub account

**Automatic Parsing:**
- Works in commit messages
- Works in PR merge commits
- Works in squash merges

**Web UI:**
Shows co-authors with avatar (if account linked) and name.

### GitLab

**Co-Authored-By Recognition:**
- Parses `Co-Authored-By: Name <email>` format
- Shows co-authors on commit details page
- Links to user profile if email matches GitLab account
- Displays in commit history

**Note:** Less prominent than GitHub but still supported.

### Bitbucket

**Limited Support:**
- Displays trailers in commit message
- Does not parse or highlight specially
- No special UI treatment
- Still useful for documentation

### Git CLI

**Native Support:**
- `git log` displays trailers as part of message
- `git interpret-trailers` command for manipulation
- `%(trailers)` format placeholder for extraction
- Git hooks can add trailers automatically

## Best Practices

### Formatting

1. **Use standard keys:** Stick to recognized trailer keys when possible
2. **Include email in brackets:** `<email@example.com>` for platform recognition
3. **One trailer per line:** Don't combine multiple on one line
4. **Blank line before trailers:** Separate message body from trailers
5. **Consistent capitalization:** Use standard capitalization for keys

### Content

1. **Valid emails:** Use real or noreply addresses, properly formatted
2. **Full names:** Include readable names, not just emails
3. **Relevant trailers:** Only add trailers that provide value
4. **Accurate attribution:** Don't add trailers for uninvolved parties

### Automation

1. **Use git hooks:** Automate trailer addition for consistency
2. **Configure defaults:** Set up git config for standard trailers
3. **Validate format:** Check trailer format before committing
4. **CI validation:** Verify required trailers in CI/CD

## Troubleshooting

### GitHub Not Recognizing Co-Author

**Problem:** GitHub doesn't show co-author

**Solutions:**
- ✅ Verify email is in angle brackets: `<email>`
- ✅ Check email is registered with a GitHub account
- ✅ Ensure trailer is at end of commit message
- ✅ Verify blank line before trailers
- ✅ Check exact format: `Co-Authored-By: Name <email>`

### Trailers in Middle of Message

**Problem:** Trailers appearing in message body

**Solutions:**
- ✅ Add blank line before trailers
- ✅ Move trailers to end of message
- ✅ Remove extra blank lines after trailers

### Invalid Email Format

**Problem:** Trailer rejected or not recognized

**Solutions:**
- ✅ Use angle brackets: `<email@example.com>`
- ✅ Verify email format is valid
- ✅ Remove extra whitespace
- ✅ Check for typos in email address

## Advanced Topics

### Custom Trailer Keys

Create custom trailer keys for specific needs:

**Configure key:**
```bash
git config trailer.ack.key "Acked-by"
```

**Add with alias:**
```bash
git config alias.ack "interpret-trailers --trailer 'Acked-by: \$1'"
```

**Use:**
```bash
git ack "Name <email>"
```

### Trailer Ifexists Policy

Control duplicate trailer handling:

```bash
git config trailer.coauthoredby.ifexists addIfDifferent
```

**Options:**
- `addIfDifferent` - Add if value differs
- `addIfDifferentNeighbor` - Add if immediate neighbor differs
- `add` - Always add
- `replace` - Replace existing
- `doNothing` - Don't add if exists

### Trailer Signing

Combine with GPG signing:

```bash
git commit -S -m "Message" -m "" -m "Co-Authored-By: Name <email>"
```

Trailers remain in signed portion of commit.

---

## References

- [git-interpret-trailers(1) Manual](https://git-scm.com/docs/git-interpret-trailers)
- [Git Commit Template Guide](https://git-scm.com/book/en/v2/Customizing-Git-Git-Configuration)
- [GitHub Co-Authors Documentation](https://docs.github.com/en/pull-requests/committing-changes-to-your-project/creating-and-editing-commits/creating-a-commit-with-multiple-authors)
- [GitLab Commit Trailers](https://docs.gitlab.com/ee/user/project/merge_requests/commit_templates.html)
