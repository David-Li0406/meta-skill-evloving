// Moya Networking Example
// Complete implementation with TargetType, Provider, and error handling

import Foundation
import Moya

// MARK: - API Target Definition

enum UserAPI {
    case getUsers
    case getUser(id: Int)
    case createUser(name: String, email: String)
    case updateUser(id: Int, name: String, email: String)
    case deleteUser(id: Int)
    case uploadAvatar(userId: Int, imageData: Data)
    case searchUsers(query: String, page: Int, limit: Int)
}

extension UserAPI: TargetType {
    var baseURL: URL {
        URL(string: "https://api.example.com/v1")!
    }

    var path: String {
        switch self {
        case .getUsers, .createUser:
            return "/users"
        case .getUser(let id), .updateUser(let id, _, _), .deleteUser(let id):
            return "/users/\(id)"
        case .uploadAvatar(let userId, _):
            return "/users/\(userId)/avatar"
        case .searchUsers:
            return "/users/search"
        }
    }

    var method: Moya.Method {
        switch self {
        case .getUsers, .getUser, .searchUsers:
            return .get
        case .createUser, .uploadAvatar:
            return .post
        case .updateUser:
            return .put
        case .deleteUser:
            return .delete
        }
    }

    var task: Moya.Task {
        switch self {
        case .getUsers, .getUser, .deleteUser:
            return .requestPlain

        case .createUser(let name, let email):
            let params: [String: Any] = [
                "name": name,
                "email": email
            ]
            return .requestParameters(
                parameters: params,
                encoding: JSONEncoding.default
            )

        case .updateUser(_, let name, let email):
            let params: [String: Any] = [
                "name": name,
                "email": email
            ]
            return .requestParameters(
                parameters: params,
                encoding: JSONEncoding.default
            )

        case .uploadAvatar(_, let imageData):
            let formData = MultipartFormData(
                provider: .data(imageData),
                name: "avatar",
                fileName: "avatar.jpg",
                mimeType: "image/jpeg"
            )
            return .uploadMultipart([formData])

        case .searchUsers(let query, let page, let limit):
            let params: [String: Any] = [
                "q": query,
                "page": page,
                "limit": limit
            ]
            return .requestParameters(
                parameters: params,
                encoding: URLEncoding.queryString
            )
        }
    }

    var headers: [String: String]? {
        var headers = [
            "Content-Type": "application/json",
            "Accept": "application/json"
        ]

        // Add multipart header for upload
        if case .uploadAvatar = self {
            headers["Content-Type"] = "multipart/form-data"
        }

        return headers
    }

    var validationType: ValidationType {
        .successCodes
    }

    // For stub testing
    var sampleData: Data {
        switch self {
        case .getUsers:
            return """
            [
                {"id": 1, "name": "Alice", "email": "alice@example.com"},
                {"id": 2, "name": "Bob", "email": "bob@example.com"}
            ]
            """.data(using: .utf8)!

        case .getUser(let id):
            return """
            {"id": \(id), "name": "User \(id)", "email": "user\(id)@example.com"}
            """.data(using: .utf8)!

        case .createUser(let name, let email):
            return """
            {"id": 100, "name": "\(name)", "email": "\(email)"}
            """.data(using: .utf8)!

        case .updateUser(let id, let name, let email):
            return """
            {"id": \(id), "name": "\(name)", "email": "\(email)"}
            """.data(using: .utf8)!

        case .deleteUser:
            return Data()

        case .uploadAvatar(let userId, _):
            return """
            {"id": \(userId), "avatarUrl": "https://example.com/avatar.jpg"}
            """.data(using: .utf8)!

        case .searchUsers:
            return """
            {
                "data": [{"id": 1, "name": "Alice", "email": "alice@example.com"}],
                "total": 1,
                "page": 1
            }
            """.data(using: .utf8)!
        }
    }
}

// MARK: - API Error

enum APIError: LocalizedError {
    case networkError(Error)
    case invalidResponse
    case decodingError(Error)
    case serverError(statusCode: Int, message: String?)
    case unauthorized
    case notFound
    case rateLimited

    var errorDescription: String? {
        switch self {
        case .networkError(let error):
            return "Network error: \(error.localizedDescription)"
        case .invalidResponse:
            return "Invalid response from server"
        case .decodingError(let error):
            return "Failed to decode response: \(error.localizedDescription)"
        case .serverError(let code, let message):
            return message ?? "Server error (\(code))"
        case .unauthorized:
            return "Authentication required"
        case .notFound:
            return "Resource not found"
        case .rateLimited:
            return "Too many requests. Please try again later."
        }
    }
}

// MARK: - Server Error Response

struct ServerErrorResponse: Decodable {
    let message: String
    let code: String?
}

// MARK: - Auth Plugin

struct AuthPlugin: PluginType {
    private let tokenProvider: () -> String?

    init(tokenProvider: @escaping () -> String?) {
        self.tokenProvider = tokenProvider
    }

    func prepare(_ request: URLRequest, target: any TargetType) -> URLRequest {
        var request = request

        if let token = tokenProvider() {
            request.addValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
        }

        return request
    }

