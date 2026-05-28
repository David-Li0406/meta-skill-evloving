# Cursor AI

## Patterns


---
  #### **Name**
Project Rules Setup
  #### **Description**
Configure AI behavior for your project
  #### **When To Use**
Start of any project using Cursor
  #### **Implementation**
    # Modern rules structure (Cursor 2.0+)
    # Use .cursor/rules/*.mdc files instead of .cursorrules
    
    # .cursor/rules/core.mdc
    # Core rules that always apply
    ---
    description: Core project rules
    globs: ["**/*"]
    ---
    
    # Project Context
    You are working on [PROJECT NAME], a [DESCRIPTION].
    
    ## Tech Stack
    - Framework: Next.js 15 with App Router
    - Language: TypeScript (strict mode)
    - Styling: Tailwind CSS
    - Database: PostgreSQL with Prisma
    
    ## Coding Standards
    - Use functional components with hooks
    - Prefer named exports over default exports
    - Handle errors at the beginning of functions
    - Use early returns to avoid deep nesting
    
    ## File Conventions
    - Components: PascalCase (UserProfile.tsx)
    - Utilities: camelCase (formatDate.ts)
    - Constants: SCREAMING_SNAKE_CASE
    
    ## Forbidden
    - Never use `any` type
    - Never commit .env files
    - Never use console.log in production code
    - Never modify files in /generated/
    
    # .cursor/rules/testing.mdc
    ---
    description: Testing conventions
    globs: ["**/*.test.ts", "**/*.spec.ts", "tests/**/*"]
    ---
    
    ## Testing Rules
    - Use Vitest for unit tests
    - Use Playwright for E2E tests
    - Each test file must have at least one test
    - Mock external services, never call real APIs
    
    # .cursor/rules/api.mdc
    ---
    description: API route conventions
    globs: ["app/api/**/*", "src/api/**/*"]
    ---
    
    ## API Rules
    - Always validate input with Zod
    - Return consistent error format
    - Use proper HTTP status codes
    - Log all errors to monitoring
    

---
  #### **Name**
Plan Mode Workflow
  #### **Description**
Structured development with planning
  #### **When To Use**
