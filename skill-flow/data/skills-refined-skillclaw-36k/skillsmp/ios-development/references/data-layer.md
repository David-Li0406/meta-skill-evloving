# Data Layer Reference

Data persistence patterns for iOS 17+ with SwiftData and Core Data.

## SwiftData (Recommended for iOS 17+)

### Model Definition

```swift
import SwiftData

@Model
class Item {
    var name: String
    var createdAt: Date
    var isCompleted: Bool

    // Relationships
    @Relationship(deleteRule: .cascade)
    var tasks: [Task] = []

    // Transient (not persisted)
    @Transient
    var isEditing = false

    init(name: String) {
        self.name = name
        self.createdAt = .now
        self.isCompleted = false
    }
}

@Model
class Task {
    var title: String
    var dueDate: Date?

    @Relationship(inverse: \Item.tasks)
    var item: Item?

    init(title: String) {
        self.title = title
    }
}
```

### Model Container Setup

```swift
@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        .modelContainer(for: [Item.self, Task.self])
    }
}

// Custom configuration
@main
struct MyApp: App {
    let container: ModelContainer

    init() {
        let schema = Schema([Item.self, Task.self])
        let config = ModelConfiguration(
            schema: schema,
            isStoredInMemoryOnly: false,
            cloudKitDatabase: .automatic
        )

        do {
            container = try ModelContainer(for: schema, configurations: config)
        } catch {
            fatalError("Failed to configure SwiftData: \(error)")
        }
    }

    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        .modelContainer(container)
    }
}
```

### Query Macro

```swift
struct ItemListView: View {
    @Query(sort: \Item.createdAt, order: .reverse)
    private var items: [Item]

    var body: some View {
        List(items) { item in
            ItemRow(item: item)
        }
    }
}

// With filter
struct ActiveItemsView: View {
    @Query(
        filter: #Predicate<Item> { !$0.isCompleted },
        sort: \Item.createdAt
    )
    private var activeItems: [Item]

    var body: some View {
        List(activeItems) { item in
            ItemRow(item: item)
        }
    }
}

// Dynamic filter
struct SearchableItemsView: View {
    @State private var searchText = ""

    var body: some View {
        ItemList(searchText: searchText)
            .searchable(text: $searchText)
    }
}

struct ItemList: View {
    @Query private var items: [Item]

    init(searchText: String) {
        let predicate = #Predicate<Item> { item in
            searchText.isEmpty || item.name.localizedStandardContains(searchText)
        }
        _items = Query(filter: predicate, sort: \Item.createdAt)
    }

    var body: some View {
        List(items) { item in
            ItemRow(item: item)
        }
    }
}
```

### CRUD Operations

```swift
struct ItemDetailView: View {
    @Environment(\.modelContext) private var modelContext
    @Bindable var item: Item

    var body: some View {
        Form {
            TextField("Name", text: $item.name)
            Toggle("Completed", isOn: $item.isCompleted)
        }
        .toolbar {
            ToolbarItem(placement: .destructiveAction) {
                Button("Delete", role: .destructive) {
                    modelContext.delete(item)
                }
            }
        }
    }
}

// Create
func createItem(name: String, context: ModelContext) {
    let item = Item(name: name)
    context.insert(item)
    // Auto-save is enabled by default
}

// Delete
func deleteItems(at offsets: IndexSet, from items: [Item], context: ModelContext) {
    for index in offsets {
        context.delete(items[index])
    }
}

// Batch operations
func markAllCompleted(items: [Item]) {
    for item in items {
        item.isCompleted = true
    }
    // Changes are auto-saved
}
```

### Background Operations

```swift
actor DataManager {
    private let container: ModelContainer

    init(container: ModelContainer) {
        self.container = container
    }

    func importItems(_ data: [ImportData]) async throws {
        let context = ModelContext(container)
        context.autosaveEnabled = false

        for item in data {
            let newItem = Item(name: item.name)
            context.insert(newItem)
        }

        try context.save()
    }

    func fetchItemCount() async throws -> Int {
        let context = ModelContext(container)
        let descriptor = FetchDescriptor<Item>()
        return try context.fetchCount(descriptor)
    }
}
```

## Core Data (Legacy Support)

### Model Setup

```swift
// Create .xcdatamodeld in Xcode
// Or define programmatically:

class CoreDataStack {
    static let shared = CoreDataStack()

    lazy var persistentContainer: NSPersistentContainer = {
        let container = NSPersistentContainer(name: "MyApp")
        container.loadPersistentStores { _, error in
            if let error {
                fatalError("Failed to load Core Data: \(error)")
            }
        }
        container.viewContext.automaticallyMergesChangesFromParent = true
        return container
    }()

    var viewContext: NSManagedObjectContext {
        persistentContainer.viewContext
    }

    func newBackgroundContext() -> NSManagedObjectContext {
        persistentContainer.newBackgroundContext()
    }
}
```

