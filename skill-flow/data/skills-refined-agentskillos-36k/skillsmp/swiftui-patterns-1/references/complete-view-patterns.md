# SwiftUI Patterns — Complete View Patterns

> **Loading Trigger**: Load when building complex SwiftUI views or implementing advanced UI patterns.

---

## Complete List View Pattern

```swift
import SwiftUI

// MARK: - Generic List View with Pull-to-Refresh, Pagination, Empty State

struct GenericListView<Item: Identifiable, RowContent: View>: View {
    @ObservedObject var viewModel: ListViewModel<Item>
    let rowContent: (Item) -> RowContent

    init(
        viewModel: ListViewModel<Item>,
        @ViewBuilder rowContent: @escaping (Item) -> RowContent
    ) {
        self.viewModel = viewModel
        self.rowContent = rowContent
    }

    var body: some View {
        Group {
            switch viewModel.state {
            case .idle, .loading where viewModel.items.isEmpty:
                loadingView

            case .loading, .loaded:
                listContent

            case .error(let message) where viewModel.items.isEmpty:
                errorView(message: message)

            case .error:
                listContent // Show list with error banner
            }
        }
        .task {
            if viewModel.items.isEmpty {
                await viewModel.loadInitial()
            }
        }
    }

    private var loadingView: some View {
        VStack(spacing: 16) {
            ProgressView()
            Text("Loading...")
                .foregroundColor(.secondary)
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)
    }

    private func errorView(message: String) -> some View {
        VStack(spacing: 16) {
            Image(systemName: "exclamationmark.triangle")
                .font(.system(size: 48))
                .foregroundColor(.red)

            Text(message)
                .multilineTextAlignment(.center)
                .foregroundColor(.secondary)

            Button("Retry") {
                Task { await viewModel.loadInitial() }
            }
            .buttonStyle(.borderedProminent)
        }
        .padding()
        .frame(maxWidth: .infinity, maxHeight: .infinity)
    }

    private var listContent: some View {
        List {
            // Error banner if error occurred but have items
            if case .error(let message) = viewModel.state {
                errorBanner(message: message)
            }

            // Items
            ForEach(viewModel.items) { item in
                rowContent(item)
                    .onAppear {
                        // Pagination trigger
                        if item.id == viewModel.items.last?.id {
                            Task { await viewModel.loadMore() }
                        }
                    }
            }

            // Loading more indicator
            if viewModel.isLoadingMore {
                HStack {
                    Spacer()
                    ProgressView()
                    Spacer()
                }
                .listRowSeparator(.hidden)
            }
        }
        .listStyle(.plain)
        .refreshable {
            await viewModel.refresh()
        }
    }

    private func errorBanner(message: String) -> some View {
        HStack {
            Image(systemName: "exclamationmark.triangle.fill")
                .foregroundColor(.white)
            Text(message)
                .foregroundColor(.white)
            Spacer()
            Button("Retry") {
                Task { await viewModel.loadInitial() }
            }
            .foregroundColor(.white)
        }
        .padding()
        .background(Color.red)
        .cornerRadius(8)
        .listRowSeparator(.hidden)
        .listRowInsets(EdgeInsets(top: 8, leading: 16, bottom: 8, trailing: 16))
    }
}

// MARK: - List ViewModel

@MainActor
final class ListViewModel<Item: Identifiable>: ObservableObject {
    enum State: Equatable {
        case idle
        case loading
        case loaded
        case error(String)

        static func == (lhs: State, rhs: State) -> Bool {
            switch (lhs, rhs) {
            case (.idle, .idle), (.loading, .loading), (.loaded, .loaded):
                return true
            case (.error(let a), .error(let b)):
                return a == b
            default:
                return false
            }
        }
    }

    @Published private(set) var items: [Item] = []
    @Published private(set) var state: State = .idle
    @Published private(set) var isLoadingMore = false

    private let fetch: (Int, Int) async throws -> [Item]
    private var currentPage = 0
    private var hasMorePages = true
    private let pageSize = 20

    init(fetch: @escaping (Int, Int) async throws -> [Item]) {
        self.fetch = fetch
    }

    func loadInitial() async {
        state = .loading
        currentPage = 0

        do {
            let newItems = try await fetch(0, pageSize)
            items = newItems
            hasMorePages = newItems.count == pageSize
            state = .loaded
        } catch {
            state = .error(error.localizedDescription)
        }
    }

    func refresh() async {
        currentPage = 0

        do {
            let newItems = try await fetch(0, pageSize)
            items = newItems
            hasMorePages = newItems.count == pageSize
            state = .loaded
        } catch {
            state = .error(error.localizedDescription)
        }
    }

    func loadMore() async {
        guard !isLoadingMore, hasMorePages else { return }

        isLoadingMore = true
        let nextPage = currentPage + 1

        do {
            let newItems = try await fetch(nextPage, pageSize)
            items.append(contentsOf: newItems)
            currentPage = nextPage
            hasMorePages = newItems.count == pageSize
        } catch {
            // Silent failure for pagination
        }

        isLoadingMore = false
    }
}
```

