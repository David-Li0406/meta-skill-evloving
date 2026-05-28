# Complete Persistence Layer Reference

<!-- Loading Trigger: Load this reference when implementing Core Data stack setup, batch imports, background operations, CloudKit sync, complex migrations, or optimizing fetch performance for iOS/tvOS applications -->

## Modern Core Data Stack

```swift
import CoreData
import CloudKit

// MARK: - Persistence Controller

@MainActor
final class PersistenceController {

    // MARK: - Singleton

    static let shared = PersistenceController()

    // MARK: - Preview Support

    static var preview: PersistenceController = {
        let controller = PersistenceController(inMemory: true)

        // Add sample data for previews
        let context = controller.container.viewContext
        for i in 0..<10 {
            let item = Item(context: context)
            item.id = UUID()
            item.timestamp = Date()
            item.title = "Sample Item \(i)"
        }

        do {
            try context.save()
        } catch {
            fatalError("Preview data creation failed: \(error)")
        }

        return controller
    }()

    // MARK: - Container

    let container: NSPersistentContainer

    // MARK: - Computed Properties

    var viewContext: NSManagedObjectContext {
        container.viewContext
    }

    // MARK: - Initialization

    init(inMemory: Bool = false) {
        container = NSPersistentContainer(name: "DataModel")

        if inMemory {
            container.persistentStoreDescriptions.first?.url = URL(fileURLWithPath: "/dev/null")
        }

        // Configure persistent store description
        guard let description = container.persistentStoreDescriptions.first else {
            fatalError("No persistent store descriptions found")
        }

        // Enable lightweight migration
        description.shouldMigrateStoreAutomatically = true
        description.shouldInferMappingModelAutomatically = true

        // Enable persistent history tracking
        description.setOption(true as NSNumber, forKey: NSPersistentHistoryTrackingKey)
        description.setOption(true as NSNumber, forKey: NSPersistentStoreRemoteChangeNotificationPostOptionKey)

        // Load stores
        container.loadPersistentStores { storeDescription, error in
            if let error = error as NSError? {
                // Handle error appropriately in production
                Logger.coreData.error("Core Data store failed to load: \(error), \(error.userInfo)")
                fatalError("Core Data store failed to load: \(error)")
            }

            Logger.coreData.info("Core Data store loaded: \(storeDescription.url?.absoluteString ?? "unknown")")
        }

        // Configure view context
        configureViewContext()

        // Setup remote change notification handling
        setupRemoteChangeNotifications()
    }

    // MARK: - View Context Configuration

    private func configureViewContext() {
        viewContext.automaticallyMergesChangesFromParent = true
        viewContext.mergePolicy = NSMergeByPropertyObjectTrumpMergePolicy

        // Performance optimizations
        viewContext.undoManager = nil  // Disable if not needed
        viewContext.shouldDeleteInaccessibleFaults = true

        // Set name for debugging
        viewContext.name = "ViewContext"
    }

    // MARK: - Remote Change Notifications

    private func setupRemoteChangeNotifications() {
        NotificationCenter.default.addObserver(
            self,
            selector: #selector(handleRemoteChange),
            name: .NSPersistentStoreRemoteChange,
            object: container.persistentStoreCoordinator
        )
    }

    @objc private func handleRemoteChange(_ notification: Notification) {
        // Process persistent history changes
        Task {
            await processPersistentHistory()
        }
    }

    // MARK: - Background Context

    func newBackgroundContext() -> NSManagedObjectContext {
        let context = container.newBackgroundContext()
        context.mergePolicy = NSMergeByPropertyObjectTrumpMergePolicy
        context.undoManager = nil
        context.name = "BackgroundContext-\(UUID().uuidString.prefix(8))"
        return context
    }

    // MARK: - Perform Background Task

    func performBackgroundTask<T>(
        _ block: @escaping (NSManagedObjectContext) throws -> T
    ) async throws -> T {
        try await container.performBackgroundTask { context in
            context.mergePolicy = NSMergeByPropertyObjectTrumpMergePolicy
            return try block(context)
        }
    }

    // MARK: - Save Operations

    func save() {
        guard viewContext.hasChanges else { return }

        do {
            try viewContext.save()
            Logger.coreData.debug("View context saved successfully")
        } catch {
            Logger.coreData.error("Failed to save view context: \(error)")
            viewContext.rollback()
        }
    }

    func saveBackgroundContext(_ context: NSManagedObjectContext) throws {
        guard context.hasChanges else { return }

        try context.performAndWait {
            try context.save()
        }
    }

    // MARK: - Persistent History

    private var lastHistoryToken: NSPersistentHistoryToken?

    private func processPersistentHistory() async {
        let context = newBackgroundContext()

        await context.perform {
            do {
                let request = NSPersistentHistoryChangeRequest.fetchHistory(after: self.lastHistoryToken)

                guard let result = try context.execute(request) as? NSPersistentHistoryResult,
                      let transactions = result.result as? [NSPersistentHistoryTransaction] else {
                    return
                }

                for transaction in transactions {
                    self.viewContext.perform {
                        self.viewContext.mergeChanges(fromContextDidSave: transaction.objectIDNotification())
                    }
                }

                self.lastHistoryToken = transactions.last?.token
            } catch {
                Logger.coreData.error("Failed to process persistent history: \(error)")
            }
        }
    }
}

// MARK: - Logger Extension

import os.log

extension Logger {
    static let coreData = Logger(subsystem: Bundle.main.bundleIdentifier ?? "", category: "CoreData")
}
```

