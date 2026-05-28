# Workflow: Understand Feature

**Purpose**: Deep dive into specific feature implementation
**Use for**: Extending features, debugging, understanding functionality, evaluating modification vs new code
**Estimated time**: 45-90 minutes (depending on feature complexity)
**Output**: Feature documentation with extension recommendations

## Overview

This workflow provides a systematic approach to deeply understanding how a specific feature is implemented. Use this when you need to extend an existing feature, debug its behavior, or decide whether to modify existing code or create new code.

## Required Tools

- **Read** - Reading feature source code
- **Grep** - Finding related code and usages
- **Glob** - Finding feature-related files
- **Bash** - Directory analysis (optional)

## Feature Analysis Process

### Phase 1: Feature Identification

#### 1.1 Define Feature Scope

Clearly identify what feature you're analyzing:

```markdown
Questions to answer:
1. What is the feature name/description?
2. What user-facing functionality does it provide?
3. What is the scope (single module or cross-cutting)?
4. Why are you analyzing this feature?
```

**Document**:
```markdown
### Feature: User Profile Management

**Description**: Allows users to create, view, update, and delete their profiles including avatar upload, bio, and preferences.

**User-facing functionality**:
- View profile page
- Edit profile information
- Upload profile picture
- Set privacy preferences
- Delete account

**Scope**: Primary in `users` module, touches `auth` and `storage` modules

**Analysis purpose**: Planning to add social links feature, need to understand current implementation to extend properly
```

#### 1.2 Locate Feature Files

Find all files related to the feature:

```markdown
Search strategy:
1. Search by feature name/domain terms
2. Use multiple search terms (synonyms)
3. Search across all file types
```

**Example searches**:
```bash
# Primary search terms
Grep: "profile" -i (output_mode: files_with_matches)
Grep: "UserProfile|user_profile" (output_mode: files_with_matches)

# Related terms
Grep: "avatar|bio|preferences" -i (output_mode: files_with_matches)

# Find files by pattern
Glob: "**/profile*.ts"
Glob: "**/user-profile*"
```

**Document**:
```markdown
### Feature Files Located

**Core files**:
- `src/users/user-profile.service.ts` - Business logic
- `src/users/user-profile.repository.ts` - Data access
- `src/users/user-profile.controller.ts` - API endpoints
- `src/models/user-profile.model.ts` - Data model
- `src/dto/update-profile.dto.ts` - Request validation

**Frontend files**:
- `src/components/ProfilePage.tsx` - Profile view
- `src/components/EditProfileForm.tsx` - Profile editing
- `src/components/AvatarUpload.tsx` - Image upload

**Tests**:
- `tests/unit/user-profile.service.test.ts`
- `tests/integration/profile-api.test.ts`
- `tests/e2e/profile-flow.test.ts`

**Database**:
- `migrations/2023-05-create-user-profiles.sql`
```

### Phase 2: Data Flow Analysis

#### 2.1 Map Data Models

Understand the data structures:

```markdown
Search strategy:
1. Read model/entity files
2. Identify fields and types
3. Map relationships to other models
4. Understand validation rules
```

**Example workflow**:
```bash
# Read model definition
Read: src/models/user-profile.model.ts

# Find related models
Grep: "User|Avatar|Preference" (path: src/models/, output_mode: content)

# Find validation
Grep: "@IsString|@IsEmail|validate" (path: src/dto/, output_mode: content)

# Read DTOs
Read: src/dto/update-profile.dto.ts
Read: src/dto/create-profile.dto.ts
```

**Document**:
```markdown
### Data Model: UserProfile

```typescript
// From src/models/user-profile.model.ts
@Entity('user_profiles')
export class UserProfile {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @OneToOne(() => User)
  @JoinColumn({ name: 'user_id' })
  user: User;

  @Column({ nullable: true })
  displayName: string;

  @Column({ type: 'text', nullable: true })
  bio: string;

  @Column({ nullable: true })
  avatarUrl: string;

  @Column({ type: 'jsonb', default: {} })
  preferences: Record<string, any>;

  @Column({ default: 'public' })
  visibility: 'public' | 'private' | 'friends';

  @CreateDateColumn()
  createdAt: Date;

