// Tesla Dashboard UI - Icons
// SF Symbols + カスタムアイコン定義
// 20種類以上のダッシュボード向けアイコン

import SwiftUI

// MARK: - Tesla Icons

/// Tesla Dashboard UI で使用するアイコン定義
/// SF Symbols をベースに、用途に応じたアイコンを提供
enum TeslaIcon: String, CaseIterable, Sendable {

    // MARK: - Navigation

    /// ナビゲーション（位置情報）
    case navigation = "location.fill"

    /// 自宅
    case home = "house.fill"

    /// 職場
    case work = "briefcase.fill"

    /// 検索
    case search = "magnifyingglass"

    /// 地図
    case map = "map.fill"

    /// ルート
    case route = "arrow.triangle.turn.up.right.diamond.fill"

    // MARK: - Vehicle

    /// 車両
    case car = "car.fill"

    /// 車両（上面図）
    case carTop = "car.top.door.front.left.and.front.right.open"

    /// ドア
    case door = "door.left.hand.open"

    /// トランク
    case trunk = "car.rear.fill"

    /// フランク（前部トランク）
    case frunk = "car.front.waves.up"

    /// ロック
    case lock = "lock.fill"

    /// アンロック
    case unlock = "lock.open.fill"

    // MARK: - Climate

    /// 空調
    case climate = "thermometer.medium"

    /// 温度上昇
    case temperatureUp = "thermometer.sun.fill"

    /// 温度下降
    case temperatureDown = "thermometer.snowflake"

    /// ファン
    case fan = "fan.fill"

    /// シートヒーター
    case seatHeater = "carseat.left.fill"

    /// デフロスター
    case defrost = "defroster.fill"

    // MARK: - Energy

    /// バッテリー
    case battery = "battery.100"

    /// 充電
    case charging = "bolt.fill"

    /// エネルギー
    case energy = "leaf.fill"

    /// 航続距離
    case range = "gauge.with.dots.needle.bottom.50percent"

    // MARK: - Media

    /// 音楽
    case music = "music.note"

    /// ラジオ
    case radio = "radio.fill"

    /// ポッドキャスト
    case podcast = "mic.fill"

    /// Bluetooth
    case bluetooth = "antenna.radiowaves.left.and.right"

    /// 再生
    case play = "play.fill"

    /// 一時停止
    case pause = "pause.fill"

    /// 次へ
    case next = "forward.fill"

    /// 前へ
    case previous = "backward.fill"

    /// 音量
    case volume = "speaker.wave.2.fill"

    // MARK: - Controls

    /// カメラ
    case camera = "camera.fill"

    /// ライト
    case light = "flashlight.on.fill"

    /// ハザード
    case hazard = "exclamationmark.triangle.fill"

    /// 設定
    case settings = "gearshape.fill"

    /// 電話
    case phone = "phone.fill"

    /// カレンダー
    case calendar = "calendar"

    /// 情報
    case info = "info.circle.fill"

    // MARK: - Drive Mode

    /// コンフォートモード
    case comfortMode = "leaf.circle.fill"

    /// スポーツモード
    case sportMode = "flame.circle.fill"

    // MARK: - Status

    /// チェックマーク
    case checkmark = "checkmark.circle.fill"

    /// 警告
    case warning = "exclamationmark.circle.fill"

    /// エラー
    case error = "xmark.circle.fill"

    /// 接続済み
    case connected = "wifi"

    /// 切断
    case disconnected = "wifi.slash"

    // MARK: - UI

    /// 展開
    case expand = "chevron.up"

    /// 折りたたみ
    case collapse = "chevron.down"

    /// 右矢印
    case chevronRight = "chevron.right"

    /// 左矢印
    case chevronLeft = "chevron.left"

    /// 閉じる
    case close = "xmark"

    /// メニュー
    case menu = "line.3.horizontal"

    // MARK: - Properties

    /// SF Symbols のシステム名
    var systemName: String { rawValue }
}

// MARK: - Tesla Icon View

/// Teslaアイコンを表示するビュー
struct TeslaIconView: View {
    let icon: TeslaIcon
    var size: CGFloat = 24
    var color: Color = TeslaColors.textPrimary

    var body: some View {
        Image(systemName: icon.systemName)
            .font(.system(size: size))
            .foregroundStyle(color)
    }
}

// MARK: - Icon Group

