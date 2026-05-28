# Complete App Lifecycle Management Implementation

<!-- Loading Trigger: Agent reads this file when implementing app lifecycle, background tasks, state restoration, or launch optimization -->

## Modern ScenePhase-Based Lifecycle

```swift
import SwiftUI
import Combine

// MARK: - App Entry Point with Lifecycle Handling

@main
struct MyApp: App {
    @Environment(\.scenePhase) private var scenePhase
    @StateObject private var appState = AppStateManager()
    @StateObject private var backgroundTaskManager = BackgroundTaskManager()

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(appState)
                .environmentObject(backgroundTaskManager)
        }
        .onChange(of: scenePhase) { oldPhase, newPhase in
            handleScenePhaseChange(from: oldPhase, to: newPhase)
        }
        #if os(iOS)
        .backgroundTask(.appRefresh("com.app.refresh")) {
            await backgroundTaskManager.performAppRefresh()
        }
        .backgroundTask(.urlSession("com.app.download")) {
            await backgroundTaskManager.handleBackgroundURLSession()
        }
        #endif
    }

    private func handleScenePhaseChange(from oldPhase: ScenePhase, to newPhase: ScenePhase) {
        switch (oldPhase, newPhase) {
        case (_, .active):
            appState.handleBecameActive()

        case (.active, .inactive):
            appState.handleWillResignActive()

        case (.inactive, .background):
            appState.handleDidEnterBackground()
            backgroundTaskManager.scheduleBackgroundTasks()

        case (.background, .inactive):
            appState.handleWillEnterForeground()

        default:
            break
        }
    }
}

// MARK: - App State Manager

@MainActor
final class AppStateManager: ObservableObject {
    @Published private(set) var isActive = false
    @Published private(set) var lastActiveDate: Date?
    @Published private(set) var sessionDuration: TimeInterval = 0

    private var sessionStartTime: Date?
    private var stateRestorationManager = StateRestorationManager()
    private var cancellables = Set<AnyCancellable>()

    init() {
        setupNotifications()
        restoreState()
    }

    private func setupNotifications() {
        // Handle memory warnings
        NotificationCenter.default.publisher(for: UIApplication.didReceiveMemoryWarningNotification)
            .sink { [weak self] _ in
                self?.handleMemoryWarning()
            }
            .store(in: &cancellables)

        // Handle significant time change
        NotificationCenter.default.publisher(for: UIApplication.significantTimeChangeNotification)
            .sink { [weak self] _ in
                self?.handleSignificantTimeChange()
            }
            .store(in: &cancellables)
    }

    func handleBecameActive() {
        isActive = true
        sessionStartTime = Date()

        // Check if returning from long background
        if let lastActive = lastActiveDate,
           Date().timeIntervalSince(lastActive) > 300 { // 5 minutes
            refreshDataIfNeeded()
        }

        // Resume any paused operations
        resumePausedOperations()
    }

    func handleWillResignActive() {
        isActive = false

        // Pause animations, timers
        pauseActiveOperations()

        // Save quick state
        saveQuickState()
    }

    func handleDidEnterBackground() {
        lastActiveDate = Date()

        // Calculate session duration
        if let startTime = sessionStartTime {
            sessionDuration += Date().timeIntervalSince(startTime)
        }

        // Save complete state
        saveCompleteState()

        // Release memory
        releaseUnnecessaryResources()
    }

    func handleWillEnterForeground() {
        // Prepare UI
        prepareUIForForeground()
    }

    private func handleMemoryWarning() {
        // Clear caches
        ImageCache.shared.clearMemoryCache()
        URLCache.shared.removeAllCachedResponses()

        // Release non-essential resources
        releaseUnnecessaryResources()
    }

    private func handleSignificantTimeChange() {
        // Refresh time-sensitive data
        refreshTimeDisplays()
    }

    private func refreshDataIfNeeded() {
        Task {
            // Refresh stale data
        }
    }

    private func pauseActiveOperations() {
        // Pause video, audio, animations
    }

    private func resumePausedOperations() {
        // Resume paused operations
    }

    private func saveQuickState() {
        stateRestorationManager.saveQuickState()
    }

    private func saveCompleteState() {
        stateRestorationManager.saveCompleteState()
    }

    private func restoreState() {
        stateRestorationManager.restoreState()
    }

    private func releaseUnnecessaryResources() {
        // Release cached data, temporary files
    }

    private func prepareUIForForeground() {
        // Refresh UI elements
    }

    private func refreshTimeDisplays() {
        // Update any time-based UI
    }
}
```

## Background Task Management

