# WebViewBridge Reference

Complete API reference for WebViewBridge Swift package.

## WebViewBridge Class

```swift
@available(macOS 26.0, *)
@MainActor
public final class WebViewBridge: NSObject {
    // Properties
    public let handlerName: String
    public weak var delegate: WebViewBridgeDelegate?
    public var onMessage: ((_ type: String, _ data: [String: Any]) -> Void)?
    public var onLog: ((String) -> Void)?
    public weak var webPage: WebPage?
    public var isWebSocketConnected: Bool

    // Initialization
    public init(handlerName: String = "websocketBridge")

    // Module Management
    public func registerModule(_ module: JavaScriptModule)
    public func registerModules(_ modules: [JavaScriptModule])
    public func registerCoreModules()

    // Configuration
    public func configure(webPage: WebPage)
    public func configure(contentController: WKUserContentController)
    public func generateInjectionScript() -> String

    // JavaScript Execution
    public func callJavaScript(_ script: String) async throws -> Any?
    public func callJavaScript(_ script: String, in page: WebPage) async throws -> Any?

    // State
    public func reset()
}
```

## WebViewBridgeDelegate

```swift
@available(macOS 26.0, *)
public protocol WebViewBridgeDelegate: AnyObject {
    func bridge(_ bridge: WebViewBridge, didReceiveMessage type: String, data: [String: Any])
    func bridge(_ bridge: WebViewBridge, webSocketStatusChanged connected: Bool)
    func bridge(_ bridge: WebViewBridge, didEncounterError error: Error)
}
```

## JavaScriptModule

```swift
public struct JavaScriptModule: Sendable {
    public let name: String
    public let source: String
    public let injectAtStart: Bool
    public let mainFrameOnly: Bool

    public init(name: String, source: String, injectAtStart: Bool = true, mainFrameOnly: Bool = false)

    public static func fromBundle(named: String, bundle: Bundle = .main, subdirectory: String? = nil) -> JavaScriptModule?
}
```

## WebViewBridgeError

```swift
public enum WebViewBridgeError: LocalizedError {
    case webPageNotAvailable
    case javaScriptExecutionFailed(String)
}
```

## bridge-core.js API

### sendToSwift
```javascript
window.__bridgeCore.sendToSwift(type, data)
// Example: window.__bridgeCore.sendToSwift('click', {x: 100, y: 200})
```

### log
```javascript
window.__bridgeCore.log(message)
```

### Base64 Utilities
```javascript
const base64 = window.__bridgeCore.arrayBufferToBase64(arrayBuffer)
const buffer = window.__bridgeCore.base64ToArrayBuffer(base64String)
window.__bridgeCore.blobToBase64(blob, (base64) => { ... })
```

### WebSocket Interceptor
```javascript
window.__bridgeCore.installWebSocketInterceptor({
    shouldIntercept: function(url) {
        return url.includes('api.example.com')
    }
})
```

## Usage Patterns

### Complex Data Exchange
```swift
// Swift side
let script = """
    return JSON.stringify({
        url: location.href,
        title: document.title,
        forms: document.forms.length
    })
"""
if let json = try await bridge.callJavaScript(script) as? String,
   let data = try? JSONSerialization.jsonObject(with: Data(json.utf8)) {
    print(data)
}
```

### Error Handling
```swift
do {
    let result = try await bridge.callJavaScript("return someFunc()")
} catch WebViewBridgeError.webPageNotAvailable {
    print("WebPage not ready")
} catch {
    print("Error: \(error)")
}
```

### Inject at Document End
```swift
let module = JavaScriptModule(
    name: "dom-modifier",
    source: "document.body.style.background = 'blue'",
    injectAtStart: false  // Wait for DOM
)
```

## Message Flow

```
JavaScript                    Swift
    │                           │
    │  sendToSwift(type, data)  │
    │ ─────────────────────────>│
    │                           │ onMessage(type, data)
    │                           │
    │      callJavaScript()     │
    │ <─────────────────────────│
    │                           │
    │     return result         │
    │ ─────────────────────────>│
    │                           │
```
