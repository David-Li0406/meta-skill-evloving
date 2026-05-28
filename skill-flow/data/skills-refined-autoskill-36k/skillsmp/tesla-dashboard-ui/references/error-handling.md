# Error Handling / エラーハンドリング

Tesla Dashboard UIのエラーハンドリングパターンについて解説します。

## Overview / 概要

`Result<T, TeslaError>` 型ベースのエラーハンドリングシステムです。

## TeslaError / エラー型

### 定義

```swift
enum TeslaError: LocalizedError {
    // Vehicle Errors
    case vehicleConnectionFailed(reason: String)
    case vehicleDataUnavailable
    case commandFailed(command: String, reason: String)
    case authenticationFailed

    // Location Errors
    case locationPermissionDenied
    case locationUnavailable
    case routeCalculationFailed(reason: String)
    case geocodingFailed(address: String)

    // Media Errors
    case mediaPlaybackFailed(reason: String)
    case mediaSourceUnavailable

    // Data Errors
    case saveFailed(entity: String, reason: String)
    case loadFailed(entity: String, reason: String)
    case deleteFailed(entity: String, reason: String)

    // Network Errors
    case networkUnavailable
    case timeout
    case serverError(statusCode: Int)

    // General Errors
    case unknown(underlying: Error?)
    case featureNotSupported(feature: String)
}
```

### LocalizedError 実装

```swift
extension TeslaError {
    var errorDescription: String? {
        switch self {
        case .vehicleConnectionFailed(let reason):
            return "車両に接続できません: \(reason)"
        case .vehicleDataUnavailable:
            return "車両データを取得できません"
        case .commandFailed(let command, let reason):
            return "コマンド「\(command)」の実行に失敗しました: \(reason)"
        // ...
        }
    }

    var recoverySuggestion: String? {
        switch self {
        case .vehicleConnectionFailed:
            return "車両がオンラインであることを確認してください"
        case .locationPermissionDenied:
            return "設定アプリで位置情報の使用を許可してください"
        case .networkUnavailable:
            return "インターネット接続を確認してください"
        // ...
        }
    }
}
```

## Result Type / Result型

### TeslaResult エイリアス

```swift
typealias TeslaResult<T> = Result<T, TeslaError>
```

### 使用例

```swift
protocol VehicleDataProvider {
    func refreshVehicleData() async -> TeslaResult<VehicleData>
    func setDoorLock(_ locked: Bool) async -> TeslaResult<Void>
}
```

## Result Extensions / Result拡張

```swift
extension Result where Failure == TeslaError {
    /// 成功時の値を返す（失敗時はnil）
    var value: Success? {
        switch self {
        case .success(let value): return value
        case .failure: return nil
        }
    }

    /// エラーを返す（成功時はnil）
    var error: TeslaError? {
        switch self {
        case .success: return nil
        case .failure(let error): return error
        }
    }

    /// 成功かどうか
    var isSuccess: Bool {
        if case .success = self { return true }
        return false
    }

    /// 失敗かどうか
    var isFailure: Bool {
        !isSuccess
    }
}
```

## Error Handling Patterns / エラーハンドリングパターン

### 基本パターン

```swift
func loadVehicleData() async {
    let result = await vehicleProvider.refreshVehicleData()

    switch result {
    case .success(let data):
        self.vehicleData = data
    case .failure(let error):
        self.errorMessage = error.localizedDescription
        self.showError = true
    }
}
```

### guard + else

```swift
func lockDoors() async {
    let result = await vehicleProvider.setDoorLock(true)

    guard case .success = result else {
        if case .failure(let error) = result {
            handleError(error)
        }
        return
    }

    // 成功処理
    showSuccessMessage("ドアをロックしました")
}
```

### map / flatMap

```swift
func getFormattedRange() async -> String? {
    let result = await vehicleProvider.refreshVehicleData()

    return result
        .map { "\(Int($0.estimatedRange)) km" }
        .value
}
```

## View Error Handling / Viewでのエラーハンドリング

### State + Alert

```swift
struct TeslaVehicleScreen: View {
    @State private var error: TeslaError?

    var body: some View {
        VStack { /* content */ }
            .alert("エラー", isPresented: .constant(error != nil)) {
                Button("OK") { error = nil }
            } message: {
                VStack {
                    Text(error?.localizedDescription ?? "")
                    if let suggestion = error?.recoverySuggestion {
                        Text(suggestion)
                            .font(.caption)
                    }
                }
            }
    }

    func loadData() async {
        let result = await vehicleProvider.refreshVehicleData()
        if case .failure(let err) = result {
            error = err
        }
    }
}
```

