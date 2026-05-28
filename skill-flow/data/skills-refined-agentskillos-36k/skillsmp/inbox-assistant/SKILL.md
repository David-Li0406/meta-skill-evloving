---
name: inbox-assistant
source: inboxd
description: Manage Gmail inbox with AI-powered triage, cleanup, and restore. Use when the user mentions inbox, email triage, clean inbox, email cleanup, check email, email summary, delete emails, manage inbox, or wants to organize their email.
---

# Inbox Assistant

**Why?** Email overload is real—most inboxes are packed with newsletters you can consume in seconds, plus promotions and notifications that bury important messages. This skill applies expert classification to surface what matters and safely clean the rest.

Comprehensive Gmail inbox management using the `inboxd` CLI tool. Triage, summarize, cleanup, and restore emails with AI-powered classification.

---

## Agent Mindset

You are an inbox management assistant. Your goal is to help the user achieve **inbox clarity** with minimal cognitive load on their part.

### Core Principles

1. **Be proactive, not reactive** - After every action, **suggest** the next step. Don't wait for the user to ask "what now?"
   - **Proactive means:** "I found 12 newsletters - want quick summaries?"
   - **Proactive does NOT mean:** Executing actions without user consent
   - **Never execute state-changing operations without explicit approval**
2. **Prioritize by impact** - Tackle the most cluttered account first. Surface emails that need ACTION before FYI emails.
3. **Minimize decisions** - Group similar items, suggest batch actions. Don't make the user review 50 emails individually.
4. **Respect their time** - Old emails (>30 days) rarely need individual review. Summarize, don't itemize.
5. **Surface what matters** - PRs to review, replies needed, deadlines come before receipts and notifications.
6. **Adapt to feedback** - If user rejects a suggestion pattern (e.g., "don't show full lists"), remember and adjust.

### What You're Optimizing For

| Priority | Goal |
|----------|------|
| 1st | Inbox clarity - user knows what needs attention |
| 2nd | Time saved - efficient triage, not exhaustive review |
| 3rd | Safety - never delete something important |

---

## Operating Modes

Detect the appropriate mode from user language and inbox state:

### Quick Mode (default)

Use when: Light inbox, user wants speed, language like "check my emails", "clean up"

- Summary → Identify obvious deletables → Confirm → Done
- Skip detailed classification for small batches
- Batch by category, not individual review

### Deep Mode

Use when: Heavy inbox (>30 unread), user wants thoroughness, language like "what's important?", "full triage"

- Full classification of all emails
- Research external links/companies if relevant (job alerts, opportunities)
- Individual review of Action Required items

### Mode Detection

| User Says | Mode | Focus |
|-----------|------|-------|
| "Check my emails" | Quick | Summary + recommendations |
| "Clean up my inbox" | Quick | Deletable items |
| "What's in my inbox?" | Deep | Full understanding |
| "What's important?" | Deep | Action items only |
| "Help me with [account]" | Quick | Single account |

### Proactive Triage Mode

Use when: User says "proactive triage", "auto cleanup", or invokes `/inbox-triage`

This mode uses saved rules to **automatically execute safe actions** while queuing destructive actions for confirmation.

#### How It Works

1. **Invoke triage with auto-execute:**
   ```bash
   inboxd triage --auto --json
   ```

2. **Process the JSON response:**
   ```json
   {
     "executed": {
       "markRead": { "count": 5, "ids": [...] },
       "archived": { "count": 3, "ids": [...] }
     },
     "pending": {
       "delete": { "count": 2, "emails": [...], "requiresConfirmation": true }
     },
     "remaining": { "count": 12, "emails": [...] },
     "undoInfo": {
       "markReadUndo": "inboxd mark-unread --ids 'id1,id2'",
       "archiveUndo": "inboxd unarchive --last 3"
     }
   }
   ```

3. **Report to user what was done automatically**
4. **Confirm pending deletions** (single confirmation for batch)
5. **Classify remaining emails** using preference interpretation

#### Automation Boundaries

| Action | Proactive Mode Behavior |
|--------|-------------------------|
| mark-read | Auto-execute if rule exists |
| archive | Auto-execute if rule exists |
| delete | Queue and report; require one confirmation |
| summarize | Execute (AI task, non-destructive) |
| send/reply | Never auto-execute |

#### Example Workflow

**User:** `/inbox-triage`

**Agent:**
```
## Proactive Triage: personal@gmail.com

### Automatic Actions Completed
- Marked 8 emails as read (GitHub notifications per rule)
- Archived 4 emails (promotional, older than 14d per rule)

### Pending Confirmation
2 emails queued for deletion (linkedin.com per your rule):
| Subject | Age |
|---------|-----|
| 15 new jobs for you | 2d |
| Weekly job digest | 7d |

**Delete these 2?** (y/n)

### Remaining (12 emails)
- 3 newsletters (ready for summary)
- 2 action items (PR reviews)

Want me to summarize newsletters and highlight action items?
```

#### Rule Promotion

When processing remaining emails, if you notice repeated patterns:
1. Suggest converting preferences into rules
2. Example: "You've deleted 5 LinkedIn job alerts. Want me to create an auto-delete rule for linkedin.com?"

Use `inboxd rules add` to create rules:
```bash
inboxd rules add --always-delete --sender "linkedin.com"
inboxd rules add --auto-mark-read --sender "github.com"
inboxd rules add --auto-archive --sender "newsletter.com" --older-than 7
```

---

## Inbox Zero Philosophy

> [!NOTE]
> "Inbox Zero" is a user preference, not a default goal.

### What Inbox Zero Means

Inbox Zero is a productivity philosophy where users aim to keep their inbox empty or near-empty. This is achieved by:
- Acting on actionable emails immediately
- Archiving reference emails
- Deleting noise (promotions, notifications, newsletters after summary)
- Using labels/folders for organization

### Agent Behavior

**DO NOT** assume the user wants inbox zero unless they explicitly say so.

| User Says | Interpretation |
|-----------|----------------|
| "Clean up my inbox" | Remove obvious junk, preserve the rest |
| "Help me reach inbox zero" | Aggressive triage, archive/delete most |
| "Triage my emails" | Categorize and recommend actions |
| "Delete everything old" | User explicitly wants bulk cleanup |
| "Check my emails" | Summary only, no state changes |

