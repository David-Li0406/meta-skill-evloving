---
name: action-execute
description: Execute follow-up actions and record them in the account history. Handles sending communications and updating state.
---

# Action Execute

## When to use this skill

- After communication is drafted and approved
- Executing a batch of follow-up actions
- Recording completed outreach

## Execution flow

1. **Validate** the drafted communication
2. **Send** via appropriate channel (or mock send)
3. **Record** in `mem/sent_communications/`
4. **Update** account state and history

## Recording sent communications

Each sent communication is saved:

```
mem/sent_communications/{account_id}/
└── {timestamp}_{channel}.md
```

Example: `mem/sent_communications/29041/2025-01-15T14-30-00_email.md`

Content format:

```markdown
# Follow-Up Communication

**Account**: {Account Name} ({Account ID})
**Channel**: email
**Sent**: 2025-01-15T14:30:00Z
**To**: owner@company.com

## Subject
Following up on your GL quote

## Body
Hi [Name],

I wanted to follow up...

## Context Used
- state.md
- call_150734/summary.md
```

## State updates after execution

1. Update `Last Contact` in state.md
2. Add entry to history.md:
   ```markdown
   ## 2025-01-15T14:30:00Z
   
   Follow-up email sent regarding quote decision.
   
   - **Action**: Email sent
   - **Evidence**: [2025-01-15T14-30-00_email.md](../../../sent_communications/29041/2025-01-15T14-30-00_email.md)
   ```

## Execution modes

### Live Mode
- Actually sends email/SMS via configured provider
- Makes real phone calls via script

### Mock Mode (Default)
- Records communication as if sent
- Updates state and history
- Does not contact actual recipients

## Batch execution

For multiple follow-ups:

1. Generate all drafts first
2. Review and approve batch
3. Execute sequentially with delay
4. Report success/failure for each
