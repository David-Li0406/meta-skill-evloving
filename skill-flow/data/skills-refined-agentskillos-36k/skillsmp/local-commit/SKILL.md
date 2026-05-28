---
name: local-commit
description: This skill should be used when the user wants to commit changes to the local private repository using lgit. It manages versioning of private AI configuration files.
allowed-tools: Bash(lgit add:*), Bash(lgit status:*), Bash(lgit diff:*), Bash(lgit commit -m:*)
---

# Local Private Repository Commit

Description of private versioning pattern: !`echo $HOME`/.claude/agent-docs/local-files-pattern.md

This command commits changes to the local private repository using the lgit wrapper.

!`lgit add .`

```bash
% lgit status
!`lgit status`
% lgit diff --cached
!`lgit diff --cached`
```

Think hard about the changes and generate a descriptive commit message.

Commit message format:

```
{one line commit summary}

{more detailed description of changes}
```

Then commit the changes using `lgit commit -m ...`.