### Error View

```swift
struct TeslaErrorView: View {
    let error: TeslaError
    var onRetry: (() -> Void)?
    var onDismiss: (() -> Void)?

    var body: some View {
        VStack(spacing: 16) {
            Image(systemName: "exclamationmark.triangle.fill")
                .font(.system(size: 48))
                .foregroundStyle(TeslaColors.statusOrange)

            Text(error.localizedDescription ?? "エラーが発生しました")
                .font(TeslaTypography.titleMedium)
                .foregroundStyle(TeslaColors.textPrimary)
                .multilineTextAlignment(.center)

            if let suggestion = error.recoverySuggestion {
                Text(suggestion)
                    .font(TeslaTypography.bodyMedium)
                    .foregroundStyle(TeslaColors.textSecondary)
                    .multilineTextAlignment(.center)
            }

            HStack(spacing: 16) {
                if let onDismiss {
                    Button("閉じる") { onDismiss() }
                        .buttonStyle(TeslaSecondaryButtonStyle())
                }

                if let onRetry {
                    Button("再試行") { onRetry() }
                        .buttonStyle(TeslaPrimaryButtonStyle())
                }
            }
        }
        .padding(32)
        .teslaCard()
    }
}
```

## Async Error Handling / 非同期エラーハンドリング

### Task + catch

```swift
func performAction() {
    Task {
        do {
            let result = await vehicleProvider.setDoorLock(true)
            switch result {
            case .success:
                await MainActor.run {
                    showSuccess = true
                }
            case .failure(let error):
                await MainActor.run {
                    self.error = error
                }
            }
        }
    }
}
```

### TaskGroup

```swift
func performMultipleActions() async -> [TeslaError] {
    var errors: [TeslaError] = []

    await withTaskGroup(of: TeslaResult<Void>.self) { group in
        group.addTask {
            await self.vehicleProvider.setClimateControl(true)
        }
        group.addTask {
            await self.vehicleProvider.setDoorLock(true)
        }

        for await result in group {
            if case .failure(let error) = result {
                errors.append(error)
            }
        }
    }

    return errors
}
```

## Error Conversion / エラー変換

### 標準ErrorからTeslaErrorへ

```swift
extension TeslaError {
    static func from(_ error: Error) -> TeslaError {
        if let teslaError = error as? TeslaError {
            return teslaError
        }

        let nsError = error as NSError

        // URLError
        if nsError.domain == NSURLErrorDomain {
            switch nsError.code {
            case NSURLErrorNotConnectedToInternet:
                return .networkUnavailable
            case NSURLErrorTimedOut:
                return .timeout
            default:
                return .unknown(underlying: error)
            }
        }

        return .unknown(underlying: error)
    }
}
```

### 使用例

```swift
do {
    let data = try await fetchData()
} catch {
    let teslaError = TeslaError.from(error)
    handleError(teslaError)
}
```

## Logging / ログ出力

```swift
import os

extension TeslaError {
    private static let logger = Logger(
        subsystem: "com.tesla.dashboard",
        category: "Error"
    )

    func log() {
        TeslaError.logger.error("\(self.localizedDescription ?? "Unknown error")")

        if case .unknown(let underlying) = self, let error = underlying {
            TeslaError.logger.debug("Underlying: \(error.localizedDescription)")
        }
    }
}
```

## Best Practices / ベストプラクティス

### 1. 具体的なエラーを使用

```swift
// ✅ Good
return .failure(.vehicleConnectionFailed(reason: "Bluetooth未接続"))

// ❌ Bad
return .failure(.unknown(underlying: nil))
```

### 2. リカバリー提案を提供

```swift
var recoverySuggestion: String? {
    switch self {
    case .networkUnavailable:
        return "インターネット接続を確認してください"
    // ...
    }
}
```

### 3. エラーをログに記録

```swift
func handleError(_ error: TeslaError) {
    error.log()
    showErrorAlert(error)
}
```

### 4. ユーザーフレンドリーなメッセージ

```swift
// ✅ Good
"車両に接続できません。Bluetooth接続を確認してください。"

// ❌ Bad
"Error: Connection failed with code -1001"
```

## Related Documents / 関連ドキュメント

- [Vehicle Data Provider](../examples/models/vehicle-data-provider.swift)
- [SwiftData Models](./swiftdata-models.md)
