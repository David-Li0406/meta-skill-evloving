# Rust Craftsman

## Patterns


---
  #### **Name**
Ownership and Borrowing Mastery
  #### **Description**
Designing data flow where ownership is clear
  #### **When**
Structuring Rust programs
  #### **Example**
    // BAD: Fighting the borrow checker with clones
    fn process_bad(data: Vec<String>) {
        let copy1 = data.clone();  // Clone to avoid move
        let copy2 = data.clone();  // Another clone
        process_a(copy1);
        process_b(copy2);
    }
    
    // GOOD: Design for clear ownership flow
    fn process_good(data: Vec<String>) {
        // Split ownership - each part goes where needed
        let (for_a, for_b): (Vec<_>, Vec<_>) = data
            .into_iter()
            .enumerate()
            .partition(|(i, _)| i % 2 == 0);
    
        process_a(for_a.into_iter().map(|(_, s)| s).collect());
        process_b(for_b.into_iter().map(|(_, s)| s).collect());
    }
    
    // BETTER: Use references when you don't need ownership
    fn analyze(data: &[String]) -> Analysis {
        // Borrowing - no clone needed, caller keeps ownership
        Analysis {
            count: data.len(),
            total_len: data.iter().map(|s| s.len()).sum(),
        }
    }
    

---
  #### **Name**
Error Handling with Result and Option
  #### **Description**
Robust error handling without exceptions
  #### **When**
Any function that can fail
  #### **Example**
    use thiserror::Error;
    
    #[derive(Error, Debug)]
    pub enum ConfigError {
        #[error("Failed to read config file: {0}")]
        Io(#[from] std::io::Error),
    
        #[error("Invalid config format: {0}")]
        Parse(#[from] serde_json::Error),
    
        #[error("Missing required field: {field}")]
        MissingField { field: String },
    
        #[error("Value out of range: {name} must be {min}..{max}, got {value}")]
        OutOfRange {
            name: String,
            min: i64,
            max: i64,
            value: i64,
        },
    }
    
    pub fn load_config(path: &Path) -> Result<Config, ConfigError> {
        // ? operator propagates errors with automatic conversion
        let content = std::fs::read_to_string(path)?;
        let raw: RawConfig = serde_json::from_str(&content)?;
    
        // Validate required fields
        let timeout = raw.timeout.ok_or_else(|| ConfigError::MissingField {
            field: "timeout".into(),
        })?;
    
        // Validate ranges
        if !(1..=3600).contains(&timeout) {
            return Err(ConfigError::OutOfRange {
                name: "timeout".into(),
                min: 1,
                max: 3600,
                value: timeout,
            });
        }
    
        Ok(Config { timeout, ..Default::default() })
    }
    

---
  #### **Name**
Async Rust with Tokio
  #### **Description**
High-performance async programming
  #### **When**
Network I/O, concurrent operations
  #### **Example**
    use tokio::sync::{mpsc, Semaphore};
    use std::sync::Arc;
    
    pub struct RateLimitedClient {
        client: reqwest::Client,
        semaphore: Arc<Semaphore>,
    }
    
    impl RateLimitedClient {
        pub fn new(max_concurrent: usize) -> Self {
            Self {
                client: reqwest::Client::new(),
                semaphore: Arc::new(Semaphore::new(max_concurrent)),
            }
        }
    
        pub async fn fetch(&self, url: &str) -> Result<String, Error> {
            // Acquire permit (blocks if at limit)
            let _permit = self.semaphore.acquire().await?;
    
            // Permit auto-released when dropped
            self.client.get(url).send().await?.text().await
        }
    
        pub async fn fetch_many(&self, urls: Vec<String>) -> Vec<Result<String, Error>> {
            let futures: Vec<_> = urls
                .into_iter()
                .map(|url| {
                    let this = self.clone();
                    async move { this.fetch(&url).await }
                })
                .collect();
    
            // Execute all concurrently (semaphore limits parallelism)
            futures::future::join_all(futures).await
        }
    }
    
    // Channel-based actor pattern
    pub struct Worker {
        receiver: mpsc::Receiver<Job>,
    }
    
    impl Worker {
        pub async fn run(mut self) {
            while let Some(job) = self.receiver.recv().await {
                if let Err(e) = self.process(job).await {
                    eprintln!("Job failed: {e}");
                }
            }
        }
    }
    

---
  #### **Name**
Type-State Pattern
  #### **Description**
Encode state machine in types for compile-time guarantees
  #### **When**
State machines, builders, connection states
  #### **Example**
    // States are zero-sized types - no runtime cost
    pub struct Unconnected;
    pub struct Connected;
    pub struct Authenticated;
    
    pub struct Connection<State> {
        socket: TcpStream,
        _state: std::marker::PhantomData<State>,
    }
    
    impl Connection<Unconnected> {
        pub async fn connect(addr: &str) -> Result<Connection<Connected>, Error> {
            let socket = TcpStream::connect(addr).await?;
            Ok(Connection {
                socket,
                _state: std::marker::PhantomData,
            })
        }
    }
    
    impl Connection<Connected> {
        pub async fn authenticate(
            self,
            token: &str,
        ) -> Result<Connection<Authenticated>, Error> {
            // Send auth, validate response
            // ...
            Ok(Connection {
                socket: self.socket,
                _state: std::marker::PhantomData,
            })
        }
    }
    
    impl Connection<Authenticated> {
        // Only authenticated connections can send queries
        pub async fn query(&mut self, q: &str) -> Result<Response, Error> {
            // ...
        }
    }
    
    // Usage - compiler enforces correct state transitions
    async fn example() -> Result<(), Error> {
        let conn = Connection::connect("db:5432").await?
            .authenticate("token").await?;
    
        // conn.authenticate() - ERROR: method doesn't exist on Authenticated
        conn.query("SELECT 1").await?;
        Ok(())
    }
    

## Anti-Patterns


---
  #### **Name**
Clone Everything
  #### **Description**
Using .clone() to avoid borrow checker errors
  #### **Why**
Defeats Rust's zero-cost abstractions, hides design problems
  #### **Instead**
Redesign data flow, use references, consider Rc/Arc only when needed

---
  #### **Name**
Unwrap in Production
  #### **Description**
Using .unwrap() or .expect() outside of tests
  #### **Why**
Panics crash the program, lose error context
  #### **Instead**
Use Result with ? operator, proper error types

---
  #### **Name**
Unsafe Everywhere
  #### **Description**
Using unsafe to bypass the borrow checker
  #### **Why**
Defeats memory safety guarantees, hard to audit
  #### **Instead**
Redesign to satisfy the borrow checker, document safety invariants

---
  #### **Name**
String Instead of &str
  #### **Description**
Taking owned String when &str would work
  #### **Why**
Unnecessary allocations, forces callers to allocate
  #### **Instead**
Take &str in APIs, use impl Into<String> for flexibility

---
  #### **Name**
Box<dyn Error> Returns
  #### **Description**
Returning Box<dyn Error> from all functions
  #### **Why**
Loses type information, hard to match on specific errors
  #### **Instead**
Use thiserror for custom error types