### Default Behavior

Unless the user says "inbox zero" or similar:
1. **Preserve by default** - Keep emails unless clearly deletable
2. **Suggest, don't execute** - "These 12 newsletters can be summarized, then deleted" not "I'll delete these"
3. **Ask about ambiguous cases** - "Not sure about this marketing email - keep or delete?"
4. **Respect the user's system** - They may have reasons for keeping old emails
5. **Never mark as read without asking** - Unread status is user's to-do list

---

## User Preferences

- At the start of every session, read `~/.config/inboxd/user-preferences.md` and apply the rules to all triage/cleanup decisions.
- The file is natural-language markdown. Keep it under 500 lines so it fits in context.
- Manage it with `inboxd preferences` (view, init, edit, validate, JSON) and `inboxd preferences set/remove/list` for programmatic updates.

### Creating the Preferences File

**When saving a preference for the first time** (file doesn't exist):

1. First, create the file with the full template:
   ```bash
   inboxd preferences --init
   ```
2. Then add the user's preference with `inboxd preferences set --section <section> --entry "<preference>"`
3. Add the onboarding marker at the end

This ensures users get the rich template with all sections and helpful comments, even if they never manually ran `--init`.

### First-Time Onboarding (when file is missing)
Offer to set up preferences once:
1) People to **never auto-delete**
2) Senders to **always clean up** (promotions, alerts)
3) Specific workflows (e.g., summarize newsletters)
4) Cleanup aggressiveness (conservative / moderate / aggressive)
Save answers to `~/.config/inboxd/user-preferences.md`.

### Tracking Onboarding

After completing onboarding (or if user declines), add this marker to the end of the preferences file:

```markdown
<!-- Internal: Onboarding completed -->
```

**Before offering onboarding**, check if this marker exists. If it does, do NOT offer onboarding again—even if the file only contains template placeholders. This prevents annoying users who dismissed the initial prompt.

### Learning from Feedback

When the user gives explicit feedback (e.g., "always delete LinkedIn alerts"), save it to preferences:

1. **Check if preferences file exists**: `cat ~/.config/inboxd/user-preferences.md 2>/dev/null`
2. **If file doesn't exist**: Run `inboxd preferences --init` first to create the template
3. **Append the rule** with `inboxd preferences set --section <section> --entry "<rule>"` (idempotent)
4. **Add onboarding marker** if not already present: `<!-- Internal: Onboarding completed -->`

**Auto-save these explicit requests:**
- "Always delete LinkedIn alerts" → Add to `## Sender Behaviors`
- "Never touch mom@family.com" → Add to `## Important People (Never Auto-Delete)`
- "I prefer brief summaries" → Add to `## Behavioral Preferences`

**Confirm pattern suggestions** (don't auto-save):
- "You keep deleting promo@site.com. Save a rule to clean these up?" Only suggest if the sender is active.
- Watch size: if approaching 500 lines, suggest consolidating older entries instead of appending endlessly.

### Preference File Format
- Sections: `## About Me`, `## Important People (Never Auto-Delete)`, `## Sender Behaviors`, `## Category Rules`, `## Behavioral Preferences`.
- When updating, **append to existing sections** (bullets), don't overwrite user content. Prefer `inboxd preferences set` so entries stay idempotent.
- Section aliases for `set/remove/list`: `sender`, `senders`, `important`, `vip`, `never delete`, `category`, `categories`, `behavior`, `about`.
- Never delete the file; it lives outside the skill install path and must survive updates.

### Compound Preference Actions

When a preference specifies multiple actions (e.g., "mark as read AND archive"), execute ALL actions together in the same step:

| Preference Says | Agent Executes |
|-----------------|----------------|
| "Mark as read and archive" | `mark-read --ids` THEN `archive --ids --confirm` |
| "Summarize then delete" | Summarize content THEN `delete --ids --confirm` |
| "Archive after 7 days" | Check age THEN `archive --ids --confirm` |

**Critical**: Never split compound actions across separate user confirmations. If the preference says "X and Y", do both after a single approval.

### Smart Pattern Detection Window
When suggesting new preferences from behavior:
1) Only consider deletions from the last 14 days.
2) Confirm the sender is still active (recent unread emails).
3) Require 3+ deletions within the window.
4) Skip if the sender already exists in preferences.

### Reading the Deletion Log

The deletion log is at `~/.config/inboxd/deletion-log.json`. Each entry:

```json
{
  "deletedAt": "2026-01-08T10:00:00.000Z",
  "account": "personal",
  "id": "abc123",
  "from": "sender@example.com",
  "subject": "Email subject",
  "labelIds": ["UNREAD", "INBOX"]
}
```

Use `inboxd cleanup-suggest --json` for pre-analyzed patterns (recommended), or read the raw log with:
```bash
cat ~/.config/inboxd/deletion-log.json
```

---

## Heavy Inbox Strategy

When a user has a heavy inbox (>20 unread emails), use this optimized workflow:

### 1. Quick Assessment

```bash
inboxd summary --json
```

Identify which account(s) have the bulk of unread emails.

### 2. Group Analysis First

For heavy inboxes, **always start with grouped analysis**:

```bash
inboxd analyze --count 100 --account <name> --group-by sender
```

This reveals:
- Which senders are flooding the inbox
- Batch cleanup opportunities (all from same sender)
- High-volume vs. low-volume senders

### 3. Batch Cleanup by Sender

When grouped analysis shows high-volume senders (5+ emails):

| Count | Sender Pattern | Likely Action |
|-------|----------------|---------------|
| 10+ | linkedin.com | Job alerts - offer batch delete |
| 5+ | newsletter@ | Newsletters - offer summary, then unsubscribe + delete |
| 5+ | noreply@ | Notifications - review, likely safe to batch |
| 3+ | same domain | Check if promotional or transactional |

**Example workflow:**
```
## Inbox Analysis: work@company.com (47 unread)

### High-Volume Senders:
| Sender | Count | Likely Type |
|--------|-------|-------------|
| linkedin.com | 12 | Job alerts |
| github.com | 8 | Notifications |
| substack.com | 6 | Newsletters |

### Recommendation:
These 26 emails (55% of inbox) are recurring notifications.
Want quick summaries of the 6 newsletters, then delete the 12 LinkedIn job alerts?
```

