// Tesla Dashboard UI - Media Screen
// メディア画面
// 音楽再生、プレイリスト、ソース選択

import SwiftUI

// MARK: - Tesla Media Screen

/// Tesla風メディア画面
struct TeslaMediaScreen: View {
    // MARK: - Properties

    @ObservedObject var player: TeslaMusicPlayer

    // MARK: - State

    @State private var selectedSource: MediaSource = .streaming
    @State private var showPlaylist: Bool = false
    @State private var showEqualizer: Bool = false

    // MARK: - Environment

    @Environment(\.teslaTheme) private var theme
    @Environment(\.horizontalSizeClass) private var horizontalSizeClass

    // MARK: - Body

    var body: some View {
        GeometryReader { geometry in
            if horizontalSizeClass == .regular {
                // iPad: Split layout
                HStack(spacing: 0) {
                    // Player Section
                    playerSection
                        .frame(width: geometry.size.width * 0.55)

                    // Playlist Section
                    playlistSection
                        .frame(maxWidth: .infinity)
                        .background(TeslaColors.surface)
                }
            } else {
                // iPhone: Stack layout
                ScrollView {
                    VStack(spacing: 24) {
                        playerSection
                        playlistSection
                    }
                    .padding(24)
                }
            }
        }
        .background(TeslaColors.background)
    }

    // MARK: - Player Section

    private var playerSection: some View {
        VStack(spacing: 32) {
            // Source Selector
            sourceSelector

            // Album Art
            albumArtView

            // Track Info
            trackInfoView

            // Progress
            progressSection

            // Controls
            controlsSection

            // Volume
            volumeSection

            Spacer()
        }
        .padding(32)
    }

    // MARK: - Source Selector

