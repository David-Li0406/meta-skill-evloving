# Desktop Development with Tauri

Building cross-platform desktop applications with Tauri, a lightweight alternative to Electron.

## Why Tauri?

- **Small bundle size**: ~3MB vs 150MB+ for Electron
- **Native performance**: Uses system webview
- **Rust backend**: Type-safe, fast, secure
- **Cross-platform**: Windows, macOS, Linux
- **Web frontend**: Use any web framework (React, Vue, Svelte)

## Getting Started

### Prerequisites

```bash
# Install Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Install system dependencies (Linux)
sudo apt install libwebkit2gtk-4.0-dev \
    build-essential \
    curl \
    wget \
    libssl-dev \
    libgtk-3-dev \
    libayatana-appindicator3-dev \
    librsvg2-dev
```

### Create New Project

```bash
# Using create-tauri-app
npm create tauri-app@latest

# Or manually
cargo install create-tauri-app
cargo create-tauri-app
```

### Project Structure

```
my-tauri-app/
├── src-tauri/           # Rust backend
│   ├── src/
│   │   └── main.rs
│   ├── Cargo.toml
│   ├── tauri.conf.json
│   └── icons/
└── src/                 # Frontend (React/Vue/etc)
    ├── index.html
    └── main.js
```

## Basic Tauri Application

### src-tauri/src/main.rs

```rust
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

fn main() {
    tauri::Builder::default()
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

### tauri.conf.json

```json
{
  "build": {
    "beforeDevCommand": "npm run dev",
    "beforeBuildCommand": "npm run build",
    "devPath": "http://localhost:1420",
    "distDir": "../dist"
  },
  "package": {
    "productName": "My App",
    "version": "0.1.0"
  },
  "tauri": {
    "allowlist": {
      "all": false,
      "fs": {
        "all": false,
        "readFile": true,
        "writeFile": true
      }
    },
    "windows": [
      {
        "title": "My App",
        "width": 800,
        "height": 600
      }
    ]
  }
}
```

## Commands (Backend API)

### Defining Commands

```rust
#[tauri::command]
fn greet(name: &str) -> String {
    format!("Hello, {}!", name)
}

#[tauri::command]
async fn fetch_data(url: String) -> Result<String, String> {
    reqwest::get(&url)
        .await
        .map_err(|e| e.to_string())?
        .text()
        .await
        .map_err(|e| e.to_string())
}

