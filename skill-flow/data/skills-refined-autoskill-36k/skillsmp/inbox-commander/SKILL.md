---
name: inbox-commander
description: Email triage and organization system for Gmail. Use when user asks to "triage my inbox", "check my email", "process emails", "what needs my attention", "inbox zero", or any request to organize, classify, or act on emails. Provides GTD-style processing with autonomous actions for clear-cut items and surfaced decisions for ambiguous ones. Creates newsletter digests, drafts replies, and suggests bulk unsubscribes.
---

# Inbox Commander

Email triage using GTD: Do it now, Decide, Defer, or Dump.

## Interface Mode

**Current: Terminal Mode** - Fast, batch-oriented. Auto-executes high-confidence actions, surfaces decisions via AskUserQuestion.

**Future: Browser Mode** - HTML template stored at `templates/browser-view.html` for future implementation. Would generate rich visual report with collapsible sections and checkboxes.

## Email Fetch Limit

**Always fetch 100+ emails** to get full inbox picture. Use pagination if needed:

```
maxResults: 100
```

For very large inboxes, process in batches of 100, prioritizing unread first.

## Tool Selection

**Check for gscli first** (faster, includes calendar/drive context):

```bash
which gscli && gscli auth status
```

If available and authenticated, use gscli for READ operations:

- `gscli gmail list` - List messages
- `gscli gmail read <id>` - Read message
- `gscli calendar list` - Get upcoming meetings
- `gscli drive search` - Find related docs

**Use Gmail MCP for WRITE operations** (gscli is read-only):

- Archive, label, snooze, create drafts, create filters

**Fallback**: If gscli unavailable, use Gmail MCP for everything.

## Triage Scope

Process ALL unarchived mail (Inbox), regardless of read state:

- **Unread + unarchived** = New, needs classification and action
- **Read + unarchived** = User saw it but didn't act → surface as "stale" for nudge
- **Archived** = processed/done → ignore
- **Snoozed** (label: `snooze/YYYY-MM-DD`) → ignore until date passes

**Stale item handling:**

- Read items > 3 days old: gentle nudge
- Read items > 7 days old: stronger nudge, likely should archive or act
- Items with `ic/needs-response` label: always surface prominently regardless of read state

## Execution Flow

```
1. Check tool availability (gscli vs MCP-only)
2. Load references:
   - learned-rules.md (corrections take precedence)
   - known-senders-private.md (if exists) or known-senders.md
3. Check snoozed items → unsnooze if date passed
4. Fetch emails (Inbox, maxResults: 100+)
5. Fetch context: calendar, Linear (graceful fail)
6. CLASSIFY ALL emails silently:
   a. Already labeled by Gmail filter? → Validate, compute urgency
   b. Unlabeled? → Classify, apply label, track pattern
   c. Invoice/Bill detected? → Validate, flag validity
7. EXECUTE Tier 1 actions immediately (no approval needed)
   - Archive receipts, calendar responses, notifications
   - Apply labels
   - Track what was done for summary
8. Aggregate Tier 2 → prepare newsletter digest
9. PRESENT batch summary with strong recommendations
10. USE AskUserQuestion for decisions (see Output Format below)
11. Execute approved actions → log corrections
12. Suggest new Gmail filters if patterns emerged
```

## Label System

### Philosophy

**Labels = stable categorization** (stored on email)
**Urgency = dynamic computation** (calculated fresh each run)

Urgency changes constantly (Monday's "this week" becomes Friday's "today"). Don't label urgency — compute it based on context.

### Hybrid Approach

Gmail filters handle deterministic patterns instantly at delivery. AI handles unlabeled items and suggests new filters when patterns emerge.

**If email is already labeled** (by Gmail filter):

- Validate the label is correct
- Focus on computing urgency and action state
- Don't re-classify unless label seems wrong

**If email is unlabeled:**

- Classify and apply appropriate label
- Track the pattern (sender, subject)
- After 3+ similar classifications → suggest Gmail filter

### Label Structure

Create labels if missing. Use Gmail MCP `get_or_create_label`.

**Content Bundles** (for Simplify Gmail visual grouping):

