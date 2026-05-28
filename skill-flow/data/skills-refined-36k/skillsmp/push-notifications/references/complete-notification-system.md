# Complete Push Notification System Implementation

<!-- Loading Trigger: Agent reads this file when implementing push notifications, permission flows, notification handling, or notification service extensions -->

## Permission Request System

```swift
import UserNotifications
import UIKit
import Combine

// MARK: - Notification Permission Manager

@MainActor
final class NotificationPermissionManager: ObservableObject {

    @Published private(set) var authorizationStatus: UNAuthorizationStatus = .notDetermined
    @Published private(set) var isRegisteredForRemoteNotifications = false
    @Published private(set) var deviceToken: String?

    private let center = UNUserNotificationCenter.current()

    init() {
        Task {
            await checkCurrentStatus()
        }
    }

    // MARK: - Status Check

    func checkCurrentStatus() async {
        let settings = await center.notificationSettings()
        authorizationStatus = settings.authorizationStatus
    }

    // MARK: - Permission Request with Optimal Timing

    /// Request permission after user has experienced value (not on first launch)
    func requestPermissionWhenReady() async -> Bool {
        // Check if already determined
        let settings = await center.notificationSettings()

        switch settings.authorizationStatus {
        case .notDetermined:
            return await requestPermission()

        case .authorized, .provisional, .ephemeral:
            await registerForRemoteNotifications()
            return true

        case .denied:
            return false

        @unknown default:
            return false
        }
    }

    /// Direct permission request
    func requestPermission() async -> Bool {
        do {
            let granted = try await center.requestAuthorization(
                options: [.alert, .badge, .sound, .criticalAlert, .providesAppNotificationSettings]
            )

            await checkCurrentStatus()

            if granted {
                await registerForRemoteNotifications()
            }

            return granted
        } catch {
            print("Failed to request notification permission: \(error)")
            return false
        }
    }

    /// Request provisional (quiet) notifications for less intrusive onboarding
    func requestProvisionalPermission() async -> Bool {
        do {
            let granted = try await center.requestAuthorization(
                options: [.alert, .badge, .sound, .provisional]
            )

            await checkCurrentStatus()

            if granted {
                await registerForRemoteNotifications()
            }

            return granted
        } catch {
            print("Failed to request provisional permission: \(error)")
            return false
        }
    }

    private func registerForRemoteNotifications() async {
        await MainActor.run {
            UIApplication.shared.registerForRemoteNotifications()
        }
    }

    // MARK: - Device Token Handling

    func handleDeviceToken(_ token: Data) {
        let tokenString = token.map { String(format: "%02.2hhx", $0) }.joined()
        self.deviceToken = tokenString

        // Send to server
        Task {
            await sendTokenToServer(tokenString)
        }
    }

    func handleRegistrationError(_ error: Error) {
        print("Failed to register for remote notifications: \(error)")
    }

    private func sendTokenToServer(_ token: String) async {
        // Send device token to your backend
    }

    // MARK: - Settings Navigation

    func openNotificationSettings() {
        if let url = URL(string: UIApplication.openSettingsURLString) {
            UIApplication.shared.open(url)
        }
    }
}

// MARK: - Pre-Permission Prompt View

struct NotificationPermissionPromptView: View {
    @ObservedObject var permissionManager: NotificationPermissionManager
    @Binding var isPresented: Bool

    var body: some View {
        VStack(spacing: 24) {
            Image(systemName: "bell.badge.fill")
                .font(.system(size: 60))
                .foregroundStyle(.blue)

            Text("Stay Updated")
                .font(.title)
                .fontWeight(.bold)

            Text("Get notified about important updates, messages, and activity on your account.")
                .multilineTextAlignment(.center)
                .foregroundStyle(.secondary)

            VStack(spacing: 12) {
                Button("Enable Notifications") {
                    Task {
                        _ = await permissionManager.requestPermission()
                        isPresented = false
                    }
                }
                .buttonStyle(.borderedProminent)

                Button("Not Now") {
                    isPresented = false
                }
                .foregroundStyle(.secondary)
            }
        }
        .padding(32)
    }
}
```

## Notification Handling

