---
id: wbs-creation
name: "Work Breakdown Structure (WBS)"
domain: PM
skill: faion-project-manager
category: "project-management"
---

# Work Breakdown Structure (WBS)

## Metadata
- **Category:** Project Management Framework / Planning Performance Domain
- **Difficulty:** Beginner
- **Tags:** #methodology #pmbok #wbs #planning #project-management
- **Agent:** faion-pm-agent

---

## Problem

Large projects feel overwhelming. You do not know where to start. Tasks are too big to estimate accurately. Team members understand the project differently. Important work gets forgotten until it is too late.

Without a WBS:
- Scope is unclear
- Estimates are wild guesses
- Dependencies hide until they block progress
- Nothing feels completable

---

## Framework

### What is a WBS?

A Work Breakdown Structure decomposes the total scope into smaller, manageable pieces.

**Key principles:**
- Hierarchical decomposition (big to small)
- Deliverable-oriented (what, not how)
- 100% rule (captures ALL work)
- Mutually exclusive elements

### Step 1: Start with Deliverables

Begin with the final product and major deliverables, not tasks.

**Wrong approach:** List activities (design, code, test)
**Right approach:** List outputs (user authentication, dashboard, reports)

### Step 2: Decompose Hierarchically

Break each deliverable into sub-deliverables:

```
Level 1: Project
    Level 2: Major Deliverables
        Level 3: Sub-deliverables
            Level 4: Work Packages
```

**Example:**
```
1. E-commerce Website
   1.1 User Management
       1.1.1 Registration System
       1.1.2 Login/Logout
       1.1.3 Profile Management
   1.2 Product Catalog
       1.2.1 Product Database
       1.2.2 Search Functionality
       1.2.3 Category Navigation
   1.3 Shopping Cart
       1.3.1 Cart Management
       1.3.2 Checkout Process
       1.3.3 Payment Integration
```

### Step 3: Apply the 100% Rule

Every level must capture 100% of work below it.

**Check:** If you complete all children, is the parent complete?

If anything is missing at any level, add it.

### Step 4: Define Work Packages

The lowest level items are work packages. They should be:

| Criteria | Guideline |
|----------|-----------|
| **Estimable** | Can assign hours/days |
| **Assignable** | One person or team |
| **Measurable** | Clear done criteria |
| **8/80 Rule** | Between 8-80 hours of effort |

### Step 5: Add WBS Dictionary

For each work package, document:

```markdown
**WBS ID:** 1.2.2
**Name:** Search Functionality
**Description:** Full-text search across products
**Deliverable:** Working search with filters
**Criteria:** Returns relevant results in < 2 seconds
**Owner:** Backend Team
**Estimate:** 40 hours
```

---

## Templates

### WBS Outline Template

```markdown
# WBS: [Project Name]

## 1. [Major Deliverable 1]
### 1.1 [Sub-deliverable]
#### 1.1.1 [Work Package]
#### 1.1.2 [Work Package]
### 1.2 [Sub-deliverable]
#### 1.2.1 [Work Package]
#### 1.2.2 [Work Package]

## 2. [Major Deliverable 2]
### 2.1 [Sub-deliverable]
...

## 3. Project Management
### 3.1 Planning
### 3.2 Monitoring
### 3.3 Closing
```

### WBS Dictionary Entry

```markdown
# WBS Dictionary Entry

| Field | Value |
|-------|-------|
| **WBS ID** | [X.X.X] |
| **Name** | [Work Package Name] |
| **Description** | [Detailed description] |
| **Deliverable** | [What is produced] |
| **Acceptance Criteria** | [How to verify complete] |
| **Owner** | [Person or team] |
| **Predecessor** | [Dependencies] |
| **Effort Estimate** | [Hours] |
| **Cost Estimate** | [$] |
| **Notes** | [Additional info] |
```

---

## Examples

### Example 1: Mobile App WBS

```
1. Fitness Tracking App
   1.1 Core Features
       1.1.1 Activity Tracking
       1.1.2 Goal Setting
       1.1.3 Progress Dashboard
   1.2 User System
       1.2.1 Authentication
       1.2.2 User Profile
       1.2.3 Settings
   1.3 Social Features
       1.3.1 Friend Connections
       1.3.2 Activity Sharing
       1.3.3 Leaderboards
   1.4 Technical Infrastructure
       1.4.1 Backend API
       1.4.2 Database Design
       1.4.3 Push Notifications
   1.5 Project Management
       1.5.1 Planning Phase
       1.5.2 Status Reporting
       1.5.3 Release Management
```

### Example 2: Marketing Campaign WBS

```
1. Product Launch Campaign
   1.1 Content Assets
       1.1.1 Landing Page
       1.1.2 Email Sequences
       1.1.3 Social Media Posts
       1.1.4 Blog Articles
   1.2 Advertising
       1.2.1 Facebook Ads
       1.2.2 Google Ads
       1.2.3 Influencer Partnerships
   1.3 Events
       1.3.1 Webinar Setup
       1.3.2 Demo Videos
   1.4 Analytics
       1.4.1 Tracking Setup
       1.4.2 Reporting Dashboard
```

---

## Common Mistakes

1. **Activity-oriented vs deliverable-oriented** - Focus on what is produced, not how
2. **Missing the 100% rule** - Forgetting project management, testing, documentation
3. **Going too deep** - More than 4-5 levels rarely needed
4. **Inconsistent levels** - Some branches detailed, others vague
5. **No WBS dictionary** - Numbers without definitions confuse everyone

---

## Visual Representations

### Tree Diagram
Best for presentations. Shows hierarchy visually.

### Outline Format
Best for documents. Easy to edit and update.

### Mind Map
Best for brainstorming. Generates ideas quickly.

### Spreadsheet
Best for tracking. Adds columns for estimates, owners, status.

---

## Next Steps

After creating your WBS:
1. Review with team and stakeholders
2. Add estimates to work packages
3. Sequence work packages for schedule
4. Connect to Schedule Development methodology

---

## References

- Project Management Framework Guide 7th Edition - Planning Performance Domain
- PM industry practice standard for Work Breakdown Structures
