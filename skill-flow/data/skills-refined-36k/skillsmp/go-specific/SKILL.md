---
name: go-specific
version: 1.0.0
description: Go语言特有审查规则（并发模式、错误处理、性能调优）
language: go
tags: [go, golang, concurrency, goroutine, channel]
frameworks: [gin, echo, fiber, beego]
---

# Go特有审查规则

## 并发模式
- **goroutine管理**: 避免goroutine泄漏、使用context控制超时、合理控制并发数量
- **channel使用**: 避免死锁、正确关闭channel、使用select处理多channel
- **context传播**: 正确传递context、使用context.WithTimeout/WithCancel
- **同步原语**: 优先使用channel、合理使用sync包、避免过度使用锁

## 错误处理
- **error包装**: 使用fmt.Errorf包装错误、使用%w进行错误链追踪
- **panic/recover**: 只在不可恢复错误使用panic、在main函数中recover
- **错误类型**: 定义自定义错误类型、使用errors.Is/errors.As进行错误判断
- **错误返回**: 始终检查错误、避免忽略错误、错误处理前置

## 性能调优
- **内存分配**: 减少不必要的内存分配、重用对象、使用sync.Pool
- **pprof使用**: 集成性能分析、定位内存泄漏、CPU热点分析
- **竞态检测**: 使用-race检测竞态条件、避免共享内存
- **编译优化**: 使用go build -ldflags优化、减少二进制大小

## 模块管理
- **go.mod**: 保持依赖整洁、使用语义化版本、避免使用replace
- **依赖版本**: 定期更新依赖、使用go mod tidy清理、避免间接依赖冲突
- **兼容性**: 遵循Go兼容性承诺、使用build tag处理版本差异

## 代码示例

### 正面示例 - goroutine管理
```go
// 推荐：使用context控制goroutine生命周期
func fetchData(ctx context.Context, urls []string) ([]Result, error) {
    ctx, cancel := context.WithTimeout(ctx, 30*time.Second)
    defer cancel()
    
    results := make([]Result, len(urls))
    g, ctx := errgroup.WithContext(ctx)
    
    for i, url := range urls {
        i, url := i, url // 避免闭包捕获问题
        g.Go(func() error {
            resp, err := http.Get(url)
            if err != nil {
                return fmt.Errorf("failed to fetch %s: %w", url, err)
            }
            defer resp.Body.Close()
            
            data, err := io.ReadAll(resp.Body)
            if err != nil {
                return fmt.Errorf("failed to read response from %s: %w", url, err)
            }
            
            results[i] = Result{URL: url, Data: data}
            return nil
        })
    }
    
    return results, g.Wait()
}
```

### 反面示例 - goroutine泄漏
```go
// 不推荐：没有控制goroutine生命周期
func badFetch(urls []string) {
    for _, url := range urls {
        go func(u string) {
            for {
                // 无限循环，没有退出条件
                resp, _ := http.Get(u)
                resp.Body.Close()
                time.Sleep(time.Minute)
            }
        }(url)
    }
}
```

### 正面示例 - 错误处理
```go
// 推荐：完整的错误处理
func readConfig(filename string) (*Config, error) {
    file, err := os.Open(filename)
    if err != nil {
        return nil, fmt.Errorf("failed to open config file %s: %w", filename, err)
    }
    defer file.Close()
    
    var config Config
    if err := json.NewDecoder(file).Decode(&config); err != nil {
        return nil, fmt.Errorf("failed to decode config from %s: %w", filename, err)
    }
    
    if err := config.Validate(); err != nil {
        return nil, fmt.Errorf("invalid config in %s: %w", filename, err)
    }
    
    return &config, nil
}
```

### 反面示例 - 忽略错误
```go
// 不推荐：忽略错误
func badReadConfig(filename string) *Config {
    file, _ := os.Open(filename) // 忽略错误
    defer file.Close()
    
    var config Config
    json.NewDecoder(file).Decode(&config) // 忽略错误
    return &config
}
```

### 正面示例 - 内存优化
```go
// 推荐：使用对象池减少GC压力
var bufferPool = sync.Pool{
    New: func() interface{} {
        return new(bytes.Buffer)
    },
}

func processData(data []byte) {
    buf := bufferPool.Get().(*bytes.Buffer)
    buf.Reset()
    defer bufferPool.Put(buf)
    
    // 使用buf处理数据
    buf.Write(data)
    // ... 处理逻辑
}
```

### 反面示例 - 频繁分配
```go
// 不推荐：频繁分配内存
func badProcess(data []byte) {
    for i := 0; i < len(data); i++ {
        buf := bytes.NewBuffer(data[:i+1]) // 每次循环都分配
        // ... 处理逻辑
    }
}
```

### 正面示例 - context使用
```go
// 推荐：正确传递context
func (s *Server) handleRequest(w http.ResponseWriter, r *http.Request) {
    ctx := r.Context()
    
    userID := r.URL.Query().Get("user_id")
    user, err := s.getUser(ctx, userID)
    if err != nil {
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }
    
    // 使用context传递请求范围的数据
    ctx = context.WithValue(ctx, userKey, user)
    s.processUserData(ctx, w, r)
}
