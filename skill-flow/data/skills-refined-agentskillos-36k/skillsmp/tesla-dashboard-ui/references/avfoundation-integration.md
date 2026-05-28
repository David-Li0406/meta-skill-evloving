# AVFoundation Integration / AVFoundation統合

Tesla Dashboard UIのAVFoundation統合とMPRemoteCommandCenterについて解説します。

## Overview / 概要

AVFoundation + MPRemoteCommandCenter を使用した完全な音楽プレーヤーシステムです。

## Audio Session / オーディオセッション

### 基本設定

```swift
import AVFoundation

func setupAudioSession() {
    do {
        try AVAudioSession.sharedInstance().setCategory(.playback, mode: .default)
        try AVAudioSession.sharedInstance().setActive(true)
    } catch {
        print("Audio session setup failed: \(error)")
    }
}
```

### カテゴリオプション

```swift
// 他のアプリと混合
try AVAudioSession.sharedInstance().setCategory(
    .playback,
    mode: .default,
    options: [.mixWithOthers]
)

// Bluetoothヘッドフォン対応
try AVAudioSession.sharedInstance().setCategory(
    .playback,
    mode: .default,
    options: [.allowBluetooth, .allowBluetoothA2DP]
)
```

### インタラプション処理

```swift
NotificationCenter.default.addObserver(
    forName: AVAudioSession.interruptionNotification,
    object: nil,
    queue: .main
) { notification in
    guard let userInfo = notification.userInfo,
          let typeValue = userInfo[AVAudioSessionInterruptionTypeKey] as? UInt,
          let type = AVAudioSession.InterruptionType(rawValue: typeValue) else {
        return
    }

    switch type {
    case .began:
        // 一時停止
        player.pause()
    case .ended:
        guard let optionsValue = userInfo[AVAudioSessionInterruptionOptionKey] as? UInt else { return }
        let options = AVAudioSession.InterruptionOptions(rawValue: optionsValue)
        if options.contains(.shouldResume) {
            player.play()
        }
    @unknown default:
        break
    }
}
```

## AVAudioPlayer / オーディオプレーヤー

### 基本実装

```swift
@MainActor
final class TeslaMusicPlayer: ObservableObject {
    @Published var currentTrack: TeslaTrack?
    @Published var isPlaying: Bool = false
    @Published var progress: Double = 0
    @Published var volume: Double = 0.5

    private var audioPlayer: AVAudioPlayer?
    private var progressTimer: Timer?

    func loadTrack(_ track: TeslaTrack) {
        currentTrack = track
        progress = 0

        guard let url = track.url else { return }

        do {
            audioPlayer = try AVAudioPlayer(contentsOf: url)
            audioPlayer?.prepareToPlay()
            audioPlayer?.volume = Float(volume)
        } catch {
            print("Failed to load track: \(error)")
        }

        updateNowPlayingInfo()
    }

    func play() {
        audioPlayer?.play()
        isPlaying = true
        startProgressTimer()
        updateNowPlayingInfo()
    }

    func pause() {
        audioPlayer?.pause()
        isPlaying = false
        stopProgressTimer()
        updateNowPlayingInfo()
    }

    func togglePlayPause() {
        if isPlaying {
            pause()
        } else {
            play()
        }
    }
}
```

### シーク

```swift
func seek(to time: TimeInterval) {
    audioPlayer?.currentTime = time
    updateProgress()
}

func seek(toProgress progress: Double) {
    guard let duration = audioPlayer?.duration else { return }
    let time = duration * progress
    seek(to: time)
}
```

### 音量コントロール

```swift
func setVolume(_ volume: Double) {
    self.volume = max(0, min(1, volume))
    audioPlayer?.volume = Float(self.volume)
}
```

## Progress Timer / 進行タイマー

```swift
private func startProgressTimer() {
    progressTimer = Timer.scheduledTimer(withTimeInterval: 0.1, repeats: true) { [weak self] _ in
        Task { @MainActor in
            self?.updateProgress()
        }
    }
}

private func stopProgressTimer() {
    progressTimer?.invalidate()
    progressTimer = nil
}

private func updateProgress() {
    guard let player = audioPlayer, player.duration > 0 else {
        progress = 0
        return
    }
    progress = player.currentTime / player.duration
}
```

## MPRemoteCommandCenter / リモートコマンドセンター

### 基本設定

```swift
import MediaPlayer

func setupRemoteCommandCenter() {
    let commandCenter = MPRemoteCommandCenter.shared()

    // Play
    commandCenter.playCommand.addTarget { [weak self] _ in
        self?.play()
        return .success
    }

    // Pause
    commandCenter.pauseCommand.addTarget { [weak self] _ in
        self?.pause()
        return .success
    }

    // Toggle Play/Pause
    commandCenter.togglePlayPauseCommand.addTarget { [weak self] _ in
        self?.togglePlayPause()
        return .success
    }

    // Next Track
    commandCenter.nextTrackCommand.addTarget { [weak self] _ in
        self?.nextTrack()
        return .success
    }

    // Previous Track
    commandCenter.previousTrackCommand.addTarget { [weak self] _ in
        self?.previousTrack()
        return .success
    }

    // Seek
    commandCenter.changePlaybackPositionCommand.addTarget { [weak self] event in
        guard let event = event as? MPChangePlaybackPositionCommandEvent else {
            return .commandFailed
        }
        self?.seek(to: event.positionTime)
        return .success
    }
}
```

### コマンドの有効/無効

