# Product Specification Examples

## Example 1: User Authentication

```markdown
# Feature: Email-based User Authentication

## Context

The application is a FastAPI backend with PostgreSQL. Currently no auth exists.
Will use `pyjwt` for tokens and `passlib` for password hashing (already in requirements).
User model exists in `models/user.py` but lacks password field.

## User Story

As a user
I want to log in with my email and password
So that I can access protected resources

## MVP Scope

**In Scope:**

- User registration with email/password
- Login endpoint returning JWT
- Password hashing with bcrypt
- Token validation middleware

**Deferred:**

- Password reset → v2
- Email verification → v2
- Refresh tokens → v2
- OAuth providers → Future

## Acceptance Criteria

### Scenario: Successful registration

Given I am a new user
When I POST to /auth/register with:
| email | test@example.com |
| password | SecurePass123! |
Then the response status is 201
And a new user is created in the database
And the password is stored as a bcrypt hash
And I receive a JWT access token

### Scenario: Registration with existing email

Given a user exists with email "taken@example.com"
When I POST to /auth/register with email "taken@example.com"
Then the response status is 409 Conflict
And the message is "Email already registered"

### Scenario: Successful login

Given a user exists with email "user@example.com" and password "MyPassword123"
When I POST to /auth/login with those credentials
Then the response status is 200
And I receive a JWT access token
And the token contains the user_id claim

### Scenario: Login with wrong password

Given a user exists with email "user@example.com"
When I POST to /auth/login with wrong password
Then the response status is 401 Unauthorized
And the message is "Invalid credentials"

### Scenario: Accessing protected endpoint

Given I have a valid JWT token
When I GET /api/protected with Authorization: Bearer <token>
Then the response status is 200
And the request context contains my user_id

### Scenario: Accessing protected endpoint without token

Given I have no token
When I GET /api/protected without Authorization header
Then the response status is 401 Unauthorized

### Scenario: Password validation rules

Given I am registering a new account
When I submit a password that:
| Condition | Result |
| Less than 8 chars | Invalid |
| No uppercase letter | Invalid |
| No lowercase letter | Invalid |
| No number | Invalid |
| Meets all criteria | Valid |
Then appropriate validation error is returned

## Non-Functional Requirements

- Performance: Auth endpoints respond in <100ms p95
- Security: Passwords hashed with bcrypt, cost factor 12
- Security: JWT expires after 24 hours
- Security: Rate limit: 5 failed logins per minute per IP

## Technical Notes

- Add `password_hash` column to existing `users` table
- Use dependency injection pattern for auth middleware
- JWT secret stored in environment variable `JWT_SECRET`
- Follow existing error response format in `api/errors.py`

## Success Metrics

- <1% login failures due to system errors
- Auth endpoints handle 100 concurrent requests
- Zero password storage vulnerabilities
```

## Example 2: File Upload

```markdown
# Feature: Document Upload

## Context

React frontend with Node/Express backend. Using AWS S3 for storage.
`aws-sdk` already installed. Existing upload logic in `services/s3.js`
for profile images can be extended.

## User Story

As a user
I want to upload documents to my account
So that I can store and access important files

## MVP Scope

**In Scope:**

- Upload single file (PDF, DOC, DOCX)
- Max file size: 10MB
- Store in S3 with user-scoped prefix
- List uploaded documents
- Download document

**Deferred:**

- Multiple file upload → v2
- File preview → v2
- Folder organization → Future
- Sharing documents → Future

## Acceptance Criteria

### Scenario: Successful file upload

Given I am logged in
And I have a 5MB PDF file
When I upload the file via the upload form
Then the file is stored in S3 at "documents/{user_id}/{uuid}.pdf"
And a document record is created in the database
And I see the file in my documents list
And I see a success notification

### Scenario: File exceeds size limit

Given I am logged in
And I have a 15MB file
When I attempt to upload the file
Then the upload is rejected before transfer
And I see "File exceeds maximum size of 10MB"

### Scenario: Invalid file type

Given I am logged in
And I have an .exe file
When I attempt to upload the file
Then the upload is rejected
And I see "File type not allowed. Supported: PDF, DOC, DOCX"

### Scenario: Download document

Given I am logged in
And I have a document "report.pdf" in my account
When I click the download button
Then the file downloads with original filename
And the Content-Disposition header is set correctly

### Scenario: Attempting to access another user's document

Given I am logged in as user A
And user B has a document with ID "doc-123"
When I try to GET /api/documents/doc-123
Then the response is 404 Not Found

### Scenario: Upload progress indication

Given I am uploading a 8MB file
When the upload is in progress
Then I see a progress bar showing percentage complete
And I can cancel the upload

## Non-Functional Requirements

- Performance: Upload starts within 1 second of selection
- Performance: Download initiates within 500ms
- Security: Files stored with private ACL
- Security: Signed URLs expire after 15 minutes
- UX: Drag-and-drop upload supported
- UX: File type icons displayed in list

## Technical Notes

- Extend existing `S3Service.upload()` method
- Use multipart upload for files >5MB
- Store metadata in `documents` table: id, user_id, filename, s3_key, size, mime_type, created_at
- Generate presigned URLs for downloads
- Frontend: Use `react-dropzone` for drag-drop

## Success Metrics

- 99% upload success rate
- Average upload speed >1MB/s
- <500ms time to first byte on download
```

