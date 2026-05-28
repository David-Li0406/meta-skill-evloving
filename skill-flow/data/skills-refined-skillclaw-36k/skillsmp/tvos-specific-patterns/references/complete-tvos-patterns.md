# Complete tvOS-Specific Patterns Implementation

<!-- Loading Trigger: Agent reads this file when implementing tvOS Focus Engine, Siri Remote gestures, Top Shelf content, or 10-foot UI patterns -->

## Focus Engine Implementation

```swift
import SwiftUI
import TVUIKit

// MARK: - Custom Focusable Card

struct FocusableCard<Content: View>: View {
    @FocusState private var isFocused: Bool
    let action: () -> Void
    @ViewBuilder let content: () -> Content

    @Environment(\.isFocused) private var environmentFocused

    var body: some View {
        Button(action: action) {
            content()
                .padding(24)
                .background(
                    RoundedRectangle(cornerRadius: 16)
                        .fill(isFocused ? Color.white : Color.white.opacity(0.1))
                )
                .scaleEffect(isFocused ? 1.05 : 1.0)
                .shadow(
                    color: .black.opacity(isFocused ? 0.3 : 0),
                    radius: isFocused ? 20 : 0,
                    y: isFocused ? 10 : 0
                )
                .animation(.easeInOut(duration: 0.2), value: isFocused)
        }
        .buttonStyle(.plain)
        .focused($isFocused)
    }
}

// MARK: - Focus-Aware Navigation

struct FocusableNavigationRow: View {
    let title: String
    let items: [ContentItem]

    @FocusState private var focusedItemID: String?
    @State private var scrollOffset: CGFloat = 0

    var body: some View {
        VStack(alignment: .leading, spacing: 20) {
            Text(title)
                .font(.title2)
                .fontWeight(.bold)
                .padding(.horizontal, 60)

            ScrollView(.horizontal, showsIndicators: false) {
                LazyHStack(spacing: 40) {
                    ForEach(items) { item in
                        FocusableContentCard(item: item)
                            .focused($focusedItemID, equals: item.id)
                    }
                }
                .padding(.horizontal, 60)
                .padding(.vertical, 20)
            }
        }
        .onChange(of: focusedItemID) { _, newValue in
            // Auto-scroll to focused item
            withAnimation {
                scrollToItem(id: newValue)
            }
        }
    }

    private func scrollToItem(id: String?) {
        // Implement scroll logic
    }
}

struct FocusableContentCard: View {
    let item: ContentItem

    @Environment(\.isFocused) private var isFocused

    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            // Poster image
            AsyncImage(url: item.posterURL) { image in
                image
                    .resizable()
                    .aspectRatio(2/3, contentMode: .fill)
            } placeholder: {
                Rectangle()
                    .fill(Color.gray.opacity(0.3))
            }
            .frame(width: 200, height: 300)
            .cornerRadius(8)

            // Title
            Text(item.title)
                .font(.callout)
                .lineLimit(2)
                .frame(width: 200, alignment: .leading)
        }
        .scaleEffect(isFocused ? 1.1 : 1.0)
        .shadow(
            color: .black.opacity(isFocused ? 0.4 : 0),
            radius: isFocused ? 25 : 0,
            y: isFocused ? 15 : 0
        )
        .animation(.spring(response: 0.3, dampingFraction: 0.7), value: isFocused)
    }
}

struct ContentItem: Identifiable {
    let id: String
    let title: String
    let posterURL: URL?
}

// MARK: - Custom Focus Effect

struct CustomFocusEffect: ViewModifier {
    @Environment(\.isFocused) private var isFocused

    let cornerRadius: CGFloat
    let scale: CGFloat
    let shadowRadius: CGFloat

    init(
        cornerRadius: CGFloat = 12,
        scale: CGFloat = 1.05,
        shadowRadius: CGFloat = 20
    ) {
        self.cornerRadius = cornerRadius
        self.scale = scale
        self.shadowRadius = shadowRadius
    }

    func body(content: Content) -> some View {
        content
            .overlay(
                RoundedRectangle(cornerRadius: cornerRadius)
                    .stroke(Color.white, lineWidth: isFocused ? 4 : 0)
            )
            .scaleEffect(isFocused ? scale : 1.0)
            .shadow(
                color: .black.opacity(isFocused ? 0.5 : 0),
                radius: isFocused ? shadowRadius : 0,
                y: isFocused ? 10 : 0
            )
            .animation(.easeInOut(duration: 0.15), value: isFocused)
    }
}

extension View {
    func customFocusEffect(
        cornerRadius: CGFloat = 12,
        scale: CGFloat = 1.05,
        shadowRadius: CGFloat = 20
    ) -> some View {
        modifier(CustomFocusEffect(
            cornerRadius: cornerRadius,
            scale: scale,
            shadowRadius: shadowRadius
        ))
    }
}

// MARK: - Focus Guide for Custom Layouts

struct GridWithFocusGuide: View {
    let items: [ContentItem]
    @FocusState private var focusedItem: String?

    let columns = [
        GridItem(.fixed(300), spacing: 40),
        GridItem(.fixed(300), spacing: 40),
        GridItem(.fixed(300), spacing: 40),
        GridItem(.fixed(300), spacing: 40)
    ]

    var body: some View {
        ScrollView {
            LazyVGrid(columns: columns, spacing: 40) {
                ForEach(items) { item in
                    FocusableContentCard(item: item)
                        .focused($focusedItem, equals: item.id)
                }
            }
            .padding(60)
        }
        .focusSection()
    }
}
```

