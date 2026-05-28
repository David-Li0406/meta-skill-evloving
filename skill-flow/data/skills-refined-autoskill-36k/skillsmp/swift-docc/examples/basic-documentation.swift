// Basic Documentation Examples (iOS 17+)
// Copy-paste ready Swift code with comprehensive documentation comments

import SwiftUI
import MapKit

// MARK: - Model Documentation

/// A geographic location with a human-readable name.
///
/// Use `Place` to represent locations throughout the application.
/// This model conforms to `Identifiable` for use in SwiftUI lists
/// and `Codable` for JSON serialization.
///
/// ## Overview
///
/// Places are the fundamental building blocks for trip planning.
/// Each place has a name, coordinate, and optional category for filtering.
///
/// ## Example
///
/// ```swift
/// let tokyo = Place(
///     name: "Tokyo Station",
///     coordinate: CLLocationCoordinate2D(latitude: 35.6812, longitude: 139.7671),
///     category: .transportation
/// )
/// ```
///
/// ## Topics
///
/// ### Creating Places
/// - ``init(name:coordinate:category:)``
///
/// ### Properties
/// - ``id``
/// - ``name``
/// - ``coordinate``
/// - ``category``
///
/// - Note: Coordinates should be valid WGS84 values.
/// - SeeAlso: ``Route``, ``SightseeingPlan``
public struct Place: Identifiable, Codable, Hashable {
    /// The unique identifier for this place.
    ///
    /// Generated automatically when creating a new place.
    public let id: UUID
    
    /// The human-readable name of the place.
    ///
    /// This value is displayed in the UI and used for search functionality.
    /// Keep names concise but descriptive.
    public var name: String
    
    /// The geographic coordinate of this place.
    ///
    /// - Important: Ensure coordinates are within valid ranges:
    ///   - Latitude: -90 to 90
    ///   - Longitude: -180 to 180
    public var coordinate: CLLocationCoordinate2D
    
    /// The category of this place for filtering purposes.
    ///
    /// Categories help users filter and organize their saved places.
    public var category: PlaceCategory
    
    /// Creates a new place with the specified properties.
    ///
    /// - Parameters:
    ///   - name: The display name for the place.
    ///   - coordinate: The geographic location of the place.
    ///   - category: The category for filtering. Defaults to `.general`.
    ///
    /// - Precondition: `name` must not be empty.
    public init(
        name: String,
        coordinate: CLLocationCoordinate2D,
        category: PlaceCategory = .general
    ) {
        self.id = UUID()
        self.name = name
        self.coordinate = coordinate
        self.category = category
    }
}

/// Categories for organizing places.
///
/// Use categories to filter and group places in the UI.
public enum PlaceCategory: String, Codable, CaseIterable {
    /// General or uncategorized places.
    case general
    
    /// Tourist attractions and landmarks.
    case attraction
    
    /// Restaurants, cafes, and food establishments.
    case food
    
    /// Train stations, airports, and bus stops.
    case transportation
    
    /// Hotels, hostels, and accommodations.
    case accommodation
}

// MARK: - ViewModel Documentation

/// Manages the state and logic for the content view.
///
/// `ContentViewModel` serves as the single source of truth for
/// the main content view. It handles data loading, user interactions,
/// and navigation state.
///
/// ## Overview
///
/// The view model follows the MVVM pattern and uses the `@Observable`
/// macro for automatic SwiftUI updates.
///
/// ## Example
///
/// ```swift
/// struct ContentView: View {
///     @State private var viewModel = ContentViewModel()
///
///     var body: some View {
///         List(viewModel.places) { place in
///             PlaceRow(place: place)
///         }
///         .task {
///             await viewModel.loadPlaces()
///         }
///     }
/// }
/// ```
///
/// ## Topics
///
/// ### State Properties
/// - ``places``
/// - ``isLoading``
/// - ``error``
///
/// ### Loading Data
/// - ``loadPlaces()``
/// - ``refresh()``
///
/// ### User Actions
/// - ``addPlace(_:)``
/// - ``deletePlace(_:)``
@Observable
public final class ContentViewModel {
    // MARK: - Published Properties
    
    /// The list of places to display.
    ///
    /// This array is automatically updated when places are loaded,
    /// added, or removed.
    public private(set) var places: [Place] = []
    
    /// Indicates whether data is currently being loaded.
    ///
    /// Use this to show loading indicators in the UI.
    public private(set) var isLoading = false
    
