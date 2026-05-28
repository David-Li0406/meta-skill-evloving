---
name: tauri-file-watching-events
description: |
  Pattern for real-time streaming from CLI tools to Tauri GUI by watching JSONL files.
  Use when: (1) building a Tauri app that needs to display output from a CLI tool,
  (2) need real-time updates in GUI from an external process, (3) bridging Rust backend
  events to React/TypeScript frontend. Covers file polling with position tracking,
  Tauri event emission, and frontend event listeners with type mapping.
author: Claude Code
version: 1.0.0
date: 2026-01-22
---

# Tauri File-Watching for CLI-to-GUI Event Streaming

## Problem

When building a Tauri desktop app that needs to display real-time updates from a CLI tool
or external process, you need a way to bridge the output from the CLI (which writes to files
or stdout) to the GUI frontend.

## Context / Trigger Conditions

- Building a Tauri app with a React/TypeScript frontend
- Have a separate CLI tool that writes events/logs to a JSONL file
- Need real-time updates in the GUI when the CLI produces new output
- Want to show agent/process status, activity logs, or progress in the GUI

## Solution

### 1. Define Event Types in Tauri Backend (Rust)

```rust
use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use std::fs::File;
use std::io::{BufRead, BufReader, Seek, SeekFrom};
use std::path::PathBuf;
use std::time::Duration;
use tauri::Emitter;
use uuid::Uuid;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct MyEvent {
    pub timestamp: DateTime<Utc>,
    pub event_id: Uuid,
    pub session_id: Uuid,
    pub event_type: String,
    pub data: EventData,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct EventData {
    pub id: String,
    pub name: String,
    pub status: String,
    // ... other fields
}
```

### 2. Implement File Watcher Command

```rust
#[tauri::command]
async fn start_event_watcher(app: tauri::AppHandle) -> Result<(), String> {
    let events_path = get_events_file_path(); // e.g., ~/.myapp/events.jsonl

    tokio::spawn(async move {
        let mut last_position: u64 = 0;
        let mut last_session_id: Option<Uuid> = None;

        loop {
            if let Ok(mut file) = File::open(&events_path) {
                if let Ok(metadata) = file.metadata() {
                    let file_size = metadata.len();

                    // Handle file truncation (new session)
                    if file_size < last_position {
                        last_position = 0;
                        last_session_id = None;
                    }

                    // Seek to last read position
                    if file.seek(SeekFrom::Start(last_position)).is_ok() {
                        let reader = BufReader::new(&file);

                        for line in reader.lines() {
                            if let Ok(line) = line {
                                if let Ok(event) = serde_json::from_str::<MyEvent>(&line) {
                                    // Track session and emit to frontend
                                    if last_session_id.is_none() || last_session_id == Some(event.session_id) {
                                        last_session_id = Some(event.session_id);
                                        let _ = app.emit("my-event", &event);
                                    } else {
                                        // New session detected
                                        last_session_id = Some(event.session_id);
                                        let _ = app.emit("session-change", event.session_id.to_string());
                                        let _ = app.emit("my-event", &event);
                                    }
                                }
                                last_position += line.len() as u64 + 1; // +1 for newline
                            }
                        }
                    }
                }
            }

            // Poll interval
            tokio::time::sleep(Duration::from_millis(200)).await;
        }
    });

    Ok(())
}

// Register in invoke_handler
.invoke_handler(tauri::generate_handler![start_event_watcher, /* ... */])
```

### 3. Frontend Event Listener (React/TypeScript)

```typescript
import { invoke } from '@tauri-apps/api/core';
import { listen, type UnlistenFn } from '@tauri-apps/api/event';

interface BackendEvent {
  timestamp: string;
  event_id: string;
  session_id: string;
  event_type: string;
  data: {
    id: string;
    name: string;
    status: string;
  };
}

// In your React component/context
useEffect(() => {
  let unlistenEvent: UnlistenFn | null = null;
  let unlistenSession: UnlistenFn | null = null;

  async function initialize() {
    // Start the backend watcher
    await invoke('start_event_watcher');

    // Listen for events
    unlistenEvent = await listen<BackendEvent>('my-event', (event) => {
      processEvent(event.payload);
    });

    // Listen for session changes (clear state)
    unlistenSession = await listen<string>('session-change', () => {
      clearState();
    });
  }

  initialize();

  return () => {
    if (unlistenEvent) unlistenEvent();
    if (unlistenSession) unlistenSession();
  };
}, []);
```

### 4. Type Mapping Between Backend and Frontend

```typescript
// Map backend status strings to frontend enum
function mapStatus(backendStatus: string): FrontendStatus {
  const statusMap: Record<string, FrontendStatus> = {
    'spawned': 'idle',
    'running': 'working',
    'completed': 'completed',
    'failed': 'error',
  };
  return statusMap[backendStatus.toLowerCase()] || 'idle';
}
```

## Verification

1. Start the CLI tool that writes to the JSONL file
2. Open the Tauri GUI
3. Verify events appear in real-time in the GUI
4. Start a new CLI session and verify old state is cleared

## Example Use Cases

- Agent monitoring dashboard (showing AI agent status)
- Build tool GUI (showing compilation progress)
- Log viewer (tailing log files)
- Process manager (showing running processes)

## Notes

- **Poll interval**: 200ms is a good balance between responsiveness and CPU usage
- **Position tracking**: Essential to avoid re-reading entire file on each poll
- **Session handling**: Clear frontend state when session_id changes
- **File truncation**: Reset position when file size decreases (new session started)
- **Error handling**: Gracefully handle missing files (CLI not running yet)

## Key Dependencies

**Rust/Tauri:**
- `tauri` with `Emitter` trait
- `serde` and `serde_json` for JSON parsing
- `chrono` for timestamps (optional)
- `uuid` for unique IDs (optional)

**TypeScript:**
- `@tauri-apps/api/core` for `invoke`
- `@tauri-apps/api/event` for `listen`

## References

- [Tauri Events Documentation](https://tauri.app/develop/calling-rust/#events)
- [Tauri Commands Documentation](https://tauri.app/develop/calling-rust/)
