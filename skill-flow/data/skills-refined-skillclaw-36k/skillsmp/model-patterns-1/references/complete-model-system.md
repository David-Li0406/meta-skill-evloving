# Model Patterns — Complete Model System

> **Loading Trigger**: Load when implementing complete DTO/domain model separation, custom Codable decoders, or validation framework.

---

## Complete DTO Layer

```swift
// MARK: - DTOs/UserDTO.swift

struct UserDTO: Codable {
    let id: String
    let first_name: String
    let last_name: String
    let email: String
    let avatar_url: String?
    let created_at: String
    let updated_at: String
    let is_verified: Bool
    let role: String
    let profile: ProfileDTO?
    let preferences: PreferencesDTO?
}

struct ProfileDTO: Codable {
    let bio: String?
    let website: String?
    let location: String?
    let phone_number: String?
    let date_of_birth: String?
}

struct PreferencesDTO: Codable {
    let notifications_enabled: Bool
    let marketing_emails: Bool
    let theme: String
    let language: String
}

// MARK: - DTOs/OrderDTO.swift

struct OrderDTO: Codable {
    let id: String
    let user_id: String
    let status: String
    let items: [OrderItemDTO]
    let shipping_address: AddressDTO
    let billing_address: AddressDTO?
    let subtotal: String
    let tax: String
    let shipping_cost: String
    let total: String
    let currency: String
    let created_at: String
    let updated_at: String
    let shipped_at: String?
    let delivered_at: String?
}

struct OrderItemDTO: Codable {
    let id: String
    let product_id: String
    let product_name: String
    let quantity: Int
    let unit_price: String
    let total_price: String
    let variant: VariantDTO?
}

struct VariantDTO: Codable {
    let size: String?
    let color: String?
    let sku: String
}

struct AddressDTO: Codable {
    let line1: String
    let line2: String?
    let city: String
    let state: String
    let postal_code: String
    let country: String
}
```

---

## Complete Domain Models

```swift
// MARK: - Domain/User.swift

struct User: Identifiable, Equatable {
    let id: String
    let fullName: String
    let email: Email
    let avatarURL: URL?
    let createdAt: Date
    let isVerified: Bool
    let role: Role
    let profile: Profile?
    let preferences: Preferences

    enum Role: String {
        case user
        case admin
        case moderator

        var displayName: String {
            rawValue.capitalized
        }

        var canModerate: Bool {
            self == .admin || self == .moderator
        }
    }

    struct Profile: Equatable {
        let bio: String?
        let website: URL?
        let location: String?
        let phoneNumber: PhoneNumber?
        let dateOfBirth: Date?

        var hasContent: Bool {
            bio != nil || website != nil || location != nil
        }
    }

    struct Preferences: Equatable {
        let notificationsEnabled: Bool
        let marketingEmails: Bool
        let theme: Theme
        let language: Language

        enum Theme: String {
            case light, dark, system
        }

        enum Language: String {
            case english = "en"
            case spanish = "es"
            case french = "fr"
        }
    }

    // Computed properties
    var initials: String {
        fullName.split(separator: " ")
            .prefix(2)
            .compactMap { $0.first }
            .map(String.init)
            .joined()
    }

    var displayRole: String {
        role.displayName
    }
}

// MARK: - Domain/Order.swift

struct Order: Identifiable, Equatable {
    let id: String
    let userId: String
    let status: Status
    let items: [OrderItem]
    let shippingAddress: Address
    let billingAddress: Address?
    let pricing: Pricing
    let createdAt: Date
    let shippedAt: Date?
    let deliveredAt: Date?

    enum Status: String {
        case pending
        case confirmed
        case processing
        case shipped
        case delivered
        case cancelled
        case refunded

        var displayName: String {
            rawValue.capitalized
        }

        var color: String {
            switch self {
            case .pending: return "orange"
            case .confirmed, .processing: return "blue"
            case .shipped: return "purple"
            case .delivered: return "green"
            case .cancelled, .refunded: return "red"
            }
        }

        var isActive: Bool {
            switch self {
            case .pending, .confirmed, .processing, .shipped:
                return true
            case .delivered, .cancelled, .refunded:
                return false
            }
        }

        var canCancel: Bool {
            self == .pending || self == .confirmed
        }
    }

    struct Pricing: Equatable {
        let subtotal: Money
        let tax: Money
        let shippingCost: Money
        let total: Money
    }

    // Computed
    var itemCount: Int {
        items.reduce(0) { $0 + $1.quantity }
    }

    var canTrack: Bool {
        status == .shipped
    }
}

struct OrderItem: Identifiable, Equatable {
    let id: String
    let productId: String
    let productName: String
    let quantity: Int
    let unitPrice: Money
    let totalPrice: Money
    let variant: Variant?

    struct Variant: Equatable {
        let size: String?
        let color: String?
        let sku: String

        var displayText: String {
            [size, color].compactMap { $0 }.joined(separator: " / ")
        }
    }
}

struct Address: Equatable {
    let line1: String
    let line2: String?
    let city: String
    let state: String
    let postalCode: String
    let country: String

    var formatted: String {
        var lines = [line1]
        if let line2 = line2 { lines.append(line2) }
        lines.append("\(city), \(state) \(postalCode)")
        lines.append(country)
        return lines.joined(separator: "\n")
    }

    var singleLine: String {
        "\(line1), \(city), \(state) \(postalCode)"
    }
}
```

