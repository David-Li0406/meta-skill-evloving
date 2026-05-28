# Rust Design Patterns

Common patterns and idioms for writing idiomatic Rust code.

## Creational Patterns

### Builder Pattern

For types with many optional configuration parameters.

```rust
#[derive(Default)]
pub struct ServerConfig {
    host: String,
    port: u16,
    max_connections: usize,
    timeout: Option<Duration>,
    tls: Option<TlsConfig>,
}

pub struct ServerConfigBuilder {
    config: ServerConfig,
}

impl ServerConfigBuilder {
    pub fn new() -> Self {
        Self {
            config: ServerConfig {
                host: "127.0.0.1".to_string(),
                port: 8080,
                max_connections: 100,
                ..Default::default()
            },
        }
    }

    pub fn host(mut self, host: impl Into<String>) -> Self {
        self.config.host = host.into();
        self
    }

    pub fn port(mut self, port: u16) -> Self {
        self.config.port = port;
        self
    }

    pub fn max_connections(mut self, max: usize) -> Self {
        self.config.max_connections = max;
        self
    }

    pub fn timeout(mut self, timeout: Duration) -> Self {
        self.config.timeout = Some(timeout);
        self
    }

    pub fn build(self) -> ServerConfig {
        self.config
    }
}

// Usage
let config = ServerConfigBuilder::new()
    .host("0.0.0.0")
    .port(3000)
    .max_connections(1000)
    .build();
```

**Using `derive_builder` crate**:

```rust
use derive_builder::Builder;

#[derive(Builder)]
#[builder(setter(into))]
pub struct ServerConfig {
    host: String,
    port: u16,
    #[builder(default = "100")]
    max_connections: usize,
    #[builder(default)]
    timeout: Option<Duration>,
}

// Generated builder
let config = ServerConfigBuilder::default()
    .host("0.0.0.0")
    .port(3000)
    .build()
    .unwrap();
```

### Typestate Pattern

Use types to enforce state transitions at compile time.

```rust
// States
pub struct Locked;
pub struct Unlocked;

pub struct Door<State = Locked> {
    _state: PhantomData<State>,
}

impl Door<Locked> {
    pub fn new() -> Self {
        Door { _state: PhantomData }
    }

    pub fn unlock(self, key: &Key) -> Result<Door<Unlocked>, Error> {
        if key.is_valid() {
            Ok(Door { _state: PhantomData })
        } else {
            Err(Error::InvalidKey)
        }
    }
}

impl Door<Unlocked> {
    pub fn open(self) {
        println!("Door is open");
    }

    pub fn lock(self) -> Door<Locked> {
        Door { _state: PhantomData }
    }
}

// Usage
let door = Door::new(); // Door<Locked>
// door.open(); // Compile error!
let door = door.unlock(&key)?; // Door<Unlocked>
door.open(); // OK!
```

### Newtype Pattern

Wrap existing types for type safety and domain modeling.

```rust
// Type safety
pub struct UserId(u64);
pub struct ProductId(u64);

fn get_user(id: UserId) -> User { /* ... */ }
// get_user(ProductId(42)); // Compile error!

// With additional functionality
pub struct Email(String);

impl Email {
    pub fn new(email: String) -> Result<Self, ValidationError> {
        if email.contains('@') {
            Ok(Email(email))
        } else {
            Err(ValidationError::InvalidEmail)
        }
    }

    pub fn domain(&self) -> &str {
        self.0.split('@').nth(1).unwrap()
    }
}

impl Deref for Email {
    type Target = str;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

// Orphan rule workaround
pub struct MyVec<T>(Vec<T>);

impl MyVec<MyType> {
    // Can now implement methods for Vec<MyType>
    pub fn my_custom_method(&self) { /* ... */ }
}
```

## Structural Patterns

### Extension Trait Pattern

Add functionality to external types.

```rust
pub trait StringExt {
    fn is_palindrome(&self) -> bool;
    fn truncate_to(&self, max_len: usize) -> String;
}

impl StringExt for str {
    fn is_palindrome(&self) -> bool {
        let chars: Vec<_> = self.chars().collect();
        chars == chars.iter().rev().copied().collect::<Vec<_>>()
    }

    fn truncate_to(&self, max_len: usize) -> String {
        if self.len() <= max_len {
            self.to_string()
        } else {
            format!("{}...", &self[..max_len])
        }
    }
}

// Usage
use crate::StringExt;
let is_pal = "racecar".is_palindrome();
```

### Sealed Trait Pattern

Prevent external implementations of traits.

