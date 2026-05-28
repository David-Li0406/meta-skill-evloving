# iOS Integration Reference

This guide covers integrating Flutter applications with iOS-specific features, including Swift/Objective-C development, native API access, CocoaPods configuration, and iOS platform conventions.

## Overview

Flutter iOS integration enables you to access iOS-specific APIs, use native frameworks, and implement features that require platform-specific code. iOS integration primarily uses Swift (recommended) or Objective-C for native code.

### iOS Project Structure

```
ios/
├── Runner/
│   ├── AppDelegate.swift          # App lifecycle and Flutter setup
│   ├── Runner-Bridging-Header.h   # Objective-C/Swift bridging
│   ├── Info.plist                 # App configuration
│   ├── Assets.xcassets/           # Images and assets
│   └── Base.lproj/                # Localized resources
├── Runner.xcodeproj/              # Xcode project file
├── Runner.xcworkspace/            # Xcode workspace (use this!)
├── Podfile                        # CocoaPods dependencies
└── Pods/                          # Installed CocoaPods
```

## Getting Started

### AppDelegate Setup

The AppDelegate is the entry point for Flutter on iOS and where you register platform channels and plugins.

#### Swift Implementation

```swift
import UIKit
import Flutter

@UIApplicationMain
@objc class AppDelegate: FlutterAppDelegate {
    private var batteryChannel: FlutterMethodChannel?
    private var locationChannel: FlutterEventChannel?

    override func application(
        _ application: UIApplication,
        didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?
    ) -> Bool {
        let controller = window?.rootViewController as! FlutterViewController

        // Setup method channel
        batteryChannel = FlutterMethodChannel(
            name: "com.example.app/battery",
            binaryMessenger: controller.binaryMessenger
        )
        batteryChannel?.setMethodCallHandler { [weak self] (call, result) in
            self?.handleMethodCall(call: call, result: result)
        }

        // Setup event channel
        locationChannel = FlutterEventChannel(
            name: "com.example.app/location",
            binaryMessenger: controller.binaryMessenger
        )
        locationChannel?.setStreamHandler(LocationStreamHandler())

        GeneratedPluginRegistrant.register(with: self)
        return super.application(application, didFinishLaunchingWithOptions: launchOptions)
    }

    private func handleMethodCall(call: FlutterMethodCall, result: @escaping FlutterResult) {
        switch call.method {
        case "getBatteryLevel":
            getBatteryLevel(result: result)
        case "setPowerSaveMode":
            if let args = call.arguments as? [String: Any],
               let enabled = args["enabled"] as? Bool {
                setPowerSaveMode(enabled: enabled, result: result)
            } else {
                result(FlutterError(
                    code: "INVALID_ARGUMENT",
                    message: "enabled argument required",
                    details: nil
                ))
            }
        default:
            result(FlutterMethodNotImplemented)
        }
    }

    private func getBatteryLevel(result: FlutterResult) {
        let device = UIDevice.current
        device.isBatteryMonitoringEnabled = true

        if device.batteryState == .unknown {
            result(FlutterError(
                code: "UNAVAILABLE",
                message: "Battery level not available",
                details: nil
            ))
        } else {
            let batteryLevel = Int(device.batteryLevel * 100)
            result(batteryLevel)
        }
    }

    private func setPowerSaveMode(enabled: Bool, result: FlutterResult) {
        // Low Power Mode can only be enabled by user in iOS
        // We can check if it's enabled
        if ProcessInfo.processInfo.isLowPowerModeEnabled {
            result(true)
        } else {
            result(false)
        }
    }
}
```

#### Objective-C Implementation