---

## Type-Safe Wrappers

```swift
// MARK: - TypeWrappers/Email.swift

struct Email: Codable, Hashable, CustomStringConvertible {
    let value: String

    private static let regex = /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i

    init?(_ value: String) {
        let trimmed = value.trimmingCharacters(in: .whitespaces).lowercased()
        guard trimmed.wholeMatch(of: Self.regex) != nil else {
            return nil
        }
        self.value = trimmed
    }

    init(from decoder: Decoder) throws {
        let container = try decoder.singleValueContainer()
        let rawValue = try container.decode(String.self)
        guard let email = Email(rawValue) else {
            throw DecodingError.dataCorrupted(
                .init(codingPath: container.codingPath,
                      debugDescription: "Invalid email format: \(rawValue)")
            )
        }
        self = email
    }

    func encode(to encoder: Encoder) throws {
        var container = encoder.singleValueContainer()
        try container.encode(value)
    }

    var description: String { value }

    var domain: String {
        value.split(separator: "@").last.map(String.init) ?? ""
    }

    var maskedValue: String {
        let parts = value.split(separator: "@")
        guard parts.count == 2 else { return value }

        let local = String(parts[0])
        let domain = String(parts[1])

        if local.count <= 2 {
            return "\(local)***@\(domain)"
        }

        let visible = local.prefix(2)
        return "\(visible)***@\(domain)"
    }
}

// MARK: - TypeWrappers/Money.swift

struct Money: Codable, Hashable, CustomStringConvertible {
    let amount: Decimal
    let currency: Currency

    enum Currency: String, Codable {
        case usd = "USD"
        case eur = "EUR"
        case gbp = "GBP"

        var symbol: String {
            switch self {
            case .usd: return "$"
            case .eur: return "€"
            case .gbp: return "£"
            }
        }
    }

    init(amount: Decimal, currency: Currency = .usd) {
        self.amount = amount
        self.currency = currency
    }

    init?(string: String, currency: Currency = .usd) {
        guard let amount = Decimal(string: string) else { return nil }
        self.amount = amount
        self.currency = currency
    }

    var description: String {
        formatted
    }

    var formatted: String {
        let formatter = NumberFormatter()
        formatter.numberStyle = .currency
        formatter.currencyCode = currency.rawValue
        return formatter.string(from: amount as NSDecimalNumber) ?? "\(currency.symbol)\(amount)"
    }

    var formattedNoSymbol: String {
        let formatter = NumberFormatter()
        formatter.numberStyle = .decimal
        formatter.minimumFractionDigits = 2
        formatter.maximumFractionDigits = 2
        return formatter.string(from: amount as NSDecimalNumber) ?? "\(amount)"
    }

    // Arithmetic
    static func + (lhs: Money, rhs: Money) -> Money {
        precondition(lhs.currency == rhs.currency, "Cannot add different currencies")
        return Money(amount: lhs.amount + rhs.amount, currency: lhs.currency)
    }

    static func * (lhs: Money, rhs: Int) -> Money {
        Money(amount: lhs.amount * Decimal(rhs), currency: lhs.currency)
    }

    static var zero: Money {
        Money(amount: 0)
    }
}

// MARK: - TypeWrappers/PhoneNumber.swift

struct PhoneNumber: Codable, Hashable {
    let countryCode: String
    let number: String

    private static let phoneRegex = /^\+?[1-9]\d{1,14}$/

    init?(raw: String) {
        let cleaned = raw.replacingOccurrences(of: "[^0-9+]", with: "", options: .regularExpression)
        guard cleaned.wholeMatch(of: Self.phoneRegex) != nil else {
            return nil
        }

        if cleaned.hasPrefix("+") {
            // Parse country code
            let digits = String(cleaned.dropFirst())
            // Simplified: assume first 1-3 digits are country code
            let countryCodeLength = digits.count > 10 ? digits.count - 10 : 1
            self.countryCode = String(digits.prefix(countryCodeLength))
            self.number = String(digits.dropFirst(countryCodeLength))
        } else {
            self.countryCode = "1" // Default to US
            self.number = cleaned
        }
    }

    var formatted: String {
        let full = countryCode + number
        // Format as +1 (xxx) xxx-xxxx for US
        if countryCode == "1" && number.count == 10 {
            let area = number.prefix(3)
            let exchange = number.dropFirst(3).prefix(3)
            let subscriber = number.suffix(4)
            return "+1 (\(area)) \(exchange)-\(subscriber)"
        }
        return "+\(full)"
    }

    var e164: String {
        "+\(countryCode)\(number)"
    }
}
```

