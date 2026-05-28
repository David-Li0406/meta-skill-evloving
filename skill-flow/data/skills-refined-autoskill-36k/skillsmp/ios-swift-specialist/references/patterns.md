# iOS/Swift Specialist

## Patterns


---
  #### **Name**
Modern SwiftUI Architecture
  #### **Description**
Clean architecture with SwiftUI and Swift concurrency
  #### **When**
Building new iOS apps
  #### **Example**
    // MVVM with Observation (iOS 17+)
    import SwiftUI
    import Observation
    
    @Observable
    class ProfileViewModel {
        var user: User?
        var isLoading = false
        var error: Error?
    
        private let userService: UserServiceProtocol
    
        init(userService: UserServiceProtocol = UserService()) {
            self.userService = userService
        }
    
        func loadUser() async {
            isLoading = true
            defer { isLoading = false }
    
            do {
                user = try await userService.getCurrentUser()
            } catch {
                self.error = error
            }
        }
    }
    
    struct ProfileView: View {
        @State private var viewModel = ProfileViewModel()
    
        var body: some View {
            Group {
                if viewModel.isLoading {
                    ProgressView()
                } else if let user = viewModel.user {
                    UserProfileContent(user: user)
                } else if let error = viewModel.error {
                    ErrorView(error: error, retry: {
                        Task { await viewModel.loadUser() }
                    })
                }
            }
            .task {
                await viewModel.loadUser()
            }
        }
    }
    

---
  #### **Name**
Protocol-Oriented Design
  #### **Description**
Composition over inheritance with protocols
  #### **When**
Designing reusable components
  #### **Example**
    // Define behavior with protocols
    protocol Identifiable {
        var id: UUID { get }
    }
    
    protocol Timestamped {
        var createdAt: Date { get }
        var updatedAt: Date { get }
    }
    
    protocol Syncable {
        var isSynced: Bool { get }
        func sync() async throws
    }
    
    // Compose capabilities
    struct Task: Identifiable, Timestamped, Syncable {
        let id = UUID()
        var title: String
        let createdAt: Date
        var updatedAt: Date
        var isSynced = false
    
        func sync() async throws {
            // Sync implementation
        }
    }
    
    // Protocol extensions provide default implementations
    extension Syncable where Self: Identifiable {
        func syncIfNeeded() async throws {
            guard !isSynced else { return }
            try await sync()
        }
    }
    
    // Type erasure for protocol collections
    struct AnyIdentifiable: Identifiable {
        let id: UUID
        private let wrapped: any Identifiable
    
        init(_ wrapped: any Identifiable) {
            self.id = wrapped.id
            self.wrapped = wrapped
        }
    }
    

---
  #### **Name**
Combine with Async/Await Bridge
  #### **Description**
Reactive programming with modern concurrency
  #### **When**
Complex data flows, real-time updates
  #### **Example**
    import Combine
    
    class SearchViewModel: ObservableObject {
        @Published var searchText = ""
        @Published var results: [SearchResult] = []
        @Published var isSearching = false
    
        private var cancellables = Set<AnyCancellable>()
        private let searchService: SearchService
    
        init(searchService: SearchService = .shared) {
            self.searchService = searchService
            setupBindings()
        }
    
        private func setupBindings() {
            $searchText
                .debounce(for: .milliseconds(300), scheduler: RunLoop.main)
                .removeDuplicates()
                .filter { $0.count >= 2 }
                .sink { [weak self] query in
                    Task { await self?.search(query) }
                }
                .store(in: &cancellables)
        }
    
        @MainActor
        private func search(_ query: String) async {
            isSearching = true
            defer { isSearching = false }
    
            do {
                results = try await searchService.search(query)
            } catch {
                results = []
            }
        }
    }
    
    // AsyncSequence bridge for Combine publishers
    extension Publisher where Failure == Never {
        var values: AsyncPublisher<Self> {
            AsyncPublisher(self)
        }
    }
    
    struct AsyncPublisher<P: Publisher>: AsyncSequence where P.Failure == Never {
        typealias Element = P.Output
    
        let publisher: P
    
        struct AsyncIterator: AsyncIteratorProtocol {
            // Implementation
        }
    
        func makeAsyncIterator() -> AsyncIterator {
            AsyncIterator()
        }
    }
    

---
  #### **Name**
UIKit Integration
  #### **Description**
Bridging UIKit components into SwiftUI
  #### **When**
SwiftUI doesn't support needed functionality
  #### **Example**
    import SwiftUI
    import UIKit
    
    // Wrap UIKit component for SwiftUI
    struct TextView: UIViewRepresentable {
        @Binding var text: String
        var isEditable = true
    
        func makeUIView(context: Context) -> UITextView {
            let textView = UITextView()
            textView.delegate = context.coordinator
            textView.isEditable = isEditable
            textView.font = .preferredFont(forTextStyle: .body)
            return textView
        }
    
        func updateUIView(_ uiView: UITextView, context: Context) {
            if uiView.text != text {
                uiView.text = text
            }
        }
    
        func makeCoordinator() -> Coordinator {
            Coordinator(self)
        }
    
        class Coordinator: NSObject, UITextViewDelegate {
            var parent: TextView
    
            init(_ parent: TextView) {
                self.parent = parent
            }
    
            func textViewDidChange(_ textView: UITextView) {
                parent.text = textView.text
            }
        }
    }
    
    // Usage in SwiftUI
    struct EditorView: View {
        @State private var content = ""
    
        var body: some View {
            TextView(text: $content)
                .frame(minHeight: 200)
        }
    }
    

## Anti-Patterns


---
  #### **Name**
Force Unwrapping Production Code
  #### **Description**
Using ! on optionals in production code
  #### **Why**
Crashes at runtime when nil, defeats Swift's safety
  #### **Instead**
Use if-let, guard-let, nil coalescing, or optional chaining

---
  #### **Name**
Massive View Controllers
  #### **Description**
Putting all logic in view controllers/views
  #### **Why**
Untestable, hard to maintain, violates SRP
  #### **Instead**
Extract to view models, services, use composition

---
  #### **Name**
Ignoring Main Thread
  #### **Description**
UI updates from background threads
  #### **Why**
Crashes or undefined behavior, hard to debug
  #### **Instead**
Use @MainActor, DispatchQueue.main, or MainActor.run

---
  #### **Name**
Retain Cycles in Closures
  #### **Description**
Strong self references in escaping closures
  #### **Why**
Memory leaks, objects never deallocated
  #### **Instead**
Use [weak self] or [unowned self] with guard

---
  #### **Name**
Stringly Typed APIs
  #### **Description**
Using strings for identifiers, keys, segues
  #### **Why**
No compile-time safety, typos cause runtime crashes
  #### **Instead**
Use enums, constants, or generated type-safe APIs