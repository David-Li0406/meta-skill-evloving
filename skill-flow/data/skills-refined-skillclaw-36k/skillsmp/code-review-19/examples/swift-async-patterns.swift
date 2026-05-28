// MARK: - Swift Code Review: Async/Await Patterns
// This file demonstrates correct async/await patterns for code review.

import SwiftUI
import Foundation

// MARK: - Basic Async/Await Patterns

// GOOD: Basic async function
func fetchUser(id: String) async throws -> User {
    let url = URL(string: "https://api.example.com/users/\(id)")!
    let (data, response) = try await URLSession.shared.data(from: url)

    guard let httpResponse = response as? HTTPURLResponse,
          httpResponse.statusCode == 200 else {
        throw NetworkError.invalidResponse
    }

    return try JSONDecoder().decode(User.self, from: data)
}

// MARK: - Task Management

@Observable
@MainActor
class TaskManagementViewModel {
    var user: User?
    var isLoading = false
    var error: Error?

    // Store task reference for cancellation
    private var loadTask: Task<Void, Never>?

    func loadUser(id: String) {
        // Cancel previous task if exists
        loadTask?.cancel()

        loadTask = Task {
            isLoading = true
            defer { isLoading = false }

            do {
                // Check for cancellation
                try Task.checkCancellation()
                user = try await fetchUser(id: id)
            } catch is CancellationError {
                // Handle cancellation gracefully
                print("Task was cancelled")
            } catch {
                self.error = error
            }
        }
    }

    func cancel() {
        loadTask?.cancel()
    }
}

// MARK: - Parallel Execution

class ParallelExecutionExample {
    // GOOD: Execute independent tasks in parallel
    func fetchDashboardData() async throws -> DashboardData {
        async let user = fetchUser(id: "1")
        async let posts = fetchPosts()
        async let notifications = fetchNotifications()

        // Wait for all results
        return try await DashboardData(
            user: user,
            posts: posts,
            notifications: notifications
        )
    }

    // GOOD: Process array items in parallel with TaskGroup
    func fetchAllUsers(ids: [String]) async throws -> [User] {
        try await withThrowingTaskGroup(of: User.self) { group in
            for id in ids {
                group.addTask {
                    try await fetchUser(id: id)
                }
            }

            var users: [User] = []
            for try await user in group {
                users.append(user)
            }
            return users
        }
    }

    // GOOD: Limit concurrency
    func fetchUsersWithLimit(ids: [String], maxConcurrent: Int = 3) async throws -> [User] {
        try await withThrowingTaskGroup(of: User.self) { group in
            var iterator = ids.makeIterator()
            var results: [User] = []

            // Start initial batch
            for _ in 0..<min(maxConcurrent, ids.count) {
                if let id = iterator.next() {
                    group.addTask { try await fetchUser(id: id) }
                }
            }

            // Process results and add new tasks
            for try await user in group {
                results.append(user)
                if let id = iterator.next() {
                    group.addTask { try await fetchUser(id: id) }
                }
            }

            return results
        }
    }

    private func fetchPosts() async throws -> [Post] { [] }
    private func fetchNotifications() async throws -> [Notification] { [] }
}

// MARK: - Error Handling in Async Context

class AsyncErrorHandling {
    // GOOD: Proper error propagation
    func loadData() async throws -> Data {
        do {
            return try await performRequest()
        } catch let error as URLError where error.code == .notConnectedToInternet {
            throw AppError.offline
        } catch let error as DecodingError {
            throw AppError.invalidData
        } catch {
            throw AppError.unknown(error)
        }
    }

    // GOOD: Retry with exponential backoff
    func fetchWithRetry<T>(
        maxAttempts: Int = 3,
        operation: () async throws -> T
    ) async throws -> T {
        var lastError: Error?

        for attempt in 0..<maxAttempts {
            do {
                return try await operation()
            } catch {
                lastError = error

                // Don't retry on cancellation
                if error is CancellationError {
                    throw error
                }

                // Exponential backoff
                let delay = UInt64(pow(2.0, Double(attempt))) * 1_000_000_000
                try await Task.sleep(nanoseconds: delay)
            }
        }

        throw lastError ?? AppError.unknown(nil)
    }

    private func performRequest() async throws -> Data {
        Data()
    }
}

// MARK: - Async Sequences

class AsyncSequenceExample {
    // GOOD: Using AsyncSequence for streaming data
    func processStream() async throws {
        let stream = makeAsyncStream()

        for await value in stream {
            // Check for cancellation periodically
            try Task.checkCancellation()
            print("Received: \(value)")
        }
    }

    // GOOD: Creating custom AsyncSequence
    func makeAsyncStream() -> AsyncStream<Int> {
        AsyncStream { continuation in
            Task {
                for i in 1...10 {
                    continuation.yield(i)
                    try? await Task.sleep(nanoseconds: 100_000_000)
                }
                continuation.finish()
            }
        }
    }

    // GOOD: Transforming async sequences
    func fetchAndTransform() async throws {
        let urls = [
            URL(string: "https://example.com/1")!,
            URL(string: "https://example.com/2")!
        ]

        // Use AsyncStream to process URLs
        for url in urls {
            let (data, _) = try await URLSession.shared.data(from: url)
            print("Downloaded \(data.count) bytes")
        }
    }
}

// MARK: - Actor Pattern

// GOOD: Use Actor for thread-safe state
actor DataStore {
    private var cache: [String: Data] = [:]

    func get(_ key: String) -> Data? {
        cache[key]
    }

    func set(_ key: String, data: Data) {
        cache[key] = data
    }

    func clear() {
        cache.removeAll()
    }
}

// GOOD: Using actor in ViewModel
@Observable
@MainActor
class CachedDataViewModel {
    private let store = DataStore()
    var data: Data?

    func loadData(key: String) async {
        // Check cache first
        if let cached = await store.get(key) {
            data = cached
            return
        }

        // Fetch from network
        do {
            let newData = try await fetchFromNetwork(key: key)
            await store.set(key, data: newData)
            data = newData
        } catch {
            print("Error: \(error)")
        }
    }

    private func fetchFromNetwork(key: String) async throws -> Data {
        Data()
    }
}

// MARK: - Continuation Patterns

class ContinuationExample {
    // GOOD: Wrapping callback-based API
    func fetchLegacyData() async throws -> Data {
        try await withCheckedThrowingContinuation { continuation in
            legacyFetch { result in
                switch result {
                case .success(let data):
                    continuation.resume(returning: data)
                case .failure(let error):
                    continuation.resume(throwing: error)
                }
            }
        }
    }

    // GOOD: Wrapping delegate-based API
    func performOperation() async -> Bool {
        await withCheckedContinuation { continuation in
            let delegate = OperationDelegate { success in
                continuation.resume(returning: success)
            }
            startOperation(delegate: delegate)
        }
    }

    private func legacyFetch(completion: @escaping (Result<Data, Error>) -> Void) {}
    private func startOperation(delegate: OperationDelegate) {}
}

class OperationDelegate {
    private let completion: (Bool) -> Void

    init(completion: @escaping (Bool) -> Void) {
        self.completion = completion
    }
}

// MARK: - Supporting Types

struct User: Codable, Identifiable {
    let id: String
    var name: String
}

struct Post: Identifiable {
    let id: String
}

struct Notification: Identifiable {
    let id: String
}

struct DashboardData {
    let user: User
    let posts: [Post]
    let notifications: [Notification]
}

enum NetworkError: Error {
    case invalidResponse
}

enum AppError: Error {
    case offline
    case invalidData
    case unknown(Error?)
}