## CloudKit Integration

```swift
import CoreData
import CloudKit

// MARK: - CloudKit-Enabled Persistence Controller

final class CloudKitPersistenceController {

    static let shared = CloudKitPersistenceController()

    let container: NSPersistentCloudKitContainer

    var viewContext: NSManagedObjectContext {
        container.viewContext
    }

    // CloudKit sync status
    @Published private(set) var syncStatus: SyncStatus = .idle

    enum SyncStatus {
        case idle
        case syncing
        case synced
        case error(Error)
    }

    private init() {
        container = NSPersistentCloudKitContainer(name: "DataModel")

        // Configure for CloudKit
        guard let description = container.persistentStoreDescriptions.first else {
            fatalError("No store description")
        }

        // Enable CloudKit sync
        description.cloudKitContainerOptions = NSPersistentCloudKitContainerOptions(
            containerIdentifier: "iCloud.com.yourapp.container"
        )

        // Enable history tracking for CloudKit
        description.setOption(true as NSNumber, forKey: NSPersistentHistoryTrackingKey)
        description.setOption(true as NSNumber, forKey: NSPersistentStoreRemoteChangeNotificationPostOptionKey)

        container.loadPersistentStores { _, error in
            if let error = error {
                fatalError("CloudKit store failed: \(error)")
            }
        }

        // Configure view context
        viewContext.automaticallyMergesChangesFromParent = true
        viewContext.mergePolicy = NSMergeByPropertyObjectTrumpMergePolicy

        // Monitor CloudKit events
        setupCloudKitEventMonitoring()
    }

    // MARK: - CloudKit Event Monitoring

    private func setupCloudKitEventMonitoring() {
        NotificationCenter.default.addObserver(
            forName: NSPersistentCloudKitContainer.eventChangedNotification,
            object: container,
            queue: .main
        ) { [weak self] notification in
            guard let event = notification.userInfo?[NSPersistentCloudKitContainer.eventNotificationUserInfoKey]
                    as? NSPersistentCloudKitContainer.Event else {
                return
            }

            self?.handleCloudKitEvent(event)
        }
    }

    private func handleCloudKitEvent(_ event: NSPersistentCloudKitContainer.Event) {
        switch event.type {
        case .setup:
            Logger.coreData.info("CloudKit setup: \(event.succeeded ? "success" : "failed")")

        case .import:
            if event.succeeded {
                syncStatus = .synced
                Logger.coreData.info("CloudKit import completed")
            } else if let error = event.error {
                syncStatus = .error(error)
                Logger.coreData.error("CloudKit import failed: \(error)")
            }

        case .export:
            if event.succeeded {
                syncStatus = .synced
                Logger.coreData.info("CloudKit export completed")
            } else if let error = event.error {
                syncStatus = .error(error)
                Logger.coreData.error("CloudKit export failed: \(error)")
            }

        @unknown default:
            break
        }
    }

    // MARK: - Manual Sync Trigger

    func triggerSync() async throws {
        syncStatus = .syncing

        // Force a refresh from CloudKit
        try await container.viewContext.perform {
            try self.container.viewContext.setQueryGenerationFrom(.current)
        }
    }

    // MARK: - Sharing Support

    func share(
        _ object: NSManagedObject,
        to share: CKShare?,
        completion: @escaping (CKShare?, Error?) -> Void
    ) {
        container.share([object], to: share) { objectIDs, share, container, error in
            completion(share, error)
        }
    }

    func fetchParticipants(
        for share: CKShare,
        completion: @escaping ([CKShare.Participant]?, Error?) -> Void
    ) {
        let operation = CKFetchShareParticipantsOperation(userIdentityLookupInfos: [])
        operation.perShareParticipantResultBlock = { _, result in
            switch result {
            case .success(let participant):
                completion([participant], nil)
            case .failure(let error):
                completion(nil, error)
            }
        }
        CKContainer.default().add(operation)
    }
}
```