---

## Form View Pattern

```swift
// MARK: - Complete Form with Validation

struct FormView: View {
    @StateObject private var viewModel = FormViewModel()
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        NavigationStack {
            Form {
                Section {
                    TextField("Name", text: $viewModel.name)
                        .textContentType(.name)

                    TextField("Email", text: $viewModel.email)
                        .textContentType(.emailAddress)
                        .keyboardType(.emailAddress)
                        .autocapitalization(.none)

                    SecureField("Password", text: $viewModel.password)
                        .textContentType(.newPassword)
                } header: {
                    Text("Account Information")
                } footer: {
                    if let error = viewModel.validationErrors.first {
                        Text(error)
                            .foregroundColor(.red)
                    }
                }

                Section {
                    Toggle("Receive updates", isOn: $viewModel.receiveUpdates)
                    Toggle("Marketing emails", isOn: $viewModel.marketingEmails)
                }
            }
            .navigationTitle("Create Account")
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Cancel") { dismiss() }
                }
                ToolbarItem(placement: .confirmationAction) {
                    Button("Save") {
                        Task { await viewModel.submit() }
                    }
                    .disabled(!viewModel.isValid || viewModel.isSubmitting)
                }
            }
            .alert("Error", isPresented: $viewModel.showError) {
                Button("OK") {}
            } message: {
                Text(viewModel.errorMessage ?? "Unknown error")
            }
            .onChange(of: viewModel.didSubmitSuccessfully) { _, success in
                if success { dismiss() }
            }
        }
    }
}

// MARK: - Form ViewModel

@MainActor
final class FormViewModel: ObservableObject {
    @Published var name = ""
    @Published var email = ""
    @Published var password = ""
    @Published var receiveUpdates = true
    @Published var marketingEmails = false

    @Published private(set) var isSubmitting = false
    @Published var showError = false
    @Published var errorMessage: String?
    @Published private(set) var didSubmitSuccessfully = false

    var isValid: Bool {
        validationErrors.isEmpty
    }

    var validationErrors: [String] {
        var errors: [String] = []

        if name.trimmingCharacters(in: .whitespaces).isEmpty {
            errors.append("Name is required")
        }

        if !email.contains("@") || !email.contains(".") {
            errors.append("Please enter a valid email")
        }

        if password.count < 8 {
            errors.append("Password must be at least 8 characters")
        }

        return errors
    }

    func submit() async {
        guard isValid else { return }

        isSubmitting = true
        defer { isSubmitting = false }

        do {
            try await createAccount()
            didSubmitSuccessfully = true
        } catch {
            errorMessage = error.localizedDescription
            showError = true
        }
    }

    private func createAccount() async throws {
        // API call
    }
}
```

---

## Search View Pattern

```swift
// MARK: - Debounced Search

struct SearchView: View {
    @StateObject private var viewModel = SearchViewModel()

    var body: some View {
        NavigationStack {
            List {
                if viewModel.isSearching {
                    HStack {
                        Spacer()
                        ProgressView()
                        Spacer()
                    }
                } else if viewModel.results.isEmpty && !viewModel.query.isEmpty {
                    ContentUnavailableView.search(text: viewModel.query)
                } else {
                    ForEach(viewModel.results) { result in
                        NavigationLink(value: result) {
                            SearchResultRow(result: result)
                        }
                    }
                }
            }
            .navigationTitle("Search")
            .searchable(
                text: $viewModel.query,
                placement: .navigationBarDrawer(displayMode: .always),
                prompt: "Search items..."
            )
            .navigationDestination(for: SearchResult.self) { result in
                DetailView(item: result)
            }
        }
    }
}

@MainActor
final class SearchViewModel: ObservableObject {
    @Published var query = ""
    @Published private(set) var results: [SearchResult] = []
    @Published private(set) var isSearching = false

    private var searchTask: Task<Void, Never>?

    init() {
        setupDebounce()
    }

    private func setupDebounce() {
        $query
            .removeDuplicates()
            .debounce(for: .milliseconds(300), scheduler: DispatchQueue.main)
            .sink { [weak self] query in
                self?.search(query: query)
            }
            .store(in: &cancellables)
    }

    private var cancellables = Set<AnyCancellable>()

    private func search(query: String) {
        searchTask?.cancel()

        guard !query.isEmpty else {
            results = []
            return
        }

        searchTask = Task {
            isSearching = true
            defer { isSearching = false }

            do {
                try await Task.sleep(for: .milliseconds(100)) // Debounce buffer
                try Task.checkCancellation()

                let newResults = try await performSearch(query: query)

                try Task.checkCancellation()
                results = newResults
            } catch is CancellationError {
                // Ignore cancellation
            } catch {
                // Handle error
            }
        }
    }

    private func performSearch(query: String) async throws -> [SearchResult] {
        // API call
        []
    }
}
```

