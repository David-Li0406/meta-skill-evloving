// MVVM Pattern Example (iOS 17+)
// Complete implementation with Repository, ViewModel, and View

import SwiftUI
import Observation

// MARK: - Domain Models

struct User: Identifiable, Codable, Equatable {
    let id: Int
    var name: String
    var email: String
    var avatarURL: URL?
}

// MARK: - Repository Protocol

protocol UserRepositoryProtocol: Sendable {
    func fetchUsers() async throws -> [User]
    func fetchUser(id: Int) async throws -> User
    func createUser(_ user: User) async throws -> User
    func updateUser(_ user: User) async throws -> User
    func deleteUser(id: Int) async throws
}

// MARK: - Repository Implementation

actor UserRepository: UserRepositoryProtocol {
    private let apiClient: APIClientProtocol

    init(apiClient: APIClientProtocol) {
        self.apiClient = apiClient
    }

    func fetchUsers() async throws -> [User] {
        try await apiClient.request(endpoint: "/users")
    }

    func fetchUser(id: Int) async throws -> User {
        try await apiClient.request(endpoint: "/users/\(id)")
    }

    func createUser(_ user: User) async throws -> User {
        try await apiClient.request(
            endpoint: "/users",
            method: .post,
            body: user
        )
    }

    func updateUser(_ user: User) async throws -> User {
        try await apiClient.request(
            endpoint: "/users/\(user.id)",
            method: .put,
            body: user
        )
    }

    func deleteUser(id: Int) async throws {
        try await apiClient.requestVoid(
            endpoint: "/users/\(id)",
            method: .delete
        )
    }
}

// MARK: - API Client Protocol

protocol APIClientProtocol: Sendable {
    func request<T: Decodable>(endpoint: String) async throws -> T
    func request<T: Decodable, U: Encodable>(
        endpoint: String,
        method: HTTPMethod,
        body: U
    ) async throws -> T
    func requestVoid(endpoint: String, method: HTTPMethod) async throws
}

enum HTTPMethod: String {
    case get = "GET"
    case post = "POST"
    case put = "PUT"
    case delete = "DELETE"
}

// MARK: - ViewModel Errors

enum UserListError: LocalizedError, Equatable {
    case fetchFailed(String)
    case deleteFailed(String)
    case networkUnavailable

    var errorDescription: String? {
        switch self {
        case .fetchFailed(let message):
            return "Failed to load users: \(message)"
        case .deleteFailed(let message):
            return "Failed to delete user: \(message)"
        case .networkUnavailable:
            return "Network is unavailable"
        }
    }

    var recoverySuggestion: String? {
        "Please try again later."
    }
}

// MARK: - User List ViewModel

@Observable
@MainActor
class UserListViewModel {
    // MARK: - Published State
    private(set) var users: [User] = []
    private(set) var isLoading = false
    private(set) var error: UserListError?

    var hasError: Bool { error != nil }

    // MARK: - Dependencies
    private let repository: UserRepositoryProtocol

    // MARK: - Initialization
    init(repository: UserRepositoryProtocol) {
        self.repository = repository
    }

    // MARK: - Actions

    func loadUsers() async {
        isLoading = true
        error = nil
        defer { isLoading = false }

        do {
            users = try await repository.fetchUsers()
        } catch {
            self.error = .fetchFailed(error.localizedDescription)
        }
    }

    func deleteUser(_ user: User) async {
        do {
            try await repository.deleteUser(id: user.id)
            users.removeAll { $0.id == user.id }
        } catch {
            self.error = .deleteFailed(error.localizedDescription)
        }
    }

    func clearError() {
        error = nil
    }
}

// MARK: - User Detail ViewModel

@Observable
@MainActor
class UserDetailViewModel {
    // MARK: - State
    private(set) var user: User?
    private(set) var isLoading = false
    private(set) var error: Error?
    private(set) var isSaving = false

    // MARK: - Editable Fields
    var name: String = ""
    var email: String = ""