## Batch Operations

```swift
import CoreData

// MARK: - Batch Import Manager

final class BatchImportManager {

    private let persistenceController: PersistenceController

    init(persistenceController: PersistenceController = .shared) {
        self.persistenceController = persistenceController
    }

    // MARK: - Batch Import with Progress

    func importItems<T: Decodable>(
        _ items: [T],
        batchSize: Int = 500,
        transform: @escaping (T, NSManagedObjectContext) -> Void,
        progress: ((Double) -> Void)? = nil
    ) async throws {
        let totalCount = items.count
        var processedCount = 0

        try await persistenceController.performBackgroundTask { context in
            context.mergePolicy = NSMergeByPropertyObjectTrumpMergePolicy

            for (index, item) in items.enumerated() {
                transform(item, context)

                // Batch save to manage memory
                if (index + 1) % batchSize == 0 {
                    try context.save()
                    context.reset()

                    processedCount = index + 1
                    let percentage = Double(processedCount) / Double(totalCount)

                    await MainActor.run {
                        progress?(percentage)
                    }
                }
            }

            // Final save for remaining items
            if context.hasChanges {
                try context.save()
            }

            await MainActor.run {
                progress?(1.0)
            }
        }
    }

    // MARK: - Batch Update

    func batchUpdate<Entity: NSManagedObject>(
        _ entityType: Entity.Type,
        predicate: NSPredicate? = nil,
        propertiesToUpdate: [String: Any]
    ) async throws -> Int {
        try await persistenceController.performBackgroundTask { context in
            let request = NSBatchUpdateRequest(entityName: String(describing: entityType))
            request.predicate = predicate
            request.propertiesToUpdate = propertiesToUpdate
            request.resultType = .updatedObjectIDsResultType

            let result = try context.execute(request) as? NSBatchUpdateResult
            let objectIDs = result?.result as? [NSManagedObjectID] ?? []

            // Merge changes to view context
            NSManagedObjectContext.mergeChanges(
                fromRemoteContextSave: [NSUpdatedObjectsKey: objectIDs],
                into: [self.persistenceController.viewContext]
            )

            return objectIDs.count
        }
    }

    // MARK: - Batch Delete

    func batchDelete<Entity: NSManagedObject>(
        _ entityType: Entity.Type,
        predicate: NSPredicate? = nil
    ) async throws -> Int {
        try await persistenceController.performBackgroundTask { context in
            let fetchRequest = NSFetchRequest<NSFetchRequestResult>(
                entityName: String(describing: entityType)
            )
            fetchRequest.predicate = predicate

            let deleteRequest = NSBatchDeleteRequest(fetchRequest: fetchRequest)
            deleteRequest.resultType = .resultTypeObjectIDs

            let result = try context.execute(deleteRequest) as? NSBatchDeleteResult
            let objectIDs = result?.result as? [NSManagedObjectID] ?? []

            // Merge changes to view context
            NSManagedObjectContext.mergeChanges(
                fromRemoteContextSave: [NSDeletedObjectsKey: objectIDs],
                into: [self.persistenceController.viewContext]
            )

            return objectIDs.count
        }
    }

    // MARK: - Batch Insert (iOS 13+)

    func batchInsert(
        entityName: String,
        objects: [[String: Any]]
    ) async throws -> Int {
        try await persistenceController.performBackgroundTask { context in
            var insertedCount = 0

            let insertRequest = NSBatchInsertRequest(
                entityName: entityName,
                objects: objects
            )
            insertRequest.resultType = .objectIDs

            let result = try context.execute(insertRequest) as? NSBatchInsertResult
            let objectIDs = result?.result as? [NSManagedObjectID] ?? []
            insertedCount = objectIDs.count

            // Merge to view context
            NSManagedObjectContext.mergeChanges(
                fromRemoteContextSave: [NSInsertedObjectsKey: objectIDs],
                into: [self.persistenceController.viewContext]
            )

            return insertedCount
        }
    }
}
```

