# Pull Request Template

Template complet pour créer des Pull Requests bien documentées.

## Template Standard

```markdown
## Summary
- [Bullet point 1 : changement principal]
- [Bullet point 2 : changement principal]
- [Bullet point 3 : changement principal]

## Changes
### Added
- [Liste des nouvelles fonctionnalités ou fichiers ajoutés]
- [Exemple : New OAuth2 authentication service]

### Changed
- [Liste des modifications de fonctionnalités existantes]
- [Exemple : Updated user API to return paginated results]

### Fixed
- [Liste des corrections de bugs]
- [Exemple : Fixed null pointer exception in user endpoint]

### Removed (si applicable)
- [Liste des fonctionnalités ou fichiers supprimés]
- [Exemple : Removed deprecated v1 API endpoints]

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Refactoring (no functional changes)
- [ ] Performance improvement
- [ ] Code style/formatting
- [ ] CI/CD changes

## Testing
- [ ] [Test effectué 1]
- [ ] [Test effectué 2]
- [ ] All existing tests pass
- [ ] New tests added for new functionality
- [ ] Manual testing completed
- [ ] No console errors or warnings

## Screenshots (si applicable)
[Ajouter des screenshots ou GIFs pour les changements UI]

## Performance Impact (si applicable)
- [ ] No performance impact
- [ ] Performance improvement: [décrire]
- [ ] Potential performance impact: [décrire et justifier]

## Breaking Changes (si applicable)
**BREAKING CHANGE**: [Description du breaking change]

**Migration Guide**:
1. [Étape 1 pour migrer]
2. [Étape 2 pour migrer]

## Dependencies
- [ ] No new dependencies
- [ ] New dependencies added: [lister]
- [ ] Dependencies updated: [lister]

## Additional Notes
[Contexte supplémentaire, décisions architecturales, alternatives considérées, etc.]

## Related Issues
Fixes #[issue number]
Refs #[issue number]

[Session URL Claude Code]
```

---

## Exemples par Type

### 1. Feature PR

```markdown
## Summary
- Add user profile image upload functionality
- Support multiple image formats (JPEG, PNG, WebP)
- Include automatic image optimization

## Changes
### Added
- ImageUploadService for handling file uploads
- Image optimization using sharp library
- User profile API endpoint `/api/users/:id/avatar`
- Avatar display component in user profile

### Changed
- Updated User model to include avatar_url field
- Enhanced user profile page to display avatar

## Type of Change
- [x] New feature (non-breaking change which adds functionality)

## Testing
- [x] Unit tests for ImageUploadService
- [x] Integration tests for avatar upload endpoint
- [x] Tested with JPEG, PNG, WebP formats
- [x] Tested file size limits (max 5MB)
- [x] Manual testing on Chrome, Firefox, Safari
- [x] All existing tests pass
- [x] No console errors

## Screenshots
[Screenshot of user profile with avatar]
[Screenshot of upload modal]

## Dependencies
- [x] New dependencies added:
  - sharp@0.33.0 (image optimization)
  - multer@1.4.5-lts.1 (file upload handling)

## Additional Notes
- Images are automatically resized to 256x256px
- Original images stored in /uploads/avatars/original/
- Optimized versions stored in /uploads/avatars/optimized/
- Maximum file size: 5MB

https://claude.ai/code/session_01PgdZKtpoXwTQw8WZzWKTU8
```

### 2. Bug Fix PR

```markdown
## Summary
- Fix null pointer exception in user endpoint
- Add defensive null checks for optional fields
- Improve error handling and logging

## Changes
### Fixed
- Null handling in `/api/users/:id` endpoint
- Missing validation for empty user queries
- Error message clarity for invalid user IDs

### Changed
- Enhanced error logging with stack traces
- Updated API response format for errors

## Type of Change
- [x] Bug fix (non-breaking change which fixes an issue)

## Testing
- [x] Added regression test for null user scenario
- [x] Tested with valid and invalid user IDs
- [x] Tested with empty database
- [x] All existing tests pass
- [x] No console errors

## Related Issues
Fixes #142

https://claude.ai/code/session_01PgdZKtpoXwTQw8WZzWKTU8
```

### 3. Breaking Change PR