Complex features, refactoring, multi-file changes
  #### **Implementation**
    # Plan Mode Best Practices
    
    ## Starting a Plan
    # Press Shift + Tab in agent input, or select "plan" mode
    
    ## Effective Planning Prompts
    
    # BAD - too vague
    "Add authentication to the app"
    
    # GOOD - specific with constraints
    "Plan: Add authentication to the app
    
    Requirements:
    - Use NextAuth.js with credentials provider
    - Support Google OAuth as secondary option
    - Store sessions in database (Prisma)
    - Protect /dashboard/* routes
    
    Constraints:
    - Don't modify existing user model structure
    - Keep backward compatibility with current sessions
    - Follow existing code patterns in /auth directory
    
    Output a step-by-step plan with:
    1. Files to create/modify
    2. Dependencies to add
    3. Migration requirements
    4. Testing approach"
    
    ## Plan Review Checklist
    Before approving a plan:
    - [ ] Does it touch only necessary files?
    - [ ] Are dependencies reasonable?
    - [ ] Is the order of operations correct?
    - [ ] Are there clear success criteria?
    
    ## Model Selection for Planning
    # Use reasoning models for planning (o1, o3)
    # Use fast models for building (Sonnet, GPT-4o)
    
    # In Cursor settings or per-prompt:
    # Plan with: claude-3-5-sonnet or o1
    # Build with: claude-3-5-sonnet or gpt-4o
    

---
  #### **Name**
Background Agents
  #### **Description**
Parallel work with isolated agents
  #### **When To Use**
Multiple features, long-running tasks, exploring alternatives
  #### **Implementation**
    # Background Agents (Cursor 2.0+)
    
    ## When to Use
    - Parallel feature development
    - Long-running refactoring
    - Exploring multiple approaches
    - Tasks that would block your flow
    
    ## How to Launch
    1. Write your prompt in agent input
    2. Select "Background" instead of running directly
    3. Agent runs in isolated environment (git worktree or VM)
    
    ## Best Practices
    
    # 1. Clear, self-contained prompts
    "Background: Implement user avatar upload
    
    Files to work in:
    - src/components/AvatarUpload.tsx (create)
    - src/api/upload.ts (create)
    - src/lib/storage.ts (modify)
    
    Requirements:
    - Max 5MB file size
    - Resize to 200x200
    - Store in S3
    - Update user profile
    
    When done:
    - All tests pass
    - Create PR with description"
    
    # 2. Run multiple agents for alternatives
    "Background Agent 1: Implement with S3 direct upload"
    "Background Agent 2: Implement with Cloudflare R2"
    "Background Agent 3: Implement with Uploadthing"
    # Review all three PRs, pick best approach
    
    # 3. Set clear completion criteria
    "Done when:
    - npm run build passes
    - npm run test passes
    - PR is created with description
    - No TypeScript errors"
    
    ## Limitations
    - Agents can't ask clarifying questions
    - Each agent works on separate branch
    - Limited to 8 concurrent agents
    - Requires good initial prompt
    

---
  #### **Name**
Context Management
  #### **Description**
Effective use of @-mentions and context
  #### **When To Use**
All Cursor interactions
  #### **Implementation**
    # Context Management in Cursor
    
    ## @-mention Types
    
    # Files - include specific files
    @src/components/Button.tsx
    @package.json
    
    # Folders - include directory contents
    @src/components/
    
    # Symbols - reference specific code
    @UserProfile (component)
    @handleSubmit (function)
    
    # Web - fetch documentation
    @Web "Next.js 15 server actions"
    
    # Docs - reference configured docs
    @Docs (searches configured documentation)
    
    # Git - reference git context
    @Git (recent commits, changes)
    
    # Codebase - semantic search
    @Codebase "authentication flow"
    
    ## Context Strategies
    
    # MINIMAL - for simple tasks
    "Fix the typo in @README.md"
    
    # FOCUSED - for specific changes
    "Add loading state to @Button.tsx
    Follow the pattern in @Spinner.tsx"
    
    # COMPREHENSIVE - for complex features
    "Implement password reset flow
    
    Reference:
    @src/auth/ (existing auth code)
    @src/email/ (email templates)
    @prisma/schema.prisma (user model)
    @Web 'NextAuth password reset'"
    
    ## Token Optimization
    # Rules files reduce needed context
    # .cursor/rules/*.mdc only load when relevant (by glob)
    # This is more efficient than one large .cursorrules
    

---
  #### **Name**
Agent Mode Optimization
  #### **Description**
Get better results from Cursor Agent
  #### **When To Use**
Complex multi-step tasks
  #### **Implementation**
    # Cursor Agent Best Practices
    
    ## 1. Write Effective Rules
    # Put these in .cursor/rules/agent.mdc
    ---
    description: Agent behavior rules
    globs: ["**/*"]
    ---
    
    When working as an agent:
    - Always read files before modifying
    - Run tests after changes
    - Commit with descriptive messages
    - Never force push
    - Ask before deleting files
    
    ## 2. Prompt Patterns
    
    # Include constraints upfront
    "Refactor the auth module.
    
    CONSTRAINTS:
    - Don't change public API
    - Keep all existing tests passing
    - One commit per logical change
    
    FORBIDDEN:
    - Adding new dependencies
    - Modifying database schema"
    
    # Paste errors directly
    "Fix this error:
    ```
    TypeError: Cannot read property 'map' of undefined
        at UserList (src/components/UserList.tsx:23:15)
    ```
    
    The users array is sometimes undefined."
    
    ## 3. Git Discipline
    - Work on feature branches
    - Commit frequently
    - Review diffs before approving
    - Keep PRs small
    
    ## 4. Recovery Patterns
    # If agent goes off track:
    - Ctrl+Z to undo changes
    - git checkout . to reset
    - Start fresh with more constraints
    - Use Plan Mode for complex tasks
    

## Anti-Patterns


---
  #### **Name**
Bloated Rules Files
  #### **Description**
Single massive .cursorrules with everything
  #### **Why Bad**
    High token usage on every request.
    Rules for tests loaded when editing components.
    Hard to maintain and update.
    
  #### **What To Do Instead**
    Split into .cursor/rules/*.mdc with glob patterns.
    core.mdc for universal rules.
    testing.mdc for test files.
    api.mdc for API routes.
    

---
  #### **Name**
Vague Prompts
  #### **Description**
Asking for changes without specifics
  #### **Why Bad**
    Agent makes assumptions.
    Results don't match expectations.
    More back-and-forth iterations.
    
  #### **What To Do Instead**
    Include specific file paths.
    Paste error messages directly.
    Define clear constraints and forbidden actions.
    Specify expected output format.
    

---
  #### **Name**
Skipping Plan Mode
  #### **Description**
Jumping straight to implementation for complex tasks
  #### **Why Bad**
    Agent may take wrong approach.
    Harder to course-correct mid-way.
    Miss architectural considerations.
    
  #### **What To Do Instead**
    Use Plan Mode for anything touching >3 files.
    Review and refine plan before building.
    Use different models for planning vs building.
    

---
  #### **Name**
Context Overload
  #### **Description**
Including entire codebase in every request
  #### **Why Bad**
    Hits token limits.
    Dilutes relevant information.
    Slower responses.
    
  #### **What To Do Instead**
    Use specific @file references.
    Let @Codebase search do semantic lookup.
    Configure rules to provide persistent context.
    

---
  #### **Name**
No Rules Version Control
  #### **Description**
Keeping rules only locally
  #### **Why Bad**
    Team members have different experiences.
    Knowledge not shared.
    Hard to onboard new developers.
    
  #### **What To Do Instead**
    Commit .cursor/rules/ to git.
    Document rules in team wiki.
    Review rules changes in PRs.
    