## Fetch Optimization

```swift
import CoreData
import SwiftUI

// MARK: - Optimized Fetch Request Builder

final class FetchRequestBuilder<Entity: NSManagedObject> {

    private var fetchRequest: NSFetchRequest<Entity>

    init() {
        self.fetchRequest = NSFetchRequest<Entity>(entityName: String(describing: Entity.self))
    }

    // MARK: - Predicate

    func `where`(_ predicate: NSPredicate) -> Self {
        fetchRequest.predicate = predicate
        return self
    }

    func `where`(_ format: String, _ args: CVarArg...) -> Self {
        fetchRequest.predicate = NSPredicate(format: format, arguments: getVaList(args))
        return self
    }

    // MARK: - Sorting

    func sorted(by keyPath: String, ascending: Bool = true) -> Self {
        var descriptors = fetchRequest.sortDescriptors ?? []
        descriptors.append(NSSortDescriptor(key: keyPath, ascending: ascending))
        fetchRequest.sortDescriptors = descriptors
        return self
    }

    func sorted<Value: Comparable>(by keyPath: KeyPath<Entity, Value>, ascending: Bool = true) -> Self {
        var descriptors = fetchRequest.sortDescriptors ?? []
        descriptors.append(NSSortDescriptor(keyPath: keyPath, ascending: ascending))
        fetchRequest.sortDescriptors = descriptors
        return self
    }

    // MARK: - Pagination

    func limit(_ limit: Int) -> Self {
        fetchRequest.fetchLimit = limit
        return self
    }

    func offset(_ offset: Int) -> Self {
        fetchRequest.fetchOffset = offset
        return self
    }

    // MARK: - Performance Optimization

    func batchSize(_ size: Int) -> Self {
        fetchRequest.fetchBatchSize = size
        return self
    }

    func prefetch(_ relationships: [String]) -> Self {
        fetchRequest.relationshipKeyPathsForPrefetching = relationships
        return self
    }

    func includesPropertyValues(_ include: Bool) -> Self {
        fetchRequest.includesPropertyValues = include
        return self
    }

    func includesSubentities(_ include: Bool) -> Self {
        fetchRequest.includesSubentities = include
        return self
    }

    func returnsObjectsAsFaults(_ faults: Bool) -> Self {
        fetchRequest.returnsObjectsAsFaults = faults
        return self
    }

    func propertiesToFetch(_ properties: [String]) -> Self {
        fetchRequest.propertiesToFetch = properties
        return self
    }

    // MARK: - Build

    func build() -> NSFetchRequest<Entity> {
        // Apply sensible defaults for common cases
        if fetchRequest.fetchBatchSize == 0 {
            fetchRequest.fetchBatchSize = 20
        }
        return fetchRequest
    }

    // MARK: - Execute

    func execute(in context: NSManagedObjectContext) throws -> [Entity] {
        try context.fetch(build())
    }

    func count(in context: NSManagedObjectContext) throws -> Int {
        try context.count(for: build())
    }
}

// MARK: - Usage Extension

extension NSManagedObject {
    static func query<T: NSManagedObject>() -> FetchRequestBuilder<T> where T == Self {
        FetchRequestBuilder<T>()
    }
}

// MARK: - Async Fetch

extension NSManagedObjectContext {

    func fetchAsync<T: NSManagedObject>(_ request: NSFetchRequest<T>) async throws -> [T] {
        try await perform {
            try self.fetch(request)
        }
    }

    func countAsync<T: NSManagedObject>(for request: NSFetchRequest<T>) async throws -> Int {
        try await perform {
            try self.count(for: request)
        }
    }
}
```

