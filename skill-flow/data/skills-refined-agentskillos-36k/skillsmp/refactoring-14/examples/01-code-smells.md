# Code Smells - Identification and Remediation

Complete guide to identifying and fixing common code smells with practical examples.

## 📝 Prompt

```
Identify and fix code smells in this user management class:

The code handles user operations but has grown too large and complex.
Show me:
- What code smells are present
- Why they're problems
- How to refactor each one
- The refactored code

Focus on:
- Large Class / God Object
- Long Method
- Duplicate Code
- Feature Envy
- Data Clumps
```

## 🔴 Before: Code with Smells

```typescript
// ❌ BAD: Multiple code smells
class UserManager {
    private users: Map<string, any> = new Map();
    private database: Database;
    private emailService: EmailService;
    private logger: Logger;
    private config: Config;
    
    constructor(database: Database, emailService: EmailService, logger: Logger, config: Config) {
        this.database = database;
        this.emailService = emailService;
        this.logger = logger;
        this.config = config;
    }
    
    // CODE SMELL: Long Method (100+ lines)
    async createUser(email: string, password: string, firstName: string, lastName: string, phone: string, address: string, city: string, country: string, postalCode: string) {
        // Validation
        if (!email || email.length === 0) {
            throw new Error("Email is required");
        }
        if (!email.includes('@')) {
            throw new Error("Email is invalid");
        }
        if (!password || password.length < 8) {
            throw new Error("Password must be at least 8 characters");
        }
        if (!/[A-Z]/.test(password)) {
            throw new Error("Password must contain uppercase");
        }
        if (!/[a-z]/.test(password)) {
            throw new Error("Password must contain lowercase");
        }
        if (!/[0-9]/.test(password)) {
            throw new Error("Password must contain number");
        }
        if (!firstName || firstName.length === 0) {
            throw new Error("First name is required");
        }
        if (!lastName || lastName.length === 0) {
            throw new Error("Last name is required");
        }
        
        // Check if user exists
        const existingUser = await this.database.query(
            'SELECT * FROM users WHERE email = $1',
            [email]
        );
        if (existingUser.length > 0) {
            throw new Error("User already exists");
        }
        
        // Hash password
        const salt = crypto.randomBytes(16).toString('hex');
        const hash = crypto.pbkdf2Sync(password, salt, 1000, 64, 'sha512').toString('hex');
        
        // Create user
        const userId = uuidv4();
        const createdAt = new Date();
        
        await this.database.query(
            'INSERT INTO users (id, email, password_hash, password_salt, first_name, last_name, phone, address, city, country, postal_code, created_at) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)',
            [userId, email, hash, salt, firstName, lastName, phone, address, city, country, postalCode, createdAt]
        );
        
        // Send welcome email
        const emailBody = `
            <html>
                <body>
                    <h1>Welcome ${firstName}!</h1>
                    <p>Thank you for joining us.</p>
                    <p>Your account has been created successfully.</p>
                </body>
            </html>
        `;
        
        try {
            await this.emailService.send({
                to: email,
                subject: 'Welcome!',
                html: emailBody
            });
        } catch (error) {
            this.logger.error('Failed to send welcome email', error);
        }
        
        // Log
        this.logger.info(`User created: ${userId}`);
        
        // Return user
        return {
            id: userId,
            email,
            firstName,
            lastName,
            phone,
            address,
            city,
            country,
            postalCode,
            createdAt
        };
    }
    
    // CODE SMELL: Duplicate Code (similar to createUser validation)
    async updateUser(userId: string, email: string, password: string, firstName: string, lastName: string, phone: string, address: string, city: string, country: string, postalCode: string) {
        // Validation (DUPLICATED)
        if (!email || email.length === 0) {
            throw new Error("Email is required");
        }
        if (!email.includes('@')) {
            throw new Error("Email is invalid");
        }
        if (password && password.length < 8) {
            throw new Error("Password must be at least 8 characters");
        }
        // ... more duplicate validation
        
        // Update logic
        // ...
    }
    
    // CODE SMELL: Feature Envy (uses emailService more than own data)
    async sendPasswordReset(email: string) {
        const token = crypto.randomBytes(32).toString('hex');
        const expiry = new Date(Date.now() + 3600000); // 1 hour
        
        await this.database.query(
            'INSERT INTO password_resets (email, token, expiry) VALUES ($1, $2, $3)',
            [email, token, expiry]
        );
        
        const resetLink = `${this.config.baseUrl}/reset-password?token=${token}`;
        const emailBody = `
            <html>
                <body>
                    <h1>Password Reset</h1>
                    <p>Click the link below to reset your password:</p>
                    <a href="${resetLink}">Reset Password</a>
                    <p>This link expires in 1 hour.</p>
                </body>
            </html>
        `;
        
        await this.emailService.send({
            to: email,
            subject: 'Password Reset',
            html: emailBody
        });
    }
    
    // CODE SMELL: Long Parameter List & Data Clumps
    async searchUsers(firstName: string, lastName: string, email: string, city: string, country: string, minAge: number, maxAge: number, sortBy: string, sortOrder: string, page: number, pageSize: number) {
        // Search logic with 11 parameters
        // ...
    }
}
```

