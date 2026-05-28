# Tauri Command Patterns

## Basic Commands

```rust
use tauri::command;

#[command]
fn greet(name: &str) -> String {
    format!("Hello, {}!", name)
}

#[command]
async fn fetch_data(url: String) -> Result<String, String> {
    reqwest::get(&url)
        .await
        .map_err(|e| e.to_string())?
        .text()
        .await
        .map_err(|e| e.to_string())
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![greet, fetch_data])
        .run(tauri::generate_context!())
        .expect("error running app");
}
```

## State Management

```rust
use std::sync::Mutex;
use tauri::State;

struct AppState {
    counter: Mutex<i32>,
    db: Database,
}

#[command]
fn increment(state: State<AppState>) -> i32 {
    let mut counter = state.counter.lock().unwrap();
    *counter += 1;
    *counter
}

#[command]
async fn get_users(state: State<'_, AppState>) -> Result<Vec<User>, String> {
    state.db.get_users()
        .await
        .map_err(|e| e.to_string())
}

fn main() {
    let state = AppState {
        counter: Mutex::new(0),
        db: Database::new(),
    };

    tauri::Builder::default()
        .manage(state)
        .invoke_handler(tauri::generate_handler![increment, get_users])
        .run(tauri::generate_context!())
        .unwrap();
}
```

## Events

```rust
use tauri::{Manager, Window};

#[command]
fn start_download(window: Window, url: String) {
    std::thread::spawn(move || {
        for progress in 0..=100 {
            std::thread::sleep(std::time::Duration::from_millis(50));
            window.emit("download-progress", progress).unwrap();
        }
        window.emit("download-complete", ()).unwrap();
    });
}

// In frontend (JavaScript)
// import { listen } from '@tauri-apps/api/event';
// await listen('download-progress', (event) => {
//     console.log('Progress:', event.payload);
// });
```

## Window Management

```rust
use tauri::{Manager, WindowBuilder, WindowUrl};

#[command]
async fn open_settings(app: tauri::AppHandle) -> Result<(), String> {
    WindowBuilder::new(
        &app,
        "settings",
        WindowUrl::App("settings.html".into())
    )
    .title("Settings")
    .inner_size(600.0, 400.0)
    .resizable(false)
    .build()
    .map_err(|e| e.to_string())?;
    
    Ok(())
}

#[command]
fn close_window(window: Window) {
    window.close().unwrap();
}

#[command]
fn minimize_window(window: Window) {
    window.minimize().unwrap();
}
```

## File Operations

```rust
use std::fs;
use tauri::api::path::app_data_dir;

#[command]
fn read_config(app: tauri::AppHandle) -> Result<String, String> {
    let config_dir = app_data_dir(&app.config())
        .ok_or("Failed to get app data dir")?;
    let config_path = config_dir.join("config.json");
    
    fs::read_to_string(config_path)
        .map_err(|e| e.to_string())
}

#[command]
fn save_config(app: tauri::AppHandle, config: String) -> Result<(), String> {
    let config_dir = app_data_dir(&app.config())
        .ok_or("Failed to get app data dir")?;
    
    fs::create_dir_all(&config_dir)
        .map_err(|e| e.to_string())?;
    
    fs::write(config_dir.join("config.json"), config)
        .map_err(|e| e.to_string())
}
```

## Menu and System Tray

```rust
use tauri::{CustomMenuItem, Menu, MenuItem, Submenu, SystemTray, SystemTrayMenu};

fn main() {
    let menu = Menu::new()
        .add_submenu(Submenu::new(
            "File",
            Menu::new()
                .add_item(CustomMenuItem::new("open", "Open"))
                .add_native_item(MenuItem::Separator)
                .add_item(CustomMenuItem::new("quit", "Quit")),
        ));

    let tray_menu = SystemTrayMenu::new()
        .add_item(CustomMenuItem::new("show", "Show"))
        .add_item(CustomMenuItem::new("quit", "Quit"));

    let tray = SystemTray::new().with_menu(tray_menu);

    tauri::Builder::default()
        .menu(menu)
        .system_tray(tray)
        .on_menu_event(|event| {
            match event.menu_item_id() {
                "quit" => std::process::exit(0),
                "open" => { /* handle open */ }
                _ => {}
            }
        })
        .on_system_tray_event(|app, event| {
            // Handle tray events
        })
        .run(tauri::generate_context!())
        .unwrap();
}
```

## Frontend Integration

```typescript
// In frontend (TypeScript)
import { invoke } from '@tauri-apps/api/tauri';

// Call commands
const greeting = await invoke<string>('greet', { name: 'World' });
const users = await invoke<User[]>('get_users');

// With error handling
try {
    const data = await invoke('fetch_data', { url: 'https://api.example.com' });
} catch (error) {
    console.error('Failed:', error);
}
```