---

## Modal Presentation Patterns

```swift
// MARK: - Complete Modal Flow

struct ModalFlowView: View {
    @State private var presentedItem: Item?
    @State private var showSettings = false
    @State private var showConfirmation = false
    @State private var confirmationAction: (() -> Void)?

    var body: some View {
        VStack {
            // Item-based sheet (recommended)
            Button("Show Item Detail") {
                presentedItem = Item(id: "1", name: "Test")
            }

            // Boolean-based sheet
            Button("Show Settings") {
                showSettings = true
            }

            // Confirmation dialog
            Button("Delete Item", role: .destructive) {
                confirmationAction = { deleteItem() }
                showConfirmation = true
            }
        }
        // Item sheet - item is guaranteed non-nil in closure
        .sheet(item: $presentedItem) { item in
            ItemDetailSheet(item: item) {
                presentedItem = nil // Dismiss
            }
        }
        // Boolean sheet
        .sheet(isPresented: $showSettings) {
            SettingsView()
        }
        // Confirmation dialog
        .confirmationDialog(
            "Delete Item?",
            isPresented: $showConfirmation,
            titleVisibility: .visible
        ) {
            Button("Delete", role: .destructive) {
                confirmationAction?()
            }
            Button("Cancel", role: .cancel) {}
        } message: {
            Text("This action cannot be undone.")
        }
    }

    private func deleteItem() {
        // Delete implementation
    }
}

// MARK: - Sheet with Environment Dismiss

struct ItemDetailSheet: View {
    let item: Item
    let onDismiss: () -> Void

    @Environment(\.dismiss) private var dismiss

    var body: some View {
        NavigationStack {
            VStack {
                Text(item.name)
            }
            .navigationTitle("Item Detail")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Done") {
                        onDismiss()
                        // or: dismiss()
                    }
                }
            }
        }
        .interactiveDismissDisabled() // Prevent swipe dismiss if needed
    }
}
```

---

## Animation Patterns

```swift
// MARK: - Animated State Transitions

struct AnimatedContentView: View {
    @State private var items: [Item] = []
    @State private var selectedId: String?

    var body: some View {
        VStack {
            // Animated list changes
            ForEach(items) { item in
                ItemRow(item: item, isSelected: item.id == selectedId)
                    .onTapGesture {
                        withAnimation(.spring(response: 0.3, dampingFraction: 0.7)) {
                            selectedId = item.id
                        }
                    }
            }
            .animation(.default, value: items) // Animate list changes

            // Phase animator for complex sequences
            PhaseAnimator([false, true]) { isHighlighted in
                Circle()
                    .fill(isHighlighted ? .blue : .gray)
                    .scaleEffect(isHighlighted ? 1.2 : 1.0)
            }

            // Keyframe animator
            KeyframeAnimator(
                initialValue: AnimationValues(),
                repeating: true
            ) { values in
                Circle()
                    .scaleEffect(values.scale)
                    .offset(y: values.yOffset)
            } keyframes: { _ in
                KeyframeTrack(\.scale) {
                    SpringKeyframe(1.2, duration: 0.3)
                    SpringKeyframe(1.0, duration: 0.3)
                }
                KeyframeTrack(\.yOffset) {
                    LinearKeyframe(-20, duration: 0.3)
                    LinearKeyframe(0, duration: 0.3)
                }
            }
        }
    }

    struct AnimationValues {
        var scale: CGFloat = 1.0
        var yOffset: CGFloat = 0
    }
}

// MARK: - Matched Geometry Effect

struct MatchedGeometryView: View {
    @Namespace private var namespace
    @State private var isExpanded = false

    var body: some View {
        VStack {
            if isExpanded {
                // Expanded state
                RoundedRectangle(cornerRadius: 20)
                    .fill(.blue)
                    .matchedGeometryEffect(id: "card", in: namespace)
                    .frame(width: 300, height: 400)
                    .onTapGesture {
                        withAnimation(.spring(response: 0.4, dampingFraction: 0.8)) {
                            isExpanded = false
                        }
                    }
            } else {
                // Collapsed state
                RoundedRectangle(cornerRadius: 10)
                    .fill(.blue)
                    .matchedGeometryEffect(id: "card", in: namespace)
                    .frame(width: 100, height: 100)
                    .onTapGesture {
                        withAnimation(.spring(response: 0.4, dampingFraction: 0.8)) {
                            isExpanded = true
                        }
                    }
            }
        }
    }
}
```
