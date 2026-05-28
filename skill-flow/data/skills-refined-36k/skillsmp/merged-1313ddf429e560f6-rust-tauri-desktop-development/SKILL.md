---
name: rust-tauri-desktop-development
description: Use this skill when building cross-platform desktop applications with Rust and Tauri, leveraging web technologies for the frontend and Rust for the backend.
---

# Rust Tauri Desktop Development

## Overview

Rust has emerged as a premier language for building desktop applications that combine native performance with memory safety. This skill covers the complete Rust desktop development lifecycle using Tauri for hybrid web UI + Rust backend apps, enabling developers to use web technologies (React, Vue, Svelte) for the frontend while leveraging Rust's performance and safety for system-level operations.

## When to Use This Skill

Activate when building desktop applications that need **native performance**, **small bundle sizes**, **system integration**, or **memory safety guarantees**. Specifically use when:

- Building Electron alternatives with web UI + Rust backend (Tauri)
- Creating high-performance developer tools or productivity apps
- Developing system utilities requiring native OS integration
- Building cross-platform apps for Windows, macOS, and Linux
- Need <10MB bundle sizes vs 100MB+ Electron apps
- Implementing real-time applications (audio/video processing, games)
- Creating embedded GUI applications (kiosks, IoT devices)

## Core Principles

1. **Framework Alignment**: Use Tauri for web-skilled teams, native GUI for Rust-first projects.
2. **Clear Separation**: Frontend handles UI, Rust backend handles business logic and system access.
3. **Type-Safe IPC**: Commands and events strongly typed with serde serialization.
4. **Async Runtime**: Use Tokio for backend concurrency, preventing blocking the main thread.
5. **Security First**: Validate all IPC inputs, minimize exposed commands, and implement CSP policies.
6. **Platform Abstraction**: Write once, handle platform differences gracefully.

## Quick Start

1. **Choose Your Framework**
   - **Tauri**: For web skills (React/Vue/Svelte) and rapid UI development.
   - **Native GUI**: For pure Rust projects with immediate mode or reactive patterns.

2. **Initialize Project**
   ```bash
   # Tauri
   cargo create-tauri-app my-app
   # Select: npm, React/Vue/Svelte, TypeScript

   # Native (egui example)
   cargo new my-app
   cargo add eframe egui
   ```

3. **Setup Architecture**
   - Tauri: Define commands in `src-tauri/src/main.rs`, handle IPC.
   - Native: Implement app state, event loop, and UI update logic.

4. **Implement Core Features**
   - Define Tauri commands with `#[tauri::command]`.
   - Setup state management (Arc<Mutex<T>> or channels).
   - Integrate Tokio for async operations.
   - Add error handling with `Result<T, E>`.

5. **Add Platform Integration**
   - File system access (dialogs, read/write).
   - System tray, notifications, auto-updates.
   - OS-specific features (Windows registry, macOS sandboxing).

6. **Build and Distribute**
   ```bash
   # Development
   cargo tauri dev  # or cargo run

   # Production build
   cargo tauri build  # Creates installers for current platform
   ```

## Tauri Development Guidelines

### Project Structure

```
src/
├── app/                # Next.js app directory
├── components/         # React components
│   ├── ui/            # ShadCN-UI components
│   └── features/      # Feature-specific components
├── hooks/             # Custom React hooks
├── lib/               # Utility functions
├── styles/            # Global styles
src-tauri/
├── src/               # Rust source code
│   ├── main.rs       # Entry point
│   └── commands/     # Tauri commands
├── Cargo.toml        # Rust dependencies
└── tauri.conf.json   # Tauri configuration
```

### TypeScript Guidelines

- Use functional components with TypeScript.
- Define proper interfaces for all data structures.
- Use async/await for asynchronous operations.
- Implement proper error handling.

### Rust Guidelines

- Use `Result` types for fallible operations.
- Validate all inputs from the frontend.
- Log errors for debugging.

### UI Development

- Use TailwindCSS for styling with a utility-first approach.
- Implement responsive design and follow accessibility best practices.

### State Management

- Use React Context for global state.
- Consider Zustand for complex state.
- Implement proper state synchronization with Rust.

### File System Operations

```rust
use std::fs;
use tauri::api::path::app_data_dir;

#[tauri::command]
fn read_file(path: String) -> Result<String, String> {
    fs::read_to_string(&path).map_err(|e| e.to_string())
}

#[tauri::command]
fn write_file(path: String, content: String) -> Result<(), String> {
    fs::write(&path, content).map_err(|e| e.to_string())
}
```

### Testing

- Write unit tests for Rust commands.
- Test frontend components.
- Implement integration tests.

## Key Patterns

**Correct Tauri Pattern:**
```rust
✅ Commands in Rust backend
✅ Type-safe IPC with serde
✅ Async operations with Tokio
✅ State management with Arc<Mutex<T>>
✅ Error propagation with Result<T, E>
✅ Frontend calls backend via invoke()
```

**Incorrect Patterns:**
```rust
❌ Business logic in frontend JavaScript
❌ Exposing unsafe commands without validation
❌ Blocking operations on main thread
```

## Red Flags - STOP

- **Blocking the main thread** - Use Tokio spawn for long operations.
- **Exposing sensitive commands** - Validate and minimize surface area.
- **Missing CSP in Tauri** - Configure Content Security Policy.

## Real-World Impact

**Performance Metrics:**
- Bundle size: 3-5MB (Tauri) vs 100-200MB (Electron).
- Memory usage: 50-100MB (Tauri) vs 500MB-1GB (Electron).

**Production Examples:**
- **Warp Terminal**: High-performance terminal built with Rust.
- **Lapce**: Fast code editor using Druid.

## The Bottom Line

**Rust desktop development offers unmatched performance with memory safety.** Choose Tauri for web UI + Rust backend with tiny bundles. Architect with clear frontend/backend separation and test cross-platform early.