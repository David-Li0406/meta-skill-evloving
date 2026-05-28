# Functional Decomposition

Break down what the system must do into a capability tree.

## Capability Tree Structure

```
Capability (system-level ability)
├── Feature (user-facing function)
│   ├── Sub-feature (specific behavior)
│   └── Sub-feature
└── Feature
    ├── Sub-feature
    └── Sub-feature
```

## Example Decomposition

```
## Capabilities

### 1. User Authentication
Capability: System can verify user identity

#### 1.1 Login
- Email/password authentication
- Session management
- Remember me functionality

#### 1.2 Registration
- Account creation
- Email verification
- Profile setup

#### 1.3 Password Recovery
- Reset request
- Token validation
- Password update

### 2. User Management
Capability: System can manage user data

#### 2.1 Profile
- View profile
- Edit profile
- Upload avatar

#### 2.2 Preferences
- Notification settings
- Theme selection
- Language preference
```

## Decomposition Rules

1. **Capabilities** = What the system can do (verbs)
2. **Features** = How users interact (user stories)
3. **Sub-features** = Specific behaviors (acceptance criteria)

## Depth Guidelines

- **2 levels** for simple projects
- **3 levels** for complex systems
- **4+ levels** = probably over-engineering

## Verification Questions

For each capability:
- Does it solve part of the problem?
- Can it be tested independently?
- Does it map to code structure?

## Output Format for PRD

```
## Functional Requirements

### Capability: [Name]
[One-line description]

**Features:**
1. [Feature name]
   - [Sub-feature]
   - [Sub-feature]
2. [Feature name]
   - [Sub-feature]
```
