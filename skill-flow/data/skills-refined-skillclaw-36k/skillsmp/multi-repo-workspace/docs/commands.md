# Commands Reference

Complete reference for all `@workspace` commands.

---

## @workspace init

Initialize a new workspace.

### Syntax
```
@workspace init [name]
```

### Parameters
- `name` (optional): Name for the workspace

### Behavior
1. Prompts for workspace base path
2. Asks which repositories to include
3. Analyzes each repository
4. Detects repository types
5. Creates dependency graph
6. Generates workspace configuration

### Example
```
@workspace init my-project

# Claude responds:
# "What is the base path of your workspace?"
# You: /Users/me/projects/my-project
#
# "Which repositories should I include?"
# You: frontend, backend, shared
#
# Claude analyzes and shows summary
```

### Output
- Repository inventory
- Detected types and tech stacks
- Dependency relationships
- Configuration status
- Recommendations

---

## @workspace add

Add a new repository to the workspace.

### Syntax
```
@workspace add [path]
```

### Parameters
- `path` (required): Relative or absolute path to repository

### Behavior
1. Analyzes repository at given path
2. Detects repository type
3. Reads configuration files
4. Updates workspace dependency graph
5. Identifies integration points

### Example
```
@workspace add ./new-service

# Claude analyzes and responds:
# Repository: new-service
# Type: backend
# Tech Stack: Node.js, Express, PostgreSQL
# Dependencies: shared-types
# Added to workspace successfully
```

### Output
- Repository details
- Detected type
- Tech stack
- Dependencies
- Integration points with existing repos

---

## @workspace analyze

Analyze the entire workspace.

### Syntax
```
@workspace analyze
```

### Parameters
None

### Behavior
1. Scans all repositories
2. Reads all configuration files
3. Analyzes dependencies
4. Detects inconsistencies
5. Identifies technical debt
6. Generates comprehensive report

### Example
```
@workspace analyze

# Claude provides detailed analysis
```

### Output

#### Repository Inventory
```
📦 Repositories (5)
├── frontend (React, TypeScript)
├── backend (Node.js, Express)
├── mobile (React Native)
├── shared-ui (React Components)
└── api-client (TypeScript)
```

#### Dependency Graph
```
Dependencies:
frontend → shared-ui, api-client
mobile → shared-ui, api-client
backend → api-client
shared-ui → (none)
api-client → (none)
```

#### Tech Stack Summary
```
Languages: TypeScript (5), JavaScript (2)
Frameworks: React (3), Express (1), React Native (1)
Build Tools: Vite (2), Webpack (1), Metro (1)
```

#### Configuration Status
```
✅ frontend: Fully configured
✅ backend: Fully configured
⚠️  mobile: Missing .claude/context.md
❌ shared-ui: No configuration found
```

#### Inconsistencies
```
⚠️  React versions differ:
   - frontend: 18.2.0
   - mobile: 18.1.0
   - shared-ui: 17.0.2

⚠️  Code styles differ:
   - frontend: airbnb
   - backend: standard
```

#### Recommendations
```
1. Standardize React version across repos
2. Add configuration to shared-ui
3. Complete mobile context documentation
4. Consider unified ESLint config
```

---

## @workspace focus

Focus on a specific repository.

### Syntax
```
@workspace focus [repo]
```

### Parameters
- `repo` (required): Repository name

### Behavior
1. Loads repository configuration
2. Reads context documentation
3. Sets active repository context
4. Adjusts code generation preferences
5. Applies repository-specific conventions

### Example
```
@workspace focus frontend

# Claude responds:
# Now focused on: frontend
# Type: Frontend (React, TypeScript, Vite)
# Conventions: Airbnb style, functional components
# Testing: Vitest
# Ready to work on this repository
```

### Output
- Repository details
- Active conventions
- Code generation preferences
- Testing framework
- Available commands

### Usage After Focus

