# Exemples de Commits

Collection d'exemples de commits suivant les **Conventional Commits**.

## Format de Base

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

---

## Exemples par Type

### 1. `feat` — Nouvelles Fonctionnalités

#### Simple
```
feat(auth): add OAuth2 login support
```

#### Avec scope et détails
```
feat(api): add user search endpoint
```

#### Avec body
```
feat(chat): add message reactions

Users can now react to messages with emoji reactions.
Includes reaction counter and user list on hover.

https://claude.ai/code/session_01PgdZKtpoXwTQw8WZzWKTU8
```

#### Avec breaking change
```
feat(api)!: change user response format

BREAKING CHANGE: User API now returns { data: User[], meta: {} }
instead of User[] directly. Update all API calls accordingly.

Migration: response.data instead of response

https://claude.ai/code/session_01PgdZKtpoXwTQw8WZzWKTU8
```

### 2. `fix` — Corrections de Bugs

#### Simple
```
fix(button): correct hover color
```

#### Avec contexte
```
fix(api): handle null response in user endpoint

Add defensive null checks to prevent crashes when
user data is not found.
```

#### Avec issue reference
```
fix(auth): resolve session timeout issue

Fixes #142
```

#### Critical fix
```
fix(security): patch XSS vulnerability in comment input

Sanitize user input to prevent script injection.

SECURITY: CVE-2024-12345
```

### 3. `docs` — Documentation

#### README update
```
docs(readme): update installation instructions
```

#### API documentation
```
docs(api): add examples for user endpoints

Include JavaScript and Python code examples for
all user-related API endpoints.
```

#### Comment improvements
```
docs(utils): add JSDoc comments to date helpers
```

### 4. `style` — Formatage

#### Code formatting
```
style(components): fix indentation in Button.tsx
```

#### Linting
```
style(all): run prettier on codebase
```

#### CSS/UI styling
```
style(navbar): adjust spacing and colors
```

### 5. `refactor` — Refactoring

#### Extract function
```
refactor(auth): extract token validation logic
```

#### Reorganize code
```
refactor(api): split large UserService into modules

- UserService: core user operations
- UserValidator: validation logic
- UserTransformer: response formatting
```

#### Simplify logic
```
refactor(utils): simplify date parsing function

Replace complex regex with date-fns library.
Improves readability and maintainability.
```

### 6. `perf` — Performance

#### Optimization
```
perf(db): add index on user_id column

Reduces query time from 800ms to 50ms for user lookups.
```

#### Caching
```
perf(api): add Redis caching for user list

Cache expires after 5 minutes.
Reduces database load by 70%.
```

#### Lazy loading
```
perf(images): implement lazy loading for gallery
```

### 7. `test` — Tests

#### Add tests
```
test(auth): add unit tests for login flow
```

#### Fix tests
```
test(api): fix flaky user endpoint test
```

#### Increase coverage
```
test(services): increase coverage to 90%

Add tests for edge cases:
- Empty inputs
- Null values
- Large datasets
```

### 8. `build` — Build System

#### Dependencies
```
build(deps): upgrade React to v19
```

#### Build configuration
```
build(webpack): optimize production bundle size

- Enable tree shaking
- Minify output
- Remove source maps in production
```

#### Package updates
```
build(deps): update security dependencies

- express@4.18.2 → 4.19.2 (security patch)
- axios@1.5.0 → 1.6.5 (vulnerability fix)
```

### 9. `ci` — CI/CD

#### GitHub Actions
```
ci(github): add automated test workflow
```

#### Deploy configuration
```
ci(deploy): add production deployment pipeline

Automatically deploy to production on main branch merge.
Includes health checks and rollback capability.
```

#### Test automation
```
ci(tests): run tests on all pull requests
```

### 10. `chore` — Maintenance

#### General maintenance
```
chore(deps): update development dependencies
```

#### Configuration
```
chore(config): update ESLint rules
```

#### Cleanup
```
chore(cleanup): remove unused imports and variables
```

### 11. `revert` — Reverts

#### Simple revert
```
revert: feat(auth): add OAuth2 login

This reverts commit a1b2c3d4.
```

#### Revert with reason
```
revert: feat(api): add pagination

This reverts commit a1b2c3d4.

Pagination causing performance issues in production.
Will re-implement with different approach.
```

---

## Exemples par Scope

### Frontend (`ui`, `components`, `pages`)
```
feat(ui): add dark mode toggle
fix(components): resolve Button alignment issue
style(pages): update homepage layout
```

### Backend (`api`, `db`, `server`)
```
feat(api): add user pagination endpoint
fix(db): resolve connection pool leak
perf(server): optimize request handling
```

### Authentication (`auth`, `security`)
```
feat(auth): add two-factor authentication
fix(security): patch SQL injection vulnerability
```

### Skills (pour ce repo)
```
feat(skills): add git-commit-pr skill
docs(skills): update build-chatwindow README
fix(skills): correct MCP config validation
```

---

## Exemples avec Body Complet

