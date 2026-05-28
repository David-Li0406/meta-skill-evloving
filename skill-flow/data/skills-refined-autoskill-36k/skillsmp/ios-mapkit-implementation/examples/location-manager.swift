// MARK: - Location Manager Example
// iOS 17+ SwiftUI Core Location 位置情報管理

import SwiftUI
import CoreLocation

// MARK: - 基本的なLocationManager

/// 位置情報を管理するシンプルなマネージャー
@MainActor
@Observable
final class LocationManager: NSObject, CLLocationManagerDelegate {
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

    /// 常時位置情報の権限をリクエスト
    func requestAlwaysAuthorization() {
        manager.requestAlwaysAuthorization()
    }

    /// 位置情報の更新を開始
    func startUpdating() {
        guard authorizationStatus == .authorizedWhenInUse ||
              authorizationStatus == .authorizedAlways else {
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
        guard authorizationStatus == .authorizedWhenInUse ||
              authorizationStatus == .authorizedAlways else {
            errorMessage = "位置情報の権限がありません"
            return
        }

        errorMessage = nil
        manager.requestLocation()
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

            // 権限が得られたら更新を開始
            if authorizationStatus == .authorizedWhenInUse ||
               authorizationStatus == .authorizedAlways {
                if isUpdating {
                    manager.startUpdatingLocation()
                }
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

// MARK: - 高度な機能付きLocationManager

/// バックグラウンド更新、ジオフェンス対応のLocationManager
@MainActor
@Observable
final class AdvancedLocationManager: NSObject, CLLocationManagerDelegate {
    // MARK: - Published Properties

    var location: CLLocation?
    var heading: CLHeading?
    var authorizationStatus: CLAuthorizationStatus = .notDetermined
    var isUpdating = false
    var monitoredRegions: Set<CLRegion> = []
    var lastVisit: CLVisit?

    // MARK: - Private Properties

    private let manager = CLLocationManager()
    private var locationContinuation: CheckedContinuation<CLLocation, Error>?

    // MARK: - Initialization

    override init() {
        super.init()
        manager.delegate = self
        manager.desiredAccuracy = kCLLocationAccuracyBest
        manager.distanceFilter = 10
        authorizationStatus = manager.authorizationStatus
    }

    // MARK: - Authorization

    func requestWhenInUseAuthorization() {
        manager.requestWhenInUseAuthorization()
    }

    func requestAlwaysAuthorization() {
        manager.requestAlwaysAuthorization()
    }

    // MARK: - Location Updates

    func startUpdating() {
        isUpdating = true
        manager.startUpdatingLocation()
    }

    func stopUpdating() {
        isUpdating = false
        manager.stopUpdatingLocation()
    }

    /// async/awaitで現在位置を取得
    func getCurrentLocation() async throws -> CLLocation {
        return try await withCheckedThrowingContinuation { continuation in
            locationContinuation = continuation
            manager.requestLocation()
        }
    }

    // MARK: - Heading

    func startUpdatingHeading() {
        guard CLLocationManager.headingAvailable() else { return }
        manager.startUpdatingHeading()
    }

    func stopUpdatingHeading() {
        manager.stopUpdatingHeading()
    }

    // MARK: - Region Monitoring (Geofencing)

    func startMonitoring(region: CLCircularRegion) {
        guard CLLocationManager.isMonitoringAvailable(for: CLCircularRegion.self) else {
            return
        }

        region.notifyOnEntry = true
        region.notifyOnExit = true
        manager.startMonitoring(for: region)
        monitoredRegions.insert(region)
    }

    func stopMonitoring(region: CLRegion) {
        manager.stopMonitoring(for: region)
        monitoredRegions.remove(region)
    }

    // MARK: - Significant Location Changes

    func startMonitoringSignificantLocationChanges() {
        manager.startMonitoringSignificantLocationChanges()
    }

    func stopMonitoringSignificantLocationChanges() {
        manager.stopMonitoringSignificantLocationChanges()
    }

    // MARK: - Visit Monitoring

    func startMonitoringVisits() {
        manager.startMonitoringVisits()
    }

    func stopMonitoringVisits() {
        manager.stopMonitoringVisits()
    }

    // MARK: - Background

    func enableBackgroundUpdates() {
        manager.allowsBackgroundLocationUpdates = true
        manager.showsBackgroundLocationIndicator = true
    }

    func disableBackgroundUpdates() {
        manager.allowsBackgroundLocationUpdates = false
        manager.showsBackgroundLocationIndicator = false
    }

    // MARK: - CLLocationManagerDelegate

    nonisolated func locationManager(
        _ manager: CLLocationManager,
        didUpdateLocations locations: [CLLocation]
    ) {
        Task { @MainActor in
            if let newLocation = locations.last {
                location = newLocation

                // async取得の継続を完了
                if let continuation = locationContinuation {
                    continuation.resume(returning: newLocation)
                    locationContinuation = nil
                }
            }
        }
    }

    nonisolated func locationManager(
        _ manager: CLLocationManager,
        didUpdateHeading newHeading: CLHeading
    ) {
        Task { @MainActor in
            heading = newHeading
        }
    }

    nonisolated func locationManagerDidChangeAuthorization(_ manager: CLLocationManager) {
        Task { @MainActor in
            authorizationStatus = manager.authorizationStatus
        }
    }

    nonisolated func locationManager(
        _ manager: CLLocationManager,
        didFailWithError error: Error
    ) {
        Task { @MainActor in
            if let continuation = locationContinuation {
                continuation.resume(throwing: error)
                locationContinuation = nil
            }
        }
    }

    nonisolated func locationManager(
        _ manager: CLLocationManager,
        didEnterRegion region: CLRegion
    ) {
        Task { @MainActor in
            print("Entered region: \(region.identifier)")
            // 通知を送信するなどの処理
        }
    }

    nonisolated func locationManager(
        _ manager: CLLocationManager,
        didExitRegion region: CLRegion
    ) {
        Task { @MainActor in
            print("Exited region: \(region.identifier)")
        }
    }

    nonisolated func locationManager(
        _ manager: CLLocationManager,
        didVisit visit: CLVisit
    ) {
        Task { @MainActor in
            lastVisit = visit
        }
    }
}

// MARK: - 使用例View

/// LocationManagerを使用したView
struct LocationManagerExampleView: View {
    @State private var locationManager = LocationManager()

    var body: some View {
        VStack(spacing: 20) {
            // 認可状態
            VStack(alignment: .leading) {
                Text("認可状態")
                    .font(.headline)
                Text(authorizationText)
                    .foregroundStyle(authorizationColor)
            }
            .frame(maxWidth: .infinity, alignment: .leading)

            // 現在地情報
            if let location = locationManager.location {
                VStack(alignment: .leading, spacing: 8) {
                    Text("現在地")
                        .font(.headline)
                    Text("緯度: \(location.coordinate.latitude, specifier: "%.6f")")
                    Text("経度: \(location.coordinate.longitude, specifier: "%.6f")")
                    Text("精度: \(location.horizontalAccuracy, specifier: "%.1f")m")
                    Text("高度: \(location.altitude, specifier: "%.1f")m")
                    Text("速度: \(location.speed, specifier: "%.1f")m/s")
                }
                .frame(maxWidth: .infinity, alignment: .leading)
            }

            // エラーメッセージ
            if let error = locationManager.errorMessage {
                Text(error)
                    .foregroundStyle(.red)
                    .font(.caption)
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

                HStack(spacing: 12) {
                    Button(locationManager.isUpdating ? "停止" : "開始") {
                        if locationManager.isUpdating {
                            locationManager.stopUpdating()
                        } else {
                            locationManager.startUpdating()
                        }
                    }
                    .buttonStyle(.bordered)

                    Button("一回取得") {
                        locationManager.requestLocation()
                    }
                    .buttonStyle(.bordered)
                }
            }
        }
        .padding()
        .navigationTitle("位置情報")
    }

    private var authorizationText: String {
        switch locationManager.authorizationStatus {
        case .notDetermined: return "未決定"
        case .restricted: return "制限あり"
        case .denied: return "拒否"
        case .authorizedWhenInUse: return "使用中のみ許可"
        case .authorizedAlways: return "常に許可"
        @unknown default: return "不明"
        }
    }

    private var authorizationColor: Color {
        switch locationManager.authorizationStatus {
        case .authorizedWhenInUse, .authorizedAlways: return .green
        case .denied, .restricted: return .red
        default: return .secondary
        }
    }
}

// MARK: - 権限リクエストUI

/// 権限リクエスト前の説明画面
struct LocationPermissionRequestView: View {
    @State private var locationManager = LocationManager()
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

            VStack(spacing: 16) {
                Button {
                    locationManager.requestWhenInUseAuthorization()
                    isPresented = false
                } label: {
                    Text("許可する")
                        .frame(maxWidth: .infinity)
                }
                .buttonStyle(.borderedProminent)

                Button {
                    isPresented = false
                } label: {
                    Text("後で")
                        .frame(maxWidth: .infinity)
                }
                .buttonStyle(.bordered)
            }
        }
        .padding(32)
    }
}

// MARK: - 権限拒否時のUI

/// 権限が拒否された場合の設定誘導
struct LocationDeniedView: View {
    var body: some View {
        VStack(spacing: 20) {
            Image(systemName: "location.slash")
                .font(.system(size: 60))
                .foregroundStyle(.secondary)

            Text("位置情報がオフです")
                .font(.title2)
                .fontWeight(.bold)

            Text("この機能を使用するには、設定アプリで位置情報を有効にしてください。")
                .multilineTextAlignment(.center)
                .foregroundStyle(.secondary)

            Button("設定を開く") {
                openSettings()
            }
            .buttonStyle(.borderedProminent)
        }
        .padding()
    }

    private func openSettings() {
        #if os(iOS)
        if let url = URL(string: UIApplication.openSettingsURLString) {
            UIApplication.shared.open(url)
        }
        #endif
    }
}

// MARK: - Preview

#Preview("Location Manager") {
    NavigationStack {
        LocationManagerExampleView()
    }
}

#Preview("Permission Request") {
    LocationPermissionRequestView(isPresented: .constant(true))
}

#Preview("Location Denied") {
    LocationDeniedView()
}
