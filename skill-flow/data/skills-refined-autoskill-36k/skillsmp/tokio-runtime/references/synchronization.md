# Tokio Synchronization

## Mutex

```rust
use tokio::sync::Mutex;
use std::sync::Arc;

async fn shared_state() {
    let counter = Arc::new(Mutex::new(0));
    
    let mut handles = vec![];
    
    for _ in 0..10 {
        let counter = Arc::clone(&counter);
        let handle = tokio::spawn(async move {
            let mut lock = counter.lock().await;
            *lock += 1;
        });
        handles.push(handle);
    }
    
    for handle in handles {
        handle.await.unwrap();
    }
    
    println!("Counter: {}", *counter.lock().await);
}
```

## RwLock

```rust
use tokio::sync::RwLock;
use std::sync::Arc;

struct Cache {
    data: Arc<RwLock<HashMap<String, String>>>,
}

impl Cache {
    async fn get(&self, key: &str) -> Option<String> {
        let read_lock = self.data.read().await;
        read_lock.get(key).cloned()
    }
    
    async fn set(&self, key: String, value: String) {
        let mut write_lock = self.data.write().await;
        write_lock.insert(key, value);
    }
}
```

## Semaphore

```rust
use tokio::sync::Semaphore;
use std::sync::Arc;

async fn limited_concurrency() {
    let semaphore = Arc::new(Semaphore::new(3)); // Max 3 concurrent
    
    let mut handles = vec![];
    
    for i in 0..10 {
        let permit = semaphore.clone().acquire_owned().await.unwrap();
        let handle = tokio::spawn(async move {
            println!("Task {} started", i);
            tokio::time::sleep(Duration::from_secs(1)).await;
            println!("Task {} done", i);
            drop(permit); // Release when done
        });
        handles.push(handle);
    }
    
    for handle in handles {
        handle.await.unwrap();
    }
}
```

## Notify

```rust
use tokio::sync::Notify;
use std::sync::Arc;

async fn wait_for_signal() {
    let notify = Arc::new(Notify::new());
    
    let notify_clone = notify.clone();
    tokio::spawn(async move {
        tokio::time::sleep(Duration::from_secs(1)).await;
        notify_clone.notify_one(); // Wake one waiter
    });
    
    notify.notified().await; // Wait for notification
    println!("Received signal!");
}
```

## Watch Channel

```rust
use tokio::sync::watch;

async fn config_updates() {
    let (tx, mut rx) = watch::channel(Config::default());
    
    // Watcher task
    tokio::spawn(async move {
        while rx.changed().await.is_ok() {
            let config = rx.borrow();
            println!("Config updated: {:?}", *config);
        }
    });
    
    // Update config
    tx.send(Config { debug: true }).unwrap();
}
```

## Barrier

```rust
use tokio::sync::Barrier;
use std::sync::Arc;

async fn sync_tasks() {
    let barrier = Arc::new(Barrier::new(5));
    
    let mut handles = vec![];
    
    for i in 0..5 {
        let barrier = barrier.clone();
        let handle = tokio::spawn(async move {
            println!("Task {} preparing", i);
            tokio::time::sleep(Duration::from_millis(i as u64 * 100)).await;
            
            // Wait for all tasks
            barrier.wait().await;
            
            println!("Task {} proceeding", i);
        });
        handles.push(handle);
    }
    
    for handle in handles {
        handle.await.unwrap();
    }
}
```
