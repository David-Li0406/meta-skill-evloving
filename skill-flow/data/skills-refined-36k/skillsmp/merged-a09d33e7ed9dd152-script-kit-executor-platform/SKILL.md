---
name: script-kit-executor-platform
description: Use this skill for executing scripts and integrating platform-specific functionalities, including hotkeys and system actions.
---

# script-kit-executor-platform

This skill combines script execution capabilities with platform integration features, allowing for the execution of TypeScript/JavaScript scripts and the management of global hotkeys and system actions.

## Script Execution

The executor module is responsible for running TypeScript/JavaScript scripts with bidirectional JSONL communication. It handles process lifecycle management, SDK preloading, scriptlet execution, error handling, and selected text operations.

### Execution Flow

1. **Script Discovery and Validation**
   - Validates the script path and encoding.
   - Determines file type (TypeScript `.ts` or JavaScript `.js`).
   - Locates the SDK for preloading globals.

2. **Runtime Selection**
   - Tries runtimes in order of preference:
     - **bun with SDK preload** (preferred for TypeScript)
     - **bun without preload** (fallback)
     - **node** (for JavaScript files)

3. **Process Spawning**
   - Scripts are spawned with piped stdio and process groups.

4. **Session Splitting**
   - After spawn, the session is split for concurrent I/O.

### IPC Communication

All communication uses newline-delimited JSON (JSONL) for message handling, including prompt messages and direct handlers.

### Builtins

The `builtins.rs` module provides built-in features that appear in the main search alongside scripts, including clipboard history, window actions, and system actions.

### Scriptlet Execution

Scriptlets are small scripts embedded in markdown, supporting various tool types such as `bash`, `python`, `node`, and `typescript`.

### Error Handling

Includes stack trace parsing and suggestion generation based on error patterns.

## Platform Integration

### Window Configuration

Platform-specific functionality for window management, including floating panels and visibility controls.

#### Floating Panel Setup

Configure windows to float above normal windows and follow the active macOS space.

### Global Hotkeys

Manage global hotkeys for various actions, including launching scripts and opening windows.

#### Hotkey Action Types

- Main launcher hotkey
- Notes window hotkey
- AI window hotkey
- Script shortcuts

#### Starting the Hotkey Listener

Initialize the hotkey listener with configuration settings.

### System Actions

Utilize AppleScript-based system actions for power management, UI controls, and volume controls.

#### Power Management Actions

- Lock screen
- Sleep
- Restart
- Shut down

### Frontmost App Tracking

Track the previously active application for context-aware actions and menu bar interactions.

### Platform Differences

- **macOS**: Full support with AppKit and Cocoa.
- **Windows/Linux**: Stub implementations with sensible defaults.

## Anti-patterns

### Common Mistakes

1. **Dropping ProcessHandle Early**: Ensure the process handle remains alive until the script completes.
2. **Calling Platform APIs from Background Threads**: Use GCD dispatch for AppKit calls.
3. **Ignoring Hotkey Registration Failures**: Always handle errors during hotkey registration.
4. **Polling Instead of Using Channels**: Use async channels for hotkey events.

## Configuration Integration

Platform hotkeys are configured via a configuration file, allowing for easy customization of key bindings and actions.

## Logging

All modules use a centralized logging system for tracking actions and events.