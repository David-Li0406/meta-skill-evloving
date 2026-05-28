# Security and Sensitive Information

## Input Validation

### Validate All External Input

Never trust data from external sources. Always validate and sanitize:

```cpp
// ❌ Vulnerable to SQL injection
std::string query = "SELECT * FROM users WHERE email = '" + userInput + "'";
db.execute(query);

// ✅ Use parameterized queries
auto stmt = db.prepare("SELECT * FROM users WHERE email = ?");
stmt.bind(1, userInput);
auto result = stmt.execute();
```

### Common Validation Patterns

**Email Validation**:
```cpp
#include <regex>

bool isValidEmail(const std::string& email) {
    static const std::regex pattern(
        R"(^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$)"
    );
    return std::regex_match(email, pattern);
}
```

**Length Validation**:
```cpp
std::string sanitizeInput(const std::string& input, size_t maxLength = 1000) {
    if (input.length() > maxLength) {
        throw std::invalid_argument("Input exceeds maximum length");
    }
    return input;
}
```

**Type Validation** (Python):
```python
from typing import TypeVar, Type

T = TypeVar('T')

def validate_type(value: any, expected_type: Type[T]) -> T:
    if not isinstance(value, expected_type):
        raise TypeError(f"Expected {expected_type}, got {type(value)}")
    return value
```

### Prevent Injection Attacks

**SQL Injection Prevention**:
```cpp
// Always use parameterized queries
class UserRepository {
public:
    User findByEmail(const std::string& email) {
        auto stmt = db_.prepare("SELECT * FROM users WHERE email = ?");
        stmt.bind(1, email);  // Parameter binding prevents injection
        return stmt.executeQuery<User>();
    }

    void updateUser(const User& user) {
        auto stmt = db_.prepare(
            "UPDATE users SET name = ?, age = ? WHERE id = ?"
        );
        stmt.bind(1, user.name);
        stmt.bind(2, user.age);
        stmt.bind(3, user.id);
        stmt.execute();
    }
};
```

**Command Injection Prevention**:
```cpp
// ❌ Vulnerable to command injection
std::string command = "ls " + userInput;
system(command.c_str());

// ✅ Use safe APIs instead of shell execution
#include <filesystem>
namespace fs = std::filesystem;

void listDirectory(const std::string& path) {
    // Validate path first
    if (!fs::exists(path) || !fs::is_directory(path)) {
        throw std::invalid_argument("Invalid directory");
    }

    for (const auto& entry : fs::directory_iterator(path)) {
        std::cout << entry.path() << '\n';
    }
}
```

**XSS Prevention** (Web contexts):
```typescript
// ❌ Vulnerable to XSS
element.innerHTML = userInput;

// ✅ Escape HTML entities
function escapeHtml(unsafe: string): string {
  return unsafe
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

element.textContent = userInput;  // Automatically safe
```

### Path Traversal Prevention

```cpp
#include <filesystem>

std::string sanitizePath(const std::string& userPath,
                         const std::string& baseDir) {
    namespace fs = std::filesystem;

    // Resolve to absolute path
    fs::path absolutePath = fs::absolute(baseDir / userPath);

    // Ensure path is within base directory
    auto [rootEnd, nothing] = std::mismatch(
        fs::absolute(baseDir).begin(),
        fs::absolute(baseDir).end(),
        absolutePath.begin()
    );

    if (rootEnd != fs::absolute(baseDir).end()) {
        throw std::invalid_argument("Path traversal attempt detected");
    }

    return absolutePath.string();
}

// Usage
try {
    std::string safePath = sanitizePath(userInput, "/var/app/uploads");
    // Now safe to use safePath
} catch (const std::invalid_argument& e) {
    // Handle path traversal attempt
}
```

## Secure Storage

### Never Hard-Code Credentials

❌ **Never do this**:
```cpp
const std::string API_KEY = "sk_live_1234567890abcdef";
const std::string DB_PASSWORD = "MyS3cr3tP@ssw0rd";
```

✅ **Use environment variables**:
```cpp
#include <cstdlib>
#include <optional>

std::optional<std::string> getEnv(const std::string& name) {
    const char* value = std::getenv(name.c_str());
    if (value == nullptr) {
        return std::nullopt;
    }
    return std::string(value);
}

// Usage
auto apiKey = getEnv("API_KEY");
if (!apiKey) {
    throw std::runtime_error("API_KEY environment variable not set");
}
```

✅ **Use configuration files** (not in version control):
```cpp
// config.json (in .gitignore)
{
  "database": {
    "host": "localhost",
    "password": "secret123"
  },
  "api_key": "sk_live_1234567890abcdef"
}
```

```cpp
// Load from file
#include <fstream>
#include <nlohmann/json.hpp>

nlohmann::json loadConfig(const std::string& path) {
    std::ifstream file(path);
    if (!file.is_open()) {
        throw std::runtime_error("Failed to open config file");
    }
    return nlohmann::json::parse(file);
}

// Usage
auto config = loadConfig("config.json");
std::string password = config["database"]["password"];
```

### Mask Sensitive Data in Logs