```swift
import UserNotifications

// MARK: - Notification Handler

@MainActor
final class NotificationHandler: NSObject, ObservableObject {

    @Published var pendingDeepLink: DeepLink?
    @Published var unreadCount: Int = 0

    private let center = UNUserNotificationCenter.current()

    override init() {
        super.init()
        center.delegate = self
    }

    // MARK: - Badge Management

    func updateBadgeCount(_ count: Int) async {
        unreadCount = count

        do {
            try await center.setBadgeCount(count)
        } catch {
            print("Failed to set badge count: \(error)")
        }
    }

    func clearBadge() async {
        await updateBadgeCount(0)
    }

    // MARK: - Local Notification Scheduling

    func scheduleLocalNotification(
        identifier: String,
        title: String,
        body: String,
        trigger: UNNotificationTrigger,
        userInfo: [String: Any] = [:],
        categoryIdentifier: String? = nil
    ) async throws {

        let content = UNMutableNotificationContent()
        content.title = title
        content.body = body
        content.sound = .default
        content.userInfo = userInfo

        if let category = categoryIdentifier {
            content.categoryIdentifier = category
        }

        let request = UNNotificationRequest(
            identifier: identifier,
            content: content,
            trigger: trigger
        )

        try await center.add(request)
    }

    func cancelNotification(identifier: String) {
        center.removePendingNotificationRequests(withIdentifiers: [identifier])
        center.removeDeliveredNotifications(withIdentifiers: [identifier])
    }

    func cancelAllNotifications() {
        center.removeAllPendingNotificationRequests()
        center.removeAllDeliveredNotifications()
    }
}

// MARK: - UNUserNotificationCenterDelegate

extension NotificationHandler: UNUserNotificationCenterDelegate {

    /// Called when notification is received while app is in foreground
    nonisolated func userNotificationCenter(
        _ center: UNUserNotificationCenter,
        willPresent notification: UNNotification
    ) async -> UNNotificationPresentationOptions {

        let userInfo = notification.request.content.userInfo

        // Process notification data
        await processNotificationData(userInfo)

        // Determine presentation based on context
        let presentationOptions = await determinePresentationOptions(
            for: notification,
            userInfo: userInfo
        )

        return presentationOptions
    }

    /// Called when user taps on notification
    nonisolated func userNotificationCenter(
        _ center: UNUserNotificationCenter,
        didReceive response: UNNotificationResponse
    ) async {

        let userInfo = response.notification.request.content.userInfo
        let actionIdentifier = response.actionIdentifier

        switch actionIdentifier {
        case UNNotificationDefaultActionIdentifier:
            // User tapped notification
            await handleNotificationTap(userInfo: userInfo)

        case UNNotificationDismissActionIdentifier:
            // User dismissed notification
            await handleNotificationDismiss(userInfo: userInfo)

        default:
            // Custom action
            await handleCustomAction(actionIdentifier, userInfo: userInfo, response: response)
        }
    }

    // MARK: - Private Handlers

    private func processNotificationData(_ userInfo: [AnyHashable: Any]) async {
        // Process and store notification data
    }

    @MainActor
    private func determinePresentationOptions(
        for notification: UNNotification,
        userInfo: [AnyHashable: Any]
    ) -> UNNotificationPresentationOptions {

        // Check if notification is for current screen
        if isNotificationForCurrentScreen(userInfo) {
            // Don't show banner if user is already viewing related content
            return [.sound, .badge]
        }

        return [.banner, .sound, .badge, .list]
    }

    @MainActor
    private func handleNotificationTap(userInfo: [AnyHashable: Any]) {
        // Parse deep link from notification
        if let deepLink = parseDeepLink(from: userInfo) {
            pendingDeepLink = deepLink
        }
    }

    private func handleNotificationDismiss(userInfo: [AnyHashable: Any]) async {
        // Track dismiss analytics
    }

    @MainActor
    private func handleCustomAction(
        _ action: String,
        userInfo: [AnyHashable: Any],
        response: UNNotificationResponse
    ) {
        switch action {
        case "REPLY_ACTION":
            if let textResponse = response as? UNTextInputNotificationResponse {
                handleReplyAction(text: textResponse.userText, userInfo: userInfo)
            }

        case "MARK_READ_ACTION":
            handleMarkReadAction(userInfo: userInfo)

        case "ARCHIVE_ACTION":
            handleArchiveAction(userInfo: userInfo)

        default:
            break
        }
    }

    @MainActor
    private func isNotificationForCurrentScreen(_ userInfo: [AnyHashable: Any]) -> Bool {
        // Check if user is viewing the related content
        return false
    }

    private func parseDeepLink(from userInfo: [AnyHashable: Any]) -> DeepLink? {
        guard let type = userInfo["type"] as? String else { return nil }

        switch type {
        case "message":
            guard let conversationId = userInfo["conversation_id"] as? String else { return nil }
            return .conversation(id: conversationId)

        case "order":
            guard let orderId = userInfo["order_id"] as? String else { return nil }
            return .order(id: orderId)

        default:
            return nil
        }
    }

    private func handleReplyAction(text: String, userInfo: [AnyHashable: Any]) {
        // Send reply
    }

    private func handleMarkReadAction(userInfo: [AnyHashable: Any]) {
        // Mark as read
    }

    private func handleArchiveAction(userInfo: [AnyHashable: Any]) {
        // Archive item
    }
}

// MARK: - Deep Link Model

enum DeepLink: Equatable {
    case conversation(id: String)
    case order(id: String)
    case profile(userId: String)
    case settings
}
```

