# Ios Swift Specialist - Sharp Edges

## Force Unwrap Crash

### **Id**
force-unwrap-crash
### **Summary**
Force unwrap crashes in production when value is nil
### **Severity**
critical
### **Situation**
Accessing optional values
### **Why**
  let name = user!.name crashes instantly if user is nil. In development,
  data is often complete. In production, partial data, race conditions,
  and API changes cause nils you didn't expect. App crashes, 1-star reviews.
  
### **Solution**
  1. Use guard-let for early return:
     guard let user = user else {
         logger.error("User was nil")
         return
     }
     // user is now non-optional
  
  2. Use if-let for optional handling:
     if let name = user?.name {
         label.text = name
     } else {
         label.text = "Guest"
     }
  
  3. Use nil coalescing for defaults:
     let name = user?.name ?? "Unknown"
  
  4. Use optional chaining:
     let city = user?.address?.city  // nil if any is nil
  
  5. Reserve ! only for:
     - IBOutlets (after viewDidLoad)
     - Truly programmer errors that should crash
  
### **Symptoms**
  - EXC_BAD_INSTRUCTION crashes
  - Crash logs with "unexpectedly found nil"
  - Works in testing, crashes in production
### **Detection Pattern**
(?<!!)\!(?![=!])|\.unwrap\(\)

## Retain Cycle Closure

### **Id**
retain-cycle-closure
### **Summary**
Strong self in closure causes memory leak
### **Severity**
high
### **Situation**
Closures stored on objects
### **Why**
  self.completion = { self.doSomething() } creates a cycle: object owns
  closure, closure owns object. Neither can deallocate. Memory grows,
  resources stay open, app eventually crashes.
  
### **Solution**
  1. Use [weak self] for most cases:
     self.completion = { [weak self] in
         guard let self = self else { return }
         self.doSomething()
     }
  
  2. Use [unowned self] when lifecycle is guaranteed:
     // Only when you KNOW self will outlive closure
     self.shortLivedClosure = { [unowned self] in
         self.quickOperation()
     }
  
  3. For Combine, use .sink with store:
     cancellable = publisher
         .sink { [weak self] value in
             self?.handle(value)
         }
         .store(in: &cancellables)
  
  4. For async/await, check task cancellation:
     Task { [weak self] in
         guard let self = self else { return }
         await self.asyncOperation()
     }
  
### **Symptoms**
  - ViewControllers not deallocated
  - Memory grows when navigating
  - deinit never called