    private var sourceSelector: some View {
        ScrollView(.horizontal, showsIndicators: false) {
            HStack(spacing: 12) {
                ForEach(MediaSource.allCases) { source in
                    Button {
                        withAnimation(TeslaAnimation.quick) {
                            selectedSource = source
                        }
                    } label: {
                        HStack(spacing: 8) {
                            Image(systemName: source.iconName)
                                .font(.system(size: 14))

                            Text(source.displayName)
                                .font(TeslaTypography.labelMedium)
                        }
                        .foregroundStyle(selectedSource == source ? .white : TeslaColors.textSecondary)
                        .padding(.horizontal, 16)
                        .padding(.vertical, 10)
                        .background(
                            RoundedRectangle(cornerRadius: 8)
                                .fill(selectedSource == source ? TeslaColors.accent : TeslaColors.glassBackground)
                        )
                    }
                    .buttonStyle(TeslaScaleButtonStyle())
                }
            }
        }
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
                    RoundedRectangle(cornerRadius: 24)
                        .fill(
                            LinearGradient(
                                colors: [TeslaColors.accent.opacity(0.3), TeslaColors.glassBackground],
                                startPoint: .topLeading,
                                endPoint: .bottomTrailing
                            )
                        )

                    Image(systemName: "music.note")
                        .font(.system(size: 80))
                        .foregroundStyle(TeslaColors.textTertiary)
                }
            }
        }
        .frame(width: 280, height: 280)
        .clipShape(RoundedRectangle(cornerRadius: 24))
        .shadow(color: .black.opacity(0.3), radius: 20, y: 10)
        .rotation3DEffect(
            .degrees(player.isPlaying ? 0 : -5),
            axis: (x: 0, y: 1, z: 0)
        )
        .animation(TeslaAnimation.standard, value: player.isPlaying)
    }

    // MARK: - Track Info

    private var trackInfoView: some View {
        VStack(spacing: 8) {
            Text(player.currentTrack?.title ?? "再生停止中")
                .font(TeslaTypography.headlineMedium)
                .foregroundStyle(TeslaColors.textPrimary)
                .lineLimit(1)

            Text(player.currentTrack?.artist ?? "---")
                .font(TeslaTypography.titleMedium)
                .foregroundStyle(TeslaColors.textSecondary)
                .lineLimit(1)

            if let album = player.currentTrack?.album {
                Text(album)
                    .font(TeslaTypography.labelMedium)
                    .foregroundStyle(TeslaColors.textTertiary)
                    .lineLimit(1)
            }
        }
    }

    // MARK: - Progress Section

    private var progressSection: some View {
        VStack(spacing: 8) {
            // Progress Slider
            TeslaSlider(
                value: Binding(
                    get: { player.progress },
                    set: { newValue in
                        // Seek implementation
                    }
                ),
                showValue: false
            )

            // Time Labels
            HStack {
                Text(formatTime(player.progress * (player.currentTrack?.duration ?? 0)))
                    .font(TeslaTypography.labelSmall)
                    .foregroundStyle(TeslaColors.textTertiary)
                    .monospacedDigit()

                Spacer()

                Text("-\(formatTime((1 - player.progress) * (player.currentTrack?.duration ?? 0)))")
                    .font(TeslaTypography.labelSmall)
                    .foregroundStyle(TeslaColors.textTertiary)
                    .monospacedDigit()
            }
        }
    }

    // MARK: - Controls Section

    private var controlsSection: some View {
        HStack(spacing: 32) {
            // Shuffle
            Button {
                // Toggle shuffle
            } label: {
                Image(systemName: "shuffle")
                    .font(.system(size: 18))
                    .foregroundStyle(TeslaColors.textSecondary)
            }

            // Previous
            Button {
                player.previousTrack()
            } label: {
                Image(systemName: "backward.fill")
                    .font(.system(size: 28))
                    .foregroundStyle(TeslaColors.textSecondary)
            }

            // Play/Pause
            Button {
                player.togglePlayPause()
            } label: {
                Image(systemName: player.isPlaying ? "pause.fill" : "play.fill")
                    .font(.system(size: 36))
                    .foregroundStyle(.white)
                    .frame(width: 80, height: 80)
                    .background(TeslaColors.accent)
                    .clipShape(Circle())
            }
            .buttonStyle(TeslaScaleButtonStyle())

            // Next
            Button {
                player.nextTrack()
            } label: {
                Image(systemName: "forward.fill")
                    .font(.system(size: 28))
                    .foregroundStyle(TeslaColors.textSecondary)
            }

            // Repeat
            Button {
                // Toggle repeat
            } label: {
                Image(systemName: "repeat")
                    .font(.system(size: 18))
                    .foregroundStyle(TeslaColors.textSecondary)
            }
        }
    }

    // MARK: - Volume Section

    private var volumeSection: some View {
        HStack(spacing: 16) {
            Image(systemName: "speaker.fill")
                .font(.system(size: 14))
                .foregroundStyle(TeslaColors.textSecondary)

            TeslaSlider(
                value: Binding(
                    get: { player.volume },
                    set: { player.setVolume($0) }
                ),
                showValue: false
            )

            Image(systemName: "speaker.wave.3.fill")
                .font(.system(size: 14))
                .foregroundStyle(TeslaColors.textSecondary)
        }
    }

    // MARK: - Playlist Section

    private var playlistSection: some View {
        VStack(alignment: .leading, spacing: 16) {
            // Header
            HStack {
                Text("次に再生")
                    .font(TeslaTypography.titleMedium)
                    .foregroundStyle(TeslaColors.textPrimary)

                Spacer()

                Button {
                    // Edit playlist
                } label: {
                    Text("編集")
                        .font(TeslaTypography.labelMedium)
                        .foregroundStyle(TeslaColors.accent)
                }
            }
            .padding(.horizontal, 24)
            .padding(.top, 24)

            // Playlist
            ScrollView {
                LazyVStack(spacing: 0) {
                    ForEach(demoPlaylist) { track in
                        playlistRow(track: track)
                    }
                }
            }
        }
    }

    private func playlistRow(track: TeslaTrack) -> some View {
        Button {
            player.loadTrack(track)
            player.play()
        } label: {
            HStack(spacing: 16) {
                // Thumbnail
                RoundedRectangle(cornerRadius: 8)
                    .fill(TeslaColors.glassBackground)
                    .frame(width: 48, height: 48)
                    .overlay(
                        Image(systemName: "music.note")
                            .font(.system(size: 16))
                            .foregroundStyle(TeslaColors.textTertiary)
                    )

                // Track Info
                VStack(alignment: .leading, spacing: 4) {
                    Text(track.title)
                        .font(TeslaTypography.bodyMedium)
                        .foregroundStyle(
                            player.currentTrack?.id == track.id ? TeslaColors.accent : TeslaColors.textPrimary
                        )
                        .lineLimit(1)

                    Text(track.artist)
                        .font(TeslaTypography.labelSmall)
                        .foregroundStyle(TeslaColors.textSecondary)
                        .lineLimit(1)
                }

                Spacer()

                // Duration
                Text(formatTime(track.duration))
                    .font(TeslaTypography.labelSmall)
                    .foregroundStyle(TeslaColors.textTertiary)
                    .monospacedDigit()

                // Now Playing Indicator
                if player.currentTrack?.id == track.id {
                    Image(systemName: player.isPlaying ? "speaker.wave.2.fill" : "speaker.fill")
                        .font(.system(size: 14))
                        .foregroundStyle(TeslaColors.accent)
                }
            }
            .padding(.horizontal, 24)
            .padding(.vertical, 12)
            .background(
                player.currentTrack?.id == track.id ? TeslaColors.accent.opacity(0.1) : Color.clear
            )
        }
    }

    // MARK: - Helper Methods

    private func formatTime(_ seconds: TimeInterval) -> String {
        let minutes = Int(seconds) / 60
        let secs = Int(seconds) % 60
        return String(format: "%d:%02d", minutes, secs)
    }

    // MARK: - Demo Data

    private var demoPlaylist: [TeslaTrack] {
        [
            TeslaTrack(title: "Bohemian Rhapsody", artist: "Queen", duration: 354),
            TeslaTrack(title: "Hotel California", artist: "Eagles", duration: 390),
            TeslaTrack(title: "Stairway to Heaven", artist: "Led Zeppelin", duration: 482),
            TeslaTrack(title: "Comfortably Numb", artist: "Pink Floyd", duration: 382),
            TeslaTrack(title: "Sweet Child O' Mine", artist: "Guns N' Roses", duration: 356),
            TeslaTrack(title: "November Rain", artist: "Guns N' Roses", duration: 537),
            TeslaTrack(title: "Smells Like Teen Spirit", artist: "Nirvana", duration: 301),
            TeslaTrack(title: "Back in Black", artist: "AC/DC", duration: 255)
        ]
    }
}

