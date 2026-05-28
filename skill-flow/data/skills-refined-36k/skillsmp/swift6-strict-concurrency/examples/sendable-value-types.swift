// MARK: - Sendable Value Types
// 値型（struct/enum）の Sendable 自動準拠例

import Foundation

// MARK: - 自動的に Sendable に準拠する struct

/// すべてのプロパティが Sendable なら、struct は自動的に Sendable
struct UserProfile: Sendable {
    let id: UUID
    let name: String
    let email: String
    let createdAt: Date
}

/// ネストした値型も自動準拠
struct Address: Sendable {
    let street: String
    let city: String
    let postalCode: String
}

struct ContactInfo: Sendable {
    let phone: String
    let address: Address  // Address も Sendable なので OK
}

// MARK: - 自動的に Sendable に準拠する enum

/// 関連値がすべて Sendable なら、enum は自動的に Sendable
enum NetworkResult<T: Sendable>: Sendable {
    case success(T)
    case failure(Error)  // Error は Sendable に準拠
}

enum AppState: Sendable {
    case idle
    case loading
    case loaded(data: [String])
    case error(message: String)
}

/// Raw value を持つ enum も自動準拠
enum Priority: Int, Sendable {
    case low = 0
    case medium = 1
    case high = 2
}

// MARK: - ジェネリック型と Sendable

/// ジェネリック型は型パラメータに Sendable 制約が必要
struct Container<T: Sendable>: Sendable {
    let value: T
}

/// 複数の型パラメータ
struct Pair<A: Sendable, B: Sendable>: Sendable {
    let first: A
    let second: B
}

// MARK: - 使用例

func demonstrateSendableValueTypes() async {
    let profile = UserProfile(
        id: UUID(),
        name: "John Doe",
        email: "john@example.com",
        createdAt: Date()
    )

    // Task 境界を安全に越えられる
    Task {
        print("User: \(profile.name)")  // OK: UserProfile は Sendable
    }

    let state = AppState.loading

    Task.detached {
        switch state {
        case .loading:
            print("Loading...")
        default:
            break
        }
    }
}

// MARK: - 注意: 非 Sendable プロパティを含む場合

/// この struct は自動的には Sendable にならない
/// （NSObject は Sendable ではない）
// struct BadExample {
//     let id: String
//     let object: NSObject  // Error: NSObject is not Sendable
// }

/// 解決策: actor を使うか、Sendable なプロパティのみにする
struct GoodExample: Sendable {
    let id: String
    let data: Data  // Data は Sendable
}
