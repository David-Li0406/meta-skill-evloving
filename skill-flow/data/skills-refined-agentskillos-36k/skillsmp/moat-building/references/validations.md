# Moat Building - Validations

## Social Feature Without Sharing

### **Id**
missing-viral-hooks
### **Severity**
info
### **Type**
regex
### **Pattern**
  - social|Social|community|Community
  - collaboration|Collaboration
  - team|Team|workspace
### **Message**
Social/collaborative feature found. Consider adding sharing and invite mechanics.
### **Fix Action**
Add invite flows, sharing buttons, and viral loops to collaborative features
### **Applies To**
  - **/*.tsx
  - **/*.jsx
### **Exceptions**
  - share|Share|invite|Invite|referral

## User Action Without Data Capture

### **Id**
no-data-persistence
### **Severity**
info
### **Type**
regex
### **Pattern**
  - onClick|onSubmit|handleClick
  - user.*action
### **Message**
User action handler without visible analytics/data capture.
### **Fix Action**
Ensure valuable user actions are logged for future ML/personalization
### **Applies To**
  - **/*.tsx
  - **/*.jsx
### **Exceptions**
  - track|log|analytics|capture

## Proprietary Format Without Export

### **Id**
exportable-data-format
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - proprietary.*format
  - custom.*format
  - \.myapp|\.internal
### **Message**
Proprietary format detected. Ensure ethical export option exists.
### **Fix Action**
Provide standard format export (CSV, JSON, etc.) alongside proprietary
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js

## Product Without Integration Points

### **Id**
no-integration-api
### **Severity**
info
### **Type**
regex
### **Pattern**
  - export default.*App
  - createRoot|render\(
### **Message**
Main app without visible API/integration layer. Consider for switching costs.
### **Fix Action**
Add webhook, API, or integration capabilities for deeper customer embedding
### **Applies To**
  - **/App.tsx
  - **/index.tsx
  - **/main.tsx
### **Exceptions**
  - api|API|webhook|integration

## Single-User Focus Without Team Features

### **Id**
single-user-only
### **Severity**
info
### **Type**
regex
### **Pattern**
  - user\s*=|currentUser|getUser
### **Message**
Single-user patterns found. Consider team/org features for network effects.
### **Fix Action**
Plan team features: shared workspaces, permissions, collaboration
### **Applies To**
  - **/*.ts
  - **/*.tsx
### **Exceptions**
  - team|org|organization|member|workspace

## User Signup Without Referral Tracking

### **Id**
no-referral-system
### **Severity**
info
### **Type**
regex
### **Pattern**
  - signup|signUp|register|createUser
### **Message**
User signup without referral tracking. Missing viral loop opportunity.
### **Fix Action**
Add referral code tracking and attribution for viral growth
### **Applies To**
  - **/*.ts
  - **/*.tsx
### **Exceptions**
  - referral|refer|invite|attribution

## Feature Without Usage History

### **Id**
no-usage-history
### **Severity**
info
### **Type**
regex
### **Pattern**
  - save|Save|create|Create|submit|Submit
### **Message**
Create/save action without history accumulation.
### **Fix Action**
Store user history/activity for personalization and switching cost depth
### **Applies To**
  - **/*.ts
  - **/*.tsx
### **Exceptions**
  - history|log|activity|audit

## Content Display Without Personalization

### **Id**
no-personalization
### **Severity**
info
### **Type**
regex
### **Pattern**
  - getAll|findAll|listAll
  - fetch.*all
### **Message**
Generic content fetch without personalization. Data moat opportunity.
### **Fix Action**
Add user preference/behavior-based personalization for data network effects
### **Applies To**
  - **/*.ts
  - **/*.tsx
### **Exceptions**
  - recommend|personalize|preference|score

## Core Feature Without Extension Points

### **Id**
missing-platform-hooks
### **Severity**
info
### **Type**
regex
### **Pattern**
  - export.*function|export.*const
  - class.*export
### **Message**
Core functionality without extension points. Platform moat opportunity.
### **Fix Action**
Consider plugin architecture, webhooks, or API for platform network effects
### **Applies To**
  - **/core/**/*.ts
  - **/lib/**/*.ts
### **Exceptions**
  - plugin|hook|extension|middleware

## Standard Format Without Lock-in

### **Id**
easy-migration-pattern
### **Severity**
info
### **Type**
regex
### **Pattern**
  - import.*csv|export.*csv
  - import.*json|export.*json
  - standard.*format
### **Message**
Standard format usage. Good for ethics, consider proprietary value-add layer.
### **Fix Action**
Balance: Standard format export + proprietary features/integrations
### **Applies To**
  - **/*.ts
  - **/*.tsx

## User-Generated Content Without Community

### **Id**
no-community-features
### **Severity**
info
### **Type**
regex
### **Pattern**
  - upload|post|publish|share
  - content.*create
### **Message**
User content creation without community features.
### **Fix Action**
Add comments, likes, follows, or reputation for social network effects
### **Applies To**
  - **/*.tsx
  - **/*.jsx
### **Exceptions**
  - comment|like|follow|community|social

## Utility Without Workflow Integration

### **Id**
no-embedded-workflows
### **Severity**
info
### **Type**
regex
### **Pattern**
  - utility|tool|helper
  - standalone.*app
### **Message**
Standalone utility pattern. Consider workflow embedding for switching costs.
### **Fix Action**
Integrate into customer workflows via integrations, plugins, or APIs
### **Applies To**
  - **/*.ts
  - **/*.tsx
### **Exceptions**
  - workflow|integrate|embed|plugin

## Feature Launch Without Competitive Context

### **Id**
competitive-analysis-missing
### **Severity**
info
### **Type**
regex
### **Pattern**
  - launchFeature|releaseFeature|newFeature
  - feature.*flag
### **Message**
Feature launch detected. Ensure competitive moat assessment.
### **Fix Action**
Document how this feature affects competitive positioning and moat strength
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/feature*