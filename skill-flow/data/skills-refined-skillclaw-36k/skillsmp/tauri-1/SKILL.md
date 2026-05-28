---
name: Tauri
description: Build desktop apps with Rust backend and WebView frontend.
metadata:
  labels: [rust, tauri, desktop, webview]
  triggers:
    files: ['tauri.conf.json', 'src-tauri/**/*.rs']
    keywords: [tauri, invoke, command, emit, State]
---

# Tauri Standards

## Architecture

```
my-app/
├── src/                    # Frontend (React/Vue/Svelte)
├── src-tauri/
│   ├── Cargo.toml
│   ├── tauri.conf.json     # Tauri config
│   ├── src/
│   │   ├── main.rs         # Entry point
│   │   └── lib.rs          # Commands
│   └── icons/
```

## Commands (Rust → Frontend)

```rust
use tauri::State;

#[tauri::command]
fn greet(name: &str) -> String {
    format!("Hello, {}!", name)
}

// With state
#[tauri::command]
fn get_count(state: State<'_, AppState>) -> u32 {
    *state.count.lock().unwrap()
}

// Async command
#[tauri::command]
async fn fetch_data(url: String) -> Result<String, String> {
    reqwest::get(&url)
        .await
        .map_err(|e| e.to_string())?
        .text()
        .await
        .map_err(|e| e.to_string())
}

// Register commands
fn main() {
    tauri::Builder::default()
        .manage(AppState::default())
        .invoke_handler(tauri::generate_handler![greet, get_count, fetch_data])
        .run(tauri::generate_context!())
        .expect("error running app");
}
```

## Frontend Invoke

```typescript
import { invoke } from '@tauri-apps/api/tauri';

// Call Rust command
const result = await invoke<string>('greet', { name: 'World' });

// With error handling
try {
  const data = await invoke<Data>('fetch_data', { url });
} catch (error) {
  console.error(error);
}
```

## State Management

```rust
use std::sync::Mutex;

struct AppState {
    count: Mutex<u32>,
    db: Mutex<Database>,
}

impl Default for AppState {
    fn default() -> Self {
        Self {
            count: Mutex::new(0),
            db: Mutex::new(Database::new()),
        }
    }
}

// Access in commands
#[tauri::command]
fn increment(state: State<'_, AppState>) -> u32 {
    let mut count = state.count.lock().unwrap();
    *count += 1;
    *count
}
```

## Events

```rust
use tauri::{AppHandle, Manager};

// Emit from Rust
#[tauri::command]
fn start_process(app: AppHandle) {
    std::thread::spawn(move || {
        for i in 0..100 {
            app.emit_all("progress", i).unwrap();
            std::thread::sleep(Duration::from_millis(100));
        }
    });
}

// Listen in Rust
app.listen_global("frontend-event", |event| {
    println!("Received: {:?}", event.payload());
});
```

```typescript
// Listen in frontend
import { listen } from '@tauri-apps/api/event';

const unlisten = await listen<number>('progress', (event) => {
  console.log('Progress:', event.payload);
});

// Emit from frontend
import { emit } from '@tauri-apps/api/event';
await emit('frontend-event', { data: 'value' });
```

## File System

```rust
use tauri::api::path::app_data_dir;

#[tauri::command]
fn save_config(app: AppHandle, config: Config) -> Result<(), String> {
    let path = app_data_dir(&app.config())
        .ok_or("No app data dir")?
        .join("config.json");

    std::fs::write(&path, serde_json::to_string(&config).unwrap())
        .map_err(|e| e.to_string())
}
```

## Permissions (tauri.conf.json)

```json
{
  "tauri": {
    "allowlist": {
      "fs": { "all": true, "scope": ["$APP/*"] },
      "shell": { "open": true },
      "dialog": { "all": true },
      "http": { "all": true, "scope": ["https://api.example.com/*"] }
    }
  }
}
```

## Best Practices

1. **Commands**: Keep thin, delegate to services
2. **State**: Use `Mutex` for shared state, avoid long locks
3. **Errors**: Return `Result<T, String>` for frontend handling
4. **Async**: Use async commands for I/O operations
5. **Security**: Scope file/http access in allowlist
