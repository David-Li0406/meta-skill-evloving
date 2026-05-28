// Tesla Dashboard UI - Vehicle Data Provider
// 車両データソースの抽象化プロトコル
// モック実装とリアル実装の切り替えに対応

import Foundation
import Combine

// MARK: - Vehicle Data Provider Protocol

/// 車両データプロバイダープロトコル
/// 実際のAPIとモック実装の切り替えに使用
@MainActor
protocol VehicleDataProvider: AnyObject {
    // MARK: - Vehicle Status

    /// 車両データストリーム
    var vehicleDataPublisher: AnyPublisher<VehicleData, Never> { get }

    /// 現在の車両データ
    var currentVehicleData: VehicleData { get }

    /// 車両データを更新
    func refreshVehicleData() async -> TeslaResult<VehicleData>

    // MARK: - Vehicle Commands

    /// ドアをロック/アンロック
    func setDoorLock(_ locked: Bool) async -> TeslaResult<Void>

    /// トランクを開く
    func openTrunk(_ trunk: TrunkType) async -> TeslaResult<Void>

    /// ライトを点滅
    func flashLights() async -> TeslaResult<Void>

    /// クラクションを鳴らす
    func honkHorn() async -> TeslaResult<Void>

    // MARK: - Climate Control

    /// 空調をオン/オフ
    func setClimateControl(_ enabled: Bool) async -> TeslaResult<Void>

    /// 温度を設定
    func setTemperature(_ temperature: Double) async -> TeslaResult<Void>

    /// シートヒーターを設定
    func setSeatHeater(seat: SeatPosition, level: Int) async -> TeslaResult<Void>

    /// デフロスターを設定
    func setDefrost(_ enabled: Bool) async -> TeslaResult<Void>

    // MARK: - Charging

    /// 充電を開始/停止
    func setCharging(_ enabled: Bool) async -> TeslaResult<Void>

    /// 充電上限を設定
    func setChargeLimit(_ percent: Int) async -> TeslaResult<Void>

    /// 充電ポートを開く/閉じる
    func setChargePort(_ open: Bool) async -> TeslaResult<Void>
}

// MARK: - Supporting Types

/// トランクの種類
enum TrunkType: String, Codable {
    case front = "frunk"
    case rear = "trunk"
}

/// シート位置
enum SeatPosition: String, Codable {
    case driverFront = "driver_front"
    case passengerFront = "passenger_front"
    case driverRear = "driver_rear"
    case passengerRear = "passenger_rear"
    case centerRear = "center_rear"
}

/// ドライブモード
enum DriveMode: String, Codable, CaseIterable {
    case comfort = "Comfort"
    case sport = "Sport"

    var displayName: String {
        rawValue
    }

    var icon: TeslaIcon {
        switch self {
        case .comfort: return .car
        case .sport: return .speedometer
        }
    }
}

/// ドア状態
struct DoorStatus: Codable, Equatable {
    var driverFront: Bool = false
    var passengerFront: Bool = false
    var driverRear: Bool = false
    var passengerRear: Bool = false
    var frunk: Bool = false
    var trunk: Bool = false

    var anyOpen: Bool {
        driverFront || passengerFront || driverRear || passengerRear || frunk || trunk
    }

    var openCount: Int {
        [driverFront, passengerFront, driverRear, passengerRear, frunk, trunk]
            .filter { $0 }.count
    }
}

/// 充電状態
enum ChargingState: String, Codable {
    case disconnected = "Disconnected"
    case connected = "Connected"
    case charging = "Charging"
    case complete = "Complete"
    case stopped = "Stopped"

    var isCharging: Bool {
        self == .charging
    }

    var isConnected: Bool {
        self != .disconnected
    }
}

// MARK: - Vehicle Data

/// 車両データ
struct VehicleData: Equatable {
    // Basic Info
    var name: String = "My Tesla"
    var model: String = "Model S"
    var isOnline: Bool = true

    // Status
    var isLocked: Bool = true
    var driveMode: DriveMode = .comfort
    var doors: DoorStatus = DoorStatus()

    // Speed & Range
    var speed: Double = 0 // km/h
    var odometer: Double = 12345 // km
    var estimatedRange: Double = 350 // km

