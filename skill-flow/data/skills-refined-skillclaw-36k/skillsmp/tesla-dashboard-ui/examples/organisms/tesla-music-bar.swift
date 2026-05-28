// Tesla Dashboard UI - Music Bar
// メディアプレーヤーバー
// AVFoundation + MPRemoteCommandCenter 完全対応

import SwiftUI
import AVFoundation
import MediaPlayer

// MARK: - Tesla Music Bar

/// Tesla風ミュージックバー
/// 現在再生中の曲情報とコントロール
struct TeslaMusicBar: View {
    // MARK: - Properties

    @ObservedObject var player: TeslaMusicPlayer
    var onExpand: (() -> Void)? = nil

    // MARK: - Environment

    @Environment(\.teslaTheme) private var theme
    @Environment(\.accessibilityReduceMotion) private var reduceMotion

    // MARK: - Body

    var body: some View {
        HStack(spacing: 16) {
            // Album Art
            albumArtView

            // Track Info
            trackInfoView

            Spacer()

            // Controls
            controlsView
        }
        .padding(16)
        .teslaGlassmorphism()
        .onTapGesture {
            onExpand?()
        }
        .accessibilityElement(children: .combine)
        .accessibilityLabel(accessibilityLabel)
        .accessibilityHint("ダブルタップで展開")
    }

    // MARK: - Album Art

    private var albumArtView: some View {
        Group {
            if let artwork = player.currentTrack?.artwork {
                Image(uiImage: artwork)
                    .resizable()
                    .aspectRatio(contentMode: .fill)
            } else {
                ZStack {
                    RoundedRectangle(cornerRadius: 8)
                        .fill(TeslaColors.glassBackground)

                    Image(systemName: "music.note")
                        .font(.system(size: 24))
                        .foregroundStyle(TeslaColors.textTertiary)
                }
            }
        }
        .frame(width: 56, height: 56)
        .clipShape(RoundedRectangle(cornerRadius: 8))
    }

    // MARK: - Track Info

    private var trackInfoView: some View {
        VStack(alignment: .leading, spacing: 4) {
            // Track Title
            Text(player.currentTrack?.title ?? "再生停止中")
                .font(TeslaTypography.titleSmall)
                .foregroundStyle(TeslaColors.textPrimary)
                .lineLimit(1)

            // Artist
            Text(player.currentTrack?.artist ?? "---")
                .font(TeslaTypography.labelMedium)
                .foregroundStyle(TeslaColors.textSecondary)
                .lineLimit(1)

            // Progress
            if player.isPlaying {
                progressView
            }
        }
    }

    // MARK: - Progress View

    private var progressView: some View {
        GeometryReader { geometry in
            ZStack(alignment: .leading) {
                // Background
                RoundedRectangle(cornerRadius: 2)
                    .fill(TeslaColors.glassBackground)

                // Progress
                RoundedRectangle(cornerRadius: 2)
                    .fill(TeslaColors.accent)
                    .frame(width: geometry.size.width * player.progress)
            }
        }
        .frame(height: 4)
    }

    // MARK: - Controls

    private var controlsView: some View {
        HStack(spacing: 20) {
            // Previous
            Button {
                player.previousTrack()
            } label: {
                Image(systemName: "backward.fill")
                    .font(.system(size: 16))
                    .foregroundStyle(TeslaColors.textSecondary)
            }
            .buttonStyle(TeslaScaleButtonStyle())

            // Play/Pause
            Button {
                player.togglePlayPause()
            } label: {
                Image(systemName: player.isPlaying ? "pause.fill" : "play.fill")
                    .font(.system(size: 24))
                    .foregroundStyle(TeslaColors.textPrimary)
                    .frame(width: 44, height: 44)
                    .background(TeslaColors.glassBackground)
                    .clipShape(Circle())
            }
            .buttonStyle(TeslaScaleButtonStyle())

            // Next
            Button {
                player.nextTrack()
            } label: {
                Image(systemName: "forward.fill")
                    .font(.system(size: 16))
                    .foregroundStyle(TeslaColors.textSecondary)
            }
            .buttonStyle(TeslaScaleButtonStyle())
        }
    }