## Siri Remote Gesture Handling

```swift
import SwiftUI
import GameController

// MARK: - Siri Remote Gesture Recognizer

class SiriRemoteGestureHandler: ObservableObject {
    @Published var swipeDirection: SwipeDirection?
    @Published var isPressed: Bool = false
    @Published var clickLocation: CGPoint?

    enum SwipeDirection {
        case up, down, left, right
    }

    private var panGestureRecognizer: UIPanGestureRecognizer?
    private var tapGestureRecognizer: UITapGestureRecognizer?
    private var pressGestureRecognizer: UILongPressGestureRecognizer?

    func setupGestures(on view: UIView) {
        // Swipe gestures
        let swipeUp = UISwipeGestureRecognizer(target: self, action: #selector(handleSwipe(_:)))
        swipeUp.direction = .up
        view.addGestureRecognizer(swipeUp)

        let swipeDown = UISwipeGestureRecognizer(target: self, action: #selector(handleSwipe(_:)))
        swipeDown.direction = .down
        view.addGestureRecognizer(swipeDown)

        let swipeLeft = UISwipeGestureRecognizer(target: self, action: #selector(handleSwipe(_:)))
        swipeLeft.direction = .left
        view.addGestureRecognizer(swipeLeft)

        let swipeRight = UISwipeGestureRecognizer(target: self, action: #selector(handleSwipe(_:)))
        swipeRight.direction = .right
        view.addGestureRecognizer(swipeRight)

        // Pan gesture for scrubbing
        let panGesture = UIPanGestureRecognizer(target: self, action: #selector(handlePan(_:)))
        view.addGestureRecognizer(panGesture)
        panGestureRecognizer = panGesture

        // Long press for context menu
        let pressGesture = UILongPressGestureRecognizer(target: self, action: #selector(handleLongPress(_:)))
        pressGesture.minimumPressDuration = 0.5
        view.addGestureRecognizer(pressGesture)
        pressGestureRecognizer = pressGesture
    }

    @objc private func handleSwipe(_ gesture: UISwipeGestureRecognizer) {
        switch gesture.direction {
        case .up: swipeDirection = .up
        case .down: swipeDirection = .down
        case .left: swipeDirection = .left
        case .right: swipeDirection = .right
        default: break
        }

        // Reset after short delay
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.1) {
            self.swipeDirection = nil
        }
    }

    @objc private func handlePan(_ gesture: UIPanGestureRecognizer) {
        // Handle pan for scrubbing/seeking
    }

    @objc private func handleLongPress(_ gesture: UILongPressGestureRecognizer) {
        switch gesture.state {
        case .began:
            isPressed = true
        case .ended, .cancelled:
            isPressed = false
        default:
            break
        }
    }
}

// MARK: - SwiftUI Gesture Handling

struct RemoteGestureView: View {
    @State private var position: CGFloat = 0
    @State private var lastSwipe: String = ""

    var body: some View {
        VStack {
            Text("Swipe on remote: \(lastSwipe)")
                .font(.headline)

            // Progress bar controlled by remote swipes
            GeometryReader { geometry in
                ZStack(alignment: .leading) {
                    Rectangle()
                        .fill(Color.gray.opacity(0.3))

                    Rectangle()
                        .fill(Color.blue)
                        .frame(width: geometry.size.width * position)
                }
            }
            .frame(height: 10)
            .cornerRadius(5)
            .padding(.horizontal, 60)
        }
        .focusable()
        .onMoveCommand { direction in
            handleMoveCommand(direction)
        }
        .onPlayPauseCommand {
            handlePlayPause()
        }
    }

    private func handleMoveCommand(_ direction: MoveCommandDirection) {
        withAnimation(.easeInOut(duration: 0.2)) {
            switch direction {
            case .left:
                position = max(0, position - 0.1)
                lastSwipe = "Left"
            case .right:
                position = min(1, position + 0.1)
                lastSwipe = "Right"
            case .up:
                lastSwipe = "Up"
            case .down:
                lastSwipe = "Down"
            @unknown default:
                break
            }
        }
    }

    private func handlePlayPause() {
        // Handle play/pause button press
    }
}

// MARK: - Game Controller Support

class GameControllerHandler: ObservableObject {
    @Published var isControllerConnected = false
    @Published var leftStickPosition: CGPoint = .zero
    @Published var rightStickPosition: CGPoint = .zero

    init() {
        setupControllerNotifications()
        checkForConnectedControllers()
    }

    private func setupControllerNotifications() {
        NotificationCenter.default.addObserver(
            self,
            selector: #selector(controllerConnected),
            name: .GCControllerDidConnect,
            object: nil
        )

        NotificationCenter.default.addObserver(
            self,
            selector: #selector(controllerDisconnected),
            name: .GCControllerDidDisconnect,
            object: nil
        )
    }

    private func checkForConnectedControllers() {
        if let controller = GCController.controllers().first {
            setupController(controller)
        }
    }

    @objc private func controllerConnected(_ notification: Notification) {
        if let controller = notification.object as? GCController {
            setupController(controller)
        }
    }

    @objc private func controllerDisconnected(_ notification: Notification) {
        isControllerConnected = false
    }

    private func setupController(_ controller: GCController) {
        isControllerConnected = true

        // Extended gamepad (full controller)
        if let gamepad = controller.extendedGamepad {
            setupExtendedGamepad(gamepad)
        }
        // Micro gamepad (Siri Remote)
        else if let microGamepad = controller.microGamepad {
            setupMicroGamepad(microGamepad)
        }
    }

    private func setupExtendedGamepad(_ gamepad: GCExtendedGamepad) {
        gamepad.leftThumbstick.valueChangedHandler = { [weak self] _, xValue, yValue in
            DispatchQueue.main.async {
                self?.leftStickPosition = CGPoint(x: CGFloat(xValue), y: CGFloat(yValue))
            }
        }

        gamepad.rightThumbstick.valueChangedHandler = { [weak self] _, xValue, yValue in
            DispatchQueue.main.async {
                self?.rightStickPosition = CGPoint(x: CGFloat(xValue), y: CGFloat(yValue))
            }
        }

        gamepad.buttonA.pressedChangedHandler = { _, _, pressed in
            if pressed {
                // Handle A button
            }
        }
    }

    private func setupMicroGamepad(_ gamepad: GCMicroGamepad) {
        gamepad.dpad.valueChangedHandler = { [weak self] _, xValue, yValue in
            DispatchQueue.main.async {
                self?.leftStickPosition = CGPoint(x: CGFloat(xValue), y: CGFloat(yValue))
            }
        }

        gamepad.buttonA.pressedChangedHandler = { _, _, pressed in
            if pressed {
                // Handle select button
            }
        }

        gamepad.buttonX.pressedChangedHandler = { _, _, pressed in
            if pressed {
                // Handle play/pause button
            }
        }
    }
}
```