    func didReceive(_ result: Result<Response, MoyaError>, target: any TargetType) {
        if case .success(let response) = result, response.statusCode == 401 {
            NotificationCenter.default.post(name: .tokenExpired, object: nil)
        }
    }
}

extension Notification.Name {
    static let tokenExpired = Notification.Name("tokenExpired")
}

// MARK: - Logging Plugin Configuration

extension NetworkLoggerPlugin.Configuration {
    static var verbose: Self {
        .init(
            formatter: .init(),
            output: { _, items in
                for item in items {
                    print(item)
                }
            },
            logOptions: [.requestMethod, .requestBody, .successResponseBody, .errorResponseBody]
        )
    }
}

// MARK: - API Client

actor APIClient {
    private let provider: MoyaProvider<UserAPI>
    private let decoder: JSONDecoder

    init(tokenProvider: @escaping () -> String? = { nil }) {
        let plugins: [PluginType] = [
            NetworkLoggerPlugin(configuration: .verbose),
            AuthPlugin(tokenProvider: tokenProvider)
        ]

        self.provider = MoyaProvider<UserAPI>(plugins: plugins)
        self.decoder = JSONDecoder()
        self.decoder.dateDecodingStrategy = .iso8601
    }

    func request<T: Decodable>(_ target: UserAPI) async throws -> T {
        try await withCheckedThrowingContinuation { continuation in
            provider.request(target) { result in
                switch result {
                case .success(let response):
                    do {
                        // Check for HTTP errors
                        if let error = self.mapHTTPError(response) {
                            continuation.resume(throwing: error)
                            return
                        }

                        // Decode response
                        let decoded = try self.decoder.decode(T.self, from: response.data)
                        continuation.resume(returning: decoded)
                    } catch let decodingError as DecodingError {
                        continuation.resume(throwing: APIError.decodingError(decodingError))
                    } catch {
                        continuation.resume(throwing: error)
                    }

                case .failure(let error):
                    continuation.resume(throwing: self.mapMoyaError(error))
                }
            }
        }
    }

    func requestVoid(_ target: UserAPI) async throws {
        try await withCheckedThrowingContinuation { (continuation: CheckedContinuation<Void, Error>) in
            provider.request(target) { result in
                switch result {
                case .success(let response):
                    if let error = self.mapHTTPError(response) {
                        continuation.resume(throwing: error)
                    } else {
                        continuation.resume(returning: ())
                    }

                case .failure(let error):
                    continuation.resume(throwing: self.mapMoyaError(error))
                }
            }
        }
    }

    private func mapHTTPError(_ response: Response) -> APIError? {
        switch response.statusCode {
        case 200...299:
            return nil
        case 401:
            return .unauthorized
        case 404:
            return .notFound
        case 429:
            return .rateLimited
        default:
            let message = try? decoder.decode(ServerErrorResponse.self, from: response.data).message
            return .serverError(statusCode: response.statusCode, message: message)
        }
    }

    private func mapMoyaError(_ error: MoyaError) -> APIError {
        switch error {
        case .underlying(let nsError as NSError, _):
            return .networkError(nsError)
        default:
            return .networkError(error)
        }
    }
}

// MARK: - Repository using API Client

actor UserRepository {
    private let apiClient: APIClient

    init(apiClient: APIClient) {
        self.apiClient = apiClient
    }

    func fetchUsers() async throws -> [User] {
        try await apiClient.request(.getUsers)
    }

    func fetchUser(id: Int) async throws -> User {
        try await apiClient.request(.getUser(id: id))
    }

    func createUser(name: String, email: String) async throws -> User {
        try await apiClient.request(.createUser(name: name, email: email))
    }

    func updateUser(id: Int, name: String, email: String) async throws -> User {
        try await apiClient.request(.updateUser(id: id, name: name, email: email))
    }

    func deleteUser(id: Int) async throws {
        try await apiClient.requestVoid(.deleteUser(id: id))
    }

    func uploadAvatar(userId: Int, imageData: Data) async throws -> User {
        try await apiClient.request(.uploadAvatar(userId: userId, imageData: imageData))
    }

    func searchUsers(query: String, page: Int = 1, limit: Int = 20) async throws -> SearchResult<User> {
        try await apiClient.request(.searchUsers(query: query, page: page, limit: limit))
    }
}

// MARK: - Response Models

struct User: Codable, Identifiable {
    let id: Int
    var name: String
    var email: String
    var avatarUrl: URL?
}

struct SearchResult<T: Codable>: Codable {
    let data: [T]
    let total: Int
    let page: Int
}

// MARK: - Usage Example

/*
 Usage in ViewModel:

 @Observable
 @MainActor
 class UserListViewModel {
     private(set) var users: [User] = []
     private(set) var isLoading = false
     private(set) var error: Error?

     private let repository: UserRepository

     init() {
         let apiClient = APIClient {
             // Provide token from your token manager
             TokenManager.shared.accessToken
         }
         self.repository = UserRepository(apiClient: apiClient)
     }

     func loadUsers() async {
         isLoading = true
         defer { isLoading = false }

         do {
             users = try await repository.fetchUsers()
         } catch {
             self.error = error
         }
     }
 }
 */