## Example 3: Notification System

```markdown
# Feature: In-App Notifications

## Context

React SPA with WebSocket support via Socket.io (already configured).
Notifications table exists but unused. Backend is Express with PostgreSQL.
Current notification model in `models/notification.js`.

## User Story

As a user
I want to receive real-time notifications
So that I'm aware of important events without refreshing

## MVP Scope

**In Scope:**

- Real-time notification delivery via WebSocket
- Notification bell with unread count
- Mark notification as read
- Mark all as read
- Notification types: mention, comment, assignment

**Deferred:**

- Email notifications → v2
- Push notifications → v2
- Notification preferences → v2
- Notification grouping → Future

## Acceptance Criteria

### Scenario: Receiving real-time notification

Given I am logged in and connected via WebSocket
When another user mentions me in a comment
Then I receive a notification within 1 second
And the notification bell shows updated unread count
And I hear a subtle notification sound

### Scenario: Viewing notification list

Given I have 5 unread and 10 read notifications
When I click the notification bell
Then I see a dropdown with notifications
And unread notifications are visually distinct
And notifications are sorted newest first
And I see a maximum of 10 notifications with "View all" link

### Scenario: Marking single notification as read

Given I have an unread notification
When I click on the notification
Then it's marked as read in the database
And the visual styling updates to "read" state
And the unread count decreases by 1

### Scenario: Mark all as read

Given I have 5 unread notifications
When I click "Mark all as read"
Then all notifications are marked as read
And the unread count becomes 0

### Scenario: Notification content by type

Given notifications of different types exist
When I view the notification list
Then each type displays appropriately:
| Type | Icon | Message Format |
| mention | @ | "{user} mentioned you in {item}" |
| comment | 💬 | "{user} commented on {item}" |
| assignment | 📋 | "{user} assigned you to {item}" |

### Scenario: Reconnection handling

Given I was connected via WebSocket
And my connection dropped
When the connection is restored
Then I receive any notifications sent during disconnection
And the unread count is accurate

## Non-Functional Requirements

- Performance: Notification delivered <1s from trigger event
- Performance: Notification list loads <200ms
- Reliability: No lost notifications on brief disconnections
- UX: Notification sound respects system preferences
- UX: Dropdown doesn't block other UI interactions

## Technical Notes

- Use existing Socket.io setup in `lib/socket.js`
- Notification created via `NotificationService.create()` which emits to socket
- Store read_at timestamp for read status
- Unread count cached in Redis, invalidated on read/new
- Frontend: Use React context for notification state

## Success Metrics

- 99.9% notification delivery rate
- <1s average delivery latency
- <5% of users disable notifications
```

## Example 4: Search Feature