All subsequent code generation will:
- Follow repository conventions
- Use repository tech stack
- Apply repository preferences
- Consider repository dependencies

```
# After focusing on frontend:
"Add a new component for user profile"

# Claude generates:
# - Functional React component
# - TypeScript types
# - Vitest tests
# - Following Airbnb style
# - Using repository patterns
```

---

## @workspace task

Execute a task across multiple repositories.

### Syntax
```
@workspace task [description]
```

### Parameters
- `description` (required): Task description

### Behavior
1. Analyzes task requirements
2. Identifies affected repositories
3. Determines dependency order
4. Proposes changes for each repo
5. Coordinates implementation
6. Suggests verification steps

### Example
```
@workspace task "Add OAuth authentication"

# Claude analyzes and responds:
```

### Output

#### Affected Repositories
```
📋 Task: Add OAuth authentication

Affected repositories:
1. backend (primary)
2. frontend (primary)
3. shared-types (supporting)
4. api-client (supporting)
```

#### Implementation Order
```
Implementation order:
1. shared-types: Add OAuth types
2. backend: Implement OAuth endpoints
3. api-client: Add OAuth methods
4. frontend: Add OAuth UI
```

#### Proposed Changes

**shared-types**
```typescript
// Add OAuth types
export interface OAuthToken {
  access_token: string;
  refresh_token: string;
  expires_in: number;
}
```

**backend**
```typescript
// Add OAuth routes
router.post('/auth/oauth/google', oauthController.google);
router.post('/auth/oauth/refresh', oauthController.refresh);
```

**api-client**
```typescript
// Add OAuth methods
export const oauth = {
  google: (code: string) => api.post('/auth/oauth/google', { code }),
  refresh: (token: string) => api.post('/auth/oauth/refresh', { token })
};
```

**frontend**
```typescript
// Add OAuth UI
export const OAuthButton = () => {
  const handleOAuth = () => {
    // Implementation
  };
  return <button onClick={handleOAuth}>Sign in with Google</button>;
};
```

#### Integration Points
```
Integration points:
- frontend calls api-client.oauth methods
- api-client uses shared-types.OAuthToken
- backend returns shared-types.OAuthToken
```

#### Verification Steps
```
Verification:
1. Test OAuth flow in backend
2. Test API client methods
3. Test frontend UI
4. Test end-to-end flow
5. Verify token refresh
```

---

## Advanced Usage

### Chaining Commands

```
@workspace init my-project
@workspace add ./new-repo
@workspace analyze
@workspace focus frontend
```

### Combining with Other Instructions

```
@workspace focus backend
Now add a new REST endpoint for user profiles with full CRUD operations
```

### Context Switching

```
@workspace focus frontend
# Work on frontend...

@workspace focus backend
# Switch to backend...

@workspace task "Sync user data"
# Coordinate across both
```

---

## Command Aliases

Some commands support aliases:

```
@workspace init = @workspace initialize
@workspace add = @workspace include
@workspace analyze = @workspace scan = @workspace review
@workspace focus = @workspace switch = @workspace use
@workspace task = @workspace do = @workspace execute
```

---

## Tips

### 1. Use Descriptive Names
```
✅ @workspace init ecommerce-platform
❌ @workspace init proj
```

### 2. Be Specific in Tasks
```
✅ @workspace task "Add user authentication with JWT tokens"
❌ @workspace task "add auth"
```

### 3. Focus Before Detailed Work
```
@workspace focus frontend
# Then ask for specific changes
```

### 4. Analyze Regularly
```
# After major changes:
@workspace analyze
```

### 5. Use Absolute Paths for Add
```
✅ @workspace add /Users/me/projects/new-repo
✅ @workspace add ./relative/path
❌ @workspace add new-repo
```

---

## Next Steps

- 📖 Read [Best Practices](./best-practices.md)
- 📖 Review [Setup Guide](./setup-guide.md)
- 🔍 Check [Examples](../examples/)