## Dynamic @FetchRequest Patterns

```swift
import SwiftUI
import CoreData

// MARK: - Configurable Fetch Request View

struct DynamicFetchView<Entity: NSManagedObject, Content: View>: View {

    @FetchRequest private var results: FetchedResults<Entity>
    private let content: ([Entity]) -> Content

    init(
        predicate: NSPredicate? = nil,
        sortDescriptors: [NSSortDescriptor] = [],
        animation: Animation? = .default,
        @ViewBuilder content: @escaping ([Entity]) -> Content
    ) {
        _results = FetchRequest(
            entity: Entity.entity(),
            sortDescriptors: sortDescriptors,
            predicate: predicate,
            animation: animation
        )
        self.content = content
    }

    var body: some View {
        content(Array(results))
    }
}

// MARK: - Search-Enabled List

struct SearchableEntityList<Entity: NSManagedObject>: View where Entity: Identifiable {

    @State private var searchText = ""
    private let searchKeyPath: String
    private let sortKeyPath: String

    init(searchKeyPath: String, sortKeyPath: String) {
        self.searchKeyPath = searchKeyPath
        self.sortKeyPath = sortKeyPath
    }

    var body: some View {
        DynamicFetchView<Entity, AnyView>(
            predicate: searchPredicate,
            sortDescriptors: [NSSortDescriptor(key: sortKeyPath, ascending: true)]
        ) { entities in
            AnyView(
                List(entities) { entity in
                    Text(String(describing: entity))
                }
                .searchable(text: $searchText)
            )
        }
    }

    private var searchPredicate: NSPredicate? {
        guard !searchText.isEmpty else { return nil }
        return NSPredicate(format: "%K CONTAINS[cd] %@", searchKeyPath, searchText)
    }
}

// MARK: - Section Fetch Request

struct SectionedFetchView<Entity: NSManagedObject, SectionKey: Hashable, Content: View>: View {

    @SectionedFetchRequest private var sections: SectionedFetchResults<SectionKey, Entity>
    private let content: (SectionedFetchResults<SectionKey, Entity>) -> Content

    init(
        sectionIdentifier: KeyPath<Entity, SectionKey>,
        sortDescriptors: [SortDescriptor<Entity>],
        predicate: NSPredicate? = nil,
        animation: Animation? = .default,
        @ViewBuilder content: @escaping (SectionedFetchResults<SectionKey, Entity>) -> Content
    ) {
        _sections = SectionedFetchRequest(
            sectionIdentifier: sectionIdentifier,
            sortDescriptors: sortDescriptors,
            predicate: predicate,
            animation: animation
        )
        self.content = content
    }

    var body: some View {
        content(sections)
    }
}

// MARK: - Pagination Support

@MainActor
final class PaginatedFetchController<Entity: NSManagedObject>: ObservableObject {

    @Published private(set) var items: [Entity] = []
    @Published private(set) var isLoading = false
    @Published private(set) var hasMore = true

    private let context: NSManagedObjectContext
    private let pageSize: Int
    private let predicate: NSPredicate?
    private let sortDescriptors: [NSSortDescriptor]
    private var currentOffset = 0

    init(
        context: NSManagedObjectContext,
        pageSize: Int = 20,
        predicate: NSPredicate? = nil,
        sortDescriptors: [NSSortDescriptor]
    ) {
        self.context = context
        self.pageSize = pageSize
        self.predicate = predicate
        self.sortDescriptors = sortDescriptors
    }

    func loadFirstPage() async {
        currentOffset = 0
        items = []
        hasMore = true
        await loadNextPage()
    }

    func loadNextPage() async {
        guard !isLoading, hasMore else { return }

        isLoading = true

        let request = NSFetchRequest<Entity>(entityName: String(describing: Entity.self))
        request.predicate = predicate
        request.sortDescriptors = sortDescriptors
        request.fetchLimit = pageSize
        request.fetchOffset = currentOffset
        request.fetchBatchSize = pageSize

        do {
            let results = try await context.fetchAsync(request)

            items.append(contentsOf: results)
            currentOffset += results.count
            hasMore = results.count == pageSize

        } catch {
            Logger.coreData.error("Pagination fetch failed: \(error)")
        }

        isLoading = false
    }
}
```

