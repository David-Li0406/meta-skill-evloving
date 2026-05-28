# Cursor Ai - Sharp Edges

## Rules File Location

### **Id**
rules-file-location
### **Summary**
Rules in wrong location are ignored
### **Severity**
high
### **Situation**
Created rules but AI doesn't follow them
### **Why**
  Cursor looks in specific locations.
  .cursorrules must be in project root.
  .cursor/rules/*.mdc for modern split rules.
  Wrong path = silently ignored.
  
### **Solution**
  // Correct rules file locations
  
  // LEGACY (still works, not recommended)
  project-root/
  └── .cursorrules           # Must be in root
  
  // MODERN (recommended)
  project-root/
  └── .cursor/
      └── rules/
          ├── core.mdc       # Universal rules
          ├── testing.mdc    # Test file rules
          └── api.mdc        # API route rules
  
  // WRONG - will be ignored
  project-root/
  ├── .cursor/rules.mdc      # Wrong - needs rules/ folder
  ├── cursor/rules/core.mdc  # Wrong - needs dot prefix
  ├── .cursorrules.md        # Wrong - no .md extension
  └── src/.cursorrules       # Wrong - must be in root
  
  // Verify rules are loaded:
  // Open Cursor, start a chat
  // Rules should appear in context
  // If not, check location and restart Cursor
  
### **Symptoms**
  - AI ignores project conventions
  - Rules work locally but not for teammates
  - No error messages about rules
### **Detection Pattern**
cursorrules|cursor/rules|\.mdc

## Mdc Glob Patterns

### **Id**
mdc-glob-patterns
### **Summary**
Wrong glob patterns in .mdc files
### **Severity**
high
### **Situation**
Rules don't apply to expected files
### **Why**
  .mdc files use frontmatter with globs.
  Wrong glob = rules never activate.
  No error when glob matches nothing.
  
### **Solution**
  // Correct .mdc frontmatter structure
  
  // .cursor/rules/testing.mdc
  ---
  description: Testing conventions
  globs: ["**/*.test.ts", "**/*.spec.ts", "tests/**/*"]
  ---
  
  Your testing rules here...
  
  // Common glob patterns:
  globs: ["**/*"]                    # All files (use sparingly)
  globs: ["src/**/*.ts"]             # TypeScript in src
  globs: ["**/*.test.{ts,tsx}"]      # Test files
  globs: ["app/api/**/*"]            # API routes
  globs: ["*.config.{js,ts,mjs}"]    # Config files in root
  
  // WRONG patterns:
  globs: ["*.ts"]        # Only matches root, not subdirs
  globs: ["src/*.ts"]    # Only direct children, not nested
  globs: ["./**/*.ts"]   # Don't use ./ prefix
  
  // CORRECT patterns:
  globs: ["**/*.ts"]     # All TypeScript files
  globs: ["src/**/*.ts"] # All TypeScript in src tree
  
  // Multiple patterns:
  globs:
    - "**/*.test.ts"
    - "**/*.spec.ts"
    - "__tests__/**/*"
  
### **Symptoms**
  - Rules apply to wrong files
  - Rules never activate
  - Inconsistent AI behavior
