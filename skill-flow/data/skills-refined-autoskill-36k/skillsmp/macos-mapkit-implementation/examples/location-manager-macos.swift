// MARK: - Location Manager for macOS
// macOS 14+ Core Location 位置情報管理

import SwiftUI
import CoreLocation
import AppKit

// MARK: - macOS用LocationManager

/// macOS向け位置情報マネージャー
@MainActor
@Observable
final class MacOSLocationManager: NSObject, CLLocationManagerDelegate {
    // MARK: - Published Properties

    /// 現在の位置
    var location: CLLocation?

    /// 位置情報の認可状態
    var authorizationStatus: CLAuthorizationStatus = .notDetermined

    /// 精度の認可状態
    var accuracyAuthorization: CLAccuracyAuthorization = .fullAccuracy

    /// 位置情報の更新中かどうか
    var isUpdating = false

    /// エラーメッセージ
    var errorMessage: String?

    // MARK: - Private Properties

    private let manager = CLLocationManager()

    // MARK: - Initialization

    override init() {
        super.init()
        manager.delegate = self
        manager.desiredAccuracy = kCLLocationAccuracyBest
        manager.distanceFilter = 10 // 10メートル移動で更新

        // 初期状態を取得
        authorizationStatus = manager.authorizationStatus
        accuracyAuthorization = manager.accuracyAuthorization
    }

    // MARK: - Public Methods

    /// 位置情報使用の権限をリクエスト
    func requestWhenInUseAuthorization() {
        manager.requestWhenInUseAuthorization()
    }

    /// 位置情報の更新を開始
    func startUpdating() {
        guard isAuthorized else {
            errorMessage = "位置情報の権限がありません"
            return
        }

        isUpdating = true
        errorMessage = nil
        manager.startUpdatingLocation()
    }

    /// 位置情報の更新を停止
    func stopUpdating() {
        isUpdating = false
        manager.stopUpdatingLocation()
    }

    /// 一回だけ位置情報を取得
    func requestLocation() {
        guard isAuthorized else {
            errorMessage = "位置情報の権限がありません"
            return
        }

        errorMessage = nil
        manager.requestLocation()
    }

    /// システム環境設定の位置情報設定を開く
    func openLocationSettings() {
        // macOSのシステム環境設定を開く
        if let url = URL(string: "x-apple.systempreferences:com.apple.preference.security?Privacy_LocationServices") {
            NSWorkspace.shared.open(url)
        }
    }

    // MARK: - Private Helpers

    /// 位置情報が許可されているか
    private var isAuthorized: Bool {
        // macOSでは.authorizedまたは.authorizedAlwaysが返される
        // Note: .authorizedWhenInUseはmacOSでは利用不可
        return authorizationStatus == .authorized ||
               authorizationStatus == .authorizedAlways
    }

    // MARK: - CLLocationManagerDelegate

    nonisolated func locationManager(
        _ manager: CLLocationManager,
        didUpdateLocations locations: [CLLocation]
    ) {
        Task { @MainActor in
            guard let newLocation = locations.last else { return }

            // 精度が十分で、古すぎないデータのみ使用
            if newLocation.horizontalAccuracy >= 0 &&
               newLocation.horizontalAccuracy <= 100 {
                let age = Date().timeIntervalSince(newLocation.timestamp)
                if age < 60 { // 60秒以内のデータ
                    location = newLocation
                    errorMessage = nil
                }
            }
        }
    }

    nonisolated func locationManagerDidChangeAuthorization(_ manager: CLLocationManager) {
        Task { @MainActor in
            authorizationStatus = manager.authorizationStatus
            accuracyAuthorization = manager.accuracyAuthorization

            // macOSでの権限状態に応じた処理
            // Note: .authorizedWhenInUseはmacOSでは利用不可
            switch authorizationStatus {
            case .authorized, .authorizedAlways:
                // 位置情報取得可能
                if isUpdating {
                    manager.startUpdatingLocation()
                }
            case .denied:
                errorMessage = "位置情報へのアクセスが拒否されました。システム環境設定で許可してください。"
                isUpdating = false
            case .restricted:
                errorMessage = "位置情報へのアクセスが制限されています"
                isUpdating = false
            case .notDetermined:
                // まだ権限が求められていない
                break
            @unknown default:
                break
            }
        }
    }

    nonisolated func locationManager(
        _ manager: CLLocationManager,
        didFailWithError error: Error
    ) {
        Task { @MainActor in
            if let clError = error as? CLError {
                switch clError.code {
                case .denied:
                    errorMessage = "位置情報へのアクセスが拒否されました"
                    isUpdating = false
                case .locationUnknown:
                    errorMessage = "位置を特定できません。リトライ中..."
                case .network:
                    errorMessage = "ネットワークエラーが発生しました"
                default:
                    errorMessage = "位置情報エラー: \(clError.localizedDescription)"
                }
            } else {
                errorMessage = error.localizedDescription
            }
        }
    }
}

// MARK: - 使用例View

/// LocationManagerを使用したView
struct MacOSLocationManagerExampleView: View {
    @State private var locationManager = MacOSLocationManager()

