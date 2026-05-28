// MARK: - Sendable Reference Types
// クラス（参照型）の Sendable 準拠例

import Foundation

// MARK: - final class + immutable properties

/// クラスを Sendable にするには:
/// 1. final であること
/// 2. すべての stored property が let（immutable）であること
/// 3. すべての stored property が Sendable であること

final class AppConfiguration: Sendable {
    let apiBaseURL: URL
    let apiKey: String
    let timeout: TimeInterval
    let maxRetries: Int

    init(
        apiBaseURL: URL,
        apiKey: String,
        timeout: TimeInterval = 30,
        maxRetries: Int = 3
    ) {
        self.apiBaseURL = apiBaseURL
        self.apiKey = apiKey
        self.timeout = timeout
        self.maxRetries = maxRetries
    }
}

// MARK: - 使用例: 設定を複数の Task で共有

func useConfiguration() async {
    let config = AppConfiguration(
        apiBaseURL: URL(string: "https://api.example.com")!,
        apiKey: "secret-key"
    )

    // 複数の Task から安全にアクセス可能
    async let task1: Void = Task {
        print("API URL: \(config.apiBaseURL)")
    }.value

    async let task2: Void = Task {
        print("Timeout: \(config.timeout)")
    }.value

    await (task1, task2)
}

// MARK: - ネストした Sendable クラス

final class DatabaseConfig: Sendable {
    let host: String
    let port: Int
    let database: String

    init(host: String, port: Int, database: String) {
        self.host = host
        self.port = port
        self.database = database
    }
}

final class ServerConfig: Sendable {
    let api: AppConfiguration
    let database: DatabaseConfig

    init(api: AppConfiguration, database: DatabaseConfig) {
        self.api = api
        self.database = database
    }
}

// MARK: - BAD: Sendable にできないクラスの例

/// このクラスは Sendable にできない（var プロパティがある）
// final class MutableConfig: Sendable {  // Error!
//     var currentTheme: String = "light"  // var は不可
// }

/// このクラスも Sendable にできない（final ではない）
// class NonFinalConfig: Sendable {  // Error!
//     let value: String
// }

// MARK: - 解決策: Actor を使う

/// 可変状態が必要な場合は actor を使用
actor MutableConfigActor {
    var currentTheme: String = "light"
    var fontSize: Int = 14

    func setTheme(_ theme: String) {
        currentTheme = theme
    }

    func setFontSize(_ size: Int) {
        fontSize = size
    }
}

// MARK: - Sendable な計算プロパティ

final class UserSettings: Sendable {
    let firstName: String
    let lastName: String
    let prefersDarkMode: Bool

    init(firstName: String, lastName: String, prefersDarkMode: Bool) {
        self.firstName = firstName
        self.lastName = lastName
        self.prefersDarkMode = prefersDarkMode
    }

    // 計算プロパティは OK（状態を変更しない）
    var fullName: String {
        "\(firstName) \(lastName)"
    }

    var themeDescription: String {
        prefersDarkMode ? "Dark Mode" : "Light Mode"
    }
}

// MARK: - Protocol と Sendable

/// Protocol に Sendable 制約を追加
protocol ConfigurationProtocol: Sendable {
    var identifier: String { get }
}

final class FeatureFlag: ConfigurationProtocol, Sendable {
    let identifier: String
    let isEnabled: Bool

    init(identifier: String, isEnabled: Bool) {
        self.identifier = identifier
        self.isEnabled = isEnabled
    }
}