### Feature avec contexte
```
feat(chat): add file upload to messages

Users can now upload files (images, PDFs, documents)
directly in chat messages. Files are stored in Supabase
Storage and displayed with preview thumbnails.

Supported formats:
- Images: JPEG, PNG, WebP, GIF
- Documents: PDF, DOCX, TXT
- Maximum size: 10MB per file

https://claude.ai/code/session_01PgdZKtpoXwTQw8WZzWKTU8
```

### Fix avec diagnostic
```
fix(api): resolve race condition in user update

User updates were occasionally lost due to concurrent
modifications. Implemented optimistic locking with
version field to prevent lost updates.

Before: 5% failure rate under load
After: 0% failures in stress tests

Fixes #234

https://claude.ai/code/session_01PgdZKtpoXwTQw8WZzWKTU8
```

### Refactor avec justification
```
refactor(services): migrate from REST to GraphQL

Migrated user and post services to GraphQL for:
- Better client-side data fetching control
- Reduced over-fetching (smaller payloads)
- Type safety with generated types
- Single endpoint for all queries

REST endpoints remain for backward compatibility
and will be deprecated in v3.0.

https://claude.ai/code/session_01PgdZKtpoXwTQw8WZzWKTU8
```

---

## Exemples Multi-Scopes

### Multiple scopes
```
feat(api,ui): add user avatar upload

Backend:
- New POST /api/users/:id/avatar endpoint
- Image validation and optimization
- Storage in Supabase

Frontend:
- Avatar upload modal
- Preview before upload
- Cropping tool integration

https://claude.ai/code/session_01PgdZKtpoXwTQw8WZzWKTU8
```

---

## Breaking Changes

### Format
```
<type>(<scope>)!: <description>

BREAKING CHANGE: <explication détaillée>

<migration guide optionnel>
```

### Exemple complet
```
feat(api)!: migrate to v2 authentication

BREAKING CHANGE: Authentication now requires JWT tokens
in Authorization header instead of session cookies.

Migration Guide:
1. Update client to use JWT tokens:
   - Obtain token: POST /api/v2/auth/login
   - Include in requests: Authorization: Bearer <token>

2. Remove session cookie handling:
   - No longer need withCredentials: true
   - No CORS credentials needed

3. Update token refresh logic:
   - Use refresh token endpoint: POST /api/v2/auth/refresh
   - Store refresh token securely

Old session-based auth will be removed in v3.0 (March 2026).

https://claude.ai/code/session_01PgdZKtpoXwTQw8WZzWKTU8
```

---

## Footers

### Issue references
```
feat(search): add fuzzy search

Implements fuzzy matching for better search results.

Fixes #123
Refs #124, #125
```

### Breaking changes
```
feat(db)!: migrate to PostgreSQL 15

BREAKING CHANGE: Requires PostgreSQL 15+.
Migration script provided in /scripts/migrate-pg15.sql
```

### Multiple footers
```
feat(auth): add SAML SSO

Implements SAML 2.0 authentication for enterprise users.

Fixes #234
Refs #235
Reviewed-by: @tech-lead
```

---

## Anti-Patterns (À Éviter)

### ❌ Messages vagues
```
fix: bug fix
update: changes
WIP
Fixed stuff
```

### ❌ Messages trop longs
```
feat: this commit adds a new user authentication system with OAuth2 and also updates the database schema and refactors some components
```
👉 **Solution** : Découper en plusieurs commits atomiques

### ❌ Pas de type
```
add login page
fixed the bug
updated readme
```

### ❌ Description au passé
```
feat(auth): added OAuth2 login
fix(api): fixed null response
```
👉 **Solution** : Utiliser l'impératif ("add", "fix")

### ❌ Point final
```
feat(auth): add OAuth2 login.
```
👉 **Solution** : Pas de point final

---

## Commits Spéciaux

### Initial commit
```
chore: initial commit

Project scaffolding with:
- Next.js 14 setup
- TypeScript configuration
- ESLint and Prettier
- Basic project structure
```

### Merge commit (auto-généré)
```
Merge pull request #123 from user/feature-branch

feat(auth): add OAuth2 login
```

### Version bump
```
chore(release): bump version to 2.0.0

See CHANGELOG.md for full release notes.
```

### Hotfix
```
fix(critical): patch production authentication bug

Emergency fix for login failure affecting all users.
Deployed directly to production.

Incident: INC-2024-001
```

---

## Checklist pour un Bon Commit

- [ ] Type approprié (feat, fix, docs, etc.)
- [ ] Scope descriptif (si applicable)
- [ ] Description concise (<72 caractères)
- [ ] Impératif présent ("add" pas "added")
- [ ] Pas de point final
- [ ] Body explique le POURQUOI (si nécessaire)
- [ ] Footer avec références (Fixes #X, si applicable)
- [ ] Breaking change marqué (! et BREAKING CHANGE:)
- [ ] Session URL Claude incluse (si applicable)
- [ ] Commit atomique (1 changement logique)
- [ ] Pas de fichiers sensibles (.env, credentials)

---

## Ressources

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Angular Commit Guidelines](https://github.com/angular/angular/blob/main/CONTRIBUTING.md#commit)
- [Commitizen](https://github.com/commitizen/cz-cli) - CLI helper
- [Commitlint](https://commitlint.js.org/) - Linter pour commits
