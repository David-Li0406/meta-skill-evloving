# ViewModel Template

> Standalone ViewModel template cho MVVM.

---

## 📁 File Generated

| File | Path |
|------|------|
| `{Feature}ViewModel.swift` | `Presentation/{Feature}/{Feature}ViewModel.swift` |

---

## 🏗️ Template

```swift
import Foundation
import Combine

// MARK: - {Feature}ViewModel

/// ViewModel for {Feature} screen
class {Feature}ViewModel: ObservableObject {
    // MARK: - Published Properties
    
    /// Current status of the operation
    @Published var status: Status = .idle
    
    /// Error message to display
    @Published var errorMessage: String?
    
    /// Loading state
    @Published var isLoading: Bool = false
    
    // MARK: - Status Enum
    
    enum Status: Equatable {
        case idle
        case loading
        case success
        case error
    }
    
    // MARK: - Dependencies
    
    private let {featureLower}UseCase: {Feature}UseCaseProtocol
    private let analyticsService: AnalyticsServiceProtocol
    private let loggerService: LoggerServiceProtocol
    private var cancellables = Set<AnyCancellable>()
    
    // MARK: - Navigation Callbacks
    
    var onSuccess: (() -> Void)?
    var onCancel: (() -> Void)?
    
    // MARK: - Initialization
    
    /// Initialize with dependencies
    init(
        {featureLower}UseCase: {Feature}UseCaseProtocol,
        analyticsService: AnalyticsServiceProtocol,
        loggerService: LoggerServiceProtocol
    ) {
        self.{featureLower}UseCase = {featureLower}UseCase
        self.analyticsService = analyticsService
        self.loggerService = loggerService
        
        setupBindings()
    }
    
    /// Convenience init for production (uses Resolver)
    convenience init() {
        self.init(
            {featureLower}UseCase: Resolver.resolve(),
            analyticsService: Resolver.resolve(),
            loggerService: Resolver.resolve()
        )
    }
    
    // MARK: - Setup
    
    private func setupBindings() {
        // Example: Reactive validation
        // $inputValue
        //   .debounce(for: 0.3, scheduler: DispatchQueue.main)
        //   .removeDuplicates()
        //   .sink { [weak self] value in
        //     self?.validate(value)
        //   }
        //   .store(in: &cancellables)
    }
    
    // MARK: - Actions
    
    /// Perform main action
    func performAction() async {
        status = .loading
        isLoading = true
        errorMessage = nil
        
        defer {
            isLoading = false
        }
        
        do {
            loggerService.log("Starting {feature} action")
            
            try await {featureLower}UseCase.execute()
            
            status = .success
            
            await analyticsService.track(event: .{featureLower}Success)
            
            onSuccess?()
        } catch {
            status = .error
            errorMessage = error.localizedDescription
            
            loggerService.error("Failed {feature} action: \(error)")
            await analyticsService.track(event: .{featureLower}Failed)
        }
    }
    
    /// Reset to idle state
    func reset() {
        status = .idle
        errorMessage = nil
        isLoading = false
    }
    
    /// Cancel operation
    func cancel() {
        reset()
        onCancel?()
    }
}
```

---

## 🧪 Testing Template

```swift
class {Feature}ViewModelTests: XCTestCase {
    var viewModel: {Feature}ViewModel!
    var mockUseCase: Mock{Feature}UseCase!
    
    override func setUp() {
        mockUseCase = Mock{Feature}UseCase()
        viewModel = {Feature}ViewModel(
            {featureLower}UseCase: mockUseCase,
            analyticsService: MockAnalyticsService(),
            loggerService: MockLoggerService()
        )
    }
    
    func testPerformActionSuccess() async {
        mockUseCase.result = .success(())
        
        await viewModel.performAction()
        
        XCTAssertEqual(viewModel.status, .success)
        XCTAssertNil(viewModel.errorMessage)
    }
    
    func testPerformActionFailure() async {
        mockUseCase.result = .failure(TestError.mock)
        
        await viewModel.performAction()
        
        XCTAssertEqual(viewModel.status, .error)
        XCTAssertNotNil(viewModel.errorMessage)
    }
}
```

---

## ✅ Best Practices

- [ ] Inject all dependencies via init
- [ ] Provide convenience init() for production
- [ ] Use @Published for state that triggers View updates
- [ ] Use async methods for asynchronous operations
- [ ] Update status with enum (idle/loading/success/error)
- [ ] Use [weak self] in closures to avoid retain cycles
- [ ] Store Combine subscriptions in cancellables
- [ ] Use callbacks for navigation (onSuccess, onCancel)
