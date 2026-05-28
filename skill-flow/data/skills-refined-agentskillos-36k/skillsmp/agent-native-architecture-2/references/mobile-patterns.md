<overview>
Mobile agent-native apps face unique challenges: background execution limits, system permissions, network constraints, and cost sensitivity. This guide covers patterns for building robust agent experiences on iOS and Android.
</overview>

<background_execution>
## Background Execution & Resumption

Mobile apps can be suspended or terminated at any time. Agents must handle this gracefully.

### The Challenge

```
User starts research agent
     ↓
Agent begins web search
     ↓
User switches to another app
     ↓
iOS suspends your app
     ↓
Agent is mid-execution... what happens?
```

### Checkpoint/Resume Pattern

Save agent state before backgrounding, restore on foreground:

```swift
class AgentOrchestrator: ObservableObject {
    @Published var activeSessions: [AgentSession] = []

    // Called when app is about to background
    func handleAppWillBackground() {
        for session in activeSessions {
            saveCheckpoint(session)
            session.transition(to: .backgrounded)
        }
    }

    // Called when app returns to foreground
    func handleAppDidForeground() {
        for session in activeSessions where session.state == .backgrounded {
            if let checkpoint = loadCheckpoint(session.id) {
                resumeFromCheckpoint(session, checkpoint)
            }
        }
    }

    private func saveCheckpoint(_ session: AgentSession) {
        let checkpoint = AgentCheckpoint(
            sessionId: session.id,
            conversationHistory: session.messages,
            pendingToolCalls: session.pendingToolCalls,
            partialResults: session.partialResults,
            timestamp: Date()
        )
        storage.save(checkpoint, for: session.id)
    }

    private func resumeFromCheckpoint(_ session: AgentSession, _ checkpoint: AgentCheckpoint) {
        session.messages = checkpoint.conversationHistory
        session.pendingToolCalls = checkpoint.pendingToolCalls

        // Resume execution if there were pending tool calls
        if !checkpoint.pendingToolCalls.isEmpty {
            session.transition(to: .running)
            Task { await executeNextTool(session) }
        }
    }
}
```

### State Machine for Agent Lifecycle

```swift
enum AgentState {
    case idle           // Not running
    case running        // Actively executing
    case waitingForUser // Paused, waiting for user input
    case backgrounded   // App backgrounded, state saved
    case completed      // Finished successfully
    case failed(Error)  // Finished with error
}

class AgentSession: ObservableObject {
    @Published var state: AgentState = .idle

    func transition(to newState: AgentState) {
        let validTransitions: [AgentState: Set<AgentState>] = [
            .idle: [.running],
            .running: [.waitingForUser, .backgrounded, .completed, .failed],
            .waitingForUser: [.running, .backgrounded],
            .backgrounded: [.running, .completed],
        ]

        guard validTransitions[state]?.contains(newState) == true else {
            logger.warning("Invalid transition: \(state) → \(newState)")
            return
        }

        state = newState
    }
}
```

### Background Task Extension (iOS)

Request extra time when backgrounded during critical operations:

```swift
class AgentOrchestrator {
    private var backgroundTask: UIBackgroundTaskIdentifier = .invalid

    func handleAppWillBackground() {
        // Request extra time for saving state
        backgroundTask = UIApplication.shared.beginBackgroundTask { [weak self] in
            self?.endBackgroundTask()
        }

        // Save all checkpoints
        Task {
            for session in activeSessions {
                await saveCheckpoint(session)
            }
            endBackgroundTask()
        }
    }

    private func endBackgroundTask() {
        if backgroundTask != .invalid {
            UIApplication.shared.endBackgroundTask(backgroundTask)
            backgroundTask = .invalid
        }
    }
}
```

### User Communication

Let users know what's happening:

```swift
struct AgentStatusView: View {
    @ObservedObject var session: AgentSession

    var body: some View {
        switch session.state {
        case .backgrounded:
            Label("Paused (app in background)", systemImage: "pause.circle")
                .foregroundColor(.orange)
        case .running:
            Label("Working...", systemImage: "ellipsis.circle")
                .foregroundColor(.blue)
        case .waitingForUser:
            Label("Waiting for your input", systemImage: "person.circle")
                .foregroundColor(.green)
        // ...
        }
    }
}
```
</background_execution>