- `Newsletters` - digested content, auto-archive after
- `Newsletters/Pending-Digest` - saved for next digest run (not archived yet)
- `Receipts` - payment confirmations, auto-archive
- `Bills` - invoices awaiting payment (never auto-archive)
- `Bills/Queued` - invoices forwarded to Brex for payment
- `Bills/Crypto-Pending` - crypto invoices awaiting manual payment
- `Bills/Paid` - paid invoices (audit trail)
- `Renewals` - subscription renewal notices (NEVER auto-archive, always surface)
- `Notifications` - tool notifications, auto-archive (unless error)
- `Transactional` - shipping, confirmations

**Entity Types** (for rules + search):

- `Team` - internal team domains
- `Investors` - known investor contacts
- `Legal` - law firms, legal matters
- `Vendors` - payroll, finance, contractors

**Action State** (workflow tracking):

- `ic/needs-response` - user owes a reply
- `ic/waiting-on` - ball in their court
- `ic/scheduled` - has follow-up date
- `ic/processed` - audit trail (apply before archiving)

**Snooze** (time-based deferral):

- `snooze/YYYY-MM-DD` - hide until this date

## Urgency Tiers (Computed, Not Labeled)

Compute urgency fresh each run based on context:

**🔴 TODAY** - Surface immediately

- Explicit deadline today or overdue
- Error/failure notifications
- Sender you're meeting today (check calendar)
- Follow-up on something already escalated
- Team + needs-response older than 24h

**🟡 THIS WEEK** - Surface prominently

- Deadline this week
- Investors + needs-response
- Legal + needs-response
- Important sender waiting 2+ days

**🟢 SOMETIME** - Surface in list

- No deadline, low stakes
- Vendors with non-urgent questions
- Requests that can wait

**⚪ FYI** - Mention briefly or skip

- Informational only, no action needed
- Already handled, just confirming

## Classification Tiers

### Tier 1: Auto-Action (No Approval)