#[tauri::command]
fn complex_operation(data: Vec<i32>) -> Result<i32, String> {
    if data.is_empty() {
        return Err("Data cannot be empty".to_string());
    }

    Ok(data.iter().sum())
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![
            greet,
            fetch_data,
            complex_operation
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

### Calling from Frontend

```javascript
import { invoke } from '@tauri-apps/api/tauri';

// Simple command
const greeting = await invoke('greet', { name: 'Alice' });
console.log(greeting);  // "Hello, Alice!"

// Async command
const data = await invoke('fetch_data', { url: 'https://api.example.com/data' });

// With error handling
try {
    const result = await invoke('complex_operation', { data: [1, 2, 3, 4, 5] });
    console.log(result);  // 15
} catch (error) {
    console.error('Error:', error);
}
```

## State Management

### Application State

```rust
use std::sync::Mutex;
use tauri::State;

struct AppState {
    counter: Mutex<i32>,
    config: Mutex<Config>,
}

#[tauri::command]
fn increment_counter(state: State<AppState>) -> i32 {
    let mut counter = state.counter.lock().unwrap();
    *counter += 1;
    *counter
}

#[tauri::command]
fn get_counter(state: State<AppState>) -> i32 {
    *state.counter.lock().unwrap()
}

fn main() {
    tauri::Builder::default()
        .manage(AppState {
            counter: Mutex::new(0),
            config: Mutex::new(Config::default()),
        })
        .invoke_handler(tauri::generate_handler![
            increment_counter,
            get_counter
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

## Events

### Emitting Events from Rust

```rust
use tauri::Manager;

#[tauri::command]
async fn process_files(window: tauri::Window) -> Result<(), String> {
    for i in 0..100 {
        // Emit progress event
        window.emit("progress", i).map_err(|e| e.to_string())?;

        // Do work
        tokio::time::sleep(tokio::time::Duration::from_millis(100)).await;
    }

    window.emit("complete", ()).map_err(|e| e.to_string())?;

    Ok(())
}
```

### Listening in Frontend

```javascript
import { listen } from '@tauri-apps/api/event';

// Listen for progress updates
const unlisten = await listen('progress', (event) => {
    console.log(`Progress: ${event.payload}%`);
    updateProgressBar(event.payload);
});

// Listen for completion
await listen('complete', () => {
    console.log('Processing complete!');
    showNotification('Done!');
});

// Clean up listener
unlisten();
```

### Frontend to Backend Events

```javascript
import { emit } from '@tauri-apps/api/event';

// Emit event from frontend
await emit('user-action', { action: 'click', target: 'button-1' });
```

```rust
use tauri::Manager;

fn main() {
    tauri::Builder::default()
        .setup(|app| {
            let window = app.get_window("main").unwrap();

            window.listen("user-action", |event| {
                println!("User action: {:?}", event.payload());
            });

            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

## File System Access

### Reading and Writing Files

```rust
use tauri::api::path::app_data_dir;
use std::fs;

#[tauri::command]
fn read_config(app: tauri::AppHandle) -> Result<String, String> {
    let app_dir = app_data_dir(&app.config())
        .ok_or("Failed to get app data dir")?;

    let config_path = app_dir.join("config.json");

    fs::read_to_string(config_path)
        .map_err(|e| e.to_string())
}

#[tauri::command]
fn write_config(app: tauri::AppHandle, data: String) -> Result<(), String> {
    let app_dir = app_data_dir(&app.config())
        .ok_or("Failed to get app data dir")?;

    fs::create_dir_all(&app_dir).map_err(|e| e.to_string())?;

    let config_path = app_dir.join("config.json");

    fs::write(config_path, data)
        .map_err(|e| e.to_string())
}
```

### Using File Dialog

```rust
use tauri::api::dialog::FileDialogBuilder;

#[tauri::command]
async fn select_file() -> Result<String, String> {
    let (tx, rx) = tokio::sync::oneshot::channel();

    FileDialogBuilder::new()
        .pick_file(move |file_path| {
            let _ = tx.send(file_path);
        });

    let path = rx.await.map_err(|e| e.to_string())?;

    path.map(|p| p.to_string_lossy().to_string())
        .ok_or_else(|| "No file selected".to_string())
}
```

## Database Integration

### Using SQLite

```toml
[dependencies]
sqlx = { version = "0.7", features = ["runtime-tokio-rustls", "sqlite"] }
```

```rust
use sqlx::{sqlite::SqlitePool, Row};
use tauri::State;

struct Database(SqlitePool);

#[tauri::command]
async fn get_users(db: State<'_, Database>) -> Result<Vec<User>, String> {
    let users = sqlx::query_as::<_, User>("SELECT * FROM users")
        .fetch_all(&db.0)
        .await
        .map_err(|e| e.to_string())?;

    Ok(users)
}

#[tauri::command]
async fn create_user(db: State<'_, Database>, name: String, email: String) -> Result<(), String> {
    sqlx::query("INSERT INTO users (name, email) VALUES (?, ?)")
        .bind(name)
        .bind(email)
        .execute(&db.0)
        .await
        .map_err(|e| e.to_string())?;

    Ok(())
}

#[tokio::main]
async fn main() {
    let pool = SqlitePool::connect("sqlite://database.db")
        .await
        .expect("Failed to create pool");

    tauri::Builder::default()
        .manage(Database(pool))
        .invoke_handler(tauri::generate_handler![get_users, create_user])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

## Window Management

### Creating Multiple Windows

```rust
use tauri::Manager;

#[tauri::command]
fn open_settings_window(app: tauri::AppHandle) {
    tauri::WindowBuilder::new(
        &app,
        "settings",
        tauri::WindowUrl::App("settings.html".into())
    )
    .title("Settings")
    .inner_size(400.0, 600.0)
    .build()
    .unwrap();
}

#[tauri::command]
fn close_window(window: tauri::Window) {
    window.close().unwrap();
}
```

### Window Communication

```rust
use tauri::Manager;

#[tauri::command]
fn send_to_window(app: tauri::AppHandle, label: String, event: String, payload: String) {
    if let Some(window) = app.get_window(&label) {
        window.emit(&event, payload).unwrap();
    }
}
```

## System Tray

```rust
use tauri::{CustomMenuItem, SystemTray, SystemTrayMenu, SystemTrayEvent};
use tauri::Manager;

fn main() {
    let quit = CustomMenuItem::new("quit".to_string(), "Quit");
    let show = CustomMenuItem::new("show".to_string(), "Show");
    let tray_menu = SystemTrayMenu::new()
        .add_item(show)
        .add_item(quit);

    let system_tray = SystemTray::new().with_menu(tray_menu);

    tauri::Builder::default()
        .system_tray(system_tray)
        .on_system_tray_event(|app, event| match event {
            SystemTrayEvent::MenuItemClick { id, .. } => {
                match id.as_str() {
                    "quit" => {
                        std::process::exit(0);
                    }
                    "show" => {
                        let window = app.get_window("main").unwrap();
                        window.show().unwrap();
                    }
                    _ => {}
                }
            }
            _ => {}
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

## Official Plugins

### tauri-plugin-store (Persistent Storage)

```toml
[dependencies]
tauri-plugin-store = "0.1"
```

```rust
use tauri_plugin_store::StoreBuilder;

fn main() {
    tauri::Builder::default()
        .plugin(tauri_plugin_store::Builder::default().build())
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

```javascript
import { Store } from 'tauri-plugin-store-api';

const store = new Store('.settings.dat');

// Save data
await store.set('theme', 'dark');
await store.set('user', { name: 'Alice', id: 42 });

// Load data
const theme = await store.get('theme');
const user = await store.get('user');

// Save to disk
await store.save();
```

### tauri-plugin-notification

```rust
use tauri_plugin_notification::NotificationExt;

#[tauri::command]
fn show_notification(app: tauri::AppHandle) {
    app.notification()
        .builder()
        .title("New Message")
        .body("You have a new notification!")
        .show()
        .unwrap();
}
```

### tauri-plugin-http

```rust
use tauri_plugin_http::reqwest;

#[tauri::command]
async fn fetch_api_data() -> Result<String, String> {
    let response = reqwest::get("https://api.example.com/data")
        .await
        .map_err(|e| e.to_string())?
        .text()
        .await
        .map_err(|e| e.to_string())?;

    Ok(response)
}
```

## Security Best Practices

### Command Allowlist

```json
{
  "tauri": {
    "allowlist": {
      "all": false,
      "fs": {
        "scope": ["$APPDATA/**", "$RESOURCE/**"]
      },
      "http": {
        "scope": ["https://api.example.com/*"]
      }
    }
  }
}
```

### Content Security Policy

```json
{
  "tauri": {
    "security": {
      "csp": "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'"
    }
  }
}
```

### Input Validation

```rust
#[tauri::command]
fn process_user_input(input: String) -> Result<String, String> {
    // Validate input
    if input.len() > 1000 {
        return Err("Input too long".to_string());
    }

    if input.contains("<script>") {
        return Err("Invalid input".to_string());
    }

    // Process validated input
    Ok(sanitize(input))
}
```

## Building and Distribution

### Development

```bash
# Run in development mode
npm run tauri dev

# Or
cargo tauri dev
```

### Production Build

```bash
# Build for production
npm run tauri build

# Output in src-tauri/target/release/bundle/
```

### Code Signing

```json
{
  "tauri": {
    "bundle": {
      "macOS": {
        "signing": {
          "identity": "Developer ID Application: Your Name (TEAM_ID)"
        }
      },
      "windows": {
        "certificateThumbprint": "YOUR_CERT_THUMBPRINT",
        "digestAlgorithm": "sha256",
        "timestampUrl": "http://timestamp.digicert.com"
      }
    }
  }
}
```

### Auto-Updates

```toml
[dependencies]
tauri-plugin-updater = "2.0"
```

```rust
use tauri_plugin_updater::UpdaterExt;

fn main() {
    tauri::Builder::default()
        .plugin(tauri_plugin_updater::Builder::new().build())
        .setup(|app| {
            let handle = app.handle();
            tauri::async_runtime::spawn(async move {
                let response = handle.updater().check().await;
                // Handle update
            });
            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

## Testing

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_greet() {
        assert_eq!(greet("Test"), "Hello, Test!");
    }

    #[tokio::test]
    async fn test_fetch_data() {
        let result = fetch_data("https://httpbin.org/get".to_string()).await;
        assert!(result.is_ok());
    }
}
```

## Best Practices

1. **Minimize allowlist**: Only enable needed APIs
2. **Use CSP**: Prevent XSS attacks
3. **Validate inputs**: Never trust frontend data
4. **Handle errors**: Return Result from commands
5. **Use State**: For shared data between commands
6. **Async for I/O**: Use async commands for network/file operations
7. **Type safety**: Leverage Rust's type system
8. **Test backend**: Write unit tests for commands
9. **Code signing**: Sign production builds
10. **Auto-updates**: Implement update mechanism

## Resources

- [Tauri Documentation](https://tauri.app/)
- [Tauri Examples](https://github.com/tauri-apps/tauri/tree/dev/examples)
- [Awesome Tauri](https://github.com/tauri-apps/awesome-tauri)