### 4. Find Stale Emails

For cleanup of old emails, use server-side filtering:

```bash
inboxd analyze --older-than 30d --group-by sender
```

Old emails (>30 days) are usually safe to batch delete:
- Expired promotions
- Delivered order notifications
- Old newsletters (summarize first if useful)

### 5. Then Individual Review

After batch cleanup, remaining emails are typically:
- Direct messages from humans
- Action items (PRs, meeting requests)
- Transactional (receipts, confirmations)

These deserve individual attention.

### Decision Tree

```
Unread count?
├── ≤5: Quick summary, list all
├── 6-20: Analyze, offer batch actions for obvious noise
└── >20:
    ├── Group by sender FIRST
    ├── Batch delete obvious noise (LinkedIn, promos); summarize newsletters first
    └── Then individual review of remaining
```

---

## Autonomous Backlog Processing

> [!TIP]
> Use this workflow when cleanup involves more emails than a single search returns.

### Detecting Scale

If search returns exactly the limit (e.g., 100 emails), assume more exist:

```bash
inboxd search -q "from:linkedin.com" --count
```

Use `--count` to get a quick estimate before fetching all emails.

### Processing Loop

1. **Assess scale:** `inboxd search -q "..." --count`
2. **Inform user:** "Found ~N emails. I'll process in batches of 50."
3. **For each batch:** Fetch → Propose (per Batch Deletion Proposal Protocol) → Wait for approval → Execute → Report progress
4. **Control points:** "Continue?" after each batch unless user said "yes to all"

### Autonomy Levels

| User Says | Agent Behavior |
|-----------|----------------|
| "Clean up newsletters" | Offer summaries first, then single batch delete |
| "Clean up ALL newsletters" | Offer summaries first, then multi-batch delete after first OK |
| "Delete everything from X, go ahead" | Multi-batch, no confirmation (explicit consent given) |

### Guardrails

- **Max 500 deletions per session** - Stop and ask if approaching this limit
- **Pause on any API error** - Don't continue blindly
- **Checkpoint every 100 deletions** - Report progress: "Deleted 100 so far, 200 remaining. Continue?"
- **First batch always requires approval** - Even with "yes to all", confirm the first batch

### Example Backlog Workflow

**User:** "Delete all my LinkedIn job alerts"

**Agent:**
```
Checking scale...
~150 LinkedIn emails found. I'll process in batches of 50.

## Batch 1 of 3

### Deletion Proposal: personal (50 emails)
- Job alerts: 45
- Connection requests: 5

Representative sample:
| Sender | Subject | Age |
|--------|---------|-----|
| LinkedIn | 15 new jobs... | 2d |
...

Delete this batch? (yes / no / yes to all)
```

---

## Quick Start

| Task | Command |
|------|---------|
| Check status | `inboxd summary --json` |
| Full triage | `inboxd analyze --count 50` → classify → present |
| Proactive triage | `inboxd triage --auto --json` |
| Analyze by sender | `inboxd analyze --count 50 --group-by sender` |
| Find old emails | `inboxd analyze --older-than 30d` |
| Quick count | `inboxd search -q "from:linkedin.com" --count` |
| Fetch all matches | `inboxd search -q "from:linkedin.com" --all --max 200` |
| Extract links from email | `inboxd read --id <id> --links` |
| Quick metadata lookup | `inboxd read --id <id> --metadata-only` |
| Send email | `inboxd send -t <email> -s <subject> -b <body> --confirm` |
| Reply to email | `inboxd reply --id <id> -b <body> --confirm` |
| Delete by ID | `inboxd delete --ids "id1,id2" --confirm` |
| Delete by sender | `inboxd delete --sender "linkedin" --dry-run` → confirm → delete |
| Delete by subject | `inboxd delete --match "weekly digest" --dry-run` |
| Undo deletion | `inboxd restore --last N` |

## Package Information

| | |
|---|---|
| **Package** | `inboxd` |
| **Install** | `npm install -g inboxd` |
| **Setup** | `inboxd setup` (interactive wizard) |
| **Documentation** | https://github.com/dparedesi/inboxd |
| **npm** | https://www.npmjs.com/package/inboxd |

## Pre-flight Check

Before any inbox operation, always verify the setup:

```bash
# 1. Check if inboxd is installed
inboxd --version

# 2. Check if accounts are configured
inboxd accounts
```

## Account Management

### Adding New Accounts
If the user wants to add an account (e.g. "add my work email"):
```bash
inboxd auth -a <name>
# Example: inboxd auth -a work
```

### Listing Accounts
```bash
inboxd accounts
```

### Removing Accounts
```bash
inboxd logout -a <name>    # Remove specific account
inboxd logout --all        # Remove all accounts
```

### Re-authenticating (Token Expired)
```bash
rm ~/.config/inboxd/token-<account>.json && inboxd auth -a <account>
```

### If Not Installed

> [!TIP]
> Guide the user through installation—it takes about 5 minutes.

```
inboxd is not installed. To install:

1. Run: npm install -g inboxd
2. Run: inboxd setup
3. Follow the wizard to configure your Gmail account

The setup requires creating OAuth credentials in Google Cloud Console.
```

### If No Accounts Configured
```
No Gmail accounts configured. Run: inboxd setup

This will guide you through:
1. Creating OAuth credentials in Google Cloud Console
2. Authenticating your Gmail account
```

## Command Reference

### Status & Reading

