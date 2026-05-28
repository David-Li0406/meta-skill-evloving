# Breaking Changes Documentation

## Purpose

Breaking changes alter public APIs, behavior, or contracts in ways that require users to modify their code. Proper documentation prevents surprises and enables smooth upgrades.

## When to Document Breaking Changes

### Always Document

**API Changes:**
- Function signature modifications
- Removed or renamed public methods
- Changed return types
- Modified parameter requirements
- Altered error behaviors

**Behavioral Changes:**
- Different default values
- Modified validation rules
- Changed side effects
- Altered timing or ordering
- Modified error handling

**Configuration Changes:**
- Removed configuration options
- Changed configuration format
- Modified environment variable names
- Altered default settings

**Dependency Changes:**
- Increased minimum version requirements
- Removed platform support
- Changed runtime requirements

### Not Breaking Changes

**Internal Changes:**
- Refactored internal code
- Optimized performance without behavior changes
- Fixed bugs to match documented behavior
- Improved error messages

**Additions:**
- New optional parameters with defaults
- New optional configuration fields
- New API endpoints
- New error codes (if properly handled by clients)

**Deprecations (without removal):**
- Marking features as deprecated
- Adding deprecation warnings
- Providing migration paths

## Breaking Change Format

### Required Elements

**1. Exclamation Mark in Subject**

Add `!` after the type (or scope if present):

```
feat!: change API response format
fix(api)!: correct user validation behavior
refactor(auth)!: simplify token structure
```

**Placement rules:**
- After type if no scope: `feat!:`
- After scope if present: `feat(api)!:`
- Not after description: `feat: change api!` ❌

**2. BREAKING CHANGE Footer**

Always include `BREAKING CHANGE:` footer with description:

```
feat(api)!: change authentication response format

Modify login endpoint to return token object instead of plain string.
This provides additional metadata for clients.

BREAKING CHANGE: AuthService.login() now returns {token: string,
expiresIn: number} instead of just the token string. Update all
clients to access response.token.
```

### Both Are Required

The `!` and `BREAKING CHANGE:` footer work together:

**Correct (both present):**
```
feat!: change config format

BREAKING CHANGE: Configuration now uses YAML instead of JSON.
```

**Incorrect (missing footer):**
```
feat!: change config format
```
❌ Has `!` but no `BREAKING CHANGE:` footer

**Incorrect (missing !):**
```
feat: change config format

BREAKING CHANGE: Configuration now uses YAML instead of JSON.
```
❌ Has footer but no `!` in subject

## Writing Good Breaking Change Descriptions

### Include What Changed

Be specific about the API or behavior change:

**Vague:**
```
BREAKING CHANGE: API changed.
```
❌ Doesn't explain what changed

**Clear:**
```
BREAKING CHANGE: UserService.create() now requires an email parameter
as the second argument. Previous signature: create(name), new
signature: create(name, email).
```
✅ Explains exact change

### Include Why It Changed

Explain the motivation:

```
BREAKING CHANGE: Remove support for Node 12. Node 12 reached end of
life and preventing use of modern ECMAScript features. Minimum
version is now Node 14.
```

### Include Migration Steps

Tell users how to adapt:

**Without migration steps:**
```
BREAKING CHANGE: Config format changed to YAML.
```
❌ Doesn't help users migrate

**With migration steps:**
```
BREAKING CHANGE: Config format changed from JSON to YAML. Convert
config.json to config.yaml using `json2yaml config.json > config.yaml`.
Update imports to reference config.yaml instead of config.json.
```
✅ Clear migration path

### Include Examples

Show before and after:

```
BREAKING CHANGE: Authentication middleware now returns 401 instead of
403 for missing tokens.

Before:
  fetch('/api/data')  // Returns 403 Forbidden

After:
  fetch('/api/data')  // Returns 401 Unauthorized

Update error handling to check for 401 status code.
```

## Multiple Breaking Changes

When one commit includes multiple breaking changes, list all in the footer:

```
refactor(api)!: overhaul authentication system

Complete rewrite of authentication to support multiple auth providers.

BREAKING CHANGE: AuthService.login() signature changed from
login(username, password) to login(credentials) where credentials
is an object {username, password, provider?}.

BREAKING CHANGE: Session tokens now expire after 1 hour instead of
24 hours. Clients must implement token refresh logic.

BREAKING CHANGE: /auth/logout endpoint now requires POST instead of
GET for security. Update all logout calls to use POST method.
```

**Note:** Still only one `!` in the subject, but multiple `BREAKING CHANGE:` footers.

## Pre-release Exceptions

### The Rule

Unless explicitly told "this is prerelease, don't worry about breaking changes," always include breaking change notation.

### When to Omit

**User explicitly states:**
- "This is prerelease, don't worry about breaking changes"
- "We're in beta, breaking changes are expected"
- "Version 0.x, breaking changes don't need special notation"

**In these cases:**
- Omit `!` from subject
- Omit `BREAKING CHANGE:` footer
- Still explain changes in commit body

**Example for prerelease:**
```
refactor(api): change authentication response format

Modify login endpoint to return token object instead of plain string.
This provides additional metadata for clients. Since we're in beta,
this change doesn't require special breaking change notation.

Update all clients to access response.token instead of using the
response directly.
```

### When NOT to Omit

**Even in prerelease, include breaking notation if:**
- Project has external users/adopters
- Maintaining a changelog
- Changes affect published APIs
- Team has agreed to track breaking changes

**When in doubt, include it.** It's better to over-document than under-document.

## Version Number Impact