### **Detection Pattern**
\{ self\.|completion = \{(?!.*weak)

## Main Thread Ui

### **Id**
main-thread-ui
### **Summary**
UI updates from background thread cause crashes or corruption
### **Severity**
critical
### **Situation**
Updating UI after async operation
### **Why**
  UIKit is not thread-safe. Updating UI from background thread causes
  undefined behavior: crashes, visual glitches, or silent corruption.
  The symptoms may appear unrelated to the actual cause.
  
### **Solution**
  1. Use @MainActor for UI-related code:
     @MainActor
     class ViewController: UIViewController {
         // All methods run on main thread
     }
  
  2. Explicitly dispatch to main:
     Task {
         let data = await fetchData()
         await MainActor.run {
             self.updateUI(with: data)
         }
     }
  
  3. For completion handlers:
     fetchData { [weak self] result in
         DispatchQueue.main.async {
             self?.updateUI(result)
         }
     }
  
  4. Use Main Thread Checker in Xcode:
     Edit Scheme > Run > Diagnostics > Main Thread Checker
  
### **Symptoms**
  - Random UI crashes
  - Visual glitches
  - "UI API called from background thread" warning
### **Detection Pattern**
DispatchQueue\.global.*self\.|async.*self\.view

## Swiftui Body Side Effects

### **Id**
swiftui-body-side-effects
### **Summary**
Side effects in SwiftUI body cause infinite loops
### **Severity**
high
### **Situation**
SwiftUI view code
### **Why**
  SwiftUI calls body whenever state changes. If body triggers state
  change (setState, modify @Published), it creates infinite loop.
  View keeps re-rendering, UI freezes, 100% CPU.
  
### **Solution**
  1. Never modify state in body:
     // BAD - triggers re-render loop
     var body: some View {
         viewModel.loadData()  // DON'T!
         Text("Hello")
     }
  
     // GOOD - use onAppear
     var body: some View {
         Text("Hello")
             .onAppear { viewModel.loadData() }
     }
  
  2. Use .task for async:
     var body: some View {
         Text(data)
             .task { await viewModel.loadData() }
     }
  
  3. Derive values, don't compute with side effects:
     // GOOD - pure computation
     var displayName: String {
         user.firstName + " " + user.lastName
     }
  
  4. Use onChange for reactions:
     .onChange(of: selection) { newValue in
         // React to change here
     }
  
### **Symptoms**
  - UI freezes
  - 100% CPU usage
  - "Maximum update depth exceeded" (React analog)
### **Detection Pattern**
var body.*View.*@State|body.*ViewModel.*load

## Keychain Not Encrypted

### **Id**
keychain-not-encrypted
### **Summary**
Storing sensitive data in UserDefaults instead of Keychain
### **Severity**
critical
### **Situation**
Storing tokens, passwords, sensitive data
### **Why**
  UserDefaults is a plist file - readable by anyone with device access.
  Jailbroken devices, backups, device sharing - all expose the data.
  Tokens in UserDefaults = compromised accounts.
  
### **Solution**
  1. Use Keychain for sensitive data:
     import Security
  
     func saveToken(_ token: String) throws {
         let data = Data(token.utf8)
         let query: [String: Any] = [
             kSecClass as String: kSecClassGenericPassword,
             kSecAttrAccount as String: "auth_token",
             kSecValueData as String: data,
             kSecAttrAccessible as String:
                 kSecAttrAccessibleAfterFirstUnlock,
         ]
         SecItemDelete(query as CFDictionary)
         let status = SecItemAdd(query as CFDictionary, nil)
         guard status == errSecSuccess else {
             throw KeychainError.saveFailed(status)
         }
     }
  
  2. Use a Keychain wrapper library:
     import KeychainAccess
  
     let keychain = Keychain(service: "com.myapp")
     keychain["token"] = authToken
  
  3. Set appropriate accessibility:
     - kSecAttrAccessibleAfterFirstUnlock (most cases)
     - kSecAttrAccessibleWhenUnlocked (higher security)
     - kSecAttrAccessibleAlways (avoid - low security)
  
  4. Consider biometric protection for high-value data
  
### **Symptoms**
  - Security audit failures
  - App store rejection
  - Account compromises
### **Detection Pattern**
UserDefaults.*token|UserDefaults.*password|UserDefaults.*secret

## Async Task Cancellation

### **Id**
async-task-cancellation
### **Summary**
Async tasks continue after view dismissed
### **Severity**
medium
### **Situation**
Swift async/await in views
### **Why**
  Task { await longOperation() } continues even if view is dismissed.
  This wastes resources, may update deallocated state, or show stale
  data on return. SwiftUI .task modifier handles this; manual Tasks don't.
  
### **Solution**
  1. Use SwiftUI .task modifier (auto-cancels):
     Text("Data")
         .task {
             await loadData()  // Cancelled when view disappears
         }
  
  2. For UIKit, manage Task lifecycle:
     class ViewController: UIViewController {
         private var loadTask: Task<Void, Never>?
  
         override func viewWillAppear(_ animated: Bool) {
             super.viewWillAppear(animated)
             loadTask = Task { await loadData() }
         }
  
         override func viewWillDisappear(_ animated: Bool) {
             super.viewWillDisappear(animated)
             loadTask?.cancel()
         }
     }
  
  3. Check for cancellation in long operations:
     func loadData() async {
         for item in items {
             if Task.isCancelled { return }
             await process(item)
         }
     }
  
  4. Use withTaskCancellationHandler:
     await withTaskCancellationHandler {
         await longRunningOperation()
     } onCancel: {
         cleanup()
     }
  
### **Symptoms**
  - Network requests after view dismissed
  - Updates to stale state
  - Resource leaks
### **Detection Pattern**
Task \{(?!.*cancel)|Task\.init

## App Transport Security

### **Id**
app-transport-security
### **Summary**
ATS blocks HTTP requests, app appears broken
### **Severity**
medium
### **Situation**
Network requests to non-HTTPS endpoints
### **Why**
  App Transport Security blocks cleartext HTTP by default. If your
  API or third-party service uses HTTP, requests silently fail.
  App appears broken with no obvious error.
  
### **Solution**
  1. Prefer HTTPS always (real fix)
  
  2. For development, allow localhost:
     <key>NSAppTransportSecurity</key>
     <dict>
         <key>NSAllowsLocalNetworking</key>
         <true/>
     </dict>
  
  3. For specific domains (avoid in production):
     <key>NSAppTransportSecurity</key>
     <dict>
         <key>NSExceptionDomains</key>
         <dict>
             <key>legacy-api.example.com</key>
             <dict>
                 <key>NSExceptionAllowsInsecureHTTPLoads</key>
                 <true/>
             </dict>
         </dict>
     </dict>
  
  4. Check ATS errors:
     - Error: "The resource could not be loaded because the ATS policy..."
     - Fix: Update to HTTPS or add exception
  
### **Symptoms**
  - Network requests fail silently
  - Works in simulator (local), fails on device
  - Works with some URLs, not others
### **Detection Pattern**
http://(?!localhost)|NSAllowsArbitraryLoads.*true

## Core Data Threading

### **Id**
core-data-threading
### **Summary**
Core Data context accessed from wrong thread crashes
### **Severity**
critical
### **Situation**
Using Core Data in multi-threaded app
### **Why**
  NSManagedObjectContext is not thread-safe. Accessing a context or
  its objects from a different thread causes crashes, data corruption,
  or silent errors. Core Data threading bugs are notoriously hard to debug.
  
### **Solution**
  1. Always use context's perform/performAndWait:
     context.perform {
         let user = context.object(with: objectID)
         user.name = "New Name"
         try? context.save()
     }
  
  2. Use background context for heavy work:
     let bgContext = persistentContainer.newBackgroundContext()
     bgContext.perform {
         // Heavy work here
         try? bgContext.save()
     }
  
  3. Pass object IDs, not objects, between threads:
     // BAD
     let user = mainContext.fetch(...)
     Task { updateBackground(user) }  // Wrong thread!
  
     // GOOD
     let userID = user.objectID
     Task {
         let bgContext = container.newBackgroundContext()
         let bgUser = bgContext.object(with: userID)
         // Safe to use bgUser here
     }
  
  4. Use -com.apple.CoreData.ConcurrencyDebug 1 in launch args
  
### **Symptoms**
  - Random Core Data crashes
  - Data corruption
  - _PFArray mutated while being enumerated
### **Detection Pattern**
NSManagedObjectContext(?!.*perform)|\.objects\.first