## 🟢 After: Refactored Code

### 1. Extract Value Objects (Fix Data Clumps)

```typescript
// Value Objects
class Email {
    constructor(private readonly value: string) {
        this.validate();
    }
    
    private validate(): void {
        if (!this.value || !this.value.includes('@')) {
            throw new Error('Invalid email address');
        }
    }
    
    toString(): string {
        return this.value;
    }
}

class Password {
    private readonly value: string;
    
    constructor(value: string) {
        this.validate(value);
        this.value = value;
    }
    
    private validate(password: string): void {
        if (!password || password.length < 8) {
            throw new Error('Password must be at least 8 characters');
        }
        if (!/[A-Z]/.test(password)) {
            throw new Error('Password must contain uppercase letter');
        }
        if (!/[a-z]/.test(password)) {
            throw new Error('Password must contain lowercase letter');
        }
        if (!/[0-9]/.test(password)) {
            throw new Error('Password must contain number');
        }
    }
    
    async hash(): Promise<HashedPassword> {
        const salt = crypto.randomBytes(16).toString('hex');
        const hash = crypto.pbkdf2Sync(this.value, salt, 1000, 64, 'sha512').toString('hex');
        return new HashedPassword(hash, salt);
    }
}

class HashedPassword {
    constructor(
        public readonly hash: string,
        public readonly salt: string
    ) {}
}

class Address {
    constructor(
        public readonly street: string,
        public readonly city: string,
        public readonly country: string,
        public readonly postalCode: string
    ) {
        this.validate();
    }
    
    private validate(): void {
        if (!this.city || !this.country) {
            throw new Error('City and country are required');
        }
    }
}

class UserProfile {
    constructor(
        public readonly firstName: string,
        public readonly lastName: string,
        public readonly phone: string
    ) {
        this.validate();
    }
    
    private validate(): void {
        if (!this.firstName || !this.lastName) {
            throw new Error('First and last name are required');
        }
    }
    
    get fullName(): string {
        return `${this.firstName} ${this.lastName}`;
    }
}
```

### 2. Extract Classes (Fix Large Class)

```typescript
// User Entity
class User {
    constructor(
        public readonly id: string,
        public readonly email: Email,
        private passwordHash: HashedPassword,
        public readonly profile: UserProfile,
        public readonly address: Address,
        public readonly createdAt: Date
    ) {}
    
    static create(
        email: Email,
        password: Password,
        profile: UserProfile,
        address: Address
    ): Promise<User> {
        return User.build(
            uuidv4(),
            email,
            await password.hash(),
            profile,
            address,
            new Date()
        );
    }
}

// Repository Pattern
interface UserRepository {
    save(user: User): Promise<void>;
    findByEmail(email: Email): Promise<User | null>;
    findById(id: string): Promise<User | null>;
    search(criteria: SearchCriteria): Promise<User[]>;
}

class PostgresUserRepository implements UserRepository {
    constructor(private database: Database) {}
    
    async save(user: User): Promise<void> {
        await this.database.query(
            `INSERT INTO users (id, email, password_hash, password_salt, first_name, last_name, phone, address, city, country, postal_code, created_at)
             VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)`,
            [
                user.id,
                user.email.toString(),
                user.passwordHash.hash,
                user.passwordHash.salt,
                user.profile.firstName,
                user.profile.lastName,
                user.profile.phone,
                user.address.street,
                user.address.city,
                user.address.country,
                user.address.postalCode,
                user.createdAt
            ]
        );
    }
    
    async findByEmail(email: Email): Promise<User | null> {
        const result = await this.database.query(
            'SELECT * FROM users WHERE email = $1',
            [email.toString()]
        );
        
        return result.length > 0 ? this.mapToUser(result[0]) : null;
    }
    
    private mapToUser(row: any): User {
        // Map database row to User entity
        return new User(
            row.id,
            new Email(row.email),
            new HashedPassword(row.password_hash, row.password_salt),
            new UserProfile(row.first_name, row.last_name, row.phone),
            new Address(row.address, row.city, row.country, row.postal_code),
            row.created_at
        );
    }
}
```