## Migration Strategies

```swift
import CoreData

// MARK: - Migration Manager

final class CoreDataMigrationManager {

    private let modelName: String
    private let bundle: Bundle

    init(modelName: String, bundle: Bundle = .main) {
        self.modelName = modelName
        self.bundle = bundle
    }

    // MARK: - Check Migration Needed

    func requiresMigration(at storeURL: URL) -> Bool {
        guard let metadata = try? NSPersistentStoreCoordinator.metadataForPersistentStore(
            ofType: NSSQLiteStoreType,
            at: storeURL
        ) else {
            return false
        }

        guard let currentModel = currentManagedObjectModel() else {
            return false
        }

        return !currentModel.isConfiguration(withName: nil, compatibleWithStoreMetadata: metadata)
    }

    // MARK: - Perform Migration

    func migrateStore(at storeURL: URL) throws {
        guard requiresMigration(at: storeURL) else {
            Logger.coreData.info("No migration required")
            return
        }

        let metadata = try NSPersistentStoreCoordinator.metadataForPersistentStore(
            ofType: NSSQLiteStoreType,
            at: storeURL
        )

        guard let sourceModel = NSManagedObjectModel.mergedModel(
            from: [bundle],
            forStoreMetadata: metadata
        ) else {
            throw MigrationError.sourceModelNotFound
        }

        guard let destinationModel = currentManagedObjectModel() else {
            throw MigrationError.destinationModelNotFound
        }

        // Try lightweight migration first
        if let mappingModel = NSMappingModel(
            from: [bundle],
            forSourceModel: sourceModel,
            destinationModel: destinationModel
        ) {
            try performMigration(
                from: storeURL,
                sourceModel: sourceModel,
                destinationModel: destinationModel,
                mappingModel: mappingModel
            )
        } else {
            // Attempt inferred mapping
            let inferredMapping = try NSMappingModel.inferredMappingModel(
                forSourceModel: sourceModel,
                destinationModel: destinationModel
            )

            try performMigration(
                from: storeURL,
                sourceModel: sourceModel,
                destinationModel: destinationModel,
                mappingModel: inferredMapping
            )
        }
    }

    private func performMigration(
        from sourceURL: URL,
        sourceModel: NSManagedObjectModel,
        destinationModel: NSManagedObjectModel,
        mappingModel: NSMappingModel
    ) throws {
        let manager = NSMigrationManager(
            sourceModel: sourceModel,
            destinationModel: destinationModel
        )

        let destinationURL = sourceURL.deletingLastPathComponent()
            .appendingPathComponent("migrated_\(modelName).sqlite")

        try manager.migrateStore(
            from: sourceURL,
            sourceType: NSSQLiteStoreType,
            options: nil,
            with: mappingModel,
            toDestinationURL: destinationURL,
            destinationType: NSSQLiteStoreType,
            destinationOptions: nil
        )

        // Replace original with migrated store
        let fileManager = FileManager.default

        // Backup original
        let backupURL = sourceURL.deletingLastPathComponent()
            .appendingPathComponent("backup_\(modelName).sqlite")
        try? fileManager.removeItem(at: backupURL)
        try fileManager.moveItem(at: sourceURL, to: backupURL)

        // Move migrated to original location
        try fileManager.moveItem(at: destinationURL, to: sourceURL)

        // Clean up WAL and SHM files
        let walURL = sourceURL.appendingPathExtension("wal")
        let shmURL = sourceURL.appendingPathExtension("shm")
        try? fileManager.removeItem(at: walURL)
        try? fileManager.removeItem(at: shmURL)

        Logger.coreData.info("Migration completed successfully")
    }

    private func currentManagedObjectModel() -> NSManagedObjectModel? {
        guard let modelURL = bundle.url(forResource: modelName, withExtension: "momd") else {
            return nil
        }
        return NSManagedObjectModel(contentsOf: modelURL)
    }

    // MARK: - Migration Error

    enum MigrationError: LocalizedError {
        case sourceModelNotFound
        case destinationModelNotFound
        case migrationFailed(Error)

        var errorDescription: String? {
            switch self {
            case .sourceModelNotFound:
                return "Could not find source model for migration"
            case .destinationModelNotFound:
                return "Could not find destination model for migration"
            case .migrationFailed(let error):
                return "Migration failed: \(error.localizedDescription)"
            }
        }
    }
}

// MARK: - Progressive Migration

final class ProgressiveMigrationManager {

    private let modelName: String
    private let bundle: Bundle

    init(modelName: String, bundle: Bundle = .main) {
        self.modelName = modelName
        self.bundle = bundle
    }

    /// Migrate through all intermediate versions
    func progressivelyMigrate(storeURL: URL) throws {
        let modelVersions = orderedModelVersions()

        guard let currentModelIndex = modelVersions.firstIndex(where: { model in
            guard let metadata = try? NSPersistentStoreCoordinator.metadataForPersistentStore(
                ofType: NSSQLiteStoreType,
                at: storeURL
            ) else { return false }
            return model.isConfiguration(withName: nil, compatibleWithStoreMetadata: metadata)
        }) else {
            throw MigrationError.sourceModelNotFound
        }

        // Already at latest version
        if currentModelIndex == modelVersions.count - 1 {
            Logger.coreData.info("Store is already at latest version")
            return
        }

        // Migrate step by step
        for i in currentModelIndex..<(modelVersions.count - 1) {
            let sourceModel = modelVersions[i]
            let destinationModel = modelVersions[i + 1]

            Logger.coreData.info("Migrating from version \(i) to \(i + 1)")

            let mappingModel = try NSMappingModel.inferredMappingModel(
                forSourceModel: sourceModel,
                destinationModel: destinationModel
            )

            let manager = NSMigrationManager(
                sourceModel: sourceModel,
                destinationModel: destinationModel
            )

            let tempURL = storeURL.deletingLastPathComponent()
                .appendingPathComponent("temp_migration_\(i).sqlite")

            try manager.migrateStore(
                from: storeURL,
                sourceType: NSSQLiteStoreType,
                options: nil,
                with: mappingModel,
                toDestinationURL: tempURL,
                destinationType: NSSQLiteStoreType,
                destinationOptions: nil
            )

            // Replace
            try FileManager.default.removeItem(at: storeURL)
            try FileManager.default.moveItem(at: tempURL, to: storeURL)
        }

        Logger.coreData.info("Progressive migration completed")
    }

    private func orderedModelVersions() -> [NSManagedObjectModel] {
        guard let modelURL = bundle.url(forResource: modelName, withExtension: "momd"),
              let modelBundle = Bundle(url: modelURL) else {
            return []
        }

        let versionURLs = modelBundle.urls(forResourcesWithExtension: "mom", subdirectory: nil) ?? []

        return versionURLs
            .compactMap { NSManagedObjectModel(contentsOf: $0) }
            .sorted { model1, model2 in
                // Sort by version identifier if available
                let v1 = model1.versionIdentifiers.first as? String ?? ""
                let v2 = model2.versionIdentifiers.first as? String ?? ""
                return v1 < v2
            }
    }

    enum MigrationError: LocalizedError {
        case sourceModelNotFound

        var errorDescription: String? {
            "Could not determine current model version"
        }
    }
}
```