```objc
#import "AppDelegate.h"
#import "GeneratedPluginRegistrant.h"

@interface AppDelegate ()
@property (nonatomic, strong) FlutterMethodChannel *batteryChannel;
@property (nonatomic, strong) FlutterEventChannel *locationChannel;
@end

@implementation AppDelegate

- (BOOL)application:(UIApplication *)application
    didFinishLaunchingWithOptions:(NSDictionary *)launchOptions {
    FlutterViewController* controller =
        (FlutterViewController*)self.window.rootViewController;

    self.batteryChannel = [FlutterMethodChannel
        methodChannelWithName:@"com.example.app/battery"
        binaryMessenger:controller.binaryMessenger];

    __weak typeof(self) weakSelf = self;
    [self.batteryChannel setMethodCallHandler:^(FlutterMethodCall* call,
                                                 FlutterResult result) {
        [weakSelf handleMethodCall:call result:result];
    }];

    self.locationChannel = [FlutterEventChannel
        eventChannelWithName:@"com.example.app/location"
        binaryMessenger:controller.binaryMessenger];

    LocationStreamHandler *handler = [[LocationStreamHandler alloc] init];
    [self.locationChannel setStreamHandler:handler];

    [GeneratedPluginRegistrant registerWithRegistry:self];
    return [super application:application didFinishLaunchingWithOptions:launchOptions];
}

- (void)handleMethodCall:(FlutterMethodCall*)call result:(FlutterResult)result {
    if ([@"getBatteryLevel" isEqualToString:call.method]) {
        [self getBatteryLevel:result];
    } else if ([@"setPowerSaveMode" isEqualToString:call.method]) {
        NSDictionary* args = call.arguments;
        NSNumber* enabled = args[@"enabled"];
        [self setPowerSaveMode:[enabled boolValue] result:result];
    } else {
        result(FlutterMethodNotImplemented);
    }
}

- (void)getBatteryLevel:(FlutterResult)result {
    UIDevice* device = [UIDevice currentDevice];
    device.batteryMonitoringEnabled = YES;

    if (device.batteryState == UIDeviceBatteryStateUnknown) {
        result([FlutterError errorWithCode:@"UNAVAILABLE"
                                   message:@"Battery level not available"
                                   details:nil]);
    } else {
        int batteryLevel = (int)(device.batteryLevel * 100);
        result(@(batteryLevel));
    }
}

- (void)setPowerSaveMode:(BOOL)enabled result:(FlutterResult)result {
    // Check if low power mode is enabled
    BOOL isLowPowerMode = [[NSProcessInfo processInfo] isLowPowerModeEnabled];
    result(@(isLowPowerMode));
}

@end
```

## Accessing iOS APIs

### Battery Information Service

```swift
import UIKit

class BatteryService {
    static let shared = BatteryService()
    private let device = UIDevice.current

    init() {
        device.isBatteryMonitoringEnabled = true
    }

    func getBatteryLevel() -> Int {
        return Int(device.batteryLevel * 100)
    }

    func getBatteryState() -> String {
        switch device.batteryState {
        case .unknown:
            return "unknown"
        case .unplugged:
            return "unplugged"
        case .charging:
            return "charging"
        case .full:
            return "full"
        @unknown default:
            return "unknown"
        }
    }

    func getBatteryInfo() -> [String: Any] {
        return [
            "level": getBatteryLevel(),
            "state": getBatteryState(),
            "isCharging": device.batteryState == .charging || device.batteryState == .full
        ]
    }

    func startMonitoring(callback: @escaping ([String: Any]) -> Void) {
        NotificationCenter.default.addObserver(
            forName: UIDevice.batteryLevelDidChangeNotification,
            object: nil,
            queue: .main
        ) { [weak self] _ in
            guard let self = self else { return }
            callback(self.getBatteryInfo())
        }

        NotificationCenter.default.addObserver(
            forName: UIDevice.batteryStateDidChangeNotification,
            object: nil,
            queue: .main
        ) { [weak self] _ in
            guard let self = self else { return }
            callback(self.getBatteryInfo())
        }
    }

    func stopMonitoring() {
        NotificationCenter.default.removeObserver(
            self,
            name: UIDevice.batteryLevelDidChangeNotification,
            object: nil
        )
        NotificationCenter.default.removeObserver(
            self,
            name: UIDevice.batteryStateDidChangeNotification,
            object: nil
        )
    }

    deinit {
        stopMonitoring()
    }
}
```

### File System Access