### 3. Extract Services (Fix Feature Envy)

```typescript
// Email Notification Service
class EmailNotificationService {
    constructor(
        private emailService: EmailService,
        private templateEngine: TemplateEngine
    ) {}
    
    async sendWelcomeEmail(user: User): Promise<void> {
        const html = this.templateEngine.render('welcome', {
            firstName: user.profile.firstName,
            email: user.email.toString()
        });
        
        await this.emailService.send({
            to: user.email.toString(),
            subject: 'Welcome!',
            html
        });
    }
    
    async sendPasswordReset(email: Email, resetToken: string, baseUrl: string): Promise<void> {
        const resetLink = `${baseUrl}/reset-password?token=${resetToken}`;
        const html = this.templateEngine.render('password-reset', {
            resetLink,
            expiryHours: 1
        });
        
        await this.emailService.send({
            to: email.toString(),
            subject: 'Password Reset',
            html
        });
    }
}

// Password Reset Service
class PasswordResetService {
    constructor(
        private database: Database,
        private notificationService: EmailNotificationService,
        private config: Config
    ) {}
    
    async initiateReset(email: Email): Promise<void> {
        const token = this.generateToken();
        const expiry = this.calculateExpiry();
        
        await this.saveResetToken(email, token, expiry);
        await this.notificationService.sendPasswordReset(
            email,
            token,
            this.config.baseUrl
        );
    }
    
    private generateToken(): string {
        return crypto.randomBytes(32).toString('hex');
    }
    
    private calculateExpiry(): Date {
        return new Date(Date.now() + 3600000); // 1 hour
    }
    
    private async saveResetToken(email: Email, token: string, expiry: Date): Promise<void> {
        await this.database.query(
            'INSERT INTO password_resets (email, token, expiry) VALUES ($1, $2, $3)',
            [email.toString(), token, expiry]
        );
    }
}
```

### 4. Extract Use Cases (Fix Long Method)

```typescript
// Use Case: Create User
class CreateUserUseCase {
    constructor(
        private userRepository: UserRepository,
        private notificationService: EmailNotificationService,
        private logger: Logger
    ) {}
    
    async execute(request: CreateUserRequest): Promise<User> {
        // 1. Check if user already exists
        await this.ensureUserDoesNotExist(request.email);
        
        // 2. Create user entity
        const user = await this.createUser(request);
        
        // 3. Save to database
        await this.userRepository.save(user);
        
        // 4. Send welcome email (async, don't wait)
        this.sendWelcomeEmailAsync(user);
        
        // 5. Log
        this.logger.info(`User created: ${user.id}`);
        
        return user;
    }
    
    private async ensureUserDoesNotExist(email: Email): Promise<void> {
        const existing = await this.userRepository.findByEmail(email);
        if (existing) {
            throw new Error('User already exists');
        }
    }
    
    private async createUser(request: CreateUserRequest): Promise<User> {
        return User.create(
            new Email(request.email),
            new Password(request.password),
            new UserProfile(request.firstName, request.lastName, request.phone),
            new Address(request.address, request.city, request.country, request.postalCode)
        );
    }
    
    private async sendWelcomeEmailAsync(user: User): Promise<void> {
        try {
            await this.notificationService.sendWelcomeEmail(user);
        } catch (error) {
            this.logger.error('Failed to send welcome email', error);
        }
    }
}

interface CreateUserRequest {
    email: string;
    password: string;
    firstName: string;
    lastName: string;
    phone: string;
    address: string;
    city: string;
    country: string;
    postalCode: string;
}
```

### 5. Extract Search Criteria (Fix Long Parameter List)

```typescript
// Search Criteria Value Object
class SearchCriteria {
    constructor(
        public readonly filters: UserFilters,
        public readonly sorting: SortOptions,
        public readonly pagination: PaginationOptions
    ) {}
}

class UserFilters {
    constructor(
        public readonly firstName?: string,
        public readonly lastName?: string,
        public readonly email?: string,
        public readonly city?: string,
        public readonly country?: string,
        public readonly ageRange?: AgeRange
    ) {}
}

class AgeRange {
    constructor(
        public readonly min: number,
        public readonly max: number
    ) {
        if (min > max) {
            throw new Error('Invalid age range');
        }
    }
}

class SortOptions {
    constructor(
        public readonly field: string,
        public readonly order: 'asc' | 'desc' = 'asc'
    ) {}
}

class PaginationOptions {
    constructor(
        public readonly page: number = 1,
        public readonly pageSize: number = 20
    ) {
        if (page < 1) throw new Error('Page must be >= 1');
        if (pageSize < 1 || pageSize > 100) {
            throw new Error('Page size must be between 1 and 100');
        }
    }
    
    get offset(): number {
        return (this.page - 1) * this.pageSize;
    }
}

// Use Case: Search Users
class SearchUsersUseCase {
    constructor(private userRepository: UserRepository) {}
    
    async execute(criteria: SearchCriteria): Promise<User[]> {
        return this.userRepository.search(criteria);
    }
}
```