    // Battery & Charging
    var batteryLevel: Int = 80 // %
    var chargingState: ChargingState = .disconnected
    var chargeLimit: Int = 80 // %
    var chargeRate: Double = 0 // kW
    var minutesToFullCharge: Int? = nil

    // Climate
    var isClimateOn: Bool = false
    var interiorTemperature: Double = 22.0 // °C
    var exteriorTemperature: Double = 25.0 // °C
    var targetTemperature: Double = 22.0 // °C
    var isDefrostOn: Bool = false
    var seatHeaterDriver: Int = 0 // 0-3
    var seatHeaterPassenger: Int = 0 // 0-3

    // Location
    var latitude: Double? = nil
    var longitude: Double? = nil
    var heading: Double? = nil

    // Timestamps
    var lastUpdated: Date = Date()
}

// MARK: - Mock Vehicle Data Provider

/// モック車両データプロバイダー
/// プレビューとテスト用
@MainActor
final class MockVehicleDataProvider: VehicleDataProvider {
    // MARK: - Properties

    private let vehicleDataSubject: CurrentValueSubject<VehicleData, Never>

    var vehicleDataPublisher: AnyPublisher<VehicleData, Never> {
        vehicleDataSubject.eraseToAnyPublisher()
    }

    var currentVehicleData: VehicleData {
        vehicleDataSubject.value
    }

    // MARK: - Configuration

    /// シミュレート遅延（秒）
    var simulatedDelay: TimeInterval = 0.5

    /// エラーをシミュレートするか
    var shouldSimulateErrors: Bool = false

    // MARK: - Initialization

    init(initialData: VehicleData = .preview) {
        self.vehicleDataSubject = CurrentValueSubject(initialData)
    }

    // MARK: - Vehicle Status

    func refreshVehicleData() async -> TeslaResult<VehicleData> {
        await simulateNetworkDelay()

        if shouldSimulateErrors {
            return .failure(.vehicleConnectionFailed(reason: "シミュレートエラー"))
        }

        var data = vehicleDataSubject.value
        data.lastUpdated = Date()
        vehicleDataSubject.send(data)

        return .success(data)
    }

    // MARK: - Vehicle Commands

    func setDoorLock(_ locked: Bool) async -> TeslaResult<Void> {
        await simulateNetworkDelay()

        if shouldSimulateErrors {
            return .failure(.commandFailed(command: "door_lock", reason: "シミュレートエラー"))
        }

        var data = vehicleDataSubject.value
        data.isLocked = locked
        vehicleDataSubject.send(data)

        return .success(())
    }

    func openTrunk(_ trunk: TrunkType) async -> TeslaResult<Void> {
        await simulateNetworkDelay()

        if shouldSimulateErrors {
            return .failure(.commandFailed(command: "open_trunk", reason: "シミュレートエラー"))
        }

        var data = vehicleDataSubject.value
        switch trunk {
        case .front:
            data.doors.frunk = true
        case .rear:
            data.doors.trunk = true
        }
        vehicleDataSubject.send(data)

        return .success(())
    }

    func flashLights() async -> TeslaResult<Void> {
        await simulateNetworkDelay()
        return shouldSimulateErrors ? .failure(.commandFailed(command: "flash_lights", reason: "シミュレートエラー")) : .success(())
    }

    func honkHorn() async -> TeslaResult<Void> {
        await simulateNetworkDelay()
        return shouldSimulateErrors ? .failure(.commandFailed(command: "honk_horn", reason: "シミュレートエラー")) : .success(())
    }

    // MARK: - Climate Control

    func setClimateControl(_ enabled: Bool) async -> TeslaResult<Void> {
        await simulateNetworkDelay()

        if shouldSimulateErrors {
            return .failure(.commandFailed(command: "climate", reason: "シミュレートエラー"))
        }

        var data = vehicleDataSubject.value
        data.isClimateOn = enabled
        vehicleDataSubject.send(data)

        return .success(())
    }