// MARK: - Media Source

/// メディアソース
enum MediaSource: String, CaseIterable, Identifiable {
    case streaming = "streaming"
    case bluetooth = "bluetooth"
    case usb = "usb"
    case radio = "radio"
    case podcast = "podcast"

    var id: String { rawValue }

    var displayName: String {
        switch self {
        case .streaming: return "ストリーミング"
        case .bluetooth: return "Bluetooth"
        case .usb: return "USB"
        case .radio: return "ラジオ"
        case .podcast: return "ポッドキャスト"
        }
    }

    var iconName: String {
        switch self {
        case .streaming: return "music.note.list"
        case .bluetooth: return "dot.radiowaves.left.and.right"
        case .usb: return "cable.connector"
        case .radio: return "radio"
        case .podcast: return "mic.fill"
        }
    }
}

// MARK: - Preview

#Preview("Tesla Media Screen") {
    struct MediaScreenPreview: View {
        @StateObject private var player = TeslaMusicPlayer()

        var body: some View {
            TeslaMediaScreen(player: player)
                .onAppear {
                    player.currentTrack = TeslaTrack(
                        title: "Bohemian Rhapsody",
                        artist: "Queen",
                        album: "A Night at the Opera",
                        duration: 354
                    )
                    player.isPlaying = true
                    player.progress = 0.35
                }
        }
    }

    return MediaScreenPreview()
        .teslaTheme()
}