```rust
mod sealed {
    pub trait Sealed {}
}

pub trait MyTrait: sealed::Sealed {
    fn method(&self);
}

pub struct AllowedType;
impl sealed::Sealed for AllowedType {}
impl MyTrait for AllowedType {
    fn method(&self) { /* ... */ }
}

// External types cannot implement MyTrait
// because they can't implement sealed::Sealed
```

### Visitor Pattern

Process different types in a type-safe way.

```rust
pub trait Visitor {
    fn visit_string(&mut self, s: &str);
    fn visit_number(&mut self, n: i32);
    fn visit_bool(&mut self, b: bool);
}

pub enum Value {
    String(String),
    Number(i32),
    Bool(bool),
}

impl Value {
    pub fn accept(&self, visitor: &mut dyn Visitor) {
        match self {
            Value::String(s) => visitor.visit_string(s),
            Value::Number(n) => visitor.visit_number(*n),
            Value::Bool(b) => visitor.visit_bool(*b),
        }
    }
}

// Example visitor
struct JsonSerializer {
    output: String,
}

impl Visitor for JsonSerializer {
    fn visit_string(&mut self, s: &str) {
        self.output.push_str(&format!("\"{}\"", s));
    }

    fn visit_number(&mut self, n: i32) {
        self.output.push_str(&n.to_string());
    }

    fn visit_bool(&mut self, b: bool) {
        self.output.push_str(if b { "true" } else { "false" });
    }
}
```

## Behavioral Patterns

### RAII (Resource Acquisition Is Initialization)

Tie resource lifetime to object lifetime.

```rust
pub struct FileGuard {
    file: File,
}

impl FileGuard {
    pub fn new(path: &Path) -> io::Result<Self> {
        Ok(FileGuard {
            file: File::create(path)?,
        })
    }

    pub fn write(&mut self, data: &[u8]) -> io::Result<()> {
        self.file.write_all(data)
    }
}

impl Drop for FileGuard {
    fn drop(&mut self) {
        // Automatically called when FileGuard goes out of scope
        let _ = self.file.sync_all();
        println!("File closed and synced");
    }
}

// Usage
{
    let mut guard = FileGuard::new(Path::new("data.txt"))?;
    guard.write(b"Hello, world!")?;
} // File automatically closed here
```

### Strategy Pattern

Encapsulate algorithms behind a trait.

```rust
pub trait CompressionStrategy {
    fn compress(&self, data: &[u8]) -> Vec<u8>;
    fn decompress(&self, data: &[u8]) -> Vec<u8>;
}

pub struct GzipCompression;
impl CompressionStrategy for GzipCompression {
    fn compress(&self, data: &[u8]) -> Vec<u8> { /* ... */ }
    fn decompress(&self, data: &[u8]) -> Vec<u8> { /* ... */ }
}

pub struct ZstdCompression;
impl CompressionStrategy for ZstdCompression {
    fn compress(&self, data: &[u8]) -> Vec<u8> { /* ... */ }
    fn decompress(&self, data: &[u8]) -> Vec<u8> { /* ... */ }
}

pub struct FileArchiver {
    strategy: Box<dyn CompressionStrategy>,
}

impl FileArchiver {
    pub fn new(strategy: Box<dyn CompressionStrategy>) -> Self {
        FileArchiver { strategy }
    }

    pub fn archive(&self, data: &[u8]) -> Vec<u8> {
        self.strategy.compress(data)
    }
}

// Usage
let archiver = FileArchiver::new(Box::new(GzipCompression));
```

### Command Pattern

Encapsulate operations as objects.

```rust
pub trait Command {
    fn execute(&mut self) -> Result<()>;
    fn undo(&mut self) -> Result<()>;
}

pub struct InsertTextCommand {
    document: Arc<Mutex<Document>>,
    position: usize,
    text: String,
}

impl Command for InsertTextCommand {
    fn execute(&mut self) -> Result<()> {
        let mut doc = self.document.lock().unwrap();
        doc.insert(self.position, &self.text);
        Ok(())
    }

    fn undo(&mut self) -> Result<()> {
        let mut doc = self.document.lock().unwrap();
        doc.delete(self.position, self.text.len());
        Ok(())
    }
}

pub struct CommandHistory {
    history: Vec<Box<dyn Command>>,
    current: usize,
}

impl CommandHistory {
    pub fn execute(&mut self, mut command: Box<dyn Command>) -> Result<()> {
        command.execute()?;
        self.history.truncate(self.current);
        self.history.push(command);
        self.current += 1;
        Ok(())
    }

    pub fn undo(&mut self) -> Result<()> {
        if self.current > 0 {
            self.current -= 1;
            self.history[self.current].undo()?;
        }
        Ok(())
    }
}
```