| Pattern                                          | Action                         |
| ------------------------------------------------ | ------------------------------ |
| Payment confirmations                            | Label: Receipts → Archive      |
| Calendar responses (Accepted/Declined/Tentative) | Archive                        |
| Tool notifications                               | Label: Notifications → Archive |
| Misrouted (wrong recipient, user not CC'd)       | Archive + note                 |

**Escalate to Tier 3** if contains: "failed", "error", "action required", "urgent", "security alert"

### Tier 1.5: Renewal Alerts (Surface Prominently)

**NEVER auto-archive subscription renewal notices.** User may want to cancel before being charged.

**Detection patterns:**

- Subject: "will renew", "subscription renew", "upcoming renewal", "will be charged", "auto-renew"
- From: `*@stripe.com` with "upcoming-invoice" or "renewal"
- From: billing/subscription addresses of known services

**Output format:**

```
🔔 RENEWAL ALERTS - 2 subscriptions renewing soon

1. Lex Pro - $XX/month renews Jan 25 (card ending 7539)
   → Keep subscription? Or cancel before renewal?

2. Adobe Creative Cloud - $XX/month renews Jan 28
   → Keep subscription? Or cancel before renewal?
```

**AskUserQuestion options:**

- "Keep all subscriptions" - Archive renewal notices
- "Review each one" - Go through 1-by-1 to decide keep/cancel
- "Show cancellation links" - Surface cancel URLs for review

**Action:** Label as `Renewals`, present in dedicated section BEFORE newsletters, give user chance to cancel.

### Tier 2: Newsletter Digest

Match: `*@substack.com`, `*@tldrnewsletter.com`, `*@beehiiv.com`, known senders (see `references/known-senders.md`)

**Also include:** Emails with `Newsletters/Pending-Digest` label (saved from prior runs)

Action: Label: Newsletters → Summarize → Archive originals

Output: Create digest with top stories, key insights. Digest is the deliverable; originals archived for reference.

### Tier 3: Surface for Decision

- Team emails (unless purely informational)
- Starred messages (user's hot list — never auto-modify)
- Investors, Legal, important Vendors
- Anything with `ic/needs-response` label
- Anything ambiguous

### Tier 4: Elimination Candidates

- Cold outreach (first contact + sales language patterns)
- Marketing drip campaigns from tools not in use
- Mailing lists with zero engagement
- Batch for bulk unsubscribe offer

## Output Format (Terminal Mode)

**NEVER use fake `[button]` syntax.** Process each section with its own AskUserQuestion.

### Flow: Section-by-Section Triage

Process inbox in logical order. For each section:

1. **Show enough detail** to approve confidently (sender, subject, why classified this way, recommended action)
2. **AskUserQuestion** with batch approve, drill-down, or skip options
3. **User can always type custom response** via "Other" option (built into AskUserQuestion)

---

### Section 1: 🔴 URGENT / TODAY

Only if urgent items exist. Show **full context** so user can approve without drilling down:

```
🔴 URGENT - 2 items need attention NOW

1. ✈️ Delta Air Lines <DeltaAirLines@t.delta.com>
   "It's Time To Check In For Your Flight"
   Flight JFK→MEX departs TODAY 4:57pm, Confirmation: HOPT3X
   → Recommend: Open check-in link

2. ⚠️ PHISHING: X <verify17@x-verify.business>
   "New login to your X from ChromeDesktop"
   FAKE - real X uses @x.com domain, content is W-8BEN form (nonsense)
   → Recommend: Delete immediately
```

Then AskUserQuestion:

```
AskUserQuestion:
  question: "2 urgent items. How to proceed?"
  header: "Urgent"
  options:
    - label: "Handle as recommended"
      description: "Open Delta check-in, delete phishing email"
    - label: "Go through 1-by-1"
      description: "Decide each item individually"
    - label: "Skip for now"
      description: "I'll handle these manually"
```

If "1-by-1" selected, use individual AskUserQuestion per item:

```
AskUserQuestion:
  question: "🔴 Delta Flight - JFK→MEX departs 4:57pm today"
  header: "Delta"
  options:
    - label: "Open check-in (Recommended)"
      description: "Opens delta.com check-in page"
    - label: "Snooze 2 hours"
      description: "Remind me at 2:57pm"
    - label: "Skip"
      description: "I'll handle manually"
```

---

### Section 2: 🟡 THIS WEEK / NEEDS ATTENTION

Only if items exist. Show **full context**:

```
🟡 THIS WEEK - 3 items need attention soon

1. 🎿 Trybal Gatherings <hello@trybalgatherings.com>
   "Flurry up! Ski Trip registration closes in 48 hours"
   Deadline: 48 hours from now
   → Recommend: Decide - register or skip?

2. 📧 Debra Meyerson <debram@stanford.edu>
   "Re: Andrews McMeel Publishing: Anthropic Copyright Settlement"
   Thread about books in AI training settlement - you're CC'd
   → Recommend: Review if you have relevant published work, else archive

3. ☁️ Google Cloud <googlecloud@google.com>
   "Welcome to your Google Cloud Free Trial"
   New account setup - may need action to activate
   → Recommend: Review or archive if not needed
```

Then AskUserQuestion:

```
AskUserQuestion:
  question: "3 items for this week. How to proceed?"
  header: "This Week"
  options:
    - label: "Review each item"
      description: "Go through 1-by-1 with options"
    - label: "Snooze all to Monday"
      description: "Clear inbox now, revisit Monday"
    - label: "Skip section"
      description: "Leave in inbox as-is"
```

---

### Section 3: ✅ AUTO-ARCHIVE CANDIDATES

Items classified as Tier 1 (high confidence). Show **grouped detail**:

```
✅ READY TO AUTO-ARCHIVE - 12 items (routine, no action needed)

RECEIPTS (4):
  • Amazon <auto-confirm@amazon.com> - "Ordered: Britax One4Life..."
  • Chase <no.reply.alerts@chase.com> - "We accepted your check deposit(s)" x2
  • TagSwag <donotreply@checkoutstores.com> - "Your Company Swag Store receipt"

NOTIFICATIONS (3):
  • Monarch <email@email.monarch.com> - "2 new updates in Monarch"
  • Porkbun <support@porkbun.com> - "2FA Code" (expired)
  • Google <no-reply@accounts.google.com> - "Security alert for claudiatheceo" x2

TRANSACTIONAL (2):
  • TurboTax <TurboTax@em1.turbotax.intuit.com> - "W-2s are being delivered"
  • CoinTracker <hello@mail.cointracker.io> - "Crypto portfolio update"

LOCAL/COMMUNITY (3):
  • Nextdoor - "Scam account", "Found cat alert"
```

Then AskUserQuestion:

```
AskUserQuestion:
  question: "Archive these 12 routine items?"
  header: "Archive"
  options:
    - label: "Archive all (Recommended)"
      description: "Label and archive all 12 items"
    - label: "Show me the full list"
      description: "Review each item before archiving"
    - label: "Skip"
      description: "Leave in inbox"
```

If "Show full list" → display details, then re-ask with option to exclude specific items.

---

### Section 4: 📰 NEWSLETTERS

Only if newsletters detected. Show **titles and sources**:

```
📰 NEWSLETTERS - 5 items ready for digest

1. The Bismarck Cables <thebismarckcables@substack.com>
   "Greenland: A Solution in Search of a Problem..."

2. CA Attorney General <info@oag.ca.gov>
   "Read the California DOJ Weekly Newsletter"

3. PSP Classifieds <digestnoreply@groups.parkslopeparents.com>
   Digest #6170, #6171, #6172 (3 emails)

4. PSP Advice <digestnoreply@groups.parkslopeparents.com>
   "PSP Advice/Community - Digest #1486"
```

Then AskUserQuestion:

```
AskUserQuestion:
  question: "5 newsletters. Create digest?"
  header: "Newsletters"
  options:
    - label: "Digest & archive (Recommended)"
      description: "Summarize key items, archive originals"
    - label: "Save for next digest"
      description: "Label as pending, include in next digest run"
    - label: "Show titles first"
      description: "See what's in each before digesting"
    - label: "Archive without digest"
      description: "Just clear them out"
    - label: "Skip"
      description: "Leave in inbox"
```

**"Save for next digest" workflow:**
When user selects this option:

1. Apply label: `Newsletters/Pending-Digest`
2. Do NOT archive (keep in inbox as visual reminder)
3. Do NOT create digest now
4. On next triage run, include these in the newsletter digest automatically

**Digest output** (after approval):

```
📰 NEWSLETTER DIGEST - Jan 19, 2026

**Morning Brew**
- Tesla stock surges on AI announcement
- Fed signals rate decision next week

**TLDR AI**
- OpenAI releases GPT-5 preview

**PSP Classifieds** (3 digests)
- Stroller for sale, babysitter available, playdate group

---
5 newsletters archived.
```

---

### Section 5: 🗑️ UNSUBSCRIBE CANDIDATES

Only if Tier 4 items detected. Show **why each is flagged**:

```
🗑️ UNSUBSCRIBE CANDIDATES - 4 senders (marketing/promos you may not want)

1. EyeBuyDirect <news@e.eyebuydirect.com>
   "[Name], Last Chance to Save More ⏳😅"
   Pattern: Marketing drip, pressure tactics

2. Ostrichpillow <hello@ostrichpillow.com>
   "Melt away tension"
   Pattern: Product marketing

3. Moms on Call <info@momsoncall.com>
   "Ready to Sleep Past 5am? Join Us January 27!"
   Pattern: Webinar/event promotion

4. Warriors <info@mail.warriors.com>
   "Back-to-Back Heaters: Warriors vs. Heat Tomorrow..."
   Pattern: Sports promos (keep if you're a fan?)
```

Then AskUserQuestion:

```
AskUserQuestion:
  question: "Unsubscribe from these 4 senders?"
  header: "Unsubscribe"
  multiSelect: true
  options:
    - label: "EyeBuyDirect"
      description: "Marketing emails, 'Last chance' promos"
    - label: "Ostrichpillow"
      description: "Product marketing"
    - label: "Moms on Call"
      description: "Webinar promotions"
    - label: "Warriors"
      description: "Game promos and ticket offers"
```

Execute unsubscribe for selected items, archive the emails.

---

### Section 6: 💰 INVOICES

Only if invoices requiring approval detected:

```
💰 INVOICES - 2 need approval

1. Legal Firm LLP - $12,500 ✅ Valid (due Jan 25)
2. Acme Consulting - $15,000 🚩 Suspicious (first invoice)
```

Then AskUserQuestion for each:

```
AskUserQuestion:
  question: "Legal Firm LLP: $12,500 (due Jan 25)"
  header: "Invoice"
  options:
    - label: "Approve → Brex (Recommended)"
      description: "Known vendor, matches history, forward to bills@brex.com"
    - label: "Review email first"
      description: "See full invoice details"
    - label: "Skip for now"
      description: "Don't process yet"
```

For suspicious invoices, options change:

```
AskUserQuestion:
  question: "🚩 Acme Consulting: $15,000 (SUSPICIOUS)"
  header: "Invoice"
  options:
    - label: "Review carefully"
      description: "First invoice ever, no prior relationship"
    - label: "Request verification"
      description: "Draft email asking for invoice verification"
    - label: "Reject as suspicious"
      description: "Mark as potential fraud, do not pay"
```

---

### Section 7: 👀 STALE / PREVIOUSLY SEEN

Items that are **read but still in inbox** - you saw them but didn't act. Surface these for a nudge:

```
👀 STALE ITEMS - 6 emails you've seen but not acted on

OLDER THAN 1 WEEK (3):
  • Jan 10: LinkedIn <messages-noreply@linkedin.com>
    "5 new connection requests"
    → Recommend: Archive or review connections

  • Jan 8: Stripe <receipts@stripe.com>
    "Your Stripe invoice is ready"
    → Recommend: Archive (likely auto-paid)

  • Jan 5: Some Vendor <sales@example.com>
    "Following up on our conversation"
    → Recommend: Reply, snooze, or archive

OLDER THAN 3 DAYS (3):
  • Jan 15: GitHub <notifications@github.com>
    "PR Review requested"
    → Recommend: Review or close

  • Jan 14: Team Member <person@company.com>
    "Quick question about X"
    → Recommend: Reply (may be waiting on you)
```

Then AskUserQuestion:

```
AskUserQuestion:
  question: "6 stale items in your inbox. How to handle?"
  header: "Stale"
  options:
    - label: "Review each item"
      description: "Go through 1-by-1 to decide"
    - label: "Archive all older than 1 week"
      description: "Clear the old stuff, keep recent"
    - label: "Snooze all to next week"
      description: "Batch defer for later review"
    - label: "Skip"
      description: "Leave as-is for now"
```

**Staleness thresholds:**

- > 7 days: Flag as "older than 1 week" - likely can archive
- > 3 days: Flag as "older than 3 days" - gentle nudge
- Items with `ic/needs-response` label get priority surfacing regardless of age

---

### Section 8: 📋 FILTER SUGGESTIONS

Only if patterns detected:

```
AskUserQuestion:
  question: "Create Gmail filters for detected patterns?"
  header: "Filters"
  multiSelect: true
  options:
    - label: "PSP Classifieds → auto-archive"
      description: "Seen 3 digests, all archived"
    - label: "Chase deposits → Finance/Banking"
      description: "Seen 2 deposit confirmations"
    - label: "Skip all"
      description: "Don't create filters now"
```

---

### Completion Summary

After all sections processed:

```
✅ TRIAGE COMPLETE

New emails processed:
  Archived: 15 emails
  Labeled: 8 emails
  Newsletters: 5 digested
  Unsubscribed: 3 senders
  Invoices: 1 forwarded to Brex
  Filters created: 2

Stale items addressed:
  Archived: 4 old items
  Replied: 1 (draft created)
  Snoozed: 2 to Monday

Remaining in inbox: 3 items
  - 2 snoozed to Monday
  - 1 awaiting external reply (ic/waiting-on)
```

## Snooze Handling

When user requests snooze:

1. Apply label: `snooze/YYYY-MM-DD`
2. Remove from inbox (archive)
3. Apply `ic/scheduled` label

On future triage runs, check snoozed items:

- If today >= snooze date → remove snooze label, move back to inbox
- Otherwise → ignore

## Draft Creation

When user approves a draft:

1. Create Gmail draft via MCP (appears in Gmail Drafts folder)
2. Show draft content in response
3. Use AskUserQuestion for next step:

```
AskUserQuestion:
  question: "Draft created. What next?"
  header: "Draft"
  options:
    - label: "Send now"
      description: "Send immediately"
    - label: "Edit in Gmail"
      description: "Open Gmail to edit before sending"
    - label: "Keep as draft"
      description: "Save for later, don't send"
```

**Never send without explicit confirmation via AskUserQuestion.**

## Invoice/Bill Processing

When an email is detected as an invoice or bill that requires manual payment action.

### Scope: Manual-Pay Invoices Only

**SKIP this flow for auto-pay items:**

- Vendors on auto-pay/autopay (check `known-senders.md` for `autopay: true`)
- Subscriptions with card on file (AWS, GCP, SaaS tools)
- Recurring charges that auto-debit
- Payment confirmations (these are Receipts, not Bills)

**PROCESS through this flow:**

- Invoices requiring manual approval/payment
- New vendors not yet on auto-pay
- One-time or irregular invoices
- Invoices where payment method needs selection

### Detection

Trigger invoice flow when email contains:

- Subject: "invoice", "bill", "payment due", "amount due", "statement"
- From: invoices@_, billing@_, ar@\*, or known billing platforms (QuickBooks, FreshBooks, Bill.com, Xero)
- Body: Invoice numbers, amounts due, due dates, payment terms

**AND** sender is NOT marked as `autopay: true` in known-senders.md.

### Validation

For each invoice, assess validity:

**✅ LOOKS VALID** - All conditions met:

- Sender domain matches known vendor in `known-senders.md`
- Amount consistent with prior invoices (±10%)
- Invoice format matches vendor's history
- No red flags present

**🚩 SUSPICIOUS** - One or more concerns:

- First invoice from this sender
- Amount differs significantly from history
- Bank details changed without prior notice
- Pressure tactics or unusual urgency
- Domain similar but not exact match (typosquatting)

**⛔ LIKELY FRAUD** - Reject signals present:

- Unexpected wire transfer demands from known ACH vendor
- Personal payment accounts (Venmo, personal PayPal) for business invoice
- "Bank details changed" claims without context
- Typosquatted domain pretending to be known vendor

### Payment Method Detection

Invoices may require different payment methods. **Validation applies to ALL payment types.**

**💳 STANDARD (Brex)** - Default for most vendors:

- ACH, wire, check, card payment
- If valid → forward to bills@brex.com

**🪙 CRYPTO/USDC** - Separate payment flow:

- Invoice explicitly requests USDC, USDT, ETH, or other crypto
- Vendor is known crypto-native service (check known-senders.md for `payment: crypto`)
- If valid → present "Pay via crypto wallet" (NOT forwarded to Brex)
- Still validate for fraud - crypto invoices can be fraudulent too

**⚠️ Note:** Crypto payment request from a vendor that normally takes USD is a RED FLAG. Crypto request from a known crypto-native vendor is expected.

### Output Format

Show invoice summary, then use AskUserQuestion for each requiring approval:

```
💰 INVOICES DETECTED (3)

📄 AWS - $2,847.23 (auto-pay, no action needed)
📄 Legal Firm LLP - $12,500.00 ✅ VALID - needs approval
📄 Acme Consulting - $15,000.00 🚩 SUSPICIOUS - needs review
```

Then for each needing approval, use AskUserQuestion:

```
AskUserQuestion:
  question: "Legal Firm LLP invoice: $12,500 (INV-2025-0042, due Jan 25)"
  header: "Invoice"
  options:
    - label: "Approve → forward to Brex (Recommended)"
      description: "Known vendor, matches retainer amount, 6 prior invoices"
    - label: "Review email first"
      description: "Open full invoice email"
    - label: "Reject"
      description: "Do not pay, flag for follow-up"
```

For suspicious invoices:

```
AskUserQuestion:
  question: "🚩 Acme Consulting: $15,000 wire request (SUSPICIOUS)"
  header: "Invoice"
  options:
    - label: "Review carefully"
      description: "First invoice from sender, no prior relationship"
    - label: "Request verification"
      description: "Draft email asking for invoice verification"
    - label: "Reject as potential fraud"
      description: "Mark as suspicious, do not pay"
```

### Brex Forwarding (Standard Payment)

When user approves a valid invoice for standard payment:

1. Confirm approval explicitly: "Forward Legal Firm invoice ($12,500) to bills@brex.com for payment?"
2. On confirmation, forward the original email to `bills@brex.com`
3. Apply label: `Bills/Queued`
4. Log action: "Forwarded to Brex: [vendor] $[amount] Invoice #[number]"

**Forward email format:**

```
To: bills@brex.com
Subject: Fwd: [Original subject]
Body: [Original email content]
```

**Never auto-forward** - Always require explicit approval per invoice.

### Crypto Payment Handling

When user approves a crypto invoice:

1. Confirm: "Pay Web3 Infra Co $5,000 via USDC?"
2. Present wallet/payment details from invoice
3. Apply label: `Bills/Crypto-Pending`
4. User executes payment manually
5. After confirmation, apply label: `Bills/Paid`

### Invoice History Tracking

Track invoice history for validation:

- Store in `references/invoice-history.md` (create if missing)
- Log: date, vendor, amount, invoice number, validation result, payment method
- Use history to establish "normal" patterns per vendor

## Bulk Unsubscribe

For Tier 4 items:

1. Extract unsubscribe links (List-Unsubscribe header or body link)
2. Present as batch: "Found 5 unsubscribe links. Execute all?"
3. On approval, execute unsubscribe:
   - **Preferred**: Use `agent-browser` skill to click unsubscribe links in the email
   - **Fallback**: Create Gmail filter to auto-archive future emails from sender
4. Log results

**Agent-Browser Unsubscribe:**
The `agent-browser` skill can automate clicking unsubscribe links. Use it when:

- User explicitly approves unsubscribe action
- Link is a simple unsubscribe page (not requiring login/forms)

```
AskUserQuestion:
  question: "Unsubscribe from 3 senders. Use browser automation?"
  header: "Unsubscribe"
  options:
    - label: "Click unsubscribe links (Recommended)"
      description: "Use agent-browser to click unsubscribe in each email"
    - label: "Create auto-archive filters"
      description: "Don't unsubscribe, just auto-archive future emails"
    - label: "Skip"
      description: "Leave subscriptions as-is"
```

## Rule Suggestions (AI Training the System)

Track patterns in unlabeled emails that AI classifies. When a pattern emerges, suggest Gmail filter creation.

**Suggest new Gmail filter when:**

- Same sender domain classified 3+ times with same label
- Same subject pattern classified 3+ times
- New vendor/service appears repeatedly

**Output format for suggestions:**

```
📋 SUGGESTED GMAIL FILTERS (3 patterns detected)

1. from:*@cooley.com → Legal (5 emails, 100% match)
2. from:*@srsacquiom.com → Vendors (3 emails)
3. from:*@amazon.com subject:"Your order" → Receipts (8 emails)
```

Then use AskUserQuestion:

```
AskUserQuestion:
  question: "Create Gmail filters for these patterns?"
  header: "Filters"
  multiSelect: true
  options:
    - label: "from:*@cooley.com → Legal"
      description: "5 emails classified this way"
    - label: "from:*@srsacquiom.com → Vendors"
      description: "3 emails classified this way"
    - label: "from:*@amazon.com orders → Receipts"
      description: "8 emails classified this way"
    - label: "Skip all"
      description: "Don't create any filters now"
```

**Suggest unsubscribe/block rules when:**

- Sender classified as Tier 4 (cold outreach) 2+ times
- Newsletter with 0 opens for 30+ days
- Marketing drip from tool not in use

## Learning from Corrections

When user overrides AI classification:

- Log the correction to `references/learned-rules.md`
- Apply learned rules before default classification on future runs
- If pattern becomes clear, suggest filter

Example correction log:

```
You archived "SRS Acquiom" despite HIGH urgency classification.
→ Noted: Shareholder notices from SRS Acquiom = FYI only
→ Suggest filter: from:*@srsacquiom.com subject:shareholder → auto-archive?
```

## Context Integrations

### Calendar (gscli or MCP)

- Flag emails from people you're meeting today/tomorrow
- Detect deadline language ("by Friday", "EOD")

### Linear (MCP)

- Link emails mentioning project names
- Note if sender is assigned to active project

### Drive (gscli)

- If email references a doc, check if it exists in Drive

All optional. Graceful fail. Note status at end: "Calendar: connected | Linear: unavailable"

## Rules

- NEVER auto-send emails. Always save as draft, use AskUserQuestion for send confirmation.
- NEVER use fake `[button]` text in output. Use AskUserQuestion for all decisions.
- Apply `ic/processed` label before archiving (audit trail)
- Log all actions for review
- Use AskUserQuestion before any destructive action (delete, unsubscribe)
- When in doubt, surface it (Tier 3) rather than auto-process
- Batch similar decisions together when possible to reduce friction

### Invoice-Specific Rules

- NEVER auto-forward invoices to bills@brex.com - always require explicit approval
- NEVER auto-pay crypto invoices - always surface for manual payment
- Flag ALL invoices with validity assessment (valid/suspicious/fraud)
- Crypto invoices get same fraud validation as standard invoices
- Skip invoice flow for vendors marked `autopay: true` in known-senders
- Log all invoice actions to `references/invoice-history.md`

## References

- `references/classification-rules.md` - Detailed patterns for each tier
- `references/known-senders.md` - VIPs, team, newsletter sources (template)
- `references/known-senders-private.md` - Personal overrides (if exists, takes precedence)
- `references/learned-rules.md` - Corrections from past runs (auto-generated)
- `references/invoice-history.md` - Invoice history for validation (auto-generated)
- `templates/browser-view.html` - HTML template for future browser mode (not yet implemented)
