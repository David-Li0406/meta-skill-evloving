# iOS/macOS API 设计最佳实践

## 概述
本文档总结 Apple 平台（iOS/macOS）在 API 设计方面的核心原则和最佳实践。

## 核心原则

### 1. 清晰性（Clarity）
- **命名原则**：
  - 使用清晰、明确的命名
  - 避免缩写（除非是众所周知的缩写）
  - 方法名应描述其作用和效果
- **示例**：
  - ✅ `removeElement(at:)` - 清晰表达移除操作
  - ❌ `remove(_:)` - 不明确移除什么

### 2. 一致性（Consistency）
- **命名约定**：
  - 动词方法：执行操作（如 `add`, `remove`, `insert`）
  - 名词属性：表示状态（如 `count`, `isEmpty`, `title`）
  - 布尔值：使用 `is` 前缀（如 `isEmpty`, `isEnabled`）
- **参数标签**：
  - 第一个参数通常无标签
  - 后续参数使用有意义的标签

### 3. 表达性（Expressiveness）
- **流畅 API**：方法链式调用
- **类型安全**：利用 Swift 的类型系统
- **可选值处理**：使用 Optional 明确表达"可能没有值"

## Swift API 设计指南

### 方法命名
```swift
// 推荐：清晰描述操作和参数
func insert(_ element: Element, at index: Int)

// 推荐：使用介词连接参数
func move(from start: Index, to end: Index)

// 推荐：布尔返回值使用 is/has
func isEmpty() -> Bool
var hasPrefix: Bool
```

### 协议（Protocol）
```swift
// 能力协议：使用 -able/-ible 后缀
protocol Equatable { }
protocol Comparable { }

// 类型协议：使用名词
protocol Collection { }
protocol Iterator { }
```

### 错误处理
```swift
// 使用 Result 或 throws
func loadData() throws -> Data
func loadData(completion: (Result<Data, Error>) -> Void)

// 定义清晰的错误类型
enum NetworkError: Error {
    case invalidURL
    case requestFailed(statusCode: Int)
    case decodingFailed
}
```

## Objective-C API 设计指南

### 命名约定
```objc
// 方法名：动词 + 直接宾语 + 介词短语
- (void)insertObject:(id)obj atIndex:(NSUInteger)index;

// 属性名：名词或形容词
@property (nonatomic, copy) NSString *title;
@property (nonatomic, assign, getter=isEnabled) BOOL enabled;

// 委托方法：包含发送者
- (void)tableView:(UITableView *)tableView didSelectRowAtIndexPath:(NSIndexPath *)indexPath;
```

## 现代 API 特性

### async/await（Swift 5.5+）
```swift
// 异步方法
func fetchData() async throws -> Data {
    let (data, _) = try await URLSession.shared.data(from: url)
    return data
}
```

### Actor（并发安全）
```swift
actor DataCache {
    private var cache: [String: Data] = [:]

    func data(for key: String) -> Data? {
        return cache[key]
    }
}
```

## 参考资源
- Swift API Design Guidelines: https://swift.org/documentation/api-design-guidelines/
- Human Interface Guidelines: https://developer.apple.com/design/human-interface-guidelines/