```swift
import BackgroundTasks

@MainActor
final class BackgroundTaskManager: ObservableObject {

    static let appRefreshIdentifier = "com.app.refresh"
    static let processingIdentifier = "com.app.processing"
    static let cleanupIdentifier = "com.app.cleanup"

    @Published private(set) var lastRefreshDate: Date?
    @Published private(set) var pendingTaskCount = 0

    init() {
        registerBackgroundTasks()
    }

    // MARK: - Registration

    private func registerBackgroundTasks() {
        BGTaskScheduler.shared.register(
            forTaskWithIdentifier: Self.appRefreshIdentifier,
            using: nil
        ) { task in
            Task { @MainActor in
                await self.handleAppRefresh(task: task as! BGAppRefreshTask)
            }
        }

        BGTaskScheduler.shared.register(
            forTaskWithIdentifier: Self.processingIdentifier,
            using: nil
        ) { task in
            Task { @MainActor in
                await self.handleProcessingTask(task: task as! BGProcessingTask)
            }
        }
    }

    // MARK: - Scheduling

    func scheduleBackgroundTasks() {
        scheduleAppRefresh()
        scheduleProcessingIfNeeded()
    }

    private func scheduleAppRefresh() {
        let request = BGAppRefreshTaskRequest(identifier: Self.appRefreshIdentifier)
        request.earliestBeginDate = Date(timeIntervalSinceNow: 15 * 60) // 15 minutes

        do {
            try BGTaskScheduler.shared.submit(request)
        } catch {
            print("Failed to schedule app refresh: \(error)")
        }
    }

    private func scheduleProcessingIfNeeded() {
        guard hasPendingProcessingWork() else { return }

        let request = BGProcessingTaskRequest(identifier: Self.processingIdentifier)
        request.requiresNetworkConnectivity = true
        request.requiresExternalPower = false
        request.earliestBeginDate = Date(timeIntervalSinceNow: 60 * 60) // 1 hour

        do {
            try BGTaskScheduler.shared.submit(request)
        } catch {
            print("Failed to schedule processing: \(error)")
        }
    }

    // MARK: - Task Handling

    @MainActor
    private func handleAppRefresh(task: BGAppRefreshTask) async {
        // Schedule next refresh
        scheduleAppRefresh()

        // Create task to perform work
        let refreshTask = Task {
            await performAppRefresh()
        }

        // Handle expiration
        task.expirationHandler = {
            refreshTask.cancel()
        }

        // Perform work
        do {
            try await refreshTask.value
            lastRefreshDate = Date()
            task.setTaskCompleted(success: true)
        } catch {
            task.setTaskCompleted(success: false)
        }
    }

    @MainActor
    private func handleProcessingTask(task: BGProcessingTask) async {
        let processingTask = Task {
            await performBackgroundProcessing()
        }

        task.expirationHandler = {
            processingTask.cancel()
        }

        do {
            try await processingTask.value
            task.setTaskCompleted(success: true)
        } catch {
            task.setTaskCompleted(success: false)
        }
    }

    // MARK: - Work Methods

    func performAppRefresh() async {
        // Fetch new data
        async let dataRefresh = refreshData()
        async let notificationSync = syncNotifications()

        _ = await (dataRefresh, notificationSync)
    }

    func handleBackgroundURLSession() async {
        // Handle completed downloads
    }

    private func performBackgroundProcessing() async throws {
        // Heavy processing like database cleanup
        try await cleanupOldData()
        try await optimizeDatabase()
        try await syncPendingChanges()
    }

    private func refreshData() async {
        // Refresh app data
    }

    private func syncNotifications() async {
        // Sync notification state
    }

    private func cleanupOldData() async throws {
        // Remove old cached data
    }

    private func optimizeDatabase() async throws {
        // Optimize Core Data
    }

    private func syncPendingChanges() async throws {
        // Sync pending changes to server
    }

    private func hasPendingProcessingWork() -> Bool {
        return pendingTaskCount > 0
    }
}

// MARK: - Background URL Session Handler

class BackgroundURLSessionManager: NSObject, URLSessionDownloadDelegate {
    static let shared = BackgroundURLSessionManager()

    private var completionHandlers: [String: () -> Void] = [:]

    lazy var backgroundSession: URLSession = {
        let config = URLSessionConfiguration.background(withIdentifier: "com.app.background.download")
        config.sessionSendsLaunchEvents = true
        config.isDiscretionary = true
        return URLSession(configuration: config, delegate: self, delegateQueue: nil)
    }()

    func setCompletionHandler(_ handler: @escaping () -> Void, forSession identifier: String) {
        completionHandlers[identifier] = handler
    }

    func urlSession(_ session: URLSession, downloadTask: URLSessionDownloadTask, didFinishDownloadingTo location: URL) {
        // Move downloaded file to permanent location
        guard let response = downloadTask.response as? HTTPURLResponse,
              (200...299).contains(response.statusCode) else {
            return
        }

        // Handle downloaded file
        handleDownloadedFile(at: location, for: downloadTask)
    }

    func urlSessionDidFinishEvents(forBackgroundURLSession session: URLSession) {
        DispatchQueue.main.async {
            if let handler = self.completionHandlers[session.configuration.identifier ?? ""] {
                handler()
                self.completionHandlers.removeValue(forKey: session.configuration.identifier ?? "")
            }
        }
    }

    private func handleDownloadedFile(at location: URL, for task: URLSessionDownloadTask) {
        // Process downloaded file
    }
}
```

