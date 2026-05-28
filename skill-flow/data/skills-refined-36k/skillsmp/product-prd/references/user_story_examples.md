# User Story Examples & Best Practices

A comprehensive guide to writing effective user stories with real-world examples across different domains.

---

## Table of Contents

1. [User Story Format](https://www.google.com/search?q=%23user-story-format)
2. [Anatomy of Good User Stories](https://www.google.com/search?q=%23anatomy-of-good-user-stories)
3. [Examples by Domain](https://www.google.com/search?q=%23examples-by-domain)
4. [Acceptance Criteria Patterns](https://www.google.com/search?q=%23acceptance-criteria-patterns)
5. [Common Mistakes](https://www.google.com/search?q=%23common-mistakes)
6. [Splitting Stories](https://www.google.com/search?q=%23splitting-stories)

---

## User Story Format

### Standard Template

Here is the standard template for our user stories:

```
# User Story: [US Name]

> **Product:** [Product Name]
> **Author:** [Name]
> **Created on:** YYYY-MM-DD
> **Status:** Draft | Under Review | Approved | In Development | Delivered

---

## 1. Problem Description

Contextualize the business or technical problem this story solves. Be specific about the current impact (e.g., error rate, time lost, complaints) and the desired scenario after implementation.

## 2. Use Case

Describe a real or representative situation of a user facing the pain point. Include: who the user is, what they were trying to do, what went wrong, and how it affected them. This humanizes the problem and aligns the team on the motivation.

## 3. Definition of Ready (DoR)

These criteria tend to remain constant. They are checkboxes to ensure the story is ready for development.

- [ ] Clear and unambiguous requirements
- [ ] Approved prototypes/wireframes (if applicable)
- [ ] Acceptance criteria defined and validated with stakeholders
- [ ] Effort estimation completed by the team

## 4. Acceptance Criteria

Specific expectations that define the correct behavior of the feature, written from the user's perspective. Here, we define what determines that the task is complete.

- [ ] Given [initial context], when [user action], then [expected result]
- [ ] Error scenarios and edge cases covered
- [ ] Performance requirements (if applicable)

## 5. Definition of Done (DoD)

These criteria tend to remain constant. They are checkboxes to ensure the story is truly complete in all its dimensions, not just code-wise:

- [ ] Code reviewed (approved code review)
- [ ] Automated tests implemented (unit/integration)
- [ ] Documentation updated (API, README, Notion)
- [ ] Deployment to staging environment validated
- [ ] Story stakeholders notified / release notes written


```

---

## Anatomy of Good User Stories

### INVEST Criteria

Good user stories are:

- **Independent:** Can be developed and delivered separately
- **Negotiable:** Details can be discussed and adjusted
- **Valuable:** Deliver clear value to users or the business
- **Estimable:** Can be sized/estimated by the team
- **Small:** Can be completed in one iteration/sprint
- **Testable:** Have clear acceptance criteria

### Key Components

1. **User Type:** Who is the user? Be specific.
2. **Action:** What do they want to do? A clear action.
3. **Value:** Why do they want it? The benefit or result.
4. **Acceptance Criteria:** How do we know it's ready? Testable conditions.

---

## Examples by Domain

### E-Commerce

#### Example 1: Product Search

**User Story:**

```
As an online shopper,
I want to filter products by price range,
So that I can find items within my budget.

```

**Acceptance Criteria:**

- [ ] Given I am on the product listing page, when I set a minimum and maximum price, then only products within that range are displayed.
- [ ] Given I have applied a price filter, when I clear the filter, then all products are shown again.
- [ ] Given I set an invalid price range (min > max), when I apply the filter, then I see an error message.
- [ ] Price filter persists when navigating between results pages.
- [ ] Filter displays the count of products matching the criteria.

**Priority:** High

---

#### Example 2: Guest Checkout

**User Story:**

```
As a first-time customer,
I want to check out without creating an account,
So that I can complete my purchase quickly.

```

**Acceptance Criteria:**

- [ ] Given I have items in the cart, when I click on checkout, then I see options for "Guest Checkout" and "Log In".
- [ ] Given I choose guest checkout, when I enter shipping and payment information, then I can complete the order.
- [ ] Given I complete a guest checkout, when the order is placed, then I receive a confirmation email.
- [ ] After guest checkout, I see an option to create an account using my order information.
- [ ] Guest checkout flow takes a maximum of 3 screens.

**Priority:** High

---

### SaaS / B2B Platform

#### Example 3: Team Collaboration

**User Story:**

```
As a project manager,
I want to assign tasks to team members,
So that everyone knows their responsibilities.

```

**Acceptance Criteria:**

- [ ] Given I am viewing a task, when I click "Assign," then I see a list of team members.
- [ ] Given I select a team member, when I confirm the assignment, then they receive a notification.
- [ ] Given a task is assigned, when I view the task list, then I can see who is assigned to each task.
- [ ] Given I am a team member, when I am assigned to a task, then it appears in my "My Tasks" view.
- [ ] I can assign multiple people to a single task.
- [ ] I can change or remove task assignments.

**Priority:** High

---

#### Example 4: Usage Analytics

**User Story:**

```
As a SaaS administrator,
I want to view team usage analytics,
So that I can optimize our subscription plan.

```

**Acceptance Criteria:**

- [ ] Given I have admin permissions, when I navigate to analytics, then I see usage metrics for the last 30 days.
- [ ] Dashboard shows: active users, feature usage, API calls, and storage used.
- [ ] Given I select a date range, when I apply the filter, then metrics update accordingly.
- [ ] I can export analytics data as a CSV.
- [ ] Metrics update in real-time (maximum 5-minute delay).

**Priority:** High

---

### Mobile App

#### Example 5: Push Notifications

**User Story:**

```
As a mobile app user,
I want to customize which notifications I receive,
So that I only see relevant updates.

```

**Acceptance Criteria:**

- [ ] Given I am in settings, when I navigate to notifications, then I see toggles for each notification type.
- [ ] Notification types include: messages, mentions, updates, promotions.
- [ ] Given I disable a notification type, when that event occurs, then I do not receive a push notification.
- [ ] Settings sync across devices using the same account.
- [ ] Default settings are: messages ON, mentions ON, updates ON, promotions OFF.

**Priority:** High

---

#### Example 6: Offline Mode

**User Story:**

```
As a mobile user with unstable connectivity,
I want to access my recently viewed content offline,
So that I can continue using the app without internet.

```

**Acceptance Criteria:**

- [ ] Given I viewed content while online, when I go offline, then I can still access the last 50 viewed items.
- [ ] Given I am offline, when I try to access new content, then I see a "No connection" message with cached content.
- [ ] Given I am offline and make changes, when I reconnect, then changes sync automatically.
- [ ] Offline indicator appears in the app when connectivity is lost.
- [ ] Cached content is automatically cleared after 7 days.

**Priority:** High

---

### Authentication & Security

#### Example 7: Two-Factor Authentication

**User Story:**

```
As a security-conscious user,
I want to enable two-factor authentication,
So that my account is protected from unauthorized access.

```

**Acceptance Criteria:**

- [ ] Given I am in security settings, when I enable 2FA, then I can choose between SMS and an authenticator app.
- [ ] Given I choose an authenticator app, when I scan the QR code, then I must enter a verification code to activate.
- [ ] Given 2FA is enabled, when I log in, then I am prompted for my second factor.
- [ ] I receive backup codes when I activate 2FA.
- [ ] I can disable 2FA with my current password + 2FA code.

**Priority:** High

---

#### Example 8: Password Reset

**User Story:**

```
As a user who forgot my password,
I want to reset it via email,
So that I can regain access to my account.

```

**Acceptance Criteria:**

- [ ] Given I click on "Forgot Password," when I enter my email, then I receive a reset link within 5 minutes.
- [ ] Reset link expires after 24 hours.
- [ ] Given I click the reset link, when I enter a new password, then it must meet the password requirements (shown on screen).
- [ ] After a successful reset, I am logged in automatically.
- [ ] If the email does not exist in the system, show a generic message (do not reveal if the account exists).

**Priority:** High

---

### Content & Media

#### Example 9: Video Upload

**User Story:**

```
As a content creator,
I want to upload videos with progress tracking,
So that I know when my upload is complete.

```

**Acceptance Criteria:**

- [ ] Given I select a video file, when I click upload, then I see a progress bar showing percentage complete.
- [ ] Supported formats: MP4, MOV, AVI (max 2GB).
- [ ] Given an upload is in progress, when I navigate away, then the upload continues in the background.
- [ ] Given the upload completes, when processing finishes, then I receive a notification.
- [ ] Given the upload fails, when an error occurs, then I see a specific error message and can try again.

**Priority:** High

---

### Admin & Configuration

#### Example 10: User Permissions

**User Story:**

```
As an administrator,
I want to assign role-based permissions to users,
So that team members have appropriate access levels.

```

**Acceptance Criteria:**

- [ ] Given I am viewing a user profile, when I click "Change Role," then I see available roles: Admin, Editor, Viewer.
- [ ] Given I assign a role, when I save, then the user immediately gains/loses associated permissions.
- [ ] Admin: full access; Editor: create/edit content; Viewer: read-only.
- [ ] I can create custom roles with specific combinations of permissions.
- [ ] Audit log records all permission changes with a timestamp and the admin who made the change.

**Priority:** High

---

## Acceptance Criteria Patterns

### Given-When-Then Format

A more structured format, excellent for complex logic:

```
Given [initial context/state],
When [action/event],
Then [expected result].

```

**Example:**

```
Given I am a logged-in user with items in my cart,
When I apply a 20% discount code,
Then the cart total is reduced by 20% and displays the discount.

```

### Checklist Format

Simpler, good for direct requirements:

```
- [ ] Requirement 1
- [ ] Requirement 2
- [ ] Edge case handling

```

### Table Format

Great for multiple scenarios:

| Condition     | Action       | Expected Result        |
| ------------- | ------------ | ---------------------- |
| Valid email   | Click "Send" | Confirmation message   |
| Invalid email | Click "Send" | Error message          |
| Empty field   | Click "Send" | "Required field" error |

---

## Common Mistakes to Avoid

### ❌ Too Technical

**Bad:**

```
As a user,
I want the system to use Redis cache with a 10-minute TTL,
So that page loads are fast.

```

**Good:**

```
As a user,
I want pages to load in less than 2 seconds,
So that I can navigate efficiently.

```

**Why:** User stories focus on user value, not implementation. Let engineers choose the solution.

---

### ❌ Too Vague

**Bad:**

```
As a user,
I want the app to be fast,
So that I have a good experience.

```

**Good:**

```
As a user,
I want search results to appear in less than 1 second,
So that I can quickly find what I need.

```

**Why:** "Fast" is subjective. Be specific and measurable.

---

### ❌ Missing the "Why"

**Bad:**

```
As a user,
I want to upload profile photos.

```

**Good:**

```
As a user,
I want to upload a profile photo,
So that other users can recognize me in the community.

```

**Why:** Understanding the "why" helps the team make better decisions.

---

### ❌ Multiple Actions in One Story

**Bad:**

```
As a user,
I want to create an account, set up my profile, and invite team members,
So that I can start using the platform.

```

**Good:** Split into three stories:

```
Story 1: As a user, I want to create an account...
Story 2: As a user, I want to set up my profile...
Story 3: As an account owner, I want to invite team members...

```

**Why:** Stories should be small and focused on one capability.

---

### ❌ No Acceptance Criteria

**Bad:**

```
As a user,
I want to search for products,
So that I can find what I need.

```

**Good:** Add specific criteria:

```
Acceptance Criteria:
- [ ] Search works on product name and description.
- [ ] Results display in less than 2 seconds.
- [ ] Displays "No results found" when there are no matches.
- [ ] Shows top 20 results with pagination.

```

**Why:** Acceptance criteria define "done" and enable testing.

---

## Story Splitting Techniques

When a story is too large, use these techniques to split it:

### 1. By Workflow Steps

**Large Story:**

```
As a user, I want to book a flight online.

```

**Split Stories:**

- Search for flights
- Select flight
- Enter passenger data
- Choose seat
- Make payment
- Receive confirmation

---

### 2. By User Persona

**Large Story:**

```
As a user, I want to manage my subscriptions.

```

**Split Stories:**

- As a free user, I want to see available plans.
- As a paid user, I want to upgrade my plan.
- As an admin, I want to manage team subscriptions.

---

### 3. By Business Rules

**Large Story:**

```
As a user, I want to apply discount codes.

```

**Split Stories:**

- Apply percentage discount (e.g., 20% off)
- Apply fixed amount discount (e.g., $10 off)
- Apply free shipping discount
- Handle expired discount codes
- Limit one discount per order

---

### 4. By Data Variations

**Large Story:**

```
As a user, I want to import contacts.

```

**Split Stories:**

- Import from CSV file
- Import from Google Contacts
- Import from Microsoft Outlook
- Import from LinkedIn

---

### 5. By CRUD Operations

**Large Story:**

```
As a user, I want to manage my projects.

```

**Split Stories:**

- Create a new project
- View project details
- Update project settings
- Delete a project

---

### 6. By Happy Path / Edge Cases

**MVP Story (Happy Path):**

```
As a user, I want to upload a profile photo (JPG, < 5MB).

```

**Follow-up Stories:**

- Support additional formats (PNG, GIF)
- Handle files larger than 5MB with an error message
- Auto-crop/resize images
- Allow photo deletion

---

## Story Sizing Guidelines

**1-2 Points (A few hours):**

- Simple UI change
- Copy update
- Minor configuration

**3-5 Points (1-2 days):**

- New form with validation
- Simple API endpoint
- Basic feature toggle

**8 Points (3-5 days):**

- Complex form with business logic
- Integration with third-party service
- New database schema with migration

**13+ Points (1+ weeks):**

- Too large! Split the story.
- Consider it an Epic.

---

## Templates for Common Scenarios

### Registration/Sign-Up

```
As a new visitor,
I want to create an account with my email,
So that I can access personalized features.

Acceptance Criteria:
- [ ] Email and password required (password: min 8 characters, 1 number, 1 special character).
- [ ] Email validation and duplicate check.
- [ ] Confirmation email sent after registration.
- [ ] Automatically logged in after email confirmation.
- [ ] Option to register with Google/Apple (social auth).

```

### Data Export

```
As a user,
I want to export my data as a CSV,
So that I can analyze it in Excel.

Acceptance Criteria:
- [ ] Export button in settings.
- [ ] Includes all user data (specify fields).
- [ ] File downloads immediately (or email if > 10MB).
- [ ] Filename format: "export_[username]_[date].csv".
- [ ] Respects data privacy regulations (only user's own data).

```

### Error Handling

```
As a user,
I want to see helpful error messages,
So that I know how to fix problems.

Acceptance Criteria:
- [ ] Error messages are specific (not generic "An error occurred").
- [ ] Suggest actionable next steps.
- [ ] Display in the user's language.
- [ ] Do not expose technical details (stack traces).
- [ ] Log errors for debugging (backend).

```

---

## Best Practices Summary

1. **Write from the user's perspective**, not the system's.
2. **Focus on value/benefit**, not just functionality.
3. **Keep stories small** (completable in one sprint).
4. **Make acceptance criteria testable**.
5. **Use a consistent format** across your team.
6. **Include edge cases** in the acceptance criteria.
7. **Collaborate** with engineers and designers when writing.
8. **Refine regularly** based on new learnings.
9. **Link to mockups/designs** when relevant.
10. **Prioritize ruthlessly** (must/should/nice-to-have).

---

## Additional Resources

### User Story Template

```
Title: [Concise feature name]

As a [specific user type],
I want to [action/capability],
So that [benefit/value].

Acceptance Criteria:
- [ ] [Testable criterion 1]
- [ ] [Testable criterion 2]
- [ ] [Edge case handling]

Priority: [Urgent / High / Medium / Low / No Priority]

Dependencies: [List if any]
Design: [Link to mockups]
Notes: [Additional context]

```

### Epic vs Story vs Task

**Epic:** Large body of work (multiple sprints)

- Example: "User Authentication System"

**Story:** Deliverable value (one sprint)

- Example: "As a user, I want to reset my password..."

**Task:** Implementation step (hours/days)

- Example: "Create password reset API endpoint"

---

## Conclusion

Effective user stories:

- Start with the user's perspective
- Articulate value clearly
- Include testable acceptance criteria
- Are sized appropriately
- Enable team collaboration

## Use these examples as templates, but adapt them to your product and the specific needs of your users!

**Would you like me to translate any more templates or perhaps help you refine a specific story you're working on?**