## Top Shelf Implementation

```swift
import TVServices

// MARK: - Top Shelf Content Provider

class TopShelfContentProvider: TVTopShelfContentProvider {

    override func loadTopShelfContent() async -> TVTopShelfContent? {
        // Determine content style based on app state
        let style = await determineContentStyle()

        switch style {
        case .sectioned:
            return await loadSectionedContent()
        case .inset:
            return await loadInsetContent()
        }
    }

    private func determineContentStyle() async -> ContentStyle {
        // Return sectioned for browse-heavy apps, inset for focused content
        return .sectioned
    }

    private enum ContentStyle {
        case sectioned
        case inset
    }

    // MARK: - Sectioned Content (Multiple Rows)

    private func loadSectionedContent() async -> TVTopShelfSectionedContent {
        let sections = await fetchContentSections()

        return TVTopShelfSectionedContent(sections: sections.map { section in
            TVTopShelfItemCollection(items: section.items.map { item in
                createSectionedItem(from: item)
            })
        })
    }

    private func createSectionedItem(from item: TopShelfItem) -> TVTopShelfSectionedItem {
        let sectionedItem = TVTopShelfSectionedItem(identifier: item.id)

        // Image (required)
        sectionedItem.setImageURL(item.imageURL, for: .screenScale1x)
        sectionedItem.setImageURL(item.imageURL2x, for: .screenScale2x)

        // Title
        sectionedItem.title = item.title

        // Play action (opens app to content)
        sectionedItem.playAction = TVTopShelfAction(url: item.playURL)

        // Display action (shows info)
        sectionedItem.displayAction = TVTopShelfAction(url: item.displayURL)

        return sectionedItem
    }

    // MARK: - Inset Content (Full Width Banner)

    private func loadInsetContent() async -> TVTopShelfInsetContent {
        let featuredItems = await fetchFeaturedContent()

        return TVTopShelfInsetContent(items: featuredItems.map { item in
            createInsetItem(from: item)
        })
    }

    private func createInsetItem(from item: TopShelfItem) -> TVTopShelfInsetItem {
        let insetItem = TVTopShelfInsetItem(identifier: item.id)

        // Large image for inset style
        insetItem.setImageURL(item.wideImageURL, for: .screenScale1x)
        insetItem.setImageURL(item.wideImageURL2x, for: .screenScale2x)

        // Content descriptor
        insetItem.title = item.title

        // Primary action
        insetItem.playAction = TVTopShelfAction(url: item.playURL)
        insetItem.displayAction = TVTopShelfAction(url: item.displayURL)

        return insetItem
    }

    // MARK: - Data Fetching

    private func fetchContentSections() async -> [ContentSection] {
        // Fetch from cache or network
        // Return quickly for good UX
        return []
    }

    private func fetchFeaturedContent() async -> [TopShelfItem] {
        return []
    }
}

// MARK: - Top Shelf Data Models

struct TopShelfItem {
    let id: String
    let title: String
    let imageURL: URL
    let imageURL2x: URL
    let wideImageURL: URL
    let wideImageURL2x: URL
    let playURL: URL
    let displayURL: URL
}

struct ContentSection {
    let title: String
    let items: [TopShelfItem]
}

// MARK: - Deep Link Handling for Top Shelf

extension AppDelegate {
    func application(
        _ app: UIApplication,
        open url: URL,
        options: [UIApplication.OpenURLOptionsKey: Any] = [:]
    ) -> Bool {
        // Handle Top Shelf deep links
        guard let components = URLComponents(url: url, resolvingAgainstBaseURL: true),
              let host = components.host else {
            return false
        }

        switch host {
        case "play":
            handlePlayDeepLink(components)
        case "display":
            handleDisplayDeepLink(components)
        default:
            return false
        }

        return true
    }

    private func handlePlayDeepLink(_ components: URLComponents) {
        // Navigate to content and start playback
        guard let contentId = components.queryItems?.first(where: { $0.name == "id" })?.value else {
            return
        }

        // Navigate and play
    }

    private func handleDisplayDeepLink(_ components: URLComponents) {
        // Navigate to content detail page
        guard let contentId = components.queryItems?.first(where: { $0.name == "id" })?.value else {
            return
        }

        // Navigate to detail
    }
}
```