## Functional Patterns

### Iterator Pattern

Lazy evaluation and composable operations.

```rust
pub struct Fibonacci {
    curr: u64,
    next: u64,
}

impl Iterator for Fibonacci {
    type Item = u64;

    fn next(&mut self) -> Option<Self::Item> {
        let current = self.curr;
        self.curr = self.next;
        self.next = current + self.next;
        Some(current)
    }
}

impl Fibonacci {
    pub fn new() -> Self {
        Fibonacci { curr: 0, next: 1 }
    }
}

// Usage - completely lazy
let sum: u64 = Fibonacci::new()
    .take(10)
    .filter(|x| x % 2 == 0)
    .sum();
```

**Custom Iterator Adapters**:

```rust
pub trait IteratorExt: Iterator {
    fn batched(self, size: usize) -> Batched<Self>
    where
        Self: Sized,
    {
        Batched { iter: self, size }
    }
}

impl<I: Iterator> IteratorExt for I {}

pub struct Batched<I> {
    iter: I,
    size: usize,
}

impl<I: Iterator> Iterator for Batched<I> {
    type Item = Vec<I::Item>;

    fn next(&mut self) -> Option<Self::Item> {
        let mut batch = Vec::with_capacity(self.size);
        for _ in 0..self.size {
            match self.iter.next() {
                Some(item) => batch.push(item),
                None if batch.is_empty() => return None,
                None => break,
            }
        }
        Some(batch)
    }
}

// Usage
use crate::IteratorExt;
let batches: Vec<Vec<i32>> = (1..=10).batched(3).collect();
// [[1,2,3], [4,5,6], [7,8,9], [10]]
```

### Combinator Pattern

Chain operations on Option and Result.

```rust
// Option combinators
fn process(input: Option<i32>) -> Option<String> {
    input
        .filter(|&x| x > 0)           // Keep only positive
        .map(|x| x * 2)                // Double it
        .and_then(|x| {                // Conditional transformation
            if x < 100 {
                Some(x)
            } else {
                None
            }
        })
        .map(|x| format!("Result: {}", x))  // Convert to string
}

// Result combinators
fn parse_and_validate(input: &str) -> Result<u32, Error> {
    input
        .parse::<u32>()                      // Result<u32, ParseIntError>
        .map_err(Error::from)                // Convert error type
        .and_then(|n| {                      // Validate
            if n > 0 {
                Ok(n)
            } else {
                Err(Error::InvalidValue)
            }
        })
}
```

### Adapter Pattern

Convert one interface to another.

```rust
// Adapt std::io::Read to our trait
pub trait DataSource {
    fn read_record(&mut self) -> Result<Record>;
}

pub struct IoAdapter<R: std::io::Read> {
    reader: R,
    buffer: Vec<u8>,
}

impl<R: std::io::Read> DataSource for IoAdapter<R> {
    fn read_record(&mut self) -> Result<Record> {
        // Adapt Read interface to DataSource interface
        self.buffer.clear();
        self.reader.read_to_end(&mut self.buffer)?;
        Record::parse(&self.buffer)
    }
}
```

## Concurrency Patterns

### Shared State with Mutex

```rust
use std::sync::{Arc, Mutex};

pub struct SharedCounter {
    count: Arc<Mutex<u64>>,
}

impl SharedCounter {
    pub fn new() -> Self {
        SharedCounter {
            count: Arc::new(Mutex::new(0)),
        }
    }

    pub fn increment(&self) {
        let mut count = self.count.lock().unwrap();
        *count += 1;
    }

    pub fn get(&self) -> u64 {
        *self.count.lock().unwrap()
    }

    pub fn clone_handle(&self) -> Self {
        SharedCounter {
            count: Arc::clone(&self.count),
        }
    }
}
```

### Message Passing with Channels

