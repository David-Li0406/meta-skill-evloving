// MARK: - nonisolated Methods and Properties
// nonisolated キーワードの使用例

import Foundation

// MARK: - Actor での nonisolated

/// Actor 内で nonisolated を使用する主なケース:
/// 1. let プロパティへのアクセス
/// 2. 状態に依存しない計算
/// 3. Protocol 準拠のためのメソッド

actor UserSession {
    // let プロパティは暗黙的に nonisolated
    let sessionId: UUID
    let createdAt: Date

    // var プロパティは actor-isolated
    private var _accessToken: String?
    private var _refreshToken: String?
    private var _lastActivity: Date

    init(sessionId: UUID = UUID()) {
        self.sessionId = sessionId
        self.createdAt = Date()
        self._lastActivity = Date()
    }

    // MARK: - nonisolated 計算プロパティ

    /// let プロパティのみを使用するので nonisolated にできる
    nonisolated var sessionInfo: String {
        "Session: \(sessionId.uuidString) created at \(createdAt)"
    }

    /// 定数のみを使用
    nonisolated var sessionAge: TimeInterval {
        Date().timeIntervalSince(createdAt)
    }

    // MARK: - Actor-isolated プロパティ

    var accessToken: String? {
        _accessToken
    }

    var isAuthenticated: Bool {
        _accessToken != nil
    }

    // MARK: - Actor-isolated メソッド

    func setTokens(access: String, refresh: String) {
        _accessToken = access
        _refreshToken = refresh
        _lastActivity = Date()
    }

    func clearTokens() {
        _accessToken = nil
        _refreshToken = nil
    }

    // MARK: - nonisolated メソッド

    /// 状態にアクセスしないメソッド
    nonisolated func validateTokenFormat(_ token: String) -> Bool {
        // JWT形式の簡易チェック（状態に依存しない）
        let parts = token.split(separator: ".")
        return parts.count == 3
    }
}

// MARK: - Protocol 準拠での nonisolated

/// Hashable 準拠には nonisolated が必要
actor Document: Hashable {
    let id: UUID
    let title: String
    private var content: String

    init(id: UUID = UUID(), title: String, content: String = "") {
        self.id = id
        self.title = title
        self.content = content
    }

    // Equatable - nonisolated が必要
    nonisolated static func == (lhs: Document, rhs: Document) -> Bool {
        lhs.id == rhs.id
    }

    // Hashable - nonisolated が必要
    nonisolated func hash(into hasher: inout Hasher) {
        hasher.combine(id)
    }

    // Actor-isolated メソッド
    func updateContent(_ newContent: String) {
        content = newContent
    }

    func getContent() -> String {
        content
    }
}

// MARK: - Codable 準拠での nonisolated

actor Settings: Codable {
    let version: Int
    private var theme: String
    private var fontSize: Int

    init(version: Int = 1, theme: String = "system", fontSize: Int = 14) {
        self.version = version
        self.theme = theme
        self.fontSize = fontSize
    }

    // Codable の CodingKeys
    enum CodingKeys: String, CodingKey {
        case version, theme, fontSize
    }

    // nonisolated init(from:) - Decodable 準拠
    nonisolated init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)
        version = try container.decode(Int.self, forKey: .version)
        theme = try container.decode(String.self, forKey: .theme)
        fontSize = try container.decode(Int.self, forKey: .fontSize)
    }

    // nonisolated encode(to:) - Encodable 準拠
    nonisolated func encode(to encoder: Encoder) throws {
        var container = encoder.container(keyedBy: CodingKeys.self)
        try container.encode(version, forKey: .version)
        // 注意: actor-isolated プロパティにアクセスできない
        // この例では初期化時の値を使用するか、別の方法が必要
    }

    // Actor-isolated でテーマを変更
    func setTheme(_ newTheme: String) {
        theme = newTheme
    }
}

// MARK: - @MainActor クラスでの nonisolated

@MainActor
class ViewModel {
    let id: UUID
    var items: [String] = []
    var isLoading = false

    init(id: UUID = UUID()) {
        self.id = id
    }

    // nonisolated - let プロパティのみ使用
    nonisolated var identifier: String {
        id.uuidString
    }

    // nonisolated メソッド - 状態に依存しない
    nonisolated func formatItem(_ item: String) -> String {
        item.trimmingCharacters(in: .whitespaces).lowercased()
    }

    // @MainActor - 状態を変更
    func addItem(_ item: String) {
        items.append(formatItem(item))
    }
}

// MARK: - nonisolated(unsafe)

/// ⚠️ nonisolated(unsafe) は危険 - 最後の手段としてのみ使用
/// データ競合の責任はプログラマーにある

actor LegacyBridge {
    // このプロパティは外部の同期機構で保護されている想定
    nonisolated(unsafe) var unsafeValue: Int = 0

    // 通常のメソッドでは安全にアクセス
    func safeIncrement() {
        unsafeValue += 1
    }
}

// MARK: - 使用例

func demonstrateNonisolated() async {
    let session = UserSession()

    // nonisolated プロパティは await なしでアクセス可能
    print(session.sessionInfo)
    print("Session age: \(session.sessionAge)")

    // nonisolated メソッドも await 不要
    let isValid = session.validateTokenFormat("header.payload.signature")
    print("Token valid format: \(isValid)")

    // actor-isolated プロパティには await が必要
    let isAuth = await session.isAuthenticated
    print("Is authenticated: \(isAuth)")

    // Document の Hashable
    let doc1 = Document(title: "Doc 1")
    let doc2 = Document(title: "Doc 2")

    // nonisolated なので Set に入れられる
    var documents: Set<Document> = [doc1, doc2]
    print("Documents count: \(documents.count)")
}