## Notification Categories and Actions

```swift
import UserNotifications

// MARK: - Notification Category Registration

final class NotificationCategoryManager {

    static func registerCategories() {
        let center = UNUserNotificationCenter.current()

        // Message category with reply action
        let replyAction = UNTextInputNotificationAction(
            identifier: "REPLY_ACTION",
            title: "Reply",
            options: [],
            textInputButtonTitle: "Send",
            textInputPlaceholder: "Type a message..."
        )

        let markReadAction = UNNotificationAction(
            identifier: "MARK_READ_ACTION",
            title: "Mark as Read",
            options: []
        )

        let messageCategory = UNNotificationCategory(
            identifier: "MESSAGE",
            actions: [replyAction, markReadAction],
            intentIdentifiers: [],
            options: [.customDismissAction]
        )

        // Order category
        let trackAction = UNNotificationAction(
            identifier: "TRACK_ACTION",
            title: "Track Order",
            options: [.foreground]
        )

        let orderCategory = UNNotificationCategory(
            identifier: "ORDER",
            actions: [trackAction],
            intentIdentifiers: [],
            options: []
        )

        // Reminder category
        let snoozeAction = UNNotificationAction(
            identifier: "SNOOZE_ACTION",
            title: "Snooze 1 Hour",
            options: []
        )

        let completeAction = UNNotificationAction(
            identifier: "COMPLETE_ACTION",
            title: "Mark Complete",
            options: [.destructive]
        )

        let reminderCategory = UNNotificationCategory(
            identifier: "REMINDER",
            actions: [snoozeAction, completeAction],
            intentIdentifiers: [],
            options: []
        )

        center.setNotificationCategories([
            messageCategory,
            orderCategory,
            reminderCategory
        ])
    }
}
```

## Notification Service Extension