<permissions>
## Permission Handling

Mobile agents may need access to system resources. Handle permission requests gracefully.

### Common Permissions

| Resource | iOS Permission | Use Case |
|----------|---------------|----------|
| Photo Library | PHPhotoLibrary | Profile generation from photos |
| Files | Document picker | Reading user documents |
| Camera | AVCaptureDevice | Scanning book covers |
| Location | CLLocationManager | Location-aware recommendations |
| Network | (automatic) | Web search, API calls |

### Permission-Aware Tools

Check permissions before executing:

```swift
struct PhotoTools {
    static func readPhotos() -> AgentTool {
        tool(
            name: "read_photos",
            description: "Read photos from the user's photo library",
            parameters: [
                "limit": .number("Maximum photos to read"),
                "dateRange": .string("Date range filter").optional()
            ],
            execute: { params, context in
                // Check permission first
                let status = await PHPhotoLibrary.requestAuthorization(for: .readWrite)

                switch status {
                case .authorized, .limited:
                    // Proceed with reading photos
                    let photos = await fetchPhotos(params)
                    return ToolResult(text: "Found \(photos.count) photos", images: photos)

                case .denied, .restricted:
                    return ToolResult(
                        text: "Photo access needed. Please grant permission in Settings → Privacy → Photos.",
                        isError: true
                    )

                case .notDetermined:
                    return ToolResult(
                        text: "Photo permission required. Please try again.",
                        isError: true
                    )

                @unknown default:
                    return ToolResult(text: "Unknown permission status", isError: true)
                }
            }
        )
    }
}
```

### Graceful Degradation

When permissions aren't granted, offer alternatives:

```swift
func readPhotos() async -> ToolResult {
    let status = PHPhotoLibrary.authorizationStatus(for: .readWrite)

    switch status {
    case .denied, .restricted:
        // Suggest alternative
        return ToolResult(
            text: """
            I don't have access to your photos. You can either:
            1. Grant access in Settings → Privacy → Photos
            2. Share specific photos directly in our chat

            Would you like me to help with something else instead?
            """,
            isError: false  // Not a hard error, just a limitation
        )
    // ...
    }
}
```

### Permission Request Timing

Don't request permissions until needed:

```swift
// BAD: Request all permissions at launch
func applicationDidFinishLaunching() {
    requestPhotoAccess()
    requestCameraAccess()
    requestLocationAccess()
    // User is overwhelmed with permission dialogs
}

// GOOD: Request when the feature is used
tool("analyze_book_cover", async ({ image }) => {
    // Only request camera access when user tries to scan a cover
    let status = await AVCaptureDevice.requestAccess(for: .video)
    if status {
        return await scanCover(image)
    } else {
        return ToolResult(text: "Camera access needed for book scanning")
    }
})
```
</permissions>

<cost_awareness>
## Cost-Aware Design

Mobile users may be on cellular data or concerned about API costs. Design agents to be efficient.

### Model Tier Selection

Use the cheapest model that achieves the outcome:

```swift
enum ModelTier {
    case fast      // claude-3-haiku: ~$0.25/1M tokens
    case balanced  // claude-3-sonnet: ~$3/1M tokens
    case powerful  // claude-3-opus: ~$15/1M tokens

    var modelId: String {
        switch self {
        case .fast: return "claude-3-haiku-20240307"
        case .balanced: return "claude-3-sonnet-20240229"
        case .powerful: return "claude-3-opus-20240229"
        }
    }
}

// Match model to task complexity
let agentConfigs: [AgentType: ModelTier] = [
    .quickLookup: .fast,        // "What's in my library?"
    .chatAssistant: .balanced,  // General conversation
    .researchAgent: .balanced,  // Web search + synthesis
    .profileGenerator: .powerful, // Complex photo analysis
    .introductionWriter: .balanced,
]
```

### Token Budgets

Limit tokens per agent session:

