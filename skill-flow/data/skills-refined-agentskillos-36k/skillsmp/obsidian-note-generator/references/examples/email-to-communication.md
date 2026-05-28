# Example: Email to Communication Note

## Input

```
From: john.smith@vendor.com
To: charles.roberts@miami.edu
Subject: RE: SubjectsPlus5 API Integration Timeline
Date: January 22, 2025 2:34 PM

Hi Charles,

Thanks for the call yesterday. As discussed, we can have the API endpoints ready by February 15th. 

The authentication will use OAuth 2.0 with the following scopes:
- read:guides
- write:guides
- admin:settings

We'll need the redirect URI for your staging environment to proceed with testing.

Action items from our side:
- Send API documentation by Jan 31
- Set up sandbox environment
- Schedule technical walkthrough

Let me know if you have any questions.

Best,
John
```

## Skill Analysis

```yaml
Classification:
  Template: Communication
  Subtype: email
  Confidence: 95%
  
Signals Detected:
  Strong: "From:", "To:", "Subject:", "RE:"
  Medium: "email" (implied)
  
Project Detection:
  Detected: "SubjectsPlus5"
  Confidence: 100%
  Tag: "#Project/SubjectsPlus5"
  
Extracted Metadata:
  date: 2025-01-22
  participants: [john.smith@vendor.com, charles.roberts@miami.edu]
  topic: SubjectsPlus5 API Integration Timeline
  status: open
  action-items:
    - "Send API documentation by Jan 31"
    - "Set up sandbox environment"
    - "Schedule technical walkthrough"
```

## Output

**Filename**: `2025-01-22-sp5-api-integration-timeline.md`
**Suggested Location**: `10-Projects/SubjectsPlus5/Communications/Emails/`

```markdown
---
type: email
date: 2025-01-22
participants:
  - john.smith@vendor.com
  - charles.roberts@miami.edu
project: SubjectsPlus5
topic: SubjectsPlus5 API Integration Timeline
status: open
action-items:
  - Send API documentation by Jan 31
  - Set up sandbox environment
  - Schedule technical walkthrough
tags:
  - Type/Communication
  - Project/SubjectsPlus5
---

# SP5 API Integration Timeline

## Summary

Vendor confirmation of API integration timeline for SubjectsPlus5. API endpoints will be ready by February 15th using OAuth 2.0 authentication.

## Details

### Timeline
- API endpoints ready: February 15, 2025
- API documentation: January 31, 2025

### Authentication
OAuth 2.0 with scopes:
- `read:guides`
- `write:guides`
- `admin:settings`

### Requirements
- Staging environment redirect URI needed for testing

## Action Items

- [ ] Send API documentation by Jan 31 (Vendor)
- [ ] Set up sandbox environment (Vendor)
- [ ] Schedule technical walkthrough (Vendor)
- [ ] Provide staging redirect URI (Us)

## Follow-up

Schedule technical walkthrough after receiving API documentation.
```