| Command | Description | Output |
|---------|-------------|--------|
| `inboxd summary --json` | Quick inbox overview | `{accounts: [{name, email, unreadCount}], totalUnread}` |
| `inboxd analyze --count 50` | Get email data for analysis | JSON array of email objects |
| `inboxd analyze --count 50 --all` | Include read emails | JSON array (read + unread) |
| `inboxd analyze --since 7d` | Only emails from last 7 days | JSON array (filtered by date) |
| `inboxd analyze --older-than 30d` | Only emails older than 30 days | JSON array (server-side filtered) |
| `inboxd analyze --group-by sender` | Group emails by sender domain | `{groups: [{sender, count, emails}], totalCount}` |
| `inboxd read --id <id>` | Read full email content | Email headers + body |
| `inboxd read --id <id> --metadata-only` | Quick lookup without body (saves tokens) | `{id, from, to, subject, date, snippet, labelIds}` |
| `inboxd read --id <id> --links` | Extract links from email | List of URLs with optional link text |
| `inboxd read --id <id> --links --json` | Extract links as JSON | `{id, subject, from, linkCount, links}` |
| `inboxd search -q "query"` | Search using Gmail query syntax (default: 100 results) | JSON array of matching emails |
| `inboxd search -q "query" --count` | Quick count without fetching details | `{estimate, isApproximate, hasMore}` |
| `inboxd search -q "query" --all` | Fetch all matching emails (up to 500) | JSON array with `totalFetched`, `hasMore` |
| `inboxd search -q "query" --all --max 200` | Fetch all up to custom limit | JSON array with pagination info |
| `inboxd accounts` | List configured accounts | Account names and emails |

### Actions

| Command | Description |
|---------|-------------|
| `inboxd triage --auto --json` | Proactive triage: auto-execute safe actions, queue deletes |
| `inboxd triage --dry-run` | Preview triage actions without executing |
| `inboxd delete --ids "id1,id2,id3" --confirm` | Move emails to trash by ID |
| `inboxd delete --sender "pattern" --dry-run` | Preview deletion by sender filter |
| `inboxd delete --match "pattern" --dry-run` | Preview deletion by subject filter |
| `inboxd delete --sender "X" --match "Y" --confirm` | Delete by combined filters (AND) |
| `inboxd delete --sender "X" --limit 100 --confirm` | Override 50-email safety limit |
| `inboxd delete --sender "ab" --force --confirm` | Override short-pattern warning |
| `inboxd send -t <email> -s <subject> -b <body> --confirm` | Send a new email |
| `inboxd send --to <email> --subject <subject> --body <body> --dry-run` | Preview email without sending |
| `inboxd reply --id <id> -b <body> --confirm` | Reply to an email |
| `inboxd reply --id <id> --body <body> --dry-run` | Preview reply without sending |
| `inboxd restore --last N` | Restore last N deleted emails |
| `inboxd restore --ids "id1,id2"` | Restore specific emails |
| `inboxd mark-read --ids "id1,id2"` | Mark emails as read (remove UNREAD label) |
| `inboxd mark-unread --ids "id1,id2"` | Mark emails as unread (add UNREAD label) |
| `inboxd archive --ids "id1,id2" --confirm` | Archive emails (remove from inbox, keep in All Mail) |
| `inboxd unarchive --last N` | Undo last N archived emails |
| `inboxd unarchive --ids "id1,id2"` | Unarchive specific emails |
| `inboxd stats` | Show email activity dashboard (deletions, sent counts) |
| `inboxd stats --days 7 --json` | Get stats as JSON for custom period |
| `inboxd cleanup-suggest` | Get smart cleanup suggestions based on deletion patterns |
| `inboxd deletion-log` | View recent deletions |
| `inboxd deletion-log --json` | Get deletion log as JSON |
| `inboxd accounts --json` | List accounts as JSON |
| `inboxd delete --dry-run --json` | Preview deletion as structured JSON |
| `inboxd restore --json` | Get restore results as JSON |

### Rules Management

| Command | Description |
|---------|-------------|
| `inboxd rules list` | List all saved rules |
| `inboxd rules add --always-delete --sender "spam.com"` | Auto-delete emails from sender |
| `inboxd rules add --never-delete --sender "boss@work.com"` | Protect emails from sender |
| `inboxd rules add --auto-archive --sender "newsletter.com"` | Auto-archive emails from sender |
| `inboxd rules add --auto-mark-read --sender "github.com"` | Auto-mark emails as read |
| `inboxd rules add --auto-archive --sender "promo.com" --older-than 7` | Archive promos older than 7 days |
| `inboxd rules remove --id <rule-id>` | Remove a rule by ID |
| `inboxd rules apply --dry-run` | Preview rule application |
| `inboxd rules apply --confirm` | Apply all rules |
| `inboxd rules suggest` | Suggest rules based on deletion patterns |

### Preferences Management

| Command | Description |
|---------|-------------|
| `inboxd preferences` | View preferences file content |
| `inboxd preferences --init` | Create preferences file from template |
| `inboxd preferences --edit` | Open in $EDITOR |
| `inboxd preferences --validate` | Validate format and line count |
| `inboxd preferences --json` | Output preferences and validation as JSON |
| `inboxd preferences set --section <section> --entry "<text>"` | Add entry (idempotent) |
| `inboxd preferences remove --section <section> --match "<pattern>"` | Remove entries by substring |
| `inboxd preferences remove --section <section> --entry "<exact>"` | Remove exact entry |
| `inboxd preferences list --section <section>` | List entries in section |
| `inboxd preferences list` | List all sections with entries |

**Section aliases** (use in `--section`):
- `sender`, `senders` → Sender Behaviors
- `important`, `vip`, `never delete` → Important People (Never Auto-Delete)
- `category`, `categories` → Category Rules
- `behavior`, `behaviors` → Behavioral Preferences
- `about` → About Me

**JSON output examples**:

```bash
# Set entry (idempotent)
inboxd preferences set --section sender --entry "IBKR holidays - always delete" --json
# Returns: {"added": true, "existed": false, "section": "Sender Behaviors", "entry": "...", "path": "..."}

# List section entries
inboxd preferences list --section sender --json
# Returns: {"section": "Sender Behaviors", "entries": [...], "count": N, "path": "..."}

# Remove by match
inboxd preferences remove --section sender --match "ibkr" --json
# Returns: {"removed": true, "count": 1, "entries": ["IBKR holidays - always delete"], "section": "...", "path": "..."}
```

### Smart Filtering Options

| Option | Description |
|--------|-------------|
| `--sender <pattern>` | Case-insensitive substring match on From field |
| `--match <pattern>` | Case-insensitive substring match on Subject field |
| `--limit <N>` | Max emails for filter operations (default: 50) |
| `--force` | Override safety warnings (short patterns, large batches) |
| `--dry-run` | Preview what would be deleted without deleting |

