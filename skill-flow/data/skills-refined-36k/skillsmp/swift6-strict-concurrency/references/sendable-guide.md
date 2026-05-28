# Sendable Protocol 完全ガイド

Swift 6 の Strict Concurrency における Sendable プロトコルの詳細ガイド。

## 概要

`Sendable` は、型が並行コンテキスト間で安全に転送できることを示すマーカープロトコル。Swift 6 では、Task 境界や Actor 境界を越えるすべての値が Sendable である必要がある。

## 自動準拠

### 値型（Struct）

すべての stored property が Sendable なら、struct は自動的に Sendable に準拠：

```swift
// 自動的に Sendable
struct UserProfile {
    let id: UUID
    let name: String
    let createdAt: Date
}

// 使用例
Task {
    let profile = UserProfile(id: UUID(), name: "Alice", createdAt: Date())
    print(profile.name)  // OK
}
```

### 列挙型（Enum）

すべての associated value が Sendable なら、enum は自動的に Sendable に準拠：

```swift
// 自動的に Sendable
enum Result<T: Sendable> {
    case success(T)
    case failure(Error)
}

enum AppState {
    case idle
    case loading
    case loaded([String])  // [String] は Sendable
}
```

### Actor

Actor は常に Sendable：

```swift
actor DataStore {
    var items: [String] = []
}

// Actor への参照は Sendable
let store = DataStore()
Task {
    await store.items  // OK
}
```

## 手動準拠（Reference Types）

### final class + immutable properties

クラスを Sendable にするための条件：
1. `final` であること
2. すべての stored property が `let`（不変）であること
3. すべての stored property が Sendable であること

```swift
final class AppConfig: Sendable {
    let apiURL: URL
    let apiKey: String
    let timeout: TimeInterval

    init(apiURL: URL, apiKey: String, timeout: TimeInterval = 30) {
        self.apiURL = apiURL
        self.apiKey = apiKey
        self.timeout = timeout
    }
}
```

### NG パターン

```swift
// ❌ var プロパティがある
final class BadConfig1: Sendable {  // Error
    var value: String = ""
}

// ❌ final でない
class BadConfig2: Sendable {  // Error
    let value: String
}

// ❌ 非 Sendable プロパティがある
final class BadConfig3: Sendable {  // Error
    let object: NSObject  // NSObject は非 Sendable
}
```

## @unchecked Sendable

内部で適切な同期処理を行っている場合にコンパイラチェックをバイパス：

```swift
final class ThreadSafeCounter: @unchecked Sendable {
    private let lock = NSLock()
    private var _count = 0

    var count: Int {
        lock.lock()
        defer { lock.unlock() }
        return _count
    }

    func increment() {
        lock.lock()
        defer { lock.unlock() }
        _count += 1
    }
}
```

### 注意事項

- `@unchecked Sendable` は最後の手段
- 内部で確実に同期処理を行っていることを保証する必要がある
- 可能な限り Actor を使用することを推奨

## @Sendable クロージャ

### 基本

```swift
// Task のクロージャは暗黙的に @Sendable
Task {
    // Sendable な値のみキャプチャ可能
}

// 明示的な @Sendable
let handler: @Sendable () -> Void = {
    print("Sendable closure")
}
```

### 関数パラメータ

```swift
func performAsync(work: @Sendable @escaping () async -> Void) {
    Task { await work() }
}

func map<T: Sendable, U: Sendable>(
    value: T,
    transform: @Sendable (T) -> U
) -> U {
    transform(value)
}
```

### キャプチャリスト

```swift
@MainActor
class ViewModel {
    var count = 0
    let id = UUID()

    func work() {
        // ❌ self は非 Sendable（@MainActor isolated）
        // Task.detached {
        //     self.count += 1  // Error
        // }

        // ✅ MainActor.run を使用
        Task.detached {
            await MainActor.run {
                self.count += 1
            }
        }

        // ✅ Sendable な値をキャプチャ
        Task.detached { [id = self.id] in
            print(id)  // OK
        }
    }
}
```

## Protocol と Sendable

### Protocol に Sendable 制約を追加

```swift
protocol DataProtocol: Sendable {
    var id: UUID { get }
}

// 準拠する型も Sendable でなければならない
struct DataItem: DataProtocol {
    let id: UUID
    let value: String
}
```

### ジェネリック制約

```swift
struct Container<T: Sendable>: Sendable {
    let value: T
}

func process<T: Sendable>(_ value: T) async {
    Task {
        print(value)  // T が Sendable なので OK
    }
}
```

## 標準ライブラリの Sendable 型

以下の型は Sendable：

- 基本型: `Int`, `Double`, `Bool`, `String`, etc.
- コレクション（要素が Sendable の場合）: `Array`, `Dictionary`, `Set`
- Foundation 型: `UUID`, `Date`, `URL`, `Data`
- `Error` プロトコル
- `Optional<T>` (T が Sendable の場合)
- タプル（すべての要素が Sendable の場合）

## Sendable でない型

以下の型は Sendable ではない：

- `NSObject` とそのサブクラス（一部例外あり）
- `class`（final + immutable でない限り）
- 可変参照を持つ型
- クロージャ（`@Sendable` でない限り）

## よくある問題と解決策

### 問題 1: 非 Sendable 型のキャプチャ

```swift
class Logger { func log(_ msg: String) {} }

let logger = Logger()
// Task { logger.log("message") }  // Error

// 解決策: Actor を使用
actor SafeLogger {
    func log(_ msg: String) { print(msg) }
}
```

### 問題 2: Delegate パターン

```swift
// protocol Delegate: AnyObject { ... }  // 非 Sendable

// 解決策: @MainActor を追加
@MainActor
protocol SafeDelegate: AnyObject {
    func didComplete()
}
```

### 問題 3: Completion Handler

```swift
// 古い API を async/await に変換
func modernAPI() async -> Data {
    await withCheckedContinuation { continuation in
        oldAPI { data in
            continuation.resume(returning: data)
        }
    }
}
```

## チェックリスト

- [ ] すべての Task 境界で Sendable な値のみを渡しているか
- [ ] Actor 境界を越える値が Sendable か
- [ ] クラスを Sendable にする場合、final + immutable か
- [ ] @unchecked Sendable を使う場合、内部で同期処理を行っているか
- [ ] Protocol に Sendable 制約を追加すべきか検討したか