### **Detection Pattern**
globs.*\[|description.*:.*\nglobs

## Context Token Limits

### **Id**
context-token-limits
### **Summary**
Too much context causes truncation
### **Severity**
medium
### **Situation**
AI seems to ignore parts of your prompt or context
### **Why**
  Each model has context window limits.
  Large @Codebase or @Folder can fill it.
  Oldest context gets truncated first.
  Your important instructions may be cut.
  
### **Solution**
  // Managing context effectively
  
  // Check what's in context:
  // Look at the context panel in Cursor
  // Files and rules show token usage
  
  // PROBLEM: Too much context
  "Add a feature
  @src/            # Includes everything!
  @lib/
  @components/"
  
  // SOLUTION: Specific references
  "Add a feature
  @src/auth/login.ts
  @src/types/user.ts
  @components/LoginForm.tsx"
  
  // Use @Codebase for search instead of including all
  "Find authentication patterns
  @Codebase 'jwt token validation'"
  
  // Reduce rules token usage:
  // Split rules by glob so only relevant ones load
  // .cursor/rules/api.mdc only loads for API files
  
  // Token-efficient prompts:
  // - Be concise
  // - Reference specific files, not folders
  // - Use rules for persistent context
  // - Paste relevant code snippets, not entire files
  
  // Model context limits (approximate):
  // Claude Sonnet: 200k tokens
  // GPT-4o: 128k tokens
  // o1: 128k tokens
  
### **Symptoms**
  - AI forgets earlier instructions
  - Partial responses
  - "I don't see that file" errors
### **Detection Pattern**
@src/|@lib/|@components/

## Background Agent Isolation

### **Id**
background-agent-isolation
### **Summary**
Background agent can't access local state
### **Severity**
medium
### **Situation**
Background agent fails or misses context
### **Why**
  Background agents run in isolated environments.
  They don't see uncommitted changes.
  They can't access local env vars.
  They can't ask clarifying questions.
  
### **Solution**
  // Background Agent Requirements
  
  // 1. Commit your current state first
  git add .
  git commit -m "WIP: save state before background agent"
  
  // 2. Include all context in the prompt
  // BAD - assumes agent sees your state
  "Continue the auth implementation"
  
  // GOOD - self-contained prompt
  "Implement Google OAuth login
  
  Current state:
  - NextAuth is configured in /auth
  - User model has googleId field
  - Environment vars: GOOGLE_CLIENT_ID, GOOGLE_SECRET
  
  Files to modify:
  - src/auth/[...nextauth]/route.ts
  - src/lib/auth-options.ts
  
  Expected outcome:
  - Users can sign in with Google
  - Tests pass
  - PR created"
  
  // 3. Don't rely on environment variables
  // Background agents have their own env
  // Either:
  // - Use Cursor's secret management
  // - Include mock values for development
  // - Document required env vars in prompt
  
  // 4. Set clear success criteria
  "Done when:
  - npm run build passes
  - npm run test passes
  - No TypeScript errors
  - PR created with description"
  
### **Symptoms**
  - Agent can't find recent files
  - Environment variables undefined
  - Agent asks questions but can't receive answers
### **Detection Pattern**
background.*agent|parallel.*agent

## Model Mismatch

### **Id**
model-mismatch
### **Summary**
Using wrong model for task type
### **Severity**
medium
### **Situation**
Poor results despite good prompts
### **Why**
  Different models excel at different tasks.
  Reasoning models (o1) slow but thorough.
  Fast models (Sonnet) quick but may miss nuance.
  Using one for everything is suboptimal.
  
### **Solution**
  // Model Selection Guide
  
  // PLANNING & ARCHITECTURE
  // Use: o1, o3, Claude Sonnet with extended thinking
  // Why: Need thorough reasoning, trade-offs analysis
  "Plan the database migration strategy..."
  
  // IMPLEMENTATION
  // Use: Claude Sonnet, GPT-4o
  // Why: Fast, good at code generation
  "Implement the login form component..."
  
  // CODE REVIEW
  // Use: Claude Sonnet, o1 for security-critical
  // Why: Need thorough analysis
  "Review this authentication code..."
  
  // DEBUGGING
  // Use: Claude Sonnet with error context
  // Why: Good at pattern matching, fast iteration
  "Fix this error: [paste stack trace]"
  
  // QUICK EDITS
  // Use: Claude Haiku, GPT-4o-mini
  // Why: Fast, low cost, simple tasks
  "Rename this variable from x to userId"
  
  // In Cursor settings:
  // Set default model for each mode
  // Or select per-prompt in the UI
  
  // Plan Mode model selection:
  // Design plan with: reasoning model (o1)
  // Build plan with: fast model (Sonnet)
  
### **Symptoms**
  - Slow responses for simple tasks
  - Shallow analysis for complex tasks
  - High token costs
### **Detection Pattern**
model|claude|gpt|sonnet|opus

## Auto Run Dangers

### **Id**
auto-run-dangers
### **Summary**
Auto-run executes unreviewed commands
### **Severity**
high
### **Situation**
Agent runs destructive commands automatically
### **Why**
  Background agents auto-run all terminal commands.
  No approval step like foreground agent.
  Could run rm, git push --force, etc.
  
### **Solution**
  // Safe Auto-Run Configuration
  
  // 1. Use rules to restrict dangerous commands
  // .cursor/rules/safety.mdc
  ---
  description: Safety rules for agent mode
  globs: ["**/*"]
  ---
  
  NEVER run these commands without explicit approval:
  - rm -rf
  - git push --force
  - git reset --hard
  - DROP TABLE / DELETE FROM
  - npm publish
  - Any command with sudo
  
  Always run in dry-run mode first:
  - npm publish --dry-run
  - prisma migrate deploy --dry-run
  
  // 2. For Background Agents, be explicit
  "Implement feature X
  
  Allowed commands:
  - npm install
  - npm run build
  - npm run test
  - git commit
  - git push (to feature branch only)
  
  NOT allowed:
  - npm publish
  - Any force operations
  - Modifying main branch"
  
  // 3. Review agent actions after completion
  // Check git log for what was committed
  // Review any PRs before merging
  // Check for unintended side effects
  
### **Symptoms**
  - Unexpected deletions
  - Force pushes
  - Published packages
### **Detection Pattern**
auto.*run|background.*agent