### 6. Final Clean UserManager (Controller)

```typescript
// ✅ GOOD: Clean, focused controller
class UserController {
    constructor(
        private createUserUseCase: CreateUserUseCase,
        private searchUsersUseCase: SearchUsersUseCase,
        private passwordResetService: PasswordResetService
    ) {}
    
    async createUser(request: CreateUserRequest): Promise<UserResponse> {
        const user = await this.createUserUseCase.execute(request);
        return this.toResponse(user);
    }
    
    async searchUsers(criteria: SearchCriteria): Promise<UserResponse[]> {
        const users = await this.searchUsersUseCase.execute(criteria);
        return users.map(u => this.toResponse(u));
    }
    
    async initiatePasswordReset(email: string): Promise<void> {
        await this.passwordResetService.initiateReset(new Email(email));
    }
    
    private toResponse(user: User): UserResponse {
        return {
            id: user.id,
            email: user.email.toString(),
            firstName: user.profile.firstName,
            lastName: user.profile.lastName,
            fullName: user.profile.fullName,
            phone: user.profile.phone,
            address: {
                street: user.address.street,
                city: user.address.city,
                country: user.address.country,
                postalCode: user.address.postalCode
            },
            createdAt: user.createdAt.toISOString()
        };
    }
}

interface UserResponse {
    id: string;
    email: string;
    firstName: string;
    lastName: string;
    fullName: string;
    phone: string;
    address: {
        street: string;
        city: string;
        country: string;
        postalCode: string;
    };
    createdAt: string;
}
```

## ✅ Benefits of Refactoring

### Before vs After Comparison

| Aspect | Before | After | Improvement |
|--------|--------|-------|-------------|
| **Lines per method** | 100+ | < 20 | 80% reduction |
| **Parameters** | 11 | 1-3 | Clearer interfaces |
| **Responsibilities** | 10+ | 1 per class | Single Responsibility |
| **Testability** | Hard | Easy | Isolated units |
| **Reusability** | Low | High | Composable |
| **Duplication** | High | None | DRY principle |
| **Coupling** | Tight | Loose | Independent modules |
| **Cohesion** | Low | High | Related logic together |

### Code Smells Fixed

1. ✅ **Large Class** → Extracted into multiple focused classes
2. ✅ **Long Method** → Broke into small, single-purpose methods
3. ✅ **Long Parameter List** → Value objects and domain models
4. ✅ **Duplicate Code** → Centralized validation logic
5. ✅ **Feature Envy** → Extracted to appropriate services
6. ✅ **Data Clumps** → Created value objects (Address, UserProfile)
7. ✅ **Primitive Obsession** → Type-safe value objects
8. ✅ **Comments** → Self-documenting code

## 💡 Key Refactoring Principles

1. **Single Responsibility Principle**: Each class has one reason to change
2. **Open/Closed Principle**: Open for extension, closed for modification
3. **Dependency Inversion**: Depend on abstractions, not concretions
4. **Value Objects**: Immutable objects representing domain concepts
5. **Repository Pattern**: Abstracts data access
6. **Use Case Pattern**: Encapsulates business logic
7. **Domain-Driven Design**: Models reflect business domain

## 🎯 Testing Benefits

```typescript
// Before: Hard to test (requires database, email service, logger)
test('createUser - hard', async () => {
    const db = new RealDatabase(); // Requires real DB
    const emailService = new RealEmailService(); // Sends real emails
    const manager = new UserManager(db, emailService, logger, config);
    // Difficult to test in isolation
});

// After: Easy to test (mocks/stubs)
test('CreateUserUseCase - easy', async () => {
    const mockRepository = {
        save: jest.fn(),
        findByEmail: jest.fn().mockResolvedValue(null)
    };
    const mockNotification = {
        sendWelcomeEmail: jest.fn()
    };
    const useCase = new CreateUserUseCase(mockRepository, mockNotification, logger);
    
    await useCase.execute({
        email: 'test@example.com',
        password: 'Test123!',
        firstName: 'John',
        lastName: 'Doe',
        phone: '123456',
        address: '123 St',
        city: 'City',
        country: 'Country',
        postalCode: '12345'
    });
    
    expect(mockRepository.save).toHaveBeenCalled();
    expect(mockNotification.sendWelcomeEmail).toHaveBeenCalled();
});
```
