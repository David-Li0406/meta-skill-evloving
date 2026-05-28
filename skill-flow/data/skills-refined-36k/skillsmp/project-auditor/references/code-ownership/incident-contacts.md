<!--
Copyright (c) 2025 Crash Override Inc. - https://crashoverride.com

SPDX-License-Identifier: GPL-3.0
-->

# Incident Response Contacts

## Overview

Zero's code ownership scanner generates "who to contact" information for incident response and developer collaboration. This feature answers the critical question: "If something breaks in this code, who should I call?"

## Use Cases

### 1. Incident Response
When a production issue occurs, quickly identify:
- Who wrote/maintains the affected code
- Who reviews changes in this area
- Backup contacts if primary is unavailable

### 2. Developer Collaboration
When working on unfamiliar code:
- Find subject matter experts
- Identify who to ask questions
- Locate code reviewers for your PRs

### 3. Knowledge Transfer
When onboarding or offboarding:
- Document tribal knowledge holders
- Plan knowledge transfer sessions
- Identify single points of failure

## Contact Types

### Primary Contacts
Top-ranked experts for a given path based on:
- Highest ownership score
- Active status (recently contributing)
- Combined expertise and availability

### Backup Contacts
Secondary experts providing redundancy:
- Next-highest ownership scores
- May have less recent activity
- Important for coverage during PTO/incidents

## Scoring Methodology

### Expertise Score (60% of ranking)
Derived from ownership score:
```
expertise_score = ownership_score / 100
```

Range: 0.0 - 1.0

### Availability Score (40% of ranking)
Based on activity status:

| Activity Status | Availability Score |
|----------------|-------------------|
| Active | 1.0 |
| Recent | 0.8 |
| Stale | 0.5 |
| Inactive | 0.2 |
| Abandoned | 0.0 |

### Combined Score
```
combined_score = (expertise_score * 0.6) + (availability_score * 0.4)
```

## Output Format

```json
{
  "incident_contacts": [
    {
      "path": "src/auth/",
      "primary": [
        {
          "name": "Alice Developer",
          "email": "alice@example.com",
          "expertise_score": 0.87,
          "availability_score": 0.95,
          "reason_for_contact": "high ownership score, recently active"
        }
      ],
      "backup": [
        {
          "name": "Bob Engineer",
          "email": "bob@example.com",
          "expertise_score": 0.65,
          "availability_score": 0.88,
          "reason_for_contact": "frequent reviewer"
        }
      ],
      "codeowners_match": {
        "pattern": "src/auth/**",
        "owners": ["@security-team"]
      }
    }
  ]
}
```

## Key Paths

Zero automatically generates contacts for critical paths:

| Path Pattern | Purpose |
|-------------|---------|
| `src/` | Main source code |
| `pkg/` | Go packages |
| `lib/` | Shared libraries |
| `api/` | API endpoints |
| `auth/` | Authentication code |
| `security/` | Security-sensitive code |
| `.github/workflows/` | CI/CD pipelines |
| `deploy/` | Deployment configurations |
| `infrastructure/` | IaC and infra code |
| `database/` | Database schemas/migrations |

## CODEOWNERS Integration

When CODEOWNERS defines owners for a path, Zero includes this information:

```json
{
  "codeowners_match": {
    "pattern": "src/auth/**",
    "owners": ["@security-team", "@auth-lead"]
  }
}
```

This helps teams understand both:
1. **Declared ownership**: What CODEOWNERS says
2. **Actual ownership**: Who really works on the code

Discrepancies indicate potential **ownership drift**.

## Reason Classification

Each contact includes a human-readable reason:

| Reason | Description |
|--------|-------------|
| `high ownership score` | Score >= 50 |
| `recently active` | Status is "active" |
| `frequent reviewer` | 10+ PR reviews given |
| `contributor to this codebase` | Default if no specific reason |

## Configuration

```json
{
  "contacts": {
    "enabled": true,
    "min_primary": 1,
    "min_backup": 1
  }
}
```

- `min_primary`: Minimum primary contacts per path (default: 1)
- `min_backup`: Minimum backup contacts per path (default: 1)

## Best Practices

### 1. Review Contact Lists Regularly
- Quarterly review of generated contacts
- Validate that contacts are still accurate
- Update when team composition changes

### 2. Integrate with Incident Management
- Import contacts into PagerDuty/OpsGenie
- Update runbooks with contact information
- Include in incident response playbooks

### 3. Use for On-Call Rotation
- Primary contacts for first-line on-call
- Backup contacts for escalation
- Distribute load across active contributors

### 4. Address Low Coverage
- Paths with only one contact need attention
- Cross-train team members on critical code
- Document tribal knowledge

### 5. Track Changes Over Time
- Monitor when primary contacts change
- Detect when expertise leaves the team
- Plan proactive knowledge transfer

## Example Workflow

### During an Incident

1. **Identify affected path**: `src/payments/processor.go`
2. **Query contacts**: Look up incident contacts for `src/payments/`
3. **Page primary**: Contact Alice (expertise: 0.87, available)
4. **Escalate if needed**: Contact Bob (backup)
5. **Check CODEOWNERS**: Verify `@payments-team` is engaged

### During Development

1. **Find experts**: Query contacts for code you're modifying
2. **Request review**: Add primary contacts as reviewers
3. **Ask questions**: Reach out to experts for guidance
4. **Document**: Update contacts if ownership changes

## Limitations

1. **No Real-Time Availability**: Cannot check PTO/calendar
2. **Email May Be Outdated**: Git email may differ from current
3. **Role Changes**: People may have moved to different teams
4. **Part-Time Contributors**: External contributors may not be reachable

## Integration Points

### Slack
```
/who-owns src/auth/
> Primary: Alice Developer (alice@example.com)
> Backup: Bob Engineer (bob@example.com)
```

### PagerDuty
Import contacts as service owners for automated escalation.

### GitHub/GitLab
Compare generated contacts with CODEOWNERS to detect drift.