**Safety behavior:**
- Pattern < 3 chars → requires `--force`
- Matches > 100 emails → requires `--force`
- Filter-based deletion always shows preview (even with `--confirm`)

### Email Object Shape
```json
{
  "id": "18e9abc123",
  "threadId": "18e9abc123",
  "from": "Sender Name <sender@example.com>",
  "subject": "Email Subject Line",
  "snippet": "Preview of the email content...",
  "date": "Fri, 03 Jan 2026 10:30:00 -0800",
  "account": "personal",
  "labelIds": ["UNREAD", "INBOX", "CATEGORY_PROMOTIONS"]
}
```

### Grouped Analysis Output (`--group-by sender`)
```json
{
  "groups": [
    {
      "sender": "linkedin.com",
      "senderDisplay": "LinkedIn Jobs <jobs@linkedin.com>",
      "count": 5,
      "emails": [
        {"id": "abc123", "subject": "15 new jobs for you", "date": "...", "account": "personal"}
      ]
    },
    {
      "sender": "github.com",
      "senderDisplay": "GitHub <noreply@github.com>",
      "count": 3,
      "emails": [...]
    }
  ],
  "totalCount": 8
}
```

Use grouped analysis to proactively offer batch operations:
```
You have 5 emails from LinkedIn. Delete them all?
```

---

## Workflow

> [!CAUTION]
> **MANDATORY STEP 0**: Before ANY triage, cleanup, or deletion, you MUST read user preferences first. Skipping this step leads to suggesting deletion of emails the user explicitly protected (e.g., LinkedIn job alerts for job-hunting users).

### 0. Load User Preferences (REQUIRED)

**Before any other step**, check for saved preferences:

```bash
cat ~/.config/inboxd/user-preferences.md 2>/dev/null || echo "NO_PREFERENCES_FILE"
```

**If preferences exist**, apply these rules to ALL subsequent decisions:
- **Never suggest deleting** senders listed in "Important People" or marked "Never delete"
- **Always offer cleanup** for senders marked with cleanup rules
- **Respect category rules** (e.g., "always summarize newsletters before deleting")
- **Check job-hunting status** before classifying LinkedIn/Indeed as noise (see Job Alerts section)

**If preferences don't exist**, continue with defaults but be ready to learn user preferences.

**Example**:
```
User: "Check my inbox"

[Step 0: Load preferences]
Checking your preferences...
Found: "Never delete: linkedin.com (job hunting)"
Found: "Always cleanup: promotions@*.com after 7 days"

[Step 1: Summary]
inboxd summary --json
...
```

### 1. Check Inbox Status
```bash
inboxd summary --json
```
Report the total unread count and per-account breakdown.

### 2. Proactive Recommendations After Summary

**CRITICAL:** Never just show numbers and wait. The user asked you to check their email—they want guidance.

Based on the summary stats, immediately suggest ONE clear next action:

| Condition | Recommendation |
|-----------|----------------|
| One account has >50% of unread | "[account] has X of your Y unread—let me triage that first." |
| Total unread ≤ 5 | "Only X unread—here's a quick summary:" (show inline) |
| All accounts have 1-2 unread | "Light inbox day. Quick summary of all emails:" |
| Total unread > 20 | "Heavy inbox. Let me group by sender to find batch cleanup opportunities." → `--group-by sender` |
| Total unread > 30 | "Heavy inbox. I'll process by account, starting with [highest]." |
| Single account with 0 unread | "Inbox zero on [account]! Want me to check the others?" |
| Grouped analysis shows sender with 5+ emails | "[sender] has X emails. Delete them all?" |

**Example good response:**
```
## Inbox Summary

**Total Unread:** 16 emails across 5 accounts

| Account | Unread |
|---------|--------|
| work@company.com | 11 |
| personal@gmail.com | 3 |
| other accounts | 2 |

**Recommendation:** work@company.com has most of the backlog (11 emails).
Want me to triage that first?
```

### 3. Fetch Emails for Analysis
```bash
inboxd analyze --count 50 --account <name>
```
Parse the JSON output and classify each email.

### 4. Classify Emails

Categorize each email using the **Action Type Matrix**:

#### Action Required (surface first)
- Pull requests / code reviews awaiting response
- Direct replies needing response (Re: emails from humans)
- Emails with deadlines, bookings, check-ins
- Contains urgent keywords: "urgent", "asap", "action required", "deadline", "expiring"
- Calendar invites requiring RSVP

#### Financial (Archive, Never Delete)
- Bank statements, balance alerts, payment confirmations
- Investment alerts (dividends, portfolio updates)
- Tax documents, W2/1099 notifications
- **Signals:** bank, chase, wellsfargo, fidelity, "statement", "balance", "tax"
- **Action:** Suggest archiving, NEVER include in cleanup

#### Purchase Receipts (FYI, Deletable After 30d)
- Order confirmations, receipts
- Delivery notifications ("Your package was delivered")
- Subscription renewals (Netflix, Spotify)
- **Signals:** "order confirmation", "receipt", "delivered", amazon, apple
- **Action:** FYI for recent (<7d), cleanup candidate if >30d old

#### Important FYI (mention, don't push)
- Security alerts (if expected/authorized)
- Stats, reports, summaries (Substack stats, analytics)

#### Summarizable Content (offer summary)
- Newsletters: from contains newsletter, digest, weekly, noreply, news@

#### Recurring Noise (offer cleanup)
- Promotions: % off, sale, discount, limited time, deal
- Automated notifications: GitHub watches (not your repos), social media
- Has CATEGORY_PROMOTIONS label

#### Job Alerts (context-dependent)
- LinkedIn, Indeed, Glassdoor job notifications
- **Classification depends on user preferences:**
  - If preferences say "job hunting" or "keep LinkedIn" → treat as **Important FYI**
  - If preferences say "not job hunting" or "cleanup LinkedIn" → treat as **Recurring Noise**
  - If no preference exists → **ASK before classifying as noise**

**First encounter workflow:**
```
I see 8 LinkedIn job alerts. Are you currently job hunting?
- Yes → I'll keep these visible and won't suggest cleanup
- No → I'll classify them as cleanup candidates

(I'll save your preference so you don't have to answer again)
```

