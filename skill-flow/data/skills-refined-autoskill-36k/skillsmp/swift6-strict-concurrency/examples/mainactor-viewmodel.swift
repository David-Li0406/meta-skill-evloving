// MARK: - @MainActor ViewModel Pattern
// iOS 17+ での @Observable + @MainActor ViewModel パターン

import SwiftUI
import Observation

// MARK: - 基本的な ViewModel パターン

/// @MainActor で ViewModel 全体を MainActor に分離
/// UI バインディングが安全に行える
@Observable
@MainActor
class ItemListViewModel {
    // MARK: - State

    var items: [Item] = []
    var isLoading = false
    var errorMessage: String?
    var searchQuery = ""

    // MARK: - Filtered Items (計算プロパティ)

    var filteredItems: [Item] {
        if searchQuery.isEmpty {
            return items
        }
        return items.filter { $0.name.localizedCaseInsensitiveContains(searchQuery) }
    }

    // MARK: - Dependencies

    private let repository: ItemRepository

    // MARK: - Initialization

    init(repository: ItemRepository = ItemRepository()) {
        self.repository = repository
    }

    // MARK: - Actions

    func loadItems() async {
        isLoading = true
        errorMessage = nil

        do {
            items = try await repository.fetchItems()
        } catch {
            errorMessage = error.localizedDescription
        }

        isLoading = false
    }

    func deleteItem(_ item: Item) async {
        do {
            try await repository.delete(item)
            items.removeAll { $0.id == item.id }
        } catch {
            errorMessage = "削除に失敗しました: \(error.localizedDescription)"
        }
    }

    func refresh() async {
        await loadItems()
    }
}

// MARK: - モデルとリポジトリ

struct Item: Identifiable, Sendable {
    let id: UUID
    var name: String
    var isCompleted: Bool
}

/// Repository も @MainActor にする必要はない（バックグラウンドで動作可能）
actor ItemRepository {
    func fetchItems() async throws -> [Item] {
        // ネットワークリクエストをシミュレート
        try await Task.sleep(for: .seconds(1))
        return [
            Item(id: UUID(), name: "Item 1", isCompleted: false),
            Item(id: UUID(), name: "Item 2", isCompleted: true),
            Item(id: UUID(), name: "Item 3", isCompleted: false),
        ]
    }

    func delete(_ item: Item) async throws {
        // 削除処理をシミュレート
        try await Task.sleep(for: .milliseconds(500))
    }
}

// MARK: - SwiftUI View

struct ItemListView: View {
    @State private var viewModel = ItemListViewModel()

    var body: some View {
        NavigationStack {
            Group {
                if viewModel.isLoading {
                    ProgressView("読み込み中...")
                } else if let error = viewModel.errorMessage {
                    ContentUnavailableView(
                        "エラー",
                        systemImage: "exclamationmark.triangle",
                        description: Text(error)
                    )
                } else {
                    itemList
                }
            }
            .navigationTitle("アイテム")
            .searchable(text: $viewModel.searchQuery)
            .refreshable {
                await viewModel.refresh()
            }
            .task {
                await viewModel.loadItems()
            }
        }
    }

    private var itemList: some View {
        List {
            ForEach(viewModel.filteredItems) { item in
                HStack {
                    Image(systemName: item.isCompleted ? "checkmark.circle.fill" : "circle")
                        .foregroundStyle(item.isCompleted ? .green : .secondary)
                    Text(item.name)
                }
            }
            .onDelete { indexSet in
                Task {
                    for index in indexSet {
                        await viewModel.deleteItem(viewModel.filteredItems[index])
                    }
                }
            }
        }
    }
}

// MARK: - 複数の ViewModel を持つ場合

@Observable
@MainActor
class AppViewModel {
    var isAuthenticated = false
    var currentUser: User?

    func signIn(email: String, password: String) async {
        // 認証処理
        try? await Task.sleep(for: .seconds(1))
        currentUser = User(id: UUID(), email: email)
        isAuthenticated = true
    }

    func signOut() {
        currentUser = nil
        isAuthenticated = false
    }
}

struct User: Sendable {
    let id: UUID
    let email: String
}

// MARK: - nonisolated メソッドの活用

@Observable
@MainActor
class UserProfileViewModel {
    var profile: UserProfile?
    var isLoading = false

    /// nonisolated 計算プロパティ（Sendable なデータのみ返す）
    nonisolated var profileSummary: String? {
        // MainActor.assumeIsolated で安全にアクセス
        // ただし、これは同期的に呼ばれた場合のみ使用可能
        nil  // 実際の実装では適切に処理
    }

    func loadProfile(userId: UUID) async {
        isLoading = true
        defer { isLoading = false }

        // プロファイル読み込み処理
        try? await Task.sleep(for: .seconds(1))
        profile = UserProfile(id: userId, name: "User", bio: "Bio")
    }
}

struct UserProfile: Sendable {
    let id: UUID
    let name: String
    let bio: String
}