```markdown
## Summary
- Migrate user API to v2 format with pagination
- Improve performance for large user lists
- Add filtering and sorting capabilities

## Changes
### Added
- Pagination support (page, limit parameters)
- Filtering by role, status
- Sorting by createdAt, name, email
- Meta information in responses (total, page, pageSize)

### Changed
- **BREAKING**: `/api/users` now returns `{ data: User[], meta: {} }` instead of `User[]`
- Response format now includes pagination metadata

### Removed
- Deprecated `/api/v1/users` endpoint (use `/api/v2/users`)

## Type of Change
- [x] Breaking change (fix or feature that would cause existing functionality to not work as expected)

## Breaking Changes
**BREAKING CHANGE**: User API response format has changed.

**Migration Guide**:
1. Update all calls to `/api/users` to handle new response format:
   ```javascript
   // Before
   const users = await fetch('/api/users').then(r => r.json());

   // After
   const response = await fetch('/api/users').then(r => r.json());
   const users = response.data;
   const total = response.meta.total;
   ```

2. Optional: Migrate to v2 endpoint explicitly for clarity:
   ```javascript
   const response = await fetch('/api/v2/users').then(r => r.json());
   ```

3. Update TypeScript types:
   ```typescript
   interface UserListResponse {
     data: User[];
     meta: {
       total: number;
       page: number;
       pageSize: number;
     };
   }
   ```

## Testing
- [x] All existing tests updated for new format
- [x] New tests for pagination
- [x] New tests for filtering and sorting
- [x] Performance tests with 10k+ users
- [x] Backward compatibility tests (v1 endpoint still works)
- [x] All tests pass
- [x] No console errors

## Performance Impact
- [x] Performance improvement:
  - Response time reduced from ~800ms to ~150ms for 1000+ users
  - Database queries optimized with pagination
  - Memory usage reduced by 60%

## Dependencies
- [ ] No new dependencies

## Additional Notes
- v1 API will be deprecated in 3 months (April 2026)
- Documentation updated in `/docs/api/users.md`
- Migration script available in `/scripts/migrate-user-api.js`

## Related Issues
Refs #156, #178, #201

https://claude.ai/code/session_01PgdZKtpoXwTQw8WZzWKTU8
```

### 4. Documentation PR

```markdown
## Summary
- Add comprehensive API documentation
- Include code examples for all endpoints
- Add troubleshooting guide

## Changes
### Added
- API reference documentation (`/docs/api/`)
- Code examples in JavaScript, Python, cURL
- Troubleshooting guide (`/docs/troubleshooting.md`)
- Architecture diagrams

### Changed
- Updated README with better getting started guide
- Improved installation instructions

## Type of Change
- [x] Documentation update

## Testing
- [x] All code examples tested and working
- [x] Links verified (no 404s)
- [x] Markdown renders correctly
- [x] Diagrams display properly

https://claude.ai/code/session_01PgdZKtpoXwTQw8WZzWKTU8
```

### 5. Refactoring PR

```markdown
## Summary
- Refactor authentication service for better maintainability
- Extract common logic into reusable utilities
- Improve code organization and readability

## Changes
### Changed
- Split AuthService into smaller, focused modules
- Extracted token validation logic to TokenValidator
- Improved error handling with custom error classes
- Reorganized file structure in `/src/auth/`

### Added
- Unit tests for new modules
- JSDoc comments for all public methods

## Type of Change
- [x] Refactoring (no functional changes)

## Testing
- [x] All existing tests still pass
- [x] New unit tests for extracted modules
- [x] Integration tests verify same behavior
- [x] No regressions detected
- [x] Code coverage maintained at 85%+

## Performance Impact
- [ ] No performance impact (same functionality, better code organization)

## Additional Notes
- No breaking changes
- All public APIs remain unchanged
- Improved code readability and maintainability
- Easier to add new authentication providers

https://claude.ai/code/session_01PgdZKtpoXwTQw8WZzWKTU8
```

---

## Conseils pour une PR de Qualité

### Summary
- **3 bullet points maximum** : Concis et impactant
- Focus sur le **quoi**, pas le **comment**
- Utiliser un langage clair et non technique si possible

### Changes
- **Séparer par type** : Added, Changed, Fixed, Removed
- **Être spécifique** : Nommer les fichiers/fonctionnalités clés
- **Rester concis** : 1 ligne par changement

### Type of Change
- **Cocher toutes les cases applicables**
- La majorité des PRs ont 1-2 types principalement

### Testing
- **Lister tous les tests effectués**
- Inclure tests unitaires, intégration, manuels
- Mentionner les navigateurs/environnements testés

### Screenshots
- **Obligatoire pour changements UI**
- Avant/Après pour les modifications
- GIFs pour interactions complexes

### Breaking Changes
- **Toujours inclure un migration guide**
- Expliquer clairement l'impact
- Fournir des exemples de code avant/après

### Additional Notes
- **Contexte architectural** : Pourquoi ce choix ?
- **Alternatives considérées** : Qu'avez-vous rejeté et pourquoi ?
- **Limitations connues** : Y a-t-il des compromis ?
- **Prochaines étapes** : Quoi d'autre à faire ?

---

## Template Minimal (pour petites PRs)

Pour des PRs très simples (typos, petites corrections) :

```markdown
## Summary
- [Description courte du changement]

## Type of Change
- [x] [Type]

## Testing
- [x] Vérifié manuellement

[Session URL]
```

**Exemple** :
```markdown
## Summary
- Fix typo in README installation section

## Type of Change
- [x] Documentation update

## Testing
- [x] Markdown renders correctly

https://claude.ai/code/session_01PgdZKtpoXwTQw8WZzWKTU8
```
