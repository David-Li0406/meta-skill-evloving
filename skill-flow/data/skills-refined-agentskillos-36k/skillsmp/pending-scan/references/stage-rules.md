# Stage-Based Follow-Up Rules

## Active Stages

These stages require ongoing follow-up:

### New Lead
- **Threshold**: 2 days
- **Urgent**: 4 days
- **Channel**: Email
- **Goal**: Schedule intake call or gather initial info

### Intake
- **Threshold**: 2 days
- **Urgent**: 4 days
- **Channel**: Email
- **Goal**: Complete intake, gather business details

### Application / Application Received
- **Threshold**: 3 days
- **Urgent**: 5 days
- **Channel**: Email
- **Goal**: Get application completed and submitted

### Submission
- **Threshold**: 5 days
- **Urgent**: 7 days
- **Channel**: Email
- **Goal**: Wait for carrier response, check status

### Quote Pitched / Quoted
- **Threshold**: 2 days
- **Urgent**: 3 days
- **Channel**: Call (more personal for closing)
- **Goal**: Get decision, address objections

## Closed Stages (No Follow-Up)

- **Bound**: Policy in place
- **Closed Won**: Deal completed
- **Closed Lost**: Not pursuing
- **Closed**: General closed status

## Urgency Calculation

```
days_since_contact = today - last_contact_date

if days_since_contact > urgent_threshold + 2:
    urgency = "critical"
elif days_since_contact > urgent_threshold:
    urgency = "high"
elif days_since_contact > threshold:
    urgency = "normal"
else:
    urgency = None  # No follow-up needed yet
```

## Channel Selection

1. Use stage's primary channel by default
2. Override to call if:
   - Urgency is critical
   - Multiple emails without response
3. Override to SMS if:
   - No email on file
   - Client prefers text