```markdown
# Feature: Global Search

## Context

E-commerce platform with products, categories, and orders.
PostgreSQL database with full-text search capabilities.
No existing search implementation.

## User Story

As a shopper
I want to search across products
So that I can quickly find what I'm looking for

## MVP Scope

**In Scope:**

- Search products by name and description
- Autocomplete suggestions as user types
- Search results with relevance ranking
- Basic filters: category, price range

**Deferred:**

- Search history → v2
- Elasticsearch integration → Future
- Fuzzy matching → Future
- Search analytics → Future

## Acceptance Criteria

### Scenario: Basic product search

Given products exist in the database
When I type "wireless headphones" in the search bar and press Enter
Then I see products matching "wireless headphones"
And results are ranked by relevance
And I see product image, name, price for each result

### Scenario: Autocomplete suggestions

Given I am on any page with the search bar
When I type "wire" in the search bar
Then I see up to 5 autocomplete suggestions within 200ms
And suggestions show matching product names
And I can select a suggestion with keyboard or mouse

### Scenario: No results found

Given no products match "xyznonexistent"
When I search for "xyznonexistent"
Then I see "No products found for 'xyznonexistent'"
And I see suggested categories or popular products

### Scenario: Filtering by category

Given search results for "headphones" are displayed
When I select category filter "Electronics > Audio"
Then results are filtered to that category
And the URL updates with filter parameters
And filter can be removed with one click

### Scenario: Filtering by price range

Given search results are displayed
When I set price filter $50 - $100
Then only products in that range are shown
And the active filter is displayed
And count of filtered results is updated

### Scenario: Empty search submission

Given I am on the search page
When I submit an empty search query
Then I see popular products or categories
And I don't see an error message

### Scenario: Search with special characters

Given products exist
When I search for "beats & audio"
Then special characters are handled safely
And relevant results are returned

## Non-Functional Requirements

- Performance: Search results in <300ms
- Performance: Autocomplete in <200ms
- UX: Minimum 3 characters before autocomplete triggers
- UX: Debounce autocomplete by 150ms
- Security: Search input sanitized to prevent injection
- Accessibility: Keyboard navigation for autocomplete

## Technical Notes

- Use PostgreSQL `tsvector` and `tsquery` for full-text search
- Create GIN index on products(search_vector)
- Autocomplete queries against materialized view for performance
- Cache popular searches in Redis with 5-minute TTL
- Frontend: Debounce search input, cancel pending requests

## Success Metrics

- > 90% of searches return relevant results (measured via click-through)
- Average search latency <200ms
- <10% of users refine their search query
```

## Anti-Patterns to Avoid

### Too Vague

```markdown
# Bad: Vague Scenario

Scenario: User can search
Given a user
When they search
Then they see results
```

### Missing Edge Cases

```markdown
# Bad: Only happy path

Scenario: Upload file
Given user is logged in
When they upload a file
Then file is uploaded

# Missing: Size limits, invalid types, network errors, permissions
```

### Untestable Criteria

```markdown
# Bad: Subjective requirements

- UX: Should feel fast
- UX: Should be intuitive
- Performance: Should be responsive

# Good: Measurable requirements

- UX: Page loads in <2s on 3G connection
- UX: Primary action reachable in <3 clicks
- Performance: API responds in <200ms p95
```

### Scope Creep

```markdown
# Bad: Kitchen sink MVP

**In Scope:**

- Basic auth
- Social login (Google, Facebook, Twitter, GitHub, LinkedIn)
- 2FA
- Password reset
- Email verification
- Session management
- SSO integration
- Biometric authentication

# Good: Focused MVP

**In Scope:**

- Email/password registration
- Login with JWT
- Basic password validation

**Deferred:**

- Social login → v2
- 2FA → v2
- Password reset → v2
```

## Example 5: Complex Feature with Parallel Execution

