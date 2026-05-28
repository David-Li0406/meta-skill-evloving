# Networking Reference

Networking patterns with Alamofire, Moya, and URLSession.

## Moya (Recommended)

### Target Type Definition

```swift
import Moya

enum UserAPI {
    case getUsers
    case getUser(id: Int)
    case createUser(name: String, email: String)
    case updateUser(id: Int, name: String, email: String)
    case deleteUser(id: Int)
    case uploadAvatar(userId: Int, imageData: Data)
}

extension UserAPI: TargetType {
    var baseURL: URL {
        URL(string: "https://api.example.com/v1")!
    }

    var path: String {
        switch self {
        case .getUsers:
            return "/users"
        case .getUser(let id), .updateUser(let id, _, _), .deleteUser(let id):
            return "/users/\(id)"
        case .createUser:
            return "/users"
        case .uploadAvatar(let userId, _):
            return "/users/\(userId)/avatar"
        }
    }

    var method: Moya.Method {
        switch self {
        case .getUsers, .getUser:
            return .get
        case .createUser:
            return .post
        case .updateUser:
            return .put
        case .deleteUser:
            return .delete
        case .uploadAvatar:
            return .post
        }
    }

    var task: Moya.Task {
        switch self {
        case .getUsers, .getUser, .deleteUser:
            return .requestPlain

        case .createUser(let name, let email):
            return .requestParameters(
                parameters: ["name": name, "email": email],
                encoding: JSONEncoding.default
            )

        case .updateUser(_, let name, let email):
            return .requestParameters(
                parameters: ["name": name, "email": email],
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
        }
    }

    var headers: [String: String]? {
        ["Content-Type": "application/json"]
    }

    var validationType: ValidationType {
        .successCodes
    }
}
```

### Provider Setup

```swift
import Moya

class APIClient {
    static let shared = APIClient()

    private let provider: MoyaProvider<UserAPI>

    init() {
        let plugins: [PluginType] = [
            NetworkLoggerPlugin(configuration: .init(logOptions: .verbose)),
            AuthPlugin()
        ]

        provider = MoyaProvider<UserAPI>(plugins: plugins)
    }

    func request<T: Decodable>(_ target: UserAPI) async throws -> T {
        try await withCheckedThrowingContinuation { continuation in
            provider.request(target) { result in
                switch result {
                case .success(let response):
                    do {
                        let decoded = try JSONDecoder().decode(T.self, from: response.data)
                        continuation.resume(returning: decoded)
                    } catch {
                        continuation.resume(throwing: APIError.decodingFailed(error))
                    }

                case .failure(let error):
                    continuation.resume(throwing: APIError.networkFailed(error))
                }
            }
        }
    }
}
```

### Auth Plugin

```swift
struct AuthPlugin: PluginType {
    func prepare(_ request: URLRequest, target: TargetType) -> URLRequest {
        var request = request

        if let token = TokenManager.shared.accessToken {
            request.addValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
        }

        return request
    }

    func didReceive(_ result: Result<Response, MoyaError>, target: TargetType) {
        if case .success(let response) = result, response.statusCode == 401 {
            NotificationCenter.default.post(name: .tokenExpired, object: nil)
        }
    }
}
```

### Retry Plugin

```swift
final class RetryPlugin: PluginType {
    private let maxRetries: Int

    init(maxRetries: Int = 3) {
        self.maxRetries = maxRetries
    }

    func process(
        _ result: Result<Response, MoyaError>,
        target: TargetType
    ) -> Result<Response, MoyaError> {
        // Implement retry logic
        result
    }
}
```

## Alamofire

### Session Configuration

```swift
import Alamofire

class NetworkManager {
    static let shared = NetworkManager()

    let session: Session

    private init() {
        let configuration = URLSessionConfiguration.af.default
        configuration.timeoutIntervalForRequest = 30
        configuration.timeoutIntervalForResource = 60

        let interceptor = AuthInterceptor()

        session = Session(
            configuration: configuration,
            interceptor: interceptor
        )
    }
}
```

### Request Interceptor

```swift
class AuthInterceptor: RequestInterceptor {
    private let tokenManager: TokenManager

    init(tokenManager: TokenManager = .shared) {
        self.tokenManager = tokenManager
    }

    func adapt(
        _ urlRequest: URLRequest,
        for session: Session,
        completion: @escaping (Result<URLRequest, Error>) -> Void
    ) {
        var request = urlRequest

        if let token = tokenManager.accessToken {
            request.headers.add(.authorization(bearerToken: token))
        }

        completion(.success(request))
    }

    func retry(
        _ request: Request,
        for session: Session,
        dueTo error: Error,
        completion: @escaping (RetryResult) -> Void
    ) {
        guard let response = request.task?.response as? HTTPURLResponse,
              response.statusCode == 401 else {
            completion(.doNotRetry)
            return
        }

        Task {
            do {
                try await tokenManager.refreshToken()
                completion(.retry)
            } catch {
                completion(.doNotRetryWithError(error))
            }
        }
    }
}
```

