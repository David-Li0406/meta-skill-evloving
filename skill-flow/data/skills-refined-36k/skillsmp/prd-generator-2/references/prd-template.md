# PRD Template

Use this template when generating PRDs. Replace bracketed placeholders with actual content.

```markdown
# [Project Name] PRD

## 1. Executive Summary

[2-3 sentences: what it is, why it matters, primary value]

## 2. Project Overview

**Project Name:** [Name]
**Purpose:** [Detailed purpose]
**Target Users:** [Primary personas]
**Success Metrics:** [How success is measured]

## 3. Tech Stack

- **Frontend:** [Framework/Library]
- **Backend:** [Framework/Runtime]
- **Database:** [Database system]
- **Authentication:** [Auth provider/method]
- **Hosting:** [Deployment target]
- **Other:** [Additional tools/services]

## 4. Scope

### 4.1 In-Scope Features

1. [Feature]
2. [Feature]
3. [Feature]

### 4.2 Out-of-Scope

- [Explicit exclusion]
- [Explicit exclusion]
- [Explicit exclusion]

## 5. User Stories & Tasks

### US-1: [User Story Title]

**As a** [user type], **I want** [goal] **so that** [benefit].

**Acceptance Criteria:**
- [ ] [Specific, testable criterion]
- [ ] [Specific, testable criterion]
- [ ] [Specific, testable criterion]

**Tasks:**
- [ ] [Implementation task]
- [ ] [Implementation task]
- [ ] [Implementation task]

---

### US-2: [User Story Title]

**As a** [user type], **I want** [goal] **so that** [benefit].

**Acceptance Criteria:**
- [ ] [Criterion]
- [ ] [Criterion]
- [ ] [Criterion]

**Tasks:**
- [ ] [Task]
- [ ] [Task]

---

## 6. Data Model

### Entity: [EntityName]

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | uuid | PK | Primary identifier |
| created_at | timestamp | NOT NULL | Creation time |
| [field] | [type] | [constraints] | [description] |

### Entity: [EntityName]

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | uuid | PK | Primary identifier |
| [field] | [type] | [constraints] | [description] |

## 7. API Endpoints

### [METHOD] /api/[endpoint]

- **Description:** [What it does]
- **Auth:** [Required/Optional/None]
- **Request:** `{ "field": "type" }`
- **Response:** `{ "field": "type" }`
- **Errors:** [4xx/5xx codes and meanings]

## 8. Non-Functional Requirements

### 8.1 Performance

- Initial page load: < [X] seconds
- API response time: < [X] ms
- [Other metrics]

### 8.2 Security

- [Requirement]
- [Requirement]

### 8.3 Accessibility

- [Requirement]

### 8.4 Error Handling

- [Approach for user-facing errors]
- [Approach for logging]
- [Retry/fallback strategies]

## 9. Environment Variables

```
DATABASE_URL=[connection string]
API_KEY=[service key]
[VAR]=[description]
```

## 10. Development Phases

### Phase 1: [Name]

- [ ] [Task]
- [ ] [Task]

### Phase 2: [Name]

- [ ] [Task]
- [ ] [Task]

### Phase 3: [Name]

- [ ] [Task]
- [ ] [Task]

## 11. Open Questions

- [ ] [Question needing resolution]
- [ ] [Question needing resolution]
```

## Example PRD

```markdown
# Super Notetaker PRD

## 1. Executive Summary

A web-based note-taking app for creating, saving, and organizing notes with a clean interface. Provides secure authentication and real-time saving for personal productivity.

## 2. Project Overview

**Project Name:** Super Notetaker
**Purpose:** Seamless note-taking with real-time saving and secure user data
**Target Users:** Individual users needing simple, reliable note organization
**Success Metrics:** User retention > 40%, notes created per user > 10/month

## 3. Tech Stack

- **Frontend:** React + Vite
- **Backend:** Supabase
- **Database:** PostgreSQL (Supabase)
- **Authentication:** Supabase Auth
- **Hosting:** Vercel
- **Other:** shadcn/ui components

## 4. Scope

### 4.1 In-Scope Features

1. User authentication (email/password)
2. Note CRUD operations
3. Real-time auto-saving
4. Rich text editing
5. Note search and filtering
6. Dark/light mode

### 4.2 Out-of-Scope

- Collaborative editing
- File attachments
- Mobile app versions
- Export/import functionality
- Advanced analytics

## 5. User Stories & Tasks

### US-1: User Authentication

**As a** user, **I want** to sign up and log in **so that** my notes are private and persistent.

**Acceptance Criteria:**
- [ ] Can sign up with email/password
- [ ] Can log in with existing credentials
- [ ] Can reset password via email
- [ ] Protected routes redirect to login
- [ ] Session persists across page refresh

**Tasks:**
- [ ] Set up Supabase project and auth configuration
- [ ] Create signup form with validation
- [ ] Create login form with validation
- [ ] Implement password reset flow
- [ ] Add auth state provider and protected route wrapper

---

### US-2: Note Management

**As a** user, **I want** to create and edit notes **so that** I can capture and organize my thoughts.

**Acceptance Criteria:**
- [ ] Can create new note with title and body
- [ ] Can edit existing notes
- [ ] Changes auto-save within 3 seconds
- [ ] Visual indicator shows save status
- [ ] Can delete notes with confirmation

**Tasks:**
- [ ] Create notes table in Supabase
- [ ] Build note editor component with rich text
- [ ] Implement auto-save with debounce
- [ ] Add save status indicator
- [ ] Create delete confirmation modal

---

## 6. Data Model

### Entity: users

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | uuid | PK | Supabase auth user ID |
| email | text | UNIQUE, NOT NULL | User email |
| created_at | timestamp | NOT NULL | Account creation |

### Entity: notes

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | uuid | PK | Note identifier |
| user_id | uuid | FK users.id | Owner |
| title | text | NOT NULL | Note title |
| body | text | | Note content |
| created_at | timestamp | NOT NULL | Creation time |
| updated_at | timestamp | NOT NULL | Last modified |

## 7. API Endpoints

Supabase client handles all data operations. Key queries:

### SELECT notes

- **Description:** Get user's notes
- **Auth:** Required (RLS policy)
- **Filter:** `user_id = auth.uid()`

### INSERT/UPDATE notes

- **Description:** Create or update note
- **Auth:** Required (RLS policy)

## 8. Non-Functional Requirements

### 8.1 Performance

- Initial load: < 2 seconds
- Auto-save latency: < 500ms
- Smooth typing with no lag

### 8.2 Security

- All routes protected with auth
- Row Level Security on notes table
- XSS protection via React

### 8.3 Accessibility

- Keyboard navigation support
- ARIA labels on interactive elements

### 8.4 Error Handling

- Toast notifications for user feedback
- Error boundaries for component failures
- Retry logic for failed saves

## 9. Environment Variables

```
VITE_SUPABASE_URL=[Supabase project URL]
VITE_SUPABASE_ANON_KEY=[Supabase anon key]
```

## 10. Development Phases

### Phase 1: Setup & Auth

- [ ] Initialize Vite + React project
- [ ] Configure Supabase client
- [ ] Implement auth flows
- [ ] Set up protected routing

### Phase 2: Core Features

- [ ] Create notes table and RLS policies
- [ ] Build note list view
- [ ] Build note editor with auto-save
- [ ] Implement search/filter

### Phase 3: Polish

- [ ] Add dark/light mode toggle
- [ ] Implement delete with confirmation
- [ ] Add loading states and error handling
- [ ] Deploy to Vercel

## 11. Open Questions

- [ ] Should notes support markdown rendering?
- [ ] Maximum note length limit?
```