```markdown
# Feature: Document Management System

## Context

Laravel 11 backend with React frontend (Inertia.js).
AWS S3 configured via `config/filesystems.php`.
No existing document handling - building from scratch.
User model exists with standard auth.

## Complexity Assessment

| Factor           | Score     | Notes                                                            |
| ---------------- | --------- | ---------------------------------------------------------------- |
| Files affected   | 3/3       | 4 backend + 6 frontend + migration                               |
| New dependencies | 2/3       | spatie/laravel-medialibrary (backend), react-dropzone (frontend) |
| Database changes | 2/3       | New `documents` table with polymorphic relations                 |
| External APIs    | 2/3       | AWS S3 for storage                                               |
| Business logic   | 2/3       | Access control, file validation, versioning logic                |
| Risk level       | 2/3       | Medium - file handling, storage costs                            |
| **Total**        | **13/18** |                                                                  |

**Workflow**: Complex (Feature-Refiner → Parallel Coders → QA)
**Parallel Execution**: Yes

- Backend: S3 service, model, controller, policies
- Frontend: Upload UI, document list, preview modal

## User Story

As a project member
I want to upload and manage documents
So that I can share files with my team

## MVP Scope

**In Scope:**

- Upload single document (PDF, DOC, DOCX, images)
- List documents with metadata
- Download documents
- Delete own documents
- Basic access control (project-scoped)

**Deferred:**

- Multiple file upload → v2
- Document preview → v2
- Version history → v2
- Folders/organization → Future
- Full-text search → Future

## Acceptance Criteria

### Scenario: Successful document upload

Given I am logged in as a project member
And I have a 5MB PDF file
When I drop the file on the upload zone
Then I see upload progress indicator
And the file is stored in S3 at "projects/{project_id}/documents/{uuid}.pdf"
And a document record is created with metadata
And the document appears in my list immediately

### Scenario: File type validation

Given I am on the upload page
When I try to upload an .exe file
Then the upload is rejected client-side
And I see "File type not allowed. Supported: PDF, DOC, DOCX, PNG, JPG"

### Scenario: File size limit

Given I am uploading a document
When the file exceeds 25MB
Then the upload is rejected
And I see "File size exceeds 25MB limit"

### Scenario: Download document

Given a document "report.pdf" exists in my project
When I click the download button
Then the file downloads with original filename
And download is tracked for analytics

### Scenario: Delete document

Given I uploaded "my-doc.pdf"
When I click delete and confirm
Then the document is soft-deleted
And it no longer appears in the list
And the S3 file is scheduled for deletion

### Scenario: Access control

Given I am member of Project A only
And Project B has document "secret.pdf"
When I try to access Project B's document
Then I receive 403 Forbidden

## Non-Functional Requirements

- Performance: Upload starts within 500ms of drop
- Performance: Document list loads in <200ms
- Security: Signed URLs expire after 15 minutes
- Security: Files stored with private ACL
- UX: Drag-and-drop with visual feedback
- UX: Upload progress percentage shown

## Technical Notes

### Backend

- Use spatie/laravel-medialibrary for S3 abstraction
- Document model with `project_id`, `user_id`, `filename`, `path`, `size`, `mime_type`
- DocumentPolicy for authorization
- Presigned URLs for secure downloads

### Frontend

- react-dropzone for drag-and-drop
- Optimistic UI updates
- useQuery for document list with polling

## Implementation Plan

### Part 1: Backend/API (specs/documents-api.md)

- [ ] Document model and migration
- [ ] DocumentService (upload, download URL, delete)
- [ ] DocumentController with resource routes
- [ ] DocumentPolicy
- [ ] Form Request for validation

### Part 2: Frontend/UI (specs/documents-ui.md)

- [ ] DocumentUploader component (dropzone)
- [ ] DocumentList component
- [ ] DocumentRow with actions
- [ ] Upload progress indicator
- [ ] Delete confirmation modal

**Execution**: Parallel - no shared state, API contract defined

## API Contract (for parallel development)
```

POST /api/projects/{id}/documents → Upload (multipart)
GET /api/projects/{id}/documents → List
GET /api/documents/{id}/download → Get signed URL
DELETE /api/documents/{id} → Soft delete

Response format:
{
"id": "uuid",
"filename": "report.pdf",
"size": 1024000,
"mime_type": "application/pdf",
"download_url": "signed-s3-url",
"created_at": "2025-01-15T10:00:00Z",
"user": { "id": 1, "name": "John" }
}

```

## Success Metrics
- 99% upload success rate
- Average upload speed >2MB/s
- <500ms time to first byte on download
- Zero unauthorized access incidents
```

---

## Example 6: Simple Feature (Coder Only)