```swift
// NotificationServiceExtension/NotificationService.swift

import UserNotifications
import UIKit

class NotificationService: UNNotificationServiceExtension {

    private var contentHandler: ((UNNotificationContent) -> Void)?
    private var bestAttemptContent: UNMutableNotificationContent?

    override func didReceive(
        _ request: UNNotificationRequest,
        withContentHandler contentHandler: @escaping (UNNotificationContent) -> Void
    ) {
        self.contentHandler = contentHandler
        bestAttemptContent = (request.content.mutableCopy() as? UNMutableNotificationContent)

        guard let bestAttemptContent = bestAttemptContent else {
            contentHandler(request.content)
            return
        }

        // Perform modifications
        Task {
            await processNotification(bestAttemptContent)
            contentHandler(bestAttemptContent)
        }
    }

    override func serviceExtensionTimeWillExpire() {
        // Called just before the extension will be terminated
        if let contentHandler = contentHandler,
           let bestAttemptContent = bestAttemptContent {
            contentHandler(bestAttemptContent)
        }
    }

    // MARK: - Notification Processing

    private func processNotification(_ content: UNMutableNotificationContent) async {
        // 1. Download and attach images
        if let imageURLString = content.userInfo["image_url"] as? String {
            await attachImage(from: imageURLString, to: content)
        }

        // 2. Decrypt end-to-end encrypted content
        if let encryptedBody = content.userInfo["encrypted_body"] as? String {
            if let decrypted = decryptContent(encryptedBody) {
                content.body = decrypted
            }
        }

        // 3. Localize content
        localizeContent(content)

        // 4. Update badge count from server
        if let badgeCount = content.userInfo["badge"] as? Int {
            content.badge = NSNumber(value: badgeCount)
        }

        // 5. Set thread identifier for grouping
        if let threadId = content.userInfo["thread_id"] as? String {
            content.threadIdentifier = threadId
        }
    }

    private func attachImage(from urlString: String, to content: UNMutableNotificationContent) async {
        guard let url = URL(string: urlString) else { return }

        do {
            let (data, _) = try await URLSession.shared.data(from: url)

            // Save to temporary file
            let tempDir = FileManager.default.temporaryDirectory
            let filename = url.lastPathComponent
            let fileURL = tempDir.appendingPathComponent(filename)

            try data.write(to: fileURL)

            let attachment = try UNNotificationAttachment(
                identifier: "image",
                url: fileURL,
                options: [
                    UNNotificationAttachmentOptionsTypeHintKey: "public.jpeg"
                ]
            )

            content.attachments = [attachment]
        } catch {
            print("Failed to attach image: \(error)")
        }
    }

    private func decryptContent(_ encrypted: String) -> String? {
        // Decrypt using shared keychain credentials
        // This allows end-to-end encryption where server can't read content
        return nil
    }

    private func localizeContent(_ content: UNMutableNotificationContent) {
        // Apply any dynamic localization
    }
}
```

## Silent Notifications

```swift
// MARK: - Silent Notification Handler

extension AppDelegate {

    func application(
        _ application: UIApplication,
        didReceiveRemoteNotification userInfo: [AnyHashable: Any],
        fetchCompletionHandler completionHandler: @escaping (UIBackgroundFetchResult) -> Void
    ) {
        // Handle silent push notifications

        guard let aps = userInfo["aps"] as? [String: Any],
              aps["content-available"] as? Int == 1 else {
            completionHandler(.noData)
            return
        }

        Task {
            let result = await handleSilentNotification(userInfo)
            completionHandler(result)
        }
    }

    private func handleSilentNotification(_ userInfo: [AnyHashable: Any]) async -> UIBackgroundFetchResult {

        guard let action = userInfo["action"] as? String else {
            return .noData
        }

        switch action {
        case "sync_data":
            return await syncDataInBackground()

        case "refresh_token":
            return await refreshAuthToken()

        case "update_badge":
            return await updateBadgeCount(userInfo)

        case "logout":
            return await handleRemoteLogout()

        case "clear_cache":
            return await clearLocalCache()

        default:
            return .noData
        }
    }

    private func syncDataInBackground() async -> UIBackgroundFetchResult {
        do {
            // Perform background sync
            try await DataSyncService.shared.sync()
            return .newData
        } catch {
            return .failed
        }
    }

    private func refreshAuthToken() async -> UIBackgroundFetchResult {
        do {
            try await AuthService.shared.refreshTokenIfNeeded()
            return .newData
        } catch {
            return .failed
        }
    }

    private func updateBadgeCount(_ userInfo: [AnyHashable: Any]) async -> UIBackgroundFetchResult {
        guard let count = userInfo["badge_count"] as? Int else {
            return .noData
        }

        do {
            try await UNUserNotificationCenter.current().setBadgeCount(count)
            return .newData
        } catch {
            return .failed
        }
    }

    private func handleRemoteLogout() async -> UIBackgroundFetchResult {
        await AuthService.shared.logout()
        return .newData
    }

    private func clearLocalCache() async -> UIBackgroundFetchResult {
        await CacheManager.shared.clearAll()
        return .newData
    }
}

// MARK: - Placeholder Services

enum DataSyncService {
    static let shared = DataSyncServiceImpl()
}

class DataSyncServiceImpl {
    func sync() async throws {}
}

enum AuthService {
    static let shared = AuthServiceImpl()
}

class AuthServiceImpl {
    func refreshTokenIfNeeded() async throws {}
    func logout() async {}
}

enum CacheManager {
    static let shared = CacheManagerImpl()
}

class CacheManagerImpl {
    func clearAll() async {}
}
```

