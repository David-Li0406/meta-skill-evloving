---
name: rust-specific
version: 1.0.0
description: Rust语言特有审查规则（所有权系统、并发安全、零成本抽象）
language: rust
tags: [rust, ownership, borrow-checker, concurrency, zero-cost-abstractions]
frameworks: [tokio, actix, rocket, axum]
---

# Rust特有审查规则

## 所有权系统
- **借用规则**: 避免悬垂引用、正确使用生命周期参数、避免借用检查器冲突
- **生命周期管理**: 显式标注复杂生命周期、避免过度使用'static、使用生命周期省略规则
- **智能指针**: 合理使用Box/Rc/Arc、避免过度包装、使用Deref trait
- **内存安全**: 避免内存泄漏、正确使用drop trait、避免循环引用

## 并发安全
- **Send/Sync**: 正确实现Send/Sync trait、避免跨线程共享非Send类型
- **无锁编程**: 使用原子操作、避免数据竞争、使用Arc<Mutex<T>>保护共享数据
- **异步编程**: 正确使用async/await、避免阻塞异步执行器、使用tokio runtime
- **线程安全**: 使用std::thread、避免全局可变状态、使用消息传递

## 错误处理
- **Result类型**: 正确处理Result、使用?运算符传播错误、避免unwrap/expect
- **自定义错误**: 实现Error trait、使用thiserror创建错误类型、错误链处理
- **panic处理**: 避免panic、使用catch_unwind处理panic、在边界处处理错误
- **错误转换**: 使用From trait进行错误转换、避免错误信息丢失

## 性能优化
- **零成本抽象**: 使用迭代器、避免不必要的堆分配、使用inline优化
- **内联优化**: 使用#[inline]属性、避免过度内联、合理使用const fn
- **SIMD优化**: 使用portable SIMD、向量化计算、避免手动优化
- **缓存友好**: 使用数组而非链表、考虑数据局部性、避免虚函数调用

## 代码示例

### 正面示例 - 所有权管理
```rust
// 推荐：正确使用借用
fn process_data(data: &str) -> String {
    let processed: String = data
        .chars()
        .filter(|c| c.is_alphanumeric())
        .collect();
    processed
}

// 推荐：使用生命周期参数
struct Parser<'a> {
    source: &'a str,
    position: usize,
}

impl<'a> Parser<'a> {
    fn new(source: &'a str) -> Self {
        Parser { source, position: 0 }
    }
    
    fn peek(&self) -> Option<char> {
        self.source[self.position..].chars().next()
    }
}
```

### 反面示例 - 悬垂引用
```rust
// 不推荐：返回悬垂引用
fn bad_dangling() -> &String {
    let s = String::from("hello");
    &s  // 错误：返回局部变量的引用
}
```

### 正面示例 - 并发安全
```rust
// 推荐：使用Arc和Mutex保护共享数据
use std::sync::{Arc, Mutex};

fn shared_counter() {
    let counter = Arc::new(Mutex::new(0));
    let mut handles = vec![];
    
    for _ in 0..10 {
        let counter = Arc::clone(&counter);
        let handle = std::thread::spawn(move || {
            let mut num = counter.lock().unwrap();
            *num += 1;
        });
        handles.push(handle);
    }
    
    for handle in handles {
        handle.join().unwrap();
    }
    
    println!("Result: {}", *counter.lock().unwrap());
}
```

### 反面示例 - 数据竞争
```rust
// 不推荐：无保护地共享可变数据
use std::thread;

fn bad_data_race() {
    let mut data = vec![1, 2, 3];
    
    for i in 0..3 {
        thread::spawn(move || {
            data[i] += 1;  // 错误：无保护地访问共享数据
        });
    }
}
```

### 正面示例 - 错误处理
```rust
// 推荐：完整的错误处理
use std::error::Error;
use std::fs::File;
use std::io::Read;

#[derive(Debug)]
enum ConfigError {
    IoError(std::io::Error),
    ParseError(String),
}

impl std::fmt::Display for ConfigError {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        match self {
            ConfigError::IoError(e) => write!(f, "IO error: {}", e),
            ConfigError::ParseError(s) => write!(f, "Parse error: {}", s),
        }
    }
}

impl Error for ConfigError {}

fn read_config(filename: &str) -> Result<String, ConfigError> {
    let mut file = File::open(filename)
        .map_err(ConfigError::IoError)?;
    
    let mut contents = String::new();
    file.read_to_string(&mut contents)
        .map_err(ConfigError::IoError)?;
    
    Ok(contents)
}
```

### 反面示例 - 错误处理不当
```rust
// 不推荐：使用unwrap可能导致panic
fn bad_config() -> String {
    let mut file = File::open("config.txt").unwrap();  // 可能panic
    let mut contents = String::new();
    file.read_to_string(&mut contents).unwrap();  // 可能panic
    contents
}
```

### 正面示例 - 零成本抽象
```rust
// 推荐：使用迭代器零成本抽象
fn sum_even_squares(numbers: &[i32]) -> i32 {
    numbers
        .iter()
        .filter(|&&x| x % 2 == 0)
        .map(|&x| x * x)
        .sum()
}

// 推荐：使用泛型减少代码重复
fn find_max<T: PartialOrd>(items: &[T]) -> Option<&T> {
    if items.is_empty() {
        None
    } else {
        let mut max = &items[0];
        for item in &items[1..] {
            if item > max {
                max = item;
            }
        }
        Some(max)
    }
}
```

### 反面示例 - 手动优化过度
```rust
// 不推荐：手动优化可能不如编译器优化
fn manual_sum_even_squares(numbers: &[i32]) -> i32 {
    let mut sum = 0;
    for i in 0..numbers.len() {
        if numbers[i] % 2 == 0 {
            sum += numbers[i] * numbers[i];
        }
    }
    sum
}
```

### 正面示例 - 异步编程
```rust
// 推荐：使用tokio进行异步编程
use tokio::fs::File;
use tokio::io::AsyncReadExt;

async fn read_file_async(path: &str) -> Result<String, std::io::Error> {
    let mut file = File::open(path).await?;
    let mut contents = String::new();
    file.read_to_string(&mut contents).await?;
    Ok(contents)
}