### Semantic Versioning

Breaking changes trigger major version bumps:

- `1.2.3 → 2.0.0` for breaking change
- `0.2.3 → 0.3.0` for breaking change in 0.x versions (different convention)

### Pre-1.0 Versions

For `0.x.y` versions, breaking changes typically bump the minor version:

```
0.2.3 → 0.3.0   (breaking change)
0.3.0 → 0.3.1   (bug fix)
0.3.1 → 0.4.0   (another breaking change)
```

Some projects treat `0.x` as prerelease and bump patch version for everything. Follow the project's established convention.

## Breaking Change Examples

### API Signature Change

```
feat(users)!: add required email parameter to create()

Add email as required parameter to UserService.create() to ensure
all users have valid contact information.

BREAKING CHANGE: UserService.create() now requires email as second
parameter. Update calls from create(name) to create(name, email).

Migration:
  // Before
  userService.create('John Doe')

  // After
  userService.create('John Doe', 'john@example.com')
```

### Removed Functionality

```
refactor(api)!: remove deprecated /v1 endpoints

Remove legacy API v1 endpoints that have been deprecated since 2023.
All functionality is available in v2 with improved performance.

BREAKING CHANGE: /v1/* endpoints removed. Migrate to /v2/* endpoints.
See migration guide at docs/v2-migration.md for mappings.

Migration examples:
  /v1/users → /v2/users
  /v1/posts/{id} → /v2/posts/{id}
```

### Behavior Change

```
fix(auth)!: enforce rate limiting on auth endpoints

Add rate limiting to prevent brute force attacks. Requests exceeding
5 attempts per minute now return 429 Too Many Requests.

BREAKING CHANGE: Authentication endpoints now rate-limited to 5
requests per minute per IP. Clients must implement exponential
backoff when receiving 429 status codes. Update error handling to
retry with delays: 1s, 2s, 4s, 8s.
```

### Configuration Change

```
feat(config)!: migrate to YAML configuration format

Switch from JSON to YAML for configuration to support comments and
improve readability. JSON configuration is no longer supported.

BREAKING CHANGE: Configuration format changed from JSON to YAML.
Rename config.json to config.yaml and convert format:

  // config.json (old)
  {"port": 3000, "host": "localhost"}

  # config.yaml (new)
  port: 3000
  host: localhost

Run `npm run migrate-config` to automate conversion.
```

### Dependency Upgrade

```
build(deps)!: upgrade to React 18

Upgrade React from 17 to 18 for improved concurrent rendering.
Required to use new React features and security patches.

BREAKING CHANGE: React 18 required. Minimum peer dependency is now
react@^18.0.0. Update package.json dependencies and test for render
behavior changes. See React 18 migration guide: https://react.dev/blog/2022/03/08/react-18-upgrade-guide
```

### Return Type Change

```
refactor(api)!: make user fetch operations async

Convert UserService methods to async to support database migrations.
All user operations now return Promises.

BREAKING CHANGE: UserService methods now return Promises. Update all
calls to use async/await or .then():

  // Before
  const user = userService.getUser(id)

  // After
  const user = await userService.getUser(id)
  // or
  userService.getUser(id).then(user => { ... })
```

### Default Value Change

```
feat(api)!: change default pagination limit to 20

Reduce default page size from 100 to 20 to improve performance for
most common use cases. Large pages caused timeouts for some queries.

BREAKING CHANGE: Default pagination limit changed from 100 to 20.
Explicitly set limit=100 in requests if you need larger pages:
/api/users?limit=100
```

## Changelog Impact

Breaking changes should prominently appear in changelogs:

```markdown
## [2.0.0] - 2024-01-15

### BREAKING CHANGES

- **api**: UserService.create() now requires email parameter
- **auth**: Session tokens now expire after 1 hour instead of 24 hours
- **config**: Configuration format changed from JSON to YAML

### Features

- Add OAuth2 authentication support
- Implement token refresh mechanism

### Bug Fixes

- Prevent race condition in event handlers
```

The `BREAKING CHANGES` section should list all breaking changes prominently at the top of the version's changelog entry.

## Review Checklist

Before committing a breaking change:

- [ ] Subject line includes `!` after type/scope
- [ ] `BREAKING CHANGE:` footer present
- [ ] Footer explains what changed
- [ ] Footer explains why it changed
- [ ] Migration steps provided
- [ ] Examples show before/after code
- [ ] Relevant to current project phase (not prerelease exception)
- [ ] Documentation updated
- [ ] Changelog entry planned
- [ ] Version bump planned (major or minor for 0.x)

## Communication

Breaking changes need broader communication:

1. **Commit message**: Complete documentation (above)
2. **Changelog**: Prominent BREAKING CHANGES section
3. **Release notes**: Highlight breaking changes
4. **Migration guide**: Detailed steps if complex
5. **Deprecation warnings**: Add before breaking change if possible
6. **Announcement**: Email, blog post, or discussion for major breaks

For significant breaking changes, consider:
- Advance notice (deprecation warnings in prior release)
- Migration tooling (codemods, scripts)
- Support for old behavior (temporary compatibility mode)
- Extended support for previous major version

## Summary

Effective breaking change documentation requires:

1. **Clear notation**: Both `!` and `BREAKING CHANGE:` footer
2. **Complete description**: What changed, why, and how to migrate
3. **Examples**: Before and after code
4. **Context**: Version impact and timeline
5. **Communication**: Beyond commit message to users

Breaking changes are user-facing. Take extra care to make them crystal clear and provide smooth migration paths.