```markdown
# Feature: Add User Timezone Preference

## Context

Laravel app with User model. Settings page exists at `resources/js/Pages/Settings/Profile.vue`.
No timezone handling currently - all times shown in UTC.

## Complexity Assessment

| Factor           | Score    | Notes                           |
| ---------------- | -------- | ------------------------------- |
| Files affected   | 1/3      | Migration, Model, Settings page |
| New dependencies | 1/3      | None                            |
| Database changes | 1/3      | Add column to users             |
| External APIs    | 1/3      | None                            |
| Business logic   | 1/3      | Simple getter/setter            |
| Risk level       | 1/3      | Very low                        |
| **Total**        | **6/18** |                                 |

**Workflow**: Simple (Coder only)
**Parallel Execution**: No

## User Story

As a user
I want to set my timezone
So that I see dates/times in my local time

## MVP Scope

**In Scope:**

- Timezone dropdown on settings page
- Save timezone to user profile
- Default to UTC for existing users

**Deferred:**

- Auto-detect timezone → v2
- Apply timezone to displayed dates → separate feature

## Acceptance Criteria

### Scenario: Set timezone

Given I am on my settings page
When I select "America/Sao_Paulo" from timezone dropdown
And click Save
Then my timezone preference is stored
And I see success message

### Scenario: Default timezone

Given I am a new user
When I view my profile
Then my timezone is "UTC"

## Technical Notes

- Add `timezone` column to users table (string, nullable, default 'UTC')
- Use PHP's `DateTimeZone::listIdentifiers()` for options
- Add to existing ProfileController update method

## Success Metrics

- Users can save timezone without errors
```

---

## Example 7: Medium Feature (Coder → QA)

```markdown
# Feature: API Rate Limiting Dashboard

## Context

Laravel API with existing rate limiting via `ThrottleRequests` middleware.
Admin panel exists using Filament. Redis configured for cache.

## Complexity Assessment

| Factor           | Score    | Notes                                    |
| ---------------- | -------- | ---------------------------------------- |
| Files affected   | 2/3      | New Filament resource, service, 2 views  |
| New dependencies | 1/3      | None (Filament exists)                   |
| Database changes | 1/3      | None (reads from Redis)                  |
| External APIs    | 1/3      | None                                     |
| Business logic   | 2/3      | Aggregate rate limit data, display logic |
| Risk level       | 1/3      | Read-only, low risk                      |
| **Total**        | **9/18** |                                          |

**Workflow**: Medium (Coder → QA)
**Parallel Execution**: No

## User Story

As an admin
I want to see API rate limit statistics
So that I can monitor usage and identify abuse

## MVP Scope

**In Scope:**

- Dashboard showing current rate limit status per API key
- List of recently throttled requests
- Basic filtering by date range

**Deferred:**

- Real-time updates → v2
- Alerts for threshold breaches → v2
- Export data → Future

## Acceptance Criteria

### Scenario: View rate limit dashboard

Given I am logged in as admin
When I navigate to Admin > Rate Limits
Then I see a table of API keys with their current usage
And each row shows: key name, requests today, limit, % used

### Scenario: View throttled requests

Given there have been throttled requests today
When I view the "Throttled Requests" tab
Then I see the most recent 100 throttled requests
And each shows: timestamp, API key, endpoint, IP address

### Scenario: Filter by date

Given I am viewing rate limit data
When I select "Last 7 days" from the date filter
Then the statistics update to show that period

## Technical Notes

- Create RateLimitService to read from Redis
- New Filament Page (not Resource - read only)
- Use Laravel's RateLimiter facade for data access

## Success Metrics

- Dashboard loads in <1s
- Data accurately reflects Redis state
- Admins can identify high-usage API keys
```

---

## Complexity Assessment Quick Reference

| Score     | Workflow             | Example Features                                          |
| --------- | -------------------- | --------------------------------------------------------- |
| **6-8**   | Coder only           | Add column, update copy, CSS fix, simple validation       |
| **9-12**  | Coder → QA           | New CRUD, form with logic, bug fix + tests, new component |
| **13-18** | Refiner → Coder → QA | Auth system, payments, external API, architecture change  |
