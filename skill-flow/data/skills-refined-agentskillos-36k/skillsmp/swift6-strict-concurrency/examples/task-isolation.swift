// MARK: - Task Isolation
// Task と Task.detached の分離コンテキストの違い

import Foundation
import SwiftUI

// MARK: - Task vs Task.detached

/// Task は親の actor context を継承する
/// Task.detached は完全に独立した context で実行される

@MainActor
class TaskIsolationDemo {
    var counter = 0

    func demonstrateTaskInheritance() {
        print("Starting on MainActor")

        // Task は MainActor を継承
        Task {
            // ここは MainActor 上で実行される
            print("Task: Running on MainActor? \(Thread.isMainThread)")
            counter += 1  // OK: MainActor context を継承
        }

        // Task.detached は MainActor から切り離される
        Task.detached {
            print("Detached: Running on MainActor? \(Thread.isMainThread)")
            // self.counter += 1  // Error: Actor-isolated property

            // MainActor に戻る必要がある
            await MainActor.run {
                self.counter += 1
            }
        }
    }
}

// MARK: - Task の優先度継承

func demonstratePriorityInheritance() {
    Task(priority: .high) {
        print("High priority task")

        // 子 Task は親の優先度を継承
        Task {
            print("Child task inherits high priority")
        }

        // Task.detached はデフォルト優先度
        Task.detached {
            print("Detached task has default priority")
        }

        // 明示的に優先度を指定
        Task.detached(priority: .low) {
            print("Detached task with low priority")
        }
    }
}

// MARK: - TaskGroup での並行実行

func processItemsConcurrently() async -> [String] {
    let items = ["A", "B", "C", "D", "E"]

    return await withTaskGroup(of: String.self) { group in
        for item in items {
            group.addTask {
                // 各タスクは並行実行される
                try? await Task.sleep(for: .milliseconds(100))
                return "Processed: \(item)"
            }
        }

        var results: [String] = []
        for await result in group {
            results.append(result)
        }
        return results
    }
}

// MARK: - ThrowingTaskGroup

enum ProcessingError: Error {
    case failed(String)
}

func processWithErrors() async throws -> [String] {
    let items = ["A", "B", "error", "D"]

    return try await withThrowingTaskGroup(of: String.self) { group in
        for item in items {
            group.addTask {
                if item == "error" {
                    throw ProcessingError.failed(item)
                }
                return "Processed: \(item)"
            }
        }

        var results: [String] = []
        for try await result in group {
            results.append(result)
        }
        return results
    }
}

// MARK: - Task のキャンセル

func demonstrateCancellation() async {
    let task = Task {
        for i in 1...10 {
            // キャンセルをチェック
            try Task.checkCancellation()

            // または、キャンセルされたかどうかを確認
            if Task.isCancelled {
                print("Task was cancelled at iteration \(i)")
                return
            }

            print("Processing \(i)")
            try await Task.sleep(for: .milliseconds(100))
        }
    }

    // 少し待ってからキャンセル
    try? await Task.sleep(for: .milliseconds(350))
    task.cancel()

    // タスクの完了を待つ
    _ = await task.result
}

// MARK: - async let での並行実行

func fetchUserData() async throws -> (profile: UserProfile, posts: [Post]) {
    // async let で並行実行
    async let profile = fetchProfile()
    async let posts = fetchPosts()

    // 両方の結果を待つ
    return try await (profile, posts)
}

func fetchProfile() async throws -> UserProfile {
    try await Task.sleep(for: .seconds(1))
    return UserProfile(id: UUID(), name: "Alice")
}

func fetchPosts() async throws -> [Post] {
    try await Task.sleep(for: .seconds(1))
    return [Post(id: UUID(), title: "Hello")]
}

struct UserProfile: Sendable {
    let id: UUID
    let name: String
}

struct Post: Sendable {
    let id: UUID
    let title: String
}

// MARK: - @MainActor での Task 使用パターン

@MainActor
class DownloadManager {
    var downloads: [UUID: DownloadTask] = [:]
    var progress: [UUID: Double] = [:]

    func startDownload(url: URL) -> UUID {
        let id = UUID()

        // Task は MainActor を継承するので、self にアクセス可能
        let task = Task {
            await performDownload(id: id, url: url)
        }

        downloads[id] = DownloadTask(id: id, task: task)
        return id
    }

    private func performDownload(id: UUID, url: URL) async {
        for i in 0...100 {
            // キャンセルチェック
            if Task.isCancelled {
                downloads.removeValue(forKey: id)
                progress.removeValue(forKey: id)
                return
            }

            // 進捗更新（MainActor 上で実行される）
            progress[id] = Double(i) / 100.0

            try? await Task.sleep(for: .milliseconds(50))
        }

        downloads.removeValue(forKey: id)
    }

    func cancelDownload(id: UUID) {
        downloads[id]?.task.cancel()
    }
}

struct DownloadTask {
    let id: UUID
    let task: Task<Void, Never>
}

// MARK: - Unstructured Task からの値の取得

func demonstrateTaskValue() async {
    // Task から値を取得
    let task = Task {
        try await Task.sleep(for: .seconds(1))
        return 42
    }

    // .value で結果を取得（throws の場合は try が必要）
    let result = await task.value
    print("Result: \(result)")

    // .result で Result 型を取得
    let resultType = await task.result
    switch resultType {
    case .success(let value):
        print("Success: \(value)")
    case .failure(let error):
        print("Error: \(error)")
    }
}

// MARK: - SwiftUI での Task 使用

struct TaskDemoView: View {
    @State private var data: [String] = []
    @State private var loadTask: Task<Void, Never>?

    var body: some View {
        List(data, id: \.self) { item in
            Text(item)
        }
        .task {
            // View のライフサイクルに紐づいた Task
            // View が消えると自動的にキャンセルされる
            await loadData()
        }
        .onDisappear {
            // 手動で管理する Task はキャンセルが必要
            loadTask?.cancel()
        }
    }

    func loadData() async {
        try? await Task.sleep(for: .seconds(1))
        data = ["Item 1", "Item 2", "Item 3"]
    }

    func startManualTask() {
        loadTask = Task {
            await loadData()
        }
    }
}
