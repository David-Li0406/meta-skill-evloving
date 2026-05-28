# Team Communications - Validations

## Application Without Documentation Link

### **Id**
no-documentation-system
### **Severity**
info
### **Type**
regex
### **Pattern**
  - README|readme|docs|documentation
  - onboarding|setup|getting-started
### **Message**
Documentation reference without clear internal docs system.
### **Fix Action**
Ensure internal documentation is organized and linked from main project
### **Applies To**
  - **/README.md
  - **/*.md
### **Exceptions**
  - notion\.so|confluence|gitbook|docs\.

## Project Without Team Communication Channel

### **Id**
no-team-channel-reference
### **Severity**
info
### **Type**
regex
### **Pattern**
  - slack|Slack|teams|Teams|discord|Discord
### **Message**
Communication tool reference without specific channel guidance.
### **Fix Action**
Document which channels to use for what purposes
### **Applies To**
  - **/README.md
  - **/CONTRIBUTING.md
### **Exceptions**
  - #team|#project|channel-name|channel-guide

## Meeting System Without Notes Template

### **Id**
no-meeting-notes-structure
### **Severity**
info
### **Type**
regex
### **Pattern**
  - meeting|Meeting|standup|Standup
  - agenda|Agenda|sync|Sync
### **Message**
Meeting references without notes structure.
### **Fix Action**
Add meeting notes template with decisions, actions, and attendees
### **Applies To**
  - **/*.md
  - **/*.yaml
### **Exceptions**
  - notes|decisions|action.*items|attendees

## Code Decision Without Documentation

### **Id**
undocumented-decision
### **Severity**
info
### **Type**
regex
### **Pattern**
  - // TODO:|// FIXME:|// HACK:|// XXX:
  - # TODO:|# FIXME:|# HACK:
### **Message**
Code decision markers without linked documentation.
### **Fix Action**
Document significant decisions in ADR or decision log
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.py
### **Exceptions**
  - ADR|decision.*log|documented.*in|see.*docs

## Hardcoded Team Contact Information

### **Id**
hardcoded-team-info
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - @\w+\.com|email.*=.*@
  - contact.*=.*\w+@
### **Message**
Hardcoded email addresses will become stale.
### **Fix Action**
Use role-based addresses or links to team directory
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.md
### **Exceptions**
  - noreply|no-reply|team@|support@|example\.com

## Error Handling Without Escalation Info

### **Id**
no-escalation-path
### **Severity**
info
### **Type**
regex
### **Pattern**
  - throw new Error|raise|panic
  - critical|fatal|emergency
### **Message**
Critical error handling without escalation guidance.
### **Fix Action**
Document who to contact for critical issues
### **Applies To**
  - **/*.ts
  - **/*.tsx
### **Exceptions**
  - oncall|pagerduty|opsgenie|escalate|notify

## Version Updates Without Changelog

### **Id**
no-changelog
### **Severity**
info
### **Type**
regex
### **Pattern**
  - version.*:\s*['"]\d
  - "version":\s*"\d
### **Message**
Version number without changelog for team visibility.
### **Fix Action**
Maintain CHANGELOG.md for team awareness of changes
### **Applies To**
  - **/package.json
  - **/pyproject.toml
### **Exceptions**
  - CHANGELOG|changelog|HISTORY|release-notes

## Setup Instructions Without Onboarding Link

### **Id**
no-onboarding-reference
### **Severity**
info
### **Type**
regex
### **Pattern**
  - npm install|yarn|pnpm|pip install
  - getting started|setup|installation
### **Message**
Setup instructions without link to full onboarding.
### **Fix Action**
Link setup instructions to comprehensive onboarding documentation
### **Applies To**
  - **/README.md
### **Exceptions**
  - onboarding|new.*hire|getting.*started.*guide

## Slack Link That Will Expire

### **Id**
slack-link-in-code
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - slack\.com/archives
  - app\.slack\.com/.*
### **Message**
Slack links expire and lose context over time.
### **Fix Action**
Document information in permanent location, not just Slack
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.md
### **Exceptions**
  - also.*documented|see.*wiki|captured.*in

## Documentation Without Owner

### **Id**
no-owner-in-docs
### **Severity**
info
### **Type**
regex
### **Pattern**
  - # |## |### 
### **Message**
Documentation without clear ownership for maintenance.
### **Fix Action**
Add document owner and last-updated date to all docs
### **Applies To**
  - **/docs/**/*.md
  - **/wiki/**/*.md
### **Exceptions**
  - owner:|maintained.*by:|last.*updated:|updated:

## Reference to Potentially Outdated Process

### **Id**
outdated-process-reference
### **Severity**
info
### **Type**
regex
### **Pattern**
  - our process|the process|current process
  - we usually|we typically|we always
### **Message**
Process reference may become outdated without versioning.
### **Fix Action**
Link to authoritative process documentation
### **Applies To**
  - **/*.md
### **Exceptions**
  - see.*process|process.*doc|link.*to|documented.*at

## Sync Requirement Without Async Option

### **Id**
no-async-alternative
### **Severity**
info
### **Type**
regex
### **Pattern**
  - schedule.*meeting|book.*time|set up.*call
  - we need to meet|let's sync
### **Message**
Sync-first communication without async alternative.
### **Fix Action**
Provide async options alongside sync when possible
### **Applies To**
  - **/*.md
  - **/README.md
### **Exceptions**
  - async|loom|video.*message|document.*first

## Time Reference Without Timezone

### **Id**
no-timezone-consideration
### **Severity**
info
### **Type**
regex
### **Pattern**
  - \d{1,2}:\d{2}|\d{1,2}(am|pm|AM|PM)
  - at \d|by \d
### **Message**
Time reference without timezone for distributed teams.
### **Fix Action**
Include timezone or use relative time for distributed teams
### **Applies To**
  - **/*.md
### **Exceptions**
  - UTC|PST|EST|timezone|time.*zone|local.*time

## ADR/Decision Without Logging System

### **Id**
no-decision-log
### **Severity**
info
### **Type**
regex
### **Pattern**
  - we decided|decision.*made|chose.*to
  - after.*discussion|team.*agreed
### **Message**
Decision reference without link to decision log.
### **Fix Action**
Maintain decision log or ADRs for team reference
### **Applies To**
  - **/*.md
### **Exceptions**
  - ADR|adr|decision.*log|decision.*record