    var body: some View {
        VStack(spacing: 20) {
            // 認可状態
            GroupBox("認可状態") {
                HStack {
                    Circle()
                        .fill(authorizationColor)
                        .frame(width: 12, height: 12)
                    Text(authorizationText)
                    Spacer()
                }
            }

            // 現在地情報
            if let location = locationManager.location {
                GroupBox("現在地") {
                    VStack(alignment: .leading, spacing: 8) {
                        LabeledContent("緯度", value: String(format: "%.6f", location.coordinate.latitude))
                        LabeledContent("経度", value: String(format: "%.6f", location.coordinate.longitude))
                        LabeledContent("精度", value: String(format: "%.1fm", location.horizontalAccuracy))
                        LabeledContent("高度", value: String(format: "%.1fm", location.altitude))
                        LabeledContent("更新時刻", value: location.timestamp.formatted(date: .omitted, time: .standard))
                    }
                }
            }

            // エラーメッセージ
            if let error = locationManager.errorMessage {
                GroupBox {
                    HStack {
                        Image(systemName: "exclamationmark.triangle")
                            .foregroundStyle(.orange)
                        Text(error)
                            .foregroundStyle(.secondary)
                        Spacer()
                    }
                }
            }

            Spacer()

            // ボタン
            VStack(spacing: 12) {
                if locationManager.authorizationStatus == .notDetermined {
                    Button("権限をリクエスト") {
                        locationManager.requestWhenInUseAuthorization()
                    }
                    .buttonStyle(.borderedProminent)
                }

                if locationManager.authorizationStatus == .denied {
                    Button("システム環境設定を開く") {
                        locationManager.openLocationSettings()
                    }
                    .buttonStyle(.borderedProminent)
                }

                HStack(spacing: 12) {
                    Button(locationManager.isUpdating ? "停止" : "追跡開始") {
                        if locationManager.isUpdating {
                            locationManager.stopUpdating()
                        } else {
                            locationManager.startUpdating()
                        }
                    }
                    .buttonStyle(.bordered)
                    .disabled(!isAuthorized)

                    Button("一回取得") {
                        locationManager.requestLocation()
                    }
                    .buttonStyle(.bordered)
                    .disabled(!isAuthorized)
                }
            }
        }
        .padding()
        .frame(minWidth: 300)
    }

    private var isAuthorized: Bool {
        // Note: .authorizedWhenInUseはmacOSでは利用不可
        let status = locationManager.authorizationStatus
        return status == .authorized || status == .authorizedAlways
    }

    private var authorizationText: String {
        // Note: .authorizedWhenInUseはmacOSでは利用不可
        switch locationManager.authorizationStatus {
        case .notDetermined: return "未決定"
        case .restricted: return "制限あり"
        case .denied: return "拒否"
        case .authorized, .authorizedAlways: return "許可済み"
        @unknown default: return "不明"
        }
    }

    private var authorizationColor: Color {
        // Note: .authorizedWhenInUseはmacOSでは利用不可
        switch locationManager.authorizationStatus {
        case .authorized, .authorizedAlways: return .green
        case .denied, .restricted: return .red
        default: return .secondary
        }
    }
}

// MARK: - 権限リクエストUI

/// 権限リクエスト前の説明画面
struct MacOSLocationPermissionRequestView: View {
    @State private var locationManager = MacOSLocationManager()
    @Binding var isPresented: Bool

    var body: some View {
        VStack(spacing: 24) {
            Image(systemName: "location.fill")
                .font(.system(size: 60))
                .foregroundStyle(.blue)

            Text("位置情報へのアクセス")
                .font(.title)
                .fontWeight(.bold)

            Text("周辺のスポットを検索したり、現在地から目的地への経路を表示するために、位置情報へのアクセスが必要です。")
                .multilineTextAlignment(.center)
                .foregroundStyle(.secondary)
                .frame(maxWidth: 400)

            VStack(spacing: 16) {
                Button {
                    locationManager.requestWhenInUseAuthorization()
                    isPresented = false
                } label: {
                    Text("許可する")
                        .frame(minWidth: 120)
                }
                .buttonStyle(.borderedProminent)
                .controlSize(.large)

                Button {
                    isPresented = false
                } label: {
                    Text("後で")
                        .frame(minWidth: 120)
                }
                .buttonStyle(.bordered)
                .controlSize(.large)
            }
        }
        .padding(32)
        .frame(width: 500)
    }
}

// MARK: - 権限拒否時のUI

/// 権限が拒否された場合の設定誘導
struct MacOSLocationDeniedView: View {
    @State private var locationManager = MacOSLocationManager()

    var body: some View {
        VStack(spacing: 20) {
            Image(systemName: "location.slash")
                .font(.system(size: 60))
                .foregroundStyle(.secondary)

            Text("位置情報がオフです")
                .font(.title2)
                .fontWeight(.bold)

            Text("この機能を使用するには、システム環境設定で位置情報を有効にしてください。")
                .multilineTextAlignment(.center)
                .foregroundStyle(.secondary)
                .frame(maxWidth: 400)

            VStack(spacing: 8) {
                Button("システム環境設定を開く") {
                    locationManager.openLocationSettings()
                }
                .buttonStyle(.borderedProminent)
                .controlSize(.large)

                Text("「プライバシーとセキュリティ」>「位置情報サービス」でこのアプリを許可してください")
                    .font(.caption)
                    .foregroundStyle(.secondary)
            }
        }
        .padding()
    }
}

// MARK: - Preview

#Preview("Location Manager") {
    MacOSLocationManagerExampleView()
        .frame(width: 400, height: 500)
}

#Preview("Permission Request") {
    MacOSLocationPermissionRequestView(isPresented: .constant(true))
}

#Preview("Location Denied") {
    MacOSLocationDeniedView()
        .frame(width: 500, height: 400)
}
