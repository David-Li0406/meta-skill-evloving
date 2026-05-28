---
name: rust-optimization-and-best-practices
description: Use this skill when optimizing Rust code for performance, memory management, concurrency, and applying best practices in ownership and error handling.
---

# Rust Optimization and Best Practices

## 适用范围
- Rust 性能与内存优化
- 缓存/并行计算策略
- 线性规划与数值计算加速
- Rust 特有审查规则（所有权系统、并发安全、错误处理）

## 关键规则
### 所有权系统
- **借用规则**: 避免悬垂引用、正确使用生命周期参数、避免借用检查器冲突
- **智能指针**: 合理使用Box/Rc/Arc、避免过度包装、使用Deref trait
- **内存安全**: 避免内存泄漏、正确使用drop trait、避免循环引用

### 并发安全
- **Send/Sync**: 正确实现Send/Sync trait、避免跨线程共享非Send类型
- **无锁编程**: 使用原子操作、避免数据竞争、使用Arc<Mutex<T>>保护共享数据
- **异步编程**: 正确使用async/await、避免阻塞异步执行器、使用tokio runtime

### 性能优化
- **零成本抽象**: 使用迭代器、避免不必要的堆分配、使用inline优化
- **缓存策略**: 高频静态数据优先缓存，使用 `moka`
- **并行计算**: CPU 密集任务使用 `rayon` 或 `tokio::task::spawn_blocking`
- **避免无意义 clone**: 优先借用切片与引用

## 快速模板
### Moka 缓存
```rust
use moka::future::Cache;
use std::time::Duration;

pub struct MaterialCache {
    cache: Cache<String, crate::material::material::Material>,
}

impl MaterialCache {
    pub fn new() -> Self {
        Self {
            cache: Cache::builder()
                .max_capacity(1000)
                .time_to_live(Duration::from_secs(3600))
                .build(),
        }
    }
}
```

### Rayon 并行
```rust
use rayon::prelude::*;

let totals: Vec<f64> = materials
    .par_iter()
    .map(|m| m.price)
    .collect();
```

### 阻塞计算下沉
```rust
let result = tokio::task::spawn_blocking(move || heavy_calc(input))
    .await?;
```

## 错误处理
- **Result类型**: 正确处理Result、使用?运算符传播错误、避免unwrap/expect
- **自定义错误**: 实现Error trait、使用thiserror创建错误类型、错误链处理

## 检查清单
- [ ] 是否存在重复计算可缓存
- [ ] CPU 密集任务是否并行化
- [ ] 异步路径无阻塞调用
- [ ] clone 明确且必要
- [ ] 是否遵循所有权和生命周期规则

## 代码示例
### 正面示例 - 所有权管理
```rust
fn process_data(data: &str) -> String {
    let processed: String = data
        .chars()
        .filter(|c| c.is_alphanumeric())
        .collect();
    processed
}
```

### 正面示例 - 并发安全
```rust
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

### 正面示例 - 错误处理
```rust
use std::error::Error;
use std::fs::File;
use std::io::Read;

fn read_config(filename: &str) -> Result<String, Box<dyn Error>> {
    let mut file = File::open(filename)?;
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;
    Ok(contents)
}
```