```swift
import Foundation

class FileService {
    private let fileManager = FileManager.default

    func getDocumentsDirectory() -> URL {
        return fileManager.urls(for: .documentDirectory, in: .userDomainMask)[0]
    }

    func writeFile(fileName: String, content: String) throws {
        let fileURL = getDocumentsDirectory().appendingPathComponent(fileName)
        try content.write(to: fileURL, atomically: true, encoding: .utf8)
    }

    func readFile(fileName: String) throws -> String {
        let fileURL = getDocumentsDirectory().appendingPathComponent(fileName)
        return try String(contentsOf: fileURL, encoding: .utf8)
    }

    func deleteFile(fileName: String) throws {
        let fileURL = getDocumentsDirectory().appendingPathComponent(fileName)
        try fileManager.removeItem(at: fileURL)
    }

    func listFiles() throws -> [String] {
        let documentsURL = getDocumentsDirectory()
        let fileURLs = try fileManager.contentsOfDirectory(
            at: documentsURL,
            includingPropertiesForKeys: nil
        )
        return fileURLs.map { $0.lastPathComponent }
    }

    func fileExists(fileName: String) -> Bool {
        let fileURL = getDocumentsDirectory().appendingPathComponent(fileName)
        return fileManager.fileExists(atPath: fileURL.path)
    }

    func getFileSize(fileName: String) throws -> Int64 {
        let fileURL = getDocumentsDirectory().appendingPathComponent(fileName)
        let attributes = try fileManager.attributesOfItem(atPath: fileURL.path)
        return attributes[.size] as? Int64 ?? 0
    }
}
```

### Location Services

```swift
import CoreLocation

class LocationService: NSObject, CLLocationManagerDelegate {
    private let locationManager = CLLocationManager()
    private var locationCallback: (([String: Double]) -> Void)?
    private var errorCallback: ((String) -> Void)?

    override init() {
        super.init()
        locationManager.delegate = self
        locationManager.desiredAccuracy = kCLLocationAccuracyBest
    }

    func requestPermission() {
        locationManager.requestWhenInUseAuthorization()
    }

    func startUpdates(
        onLocation: @escaping ([String: Double]) -> Void,
        onError: @escaping (String) -> Void
    ) {
        self.locationCallback = onLocation
        self.errorCallback = onError
        locationManager.startUpdatingLocation()
    }

    func stopUpdates() {
        locationManager.stopUpdatingLocation()
        locationCallback = nil
        errorCallback = nil
    }

    // CLLocationManagerDelegate methods
    func locationManager(
        _ manager: CLLocationManager,
        didUpdateLocations locations: [CLLocation]
    ) {
        guard let location = locations.last else { return }

        let locationData: [String: Double] = [
            "latitude": location.coordinate.latitude,
            "longitude": location.coordinate.longitude,
            "altitude": location.altitude,
            "accuracy": location.horizontalAccuracy,
            "speed": location.speed,
            "heading": location.course
        ]

        locationCallback?(locationData)
    }

    func locationManager(
        _ manager: CLLocationManager,
        didFailWithError error: Error
    ) {
        errorCallback?(error.localizedDescription)
    }

    func locationManager(
        _ manager: CLLocationManager,
        didChangeAuthorization status: CLAuthorizationStatus
    ) {
        switch status {
        case .notDetermined:
            requestPermission()
        case .restricted, .denied:
            errorCallback?("Location permission denied")
        case .authorizedWhenInUse, .authorizedAlways:
            // Permission granted
            break
        @unknown default:
            break
        }
    }
}
```

### Camera Access