## Testing Core Data

```swift
import XCTest
import CoreData
@testable import YourApp

// MARK: - Core Data Test Case Base

class CoreDataTestCase: XCTestCase {

    var persistenceController: PersistenceController!
    var context: NSManagedObjectContext!

    override func setUp() {
        super.setUp()
        persistenceController = PersistenceController(inMemory: true)
        context = persistenceController.viewContext
    }

    override func tearDown() {
        context = nil
        persistenceController = nil
        super.tearDown()
    }

    // MARK: - Helper Methods

    func createSampleUser(name: String = "Test User") -> User {
        let user = User(context: context)
        user.id = UUID()
        user.name = name
        user.createdAt = Date()
        return user
    }

    func saveContext() throws {
        try context.save()
    }
}

// MARK: - Model Tests

final class UserModelTests: CoreDataTestCase {

    func testUserCreation() throws {
        let user = createSampleUser(name: "John")

        XCTAssertNotNil(user.id)
        XCTAssertEqual(user.name, "John")
        XCTAssertNotNil(user.createdAt)

        try saveContext()

        // Fetch and verify
        let request = User.fetchRequest()
        let users = try context.fetch(request)

        XCTAssertEqual(users.count, 1)
        XCTAssertEqual(users.first?.name, "John")
    }

    func testUserDeletion() throws {
        let user = createSampleUser()
        try saveContext()

        context.delete(user)
        try saveContext()

        let request = User.fetchRequest()
        let users = try context.fetch(request)

        XCTAssertTrue(users.isEmpty)
    }

    func testUserUpdate() throws {
        let user = createSampleUser(name: "Original")
        try saveContext()

        user.name = "Updated"
        try saveContext()

        let request = User.fetchRequest()
        request.predicate = NSPredicate(format: "name == %@", "Updated")
        let users = try context.fetch(request)

        XCTAssertEqual(users.count, 1)
    }
}

// MARK: - Batch Operation Tests

final class BatchOperationTests: CoreDataTestCase {

    func testBatchImport() async throws {
        let importManager = BatchImportManager(persistenceController: persistenceController)

        let items = (0..<100).map { UserDTO(id: UUID(), name: "User \($0)") }

        try await importManager.importItems(items, batchSize: 20) { dto, context in
            let user = User(context: context)
            user.id = dto.id
            user.name = dto.name
            user.createdAt = Date()
        }

        let request = User.fetchRequest()
        let count = try context.count(for: request)

        XCTAssertEqual(count, 100)
    }

    func testBatchDelete() async throws {
        // Create test data
        for i in 0..<50 {
            let user = createSampleUser(name: "User \(i)")
            user.isActive = i < 25  // Half active, half inactive
        }
        try saveContext()

        let importManager = BatchImportManager(persistenceController: persistenceController)

        let deletedCount = try await importManager.batchDelete(
            User.self,
            predicate: NSPredicate(format: "isActive == NO")
        )

        XCTAssertEqual(deletedCount, 25)

        let remainingCount = try context.count(for: User.fetchRequest())
        XCTAssertEqual(remainingCount, 25)
    }
}

// MARK: - Fetch Request Builder Tests

final class FetchRequestBuilderTests: CoreDataTestCase {

    func testQueryBuilder() throws {
        // Create test data
        for i in 0..<10 {
            let user = createSampleUser(name: "User \(i)")
            user.age = Int16(20 + i)
        }
        try saveContext()

        let results = try User.query()
            .where(NSPredicate(format: "age >= %d", 25))
            .sorted(by: "age", ascending: false)
            .limit(3)
            .execute(in: context)

        XCTAssertEqual(results.count, 3)
        XCTAssertEqual(results.first?.age, 29)
    }

    func testCountQuery() throws {
        for _ in 0..<20 {
            _ = createSampleUser()
        }
        try saveContext()

        let count = try User.query()
            .count(in: context)

        XCTAssertEqual(count, 20)
    }
}

// MARK: - Supporting Types for Tests

struct UserDTO {
    let id: UUID
    let name: String
}
```