## 10-Foot UI Patterns

```swift
import SwiftUI

// MARK: - 10-Foot Safe Area Padding

struct SafeAreaConstants {
    static let horizontal: CGFloat = 90  // Safe area for TV edges
    static let top: CGFloat = 60
    static let bottom: CGFloat = 60

    static var insets: EdgeInsets {
        EdgeInsets(
            top: top,
            leading: horizontal,
            bottom: bottom,
            trailing: horizontal
        )
    }
}

struct TVSafeAreaView<Content: View>: View {
    @ViewBuilder let content: () -> Content

    var body: some View {
        content()
            .padding(SafeAreaConstants.insets)
    }
}

// MARK: - Readable Content Width

struct ReadableContentView<Content: View>: View {
    @ViewBuilder let content: () -> Content

    var body: some View {
        GeometryReader { geometry in
            let maxWidth = min(geometry.size.width * 0.6, 800)

            HStack {
                Spacer()
                content()
                    .frame(maxWidth: maxWidth)
                Spacer()
            }
        }
    }
}

// MARK: - Large Text Styles for TV

extension Font {
    static var tvTitle: Font {
        .system(size: 76, weight: .bold)
    }

    static var tvHeadline: Font {
        .system(size: 48, weight: .semibold)
    }

    static var tvBody: Font {
        .system(size: 38, weight: .regular)
    }

    static var tvCaption: Font {
        .system(size: 29, weight: .regular)
    }

    static var tvCallout: Font {
        .system(size: 31, weight: .regular)
    }
}

// MARK: - Full Screen Detail View

struct TVDetailView: View {
    let item: ContentItem
    @Environment(\.dismiss) private var dismiss
    @FocusState private var focusedButton: ButtonType?

    enum ButtonType {
        case play, addToList, moreInfo
    }

    var body: some View {
        ZStack {
            // Background image
            AsyncImage(url: item.posterURL) { image in
                image
                    .resizable()
                    .aspectRatio(contentMode: .fill)
            } placeholder: {
                Color.black
            }
            .ignoresSafeArea()
            .overlay(
                LinearGradient(
                    colors: [.clear, .black.opacity(0.8), .black],
                    startPoint: .top,
                    endPoint: .bottom
                )
            )

            // Content
            VStack(alignment: .leading, spacing: 40) {
                Spacer()

                Text(item.title)
                    .font(.tvTitle)
                    .foregroundStyle(.white)

                Text("2024 • 2h 15m • Action, Adventure")
                    .font(.tvCallout)
                    .foregroundStyle(.white.opacity(0.7))

                Text("A thrilling adventure that takes you across the world...")
                    .font(.tvBody)
                    .foregroundStyle(.white.opacity(0.9))
                    .lineLimit(3)
                    .frame(maxWidth: 800, alignment: .leading)

                // Action buttons
                HStack(spacing: 30) {
                    TVButton(title: "Play", icon: "play.fill") {
                        // Play action
                    }
                    .focused($focusedButton, equals: .play)

                    TVButton(title: "Add to List", icon: "plus") {
                        // Add to list
                    }
                    .focused($focusedButton, equals: .addToList)

                    TVButton(title: "More Info", icon: "info.circle") {
                        // Show more info
                    }
                    .focused($focusedButton, equals: .moreInfo)
                }
            }
            .padding(SafeAreaConstants.insets)
        }
        .onAppear {
            focusedButton = .play
        }
    }
}

// MARK: - TV-Optimized Button

struct TVButton: View {
    let title: String
    let icon: String
    let action: () -> Void

    @Environment(\.isFocused) private var isFocused

    var body: some View {
        Button(action: action) {
            HStack(spacing: 12) {
                Image(systemName: icon)
                    .font(.title2)
                Text(title)
                    .font(.tvCallout)
            }
            .padding(.horizontal, 40)
            .padding(.vertical, 16)
            .background(
                Capsule()
                    .fill(isFocused ? Color.white : Color.white.opacity(0.2))
            )
            .foregroundStyle(isFocused ? .black : .white)
        }
        .buttonStyle(.plain)
        .scaleEffect(isFocused ? 1.1 : 1.0)
        .animation(.easeInOut(duration: 0.15), value: isFocused)
    }
}

// MARK: - TV Tab Bar

struct TVTabBar: View {
    @Binding var selectedTab: Int
    let tabs: [TabItem]

    @FocusState private var focusedTab: Int?

    struct TabItem {
        let title: String
        let icon: String
    }

    var body: some View {
        HStack(spacing: 60) {
            ForEach(Array(tabs.enumerated()), id: \.offset) { index, tab in
                TVTabButton(
                    title: tab.title,
                    icon: tab.icon,
                    isSelected: selectedTab == index
                ) {
                    selectedTab = index
                }
                .focused($focusedTab, equals: index)
            }
        }
        .padding(.horizontal, SafeAreaConstants.horizontal)
        .padding(.vertical, 20)
        .background(
            Rectangle()
                .fill(.ultraThinMaterial)
                .ignoresSafeArea()
        )
    }
}

struct TVTabButton: View {
    let title: String
    let icon: String
    let isSelected: Bool
    let action: () -> Void

    @Environment(\.isFocused) private var isFocused

    var body: some View {
        Button(action: action) {
            VStack(spacing: 8) {
                Image(systemName: icon)
                    .font(.title)
                Text(title)
                    .font(.tvCaption)
            }
            .foregroundStyle(isSelected || isFocused ? .white : .white.opacity(0.6))
            .padding(.horizontal, 20)
            .padding(.vertical, 10)
            .background(
                RoundedRectangle(cornerRadius: 12)
                    .fill(isFocused ? Color.white.opacity(0.2) : Color.clear)
            )
        }
        .buttonStyle(.plain)
    }
}
```

