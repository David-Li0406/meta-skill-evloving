// MARK: - Migration Before/After Examples
// Swift 5 から Swift 6 への移行例

import Foundation
import SwiftUI
import Observation

// ============================================================
// MARK: - Example 1: ViewModel Migration
// ============================================================

// BEFORE: Swift 5 - ObservableObject
// class OldViewModel: ObservableObject {
//     @Published var items: [Item] = []
//     @Published var isLoading = false
//     @Published var errorMessage: String?
//
//     func loadItems() {
//         isLoading = true
//         Task {
//             do {
//                 items = try await fetchItems()
//             } catch {
//                 errorMessage = error.localizedDescription
//             }
//             isLoading = false  // 警告: MainActor で実行されていない可能性
//         }
//     }
// }

// AFTER: Swift 6 - @Observable + @MainActor
@Observable
@MainActor
class NewViewModel {
    var items: [Item] = []
    var isLoading = false
    var errorMessage: String?

    func loadItems() async {
        isLoading = true
        defer { isLoading = false }

        do {
            items = try await fetchItems()
        } catch {
            errorMessage = error.localizedDescription
        }
    }
}

struct Item: Identifiable, Sendable {
    let id: UUID
    let name: String
}

func fetchItems() async throws -> [Item] {
    try await Task.sleep(for: .seconds(1))
    return [Item(id: UUID(), name: "Item 1")]
}

// ============================================================
// MARK: - Example 2: Shared Mutable State
// ============================================================

// BEFORE: Swift 5 - DispatchQueue での同期
// class OldCache {
//     private let queue = DispatchQueue(label: "cache")
//     private var storage: [String: Data] = [:]
//
//     func get(_ key: String) -> Data? {
//         queue.sync { storage[key] }
//     }
//
//     func set(_ key: String, value: Data) {
//         queue.async { self.storage[key] = value }
//     }
// }

// AFTER: Swift 6 - Actor
actor NewCache {
    private var storage: [String: Data] = [:]

    func get(_ key: String) -> Data? {
        storage[key]
    }

    func set(_ key: String, value: Data) {
        storage[key] = value
    }
}

// ============================================================
// MARK: - Example 3: Delegate Pattern
// ============================================================

// BEFORE: Swift 5 - Protocol without Sendable
// protocol OldDelegate: AnyObject {
//     func didReceiveData(_ data: Data)
// }
//
// class OldDataFetcher {
//     weak var delegate: OldDelegate?
//
//     func fetch() {
//         Task {
//             let data = await fetchData()
//             delegate?.didReceiveData(data)  // 警告: データ競合の可能性
//         }
//     }
// }

// AFTER: Swift 6 - @MainActor Delegate
@MainActor
protocol NewDelegate: AnyObject {
    func didReceiveData(_ data: Data)
}

@MainActor
class NewDataFetcher {
    weak var delegate: NewDelegate?

    func fetch() async {
        let data = await fetchData()
        delegate?.didReceiveData(data)  // 安全: MainActor 上で実行
    }
}

func fetchData() async -> Data {
    try? await Task.sleep(for: .seconds(1))
    return Data()
}

// ============================================================
// MARK: - Example 4: Completion Handler to async/await
// ============================================================

// BEFORE: Swift 5 - Completion Handler
// func oldFetchUser(id: String, completion: @escaping (Result<User, Error>) -> Void) {
//     URLSession.shared.dataTask(with: URL(string: "...")!) { data, _, error in
//         if let error {
//             completion(.failure(error))
//             return
//         }
//         // デコード処理
//         completion(.success(user))
//     }.resume()
// }

// AFTER: Swift 6 - async/await
func newFetchUser(id: String) async throws -> User {
    let url = URL(string: "https://api.example.com/users/\(id)")!
    let (data, _) = try await URLSession.shared.data(from: url)
    return try JSONDecoder().decode(User.self, from: data)
}

struct User: Codable, Sendable {
    let id: String
    let name: String
}

// ============================================================
// MARK: - Example 5: Notification Handling
// ============================================================

// BEFORE: Swift 5 - NotificationCenter with closure
// class OldObserver {
//     var observer: NSObjectProtocol?
//
//     func startObserving() {
//         observer = NotificationCenter.default.addObserver(
//             forName: .someNotification,
//             object: nil,
//             queue: .main
//         ) { [weak self] notification in
//             self?.handleNotification(notification)
//         }
//     }
// }

// AFTER: Swift 6 - AsyncSequence
@MainActor
class NewObserver {
    private var observationTask: Task<Void, Never>?

    func startObserving() {
        observationTask = Task {
            for await notification in NotificationCenter.default.notifications(named: .someNotification) {
                handleNotification(notification)
            }
        }
    }

    func stopObserving() {
        observationTask?.cancel()
    }

    private func handleNotification(_ notification: Notification) {
        print("Received: \(notification)")
    }
}

extension Notification.Name {
    static let someNotification = Notification.Name("someNotification")
}

// ============================================================
// MARK: - Example 6: Singleton Pattern
// ============================================================

// BEFORE: Swift 5 - Class Singleton
// class OldNetworkManager {
//     static let shared = OldNetworkManager()
//     private init() {}
//
//     var baseURL: URL?  // 警告: データ競合の可能性
//
//     func request(_ endpoint: String) async throws -> Data {
//         // ...
//     }
// }

// AFTER: Swift 6 - Actor Singleton
actor NewNetworkManager {
    static let shared = NewNetworkManager()
    private init() {}

    var baseURL: URL?

    func request(_ endpoint: String) async throws -> Data {
        guard let baseURL else {
            throw NetworkError.noBaseURL
        }
        let url = baseURL.appendingPathComponent(endpoint)
        let (data, _) = try await URLSession.shared.data(from: url)
        return data
    }
}

enum NetworkError: Error {
    case noBaseURL
}

// ============================================================
// MARK: - Example 7: Property Wrapper Migration
// ============================================================

// BEFORE: Swift 5 - @Published in ObservableObject
// class OldSettings: ObservableObject {
//     @Published var isDarkMode = false
//     @Published var fontSize: CGFloat = 14
// }

// AFTER: Swift 6 - @Observable (no @Published needed)
@Observable
@MainActor
class NewSettings {
    var isDarkMode = false
    var fontSize: CGFloat = 14
}

// SwiftUI View での使用
// BEFORE:
// struct OldSettingsView: View {
//     @StateObject private var settings = OldSettings()
// }

// AFTER:
struct NewSettingsView: View {
    @State private var settings = NewSettings()

    var body: some View {
        Form {
            Toggle("Dark Mode", isOn: $settings.isDarkMode)
            Slider(value: $settings.fontSize, in: 10...24)
        }
    }
}

// ============================================================
// MARK: - Example 8: Timer Migration
// ============================================================

// BEFORE: Swift 5 - Timer with closure
// class OldTimerManager {
//     var timer: Timer?
//
//     func start() {
//         timer = Timer.scheduledTimer(withTimeInterval: 1.0, repeats: true) { [weak self] _ in
//             self?.tick()
//         }
//     }
// }

// AFTER: Swift 6 - Task with sleep
@MainActor
class NewTimerManager {
    private var timerTask: Task<Void, Never>?
    var tickCount = 0

    func start() {
        timerTask = Task {
            while !Task.isCancelled {
                tick()
                try? await Task.sleep(for: .seconds(1))
            }
        }
    }

    func stop() {
        timerTask?.cancel()
    }

    private func tick() {
        tickCount += 1
        print("Tick: \(tickCount)")
    }
}
