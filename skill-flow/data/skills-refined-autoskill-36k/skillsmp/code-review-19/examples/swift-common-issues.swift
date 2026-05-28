// MARK: - Swift Code Review: Common Issues
// This file demonstrates common issues found in Swift code reviews and their fixes.

import SwiftUI
import Foundation

// MARK: - Issue 1: Retain Cycles in Closures

class RetainCycleExample {
    var completionHandler: (() -> Void)?
    var name = "Example"

    // BAD: Creates retain cycle
    func setupBad() {
        completionHandler = {
            print(self.name)  // Strong reference to self
        }
    }

    // GOOD: Use weak self
    func setupGood() {
        completionHandler = { [weak self] in
            guard let self else { return }
            print(self.name)
        }
    }

    // GOOD: Use unowned when you're certain self outlives the closure
    func setupUnowned() {
        // Only use unowned when closure lifecycle is shorter than self
        completionHandler = { [unowned self] in
            print(self.name)
        }
    }
}

// MARK: - Issue 2: Force Unwrapping

class ForceUnwrapExample {
    // BAD: Force unwrap can crash
    func getBadFirstUser(users: [User]) -> User {
        return users.first!
    }

    // BAD: Implicitly unwrapped optional as property
    var badConfig: Configuration!

    // GOOD: Use guard let
    func getGoodFirstUser(users: [User]) -> User? {
        guard let user = users.first else {
            return nil
        }
        return user
    }

    // GOOD: Use if let with early return
    func processUser(users: [User]) {
        if let user = users.first {
            // Process user
            print(user.name)
        }
    }

    // GOOD: Use optional chaining
    func getUserName(users: [User]) -> String {
        users.first?.name ?? "Unknown"
    }
}

// MARK: - Issue 3: Main Thread Violations

@Observable
class MainThreadExample {
    var items: [String] = []

    // BAD: No MainActor, UI update may happen on background thread
    func loadItemsBad() async {
        let fetchedItems = await fetchFromNetwork()
        items = fetchedItems  // May not be on main thread!
    }

    // GOOD: Use @MainActor
    @MainActor
    func loadItemsGood() async {
        let fetchedItems = await fetchFromNetwork()
        items = fetchedItems  // Guaranteed on main thread
    }

    // GOOD: Alternative with MainActor.run
    func loadItemsAlternative() async {
        let fetchedItems = await fetchFromNetwork()
        await MainActor.run {
            items = fetchedItems
        }
    }

    private func fetchFromNetwork() async -> [String] {
        // Simulated network call
        return ["Item 1", "Item 2"]
    }
}

// MARK: - Issue 4: Improper Error Handling

enum NetworkError: Error {
    case invalidResponse
    case serverError(code: Int)
}

class ErrorHandlingExample {
    // BAD: Swallowing errors
    func fetchDataBad() async {
        do {
            let _ = try await performRequest()
        } catch {
            // Silent failure - bad!
        }
    }

    // BAD: Using try? when error matters
    func fetchDataBad2() async -> Data? {
        return try? await performRequest()  // Error information lost
    }

    // GOOD: Proper error propagation
    func fetchDataGood() async throws -> Data {
        do {
            return try await performRequest()
        } catch {
            // Log error for debugging
            print("Network error: \(error)")
            throw error
        }
    }

    // GOOD: Transform to domain error
    func fetchDataWithDomainError() async throws -> Data {
        do {
            return try await performRequest()
        } catch let urlError as URLError {
            throw NetworkError.serverError(code: urlError.errorCode)
        } catch {
            throw NetworkError.invalidResponse
        }
    }

    private func performRequest() async throws -> Data {
        Data()
    }
}

// MARK: - Issue 5: Inefficient String Operations

class StringOperationsExample {
    // BAD: String concatenation in loop
    func buildStringBad(items: [String]) -> String {
        var result = ""
        for item in items {
            result += item + ", "  // Creates new string each iteration
        }
        return result
    }

    // GOOD: Use joined
    func buildStringGood(items: [String]) -> String {
        items.joined(separator: ", ")
    }

    // BAD: Multiple string interpolations
    func formatMessageBad(user: User, count: Int) -> String {
        let part1 = "User: " + user.name
        let part2 = part1 + " has "
        let part3 = part2 + String(count)
        return part3 + " items"
    }

    // GOOD: Single interpolation
    func formatMessageGood(user: User, count: Int) -> String {
        "User: \(user.name) has \(count) items"
    }
}

// MARK: - Issue 6: Excessive Optional Chaining

class OptionalChainingExample {
    // BAD: Deep optional chaining is hard to debug
    func getCityBad(user: User?) -> String? {
        user?.profile?.address?.city?.name?.uppercased()
    }

    // GOOD: Break into meaningful steps with guard
    func getCityGood(user: User?) -> String? {
        guard let user = user,
              let profile = user.profile,
              let address = profile.address,
              let city = address.city else {
            return nil
        }
        return city.name?.uppercased()
    }
}

// MARK: - Issue 7: Misusing @State

struct StateExample: View {
    // BAD: Initializing @State with computed value
    @State private var badItems = loadInitialItems()  // Called every view init

    // GOOD: Use init for complex initialization
    @State private var goodItems: [String]

    init(initialItems: [String] = []) {
        _goodItems = State(initialValue: initialItems)
    }

    var body: some View {
        List(goodItems, id: \.self) { item in
            Text(item)
        }
    }

    private static func loadInitialItems() -> [String] {
        ["Item 1", "Item 2"]
    }
}

// MARK: - Issue 8: Not Using Swift Concurrency Features

class ConcurrencyExample {
    // BAD: Callback-based async
    func fetchUserBad(completion: @escaping (User?) -> Void) {
        DispatchQueue.global().async {
            // Fetch user
            let user = User(id: UUID(), name: "Test", isActive: true, address: nil)
            DispatchQueue.main.async {
                completion(user)
            }
        }
    }

    // GOOD: async/await
    func fetchUserGood() async -> User? {
        // Fetch user
        return User(id: UUID(), name: "Test", isActive: true, address: nil)
    }

    // BAD: Nested callbacks (callback hell)
    func fetchDataBad(completion: @escaping (Data?) -> Void) {
        fetchUser { user in
            guard let user else {
                completion(nil)
                return
            }
            self.fetchProfile(for: user) { profile in
                guard let profile else {
                    completion(nil)
                    return
                }
                self.fetchData(for: profile) { data in
                    completion(data)
                }
            }
        }
    }

    // GOOD: Sequential async/await
    func fetchDataGood() async -> Data? {
        guard let user = await fetchUserGood(),
              let profile = await fetchProfile(for: user),
              let data = await fetchData(for: profile) else {
            return nil
        }
        return data
    }

    private func fetchUser(completion: @escaping (User?) -> Void) {}
    private func fetchProfile(for user: User, completion: @escaping (Profile?) -> Void) {}
    private func fetchData(for profile: Profile, completion: @escaping (Data?) -> Void) {}
    private func fetchProfile(for user: User) async -> Profile? { nil }
    private func fetchData(for profile: Profile) async -> Data? { nil }
}

// MARK: - Supporting Types

struct User: Identifiable {
    let id: UUID
    var name: String
    var isActive: Bool
    var address: Address?
    var profile: Profile?
}

struct Address {
    var city: City?
    var street: String?
}

struct City {
    var name: String?
}

struct Profile {
    var address: Address?
}

struct Configuration {
    var apiKey: String
}