## tvOS Video Player

```swift
import SwiftUI
import AVKit

// MARK: - Custom TV Video Player

struct TVVideoPlayer: View {
    let url: URL
    @StateObject private var playerViewModel = VideoPlayerViewModel()
    @State private var showControls = true
    @FocusState private var controlsFocused: Bool

    var body: some View {
        ZStack {
            // Video layer
            VideoPlayer(player: playerViewModel.player)
                .ignoresSafeArea()

            // Controls overlay
            if showControls {
                TVVideoControls(viewModel: playerViewModel)
                    .transition(.opacity)
            }
        }
        .onAppear {
            playerViewModel.setupPlayer(url: url)
        }
        .onDisappear {
            playerViewModel.cleanup()
        }
        .onPlayPauseCommand {
            playerViewModel.togglePlayPause()
        }
        .onMoveCommand { direction in
            handleMoveCommand(direction)
        }
        .onExitCommand {
            // Handle menu button - show controls or exit
            if showControls {
                // Let system handle exit
            } else {
                withAnimation {
                    showControls = true
                }
            }
        }
    }

    private func handleMoveCommand(_ direction: MoveCommandDirection) {
        switch direction {
        case .left:
            playerViewModel.seekBackward()
        case .right:
            playerViewModel.seekForward()
        case .up, .down:
            withAnimation {
                showControls.toggle()
            }
        @unknown default:
            break
        }
    }
}

// MARK: - Video Player ViewModel

@MainActor
class VideoPlayerViewModel: ObservableObject {
    @Published var player: AVPlayer?
    @Published var isPlaying = false
    @Published var currentTime: TimeInterval = 0
    @Published var duration: TimeInterval = 0
    @Published var isBuffering = false

    private var timeObserver: Any?

    func setupPlayer(url: URL) {
        let playerItem = AVPlayerItem(url: url)
        player = AVPlayer(playerItem: playerItem)

        setupTimeObserver()
        setupNotifications()

        player?.play()
        isPlaying = true
    }

    func cleanup() {
        if let observer = timeObserver {
            player?.removeTimeObserver(observer)
        }
        player?.pause()
        player = nil
    }

    func togglePlayPause() {
        if isPlaying {
            player?.pause()
        } else {
            player?.play()
        }
        isPlaying.toggle()
    }

    func seekForward() {
        seek(by: 10)
    }

    func seekBackward() {
        seek(by: -10)
    }

    func seek(to percentage: Double) {
        let time = CMTime(seconds: duration * percentage, preferredTimescale: 600)
        player?.seek(to: time)
    }

    private func seek(by seconds: Double) {
        guard let currentTime = player?.currentTime() else { return }
        let newTime = CMTime(
            seconds: currentTime.seconds + seconds,
            preferredTimescale: 600
        )
        player?.seek(to: newTime)
    }

    private func setupTimeObserver() {
        let interval = CMTime(seconds: 0.5, preferredTimescale: 600)
        timeObserver = player?.addPeriodicTimeObserver(
            forInterval: interval,
            queue: .main
        ) { [weak self] time in
            self?.currentTime = time.seconds
            if let duration = self?.player?.currentItem?.duration.seconds,
               !duration.isNaN {
                self?.duration = duration
            }
        }
    }

    private func setupNotifications() {
        NotificationCenter.default.addObserver(
            forName: .AVPlayerItemDidPlayToEndTime,
            object: player?.currentItem,
            queue: .main
        ) { [weak self] _ in
            self?.isPlaying = false
        }
    }
}

// MARK: - TV Video Controls

struct TVVideoControls: View {
    @ObservedObject var viewModel: VideoPlayerViewModel

    var body: some View {
        VStack {
            Spacer()

            // Progress bar
            VStack(spacing: 16) {
                // Time display
                HStack {
                    Text(formatTime(viewModel.currentTime))
                    Spacer()
                    Text(formatTime(viewModel.duration))
                }
                .font(.tvCaption)
                .foregroundStyle(.white)

                // Scrubber
                GeometryReader { geometry in
                    ZStack(alignment: .leading) {
                        // Background
                        Rectangle()
                            .fill(Color.white.opacity(0.3))

                        // Progress
                        Rectangle()
                            .fill(Color.white)
                            .frame(width: progressWidth(in: geometry.size.width))
                    }
                }
                .frame(height: 8)
                .cornerRadius(4)
            }
            .padding(.horizontal, SafeAreaConstants.horizontal)
            .padding(.bottom, 40)
            .background(
                LinearGradient(
                    colors: [.clear, .black.opacity(0.8)],
                    startPoint: .top,
                    endPoint: .bottom
                )
            )
        }
    }

    private func progressWidth(in totalWidth: CGFloat) -> CGFloat {
        guard viewModel.duration > 0 else { return 0 }
        return totalWidth * CGFloat(viewModel.currentTime / viewModel.duration)
    }

    private func formatTime(_ seconds: TimeInterval) -> String {
        let hours = Int(seconds) / 3600
        let minutes = Int(seconds) / 60 % 60
        let secs = Int(seconds) % 60

        if hours > 0 {
            return String(format: "%d:%02d:%02d", hours, minutes, secs)
        } else {
            return String(format: "%d:%02d", minutes, secs)
        }
    }
}
```