---

## Complete Mappers

```swift
// MARK: - Mappers/UserMapper.swift

enum UserMapper {

    static func toDomain(_ dto: UserDTO) throws -> User {
        // Required fields
        guard let email = Email(dto.email) else {
            throw MappingError.invalidField("email", value: dto.email)
        }

        guard let role = User.Role(rawValue: dto.role) else {
            throw MappingError.invalidField("role", value: dto.role)
        }

        guard let createdAt = ISO8601DateFormatter().date(from: dto.created_at) else {
            throw MappingError.invalidField("created_at", value: dto.created_at)
        }

        // Optional profile
        let profile: User.Profile? = dto.profile.map { profileDTO in
            User.Profile(
                bio: profileDTO.bio,
                website: profileDTO.website.flatMap(URL.init),
                location: profileDTO.location,
                phoneNumber: profileDTO.phone_number.flatMap(PhoneNumber.init),
                dateOfBirth: profileDTO.date_of_birth.flatMap { ISO8601DateFormatter().date(from: $0) }
            )
        }

        // Preferences with defaults
        let preferences = dto.preferences.map { prefsDTO in
            User.Preferences(
                notificationsEnabled: prefsDTO.notifications_enabled,
                marketingEmails: prefsDTO.marketing_emails,
                theme: User.Preferences.Theme(rawValue: prefsDTO.theme) ?? .system,
                language: User.Preferences.Language(rawValue: prefsDTO.language) ?? .english
            )
        } ?? User.Preferences(
            notificationsEnabled: true,
            marketingEmails: false,
            theme: .system,
            language: .english
        )

        return User(
            id: dto.id,
            fullName: "\(dto.first_name) \(dto.last_name)",
            email: email,
            avatarURL: dto.avatar_url.flatMap(URL.init),
            createdAt: createdAt,
            isVerified: dto.is_verified,
            role: role,
            profile: profile,
            preferences: preferences
        )
    }

    static func toDTO(_ domain: User) -> UserDTO {
        let nameParts = domain.fullName.split(separator: " ", maxSplits: 1)
        let firstName = String(nameParts.first ?? "")
        let lastName = nameParts.count > 1 ? String(nameParts[1]) : ""

        return UserDTO(
            id: domain.id,
            first_name: firstName,
            last_name: lastName,
            email: domain.email.value,
            avatar_url: domain.avatarURL?.absoluteString,
            created_at: ISO8601DateFormatter().string(from: domain.createdAt),
            updated_at: ISO8601DateFormatter().string(from: Date()),
            is_verified: domain.isVerified,
            role: domain.role.rawValue,
            profile: domain.profile.map(ProfileMapper.toDTO),
            preferences: PreferencesMapper.toDTO(domain.preferences)
        )
    }
}

// MARK: - Mappers/OrderMapper.swift

enum OrderMapper {

    static func toDomain(_ dto: OrderDTO) throws -> Order {
        guard let status = Order.Status(rawValue: dto.status) else {
            throw MappingError.invalidField("status", value: dto.status)
        }

        guard let createdAt = ISO8601DateFormatter().date(from: dto.created_at) else {
            throw MappingError.invalidField("created_at", value: dto.created_at)
        }

        let items = try dto.items.map { try OrderItemMapper.toDomain($0) }
        let shippingAddress = AddressMapper.toDomain(dto.shipping_address)
        let billingAddress = dto.billing_address.map(AddressMapper.toDomain)

        guard let subtotal = Money(string: dto.subtotal),
              let tax = Money(string: dto.tax),
              let shippingCost = Money(string: dto.shipping_cost),
              let total = Money(string: dto.total) else {
            throw MappingError.invalidField("pricing", value: "Invalid money format")
        }

        return Order(
            id: dto.id,
            userId: dto.user_id,
            status: status,
            items: items,
            shippingAddress: shippingAddress,
            billingAddress: billingAddress,
            pricing: Order.Pricing(
                subtotal: subtotal,
                tax: tax,
                shippingCost: shippingCost,
                total: total
            ),
            createdAt: createdAt,
            shippedAt: dto.shipped_at.flatMap { ISO8601DateFormatter().date(from: $0) },
            deliveredAt: dto.delivered_at.flatMap { ISO8601DateFormatter().date(from: $0) }
        )
    }
}

// MARK: - MappingError.swift

enum MappingError: LocalizedError {
    case invalidField(String, value: String)
    case missingField(String)
    case typeMismatch(expected: String, got: String)

    var errorDescription: String? {
        switch self {
        case .invalidField(let field, let value):
            return "Invalid value '\(value)' for field '\(field)'"
        case .missingField(let field):
            return "Missing required field '\(field)'"
        case .typeMismatch(let expected, let got):
            return "Type mismatch: expected \(expected), got \(got)"
        }
    }
}
```