    // MARK: - Accessibility

    private var accessibilityLabel: String {
        if let track = player.currentTrack {
            let status = player.isPlaying ? "再生中" : "一時停止"
            return "\(track.title) - \(track.artist) \(status)"
        }
        return "再生停止中"
    }
}

// MARK: - Tesla Music Player

/// 音楽プレーヤー管理クラス
/// AVFoundation + MPRemoteCommandCenter 統合
@MainActor
final class TeslaMusicPlayer: ObservableObject {
    // MARK: - Published Properties

    @Published var currentTrack: TeslaTrack?
    @Published var isPlaying: Bool = false
    @Published var progress: Double = 0
    @Published var volume: Double = 0.5

    // MARK: - Private Properties

    private var audioPlayer: AVAudioPlayer?
    private var progressTimer: Timer?

    // MARK: - Initialization

    init() {
        setupRemoteCommandCenter()
        setupAudioSession()
    }

    // MARK: - Audio Session Setup

    private func setupAudioSession() {
        do {
            try AVAudioSession.sharedInstance().setCategory(.playback, mode: .default)
            try AVAudioSession.sharedInstance().setActive(true)
        } catch {
            print("Audio session setup failed: \(error)")
        }
    }

    // MARK: - Remote Command Center Setup

    private func setupRemoteCommandCenter() {
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

        // Next
        commandCenter.nextTrackCommand.addTarget { [weak self] _ in
            self?.nextTrack()
            return .success
        }

        // Previous
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

    // MARK: - Playback Controls

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

    func nextTrack() {
        // Implementation depends on playlist management
        // For demo purposes, just restart current track
        audioPlayer?.currentTime = 0
        play()
    }

    func previousTrack() {
        // Implementation depends on playlist management
        // For demo purposes, just restart current track
        audioPlayer?.currentTime = 0
        play()
    }

    func seek(to time: TimeInterval) {
        audioPlayer?.currentTime = time
        updateProgress()
    }

    func setVolume(_ volume: Double) {
        self.volume = max(0, min(1, volume))
        audioPlayer?.volume = Float(self.volume)
    }

    // MARK: - Track Loading

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

    // MARK: - Progress Timer

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

    // MARK: - Now Playing Info

    private func updateNowPlayingInfo() {
        var nowPlayingInfo: [String: Any] = [:]

        if let track = currentTrack {
            nowPlayingInfo[MPMediaItemPropertyTitle] = track.title
            nowPlayingInfo[MPMediaItemPropertyArtist] = track.artist
            nowPlayingInfo[MPMediaItemPropertyAlbumTitle] = track.album

            if let artwork = track.artwork {
                nowPlayingInfo[MPMediaItemPropertyArtwork] = MPMediaItemArtwork(boundsSize: artwork.size) { _ in
                    artwork
                }
            }
        }

        if let player = audioPlayer {
            nowPlayingInfo[MPMediaItemPropertyPlaybackDuration] = player.duration
            nowPlayingInfo[MPNowPlayingInfoPropertyElapsedPlaybackTime] = player.currentTime
            nowPlayingInfo[MPNowPlayingInfoPropertyPlaybackRate] = isPlaying ? 1.0 : 0.0
        }

        MPNowPlayingInfoCenter.default().nowPlayingInfo = nowPlayingInfo
    }
}

// MARK: - Tesla Track

/// トラック情報
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

// MARK: - Expanded Music View

/// 展開された音楽プレーヤービュー
struct TeslaExpandedMusicView: View {
    @ObservedObject var player: TeslaMusicPlayer
    @Binding var isExpanded: Bool