```swift
import AVFoundation
import UIKit

class CameraService: NSObject {
    func checkCameraPermission() -> Bool {
        let status = AVCaptureDevice.authorizationStatus(for: .video)
        return status == .authorized
    }

    func requestCameraPermission(completion: @escaping (Bool) -> Void) {
        AVCaptureDevice.requestAccess(for: .video) { granted in
            DispatchQueue.main.async {
                completion(granted)
            }
        }
    }

    func hasCamera() -> Bool {
        return UIImagePickerController.isSourceTypeAvailable(.camera)
    }

    func hasFrontCamera() -> Bool {
        return UIImagePickerController.isCameraDeviceAvailable(.front)
    }

    func hasRearCamera() -> Bool {
        return UIImagePickerController.isCameraDeviceAvailable(.rear)
    }

    func hasFlash() -> Bool {
        guard let device = AVCaptureDevice.default(for: .video) else {
            return false
        }
        return device.hasTorch && device.hasFlash
    }

    func setFlashlight(enabled: Bool) throws {
        guard let device = AVCaptureDevice.default(for: .video),
              device.hasTorch else {
            throw CameraError.flashNotAvailable
        }

        try device.lockForConfiguration()
        device.torchMode = enabled ? .on : .off
        device.unlockForConfiguration()
    }
}

enum CameraError: Error {
    case flashNotAvailable
    case cameraNotAvailable
    case permissionDenied
}
```

## Permissions

### Info.plist Configuration

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <!-- Camera -->
    <key>NSCameraUsageDescription</key>
    <string>This app needs camera access to take photos</string>

    <!-- Photo Library -->
    <key>NSPhotoLibraryUsageDescription</key>
    <string>This app needs photo library access to select photos</string>
    <key>NSPhotoLibraryAddUsageDescription</key>
    <string>This app needs permission to save photos</string>

    <!-- Location -->
    <key>NSLocationWhenInUseUsageDescription</key>
    <string>This app needs location access to show your position</string>
    <key>NSLocationAlwaysUsageDescription</key>
    <string>This app needs location access to track your route</string>
    <key>NSLocationAlwaysAndWhenInUseUsageDescription</key>
    <string>This app needs location access to track your route</string>

    <!-- Microphone -->
    <key>NSMicrophoneUsageDescription</key>
    <string>This app needs microphone access to record audio</string>

    <!-- Contacts -->
    <key>NSContactsUsageDescription</key>
    <string>This app needs contacts access to select recipients</string>

    <!-- Calendar -->
    <key>NSCalendarsUsageDescription</key>
    <string>This app needs calendar access to schedule events</string>

    <!-- Reminders -->
    <key>NSRemindersUsageDescription</key>
    <string>This app needs reminders access to create tasks</string>

    <!-- Motion -->
    <key>NSMotionUsageDescription</key>
    <string>This app needs motion access to track activity</string>

    <!-- Bluetooth -->
    <key>NSBluetoothAlwaysUsageDescription</key>
    <string>This app needs Bluetooth access to connect to devices</string>
    <key>NSBluetoothPeripheralUsageDescription</key>
    <string>This app needs Bluetooth access to connect to devices</string>

    <!-- Face ID -->
    <key>NSFaceIDUsageDescription</key>
    <string>This app uses Face ID for authentication</string>
</dict>
</plist>
```

### Runtime Permission Handling

```swift
import Photos
import AVFoundation
import CoreLocation

class PermissionService {
    enum PermissionType {
        case camera
        case photoLibrary
        case locationWhenInUse
        case locationAlways
        case microphone
    }

    func checkPermission(_ type: PermissionType) -> Bool {
        switch type {
        case .camera:
            return AVCaptureDevice.authorizationStatus(for: .video) == .authorized
        case .photoLibrary:
            return PHPhotoLibrary.authorizationStatus() == .authorized
        case .locationWhenInUse, .locationAlways:
            return CLLocationManager.authorizationStatus() == .authorizedWhenInUse ||
                   CLLocationManager.authorizationStatus() == .authorizedAlways
        case .microphone:
            return AVAudioSession.sharedInstance().recordPermission == .granted
        }
    }