  @UpdateDateColumn()
  updatedAt: Date;
}
```

**Relationships**:
- One-to-One with User (user_id foreign key)
- References Avatar via avatarUrl (URL to storage service)

**Validation** (from UpdateProfileDto):
- displayName: Optional string, 1-100 characters
- bio: Optional string, max 500 characters
- avatarUrl: Optional valid URL
- preferences: Optional JSON object
- visibility: Enum ['public', 'private', 'friends']

**Database constraints**:
- user_id must be unique (enforced at DB level)
- Cascade delete when User is deleted
```

#### 2.2 Trace Data Flows

Map how data moves through the system:

```markdown
Search strategy:
1. Find entry points (API endpoints, UI forms)
2. Trace through layers (controller → service → repository)
3. Identify transformations and validations
4. Map database operations
```

**Example workflow**:
```bash
# Read controller
Read: src/users/user-profile.controller.ts

# Read service
Read: src/users/user-profile.service.ts

# Read repository
Read: src/users/user-profile.repository.ts

# Find validation middleware
Grep: "ValidationPipe|validate" (path: src/users/, output_mode: content)
```

**Document**:
```markdown
### Data Flow: Update Profile

**1. API Request**
```
PATCH /api/v1/users/:id/profile
Body: { displayName: "John", bio: "Developer" }
Headers: Authorization: Bearer <token>
```

**2. Controller Layer** (`user-profile.controller.ts`)
```typescript
@Patch(':id/profile')
@UseGuards(AuthGuard)
async updateProfile(
  @Param('id') userId: string,
  @Body() updateDto: UpdateProfileDto,
  @CurrentUser() user: User
) {
  // Authorization check
  if (userId !== user.id) throw new ForbiddenException();

  // Delegate to service
  return await this.profileService.update(userId, updateDto);
}
```
- **Validates**: JWT token (AuthGuard)
- **Validates**: Request body against UpdateProfileDto
- **Validates**: User can only update own profile

**3. Service Layer** (`user-profile.service.ts`)
```typescript
async update(userId: string, data: UpdateProfileDto): Promise<UserProfile> {
  // Check profile exists
  const profile = await this.profileRepository.findByUserId(userId);
  if (!profile) throw new NotFoundException();

  // If avatar changed, handle upload
  if (data.avatarUrl) {
    await this.storageService.validateImage(data.avatarUrl);
  }

  // Update profile
  const updated = await this.profileRepository.update(profile.id, data);

  // Emit event for other services
  await this.eventEmitter.emit('profile.updated', updated);

  return updated;
}
```
- **Business logic**: Existence check, avatar validation, event emission
- **Dependencies**: ProfileRepository, StorageService, EventEmitter

**4. Repository Layer** (`user-profile.repository.ts`)
```typescript
async update(id: string, data: Partial<UserProfile>): Promise<UserProfile> {
  await this.db.userProfile.update({
    where: { id },
    data: {
      ...data,
      updatedAt: new Date()
    }
  });

  return await this.findById(id);
}
```
- **Database operation**: UPDATE user_profiles SET ... WHERE id = ?
- **Returns**: Updated profile

**5. Response**
```json
{
  "id": "uuid",
  "userId": "uuid",
  "displayName": "John",
  "bio": "Developer",
  "avatarUrl": "https://...",
  "preferences": {},
  "visibility": "public",
  "createdAt": "2023-...",
  "updatedAt": "2023-..."
}
```

**Side Effects**:
- Event emitted: `profile.updated` (consumed by notification service)
- Cache invalidated: User profile cache
```

#### 2.3 Identify Data Transformations

Understand how data is transformed:

```markdown
Transformations to identify:
1. DTO validation (input sanitization)
2. Entity mapping (DB ↔ domain objects)
3. Response serialization (hiding sensitive fields)
4. Data enrichment (adding computed fields)
```

**Document transformations with code examples**

### Phase 3: Business Logic Analysis

#### 3.1 Map Business Rules

Understand the business rules enforced:

```markdown
Search strategy:
1. Read service layer code
2. Find validation checks
3. Identify business constraints
4. Look for error conditions
```

**Example workflow**:
```bash
# Read service implementation
Read: src/users/user-profile.service.ts

# Find validation logic
Grep: "if.*throw|validate|check" (path: src/users/, output_mode: content)

# Find constants/config
Grep: "MAX_|MIN_|ALLOWED_" (output_mode: content)
```

