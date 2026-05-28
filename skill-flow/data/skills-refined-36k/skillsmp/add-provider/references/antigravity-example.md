# Antigravity Provider Implementation Example

A complete reference implementation showing how to add a new provider.

## Files Created

```
Sources/Domain/Provider/AntigravityProvider.swift
Sources/Infrastructure/CLI/AntigravityUsageProbe.swift
Tests/InfrastructureTests/CLI/AntigravityUsageProbeParsingTests.swift
Tests/InfrastructureTests/CLI/AntigravityUsageProbeTests.swift
```

## Parsing Tests Example

```swift
@Suite
struct AntigravityUsageProbeParsingTests {

    static let sampleUserStatusResponse = """
    {
      "userStatus": {
        "email": "user@example.com",
        "cascadeModelConfigData": {
          "clientModelConfigs": [
            {
              "label": "Claude Sonnet",
              "modelOrAlias": { "model": "claude-sonnet-4" },
              "quotaInfo": { "remainingFraction": 0.75, "resetTime": "2025-01-01T00:00:00Z" }
            }
          ]
        }
      }
    }
    """

    @Test func `parses model quota into UsageQuota`() throws {
        let data = Data(Self.sampleUserStatusResponse.utf8)
        let snapshot = try AntigravityUsageProbe.parseUserStatusResponse(data, providerId: "antigravity")
        #expect(snapshot.quotas.count == 1)
        #expect(snapshot.quotas[0].quotaType == .modelSpecific("Claude Sonnet"))
    }

    @Test func `maps remainingFraction to percentRemaining`() throws {
        let data = Data(Self.sampleUserStatusResponse.utf8)
        let snapshot = try AntigravityUsageProbe.parseUserStatusResponse(data, providerId: "antigravity")
        #expect(snapshot.quotas[0].percentRemaining == 75.0)
    }

    @Test func `parses ISO-8601 resetTime to Date`() throws {
        let data = Data(Self.sampleUserStatusResponse.utf8)
        let snapshot = try AntigravityUsageProbe.parseUserStatusResponse(data, providerId: "antigravity")
        let expectedDate = ISO8601DateFormatter().date(from: "2025-01-01T00:00:00Z")
        #expect(snapshot.quotas[0].resetsAt == expectedDate)
    }

    @Test func `extracts account email from userStatus`() throws {
        let data = Data(Self.sampleUserStatusResponse.utf8)
        let snapshot = try AntigravityUsageProbe.parseUserStatusResponse(data, providerId: "antigravity")
        #expect(snapshot.accountEmail == "user@example.com")
    }
}
```

## Probe Behavior Tests Example

```swift
@Suite
struct AntigravityUsageProbeTests {

    static let samplePsOutputWithAntigravity = """
    12345 /path/to/language_server_macos --csrf_token abc123token --app_data_dir antigravity
    """

    @Test func `isAvailable returns false when process not running`() async {
        let mockExecutor = MockCLIExecutor()
        given(mockExecutor)
            .execute(binary: .any, args: .any, input: .any, timeout: .any, workingDirectory: .any, autoResponses: .any)
            .willReturn(CLIResult(output: "no antigravity here", exitCode: 0))

        let probe = AntigravityUsageProbe(cliExecutor: mockExecutor)
        #expect(await probe.isAvailable() == false)
    }

    @Test func `isAvailable returns true when process detected`() async {
        let mockExecutor = MockCLIExecutor()
        given(mockExecutor)
            .execute(binary: .any, args: .any, input: .any, timeout: .any, workingDirectory: .any, autoResponses: .any)
            .willReturn(CLIResult(output: Self.samplePsOutputWithAntigravity, exitCode: 0))

        let probe = AntigravityUsageProbe(cliExecutor: mockExecutor)
        #expect(await probe.isAvailable() == true)
    }

    @Test func `probe throws cliNotFound when no process`() async throws {
        let mockExecutor = MockCLIExecutor()
        given(mockExecutor)
            .execute(binary: .any, args: .any, input: .any, timeout: .any, workingDirectory: .any, autoResponses: .any)
            .willReturn(CLIResult(output: "", exitCode: 0))

        let probe = AntigravityUsageProbe(cliExecutor: mockExecutor)
        await #expect(throws: ProbeError.cliNotFound("Antigravity")) {
            try await probe.probe()
        }
    }
}
```

