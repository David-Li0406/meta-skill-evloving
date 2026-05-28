// SwiftUI Components Examples (iOS 17+)
// Demonstrates @Observable, NavigationStack, custom modifiers, and modern patterns

import SwiftUI
import Observation

// MARK: - Observable State Management

@Observable
class CounterState {
    var count = 0
    var isLoading = false

    var doubleCount: Int { count * 2 }

    func increment() {
        count += 1
    }

    func decrement() {
        guard count > 0 else { return }
        count -= 1
    }
}

struct CounterView: View {
    @State private var state = CounterState()

    var body: some View {
        VStack(spacing: 20) {
            Text("Count: \(state.count)")
                .font(.largeTitle)
                .fontWeight(.bold)

            Text("Double: \(state.doubleCount)")
                .font(.title2)
                .foregroundStyle(.secondary)

            HStack(spacing: 16) {
                Button("−") {
                    state.decrement()
                }
                .buttonStyle(CircleButtonStyle(color: .red))

                Button("+") {
                    state.increment()
                }
                .buttonStyle(CircleButtonStyle(color: .green))
            }
        }
        .padding()
    }
}

// MARK: - Custom Button Style

struct CircleButtonStyle: ButtonStyle {
    let color: Color

    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .font(.title)
            .fontWeight(.bold)
            .frame(width: 60, height: 60)
            .background(color)
            .foregroundStyle(.white)
            .clipShape(Circle())
            .scaleEffect(configuration.isPressed ? 0.9 : 1.0)
            .animation(.spring(duration: 0.2), value: configuration.isPressed)
    }
}

// MARK: - Custom View Modifier

struct CardModifier: ViewModifier {
    var padding: CGFloat = 16
    var cornerRadius: CGFloat = 12

    func body(content: Content) -> some View {
        content
            .padding(padding)
            .background(.background)
            .clipShape(RoundedRectangle(cornerRadius: cornerRadius))
            .shadow(color: .black.opacity(0.1), radius: 4, y: 2)
    }
}

extension View {
    func cardStyle(padding: CGFloat = 16, cornerRadius: CGFloat = 12) -> some View {
        modifier(CardModifier(padding: padding, cornerRadius: cornerRadius))
    }
}

// MARK: - Navigation with Router

enum Destination: Hashable {
    case detail(id: Int)
    case settings
    case profile
}

@Observable
class Router {
    var path = NavigationPath()

    func navigate(to destination: Destination) {
        path.append(destination)
    }

    func pop() {
        guard !path.isEmpty else { return }
        path.removeLast()
    }

    func popToRoot() {
        path.removeLast(path.count)
    }
}

struct NavigationExample: View {
    @State private var router = Router()

    var body: some View {
        NavigationStack(path: $router.path) {
            List {
                Section("Items") {
                    ForEach(1...5, id: \.self) { id in
                        Button("Item \(id)") {
                            router.navigate(to: .detail(id: id))
                        }
                    }
                }

                Section("Other") {
                    Button("Settings") {
                        router.navigate(to: .settings)
                    }

                    Button("Profile") {
                        router.navigate(to: .profile)
                    }
                }
            }
            .navigationTitle("Home")
            .navigationDestination(for: Destination.self) { destination in
                switch destination {
                case .detail(let id):
                    DetailView(id: id)
                case .settings:
                    SettingsView()
                case .profile:
                    ProfileView()
                }
            }
        }
        .environment(router)
    }
}

struct DetailView: View {
    let id: Int
    @Environment(Router.self) private var router

    var body: some View {
        VStack(spacing: 20) {
            Text("Detail View")
                .font(.title)

            Text("Item ID: \(id)")
                .font(.headline)

            Button("Go to Settings") {
                router.navigate(to: .settings)
            }
            .buttonStyle(.borderedProminent)

            Button("Back to Root") {
                router.popToRoot()
            }
            .buttonStyle(.bordered)
        }
        .navigationTitle("Detail")
    }
}

struct SettingsView: View {
    var body: some View {
        List {
            Text("Settings content here")
        }
        .navigationTitle("Settings")
    }
}