    var hasChanges: Bool {
        guard let user else { return false }
        return name != user.name || email != user.email
    }

    var isValid: Bool {
        !name.isEmpty && email.contains("@")
    }

    // MARK: - Dependencies
    private let userId: Int
    private let repository: UserRepositoryProtocol

    // MARK: - Initialization
    init(userId: Int, repository: UserRepositoryProtocol) {
        self.userId = userId
        self.repository = repository
    }

    // MARK: - Actions

    func loadUser() async {
        isLoading = true
        defer { isLoading = false }

        do {
            let user = try await repository.fetchUser(id: userId)
            self.user = user
            self.name = user.name
            self.email = user.email
        } catch {
            self.error = error
        }
    }

    func saveChanges() async -> Bool {
        guard let user, hasChanges, isValid else { return false }

        isSaving = true
        defer { isSaving = false }

        do {
            let updatedUser = User(
                id: user.id,
                name: name,
                email: email,
                avatarURL: user.avatarURL
            )
            self.user = try await repository.updateUser(updatedUser)
            return true
        } catch {
            self.error = error
            return false
        }
    }

    func discardChanges() {
        guard let user else { return }
        name = user.name
        email = user.email
    }
}

// MARK: - User List View

struct UserListView: View {
    @State private var viewModel: UserListViewModel

    init(repository: UserRepositoryProtocol) {
        _viewModel = State(initialValue: UserListViewModel(repository: repository))
    }

    var body: some View {
        Group {
            if viewModel.isLoading && viewModel.users.isEmpty {
                loadingView
            } else if viewModel.users.isEmpty {
                emptyView
            } else {
                userList
            }
        }
        .navigationTitle("Users")
        .refreshable {
            await viewModel.loadUsers()
        }
        .task {
            await viewModel.loadUsers()
        }
        .alert(
            "Error",
            isPresented: .init(
                get: { viewModel.hasError },
                set: { if !$0 { viewModel.clearError() } }
            )
        ) {
            Button("OK") {
                viewModel.clearError()
            }
        } message: {
            if let error = viewModel.error {
                Text(error.localizedDescription)
            }
        }
    }

    private var loadingView: some View {
        ProgressView("Loading users...")
    }

    private var emptyView: some View {
        ContentUnavailableView(
            "No Users",
            systemImage: "person.3",
            description: Text("Pull to refresh")
        )
    }

    private var userList: some View {
        List {
            ForEach(viewModel.users) { user in
                NavigationLink(value: user) {
                    UserRow(user: user)
                }
                .swipeActions(edge: .trailing, allowsFullSwipe: true) {
                    Button(role: .destructive) {
                        Task {
                            await viewModel.deleteUser(user)
                        }
                    } label: {
                        Label("Delete", systemImage: "trash")
                    }
                }
            }
        }
    }
}

// MARK: - User Row

struct UserRow: View {
    let user: User

    var body: some View {
        HStack(spacing: 12) {
            AsyncImage(url: user.avatarURL) { image in
                image
                    .resizable()
                    .aspectRatio(contentMode: .fill)
            } placeholder: {
                Image(systemName: "person.circle.fill")
                    .font(.largeTitle)
                    .foregroundStyle(.secondary)
            }
            .frame(width: 44, height: 44)
            .clipShape(Circle())

            VStack(alignment: .leading, spacing: 2) {
                Text(user.name)
                    .font(.headline)

                Text(user.email)
                    .font(.subheadline)
                    .foregroundStyle(.secondary)
            }
        }
        .padding(.vertical, 4)
    }
}

// MARK: - User Detail View