## Notification Content Extension

```swift
// NotificationContentExtension/NotificationViewController.swift

import UIKit
import UserNotifications
import UserNotificationsUI

class NotificationViewController: UIViewController, UNNotificationContentExtension {

    @IBOutlet weak var imageView: UIImageView!
    @IBOutlet weak var titleLabel: UILabel!
    @IBOutlet weak var subtitleLabel: UILabel!
    @IBOutlet weak var bodyLabel: UILabel!
    @IBOutlet weak var actionButton: UIButton!

    private var notificationContent: UNNotificationContent?

    override func viewDidLoad() {
        super.viewDidLoad()
        setupUI()
    }

    func didReceive(_ notification: UNNotification) {
        notificationContent = notification.request.content

        titleLabel.text = notification.request.content.title
        subtitleLabel.text = notification.request.content.subtitle
        bodyLabel.text = notification.request.content.body

        // Load custom content
        if let userInfo = notification.request.content.userInfo as? [String: Any] {
            loadCustomContent(from: userInfo)
        }

        // Load attachment
        if let attachment = notification.request.content.attachments.first {
            loadAttachment(attachment)
        }
    }

    func didReceive(
        _ response: UNNotificationResponse,
        completionHandler completion: @escaping (UNNotificationContentExtensionResponseOption) -> Void
    ) {
        switch response.actionIdentifier {
        case "LIKE_ACTION":
            handleLikeAction(completion: completion)

        case "REPLY_ACTION":
            if let textResponse = response as? UNTextInputNotificationResponse {
                handleReplyAction(text: textResponse.userText, completion: completion)
            } else {
                completion(.dismissAndForwardAction)
            }

        default:
            completion(.dismissAndForwardAction)
        }
    }

    private func setupUI() {
        // Configure UI elements
        imageView.layer.cornerRadius = 8
        imageView.clipsToBounds = true
    }

    private func loadCustomContent(from userInfo: [String: Any]) {
        // Load additional content from userInfo
        if let mediaType = userInfo["media_type"] as? String {
            switch mediaType {
            case "image":
                // Already handled by attachments
                break
            case "video":
                setupVideoPlayer(userInfo: userInfo)
            case "map":
                setupMapView(userInfo: userInfo)
            default:
                break
            }
        }
    }

    private func loadAttachment(_ attachment: UNNotificationAttachment) {
        guard attachment.url.startAccessingSecurityScopedResource() else { return }
        defer { attachment.url.stopAccessingSecurityScopedResource() }

        if let data = try? Data(contentsOf: attachment.url),
           let image = UIImage(data: data) {
            imageView.image = image
        }
    }

    private func setupVideoPlayer(userInfo: [String: Any]) {
        // Setup video player for rich notifications
    }

    private func setupMapView(userInfo: [String: Any]) {
        // Setup map view for location notifications
    }

    private func handleLikeAction(
        completion: @escaping (UNNotificationContentExtensionResponseOption) -> Void
    ) {
        // Animate like action
        UIView.animate(withDuration: 0.3) {
            self.actionButton.transform = CGAffineTransform(scaleX: 1.3, y: 1.3)
        } completion: { _ in
            UIView.animate(withDuration: 0.2) {
                self.actionButton.transform = .identity
            }

            // Perform like action
            // ...

            completion(.doNotDismiss)
        }
    }

    private func handleReplyAction(
        text: String,
        completion: @escaping (UNNotificationContentExtensionResponseOption) -> Void
    ) {
        // Send reply
        // ...

        completion(.dismiss)
    }
}
```
