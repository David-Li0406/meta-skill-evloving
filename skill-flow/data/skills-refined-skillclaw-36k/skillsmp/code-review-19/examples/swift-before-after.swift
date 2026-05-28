// MARK: - Swift Code Review: Before/After Examples
// This file demonstrates common refactoring patterns for Swift code review.

import SwiftUI

// MARK: - Example 1: State Management

// BEFORE: Using ObservableObject (iOS 16 and earlier pattern)
class OldViewModel: ObservableObject {
    @Published var items: [String] = []
    @Published var isLoading = false

    func loadItems() {
        isLoading = true
        // ... load items
        isLoading = false
    }
}

struct OldView: View {
    @StateObject private var viewModel = OldViewModel()

    var body: some View {
        List(viewModel.items, id: \.self) { item in
            Text(item)
        }
    }
}

// AFTER: Using @Observable (iOS 17+)
@Observable
@MainActor
class NewViewModel {
    var items: [String] = []
    var isLoading = false

    func loadItems() async {
        isLoading = true
        defer { isLoading = false }
        // ... load items asynchronously
    }
}

struct NewView: View {
    @State private var viewModel = NewViewModel()

    var body: some View {
        List(viewModel.items, id: \.self) { item in
            Text(item)
        }
    }
}

// MARK: - Example 2: Error Handling

// BEFORE: Force try and implicit error handling
func loadDataBefore() {
    let data = try! JSONDecoder().decode([String].self, from: Data())
    print(data)
}

// AFTER: Proper error handling with Result type
enum DataError: Error, LocalizedError {
    case decodingFailed
    case networkError(underlying: Error)

    var errorDescription: String? {
        switch self {
        case .decodingFailed:
            return "Failed to decode data"
        case .networkError(let error):
            return "Network error: \(error.localizedDescription)"
        }
    }
}

func loadDataAfter() async -> Result<[String], DataError> {
    do {
        let data = try JSONDecoder().decode([String].self, from: Data())
        return .success(data)
    } catch {
        return .failure(.decodingFailed)
    }
}

// MARK: - Example 3: Optional Handling

// BEFORE: Force unwrap and nested optionals
func processUserBefore(users: [User]) -> String {
    let user = users.first!
    let address = user.address!
    return address.city!
}

// AFTER: Safe optional handling
func processUserAfter(users: [User]) -> String? {
    guard let user = users.first,
          let address = user.address else {
        return nil
    }
    return address.city
}

// Alternative with optional chaining
func processUserAfterChained(users: [User]) -> String? {
    users.first?.address?.city
}

// MARK: - Example 4: Collection Operations

// BEFORE: Manual iteration
func findActiveUsersBefore(users: [User]) -> [User] {
    var activeUsers: [User] = []
    for user in users {
        if user.isActive {
            activeUsers.append(user)
        }
    }
    return activeUsers
}

// AFTER: Functional approach
func findActiveUsersAfter(users: [User]) -> [User] {
    users.filter(\.isActive)
}

// MARK: - Example 5: View Composition

// BEFORE: Monolithic view
struct MonolithicView: View {
    @State private var username = ""
    @State private var password = ""
    @State private var isLoading = false

    var body: some View {
        VStack {
            TextField("Username", text: $username)
                .textFieldStyle(.roundedBorder)
                .textInputAutocapitalization(.never)
                .padding()

            SecureField("Password", text: $password)
                .textFieldStyle(.roundedBorder)
                .padding()

            Button(action: login) {
                if isLoading {
                    ProgressView()
                } else {
                    Text("Login")
                }
            }
            .disabled(username.isEmpty || password.isEmpty)
            .padding()
        }
    }

    private func login() {
        // login logic
    }
}

// AFTER: Composed smaller views
struct UsernameField: View {
    @Binding var username: String

    var body: some View {
        TextField("Username", text: $username)
            .textFieldStyle(.roundedBorder)
            .textInputAutocapitalization(.never)
    }
}

struct PasswordField: View {
    @Binding var password: String

    var body: some View {
        SecureField("Password", text: $password)
            .textFieldStyle(.roundedBorder)
    }
}

struct LoadingButton: View {
    let title: String
    let isLoading: Bool
    let isDisabled: Bool
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            if isLoading {
                ProgressView()
            } else {
                Text(title)
            }
        }
        .disabled(isDisabled)
    }
}

struct ComposedLoginView: View {
    @State private var username = ""
    @State private var password = ""
    @State private var isLoading = false

    var body: some View {
        VStack(spacing: 16) {
            UsernameField(username: $username)
            PasswordField(password: $password)
            LoadingButton(
                title: "Login",
                isLoading: isLoading,
                isDisabled: username.isEmpty || password.isEmpty,
                action: login
            )
        }
        .padding()
    }

    private func login() {
        // login logic
    }
}

// MARK: - Supporting Types

struct User: Identifiable {
    let id: UUID
    var name: String
    var isActive: Bool
    var address: Address?
}

struct Address {
    var city: String?
    var street: String?
}