```swift
// 無効化
commandCenter.nextTrackCommand.isEnabled = false

// 有効化
commandCenter.nextTrackCommand.isEnabled = true
```

## Now Playing Info / Now Playing情報

### 基本設定

```swift
private func updateNowPlayingInfo() {
    var nowPlayingInfo: [String: Any] = [:]

    if let track = currentTrack {
        nowPlayingInfo[MPMediaItemPropertyTitle] = track.title
        nowPlayingInfo[MPMediaItemPropertyArtist] = track.artist
        nowPlayingInfo[MPMediaItemPropertyAlbumTitle] = track.album

        if let artwork = track.artwork {
            nowPlayingInfo[MPMediaItemPropertyArtwork] = MPMediaItemArtwork(
                boundsSize: artwork.size
            ) { _ in artwork }
        }
    }

    if let player = audioPlayer {
        nowPlayingInfo[MPMediaItemPropertyPlaybackDuration] = player.duration
        nowPlayingInfo[MPNowPlayingInfoPropertyElapsedPlaybackTime] = player.currentTime
        nowPlayingInfo[MPNowPlayingInfoPropertyPlaybackRate] = isPlaying ? 1.0 : 0.0
    }

    MPNowPlayingInfoCenter.default().nowPlayingInfo = nowPlayingInfo
}
```

### 再生位置の更新

```swift
// プログレスバー操作後に呼び出し
func updateNowPlayingPosition() {
    guard var nowPlayingInfo = MPNowPlayingInfoCenter.default().nowPlayingInfo else { return }
    nowPlayingInfo[MPNowPlayingInfoPropertyElapsedPlaybackTime] = audioPlayer?.currentTime
    MPNowPlayingInfoCenter.default().nowPlayingInfo = nowPlayingInfo
}
```

## Track Model / トラックモデル

```swift
struct TeslaTrack: Identifiable, Equatable {
    let id: String
    let title: String
    let artist: String
    let album: String?
    let artwork: UIImage?
    let url: URL?
    let duration: TimeInterval

    init(
        id: String = UUID().uuidString,
        title: String,
        artist: String,
        album: String? = nil,
        artwork: UIImage? = nil,
        url: URL? = nil,
        duration: TimeInterval = 0
    ) {
        self.id = id
        self.title = title
        self.artist = artist
        self.album = album
        self.artwork = artwork
        self.url = url
        self.duration = duration
    }

    static func == (lhs: TeslaTrack, rhs: TeslaTrack) -> Bool {
        lhs.id == rhs.id
    }
}
```

## Playlist Management / プレイリスト管理

```swift
@MainActor
final class TeslaMusicPlayer: ObservableObject {
    @Published var playlist: [TeslaTrack] = []
    @Published var currentIndex: Int = 0

    func nextTrack() {
        guard !playlist.isEmpty else { return }
        currentIndex = (currentIndex + 1) % playlist.count
        loadTrack(playlist[currentIndex])
        play()
    }

    func previousTrack() {
        guard !playlist.isEmpty else { return }
        currentIndex = (currentIndex - 1 + playlist.count) % playlist.count
        loadTrack(playlist[currentIndex])
        play()
    }

    func playTrack(at index: Int) {
        guard index >= 0 && index < playlist.count else { return }
        currentIndex = index
        loadTrack(playlist[currentIndex])
        play()
    }
}
```

## Shuffle & Repeat / シャッフル&リピート

```swift
enum RepeatMode {
    case off
    case all
    case one
}

@MainActor
final class TeslaMusicPlayer: ObservableObject {
    @Published var isShuffled: Bool = false
    @Published var repeatMode: RepeatMode = .off

    private var originalPlaylist: [TeslaTrack] = []

    func toggleShuffle() {
        isShuffled.toggle()

        if isShuffled {
            originalPlaylist = playlist
            playlist.shuffle()
        } else {
            playlist = originalPlaylist
        }
    }

    func cycleRepeatMode() {
        switch repeatMode {
        case .off: repeatMode = .all
        case .all: repeatMode = .one
        case .one: repeatMode = .off
        }
    }

    func handleTrackEnded() {
        switch repeatMode {
        case .off:
            if currentIndex < playlist.count - 1 {
                nextTrack()
            } else {
                pause()
            }
        case .all:
            nextTrack()
        case .one:
            seek(to: 0)
            play()
        }
    }
}
```

## Background Audio / バックグラウンド再生

### Info.plist 設定

```xml
<key>UIBackgroundModes</key>
<array>
    <string>audio</string>
</array>
```

### バックグラウンド対応

```swift
func setupBackgroundAudio() {
    do {
        try AVAudioSession.sharedInstance().setCategory(
            .playback,
            mode: .default,
            options: []
        )
        try AVAudioSession.sharedInstance().setActive(true)
    } catch {
        print("Failed to setup background audio: \(error)")
    }
}
```

## Error Handling / エラーハンドリング

```swift
enum MediaError: LocalizedError {
    case loadFailed(reason: String)
    case playbackFailed(reason: String)
    case sessionSetupFailed

    var errorDescription: String? {
        switch self {
        case .loadFailed(let reason):
            return "メディアの読み込みに失敗しました: \(reason)"
        case .playbackFailed(let reason):
            return "再生に失敗しました: \(reason)"
        case .sessionSetupFailed:
            return "オーディオセッションの設定に失敗しました"
        }
    }
}
```

## Related Documents / 関連ドキュメント

- [Error Handling](./error-handling.md)
- [MapKit Integration](./mapkit-integration.md)（音声案内）