    /// The most recent error that occurred, if any.
    ///
    /// Check this property after operations complete to handle errors.
    public private(set) var error: Error?
    
    // MARK: - Dependencies
    
    private let repository: PlaceRepositoryProtocol
    
    // MARK: - Initialization
    
    /// Creates a new view model with the specified repository.
    ///
    /// - Parameter repository: The data source for places.
    ///   Defaults to the shared ``PlaceRepository``.
    public init(repository: PlaceRepositoryProtocol = PlaceRepository.shared) {
        self.repository = repository
    }
    
    // MARK: - Public Methods
    
    /// Loads places from the repository.
    ///
    /// This method fetches all places and updates the ``places`` array.
    /// While loading, ``isLoading`` is set to `true`.
    ///
    /// - Note: This method is safe to call multiple times.
    ///   Subsequent calls will refresh the data.
    ///
    /// - Important: Call this method when the view appears.
    @MainActor
    public func loadPlaces() async {
        isLoading = true
        error = nil
        defer { isLoading = false }
        
        do {
            places = try await repository.fetchAll()
        } catch {
            self.error = error
        }
    }
    
    /// Refreshes the places list.
    ///
    /// Equivalent to ``loadPlaces()`` but intended for pull-to-refresh.
    ///
    /// - Returns: A boolean indicating success.
    @MainActor
    @discardableResult
    public func refresh() async -> Bool {
        await loadPlaces()
        return error == nil
    }
    
    /// Adds a new place to the list.
    ///
    /// - Parameter place: The place to add.
    ///
    /// - Throws: ``PlaceError/duplicateName`` if a place with
    ///   the same name already exists.
    @MainActor
    public func addPlace(_ place: Place) async throws {
        try await repository.save(place)
        places.append(place)
    }
    
    /// Deletes a place from the list.
    ///
    /// - Parameter place: The place to delete.
    ///
    /// - Warning: This action cannot be undone.
    @MainActor
    public func deletePlace(_ place: Place) async throws {
        try await repository.delete(place)
        places.removeAll { $0.id == place.id }
    }
}

// MARK: - Protocol Documentation

/// A protocol for accessing place data.
///
/// Implement this protocol to create custom data sources for places.
/// The default implementation is ``PlaceRepository``.
///
/// ## Conforming to PlaceRepositoryProtocol
///
/// To create a custom repository:
///
/// ```swift
/// class MockPlaceRepository: PlaceRepositoryProtocol {
///     var places: [Place] = []
///
///     func fetchAll() async throws -> [Place] {
///         return places
///     }
///
///     func save(_ place: Place) async throws {
///         places.append(place)
///     }
///
///     func delete(_ place: Place) async throws {
///         places.removeAll { $0.id == place.id }
///     }
/// }
/// ```
public protocol PlaceRepositoryProtocol {
    /// Fetches all places from the data source.
    ///
    /// - Returns: An array of all stored places.
    /// - Throws: An error if the fetch operation fails.
    func fetchAll() async throws -> [Place]
    
    /// Saves a place to the data source.
    ///
    /// - Parameter place: The place to save.
    /// - Throws: ``PlaceError/duplicateName`` if a duplicate exists.
    func save(_ place: Place) async throws
    
    /// Deletes a place from the data source.
    ///
    /// - Parameter place: The place to delete.
    /// - Throws: ``PlaceError/notFound`` if the place doesn't exist.
    func delete(_ place: Place) async throws
}

// MARK: - Error Documentation

/// Errors that can occur when working with places.
///
/// Handle these errors appropriately in your UI to provide
/// meaningful feedback to users.
public enum PlaceError: LocalizedError {
    /// A place with the same name already exists.
    case duplicateName
    
    /// The requested place was not found.
    case notFound
    
    /// A network error occurred.
    case networkError(underlying: Error)
    
    /// Provides a localized description of the error.
    public var errorDescription: String? {
        switch self {
        case .duplicateName:
            return "A place with this name already exists."
        case .notFound:
            return "The place could not be found."
        case .networkError(let error):
            return "Network error: \(error.localizedDescription)"
        }
    }
}

// MARK: - Placeholder Implementations

/// The default implementation of ``PlaceRepositoryProtocol``.
public final class PlaceRepository: PlaceRepositoryProtocol {
    /// The shared singleton instance.
    public static let shared = PlaceRepository()
    
    public func fetchAll() async throws -> [Place] { [] }
    public func save(_ place: Place) async throws { }
    public func delete(_ place: Place) async throws { }
}
