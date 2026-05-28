---
name: spec-context
description: Generate specifications for all child components of a context
user-invocable: true
allowed-tools: Bash(mix cli *), Read, Task
argument-hint: [ContextModuleName]
---

!`MIX_ENV=cli mix cli start-agent-task -e ${CLAUDE_SESSION_ID} -t context_component_specs -m $ARGUMENTS`
