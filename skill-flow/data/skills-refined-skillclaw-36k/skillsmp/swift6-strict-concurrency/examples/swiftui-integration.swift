// MARK: - SwiftUI Integration
// SwiftUI と Swift 6 Strict Concurrency の統合パターン

import SwiftUI
import Observation

// MARK: - 基本的な ViewModel パターン

@Observable
@MainActor
class ContentViewModel {
    var items: [ListItem] = []
    var selectedItem: ListItem?
    var isLoading = false
    var searchText = ""

    var filteredItems: [ListItem] {
        if searchText.isEmpty {
            return items
        }
        return items.filter { $0.title.localizedCaseInsensitiveContains(searchText) }
    }

    func loadItems() async {
        isLoading = true
        defer { isLoading = false }

        // API リクエストをシミュレート
        try? await Task.sleep(for: .seconds(1))
        items = [
            ListItem(id: UUID(), title: "Item 1", isCompleted: false),
            ListItem(id: UUID(), title: "Item 2", isCompleted: true),
            ListItem(id: UUID(), title: "Item 3", isCompleted: false),
        ]
    }

    func toggleCompletion(for item: ListItem) {
        guard let index = items.firstIndex(where: { $0.id == item.id }) else { return }
        items[index].isCompleted.toggle()
    }
}

struct ListItem: Identifiable, Sendable {
    let id: UUID
    var title: String
    var isCompleted: Bool
}

// MARK: - SwiftUI View

struct ContentListView: View {
    @State private var viewModel = ContentViewModel()

    var body: some View {
        NavigationStack {
            Group {
                if viewModel.isLoading {
                    ProgressView("読み込み中...")
                } else {
                    itemList
                }
            }
            .navigationTitle("アイテム")
            .searchable(text: $viewModel.searchText)
            .refreshable {
                await viewModel.loadItems()
            }
            .task {
                // View が表示されたときに自動実行
                // View が非表示になると自動キャンセル
                await viewModel.loadItems()
            }
        }
    }

    private var itemList: some View {
        List(viewModel.filteredItems) { item in
            HStack {
                Image(systemName: item.isCompleted ? "checkmark.circle.fill" : "circle")
                    .foregroundStyle(item.isCompleted ? .green : .secondary)
                    .onTapGesture {
                        viewModel.toggleCompletion(for: item)
                    }
                Text(item.title)
            }
        }
    }
}

// MARK: - 環境値での ViewModel 共有

@Observable
@MainActor
class AppState {
    var isAuthenticated = false
    var currentUser: AppUser?

    func signIn() async {
        try? await Task.sleep(for: .seconds(1))
        currentUser = AppUser(id: UUID(), name: "User")
        isAuthenticated = true
    }

    func signOut() {
        currentUser = nil
        isAuthenticated = false
    }
}

struct AppUser: Sendable {
    let id: UUID
    let name: String
}

// Environment Key
private struct AppStateKey: EnvironmentKey {
    @MainActor static let defaultValue = AppState()
}

extension EnvironmentValues {
    var appState: AppState {
        get { self[AppStateKey.self] }
        set { self[AppStateKey.self] = newValue }
    }
}

// 使用例
struct RootView: View {
    @State private var appState = AppState()

    var body: some View {
        Group {
            if appState.isAuthenticated {
                MainTabView()
            } else {
                LoginView()
            }
        }
        .environment(appState)
    }
}

struct LoginView: View {
    @Environment(AppState.self) private var appState

    var body: some View {
        Button("Sign In") {
            Task {
                await appState.signIn()
            }
        }
    }
}

struct MainTabView: View {
    @Environment(AppState.self) private var appState

    var body: some View {
        TabView {
            Text("Home")
                .tabItem { Label("Home", systemImage: "house") }

            Text("Profile")
                .tabItem { Label("Profile", systemImage: "person") }
        }
    }
}

// MARK: - Actor を使ったデータ管理

actor DataStore {
    private var items: [UUID: ListItem] = [:]

    func add(_ item: ListItem) {
        items[item.id] = item
    }

    func remove(_ id: UUID) {
        items.removeValue(forKey: id)
    }

    func getAll() -> [ListItem] {
        Array(items.values)
    }

    func get(_ id: UUID) -> ListItem? {
        items[id]
    }
}

@Observable
@MainActor
class DataStoreViewModel {
    private let store = DataStore()
    var items: [ListItem] = []

    func loadItems() async {
        items = await store.getAll()
    }

    func addItem(title: String) async {
        let item = ListItem(id: UUID(), title: title, isCompleted: false)
        await store.add(item)
        await loadItems()
    }

    func removeItem(_ id: UUID) async {
        await store.remove(id)
        await loadItems()
    }
}

// MARK: - AsyncSequence の購読

struct NotificationListenerView: View {
    @State private var notifications: [String] = []
    @State private var listenerTask: Task<Void, Never>?

    var body: some View {
        List(notifications, id: \.self) { notification in
            Text(notification)
        }
        .onAppear {
            startListening()
        }
        .onDisappear {
            listenerTask?.cancel()
        }
    }

    private func startListening() {
        listenerTask = Task {
            for await notification in NotificationCenter.default.notifications(named: .customNotification) {
                if let message = notification.userInfo?["message"] as? String {
                    notifications.append(message)
                }
            }
        }
    }
}

extension Notification.Name {
    static let customNotification = Notification.Name("customNotification")
}

// MARK: - @Bindable の使用（iOS 17+）

@Observable
@MainActor
class FormViewModel {
    var name = ""
    var email = ""
    var agreeToTerms = false

    var isValid: Bool {
        !name.isEmpty && !email.isEmpty && agreeToTerms
    }

    func submit() async {
        print("Submitting: \(name), \(email)")
        // 送信処理
    }
}

struct FormView: View {
    @State private var viewModel = FormViewModel()

    var body: some View {
        Form {
            // @Bindable を使って ViewModel のプロパティにバインド
            @Bindable var vm = viewModel

            TextField("Name", text: $vm.name)
            TextField("Email", text: $vm.email)
            Toggle("Agree to Terms", isOn: $vm.agreeToTerms)

            Button("Submit") {
                Task {
                    await viewModel.submit()
                }
            }
            .disabled(!viewModel.isValid)
        }
    }
}

// MARK: - Sheet/Navigation での ViewModel の受け渡し

struct DetailView: View {
    let item: ListItem
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        VStack {
            Text(item.title)
                .font(.largeTitle)

            Text(item.isCompleted ? "Completed" : "Not Completed")
                .foregroundStyle(item.isCompleted ? .green : .secondary)

            Button("Close") {
                dismiss()
            }
        }
        .padding()
    }
}

struct MasterDetailView: View {
    @State private var viewModel = ContentViewModel()
    @State private var selectedItem: ListItem?

    var body: some View {
        NavigationStack {
            List(viewModel.filteredItems) { item in
                Button(item.title) {
                    selectedItem = item
                }
            }
            .sheet(item: $selectedItem) { item in
                // ListItem は Sendable なので安全に渡せる
                DetailView(item: item)
            }
            .task {
                await viewModel.loadItems()
            }
        }
    }
}