**Document**:
```markdown
### Business Rules

**Profile Creation**:
1. Profile automatically created when User signs up
2. Initial values from User.email and User.name
3. Default visibility is "public"

**Profile Updates**:
1. Users can only update their own profile
2. displayName must be unique (soft constraint - warning only)
3. Avatar must be valid image (checked by StorageService)
4. Bio limited to 500 characters
5. Preferences must be valid JSON object

**Profile Deletion**:
1. Cannot delete profile independently - deleted with User
2. Cascade delete removes avatar from storage
3. Soft delete option via visibility="deleted"

**Privacy Rules**:
- visibility="public": Anyone can view
- visibility="private": Only user can view
- visibility="friends": Only friends can view (requires Friend relationship)

**Avatar Upload**:
1. Max file size: 5MB
2. Allowed types: JPEG, PNG, GIF
3. Auto-resize to 400x400
4. Stored in cloud storage, URL saved in profile
```

#### 3.2 Identify Dependencies

Map what other services/modules this feature depends on:

```markdown
Search strategy:
1. Analyze service constructor (DI)
2. Find service method calls
3. Identify external API calls
4. Map database dependencies
```

**Example workflow**:
```bash
# Find constructor dependencies
Grep: "constructor\\(" (path: src/users/user-profile.service.ts, output_mode: content)

# Find method calls to other services
Grep: "this.\\w+Service\\." (path: src/users/user-profile.service.ts, output_mode: content)
```

**Document**:
```markdown
### Feature Dependencies

**Direct dependencies** (injected services):
- `UserProfileRepository` - Data access
- `StorageService` - Avatar upload/deletion
- `EventEmitter` - Event publishing
- `CacheService` - Profile caching
- `AuthService` - Permission checking

**Indirect dependencies**:
- `User` model - Profile belongs to User
- `Friend` model - For friends-only visibility
- `NotificationService` - Consumes profile.updated events
- Cloud storage (S3/GCS) - Via StorageService

**Database dependencies**:
- `users` table - Foreign key relationship
- `user_profiles` table - Primary table

**External APIs**:
- None (avatar storage via internal StorageService)
```

#### 3.3 Identify Consumers

Find what depends on this feature:

```markdown
Search strategy:
1. Search for imports of feature modules
2. Search for API endpoint usage (frontend)
3. Find event listeners
```

**Example workflow**:
```bash
# Find imports
Grep: "import.*UserProfile|from.*user-profile" (output_mode: files_with_matches)

# Find API calls (frontend)
Grep: "'/api.*profile|fetch.*profile" (path: src/components/, output_mode: content)

# Find event listeners
Grep: "profile.updated|profile.created" (output_mode: files_with_matches)
```

**Document**:
```markdown
### Feature Consumers

**Backend consumers**:
- `NotificationService` - Listens to profile.updated events
- `SearchService` - Indexes public profiles
- `RecommendationService` - Uses profile data for recommendations

**Frontend consumers**:
- `ProfilePage` component - Displays profile
- `EditProfileForm` component - Edits profile
- `UserCard` component - Shows profile summary
- `SettingsPage` component - Manages privacy settings

**External consumers**:
- Public API - GET /api/public/profiles/:username
- Webhooks - profile.updated events sent to integrations
```

### Phase 4: Extension Opportunity Analysis

#### 4.1 Identify Extension Points

Look for designed extension points:

```markdown
Extension points to find:
1. Plugin/hook systems
2. Event emitters
3. Abstract classes/interfaces
4. Configuration injection points
```

**Example workflow**:
```bash
# Find hooks/events
Grep: "emit|hook|plugin|extend" (path: src/users/, output_mode: content)

# Find interfaces
Grep: "interface.*Profile|abstract class" (output_mode: content)

# Read for extension patterns
Read: src/users/user-profile.service.ts
```

**Document**:
```markdown
### Extension Points

**Event System**:
```typescript
// Events emitted by ProfileService
this.eventEmitter.emit('profile.created', profile);
this.eventEmitter.emit('profile.updated', { old, new });
this.eventEmitter.emit('profile.deleted', profile);
```
- **Extension opportunity**: Listen to events for custom logic

**Plugin System**:
```typescript
// ProfileService accepts optional plugins
constructor(
  private repository: UserProfileRepository,
  @Optional() private plugins: ProfilePlugin[] = []
) {}

// Plugins can hook into lifecycle
async update(data) {
  await this.runPlugins('beforeUpdate', data);
  const result = await this.repository.update(data);
  await this.runPlugins('afterUpdate', result);
  return result;
}
```
- **Extension opportunity**: Create ProfilePlugin implementations

**Configuration**:
```typescript
// Feature flags
if (config.features.profileSocialLinks) {
  // Social links feature
}
```
- **Extension opportunity**: Feature flags for gradual rollout
```

