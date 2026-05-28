# Hiring Strategy - Validations

## User System Without Role Definitions

### **Id**
no-role-based-access
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - createUser|addUser|newUser
  - userRole|role.*user
### **Message**
User creation without role-based access control.
### **Fix Action**
Implement role-based permissions for team-based products
### **Applies To**
  - **/*.ts
  - **/*.tsx
### **Exceptions**
  - role|Role|admin|Admin|member|permission

## Team Product Without Invite System

### **Id**
no-invitation-system
### **Severity**
info
### **Type**
regex
### **Pattern**
  - team|Team|workspace|Workspace
  - organization|Organization
### **Message**
Team/org feature without visible invitation system.
### **Fix Action**
Add invite flow for team growth and PLG expansion
### **Applies To**
  - **/*.tsx
  - **/*.jsx
### **Exceptions**
  - invite|Invite|invitation|addMember

## User Creation Without Onboarding

### **Id**
no-onboarding-flow
### **Severity**
info
### **Type**
regex
### **Pattern**
  - signup|signUp|register|createAccount
### **Message**
User signup without onboarding flow.
### **Fix Action**
Add onboarding for activation and time-to-value
### **Applies To**
  - **/*.tsx
  - **/*.jsx
### **Exceptions**
  - onboarding|Onboarding|welcome|Welcome|getStarted

## Hardcoded Team Size Limits

### **Id**
hardcoded-team-limits
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - maxUsers.*=.*\d+
  - teamLimit.*=.*\d+
  - seatLimit.*=.*\d+
### **Message**
Hardcoded team limits. Consider configuration-based limits.
### **Fix Action**
Move team limits to configuration for pricing flexibility
### **Applies To**
  - **/*.ts
  - **/*.tsx
### **Exceptions**
  - config|Config|env|ENV|process\.env

## Team Feature Without Seat Tracking

### **Id**
no-seat-tracking
### **Severity**
info
### **Type**
regex
### **Pattern**
  - addMember|inviteMember|joinTeam
### **Message**
Team membership without seat tracking for billing.
### **Fix Action**
Track seat count for usage-based or per-seat billing
### **Applies To**
  - **/*.ts
  - **/*.tsx
### **Exceptions**
  - seat|Seat|billing|Billing|subscription

## Action Without Permission Check

### **Id**
no-permission-check
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - delete|Delete|remove|Remove
  - update|Update|edit|Edit
### **Message**
Destructive action without visible permission check.
### **Fix Action**
Add permission verification before destructive operations
### **Applies To**
  - **/api/**/*.ts
  - **/routes/**/*.ts
### **Exceptions**
  - permission|authorize|canDelete|isAdmin|hasAccess

## Admin Action Without Audit Log

### **Id**
no-audit-trail
### **Severity**
info
### **Type**
regex
### **Pattern**
  - admin|Admin|superuser
  - changeRole|updatePermission
### **Message**
Admin action without audit logging.
### **Fix Action**
Log admin actions for security and compliance
### **Applies To**
  - **/*.ts
  - **/*.tsx
### **Exceptions**
  - audit|log|track|record|history

## Team Event Without Notification

### **Id**
no-email-notifications
### **Severity**
info
### **Type**
regex
### **Pattern**
  - inviteMember|addToTeam|removeFromTeam
  - roleChange|permissionUpdate
### **Message**
Team change without email notification.
### **Fix Action**
Send notifications for team membership changes
### **Applies To**
  - **/*.ts
  - **/*.tsx
### **Exceptions**
  - email|notify|notification|sendEmail

## Remove User Without Offboarding

### **Id**
no-offboarding
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - removeUser|deleteUser|deactivateUser
  - removeMember|leaveTeam
### **Message**
User removal without data handling.
### **Fix Action**
Handle user data properly on removal (transfer, archive)
### **Applies To**
  - **/*.ts
  - **/*.tsx
### **Exceptions**
  - transfer|archive|reassign|offboard

## Enterprise Feature Without SSO

### **Id**
no-sso-support
### **Severity**
info
### **Type**
regex
### **Pattern**
  - enterprise|Enterprise|organization|Organization
### **Message**
Enterprise feature without visible SSO support.
### **Fix Action**
Plan SSO (SAML/OIDC) for enterprise readiness
### **Applies To**
  - **/*.ts
  - **/*.tsx
### **Exceptions**
  - sso|SSO|saml|SAML|oidc|OIDC

## User Actions Without Activity Log

### **Id**
no-activity-tracking
### **Severity**
info
### **Type**
regex
### **Pattern**
  - create|update|delete
  - submit|save|publish
### **Message**
User action without activity tracking.
### **Fix Action**
Track user activity for engagement analysis
### **Applies To**
  - **/*.ts
  - **/*.tsx
### **Exceptions**
  - activity|track|log|analytics|event

## Signup Without Welcome Email

### **Id**
no-welcome-email
### **Severity**
info
### **Type**
regex
### **Pattern**
  - signup|signUp|register|createUser
### **Message**
User signup without welcome email.
### **Fix Action**
Send welcome email to improve activation
### **Applies To**
  - **/*.ts
  - **/*.tsx
### **Exceptions**
  - welcome|sendEmail|notification|email

## Team Trial Without Management

### **Id**
no-trial-management
### **Severity**
info
### **Type**
regex
### **Pattern**
  - trial|Trial|freeTrial
  - trialStart|startTrial
### **Message**
Trial start without expiration management.
### **Fix Action**
Track and manage trial expiration and conversion
### **Applies To**
  - **/*.ts
  - **/*.tsx
### **Exceptions**
  - expir|end|convert|upgrade