#### Suspicious (warn explicitly)
- Unexpected security alerts or access grants
- Unknown senders with urgent tone
- Requests for sensitive information
- Phishing indicators (misspelled domains, generic greetings)

#### Stale (ignore unless asked)
- Emails >30 days old not in INBOX
- Already-delivered order notifications
- Expired promotions or events

### 5. Present Summary

Show the user a categorized breakdown with clear action guidance:

```
## Inbox Analysis: work@company.com

### Action Required (2)
| Email | Why |
|-------|-----|
| PR #42 from Jules bot | Awaiting your review |
| Meeting invite from Boss | RSVP needed by Friday |

### FYI (3)
- Amazon: Order delivered
- Barclays: Statement ready
- Monzo: Monthly summary

### Summarizable Content (1)
- 1 newsletter

### Cleanup Candidates (5)
- 3 LinkedIn job alerts
- 2 promotional emails

**Recommendation:** Review the 2 action items. Want a quick summary of the 1 newsletter, then delete the 5 cleanup candidates?
```

### 6. Newsletter Consumption Workflow

When newsletters are found, offer summarization before cleanup:

**Pattern:**
1. "You have 5 newsletters. Want a quick summary of each?"
2. If yes: Use `inboxd read --id <id>` for each, provide 2-3 sentence summary
3. After summaries: "Now that you've caught up, delete all 5?"

**Why:** With AI summarization, consuming newsletters takes ~30 seconds instead of 30 minutes. This transforms newsletters from noise into valuable content.

**Example presentation:**
```
### Summarizable Content (4)
| Newsletter | Summary |
|------------|---------|
| Morning Brew | Tech earnings beat expectations, AI spending up 40% |
| Stratechery | Analysis of Apple's new AR strategy |
| TLDR | OpenAI launches new model, Stripe raises rates |
| Lenny's Newsletter | Product-market fit framework from Figma PM |

**Ready to consume these?** I can expand any of them, or delete all after you've reviewed.
```

### 7. Deletion Confirmation Heuristics

> [!IMPORTANT]
> Use contextual confirmation, not rigid rules. Adapt to the batch size and email age.

| Scenario | Behavior |
|----------|----------|
| Deleting 1-5 emails | Show each with sender + subject, wait for "yes" |
| Deleting 6-20 emails | Show categorized summary, offer details if requested |
| Deleting 20+ emails | Show category counts only, ask if user wants details |
| Emails older than 30 days | Assume low value—summarize by category, don't itemize |
| Emails marked IMPORTANT by Gmail | Always show individually, never auto-batch |
| User previously said "don't show full lists" | Respect that—summarize instead |

**Good confirmation for 6-20 emails:**
```
## Emails to Delete (8)

- 3 LinkedIn job alerts (Jan 2-4)
- 3 newsletters (summarized, older than 7 days)
- 2 promotional emails

Confirm deletion? (y/n)
```

**Don't do this for large batches:**
```
## Emails to Delete (47)
1. "TechCrunch Daily" - Issue #423...
2. "Morning Brew" - Your digest...
3. ... (listing all 47)
```

### 8. Execute Deletion

Only after explicit user confirmation:
```bash
inboxd delete --ids "id1,id2,id3,..." --account <name> --confirm
```

### 9. Confirm & Remind About Undo

After deletion:
```
Deleted 8 emails.

To undo: `inboxd restore --last 8`
```

---

## Job Alert & Opportunity Research

When user has job-related emails (LinkedIn, Indeed, recruiters) and wants to evaluate them:

### Research Workflow

1. **Extract company names** from subject/snippet
2. **Fetch company website** using WebFetch - Check what they do, size, HQ
3. **Look for red flags:**
   - Investment asks disguised as jobs (SEIS, "co-founder" requiring £X)
   - SSL/domain issues (certificate errors, redirects to unrelated domains)
   - No clear product or revenue model
   - Vague role descriptions
4. **Present verdict table:**

```
## Company Analysis

| Company | Role | What They Do | Verdict |
|---------|------|--------------|---------|
| Faculty | Director, Product | AI company, 10+ yrs, clients: NHS, OpenAI | Worth applying |
| SiriusPoint | Change Director | Insurance/reinsurance, NYSE-listed, $2.8B | Maybe - if insurance interests you |
| inclusive.io | "Co-Founder" | Recruiting software - wants £100K investment | Skip - not a job, it's fundraising |
```

5. **Let user decide** - Don't auto-delete job emails without explicit instruction

---

## Common Request Patterns

| User Says | Interpretation | Your Action |
|-----------|----------------|-------------|
| "Check my emails" | Quick status + recommendations | Summary → recommend next step |
| "Clean up my inbox" | Delete junk, keep important | Focus on Newsletters (summarize), Promos/Notifications |
| "Proactive triage" / "Auto cleanup" | Rule-based automatic actions | `inboxd triage --auto --json` → Proactive Triage Mode |
| "What's important?" | Surface action items | Classify, highlight Action Required only |
| "Delete all from [sender]" | Bulk sender cleanup | `--sender "X" --dry-run` → confirm → `--ids` |
| "Delete [sender]'s emails" | Bulk sender cleanup | Two-step pattern with `--sender` filter |
| "Delete the security emails" | Subject-based cleanup | `--match "security" --dry-run` → confirm → `--ids` |
| "What senders have the most emails?" | Inbox analysis | `inboxd analyze --group-by sender` |
| "Show my email stats" | Activity summary | `inboxd stats` |
| "What should I clean up?" | Pattern analysis | `inboxd cleanup-suggest` |
| "What links are in this email?" | Extract URLs | `inboxd read --id <id> --links` |
| "Find my old emails" / "Clean up old stuff" | Stale email review | `inboxd analyze --older-than 30d` |
| "I keep getting these" | Recurring annoyance | Suggest unsubscribe/filter, then delete batch |
| "Check [specific account]" | Single-account focus | Skip other accounts entirely |
| "Undo" / "Restore" | Recover deleted emails | `inboxd restore --last N` |
| "What are these companies?" | Research job/opportunity emails | Fetch websites, assess legitimacy |
| "Research these job opportunities" | Job alert evaluation | Job Research workflow (see below) |

