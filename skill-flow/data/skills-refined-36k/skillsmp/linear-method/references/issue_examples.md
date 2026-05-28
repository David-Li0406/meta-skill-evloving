# Issue Examples

This reference provides extensive examples of well-written and poorly-written issues to illustrate Linear Method principles.

## Feature Development Issues

### ✅ Good Examples

**Backend/API**
```
Title: Add rate limiting to login endpoint
Description:
Currently users can attempt unlimited logins. Add rate limiting:
- 5 attempts per IP per 15 minutes
- Return 429 with retry-after header
- Log excessive attempts for monitoring
```

```
Title: Implement webhook signature verification
Description:
Verify incoming Stripe webhooks are authentic before processing.
Use Stripe SDK's verify method with our webhook secret.
Return 401 for invalid signatures.
```

**Frontend**
```
Title: Add loading spinner to dashboard data fetch
Description:
Dashboard shows blank while fetching data. Add skeleton loader 
that displays during the initial fetch to improve perceived performance.
```

```
Title: Fix mobile menu overlapping content on iOS Safari
Description:
Mobile nav menu doesn't respect safe area on iPhone X+.
The close button gets hidden behind the notch. 
Add safe-area-inset-top to the header.
```

**Database/Schema**
```
Title: Add index on users.email for login performance
Description:
Login queries are slow (500ms+) as user count grows.
Add btree index on users.email since we query it on every login.
```

### ❌ Bad Examples (User Stories)

```
Title: User Authentication
Description:
As a user, I want to be able to log in to the system so that 
I can access my personalized dashboard and manage my account settings.

Acceptance Criteria:
- Given I am on the login page
- When I enter valid credentials
- Then I should be redirected to my dashboard
- And I should see my user information displayed
```
**Problem**: Too vague, written as a story not a task, no technical specifics

```
Title: Improve Performance
Description:
As a developer, I want the application to load faster so that 
users have a better experience.
```
**Problem**: Not actionable, no specific task, no clear outcome

```
Title: Dashboard Enhancements
Description:
As a user, I want an improved dashboard so that I can better 
understand my data and make informed decisions about my business.
```
**Problem**: Too broad, multiple features bundled, should be a project with multiple issues

## Bug Report Issues

### ✅ Good Examples

```
Title: CSV export fails for datasets over 10k rows
Description:
Steps to reproduce:
1. Go to Reports > Export
2. Select any report with 10k+ rows
3. Click "Export to CSV"
4. Browser shows "Script unresponsive" error

Expected: CSV downloads
Actual: Browser freezes, no download

User report: "Can't export our monthly sales report anymore - @jessica from Acme Corp"
Link to conversation: [URL]
```

```
Title: Password reset emails not arriving for Gmail users
Description:
Users with @gmail.com addresses report not receiving password reset emails.
Other providers (Outlook, Yahoo) work fine.

Checked:
- Emails are being sent (confirmed in logs)
- Not in spam folder (users confirmed)
- Possibly hitting Gmail rate limits?

Affects ~40% of users based on email domain stats.
Priority: High - blocking user access
```

### ❌ Bad Examples

```
Title: Fix bugs
Description: There are several bugs that need to be fixed in the application.
```
**Problem**: No specific bug identified, not actionable

```
Title: Issue with login
Description: Sometimes the login doesn't work properly.
```
**Problem**: Vague, no reproduction steps, no error details

## Research/Exploration Issues

### ✅ Good Examples

```
Title: Research authentication libraries for MVP
Description:
Need to pick auth solution for upcoming user system.
Evaluate: Auth0, Supabase Auth, Clerk, NextAuth
Consider: pricing, DX, time to implement, features needed

Output: Decision doc with recommendation
```

```
Title: Explore design options for project timeline view
Description:
Need to visualize projects on a timeline. Try different approaches:
- Gantt-style bars
- Card-based timeline
- Vertical timeline with milestones

Create 2-3 rough mockups for team feedback
```

### ❌ Bad Examples

```
Title: Research stuff
Description: Need to research some options for the project.
```
**Problem**: No scope, unclear deliverable

```
Title: As a PM, I want to research competitors so that we can build better features
```
**Problem**: User story format for a research task

## Design Issues

### ✅ Good Examples

```
Title: Design mobile navigation menu
Description:
Create mobile nav design that fits 6 main sections + user profile.
Consider: hamburger vs bottom nav, icon + label vs icon-only.

Deliverable: Figma screens showing opened/closed states
```

