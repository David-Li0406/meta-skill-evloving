---
name: rust-tauri-desktop-development
description: Use this skill when building cross-platform desktop applications with Tauri, leveraging TypeScript for the frontend and Rust for the backend.
---

# Skill body

## Overview

This skill provides guidelines for developing cross-platform desktop applications using the Tauri framework, which combines a web frontend (using TypeScript and modern web technologies) with a Rust backend. Tauri enables developers to create lightweight applications with native performance and small bundle sizes.

## Core Principles

- Write clean, maintainable TypeScript and Rust code.
- Use TailwindCSS and ShadCN-UI for styling.
- Follow step-by-step planning for complex features.
- Prioritize code quality, security, and performance.

## Technology Stack

- **Frontend**: TypeScript, React/Next.js, TailwindCSS, ShadCN-UI
- **Backend**: Rust, Tauri APIs
- **Build**: Tauri CLI, Vite/Webpack

## Project Structure

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

## TypeScript Guidelines

### Code Style
- Use functional components with TypeScript.
- Define proper interfaces for all data structures.
- Use async/await for asynchronous operations.
- Implement proper error handling.

### Tauri Integration
```typescript
import { invoke } from '@tauri-apps/api/tauri';

// Call Rust commands from frontend
const result = await invoke<string>('my_command', { arg: 'value' });

// Listen to events from Rust
import { listen } from '@tauri-apps/api/event';
await listen('event-name', (event) => {
  console.log(event.payload);
});
```

## Rust Guidelines

### Command Definitions
```rust
#[tauri::command]
fn my_command(arg: String) -> Result<String, String> {
    // Implementation
    Ok(format!("Received: {}", arg))
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![my_command])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

### Error Handling
- Use Result types for fallible operations.
- Define custom error types when needed.
- Propagate errors appropriately.
- Log errors for debugging.

### Security
- Validate all inputs from the frontend.
- Use Tauri's security features (CSP, allowlist).
- Minimize potential vulnerabilities by following best practices.

## When to Use This Skill

Activate this skill when building desktop applications that require native performance, small bundle sizes, system integration, or memory safety guarantees, particularly when using Tauri for a hybrid web UI and Rust backend.