```rust
use std::sync::mpsc;
use std::thread;

pub enum WorkerMessage {
    Task(Task),
    Shutdown,
}

pub struct WorkerPool {
    sender: mpsc::Sender<WorkerMessage>,
    workers: Vec<thread::JoinHandle<()>>,
}

impl WorkerPool {
    pub fn new(size: usize) -> Self {
        let (sender, receiver) = mpsc::channel();
        let receiver = Arc::new(Mutex::new(receiver));

        let workers = (0..size)
            .map(|id| {
                let receiver = Arc::clone(&receiver);
                thread::spawn(move || loop {
                    let message = receiver.lock().unwrap().recv().unwrap();
                    match message {
                        WorkerMessage::Task(task) => {
                            println!("Worker {} processing task", id);
                            task.execute();
                        }
                        WorkerMessage::Shutdown => break,
                    }
                })
            })
            .collect();

        WorkerPool { sender, workers }
    }

    pub fn execute(&self, task: Task) {
        self.sender.send(WorkerMessage::Task(task)).unwrap();
    }
}

impl Drop for WorkerPool {
    fn drop(&mut self) {
        for _ in &self.workers {
            self.sender.send(WorkerMessage::Shutdown).unwrap();
        }

        for worker in &mut self.workers {
            if let Some(handle) = worker.take() {
                handle.join().unwrap();
            }
        }
    }
}
```

### Actor Pattern

```rust
use tokio::sync::mpsc;

pub enum ActorMessage {
    GetState { respond_to: mpsc::Sender<State> },
    Update(Update),
}

pub struct Actor {
    receiver: mpsc::Receiver<ActorMessage>,
    state: State,
}

impl Actor {
    pub fn new(receiver: mpsc::Receiver<ActorMessage>) -> Self {
        Actor {
            receiver,
            state: State::default(),
        }
    }

    async fn handle_message(&mut self, msg: ActorMessage) {
        match msg {
            ActorMessage::GetState { respond_to } => {
                let _ = respond_to.send(self.state.clone()).await;
            }
            ActorMessage::Update(update) => {
                self.state.apply(update);
            }
        }
    }

    pub async fn run(mut self) {
        while let Some(msg) = self.receiver.recv().await {
            self.handle_message(msg).await;
        }
    }
}

pub struct ActorHandle {
    sender: mpsc::Sender<ActorMessage>,
}

impl ActorHandle {
    pub fn new(state: State) -> Self {
        let (sender, receiver) = mpsc::channel(32);
        let actor = Actor::new(receiver);
        tokio::spawn(actor.run());

        ActorHandle { sender }
    }

    pub async fn get_state(&self) -> State {
        let (send, mut recv) = mpsc::channel(1);
        self.sender
            .send(ActorMessage::GetState { respond_to: send })
            .await
            .unwrap();
        recv.recv().await.unwrap()
    }

    pub async fn update(&self, update: Update) {
        self.sender.send(ActorMessage::Update(update)).await.unwrap();
    }
}
```

## Anti-Patterns

### Deref Polymorphism

**Bad**: Using `Deref` for type relationships.

```rust
// Don't do this!
struct MyString(String);

impl Deref for MyString {
    type Target = String;
    fn deref(&self) -> &Self::Target {
        &self.0
    }
}
```

**Good**: Use explicit methods or implement traits.

```rust
struct MyString(String);

impl MyString {
    pub fn as_str(&self) -> &str {
        &self.0
    }
}

impl AsRef<str> for MyString {
    fn as_ref(&self) -> &str {
        &self.0
    }
}
```

### Clone to Satisfy Borrow Checker

**Bad**: Cloning to avoid thinking about lifetimes.

```rust
fn process(data: &Data) -> String {
    // Unnecessary clone
    let owned = data.clone();
    format!("Processing: {}", owned.value)
}
```

**Good**: Borrow what you need.

```rust
fn process(data: &Data) -> String {
    format!("Processing: {}", data.value)
}
```

### Overusing Rc/Arc

**Bad**: Wrapping everything in Arc.

```rust
struct App {
    config: Arc<Config>,
    cache: Arc<Cache>,
    db: Arc<Database>,
}
```

**Good**: Use ownership and borrowing.

```rust
struct App {
    config: Config,
    cache: Cache,
    db: Database,
}

impl App {
    fn handle_request(&self, req: &Request) -> Response {
        // Borrow what you need
        self.cache.get(&req.key)
    }
}
```

## Pattern Selection Guide

| Need | Pattern |
|------|---------|
| Many optional parameters | Builder |
| Type-safe state machine | Typestate |
| Add functionality to external type | Extension Trait / Newtype |
| Prevent external implementations | Sealed Trait |
| Resource cleanup | RAII |
| Polymorphic algorithms | Strategy (trait objects) |
| Undo/redo functionality | Command |
| Lazy computation | Iterator |
| Shared mutable state | Arc<Mutex<T>> |
| Message-based concurrency | Channels / Actor |
| Type safety for primitives | Newtype |