### Fetch Request Wrapper

```swift
struct CoreDataItemListView: View {
    @FetchRequest(
        sortDescriptors: [SortDescriptor(\.createdAt, order: .reverse)],
        predicate: NSPredicate(format: "isCompleted == NO")
    )
    private var items: FetchedResults<CDItem>

    var body: some View {
        List(items) { item in
            Text(item.name ?? "")
        }
    }
}
```

## UserDefaults

### Property Wrapper

```swift
@propertyWrapper
struct UserDefault<T> {
    let key: String
    let defaultValue: T
    let container: UserDefaults

    init(key: String, defaultValue: T, container: UserDefaults = .standard) {
        self.key = key
        self.defaultValue = defaultValue
        self.container = container
    }

    var wrappedValue: T {
        get { container.object(forKey: key) as? T ?? defaultValue }
        set { container.set(newValue, forKey: key) }
    }
}

// Usage
enum Settings {
    @UserDefault(key: "hasSeenOnboarding", defaultValue: false)
    static var hasSeenOnboarding: Bool

    @UserDefault(key: "preferredTheme", defaultValue: "system")
    static var preferredTheme: String
}
```

### AppStorage

```swift
struct SettingsView: View {
    @AppStorage("notificationsEnabled") private var notificationsEnabled = true
    @AppStorage("fontSize") private var fontSize = 14.0

    var body: some View {
        Form {
            Toggle("Notifications", isOn: $notificationsEnabled)
            Slider(value: $fontSize, in: 10...24) {
                Text("Font Size: \(Int(fontSize))")
            }
        }
    }
}
```

## Keychain

### Keychain Wrapper

```swift
actor KeychainManager {
    enum KeychainError: Error {
        case duplicateItem
        case itemNotFound
        case unexpectedStatus(OSStatus)
    }

    func save(_ data: Data, forKey key: String) throws {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: key,
            kSecValueData as String: data,
            kSecAttrAccessible as String: kSecAttrAccessibleWhenUnlockedThisDeviceOnly
        ]

        let status = SecItemAdd(query as CFDictionary, nil)

        if status == errSecDuplicateItem {
            try update(data, forKey: key)
        } else if status != errSecSuccess {
            throw KeychainError.unexpectedStatus(status)
        }
    }

    func load(forKey key: String) throws -> Data {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: key,
            kSecReturnData as String: true
        ]

        var result: AnyObject?
        let status = SecItemCopyMatching(query as CFDictionary, &result)

        guard status == errSecSuccess, let data = result as? Data else {
            throw KeychainError.itemNotFound
        }

        return data
    }

    func delete(forKey key: String) throws {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: key
        ]

        let status = SecItemDelete(query as CFDictionary)

        guard status == errSecSuccess || status == errSecItemNotFound else {
            throw KeychainError.unexpectedStatus(status)
        }
    }

    private func update(_ data: Data, forKey key: String) throws {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: key
        ]

        let attributes: [String: Any] = [
            kSecValueData as String: data
        ]

        let status = SecItemUpdate(query as CFDictionary, attributes as CFDictionary)

        guard status == errSecSuccess else {
            throw KeychainError.unexpectedStatus(status)
        }
    }
}

// Token storage
extension KeychainManager {
    func saveToken(_ token: String) throws {
        guard let data = token.data(using: .utf8) else { return }
        try save(data, forKey: "authToken")
    }

    func loadToken() throws -> String? {
        let data = try load(forKey: "authToken")
        return String(data: data, encoding: .utf8)
    }
}
```

## Best Practices

### SwiftData

1. **Use @Model for entities** - Automatic persistence
2. **@Query for reactive fetching** - Auto-updates UI
3. **Background contexts for heavy operations** - Prevent UI blocking
4. **CloudKit sync** - Use `cloudKitDatabase: .automatic`

### Core Data

1. **Batch operations** - Use `NSBatchInsertRequest` for large imports
2. **Background contexts** - Use `performBackgroundTask` for heavy work
3. **Fetch limits** - Always set `fetchLimit` and `fetchBatchSize`

### Security

1. **Keychain for secrets** - Never store tokens in UserDefaults
2. **Data protection** - Use appropriate `kSecAttrAccessible` level
3. **Encryption** - Consider additional encryption for sensitive data