#### 4.2 Evaluate: Extend vs New Code

Assess whether to modify existing code or create new:

```markdown
Analysis framework:
1. Single Responsibility Principle check
2. Complexity assessment
3. Testing impact
4. Risk assessment
```

**Document**:
```markdown
### Extend vs New Code Analysis

**Planned change**: Add social links (Twitter, GitHub, LinkedIn) to profile

#### Option 1: Extend UserProfile Model

**Approach**:
```typescript
// Add to UserProfile model
@Column({ type: 'jsonb', nullable: true })
socialLinks: {
  twitter?: string;
  github?: string;
  linkedin?: string;
}
```

**Pros**:
- Minimal code changes
- Reuses existing validation/storage logic
- Natural fit in profile data structure

**Cons**:
- Increases UserProfile model complexity
- No specialized validation for social URLs
- Limited flexibility for future social networks

**SRP Assessment**: ✓ OK - Social links are profile data
**Risk**: Low
**Testing impact**: Add tests to existing suite

#### Option 2: Create SocialLinks Module

**Approach**:
```typescript
// New model
@Entity('user_social_links')
export class UserSocialLinks {
  @OneToOne(() => UserProfile)
  profile: UserProfile;

  @Column({ nullable: true })
  @IsUrl()
  twitter: string;

  // ...
}
```

**Pros**:
- Separation of concerns
- Specialized validation logic
- Easy to extend with new networks
- Independent testing

**Cons**:
- More code/complexity
- Additional database table
- More API endpoints
- Overkill for simple feature

**SRP Assessment**: May violate YAGNI (You Aren't Gonna Need It)
**Risk**: Low
**Testing impact**: New test suite needed

#### Recommendation

**Extend UserProfile model** (Option 1)

**Rationale**:
1. Social links are inherently profile data
2. Low complexity addition
3. Minimal testing impact
4. Can refactor later if needed
5. Existing plugin system allows custom validation

**Implementation approach**:
1. Add `socialLinks` field to UserProfile model
2. Create SocialLinksDto for validation
3. Add URL validation via class-validator
4. Create ProfileSocialLinksPlugin for custom logic
5. Update frontend forms
6. Add tests to existing suite

**Migration path if complexity grows**:
- Events already emitted, easy to extend
- Can extract to module later without API changes
- Use feature flag for gradual rollout
```

### Phase 5: Testing & Quality Analysis

#### 5.1 Analyze Existing Tests

Understand test coverage and patterns:

```markdown
Search strategy:
1. Find test files
2. Read test structure
3. Identify test patterns (AAA, mocking, fixtures)
4. Assess coverage
```

**Example workflow**:
```bash
# Find tests
Glob: "**/*profile*.test.ts"
Glob: "**/test_*profile*.py"

# Read test files
Read: tests/unit/user-profile.service.test.ts
Read: tests/integration/profile-api.test.ts
```

**Document**:
```markdown
### Testing Analysis

**Test coverage**:
- Unit tests: user-profile.service.test.ts (24 tests, 95% coverage)
- Integration tests: profile-api.test.ts (12 tests, all endpoints)
- E2E tests: profile-flow.test.ts (5 user flows)

**Test patterns**:
- Arrange-Act-Assert (AAA) pattern
- Jest for unit/integration tests
- Cypress for E2E tests
- Repository/services mocked in unit tests
- Real database in integration tests

**Example test structure**:
```typescript
describe('UserProfileService', () => {
  describe('update', () => {
    it('should update profile successfully', async () => {
      // Arrange
      const mockProfile = { id: '1', userId: 'user1' };
      const updateData = { displayName: 'New Name' };
      mockRepository.findByUserId.mockResolvedValue(mockProfile);
      mockRepository.update.mockResolvedValue({ ...mockProfile, ...updateData });

      // Act
      const result = await service.update('user1', updateData);

      // Assert
      expect(result.displayName).toBe('New Name');
      expect(mockRepository.update).toHaveBeenCalledWith('1', updateData);
    });
  });
});
```

**Testing gaps**:
- No tests for avatar upload failure scenarios
- Limited tests for privacy settings
- No performance tests for large profiles
```

#### 5.2 Identify Quality Standards

Understand quality requirements:

```markdown
Standards to identify:
1. Code style (linting rules)
2. Documentation requirements
3. Performance expectations
4. Security considerations
```

**Document quality standards found in feature**