---

## Validation Framework

```swift
// MARK: - Validation/Validator.swift

protocol Validator<Value> {
    associatedtype Value
    func validate(_ value: Value) -> ValidationResult
}

enum ValidationResult {
    case valid
    case invalid([ValidationFailure])

    var isValid: Bool {
        if case .valid = self { return true }
        return false
    }

    var failures: [ValidationFailure] {
        guard case .invalid(let failures) = self else { return [] }
        return failures
    }
}

struct ValidationFailure: Error, Equatable {
    let field: String
    let message: String
    let code: String?

    init(field: String, message: String, code: String? = nil) {
        self.field = field
        self.message = message
        self.code = code
    }
}

// MARK: - Validation/UserValidator.swift

struct UserValidator: Validator {
    typealias Value = UserFormData

    func validate(_ value: UserFormData) -> ValidationResult {
        var failures: [ValidationFailure] = []

        // Name validation
        if value.name.trimmingCharacters(in: .whitespaces).isEmpty {
            failures.append(ValidationFailure(
                field: "name",
                message: "Name is required",
                code: "required"
            ))
        } else if value.name.count < 2 {
            failures.append(ValidationFailure(
                field: "name",
                message: "Name must be at least 2 characters",
                code: "min_length"
            ))
        }

        // Email validation
        if value.email.trimmingCharacters(in: .whitespaces).isEmpty {
            failures.append(ValidationFailure(
                field: "email",
                message: "Email is required",
                code: "required"
            ))
        } else if Email(value.email) == nil {
            failures.append(ValidationFailure(
                field: "email",
                message: "Please enter a valid email address",
                code: "invalid_format"
            ))
        }

        // Password validation (if present)
        if let password = value.password, !password.isEmpty {
            if password.count < 8 {
                failures.append(ValidationFailure(
                    field: "password",
                    message: "Password must be at least 8 characters",
                    code: "min_length"
                ))
            }

            if !password.contains(where: { $0.isNumber }) {
                failures.append(ValidationFailure(
                    field: "password",
                    message: "Password must contain at least one number",
                    code: "missing_number"
                ))
            }

            if !password.contains(where: { $0.isUppercase }) {
                failures.append(ValidationFailure(
                    field: "password",
                    message: "Password must contain at least one uppercase letter",
                    code: "missing_uppercase"
                ))
            }
        }

        return failures.isEmpty ? .valid : .invalid(failures)
    }
}

// MARK: - Form Data

struct UserFormData {
    var name: String
    var email: String
    var password: String?

    var isValid: Bool {
        UserValidator().validate(self).isValid
    }

    var validationErrors: [String: String] {
        let result = UserValidator().validate(self)
        guard case .invalid(let failures) = result else { return [:] }
        return Dictionary(uniqueKeysWithValues: failures.map { ($0.field, $0.message) })
    }
}
```