/// アイコンのカテゴリグループ
enum TeslaIconGroup: String, CaseIterable {
    case navigation = "Navigation"
    case vehicle = "Vehicle"
    case climate = "Climate"
    case energy = "Energy"
    case media = "Media"
    case controls = "Controls"
    case driveMode = "Drive Mode"
    case status = "Status"
    case ui = "UI"

    /// グループに属するアイコン
    var icons: [TeslaIcon] {
        switch self {
        case .navigation:
            return [.navigation, .home, .work, .search, .map, .route]
        case .vehicle:
            return [.car, .carTop, .door, .trunk, .frunk, .lock, .unlock]
        case .climate:
            return [.climate, .temperatureUp, .temperatureDown, .fan, .seatHeater, .defrost]
        case .energy:
            return [.battery, .charging, .energy, .range]
        case .media:
            return [.music, .radio, .podcast, .bluetooth, .play, .pause, .next, .previous, .volume]
        case .controls:
            return [.camera, .light, .hazard, .settings, .phone, .calendar, .info]
        case .driveMode:
            return [.comfortMode, .sportMode]
        case .status:
            return [.checkmark, .warning, .error, .connected, .disconnected]
        case .ui:
            return [.expand, .collapse, .chevronRight, .chevronLeft, .close, .menu]
        }
    }
}

// MARK: - Icon Extensions

extension TeslaIcon {
    /// アイコンのローカライズされたラベル（アクセシビリティ用）
    var accessibilityLabel: String {
        switch self {
        case .navigation: return "ナビゲーション"
        case .home: return "自宅"
        case .work: return "職場"
        case .search: return "検索"
        case .map: return "地図"
        case .route: return "ルート"
        case .car: return "車両"
        case .carTop: return "車両上面図"
        case .door: return "ドア"
        case .trunk: return "トランク"
        case .frunk: return "フランク"
        case .lock: return "ロック"
        case .unlock: return "アンロック"
        case .climate: return "空調"
        case .temperatureUp: return "温度上昇"
        case .temperatureDown: return "温度下降"
        case .fan: return "ファン"
        case .seatHeater: return "シートヒーター"
        case .defrost: return "デフロスター"
        case .battery: return "バッテリー"
        case .charging: return "充電"
        case .energy: return "エネルギー"
        case .range: return "航続距離"
        case .music: return "音楽"
        case .radio: return "ラジオ"
        case .podcast: return "ポッドキャスト"
        case .bluetooth: return "Bluetooth"
        case .play: return "再生"
        case .pause: return "一時停止"
        case .next: return "次へ"
        case .previous: return "前へ"
        case .volume: return "音量"
        case .camera: return "カメラ"
        case .light: return "ライト"
        case .hazard: return "ハザード"
        case .settings: return "設定"
        case .phone: return "電話"
        case .calendar: return "カレンダー"
        case .info: return "情報"
        case .comfortMode: return "コンフォートモード"
        case .sportMode: return "スポーツモード"
        case .checkmark: return "完了"
        case .warning: return "警告"
        case .error: return "エラー"
        case .connected: return "接続済み"
        case .disconnected: return "切断"
        case .expand: return "展開"
        case .collapse: return "折りたたみ"
        case .chevronRight: return "右"
        case .chevronLeft: return "左"
        case .close: return "閉じる"
        case .menu: return "メニュー"
        }
    }
}

// MARK: - Preview

#Preview("Tesla Icons") {
    ScrollView {
        VStack(alignment: .leading, spacing: 24) {
            ForEach(TeslaIconGroup.allCases, id: \.self) { group in
                VStack(alignment: .leading, spacing: 12) {
                    Text(group.rawValue)
                        .font(TeslaTypography.headlineSmall)
                        .foregroundStyle(TeslaColors.textPrimary)

                    LazyVGrid(columns: [
                        GridItem(.adaptive(minimum: 60))
                    ], spacing: 16) {
                        ForEach(group.icons, id: \.self) { icon in
                            VStack(spacing: 8) {
                                TeslaIconView(icon: icon, size: 24)

                                Text(icon.accessibilityLabel)
                                    .font(TeslaTypography.labelSmall)
                                    .foregroundStyle(TeslaColors.textSecondary)
                                    .lineLimit(1)
                                    .minimumScaleFactor(0.8)
                            }
                            .frame(width: 60)
                        }
                    }
                }

                if group != TeslaIconGroup.allCases.last {
                    Divider()
                        .background(TeslaColors.glassBorder)
                }
            }
        }
        .padding(24)
    }
    .background(TeslaColors.background)
}