    func requestPermission(
        _ type: PermissionType,
        completion: @escaping (Bool) -> Void
    ) {
        switch type {
        case .camera:
            AVCaptureDevice.requestAccess(for: .video) { granted in
                DispatchQueue.main.async {
                    completion(granted)
                }
            }

        case .photoLibrary:
            PHPhotoLibrary.requestAuthorization { status in
                DispatchQueue.main.async {
                    completion(status == .authorized)
                }
            }

        case .locationWhenInUse:
            let manager = CLLocationManager()
            manager.requestWhenInUseAuthorization()
            // Note: Actual result comes through delegate

        case .locationAlways:
            let manager = CLLocationManager()
            manager.requestAlwaysAuthorization()
            // Note: Actual result comes through delegate

        case .microphone:
            AVAudioSession.sharedInstance().requestRecordPermission { granted in
                DispatchQueue.main.async {
                    completion(granted)
                }
            }
        }
    }

    func openSettings() {
        if let url = URL(string: UIApplication.openSettingsURLString) {
            UIApplication.shared.open(url)
        }
    }
}
```

## CocoaPods Configuration

### Podfile

```ruby
# Podfile
platform :ios, '12.0'

# Use frameworks for Swift compatibility
use_frameworks!

# Prevent CocoaPods from embedding Swift libraries
ENV['COCOAPODS_DISABLE_STATS'] = 'true'

project 'Runner', {
  'Debug' => :debug,
  'Profile' => :release,
  'Release' => :release,
}

def flutter_root
  generated_xcode_build_settings_path = File.expand_path(
    File.join('..', 'Flutter', 'Generated.xcconfig'),
    __FILE__
  )
  unless File.exist?(generated_xcode_build_settings_path)
    raise "#{generated_xcode_build_settings_path} must exist."
  end

  File.foreach(generated_xcode_build_settings_path) do |line|
    matches = line.match(/FLUTTER_ROOT\=(.*)/)
    return matches[1].strip if matches
  end
  raise "FLUTTER_ROOT not found in #{generated_xcode_build_settings_path}."
end

require File.expand_path(File.join('packages', 'flutter_tools', 'bin', 'podhelper'), flutter_root)

flutter_ios_podfile_setup

target 'Runner' do
  use_modular_headers!

  flutter_install_all_ios_pods File.dirname(File.realpath(__FILE__))

  # Add custom pods here
  pod 'Alamofire', '~> 5.8'
  pod 'SDWebImage', '~> 5.18'
  pod 'SnapKit', '~> 5.7'
end

post_install do |installer|
  installer.pods_project.targets.each do |target|
    flutter_additional_ios_build_settings(target)

    # Set minimum deployment target
    target.build_configurations.each do |config|
      config.build_settings['IPHONEOS_DEPLOYMENT_TARGET'] = '12.0'
    end
  end
end
```

### Installing Pods

```bash
cd ios
pod install
pod update  # To update dependencies
```

## Background Processing

### Background Fetch

```swift
import UIKit
import BackgroundTasks

class AppDelegate: FlutterAppDelegate {
    private let backgroundTaskIdentifier = "com.example.app.refresh"

    override func application(
        _ application: UIApplication,
        didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?
    ) -> Bool {
        // Register background task
        BGTaskScheduler.shared.register(
            forTaskWithIdentifier: backgroundTaskIdentifier,
            using: nil
        ) { task in
            self.handleBackgroundTask(task: task as! BGAppRefreshTask)
        }

        GeneratedPluginRegistrant.register(with: self)
        return super.application(application, didFinishLaunchingWithOptions: launchOptions)
    }

    func scheduleBackgroundTask() {
        let request = BGAppRefreshTaskRequest(identifier: backgroundTaskIdentifier)
        request.earliestBeginDate = Date(timeIntervalSinceNow: 15 * 60) // 15 minutes

        do {
            try BGTaskScheduler.shared.submit(request)
        } catch {
            print("Could not schedule background task: \(error)")
        }
    }

    private func handleBackgroundTask(task: BGAppRefreshTask) {
        scheduleBackgroundTask() // Schedule next refresh

        let queue = OperationQueue()
        queue.maxConcurrentOperationCount = 1

        let operation = BackgroundSyncOperation()

        task.expirationHandler = {
            queue.cancelAllOperations()
        }

        operation.completionBlock = {
            task.setTaskCompleted(success: !operation.isCancelled)
        }

        queue.addOperation(operation)
    }
}