```cpp
class Logger {
public:
    void log(const std::string& message) {
        std::cout << message << std::endl;
    }

    void logSensitive(const std::string& message,
                     const std::vector<std::string>& sensitiveFields) {
        std::string masked = message;

        for (const auto& field : sensitiveFields) {
            // Find and replace sensitive data with asterisks
            size_t pos = masked.find(field);
            if (pos != std::string::npos) {
                size_t valueStart = masked.find(':', pos) + 1;
                size_t valueEnd = masked.find_first_of(",}\n", valueStart);
                if (valueEnd == std::string::npos) valueEnd = masked.length();

                masked.replace(valueStart, valueEnd - valueStart, " ****");
            }
        }

        log(masked);
    }
};

// Usage
logger.logSensitive(
    "User login: {email: user@example.com, password: secret123}",
    {"password"}
);
// Output: "User login: {email: user@example.com, password: ****}"
```

### Secure Password Handling

```cpp
#include <openssl/evp.h>
#include <openssl/rand.h>

class PasswordHasher {
public:
    struct HashResult {
        std::vector<uint8_t> hash;
        std::vector<uint8_t> salt;
    };

    static HashResult hashPassword(const std::string& password) {
        // Generate random salt
        std::vector<uint8_t> salt(16);
        RAND_bytes(salt.data(), salt.size());

        // Hash password with salt using PBKDF2
        std::vector<uint8_t> hash(32);
        PKCS5_PBKDF2_HMAC(
            password.c_str(), password.length(),
            salt.data(), salt.size(),
            100000,  // iterations
            EVP_sha256(),
            hash.size(), hash.data()
        );

        return {hash, salt};
    }

    static bool verifyPassword(const std::string& password,
                              const std::vector<uint8_t>& expectedHash,
                              const std::vector<uint8_t>& salt) {
        std::vector<uint8_t> hash(32);
        PKCS5_PBKDF2_HMAC(
            password.c_str(), password.length(),
            salt.data(), salt.size(),
            100000,
            EVP_sha256(),
            hash.size(), hash.data()
        );

        return hash == expectedHash;
    }
};
```

## Dependency Scanning

### Regular Vulnerability Checks

**C++ (vcpkg)**:
```bash
# Check for known vulnerabilities
vcpkg update
vcpkg upgrade --no-dry-run
```

**Python**:
```bash
# Check for vulnerabilities in dependencies
pip install safety
safety check

# Update dependencies
pip list --outdated
pip install --upgrade package-name
```

**Node.js**:
```bash
# Check for vulnerabilities
npm audit

# Fix vulnerabilities automatically
npm audit fix

# Update specific package
npm update package-name
```

**Kotlin/Java (Gradle)**:
```bash
# Use dependency-check plugin
./gradlew dependencyCheckAnalyze

# Update dependencies
./gradlew dependencyUpdates
```

### Pin Versions

Always pin dependency versions to prevent supply chain attacks:

```json
// package.json - Use exact versions
{
  "dependencies": {
    "express": "4.18.2",  // Not "^4.18.2"
    "jsonwebtoken": "9.0.2"
  }
}
```

```toml
# pyproject.toml - Use exact versions for critical dependencies
[tool.poetry.dependencies]
python = "^3.11"
cryptography = "41.0.5"  # Exact version for security-critical package
requests = "^2.31.0"     # Allow minor updates for less critical packages
```

### Automated Scanning in CI/CD

```yaml
# .github/workflows/security.yml
name: Security Scan

on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Run Snyk security scan
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}

      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          format: 'sarif'
          output: 'trivy-results.sarif'

      - name: Upload Trivy results to GitHub Security
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'
```

## Security Best Practices

### Principle of Least Privilege

```cpp
// ❌ Running with root privileges
system("rm -rf /tmp/cache");

// ✅ Drop privileges before sensitive operations
#include <unistd.h>

void dropPrivileges(uid_t uid, gid_t gid) {
    if (setgid(gid) != 0) {
        throw std::runtime_error("Failed to drop group privileges");
    }
    if (setuid(uid) != 0) {
        throw std::runtime_error("Failed to drop user privileges");
    }
}
```

### Secure Defaults

```cpp
class ServerConfig {
public:
    // Secure defaults
    bool enableSsl = true;
    int sessionTimeoutMinutes = 30;
    bool allowWeakCiphers = false;
    std::string allowedOrigins = "";  // Empty = no CORS

    // Force explicit opt-in for insecure options
    void disableSsl() {
        logger_.warn("SSL disabled - only use in development!");
        enableSsl = false;
    }
};
```

### Rate Limiting

```cpp
#include <chrono>
#include <unordered_map>

class RateLimiter {
    struct ClientInfo {
        int requestCount;
        std::chrono::steady_clock::time_point windowStart;
    };

    std::unordered_map<std::string, ClientInfo> clients_;
    const int maxRequests_ = 100;
    const std::chrono::seconds window_{60};

public:
    bool allowRequest(const std::string& clientId) {
        auto now = std::chrono::steady_clock::now();
        auto& info = clients_[clientId];

        // Reset window if expired
        if (now - info.windowStart >= window_) {
            info.requestCount = 0;
            info.windowStart = now;
        }

        // Check limit
        if (info.requestCount >= maxRequests_) {
            return false;
        }

        info.requestCount++;
        return true;
    }
};
```
