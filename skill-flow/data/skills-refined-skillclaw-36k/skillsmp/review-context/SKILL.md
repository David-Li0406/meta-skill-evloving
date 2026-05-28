---
name: review-context
description: Review a context design and its child components for architecture issues
user-invocable: true
allowed-tools: Bash(mix cli *), Read, Edit
argument-hint: [ContextModuleName]
---

!`MIX_ENV=cli mix cli start-agent-task -e ${CLAUDE_SESSION_ID} -t context_design_review -m $ARGUMENTS`
