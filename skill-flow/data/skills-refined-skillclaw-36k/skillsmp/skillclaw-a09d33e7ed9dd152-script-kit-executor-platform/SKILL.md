---
name: script-kit-executor-platform
description: Use this skill when you need to execute scripts and manage platform-specific functionalities in a script execution environment.
---

# Skill body

## Overview

This skill combines the capabilities of executing TypeScript/JavaScript scripts with platform-specific integrations, including window management and global hotkeys.

## Script Execution

1. **Select Script**: Choose the script you want to execute.
2. **Find SDK Path**: Locate the SDK path, typically at `~/.scriptkit/sdk/`.
3. **Locate Executable**: Identify the bun/node executable required for script execution.
4. **Spawn Process**: Start the script execution with process management.

### Execution Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Script Execution Flow                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   User selects script                                                │
│          │                                                           │
│          ▼                                                           │
│   ┌──────────────────┐                                               │
│   │ execute_script_  │                                               │
│   │ interactive()    │                                               │
│   └────────┬─────────┘                                               │
│            │                                                         │
│            ▼                                                         │
│   ┌──────────────────┐     ┌──────────────────┐                      │
│   │  ScriptSession   │────▶│  SplitSession    │                      │
│   │  (unified)       │     │  (for threading) │                      │
│   └────────┬─────────┘     └──────────────────┘                      │
│            │                        │                                │
│            │ split()                │                                │
│            ▼                        ▼                                │
│   ┌──────────────────┐     ┌──────────────────┐                      │
│   │  Writer Thread   │     │  Reader Thread   │                      │
│   │  (stdin)         │     │  (stdout/stderr) │                      │
│   └──────────────────┘     └──────────────────┘                      │
│            │                        │                                │
│            │  JSONL Messages        │                                │
│            ▼                        ▼                                │
│   ┌────────────────────────────────────────────┐        
```

## Platform Integration

### Window Configuration

- **Floating Panel Setup**: Configure windows to float above normal windows and follow the active macOS space.
  
```rust
use crate::platform;

// Configure app as accessory (no Dock icon, no menu bar ownership)
platform::configure_as_accessory_app();

// Make window float above others and move to active space
platform::configure_as_floating_panel();
```

### Global Hotkeys

- Register and manage global hotkeys for quick access to functionalities.

### System Actions

- Implement platform-specific system actions using AppleScript or equivalent methods.

### Frontmost App Tracking

- Track the currently active application to manage interactions effectively.

## Conclusion

This skill provides a comprehensive framework for executing scripts while integrating with platform-specific features, enhancing the user experience in script execution environments.