```
Title: Create empty state designs for all major views
Description:
Currently empty views show nothing - confusing for new users.
Design empty states for: Dashboard, Projects, Team, Settings.

Include: Illustration/icon, helpful text, CTA to add first item
```

### ❌ Bad Examples

```
Title: As a designer, I want to create beautiful designs
```
**Problem**: Not a task, no specific deliverable

```
Title: Design everything
Description: We need designs for the whole app
```
**Problem**: Too broad, should be multiple issues

## Chores/Technical Debt Issues

### ✅ Good Examples

```
Title: Upgrade React Router v5 → v6
Description:
React Router v6 has better performance and we need nested routes.
Update all Route declarations to new API.
Test critical flows: auth, onboarding, settings.
```

```
Title: Extract UserAvatar into shared component
Description:
UserAvatar logic is duplicated in 8 places with slight variations.
Extract to shared component in /components/shared/
Props: userId, size, showOnlineStatus
```

```
Title: Add error boundary to prevent white screen crashes
Description:
When components crash, users see blank white screen.
Add error boundary that shows "Something went wrong" message
with option to reload or contact support.
```

### ❌ Bad Examples

```
Title: Refactoring
Description: The codebase needs refactoring
```
**Problem**: No specific change, unclear scope

```
Title: Technical debt
Description: As a developer, I want to reduce technical debt so the codebase is maintainable
```
**Problem**: User story for technical work, not specific

## Documentation Issues

### ✅ Good Examples

```
Title: Document API authentication flow in README
Description:
New backend devs are confused about auth flow.
Add section to README covering:
- How JWT tokens are issued
- Token refresh process
- Where tokens are stored
- Example request with auth header
```

```
Title: Add JSDoc comments to all API route handlers
Description:
API routes lack documentation of params, responses, errors.
Add JSDoc to each route handler documenting:
- @param types and descriptions
- @returns shape of response
- @throws possible error codes
```

### ❌ Bad Examples

```
Title: Better documentation
Description: As a developer, I want better docs so I can understand the code
```
**Problem**: Vague, not specific about what to document

## Issue Sizing Guidelines

### Good Issue Sizes (1-3 days)

- Build one form
- Add one API endpoint
- Fix one specific bug
- Design one view
- Write one test suite
- Research one specific question
- Add one integration

### Too Large (Break Down)

- "Build authentication system" → Break into 8-10 issues
- "Redesign dashboard" → Break into view-by-view issues
- "Add analytics" → Break into events, tracking, reporting issues
- "Implement payments" → Break into Stripe setup, checkout flow, webhooks, etc.

### Too Small (Combine or Skip)

- "Change button color" → Part of larger styling issue
- "Fix typo" → Just do it, might not need issue
- "Update dependency" → Unless it requires testing, just do it

## When Issues Reference Each Other

### Using Sub-issues

```
Parent: Implement user onboarding flow
- Sub: Design onboarding screens
- Sub: Build step 1 (account setup)
- Sub: Build step 2 (profile creation)
- Sub: Build step 3 (team invitation)
- Sub: Add progress indicator
- Sub: Connect to backend API
```

### Blocking Relationships

```
Issue: Add team member invitation

Blocked by: 
- #123 (Email service integration)
- #124 (Team permissions system)

Description:
Can't send invites until email works.
Can't assign roles until permissions exist.
```

### Related Issues

```
Issue: Fix mobile layout on product page

Related:
- #145 (Similar mobile issue on checkout)
- #67 (Original mobile layout design)

Description:
Product images don't scale properly on mobile.
Similar to issue #145 - likely same root cause.
```

## User Feedback Integration

### Quoting Directly

✅ Good:
```
Title: Add dark mode

User feedback:
"I work late nights and the bright white background hurts my eyes. 
Would love a dark mode option!" - Sarah from Acme Corp

"Same here, dark mode would be amazing" - Mike from TechStart

Link to conversation: [Slack thread]
```

❌ Bad:
```
Title: Add dark mode
Description: Users want dark mode for better nighttime viewing experience
```
**Problem**: Lost authentic voice, no attribution, can't follow up

## Quick Reference

**Before writing an issue, ask:**
1. Is this a single, concrete task?
2. Can someone complete this in 1-3 days?
3. Is the outcome clear?
4. Would the assignee understand what to do?

**If unsure, it's probably:**
- Too big → Break it down
- Too vague → Add specifics
- Not a task → Move to project doc or discussion