struct UserDetailView: View {
    @Bindable var viewModel: UserDetailViewModel
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        Form {
            if let user = viewModel.user {
                Section {
                    HStack {
                        Spacer()
                        AsyncImage(url: user.avatarURL) { image in
                            image
                                .resizable()
                                .aspectRatio(contentMode: .fill)
                        } placeholder: {
                            Image(systemName: "person.circle.fill")
                                .font(.system(size: 80))
                                .foregroundStyle(.secondary)
                        }
                        .frame(width: 100, height: 100)
                        .clipShape(Circle())
                        Spacer()
                    }
                }
                .listRowBackground(Color.clear)

                Section("Personal Information") {
                    TextField("Name", text: $viewModel.name)
                    TextField("Email", text: $viewModel.email)
                        .textContentType(.emailAddress)
                        .keyboardType(.emailAddress)
                        .autocapitalization(.none)
                }
            }
        }
        .navigationTitle("User Details")
        .navigationBarTitleDisplayMode(.inline)
        .overlay {
            if viewModel.isLoading {
                ProgressView()
            }
        }
        .toolbar {
            ToolbarItem(placement: .confirmationAction) {
                Button("Save") {
                    Task {
                        if await viewModel.saveChanges() {
                            dismiss()
                        }
                    }
                }
                .disabled(!viewModel.hasChanges || !viewModel.isValid || viewModel.isSaving)
            }

            ToolbarItem(placement: .cancellationAction) {
                Button("Cancel") {
                    if viewModel.hasChanges {
                        viewModel.discardChanges()
                    }
                    dismiss()
                }
            }
        }
        .task {
            await viewModel.loadUser()
        }
    }
}

// MARK: - Dependency Container

@Observable
class DependencyContainer {
    private lazy var apiClient: APIClientProtocol = MockAPIClient()

    lazy var userRepository: UserRepositoryProtocol = UserRepository(
        apiClient: apiClient
    )

    @MainActor
    func makeUserListViewModel() -> UserListViewModel {
        UserListViewModel(repository: userRepository)
    }

    @MainActor
    func makeUserDetailViewModel(userId: Int) -> UserDetailViewModel {
        UserDetailViewModel(userId: userId, repository: userRepository)
    }
}

// MARK: - Mock API Client (for Preview/Testing)

actor MockAPIClient: APIClientProtocol {
    private var mockUsers: [User] = [
        User(id: 1, name: "Alice Johnson", email: "alice@example.com"),
        User(id: 2, name: "Bob Smith", email: "bob@example.com"),
        User(id: 3, name: "Charlie Brown", email: "charlie@example.com")
    ]

    func request<T: Decodable>(endpoint: String) async throws -> T {
        try await Task.sleep(for: .milliseconds(500))

        if endpoint == "/users" {
            return mockUsers as! T
        }

        if endpoint.hasPrefix("/users/"), let id = Int(endpoint.split(separator: "/").last!) {
            if let user = mockUsers.first(where: { $0.id == id }) {
                return user as! T
            }
        }

        throw URLError(.badURL)
    }

    func request<T: Decodable, U: Encodable>(
        endpoint: String,
        method: HTTPMethod,
        body: U
    ) async throws -> T {
        try await Task.sleep(for: .milliseconds(500))

        if let user = body as? User {
            if method == .put {
                if let index = mockUsers.firstIndex(where: { $0.id == user.id }) {
                    mockUsers[index] = user
                    return user as! T
                }
            } else if method == .post {
                let newUser = User(id: mockUsers.count + 1, name: user.name, email: user.email)
                mockUsers.append(newUser)
                return newUser as! T
            }
        }

        throw URLError(.badURL)
    }

    func requestVoid(endpoint: String, method: HTTPMethod) async throws {
        try await Task.sleep(for: .milliseconds(500))

        if method == .delete, endpoint.hasPrefix("/users/"),
           let id = Int(endpoint.split(separator: "/").last!) {
            mockUsers.removeAll { $0.id == id }
            return
        }

        throw URLError(.badURL)
    }
}

// MARK: - Preview

#Preview("User List") {
    NavigationStack {
        UserListView(repository: UserRepository(apiClient: MockAPIClient()))
    }
}

#Preview("User Detail") {
    NavigationStack {
        UserDetailView(
            viewModel: UserDetailViewModel(
                userId: 1,
                repository: UserRepository(apiClient: MockAPIClient())
            )
        )
    }
}