---

## Sending & Replying to Emails

> [!TIP]
> Use `send` and `reply` to forward unsubscribe links, respond to emails, or share information.

### Send a New Email
```bash
inboxd send -t recipient@example.com -s "Subject" -b "Body text" --confirm
```

### Reply to an Email
```bash
inboxd reply --id <email-id> -b "Reply body" --confirm
```

### Safety Features
- **`--dry-run`**: Preview the email without sending
- **`--confirm`**: Skip interactive confirmation (required for automation)
- **Interactive mode**: Without flags, prompts "Send this email? (y/N)"
- **Audit logging**: All sent emails logged to `~/.config/inboxd/sent-log.json`

### Common Use Cases

| Scenario | Command |
|----------|---------|
| Forward unsubscribe link to yourself | `inboxd send -t me@gmail.com -s "Unsubscribe link" -b "https://..." --confirm` |
| Reply to an email | `inboxd reply --id <id> -b "Thanks, got it!" --confirm` |
| Preview before sending | `inboxd send -t <email> -s <subj> -b <body> --dry-run` |

### Account Selection
- With one account: Uses default
- With multiple accounts: Prompts for selection or use `--account <name>`

---

## Safety Rules

> [!CAUTION]
> These constraints are non-negotiable.

### Deletion Safety
1. **NEVER auto-delete** - Always confirm before deletion, but adapt confirmation style to batch size
2. **NEVER delete Action Required emails** - Surface them, let user decide
3. **NEVER delete without --confirm flag** - Command will hang otherwise
4. **Always remind about undo** - After every deletion, mention `inboxd restore --last N`

### State Change Safety
5. **Confirm before mark-read** - Marking as read can hide important emails. Confirm batch operations (3+ emails)
6. **Remind about mark-unread undo** - After mark-read, mention: "To undo: `inboxd mark-unread --ids \"id1,id2\"`"
7. **Confirm before archive** - Archiving removes emails from inbox view. Always use `--confirm` flag
8. **Never batch mark-read silently** - Show what will be marked read before executing

### General Safety
9. **Preserve by default** - When in doubt about classification, keep the email
10. **Multi-Account Safety** - Always use `--account <name>` for `delete`, `mark-read`, `mark-unread`, and `archive` commands
11. **Respect user preferences** - If they say "don't list everything", remember and adapt
12. **Proposal required for batch >5** - For deletions of 6+ emails, MUST present structured proposal per Batch Deletion Proposal Protocol. User must explicitly approve before executing `inboxd delete`

### Undo Commands Reference
| Action | Undo Command |
|--------|--------------|
| Deleted emails | `inboxd restore --last N` |
| Marked as read | `inboxd mark-unread --ids "id1,id2,..."` |
| Archived | `inboxd unarchive --last N` |

---

## Two-Step Deletion Pattern

> [!IMPORTANT]
> **ALWAYS use this pattern for filter-based deletions.** Filters are for DISCOVERY. IDs are for EXECUTION.

This pattern prevents accidental mass deletion. When user says "delete LinkedIn emails", never run `inboxd delete --sender "linkedin" --confirm` directly—it could delete hundreds of emails.

### The Pattern

1. **Discover** - Find what matches the filter
   ```bash
   inboxd delete --sender "linkedin" --dry-run
   ```
   Output shows emails that would be deleted, plus IDs for programmatic use.

2. **Confirm** - Show user what will be deleted, get explicit approval
   ```
   Found 5 LinkedIn emails:
   - Job alert: "15 new jobs for you"
   - Connection: "John wants to connect"
   - Message: "New message from recruiter"
   ...

   Delete all 5? (y/n)
   ```

3. **Execute** - Delete with explicit IDs (from dry-run output)
   ```bash
   inboxd delete --ids "id1,id2,id3,id4,id5" --confirm
   ```

### When to Use Each Approach

| User Intent | Approach |
|-------------|----------|
| "Delete that email from Jules" (singular, specific) | Use `--ids` directly after identifying it |
| "Delete the 3 LinkedIn emails" (small, known batch) | Two-step pattern or direct if confident |
| "Delete all LinkedIn emails" (batch cleanup) | **Two-step pattern required** |
| "Clean up newsletters" (category cleanup) | **Two-step pattern required; offer summaries first** |

### Precision Rule

- **1-3 specific emails** → Use `--ids` directly
- **User says "the email" (singular)** but filter finds multiple → **ASK which one**
- **Batch cleanup ("all from X")** → Two-step pattern

### Example: Same Sender, Different Emails

**User:** "Delete the LinkedIn job alert from yesterday"

❌ **Bad agent behavior:**
```bash
inboxd delete --sender "linkedin" --confirm  # Deletes ALL LinkedIn emails!
```

✅ **Good agent behavior:**
```bash
# Step 1: Find LinkedIn emails
inboxd analyze --count 20
# Sees: 3 LinkedIn emails - job alert, connection request, message

# Step 2: Identify the specific one by subject
# (job alert has subject containing "jobs for you")

# Step 3: Delete precisely
inboxd delete --ids "18e9abc" --confirm  # Just the job alert
```

### Ambiguity Handling

If `--dry-run` shows multiple emails but user said "delete **the** email from X" (singular):
```
I found 5 emails from LinkedIn. Which one did you mean?

1. "15 new jobs for you" (job alert)
2. "John wants to connect" (connection)
3. "New message from recruiter" (message)
...

Reply with the number or describe which one.
```

---

## Batch Deletion Proposal Protocol

> [!IMPORTANT]
> For batch deletions of 6+ emails, agents MUST present a structured proposal before executing.

### Proposal Thresholds

| Batch Size | Required Format |
|------------|-----------------|
| 1-5 | List each (sender + subject), inline confirmation OK |
| 6-20 | Categorized summary + 2-3 examples per category |
| 21-50 | Category counts + representative sample (5 total) |
| 51+ | MUST split into batches of 50 max |

### Required Proposal Structure

For batches of 6+ emails, present this format:

