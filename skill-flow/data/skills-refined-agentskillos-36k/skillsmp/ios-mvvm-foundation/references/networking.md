# Networking

> URLSession + async/await networking layer.

---

## 🎯 Architecture

| Component | Role |
|-----------|------|
| `APIClient` | HTTP requests |
| `Repository` | Data operations |
| `UseCase` | Business logic |

---

## 📦 APIClient

```swift
// Core/Services/APIClient.swift

class APIClient {
    private let session: URLSession
    private let baseURL: URL
    private let tokenStorage: TokenStorageProtocol
    private let decoder: JSONDecoder
    
    init(
        baseURL: URL = URL(string: "https://api.example.com")!,
        tokenStorage: TokenStorageProtocol = Resolver.resolve()
    ) {
        self.baseURL = baseURL
        self.tokenStorage = tokenStorage
        self.session = URLSession.shared
        self.decoder = JSONDecoder()
        self.decoder.keyDecodingStrategy = .convertFromSnakeCase
    }
    
    func request<T: Decodable>(
        _ endpoint: String,
        method: HTTPMethod = .get,
        body: Encodable? = nil,
        headers: [String: String] = [:]
    ) async throws -> T {
        var request = URLRequest(url: baseURL.appendingPathComponent(endpoint))
        request.httpMethod = method.rawValue
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        // Add auth token if available
        if let token = try await tokenStorage.getToken() {
            request.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
        }
        
        // Add custom headers
        headers.forEach { request.setValue($1, forHTTPHeaderField: $0) }
        
        // Encode body
        if let body = body {
            request.httpBody = try JSONEncoder().encode(body)
        }
        
        return try await performWithRetry(request: request)
    }
}

// HTTP Methods
enum HTTPMethod: String {
    case get = "GET"
    case post = "POST"
    case put = "PUT"
    case patch = "PATCH"
    case delete = "DELETE"
}
```

---

## 🔄 Retry Logic

```swift
private func performWithRetry<T: Decodable>(
    request: URLRequest,
    attempt: Int = 1
) async throws -> T {
    do {
        let (data, response) = try await session.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse else {
            throw NetworkError.invalidResponse
        }
        
        // Success
        guard (200...299).contains(httpResponse.statusCode) else {
            // Retry on 5xx server errors
            if httpResponse.statusCode >= 500 && attempt < 3 {
                let delay = UInt64(pow(2.0, Double(attempt)) * 1_000_000_000)
                try await Task.sleep(nanoseconds: delay)
                return try await performWithRetry(request: request, attempt: attempt + 1)
            }
            throw NetworkError.httpError(httpResponse.statusCode)
        }
        
        return try decoder.decode(T.self, from: data)
        
    } catch let error as NetworkError {
        throw error
    } catch let decodingError as DecodingError {
        throw NetworkError.decodingError(decodingError)
    } catch {
        // Retry on network errors
        if attempt < 3 && isRetryableError(error) {
            let delay = UInt64(pow(2.0, Double(attempt)) * 1_000_000_000)
            try await Task.sleep(nanoseconds: delay)
            return try await performWithRetry(request: request, attempt: attempt + 1)
        }
        throw NetworkError.underlying(error)
    }
}

private func isRetryableError(_ error: Error) -> Bool {
    let nsError = error as NSError
    return nsError.domain == NSURLErrorDomain && [
        NSURLErrorTimedOut,
        NSURLErrorCannotConnectToHost,
        NSURLErrorNetworkConnectionLost
    ].contains(nsError.code)
}
```

**Retry policy**: 3 attempts, exponential backoff (1s, 2s, 4s)

---

## ❌ Error Handling

```swift
enum NetworkError: Error, LocalizedError {
    case noInternet
    case timeout
    case invalidResponse
    case httpError(Int)
    case decodingError(Error)
    case unauthorized
    case serverError(String)
    case underlying(Error)
    
    var errorDescription: String? {
        switch self {
        case .noInternet:
            return "Không có kết nối mạng"
        case .timeout:
            return "Kết nối quá thời gian"
        case .invalidResponse:
            return "Phản hồi không hợp lệ"
        case .httpError(let code):
            return "Lỗi HTTP: \(code)"
        case .decodingError:
            return "Không thể xử lý dữ liệu"
        case .unauthorized:
            return "Phiên đăng nhập hết hạn"
        case .serverError(let message):
            return message
        case .underlying(let error):
            return error.localizedDescription
        }
    }
}
```

---

## 📡 Repository Usage

```swift
class UserRepository: UserRepositoryProtocol {
    private let apiClient: APIClient
    
    init(apiClient: APIClient = Resolver.resolve()) {
        self.apiClient = apiClient
    }
    
    func getUser(id: String) async throws -> User {
        try await apiClient.request("users/\(id)")
    }
    
    func updateUser(_ user: User) async throws -> User {
        try await apiClient.request(
            "users/\(user.id)",
            method: .put,
            body: user
        )
    }
    
    func login(email: String, password: String) async throws -> AuthResponse {
        try await apiClient.request(
            "auth/login",
            method: .post,
            body: LoginRequest(email: email, password: password)
        )
    }
}
```

---

## 🔗 Related

- [di.md](di.md) - Dependency injection
- [testing.md](testing.md) - Mock APIClient