```swift
struct AgentConfig {
    let modelTier: ModelTier
    let maxInputTokens: Int
    let maxOutputTokens: Int
    let maxTurns: Int

    static let research = AgentConfig(
        modelTier: .balanced,
        maxInputTokens: 50_000,
        maxOutputTokens: 4_000,
        maxTurns: 20
    )

    static let quickChat = AgentConfig(
        modelTier: .fast,
        maxInputTokens: 10_000,
        maxOutputTokens: 1_000,
        maxTurns: 5
    )
}

class AgentSession {
    var totalTokensUsed: Int = 0

    func checkBudget() -> Bool {
        if totalTokensUsed > config.maxInputTokens {
            transition(to: .failed(AgentError.budgetExceeded))
            return false
        }
        return true
    }
}
```

### Network-Aware Execution

Defer heavy operations to WiFi:

```swift
class NetworkMonitor: ObservableObject {
    @Published var isOnWiFi: Bool = false
    @Published var isExpensive: Bool = false  // Cellular or hotspot

    private let monitor = NWPathMonitor()

    func startMonitoring() {
        monitor.pathUpdateHandler = { [weak self] path in
            DispatchQueue.main.async {
                self?.isOnWiFi = path.usesInterfaceType(.wifi)
                self?.isExpensive = path.isExpensive
            }
        }
        monitor.start(queue: .global())
    }
}

class AgentOrchestrator {
    @ObservedObject var network = NetworkMonitor()

    func startResearchAgent(for book: Book) async {
        if network.isExpensive {
            // Warn user or defer
            let proceed = await showAlert(
                "Research uses data",
                message: "This will use approximately 1-2 MB of cellular data. Continue?"
            )
            if !proceed { return }
        }

        // Proceed with research
        await runAgent(ResearchAgent.create(book: book))
    }
}
```

### Batch API Calls

Combine multiple small requests:

```swift
// BAD: Many small API calls
for book in books {
    await agent.chat("Summarize \(book.title)")
}

// GOOD: Batch into one request
let bookList = books.map { $0.title }.joined(separator: ", ")
await agent.chat("Summarize each of these books briefly: \(bookList)")
```

### Caching

Cache expensive operations:

```swift
class ResearchCache {
    private var cache: [String: CachedResearch] = [:]

    func getCachedResearch(for bookId: String) -> CachedResearch? {
        guard let cached = cache[bookId] else { return nil }

        // Expire after 24 hours
        if Date().timeIntervalSince(cached.timestamp) > 86400 {
            cache.removeValue(forKey: bookId)
            return nil
        }

        return cached
    }

    func cacheResearch(_ research: Research, for bookId: String) {
        cache[bookId] = CachedResearch(
            research: research,
            timestamp: Date()
        )
    }
}

// In research tool
tool("web_search", async ({ query, bookId }) => {
    // Check cache first
    if let cached = cache.getCachedResearch(for: bookId) {
        return ToolResult(text: cached.research.summary, cached: true)
    }

    // Otherwise, perform search
    let results = await webSearch(query)
    cache.cacheResearch(results, for: bookId)
    return ToolResult(text: results.summary)
})
```

### Cost Visibility

Show users what they're spending:

```swift
struct AgentCostView: View {
    @ObservedObject var session: AgentSession

    var body: some View {
        VStack(alignment: .leading) {
            Text("Session Stats")
                .font(.headline)

            HStack {
                Label("\(session.turnCount) turns", systemImage: "arrow.2.squarepath")
                Spacer()
                Label(formatTokens(session.totalTokensUsed), systemImage: "text.word.spacing")
            }

            if let estimatedCost = session.estimatedCost {
                Text("Est. cost: \(estimatedCost, format: .currency(code: "USD"))")
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
        }
    }
}
```
</cost_awareness>

<offline_handling>
## Offline Graceful Degradation

Handle offline scenarios gracefully:

```swift
class ConnectivityAwareAgent {
    @ObservedObject var network = NetworkMonitor()

    func executeToolCall(_ toolCall: ToolCall) async -> ToolResult {
        // Check if tool requires network
        let requiresNetwork = ["web_search", "web_fetch", "call_api"]
            .contains(toolCall.name)

        if requiresNetwork && !network.isConnected {
            return ToolResult(
                text: """
                I can't access the internet right now. Here's what I can do offline:
                - Read your library and existing research
                - Answer questions from cached data
                - Write notes and drafts for later

                Would you like me to try something that works offline?
                """,
                isError: false
            )
        }

        return await executeOnline(toolCall)
    }
}
```

### Offline-First Tools

Some tools should work entirely offline:

```swift
let offlineTools: Set<String> = [
    "read_file",
    "write_file",
    "list_files",
    "read_library",  // Local database
    "search_local",  // Local search
]

let onlineTools: Set<String> = [
    "web_search",
    "web_fetch",
    "publish_to_cloud",
]

let hybridTools: Set<String> = [
    "publish_to_feed",  // Works offline, syncs later
]
```

### Queued Actions

Queue actions that require connectivity:

```swift
class OfflineQueue: ObservableObject {
    @Published var pendingActions: [QueuedAction] = []

    func queue(_ action: QueuedAction) {
        pendingActions.append(action)
        persist()
    }

    func processWhenOnline() {
        network.$isConnected
            .filter { $0 }
            .sink { [weak self] _ in
                self?.processPendingActions()
            }
    }

    private func processPendingActions() {
        for action in pendingActions {
            Task {
                try await execute(action)
                remove(action)
            }
        }
    }
}
```
</offline_handling>

<battery_awareness>
## Battery-Aware Execution

Respect device battery state:

```swift
class BatteryMonitor: ObservableObject {
    @Published var batteryLevel: Float = 1.0
    @Published var isCharging: Bool = false
    @Published var isLowPowerMode: Bool = false

    var shouldDeferHeavyWork: Bool {
        return batteryLevel < 0.2 && !isCharging
    }

    func startMonitoring() {
        UIDevice.current.isBatteryMonitoringEnabled = true

        NotificationCenter.default.addObserver(
            forName: UIDevice.batteryLevelDidChangeNotification,
            object: nil,
            queue: .main
        ) { [weak self] _ in
            self?.batteryLevel = UIDevice.current.batteryLevel
        }

        NotificationCenter.default.addObserver(
            forName: NSNotification.Name.NSProcessInfoPowerStateDidChange,
            object: nil,
            queue: .main
        ) { [weak self] _ in
            self?.isLowPowerMode = ProcessInfo.processInfo.isLowPowerModeEnabled
        }
    }
}

class AgentOrchestrator {
    @ObservedObject var battery = BatteryMonitor()

    func startAgent(_ config: AgentConfig) async {
        if battery.shouldDeferHeavyWork && config.isHeavy {
            let proceed = await showAlert(
                "Low Battery",
                message: "This task uses significant battery. Continue or defer until charging?"
            )
            if !proceed { return }
        }

        // Adjust model tier based on battery
        let adjustedConfig = battery.isLowPowerMode
            ? config.withModelTier(.fast)
            : config

        await runAgent(adjustedConfig)
    }
}
```
</battery_awareness>

<checklist>
## Mobile Agent-Native Checklist

**Background Execution:**
- [ ] Checkpoint/resume implemented for all agent sessions
- [ ] State machine for agent lifecycle (idle, running, backgrounded, etc.)
- [ ] Background task extension for critical saves
- [ ] User-visible status for backgrounded agents

**Permissions:**
- [ ] Permissions requested only when needed, not at launch
- [ ] Graceful degradation when permissions denied
- [ ] Clear error messages with Settings deep links
- [ ] Alternative paths when permissions unavailable

**Cost Awareness:**
- [ ] Model tier matched to task complexity
- [ ] Token budgets per session
- [ ] Network-aware (defer heavy work to WiFi)
- [ ] Caching for expensive operations
- [ ] Cost visibility to users

**Offline Handling:**
- [ ] Offline-capable tools identified
- [ ] Graceful degradation for online-only features
- [ ] Action queue for sync when online
- [ ] Clear user communication about offline state

**Battery Awareness:**
- [ ] Battery monitoring for heavy operations
- [ ] Low power mode detection
- [ ] Defer or downgrade based on battery state
</checklist>