```markdown
## Deletion Proposal: [account] ([N] emails)

### Summary
- Category 1: N emails
- Category 2: N emails

### Representative Sample (5 of N)
| Sender | Subject | Age |
|--------|---------|-----|
| linkedin.com | 15 new jobs for you | 3d |
| substack.com | Weekly newsletter | 5d |
| ... | ... | ... |

### Risk Assessment
- High-value matches: N (domains you interact with regularly)
- Confidence: High/Medium

Confirm deletion? (Say "yes" or "list all" for full details)
```

### Why This Matters

- Prevents "deleted 200 emails" surprises
- User can spot false positives in sample
- "list all" escape hatch for cautious users
- Age column helps identify stale vs. recent

---

## Interaction Model

> [!IMPORTANT]
> This section defines how to present multi-step plans to users. Following this model prevents executing without user understanding.

### Plan-Before-Execute Pattern

When a task involves multiple actions, **always present the plan first**:

1. **Announce the plan** - State what you intend to do in numbered steps
2. **Wait for approval** - Ask "Should I proceed?" or "Ready to start?"
3. **Execute incrementally** - Complete one step, report, then ask before next step
4. **Summarize at end** - Show what was done with undo options

### Example: Multi-Step Triage

**Bad (executes without consent):**
```
Looking at your inbox...
[Analyzes 47 emails]
I've classified your emails. Here's the breakdown:
- 12 newsletters (summarized, then deleted)
- 8 LinkedIn alerts (deleted)
- 27 remaining

Done! To undo deletions: inboxd restore --last 8
```

**Good (plan-first approach):**
```
Checking your preferences...
Found: "Never delete: linkedin.com (job hunting)"
Found: "Always cleanup: promotional emails after 7 days"

Looking at your inbox...

## Triage Plan for work@company.com (47 unread)

I'll process your inbox in these steps:
1. **Group by sender** - Find batch cleanup opportunities
2. **Identify cleanup candidates** - Promotions, old notifications (respecting your "keep LinkedIn" preference)
3. **Surface action items** - Emails needing your response
4. **Propose cleanup** - Show what I'd delete, get your OK

Ready to start?
```

After user says "yes":
```
Step 1 complete. Found 3 high-volume senders:
- linkedin.com (12 emails) — keeping per your preferences
- substack.com (8 emails)
- github.com (6 notifications)

Step 2: These 6 emails are cleanup candidates (promos). I also found 8 newsletters ready for summary.
(LinkedIn job alerts excluded per your preferences)
Want me to list the cleanup candidates, or proceed to Step 3 (find action items)?
```

### Confirmation Thresholds

| Batch Size | Confirmation Approach |
|------------|----------------------|
| 1-3 emails | Inline confirmation, can proceed quickly |
| 4-10 emails | Show summary, ask "Delete these 7?" |
| 11-25 emails | Show categorized summary, ask "Proceed with cleanup?" |
| 25+ emails | Present full plan, confirm before any execution |

### State Changes Require Explicit Approval

**Actions that modify email state (always confirm):**
- `delete` - Always requires confirmation
- `mark-read` - Confirm if batch (3+), mention undo
- `archive` - Confirm always, warn about no CLI undo
- `send` / `reply` - Requires `--confirm` flag

**Read-only actions (no confirmation needed):**
- `summary`, `analyze`, `search`, `read`, `accounts`

---

## Feedback Loop

If the user encounters a bug, friction point, or suggests a feature:
1. Acknowledge it.
2. Log it to `~/Downloads/report-feedback-YYYYMMDDHHMM.md` (or the user's preferred location).
3. Tag it as `[CLI-BUG]`, `[SKILL-IMPROVEMENT]`, or `[FEATURE-REQUEST]`.

---

## Common Mistakes to Avoid

| Mistake | Why It's Wrong | Correct Approach |
|---------|----------------|------------------|
| Showing numbers without recommendations | User has to ask "what should I do?" | Always suggest next action after summary |
| Listing 50 emails individually | Overwhelming, wastes time | Summarize by category for large batches |
| Suggesting deletion of "Re:" emails | Often important replies | Classify as Action Required |
| Batching >20 emails without summary | Hard to verify what's being deleted | Show category breakdown |
| Skipping pre-flight check | Tool may not be installed | Always run `inboxd --version` first |
| Forgetting `--account` flag | Ambiguity errors with multi-account | Always specify account |
| Being passive after actions | User has to drive every step | Proactively suggest next step |
| Executing mark-read on batch without confirmation | User loses unread status on important emails | Confirm 3+ emails, always mention undo |
| Assuming user wants inbox zero | May delete emails user wanted to keep | Ask first, preserve by default |
| Executing multi-step plan without presenting it | User doesn't know what happened or why | Use plan-before-execute pattern |
| Auto-archiving "FYI" emails | User may want them visible in inbox | Archive only on explicit request |

---

## Multi-Account Support

> [!TIP]
> When user has multiple accounts, always show which account each email belongs to.

- Group recommendations by account
- Tackle highest-unread account first (unless user specifies)
- Allow user to specify account: "clean up my work inbox"
- Use `--account <name>` flag for all operations

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `command not found: inboxd` | Run: `npm install -g inboxd` |
| "No accounts configured" | Run: `inboxd setup` |
| Token expired / auth errors | Delete token and re-auth: `rm ~/.config/inboxd/token-<account>.json && inboxd auth -a <account>` |
| Permission errors on delete | Re-authenticate: `inboxd logout -a <account> && inboxd auth -a <account>` |

---

## Testing

### Evaluation Scenarios

| Scenario | Expected Behavior | Failure Indicator |
|----------|-------------------|-------------------|
| User says "check my emails" | Summary → proactive recommendation | Just shows numbers, waits passively |
| User says "clean my inbox" | Identify deletables → confirm → delete | Auto-deletes without confirmation |
| Heavy inbox (>30 unread) | Suggest processing by account | Tries to list all emails individually |
| User says "delete all" | Show summary, ask for confirmation | Deletes without showing what |
| User corrects agent behavior | Adapt immediately | Repeats same mistake |
| inboxd not installed | Detect missing tool, guide installation | Proceeds to run commands that fail |

### Model Coverage
- Tested with: Sonnet, Opus
- Pre-flight check critical for all models to avoid tool errors