    var body: some View {
        VStack(spacing: 32) {
            // Header
            HStack {
                Text("再生中")
                    .font(TeslaTypography.titleMedium)
                    .foregroundStyle(TeslaColors.textPrimary)

                Spacer()

                Button {
                    withAnimation(TeslaAnimation.standard) {
                        isExpanded = false
                    }
                } label: {
                    Image(systemName: "chevron.down")
                        .font(.system(size: 16, weight: .semibold))
                        .foregroundStyle(TeslaColors.textSecondary)
                        .frame(width: 36, height: 36)
                        .background(TeslaColors.glassBackground)
                        .clipShape(Circle())
                }
            }

            // Large Album Art
            Group {
                if let artwork = player.currentTrack?.artwork {
                    Image(uiImage: artwork)
                        .resizable()
                        .aspectRatio(contentMode: .fill)
                } else {
                    ZStack {
                        RoundedRectangle(cornerRadius: 16)
                            .fill(TeslaColors.glassBackground)

                        Image(systemName: "music.note")
                            .font(.system(size: 64))
                            .foregroundStyle(TeslaColors.textTertiary)
                    }
                }
            }
            .frame(width: 280, height: 280)
            .clipShape(RoundedRectangle(cornerRadius: 16))
            .shadow(color: .black.opacity(0.3), radius: 20, y: 10)

            // Track Info
            VStack(spacing: 8) {
                Text(player.currentTrack?.title ?? "再生停止中")
                    .font(TeslaTypography.headlineMedium)
                    .foregroundStyle(TeslaColors.textPrimary)

                Text(player.currentTrack?.artist ?? "---")
                    .font(TeslaTypography.titleMedium)
                    .foregroundStyle(TeslaColors.textSecondary)
            }

            // Progress Slider
            VStack(spacing: 8) {
                TeslaSlider(
                    value: Binding(
                        get: { player.progress },
                        set: { newValue in
                            if let duration = player.audioPlayer?.duration {
                                player.seek(to: duration * newValue)
                            }
                        }
                    ),
                    showValue: false
                )

                HStack {
                    Text(formatTime(player.audioPlayer?.currentTime ?? 0))
                        .font(TeslaTypography.labelSmall)
                        .foregroundStyle(TeslaColors.textTertiary)

                    Spacer()

                    Text(formatTime(player.audioPlayer?.duration ?? 0))
                        .font(TeslaTypography.labelSmall)
                        .foregroundStyle(TeslaColors.textTertiary)
                }
            }

            // Large Controls
            HStack(spacing: 40) {
                Button {
                    player.previousTrack()
                } label: {
                    Image(systemName: "backward.fill")
                        .font(.system(size: 28))
                        .foregroundStyle(TeslaColors.textSecondary)
                }

                Button {
                    player.togglePlayPause()
                } label: {
                    Image(systemName: player.isPlaying ? "pause.fill" : "play.fill")
                        .font(.system(size: 36))
                        .foregroundStyle(.white)
                        .frame(width: 72, height: 72)
                        .background(TeslaColors.accent)
                        .clipShape(Circle())
                }

                Button {
                    player.nextTrack()
                } label: {
                    Image(systemName: "forward.fill")
                        .font(.system(size: 28))
                        .foregroundStyle(TeslaColors.textSecondary)
                }
            }

            // Volume
            TeslaSlider(volume: Binding(
                get: { player.volume },
                set: { player.setVolume($0) }
            ))
        }
        .padding(32)
        .background(TeslaColors.surface)
    }

    private func formatTime(_ seconds: TimeInterval) -> String {
        let minutes = Int(seconds) / 60
        let secs = Int(seconds) % 60
        return String(format: "%d:%02d", minutes, secs)
    }
}

// MARK: - Preview

#Preview("Tesla Music Bar") {
    struct MusicBarPreview: View {
        @StateObject private var player = TeslaMusicPlayer()
        @State private var isExpanded = false

        var body: some View {
            ZStack {
                VStack {
                    Spacer()

                    TeslaMusicBar(player: player) {
                        withAnimation(TeslaAnimation.standard) {
                            isExpanded = true
                        }
                    }
                    .padding(24)
                }

                if isExpanded {
                    TeslaExpandedMusicView(player: player, isExpanded: $isExpanded)
                        .transition(.move(edge: .bottom))
                }
            }
            .background(TeslaColors.background)
            .onAppear {
                player.currentTrack = TeslaTrack(
                    title: "Bohemian Rhapsody",
                    artist: "Queen",
                    album: "A Night at the Opera"
                )
                player.isPlaying = true
                player.progress = 0.35
            }
        }
    }

    return MusicBarPreview()
}