## State Restoration

```swift
import Foundation

actor StateRestorationManager {
    private let userDefaults = UserDefaults.standard
    private let fileManager = FileManager.default

    private var quickState: [String: Any] = [:]
    private var restorationData: RestorationData?

    struct RestorationData: Codable {
        var navigationPath: [String]
        var selectedTab: Int
        var scrollPositions: [String: CGFloat]
        var formData: [String: String]
        var lastViewedItem: String?
        var timestamp: Date
    }

    // MARK: - Quick State (for brief interruptions)

    func saveQuickState() {
        // Save minimal state for quick resume
        quickState["lastScreen"] = getCurrentScreen()
        quickState["timestamp"] = Date()
    }

    func restoreQuickState() -> [String: Any] {
        return quickState
    }

    // MARK: - Complete State (for background)

    func saveCompleteState() {
        let data = RestorationData(
            navigationPath: getNavigationPath(),
            selectedTab: getSelectedTab(),
            scrollPositions: getScrollPositions(),
            formData: getFormData(),
            lastViewedItem: getLastViewedItem(),
            timestamp: Date()
        )

        do {
            let encoded = try JSONEncoder().encode(data)
            try encoded.write(to: stateFileURL)
            restorationData = data
        } catch {
            print("Failed to save state: \(error)")
        }
    }

    func restoreState() {
        do {
            let data = try Data(contentsOf: stateFileURL)
            restorationData = try JSONDecoder().decode(RestorationData.self, from: data)

            // Check if state is still valid (not too old)
            if let restoration = restorationData,
               Date().timeIntervalSince(restoration.timestamp) < 24 * 60 * 60 {
                applyRestoredState(restoration)
            }
        } catch {
            print("Failed to restore state: \(error)")
        }
    }

    private func applyRestoredState(_ data: RestorationData) {
        // Apply restored state to app
        setSelectedTab(data.selectedTab)
        setNavigationPath(data.navigationPath)
        setScrollPositions(data.scrollPositions)
        restoreFormData(data.formData)
    }

    private var stateFileURL: URL {
        let documentsPath = fileManager.urls(for: .documentDirectory, in: .userDomainMask)[0]
        return documentsPath.appendingPathComponent("app_state.json")
    }

    // MARK: - State Getters (implement based on app structure)

    private func getCurrentScreen() -> String { "" }
    private func getNavigationPath() -> [String] { [] }
    private func getSelectedTab() -> Int { 0 }
    private func getScrollPositions() -> [String: CGFloat] { [:] }
    private func getFormData() -> [String: String] { [:] }
    private func getLastViewedItem() -> String? { nil }

    // MARK: - State Setters

    private func setSelectedTab(_ tab: Int) { }
    private func setNavigationPath(_ path: [String]) { }
    private func setScrollPositions(_ positions: [String: CGFloat]) { }
    private func restoreFormData(_ data: [String: String]) { }
}

// MARK: - Scene Storage for SwiftUI Views

struct ContentView: View {
    @SceneStorage("selectedTab") private var selectedTab = 0
    @SceneStorage("searchText") private var searchText = ""
    @SceneStorage("scrollPosition") private var scrollPosition: String?

    var body: some View {
        TabView(selection: $selectedTab) {
            HomeView(scrollPosition: $scrollPosition)
                .tag(0)

            SearchView(searchText: $searchText)
                .tag(1)

            ProfileView()
                .tag(2)
        }
    }
}
```

## Launch Optimization

