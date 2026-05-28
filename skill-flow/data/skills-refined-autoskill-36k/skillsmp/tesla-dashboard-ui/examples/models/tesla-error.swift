// Tesla Dashboard UI - Error Types
// Result<T, TeslaError> パターン用のエラー定義
// エラーハンドリングとローカライズ対応

import Foundation

// MARK: - Tesla Error

/// Tesla Dashboard UIのエラー型
/// Result<T, TeslaError> パターンで使用
enum TeslaError: LocalizedError {
    // MARK: - Vehicle Errors

    /// 車両接続エラー
    case vehicleConnectionFailed(reason: String)

    /// 車両データ取得エラー
    case vehicleDataUnavailable

    /// コマンド送信エラー
    case commandFailed(command: String, reason: String)

    /// 認証エラー
    case authenticationFailed

    // MARK: - Location Errors

    /// 位置情報権限エラー
    case locationPermissionDenied

    /// 位置情報取得エラー
    case locationUnavailable

    /// ルート検索エラー
    case routeCalculationFailed(reason: String)

    /// ジオコーディングエラー
    case geocodingFailed(address: String)

    // MARK: - Media Errors

    /// メディア再生エラー
    case mediaPlaybackFailed(reason: String)

    /// メディアソース利用不可
    case mediaSourceUnavailable

    // MARK: - Data Errors

    /// データ保存エラー
    case saveFailed(entity: String, reason: String)

    /// データ読み込みエラー
    case loadFailed(entity: String, reason: String)

    /// データ削除エラー
    case deleteFailed(entity: String, reason: String)

    // MARK: - Network Errors

    /// ネットワーク接続エラー
    case networkUnavailable

    /// タイムアウト
    case timeout

    /// サーバーエラー
    case serverError(statusCode: Int)

    // MARK: - General Errors

    /// 不明なエラー
    case unknown(underlying: Error?)

    /// 機能未対応
    case featureNotSupported(feature: String)

    // MARK: - LocalizedError

    var errorDescription: String? {
        switch self {
        case .vehicleConnectionFailed(let reason):
            return "車両に接続できません: \(reason)"
        case .vehicleDataUnavailable:
            return "車両データを取得できません"
        case .commandFailed(let command, let reason):
            return "コマンド「\(command)」の実行に失敗しました: \(reason)"
        case .authenticationFailed:
            return "認証に失敗しました"
        case .locationPermissionDenied:
            return "位置情報の使用が許可されていません"
        case .locationUnavailable:
            return "現在地を取得できません"
        case .routeCalculationFailed(let reason):
            return "ルート検索に失敗しました: \(reason)"
        case .geocodingFailed(let address):
            return "「\(address)」の位置を特定できません"
        case .mediaPlaybackFailed(let reason):
            return "メディアを再生できません: \(reason)"
        case .mediaSourceUnavailable:
            return "メディアソースが利用できません"
        case .saveFailed(let entity, let reason):
            return "\(entity)の保存に失敗しました: \(reason)"
        case .loadFailed(let entity, let reason):
            return "\(entity)の読み込みに失敗しました: \(reason)"
        case .deleteFailed(let entity, let reason):
            return "\(entity)の削除に失敗しました: \(reason)"
        case .networkUnavailable:
            return "ネットワークに接続できません"
        case .timeout:
            return "接続がタイムアウトしました"
        case .serverError(let statusCode):
            return "サーバーエラー（コード: \(statusCode)）"
        case .unknown(let underlying):
            if let error = underlying {
                return "エラーが発生しました: \(error.localizedDescription)"
            }
            return "不明なエラーが発生しました"
        case .featureNotSupported(let feature):
            return "「\(feature)」はこのデバイスでサポートされていません"
        }
    }

    var recoverySuggestion: String? {
        switch self {
        case .vehicleConnectionFailed:
            return "車両がオンラインであることを確認してください"
        case .vehicleDataUnavailable:
            return "しばらくしてから再度お試しください"
        case .commandFailed:
            return "再度お試しください"
        case .authenticationFailed:
            return "ログインし直してください"
        case .locationPermissionDenied:
            return "設定アプリで位置情報の使用を許可してください"
        case .locationUnavailable:
            return "GPSの受信状況を確認してください"
        case .routeCalculationFailed:
            return "目的地を変更するか、再度お試しください"
        case .geocodingFailed:
            return "住所を確認して再度お試しください"
        case .mediaPlaybackFailed:
            return "別のメディアソースをお試しください"
        case .mediaSourceUnavailable:
            return "メディアソースの接続を確認してください"
        case .saveFailed, .loadFailed, .deleteFailed:
            return "ストレージの空き容量を確認してください"
        case .networkUnavailable:
            return "インターネット接続を確認してください"
        case .timeout:
            return "ネットワーク環境を確認して再度お試しください"
        case .serverError:
            return "しばらくしてから再度お試しください"
        case .unknown:
            return "アプリを再起動してください"
        case .featureNotSupported:
            return nil
        }
    }
}

// MARK: - Result Extensions

extension Result where Failure == TeslaError {
    /// 成功時の値を返す（失敗時はnil）
    var value: Success? {
        switch self {
        case .success(let value):
            return value
        case .failure:
            return nil
        }
    }

    /// エラーを返す（成功時はnil）
    var error: TeslaError? {
        switch self {
        case .success:
            return nil
        case .failure(let error):
            return error
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

// MARK: - Async Result Helpers

/// 非同期Result型のエイリアス
typealias TeslaResult<T> = Result<T, TeslaError>

/// 非同期操作の結果型
typealias AsyncTeslaResult<T> = Task<TeslaResult<T>, Never>

// MARK: - Error Conversion

extension TeslaError {
    /// 標準ErrorからTeslaErrorへの変換
    static func from(_ error: Error) -> TeslaError {
        if let teslaError = error as? TeslaError {
            return teslaError
        }

        let nsError = error as NSError

        // URLErrorの変換
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

// MARK: - Preview Helpers

#if DEBUG
extension TeslaError {
    /// プレビュー用のサンプルエラー
    static let previewSamples: [TeslaError] = [
        .vehicleConnectionFailed(reason: "Bluetooth接続失敗"),
        .vehicleDataUnavailable,
        .locationPermissionDenied,
        .networkUnavailable,
        .timeout
    ]
}
#endif