    func setTemperature(_ temperature: Double) async -> TeslaResult<Void> {
        await simulateNetworkDelay()

        if shouldSimulateErrors {
            return .failure(.commandFailed(command: "set_temperature", reason: "シミュレートエラー"))
        }

        var data = vehicleDataSubject.value
        data.targetTemperature = temperature
        vehicleDataSubject.send(data)

        return .success(())
    }

    func setSeatHeater(seat: SeatPosition, level: Int) async -> TeslaResult<Void> {
        await simulateNetworkDelay()

        if shouldSimulateErrors {
            return .failure(.commandFailed(command: "seat_heater", reason: "シミュレートエラー"))
        }

        var data = vehicleDataSubject.value
        switch seat {
        case .driverFront:
            data.seatHeaterDriver = level
        case .passengerFront:
            data.seatHeaterPassenger = level
        default:
            break
        }
        vehicleDataSubject.send(data)

        return .success(())
    }

    func setDefrost(_ enabled: Bool) async -> TeslaResult<Void> {
        await simulateNetworkDelay()

        if shouldSimulateErrors {
            return .failure(.commandFailed(command: "defrost", reason: "シミュレートエラー"))
        }

        var data = vehicleDataSubject.value
        data.isDefrostOn = enabled
        vehicleDataSubject.send(data)

        return .success(())
    }

    // MARK: - Charging

    func setCharging(_ enabled: Bool) async -> TeslaResult<Void> {
        await simulateNetworkDelay()

        if shouldSimulateErrors {
            return .failure(.commandFailed(command: "charging", reason: "シミュレートエラー"))
        }

        var data = vehicleDataSubject.value
        data.chargingState = enabled ? .charging : .stopped
        data.chargeRate = enabled ? 11.0 : 0
        vehicleDataSubject.send(data)

        return .success(())
    }

    func setChargeLimit(_ percent: Int) async -> TeslaResult<Void> {
        await simulateNetworkDelay()

        if shouldSimulateErrors {
            return .failure(.commandFailed(command: "charge_limit", reason: "シミュレートエラー"))
        }

        var data = vehicleDataSubject.value
        data.chargeLimit = percent
        vehicleDataSubject.send(data)

        return .success(())
    }

    func setChargePort(_ open: Bool) async -> TeslaResult<Void> {
        await simulateNetworkDelay()
        return shouldSimulateErrors ? .failure(.commandFailed(command: "charge_port", reason: "シミュレートエラー")) : .success(())
    }

    // MARK: - Private Methods

    private func simulateNetworkDelay() async {
        try? await Task.sleep(nanoseconds: UInt64(simulatedDelay * 1_000_000_000))
    }
}

// MARK: - Preview Data

extension VehicleData {
    /// プレビュー用のサンプルデータ
    static var preview: VehicleData {
        VehicleData(
            name: "My Model S",
            model: "Model S",
            isOnline: true,
            isLocked: true,
            driveMode: .comfort,
            doors: DoorStatus(),
            speed: 0,
            odometer: 12345,
            estimatedRange: 350,
            batteryLevel: 80,
            chargingState: .disconnected,
            chargeLimit: 80,
            chargeRate: 0,
            minutesToFullCharge: nil,
            isClimateOn: false,
            interiorTemperature: 22.0,
            exteriorTemperature: 25.0,
            targetTemperature: 22.0,
            isDefrostOn: false,
            seatHeaterDriver: 0,
            seatHeaterPassenger: 0,
            latitude: 35.6812,
            longitude: 139.7671,
            heading: 0,
            lastUpdated: Date()
        )
    }

    /// 充電中のサンプルデータ
    static var chargingPreview: VehicleData {
        var data = preview
        data.batteryLevel = 65
        data.chargingState = .charging
        data.chargeRate = 11.0
        data.minutesToFullCharge = 45
        return data
    }

    /// 走行中のサンプルデータ
    static var drivingPreview: VehicleData {
        var data = preview
        data.speed = 80
        data.driveMode = .sport
        data.batteryLevel = 72
        data.estimatedRange = 280
        return data
    }
}

extension DoorStatus {
    /// ドア開放状態のサンプル
    static var someOpen: DoorStatus {
        var status = DoorStatus()
        status.driverFront = true
        status.trunk = true
        return status
    }
}