```swift
import UIKit
import os.signpost

// MARK: - Launch Performance Tracking

final class LaunchPerformanceTracker {
    static let shared = LaunchPerformanceTracker()

    private let log = OSLog(subsystem: Bundle.main.bundleIdentifier ?? "app", category: "Launch")
    private var launchStartTime: CFAbsoluteTime = 0
    private var milestones: [String: CFAbsoluteTime] = [:]

    private init() {}

    func recordLaunchStart() {
        launchStartTime = CFAbsoluteTimeGetCurrent()
        os_signpost(.begin, log: log, name: "App Launch")
    }

    func recordMilestone(_ name: String) {
        let time = CFAbsoluteTimeGetCurrent()
        milestones[name] = time - launchStartTime
        os_signpost(.event, log: log, name: "Milestone", "%{public}s", name)
    }

    func recordLaunchComplete() {
        let totalTime = CFAbsoluteTimeGetCurrent() - launchStartTime
        os_signpost(.end, log: log, name: "App Launch")

        #if DEBUG
        print("Launch completed in \(totalTime * 1000)ms")
        for (milestone, time) in milestones.sorted(by: { $0.value < $1.value }) {
            print("  \(milestone): \(time * 1000)ms")
        }
        #endif
    }
}

// MARK: - Deferred Initialization

@MainActor
final class DeferredInitializer {
    static let shared = DeferredInitializer()

    private var deferredTasks: [() async -> Void] = []
    private var hasInitialized = false

    func deferUntilIdle(_ task: @escaping () async -> Void) {
        deferredTasks.append(task)
    }

    func executeDeferredTasks() {
        guard !hasInitialized else { return }
        hasInitialized = true

        Task(priority: .utility) {
            // Wait for UI to be interactive
            try? await Task.sleep(nanoseconds: 500_000_000) // 0.5 seconds

            for task in deferredTasks {
                await task()
            }
            deferredTasks.removeAll()
        }
    }
}

// MARK: - Prewarming Critical Paths

final class AppPrewarmer {
    static func prewarmCriticalPaths() {
        // Prewarm URLSession
        _ = URLSession.shared.configuration

        // Prewarm formatters (expensive to create)
        _ = ISO8601DateFormatter()
        _ = NumberFormatter()

        // Prewarm Core Data stack (in background)
        Task.detached(priority: .utility) {
            _ = PersistenceController.shared.container
        }
    }
}

// MARK: - Optimized App Delegate

class AppDelegate: NSObject, UIApplicationDelegate {

    func application(
        _ application: UIApplication,
        didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?
    ) -> Bool {

        LaunchPerformanceTracker.shared.recordLaunchStart()

        // 1. Critical path only - required before UI
        configureCriticalServices()
        LaunchPerformanceTracker.shared.recordMilestone("Critical services")

        // 2. Prewarm expensive operations
        AppPrewarmer.prewarmCriticalPaths()
        LaunchPerformanceTracker.shared.recordMilestone("Prewarming started")

        // 3. Defer non-critical initialization
        DeferredInitializer.shared.deferUntilIdle {
            await self.configureAnalytics()
        }

        DeferredInitializer.shared.deferUntilIdle {
            await self.configureRemoteConfig()
        }

        DeferredInitializer.shared.deferUntilIdle {
            await self.prefetchData()
        }

        return true
    }

    func applicationDidBecomeActive(_ application: UIApplication) {
        LaunchPerformanceTracker.shared.recordLaunchComplete()
        DeferredInitializer.shared.executeDeferredTasks()
    }

    private func configureCriticalServices() {
        // Only what's needed for first frame
        // - Authentication state check
        // - Feature flags (cached)
        // - Theme/appearance
    }

    private func configureAnalytics() async {
        // Initialize analytics SDK
    }

    private func configureRemoteConfig() async {
        // Fetch remote configuration
    }

    private func prefetchData() async {
        // Prefetch commonly needed data
    }
}
```

## tvOS Lifecycle Differences

```swift
#if os(tvOS)
import TVUIKit

@main
struct TVApp: App {
    @Environment(\.scenePhase) private var scenePhase
    @StateObject private var focusState = TVFocusStateManager()

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(focusState)
        }
        .onChange(of: scenePhase) { _, newPhase in
            switch newPhase {
            case .active:
                // Resume playback, restore focus
                focusState.restoreFocus()

            case .inactive:
                // Pause playback, save focus state
                focusState.saveFocusState()

            case .background:
                // tvOS apps rarely go to background
                // Clean up resources
                break

            @unknown default:
                break
            }
        }
    }
}

@MainActor
class TVFocusStateManager: ObservableObject {
    @Published var lastFocusedItemID: String?

    func saveFocusState() {
        // Save current focus for restoration
    }

    func restoreFocus() {
        // Restore focus to last focused item
    }
}
#endif
```