### Generic Request

```swift
extension NetworkManager {
    func request<T: Decodable>(
        _ endpoint: String,
        method: HTTPMethod = .get,
        parameters: Parameters? = nil,
        encoding: ParameterEncoding = JSONEncoding.default
    ) async throws -> T {
        try await session.request(
            endpoint,
            method: method,
            parameters: parameters,
            encoding: encoding
        )
        .validate()
        .serializingDecodable(T.self)
        .value
    }
}
```

## URLSession (Standard)

### API Client

```swift
actor URLSessionAPIClient {
    private let session: URLSession
    private let baseURL: URL
    private let decoder: JSONDecoder

    init(baseURL: URL, session: URLSession = .shared) {
        self.baseURL = baseURL
        self.session = session
        self.decoder = JSONDecoder()
        self.decoder.dateDecodingStrategy = .iso8601
    }

    func request<T: Decodable>(_ endpoint: Endpoint) async throws -> T {
        let request = try buildRequest(for: endpoint)
        let (data, response) = try await session.data(for: request)

        guard let httpResponse = response as? HTTPURLResponse else {
            throw APIError.invalidResponse
        }

        guard (200...299).contains(httpResponse.statusCode) else {
            throw APIError.httpError(statusCode: httpResponse.statusCode, data: data)
        }

        return try decoder.decode(T.self, from: data)
    }

    private func buildRequest(for endpoint: Endpoint) throws -> URLRequest {
        guard let url = URL(string: endpoint.path, relativeTo: baseURL) else {
            throw APIError.invalidURL
        }

        var request = URLRequest(url: url)
        request.httpMethod = endpoint.method.rawValue
        request.allHTTPHeaderFields = endpoint.headers

        if let body = endpoint.body {
            request.httpBody = try JSONEncoder().encode(body)
            request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        }

        return request
    }
}
```

### Endpoint Protocol

```swift
protocol Endpoint {
    var path: String { get }
    var method: HTTPMethod { get }
    var headers: [String: String]? { get }
    var body: Encodable? { get }
}

enum HTTPMethod: String {
    case get = "GET"
    case post = "POST"
    case put = "PUT"
    case delete = "DELETE"
    case patch = "PATCH"
}
```

## Error Handling

### API Error Types

```swift
enum APIError: LocalizedError {
    case invalidURL
    case invalidResponse
    case httpError(statusCode: Int, data: Data?)
    case decodingFailed(Error)
    case networkFailed(Error)
    case unauthorized
    case serverError(message: String)

    var errorDescription: String? {
        switch self {
        case .invalidURL:
            return "Invalid URL"
        case .invalidResponse:
            return "Invalid response from server"
        case .httpError(let code, _):
            return "HTTP error: \(code)"
        case .decodingFailed:
            return "Failed to decode response"
        case .networkFailed:
            return "Network request failed"
        case .unauthorized:
            return "Authentication required"
        case .serverError(let message):
            return message
        }
    }
}
```

### Error Response Parsing

```swift
struct ErrorResponse: Decodable {
    let message: String
    let code: String?
}

extension APIError {
    static func from(statusCode: Int, data: Data?) -> APIError {
        if statusCode == 401 {
            return .unauthorized
        }

        if let data, let errorResponse = try? JSONDecoder().decode(ErrorResponse.self, from: data) {
            return .serverError(message: errorResponse.message)
        }

        return .httpError(statusCode: statusCode, data: data)
    }
}
```

## Network Monitoring

```swift
import Network

@Observable
class NetworkMonitor {
    private(set) var isConnected = true
    private(set) var connectionType: ConnectionType = .unknown

    private let monitor = NWPathMonitor()
    private let queue = DispatchQueue(label: "NetworkMonitor")

    enum ConnectionType {
        case wifi
        case cellular
        case wired
        case unknown
    }

    init() {
        startMonitoring()
    }

    private func startMonitoring() {
        monitor.pathUpdateHandler = { [weak self] path in
            Task { @MainActor in
                self?.isConnected = path.status == .satisfied
                self?.connectionType = self?.getConnectionType(path) ?? .unknown
            }
        }
        monitor.start(queue: queue)
    }

    private func getConnectionType(_ path: NWPath) -> ConnectionType {
        if path.usesInterfaceType(.wifi) { return .wifi }
        if path.usesInterfaceType(.cellular) { return .cellular }
        if path.usesInterfaceType(.wiredEthernet) { return .wired }
        return .unknown
    }
}
```

## Best Practices

1. **Use Moya for structured APIs** - Type-safe, testable
2. **Implement retry logic** - Handle transient failures
3. **Token refresh** - Automatic refresh with interceptors
4. **Error handling** - Map to user-friendly messages
5. **Network monitoring** - Show offline state to users
6. **Request timeouts** - Set appropriate timeout values
7. **Caching** - Use URLCache or custom caching layer