class BackgroundSyncOperation: Operation {
    override func main() {
        guard !isCancelled else { return }

        // Perform background work
        performSync()
    }

    private func performSync() {
        // Implementation
    }
}
```

Add to Info.plist:

```xml
<key>BGTaskSchedulerPermittedIdentifiers</key>
<array>
    <string>com.example.app.refresh</string>
</array>
```

### Location Updates in Background

```swift
import CoreLocation

class BackgroundLocationManager: NSObject, CLLocationManagerDelegate {
    private let locationManager = CLLocationManager()

    override init() {
        super.init()
        locationManager.delegate = self
        locationManager.desiredAccuracy = kCLLocationAccuracyBest
        locationManager.allowsBackgroundLocationUpdates = true
        locationManager.pausesLocationUpdatesAutomatically = false
        locationManager.showsBackgroundLocationIndicator = true
    }

    func startTracking() {
        locationManager.startUpdatingLocation()
    }

    func stopTracking() {
        locationManager.stopUpdatingLocation()
    }

    func locationManager(
        _ manager: CLLocationManager,
        didUpdateLocations locations: [CLLocation]
    ) {
        // Handle location updates
        guard let location = locations.last else { return }
        print("Background location: \(location.coordinate)")
    }
}
```

Add to Info.plist:

```xml
<key>UIBackgroundModes</key>
<array>
    <string>location</string>
</array>
```

## Native Views (Platform Views)

### Creating Custom iOS View

```swift
import Flutter
import UIKit

class CustomNativeView: NSObject, FlutterPlatformView {
    private let frame: CGRect
    private let viewId: Int64
    private let label: UILabel

    init(
        frame: CGRect,
        viewId: Int64,
        arguments: Any?,
        binaryMessenger: FlutterBinaryMessenger
    ) {
        self.frame = frame
        self.viewId = viewId

        // Create native UIView
        self.label = UILabel(frame: frame)
        self.label.textAlignment = .center
        self.label.backgroundColor = .systemBlue
        self.label.textColor = .white

        // Parse arguments
        if let args = arguments as? [String: Any],
           let text = args["text"] as? String {
            self.label.text = text
        } else {
            self.label.text = "Native iOS View"
        }

        super.init()
    }

    func view() -> UIView {
        return label
    }

    func updateText(_ text: String) {
        label.text = text
    }
}
```

### Factory and Registration

```swift
import Flutter

class CustomNativeViewFactory: NSObject, FlutterPlatformViewFactory {
    private let messenger: FlutterBinaryMessenger

    init(messenger: FlutterBinaryMessenger) {
        self.messenger = messenger
        super.init()
    }

    func create(
        withFrame frame: CGRect,
        viewIdentifier viewId: Int64,
        arguments args: Any?
    ) -> FlutterPlatformView {
        return CustomNativeView(
            frame: frame,
            viewId: viewId,
            arguments: args,
            binaryMessenger: messenger
        )
    }

    func createArgsCodec() -> FlutterMessageCodec & NSObjectProtocol {
        return FlutterStandardMessageCodec.sharedInstance()
    }
}

// In AppDelegate
override func application(
    _ application: UIApplication,
    didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?
) -> Bool {
    let controller = window?.rootViewController as! FlutterViewController

    let factory = CustomNativeViewFactory(
        messenger: controller.binaryMessenger
    )

    registrar(forPlugin: "CustomNativeView")?.register(
        factory,
        withId: "custom-native-view"
    )

    GeneratedPluginRegistrant.register(with: self)
    return super.application(application, didFinishLaunchingWithOptions: launchOptions)
}
```

## Async/Await and Concurrency

### Modern Swift Concurrency

```swift
class NetworkService {
    func fetchData() async throws -> String {
        let url = URL(string: "https://api.example.com/data")!
        let (data, _) = try await URLSession.shared.data(from: url)
        return String(data: data, encoding: .utf8) ?? ""
    }

