# Create Project

Allows authenticated users to create a new project from the projects page.

# Functional Specification

## Behavior: Create Project

Allows authenticated users to create a new project. The user fills out a form with a project name and submits it. Upon successful creation, the new project appears in the project list with a default "draft" status.

Directory: `app/client/projects/behaviors/create-project/`

### Rules

#### Authentication Required
- When:
  - User is not authenticated
- Then:
  - Reject with "Unauthorized"
  - Redirect to login page

#### Name Required
- When:
  - Project name is empty
- Then:
  - Reject with "Name is required"
  - Form field "name" shows error

#### Name Too Long
- When:
  - Project name exceeds 100 characters
- Then:
  - Reject with "Name must be 100 characters or less"
  - Form field "name" shows error

#### Unique Name Per User
- When:
  - Project name already exists for this user
- Then:
  - Reject with "Project name already exists"
  - Form field "name" shows error

#### Default Status
- When:
  - Project is created successfully
- Then:
  - Status defaults to "draft"
  - Created timestamp is set to current time

### Examples

#### User creates a new project successfully

##### PreDB
users:
id, email, role, status
1, user@example.com, client, active

projects:
id, user_id, name, status, created_at
1, 1, Existing Project, active, <timestamp>

##### Steps
* Act: User logs in as "client"
* Act: User navigates to the projects page
* Act: User clicks "Create Project" button
* Act: User enters "New Project" in the name field
* Act: User clicks "Submit"
* Check: Success toast "Project created" is shown
* Check: New project "New Project" appears in the list
* Check: Project status shows "draft"

##### PostDB
projects:
id, user_id, name, status, created_at
1, 1, Existing Project, active, <timestamp>
2, 1, New Project, draft, <timestamp>

---

#### User tries to create project with duplicate name

##### PreDB
users:
id, email, role, status
1, user@example.com, client, active

projects:
id, user_id, name, status
1, 1, Existing Project, active

##### Steps
* Act: User logs in as "client"
* Act: User navigates to the projects page
* Act: User clicks "Create Project" button
* Act: User enters "Existing Project" in the name field
* Act: User clicks "Submit"
* Check: Error "Project name already exists" is shown on name field
* Check: No new project is created

##### PostDB
projects:
id, user_id, name, status
1, 1, Existing Project, active

---

# Technical Specification

## createProject(input: CreateProjectInput): Promise<Project>

Creates a new project for the authenticated user after validating the input.

- Given: project name (1-100 chars) and authenticated user with "client" role
- Returns: the newly created project with status "draft"
- Calls: ProjectModel.findByNameAndUser, ProjectModel.create

### Example: Create project successfully

#### PreDB
users:
id, email, role, status
1, user@example.com, client, active

projects:
id, user_id, name, status
1, 1, Existing Project, active

#### PostDB
projects:
id, user_id, name, status, created_at
1, 1, Existing Project, active, <timestamp>
2, 1, New Project, draft, <timestamp>

### Example: Reject duplicate name

#### PreDB
users:
id, email, role, status
1, user@example.com, client, active

projects:
id, user_id, name, status
1, 1, Existing Project, active

#### PostDB
(no changes - operation rejected with "Project name already exists")

---

## useCreateProject(options?: CreateProjectOptions)

Manages form state and submission logic for creating a new project with optimistic updates.

### Parameters
- options.onSuccess: (project: Project) => void - callback after successful creation

### State
- name: string
- errors: ValidationErrors
- isPending: boolean

### Returns
- name: string - current name value
- errors: ValidationErrors - field-level errors (name)
- isPending: boolean - submission in progress
- setName: (value: string) => void - update name field
- submit: () => Promise<void> - validate and submit the form
- reset: () => void - clear form to initial state

### Dependencies
- useProjects - for optimistic updates to project list
- useToast - for success/error notifications

---

## CreateProjectForm

Renders the form used to create a new project with a name input and submit button.

### Props
- onSuccess: (project: Project) => void - optional callback after creation

### State

#### Local
- (none - delegated to hook)

#### Shared
- projects: Project[] - via useProjects atom

### Children
- TextInput
- SubmitButton

---

# Tasks

* [ ] Backend implementation
  * [ ] Create create-project.action.ts with validation
  * [ ] Add ProjectModel.create method if not exists
  * [ ] Add ProjectModel.findByNameAndUser for uniqueness check
* [ ] Frontend components
  * [ ] Create use-create-project hook with optimistic updates
  * [ ] Create CreateProjectForm component
  * [ ] Add projectsAtom to state if not exists
* [ ] Testing
  * [ ] Write behavior test: User creates project successfully
  * [ ] Write behavior test: User tries duplicate name
  * [ ] Write action test: create-project.action.test.ts

# Notes

- Consider adding description field in future iteration
- Project creation should be tracked for analytics
- May need to create associated resources (sandbox, repository) in workflow
