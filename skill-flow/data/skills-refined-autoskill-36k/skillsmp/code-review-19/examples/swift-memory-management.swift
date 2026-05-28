// MARK: - Swift Code Review: Memory Management
// This file demonstrates memory management patterns for code review.

import SwiftUI
import Combine

// MARK: - Retain Cycles in Closures

class ClosureRetainCycleExample {
    var name = "Example"
    var onComplete: (() -> Void)?
    var cancellables = Set<AnyCancellable>()

    // BAD: Strong reference cycle
    func badSetup() {
        onComplete = {
            print(self.name)  // self is strongly captured
        }
    }

    // GOOD: Weak capture
    func goodSetup() {
        onComplete = { [weak self] in
            guard let self else { return }
            print(self.name)
        }
    }

    // GOOD: Capture only needed values
    func captureValuesSetup() {
        let name = self.name
        onComplete = {
            print(name)  // Only captures the string, not self
        }
    }

    // BAD: Retain cycle in Combine
    func badCombineSetup(publisher: AnyPublisher<String, Never>) {
        publisher
            .sink { value in
                self.handleValue(value)  // Strong reference
            }
            .store(in: &cancellables)
    }

    // GOOD: Weak self in Combine
    func goodCombineSetup(publisher: AnyPublisher<String, Never>) {
        publisher
            .sink { [weak self] value in
                self?.handleValue(value)
            }
            .store(in: &cancellables)
    }

    private func handleValue(_ value: String) {
        print(value)
    }
}

// MARK: - Timer Retain Cycles

class TimerExample {
    var timer: Timer?

    // BAD: Timer retains target strongly
    func badStartTimer() {
        timer = Timer.scheduledTimer(
            timeInterval: 1.0,
            target: self,
            selector: #selector(timerFired),
            userInfo: nil,
            repeats: true
        )
    }

    // GOOD: Use closure-based timer with weak capture
    func goodStartTimer() {
        timer = Timer.scheduledTimer(withTimeInterval: 1.0, repeats: true) { [weak self] _ in
            self?.timerFired()
        }
    }

    @objc private func timerFired() {
        print("Timer fired")
    }

    deinit {
        timer?.invalidate()
    }
}

// MARK: - Delegate Patterns

// BAD: Strong delegate reference
class BadNetworkManager {
    var delegate: NetworkDelegate?  // Should be weak!

    func fetchData() {
        // ... fetch data
        delegate?.didFetchData(Data())
    }
}

// GOOD: Weak delegate reference
class GoodNetworkManager {
    weak var delegate: NetworkDelegate?

    func fetchData() {
        // ... fetch data
        delegate?.didFetchData(Data())
    }
}

protocol NetworkDelegate: AnyObject {
    func didFetchData(_ data: Data)
}

// MARK: - Notification Center

class NotificationExample {
    // BAD: Old-style observer without removal
    func badSetup() {
        NotificationCenter.default.addObserver(
            self,
            selector: #selector(handleNotification),
            name: .someNotification,
            object: nil
        )
        // Never removed - potential crash after dealloc
    }

    // GOOD: Modern closure-based with proper cleanup
    private var notificationObserver: NSObjectProtocol?

    func goodSetup() {
        notificationObserver = NotificationCenter.default.addObserver(
            forName: .someNotification,
            object: nil,
            queue: .main
        ) { [weak self] notification in
            self?.handleNotification(notification)
        }
    }

    deinit {
        if let observer = notificationObserver {
            NotificationCenter.default.removeObserver(observer)
        }
    }

    @objc private func handleNotification(_ notification: Notification) {
        print("Notification received")
    }
}

extension Notification.Name {
    static let someNotification = Notification.Name("someNotification")
}

// MARK: - SwiftUI Memory Patterns

// BAD: Storing reference type in @State
class HeavyObject {
    var data: [Int] = Array(repeating: 0, count: 10000)
}

struct BadView: View {
    // This creates new HeavyObject on every view recreation
    @State private var heavy = HeavyObject()

    var body: some View {
        Text("Count: \(heavy.data.count)")
    }
}

// GOOD: Use @StateObject for reference types (pre-iOS 17)
struct GoodViewPreiOS17: View {
    @StateObject private var viewModel = ViewModel()

    var body: some View {
        Text("Count: \(viewModel.count)")
    }
}

class ViewModel: ObservableObject {
    @Published var count = 0
}

// GOOD: Use @State with @Observable (iOS 17+)
@Observable
class ModernViewModel {
    var count = 0
}

struct GoodViewiOS17: View {
    @State private var viewModel = ModernViewModel()

    var body: some View {
        Text("Count: \(viewModel.count)")
    }
}

// MARK: - Task Cancellation

@Observable
@MainActor
class TaskCancellationExample {
    var data: [String] = []
    private var currentTask: Task<Void, Never>?

    // BAD: Not cancelling previous task
    func loadDataBad() {
        Task {
            data = await fetchData()  // Previous task may still be running
        }
    }

    // GOOD: Cancel previous task
    func loadDataGood() {
        currentTask?.cancel()
        currentTask = Task {
            do {
                try Task.checkCancellation()
                data = await fetchData()
            } catch {
                // Task was cancelled
            }
        }
    }

    // Call this when view disappears
    func cleanup() {
        currentTask?.cancel()
    }

    private func fetchData() async -> [String] {
        []
    }
}

// MARK: - Proper Cleanup in Views

struct ProperCleanupView: View {
    @State private var viewModel = TaskCancellationExample()

    var body: some View {
        List(viewModel.data, id: \.self) { item in
            Text(item)
        }
        .task {
            // Automatically cancelled when view disappears
            await viewModel.loadDataGood()
        }
    }
}

// MARK: - Avoiding Unnecessary Allocations

class AllocationExample {
    // BAD: Creating formatter on every call
    func formatDateBad(_ date: Date) -> String {
        let formatter = DateFormatter()  // Expensive allocation
        formatter.dateStyle = .medium
        return formatter.string(from: date)
    }

    // GOOD: Reuse formatter
    private static let dateFormatter: DateFormatter = {
        let formatter = DateFormatter()
        formatter.dateStyle = .medium
        return formatter
    }()

    func formatDateGood(_ date: Date) -> String {
        Self.dateFormatter.string(from: date)
    }

    // BAD: Creating regex on every call
    func validateEmailBad(_ email: String) -> Bool {
        let pattern = "[A-Z0-9a-z._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,64}"
        return email.range(of: pattern, options: .regularExpression) != nil
    }

    // GOOD: Compile regex once
    private static let emailRegex = try? NSRegularExpression(
        pattern: "[A-Z0-9a-z._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,64}"
    )

    func validateEmailGood(_ email: String) -> Bool {
        guard let regex = Self.emailRegex else { return false }
        let range = NSRange(email.startIndex..., in: email)
        return regex.firstMatch(in: email, range: range) != nil
    }
}

// MARK: - Collection Memory

class CollectionMemoryExample {
    var items: [LargeItem] = []

    // BAD: Not reserving capacity for known size
    func populateBad(count: Int) {
        items = []
        for i in 0..<count {
            items.append(LargeItem(id: i))  // May trigger multiple reallocations
        }
    }

    // GOOD: Reserve capacity
    func populateGood(count: Int) {
        items = []
        items.reserveCapacity(count)
        for i in 0..<count {
            items.append(LargeItem(id: i))
        }
    }

    // BETTER: Use map
    func populateBetter(count: Int) {
        items = (0..<count).map { LargeItem(id: $0) }
    }
}

struct LargeItem {
    let id: Int
    let data: [Int] = Array(repeating: 0, count: 100)
}