### Phase 6: Documentation

#### 6.1 Create Feature Documentation

Compile comprehensive feature documentation:

```markdown
Template:
1. Feature overview
2. Data models and flows
3. Business rules
4. Dependencies and consumers
5. Extension points
6. Testing approach
7. Known issues and limitations
8. Extension recommendations
```

## Output Format

Create comprehensive feature documentation:

```markdown
# Feature Documentation: {Feature Name}

**Date**: {YYYY-MM-DD}
**Analyst**: {your-name}
**Version**: {feature-version-if-applicable}

## Feature Overview

{Description of what the feature does}

**User-facing functionality**:
- {capability 1}
- {capability 2}

**Scope**: {modules involved}

## Data Models

### {ModelName}

{Model definition with fields, types, constraints}

**Relationships**: {related models}
**Validation**: {validation rules}

## Data Flows

### {Flow Name} (e.g., Create Profile, Update Profile)

{Step-by-step data flow from entry point to database}

**Entry point**: {API endpoint or UI action}
**Layers**: {controller → service → repository → database}
**Transformations**: {data transformations applied}
**Side effects**: {events, cache, external calls}

## Business Rules

{List of business rules enforced}

## Dependencies

**Services used**: {list with purposes}
**Database tables**: {list}
**External APIs**: {list if applicable}

## Consumers

**Backend**: {services that use this feature}
**Frontend**: {components that use this feature}
**External**: {public APIs, webhooks}

## Extension Points

**Events**: {events emitted}
**Plugins**: {plugin system if available}
**Configuration**: {feature flags, config}

## Extension Recommendation

**Planned change**: {what you want to add}

### Option Analysis

#### Option 1: {Approach}
**Pros**: {list}
**Cons**: {list}
**SRP Assessment**: {pass/fail}
**Risk**: {low/medium/high}

#### Option 2: {Approach}
**Pros**: {list}
**Cons**: {list}
**SRP Assessment**: {pass/fail}
**Risk**: {low/medium/high}

### Recommendation

**Chosen approach**: {option}

**Rationale**: {reasoning}

**Implementation steps**:
1. {step}
2. {step}

## Testing

**Existing tests**: {coverage summary}
**Test patterns**: {approach}
**Testing gaps**: {what's missing}
**New tests needed**: {for extension}

## Known Issues & Limitations

{Any issues or constraints}

## Files Reference

**Core files**:
- {file} - {purpose}

**Tests**:
- {test-file} - {coverage}

## References

- Original PRD: {link}
- Related features: {links}
- Database schema: {link}
```

## Success Criteria

Feature analysis is complete when:
- [ ] Feature scope clearly defined
- [ ] All feature files located and cataloged
- [ ] Data models fully documented with relationships
- [ ] Data flows mapped end-to-end
- [ ] Business rules identified and documented
- [ ] Dependencies and consumers mapped
- [ ] Extension points identified
- [ ] Extend vs new code decision made
- [ ] Testing approach understood
- [ ] Comprehensive feature documentation created
- [ ] Extension recommendation is specific and actionable

## Tips & Best Practices

### Do's
1. **Start with user perspective** - Understand what the feature does for users
2. **Trace data flows visually** - Diagrams help understanding
3. **Read actual code** - Don't assume based on file names
4. **Consider SRP** - Respect Single Responsibility Principle
5. **Document for others** - Future you or team members will thank you

### Don'ts
1. **Don't skip testing analysis** - Tests reveal feature contracts
2. **Don't ignore edge cases** - Business rules often hide in error handlers
3. **Don't assume patterns** - Read code to verify
4. **Don't overlook dependencies** - Missing a dependency causes issues
5. **Don't rush the decision** - Take time to evaluate extension options

### Time Management

**Quick understanding** (20-30 min):
- Feature scope + file location + data model
- Sufficient for simple extensions

**Standard understanding** (45-60 min):
- Add data flows + business rules + dependencies
- Sufficient for most extensions

**Deep understanding** (90+ min):
- Complete analysis with testing + quality
- Needed for complex extensions or refactoring

## Related Workflows

- Use **analyze-codebase** for initial project context
- Use **find-patterns** to understand conventions before extending
- Use **trace-dependencies** for complex dependency analysis
- Output informs implementation planning

## Related Context Files

- `../context/analysis-patterns.md` - Feature analysis techniques
- `../context/search-strategies.md` - Finding feature-related code
- `../context/documentation-standards.md` - Feature documentation templates