    func handleFlutterCall(call: FlutterMethodCall, result: @escaping FlutterResult) {
        Task {
            do {
                let data = try await fetchData()
                result(data)
            } catch {
                result(FlutterError(
                    code: "NETWORK_ERROR",
                    message: error.localizedDescription,
                    details: nil
                ))
            }
        }
    }
}
```

### Combining with Platform Channels

```swift
class DataService {
    private let channel: FlutterMethodChannel

    init(binaryMessenger: FlutterBinaryMessenger) {
        channel = FlutterMethodChannel(
            name: "com.example.app/data",
            binaryMessenger: binaryMessenger
        )

        channel.setMethodCallHandler { [weak self] call, result in
            self?.handleMethodCall(call: call, result: result)
        }
    }

    private func handleMethodCall(
        call: FlutterMethodCall,
        result: @escaping FlutterResult
    ) {
        Task {
            do {
                switch call.method {
                case "fetchData":
                    let data = try await self.fetchData()
                    result(data)
                case "processData":
                    if let args = call.arguments as? [String: Any],
                       let input = args["input"] as? String {
                        let processed = try await self.processData(input)
                        result(processed)
                    } else {
                        result(FlutterError(
                            code: "INVALID_ARGUMENT",
                            message: "input required",
                            details: nil
                        ))
                    }
                default:
                    result(FlutterMethodNotImplemented)
                }
            } catch {
                result(FlutterError(
                    code: "ERROR",
                    message: error.localizedDescription,
                    details: nil
                ))
            }
        }
    }

    private func fetchData() async throws -> [String: Any] {
        // Async implementation
        try await Task.sleep(nanoseconds: 1_000_000_000)
        return ["status": "success", "data": "Sample data"]
    }

    private func processData(_ input: String) async throws -> String {
        // Async processing
        try await Task.sleep(nanoseconds: 500_000_000)
        return "Processed: \(input)"
    }
}
```

## Testing

### Unit Testing Swift Code

```swift
import XCTest
@testable import Runner

class BatteryServiceTests: XCTestCase {
    var batteryService: BatteryService!

    override func setUp() {
        super.setUp()
        batteryService = BatteryService.shared
    }

    override func tearDown() {
        batteryService = nil
        super.tearDown()
    }

    func testGetBatteryLevel() {
        let level = batteryService.getBatteryLevel()
        XCTAssertGreaterThanOrEqual(level, 0)
        XCTAssertLessThanOrEqual(level, 100)
    }

    func testGetBatteryState() {
        let state = batteryService.getBatteryState()
        let validStates = ["unknown", "unplugged", "charging", "full"]
        XCTAssertTrue(validStates.contains(state))
    }

    func testGetBatteryInfo() {
        let info = batteryService.getBatteryInfo()
        XCTAssertNotNil(info["level"])
        XCTAssertNotNil(info["state"])
        XCTAssertNotNil(info["isCharging"])
    }
}
```

### Async Testing

```swift
class NetworkServiceTests: XCTestCase {
    func testFetchData() async throws {
        let service = NetworkService()

        let data = try await service.fetchData()

        XCTAssertFalse(data.isEmpty)
    }

    func testFetchDataError() async {
        let service = NetworkService()

        do {
            _ = try await service.fetchInvalidEndpoint()
            XCTFail("Should have thrown error")
        } catch {
            // Expected error
            XCTAssertTrue(true)
        }
    }
}
```

## Best Practices

### Memory Management
- Use `weak self` in closures to avoid retain cycles
- Clean up observers in deinit
- Release resources properly
- Use `@escaping` for async callbacks

### Threading
- Use GCD or modern Swift concurrency for async work
- Return results on main thread for UI updates
- Use `DispatchQueue.main.async` when needed

### Error Handling
- Use Swift's error handling with throw/try/catch
- Provide detailed FlutterError responses
- Log errors for debugging

### Performance
- Profile with Instruments
- Optimize image loading and caching
- Minimize main thread work
- Use lazy initialization

### Security
- Validate all inputs from Flutter
- Use Keychain for sensitive data
- Enable App Transport Security
- Follow Apple security guidelines

## Related Resources

- [Platform Channels](platform-channels.md)
- [Android Integration](android-integration.md)
- [Plugin Development](plugin-development.md)
