# MVVM Screen Template

> Complete screen template với ViewModel và View.

---

## 📁 Files Generated

| File | Path |
|------|------|
| `{Feature}ViewModel.swift` | `Presentation/{Feature}/{Feature}ViewModel.swift` |
| `{Feature}View.swift` | `Presentation/{Feature}/{Feature}View.swift` |

---

## 🏗️ ViewModel Template

```swift
import Foundation
import Combine

// MARK: - {Feature}ViewModel

class {Feature}ViewModel: ObservableObject {
    // MARK: - Published Properties
    
    @Published var status: Status = .idle
    @Published var errorMessage: String?
    
    enum Status: Equatable {
        case idle
        case loading
        case success
        case error
    }
    
    // MARK: - Dependencies
    
    private let {featureLower}UseCase: {Feature}UseCaseProtocol
    private var cancellables = Set<AnyCancellable>()
    
    // MARK: - Navigation
    
    @Published var navigationIntent: NavigationIntent?
    
    enum NavigationIntent: Equatable {
        case success
        case cancel
    }
    
    // MARK: - Initialization
    
    init({featureLower}UseCase: {Feature}UseCaseProtocol) {
        self.{featureLower}UseCase = {featureLower}UseCase
    }
    
    /// Convenience init for production (uses Resolver)
    convenience init() {
        self.init({featureLower}UseCase: Resolver.resolve())
    }
    
    // MARK: - Actions
    
    func performAction() async {
        status = .loading
        errorMessage = nil
        
        do {
            try await {featureLower}UseCase.execute()
            status = .success
            navigationIntent = .success
        } catch {
            status = .error
            errorMessage = error.localizedDescription
        }
    }
}
```

---

## 🎨 View Template

```swift
import SwiftUI

// MARK: - {Feature}View

struct {Feature}View: View {
    // MARK: - Properties
    
    @StateObject private var viewModel: {Feature}ViewModel
    @Environment(\.theme) var theme
    
    // Animation state (NOT in ViewModel)
    @State private var buttonScale: CGFloat = 1.0
    
    // MARK: - Initialization
    
    init(viewModel: {Feature}ViewModel = {Feature}ViewModel()) {
        _viewModel = StateObject(wrappedValue: viewModel)
    }
    
    // MARK: - Body
    
    var body: some View {
        VStack(spacing: 24) {
            switch viewModel.status {
            case .idle:
                idleView
            case .loading:
                ProgressView()
            case .success:
                successView
            case .error:
                errorView
            }
        }
        .padding()
        .background(theme.colors.background)
        .onChange(of: viewModel.navigationIntent) { intent in
            handleNavigation(intent)
        }
    }
    
    // MARK: - Subviews
    
    private var idleView: some View {
        VStack(spacing: 16) {
            Text("{Feature}")
                .font(theme.typography.h1)
                .foregroundColor(theme.colors.textPrimary)
            
            Button("Start") {
                Task { await viewModel.performAction() }
            }
            .buttonStyle(ThemedButtonStyle(theme: theme))
            .scaleEffect(buttonScale)
            .onChange(of: viewModel.status) { status in
                withAnimation(.easeInOut(duration: 0.15)) {
                    buttonScale = status == .loading ? 0.95 : 1.0
                }
            }
        }
    }
    
    private var successView: some View {
        Text("Success!")
            .font(theme.typography.body)
            .foregroundColor(theme.colors.primary)
    }
    
    private var errorView: some View {
        VStack(spacing: 12) {
            if let errorMessage = viewModel.errorMessage {
                Text(errorMessage)
                    .font(theme.typography.body)
                    .foregroundColor(theme.colors.error)
            }
            
            Button("Retry") {
                Task { await viewModel.performAction() }
            }
            .buttonStyle(ThemedButtonStyle(theme: theme))
        }
    }
    
    // MARK: - Navigation
    
    private func handleNavigation(_ intent: {Feature}ViewModel.NavigationIntent?) {
        guard let intent = intent else { return }
        
        switch intent {
        case .success:
            // Handle navigation
            break
        case .cancel:
            break
        }
        
        viewModel.navigationIntent = nil  // Consume intent
    }
}

// MARK: - Preview

struct {Feature}View_Previews: PreviewProvider {
    static var previews: some View {
        {Feature}View()
            .environment(\.theme, .defaultLight)
    }
}
```

---

## 🔄 ViewModel + ViewState (Optional)

Cho screens có complex formatting logic:

```swift
class {Feature}ViewModel: ObservableObject {
    // MARK: - ViewState (public, single source for View)
    
    @Published private(set) var viewState: ViewState = .idle
    
    struct ViewState: Equatable {
        let title: String
        let buttonTitle: String
        let isButtonEnabled: Bool
        let showsLoading: Bool
        let errorMessage: String?
        
        static let idle = ViewState(
            title: "{Feature}",
            buttonTitle: "Start",
            isButtonEnabled: true,
            showsLoading: false,
            errorMessage: nil
        )
    }
    
    // MARK: - Business State (private)
    
    @Published private var status: Status = .idle
    
    // MARK: - Setup
    
    private func setupBindings() {
        $status
            .map { status in
                ViewState(
                    title: "{Feature}",
                    buttonTitle: status == .loading ? "Loading..." : "Start",
                    isButtonEnabled: status != .loading,
                    showsLoading: status == .loading,
                    errorMessage: status.errorMessage
                )
            }
            .assign(to: &$viewState)
    }
}
```

---

## ✅ Checklist

- [ ] ViewModel conforms to ObservableObject
- [ ] Uses @Published for business state
- [ ] Injects UseCases via init
- [ ] Provides convenience init() with Resolver
- [ ] View uses @StateObject for ViewModel
- [ ] Animation state in @State (NOT ViewModel)
- [ ] Async actions called via Task
- [ ] Theme accessed via @Environment
- [ ] Navigation intent consumed after handling
- [ ] No animation values in ViewModel @Published

---

## 🔄 Navigation Options

| Pattern | When to Use |
|---------|-------------|
| **Intent-based** (default) | Most screens, simple flows |
| **Navigator injection** | Need to mock navigation in tests |
| **Callbacks** | Complex flows with Coordinator |
