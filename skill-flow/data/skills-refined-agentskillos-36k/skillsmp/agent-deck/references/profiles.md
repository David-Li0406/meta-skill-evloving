# Profile Management Guide

Guide for using profiles to organize agent-deck sessions.

## Overview

Profiles provide complete isolation between different sets of sessions.

**Common Use Cases:**
- Personal vs Work separation
- Client isolation
- Testing/demo environments

## Commands

```bash
# List profiles
agent-deck profile list

# Create profile
agent-deck profile create work

# Set default
agent-deck profile default work

# Use specific profile
agent-deck -p work list
agent-deck -p work session start my-project

# Delete profile
agent-deck profile delete old-profile
```

## Profile Storage

```
~/.agent-deck/profiles/
├── default/
│   └── sessions.json
├── work/
│   └── sessions.json
└── demo/
    └── sessions.json
```

## Environment Variable

```bash
export AGENTDECK_PROFILE=work
agent-deck list  # Uses 'work' profile
```

## Best Practices

1. Use explicit `-p` flag for important operations
2. Use consistent naming conventions
3. Set a default profile for primary usage