struct ProfileView: View {
    var body: some View {
        List {
            Text("Profile content here")
        }
        .navigationTitle("Profile")
    }
}

// MARK: - List with Swipe Actions

struct Item: Identifiable {
    let id = UUID()
    var name: String
    var isArchived = false
}

@Observable
class ItemListState {
    var items: [Item] = [
        Item(name: "First Item"),
        Item(name: "Second Item"),
        Item(name: "Third Item")
    ]

    func delete(_ item: Item) {
        items.removeAll { $0.id == item.id }
    }

    func archive(_ item: Item) {
        if let index = items.firstIndex(where: { $0.id == item.id }) {
            items[index].isArchived = true
        }
    }
}

struct SwipeActionsExample: View {
    @State private var state = ItemListState()

    var body: some View {
        List {
            ForEach(state.items) { item in
                ItemRow(item: item)
                    .swipeActions(edge: .trailing, allowsFullSwipe: true) {
                        Button(role: .destructive) {
                            state.delete(item)
                        } label: {
                            Label("Delete", systemImage: "trash")
                        }
                    }
                    .swipeActions(edge: .leading) {
                        Button {
                            state.archive(item)
                        } label: {
                            Label("Archive", systemImage: "archivebox")
                        }
                        .tint(.orange)
                    }
            }
        }
        .navigationTitle("Items")
    }
}

struct ItemRow: View {
    let item: Item

    var body: some View {
        HStack {
            Text(item.name)
            Spacer()
            if item.isArchived {
                Image(systemName: "archivebox.fill")
                    .foregroundStyle(.orange)
            }
        }
    }
}

// MARK: - Async Loading

@Observable
class AsyncLoadingState {
    var data: [String] = []
    var isLoading = false
    var error: Error?

    @MainActor
    func load() async {
        isLoading = true
        defer { isLoading = false }

        do {
            // Simulate network delay
            try await Task.sleep(for: .seconds(1))
            data = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"]
        } catch {
            self.error = error
        }
    }
}

struct AsyncLoadingExample: View {
    @State private var state = AsyncLoadingState()

    var body: some View {
        List(state.data, id: \.self) { item in
            Text(item)
        }
        .overlay {
            if state.isLoading {
                ProgressView()
            }
        }
        .overlay {
            if state.data.isEmpty && !state.isLoading {
                ContentUnavailableView(
                    "No Data",
                    systemImage: "doc.text",
                    description: Text("Pull to refresh")
                )
            }
        }
        .refreshable {
            await state.load()
        }
        .task {
            await state.load()
        }
        .navigationTitle("Async Loading")
    }
}

// MARK: - Form with Bindable

@Observable
class FormState {
    var name = ""
    var email = ""
    var bio = ""
    var receiveNotifications = true

    var isValid: Bool {
        !name.isEmpty && email.contains("@")
    }
}

struct FormExample: View {
    @Bindable var state: FormState
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        Form {
            Section("Personal Info") {
                TextField("Name", text: $state.name)
                TextField("Email", text: $state.email)
                    .textContentType(.emailAddress)
                    .keyboardType(.emailAddress)
                    .autocapitalization(.none)
            }

            Section("About") {
                TextEditor(text: $state.bio)
                    .frame(minHeight: 100)
            }

            Section("Preferences") {
                Toggle("Receive Notifications", isOn: $state.receiveNotifications)
            }
        }
        .navigationTitle("Edit Profile")
        .toolbar {
            ToolbarItem(placement: .confirmationAction) {
                Button("Save") {
                    dismiss()
                }
                .disabled(!state.isValid)
            }

            ToolbarItem(placement: .cancellationAction) {
                Button("Cancel") {
                    dismiss()
                }
            }
        }
    }
}

// MARK: - Preview

#Preview("Counter") {
    CounterView()
}

#Preview("Navigation") {
    NavigationExample()
}

#Preview("Swipe Actions") {
    NavigationStack {
        SwipeActionsExample()
    }
}

#Preview("Async Loading") {
    NavigationStack {
        AsyncLoadingExample()
    }
}

#Preview("Form") {
    NavigationStack {
        FormExample(state: FormState())
    }
}