## Probe Implementation Pattern

```swift
public struct AntigravityUsageProbe: UsageProbe {
    private let cliExecutor: any CLIExecutor
    private let networkClient: any NetworkClient
    private let timeout: TimeInterval

    public init(
        cliExecutor: (any CLIExecutor)? = nil,
        networkClient: (any NetworkClient)? = nil,
        timeout: TimeInterval = 8.0
    ) {
        self.cliExecutor = cliExecutor ?? DefaultCLIExecutor()
        self.networkClient = networkClient ?? URLSession.shared
        self.timeout = timeout
    }

    public func isAvailable() async -> Bool {
        do {
            _ = try await detectProcess()
            return true
        } catch {
            return false
        }
    }

    public func probe() async throws -> UsageSnapshot {
        let processInfo = try await detectProcess()
        let ports = try await discoverPorts(pid: processInfo.pid)
        let data = try await fetchQuota(ports: ports, csrfToken: processInfo.csrfToken)
        return try Self.parseUserStatusResponse(data, providerId: "antigravity")
    }

    // Static for testability
    static func parseUserStatusResponse(_ data: Data, providerId: String) throws -> UsageSnapshot {
        let decoder = JSONDecoder()
        let response = try decoder.decode(UserStatusResponse.self, from: data)
        // Map to UsageSnapshot with UsageQuota array
    }
}
```

## Provider Class Pattern

Antigravity uses the **base `ProviderSettingsRepository`** since it has no special config/credentials.

```swift
@Observable
public final class AntigravityProvider: AIProvider, @unchecked Sendable {
    public let id = "antigravity"
    public let name = "Antigravity"
    public let cliCommand = "antigravity"

    public var dashboardURL: URL? { nil }
    public var statusPageURL: URL? { nil }

    /// Whether the provider is enabled (persisted via settingsRepository)
    public var isEnabled: Bool {
        didSet {
            settingsRepository.setEnabled(isEnabled, forProvider: id)
        }
    }

    public private(set) var isSyncing: Bool = false
    public private(set) var snapshot: UsageSnapshot?
    public private(set) var lastError: Error?

    private let probe: any UsageProbe
    private let settingsRepository: any ProviderSettingsRepository  // Base protocol - no special config

    public init(probe: any UsageProbe, settingsRepository: any ProviderSettingsRepository) {
        self.probe = probe
        self.settingsRepository = settingsRepository
        self.isEnabled = settingsRepository.isEnabled(forProvider: "antigravity")
    }

    public func isAvailable() async -> Bool {
        await probe.isAvailable()
    }

    @discardableResult
    public func refresh() async throws -> UsageSnapshot {
        isSyncing = true
        defer { isSyncing = false }
        do {
            let newSnapshot = try await probe.probe()
            snapshot = newSnapshot
            lastError = nil
            return newSnapshot
        } catch {
            lastError = error
            throw error
        }
    }
}
```

**Note:** For providers needing special config (like Z.ai or Copilot), use a sub-protocol:
- `ZaiSettingsRepository` - config path + env var
- `CopilotSettingsRepository` - env var + credentials

## Common Probe Types

### CLI Binary Probe (like Claude, Codex)
- Use `CLIExecutor.locate()` to find binary
- Use `CLIExecutor.execute()` to run commands
- Parse CLI output

### Local Process Probe (like Antigravity)
- Use `ps` to detect running process
- Extract auth tokens from process args
- Use `lsof` for port discovery
- Make HTTP requests to local API

### Remote API Probe (like Gemini, Copilot)
- Read credentials from config file
- Use `NetworkClient` for HTTP requests
- Handle OAuth token refresh
