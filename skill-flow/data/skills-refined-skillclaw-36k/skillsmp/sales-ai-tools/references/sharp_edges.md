# Sales - Sharp Edges

## Domain Reputation Death

### **Id**
domain-reputation-death
### **Summary**
Cold email can destroy your domain reputation permanently
### **Severity**
critical
### **Tools Affected**
  - apollo
  - instantly
  - lemlist
  - outreach
### **Situation**
Sending cold emails from main company domain
### **Why**
  If your main domain gets blacklisted:
  - All company email goes to spam
  - Very hard to recover (months)
  - Affects customer communication too
  - Some blacklists are permanent
  
  This is the #1 cold email mistake.
  
### **Solution**
  1. NEVER use main domain for cold outreach
  2. Buy separate domains (variant names)
  3. Warm up domains for 2-3 weeks before sending
  4. Monitor deliverability metrics
  5. Use dedicated cold email infrastructure
  
  ```
  # Bad:
  john@company.com sending cold
  
  # Good:
  john@trycompany.io (separate, warmed domain)
  ```
  
### **Symptoms**
  - Reply rates suddenly drop
  - Emails bouncing
  - Marketing emails going to spam

## Spam Trap Lists

### **Id**
spam-trap-lists
### **Summary**
Purchased lists often contain spam traps
### **Severity**
high
### **Tools Affected**
  - apollo
  - zoominfo
  - lusha
  - cognism
### **Situation**
Buying or scraping email lists and blasting them
### **Why**
  ESP providers and anti-spam companies plant fake emails:
  - Spam traps look like real addresses
  - Hitting them = instant blacklist
  - No legit person would email these
  - Even big data providers have some
  
  One spam trap can end your outreach program.
  
### **Solution**
  1. Always verify emails before sending
  2. Use verification tools (NeverBounce, ZeroBounce)
  3. Start with small test sends
  4. Remove bounces immediately
  5. Don't email anyone who hasn't engaged in 6+ months
  
### **Symptoms**
  - Sudden blacklisting
  - ESP account suspended
  - Deliverability crashes overnight

## Linkedin Automation Ban

### **Id**
linkedin-automation-ban
### **Summary**
LinkedIn aggressively bans automation
### **Severity**
high
### **Tools Affected**
  - apollo
  - lemlist
  - phantombuster
### **Situation**
Using LinkedIn automation at scale
### **Why**
  LinkedIn detects and bans automation:
  - Browser fingerprinting
  - Activity pattern detection
  - API monitoring
  - Connection request limits
  
  Losing your LinkedIn profile = losing your network.
  
### **Solution**
  1. Stay under daily limits (20-30 connections/day)
  2. Use tools that mimic human behavior
  3. Randomize activity patterns
  4. Don't run automation 24/7
  5. Use Sales Navigator for higher limits
  6. Consider LinkedIn premium accounts
  
### **Symptoms**
  - Connection requests restricted
  - Account temporarily suspended
  - Profile banned permanently

## Data Decay

### **Id**
data-decay
### **Summary**
B2B data decays 30-40% per year
### **Severity**
high
### **Tools Affected**
  - zoominfo
  - apollo
  - lusha
  - clearbit
### **Situation**
Treating data as accurate without verification
### **Why**
  People change jobs constantly:
  - 30-40% of B2B data stale within a year
  - Direct dials change even faster
  - Company data (size, tech) changes
  - Even "fresh" data can be months old
  
  Sending to bad data = bounces = reputation damage.
  
### **Solution**
  1. Verify emails before major campaigns
  2. Look for job change signals
  3. Re-verify data older than 3-6 months
  4. Use waterfall enrichment (multiple sources)
  5. Remove bounces immediately
  
### **Symptoms**
  - High bounce rates (>3%)
  - Wrong person replies
  - Job titles don't match

## Enrichment Credit Explosion

### **Id**
enrichment-credit-explosion
### **Summary**
Enrichment credits can burn faster than expected
### **Severity**
medium
### **Tools Affected**
  - clay
  - clearbit
  - zoominfo
### **Situation**
Running enrichment on large lists without budgeting
### **Why**
  Credits add up quickly:
  - Each enrichment field = credits
  - Waterfall tries multiple sources
  - Re-enrichment doubles cost
  - "Just checking" burns credits too
  
  Easy to 10x your expected spend.
  
### **Solution**
  1. Budget credits per campaign upfront
  2. Pre-filter lists before enrichment
  3. Only enrich fields you actually use
  4. Set up credit alerts at 50%, 75%
  5. Audit credit usage weekly
  
### **Symptoms**
  - Hit credit limit mid-month
  - Unexpected overage charges
  - Can't enrich at end of month

## Crm Data Quality Garbage

### **Id**
crm-data-quality-garbage
### **Summary**
Bad CRM data makes AI useless
### **Severity**
high
### **Tools Affected**
  - salesforce
  - hubspot-sales
  - gong
  - clari
### **Situation**
Expecting AI insights from messy CRM
### **Why**
  AI tools rely on CRM data:
  - Forecasting needs accurate stages
  - Scoring needs consistent properties
  - Analytics needs complete records
  - Garbage in = garbage out
  
  AI can't fix fundamental data problems.
  
### **Solution**
  1. Establish data entry standards
  2. Use required fields at stage changes
  3. Audit data quality monthly
  4. Auto-populate from reliable sources
  5. Clean duplicates regularly
  6. Train team on data hygiene
  
### **Symptoms**
  - AI predictions wildly wrong
  - Can't trust dashboards
  - Duplicate records everywhere

## Salesforce Admin Dependency

### **Id**
salesforce-admin-dependency
### **Summary**
Salesforce becomes a black box without admin
### **Severity**
high
### **Tools Affected**
  - salesforce
### **Situation**
Implementing Salesforce without dedicated admin
### **Why**
  Salesforce is infinitely configurable:
  - Custom objects, fields, automations
  - Complex permission structures
  - Integrations break without maintenance
  - Tribal knowledge accumulates
  
  When your "Salesforce person" leaves, chaos ensues.
  
### **Solution**
  1. Document all customizations
  2. Have backup admin knowledge
  3. Consider managed services
  4. Keep customization minimal
  5. Use standard objects when possible
  6. Regular admin training
  
### **Symptoms**
  - Nobody knows how it works
  - Integrations randomly break
  - Can't change workflows

## Gong Privacy Concerns

### **Id**
gong-privacy-concerns
### **Summary**
Call recording raises privacy and legal issues
### **Severity**
high
### **Tools Affected**
  - gong
  - salesloft
  - outreach
### **Situation**
Recording calls without proper consent
### **Why**
  Recording laws vary:
  - Two-party consent states (California, etc.)
  - GDPR requirements in EU
  - Some countries prohibit entirely
  - Customer pushback
  
  Violations can mean lawsuits and fines.
  
### **Solution**
  1. Know laws for every jurisdiction you sell into
  2. Get explicit consent on every call
  3. Add to meeting invites/scripts
  4. Allow opt-out gracefully
  5. Consult legal before rollout
  
### **Symptoms**
  - Customer complaints
  - Legal threats
  - Deals killed by recording

## Ai Email Generic

### **Id**
ai-email-generic
### **Summary**
AI-generated emails all sound the same
### **Severity**
medium
### **Tools Affected**
  - lavender
  - regie-ai
  - apollo
### **Situation**
Using AI email suggestions without editing
### **Why**
  AI email tools train on similar data:
  - Same patterns, phrases, structures
  - Prospects see same AI emails daily
  - Detection skills improving
  - "AI voice" becoming recognizable
  
  If everyone uses same AI, no one stands out.
  
### **Solution**
  1. Use AI for drafts, not final copy
  2. Inject specific research/personalization
  3. Develop your own voice
  4. Customize AI suggestions heavily
  5. A/B test AI vs human-written
  
### **Symptoms**
  - Low reply rates
  - Prospects mention 'AI email'
  - Sound like every other SDR

## Conversation Intelligence Overload

### **Id**
conversation-intelligence-overload
### **Summary**
Too much call data, not enough action
### **Severity**
medium
### **Tools Affected**
  - gong
  - clari
### **Situation**
Having all the insights but not changing behavior
### **Why**
  Gong shows everything:
  - Every call recorded
  - Hundreds of metrics
  - Dozens of talk tracks
  - Weekly report emails
  
  Information overload leads to paralysis.
  
### **Solution**
  1. Pick 2-3 metrics to focus on
  2. Create clear coaching workflows
  3. Schedule regular review sessions
  4. Connect insights to specific actions
  5. Don't try to boil the ocean
  
### **Symptoms**
  - Gong mostly unused
  - No behavior change
  - Expensive shelfware

## Sync Conflicts

### **Id**
sync-conflicts
### **Summary**
Tool sync conflicts corrupt CRM data
### **Severity**
high
### **Tools Affected**
  - apollo
  - outreach
  - salesloft
  - hubspot-sales
### **Situation**
Multiple tools writing to same CRM fields
### **Why**
  When multiple tools sync:
  - Race conditions occur
  - Last write wins (may be wrong)
  - Duplicates created
  - Activity attribution breaks
  
  Hard to diagnose, harder to fix.
  
### **Solution**
  1. Map all integrations before setup
  2. Designate one source of truth per field
  3. Use one-way syncs where possible
  4. Test integrations in sandbox
  5. Monitor for sync errors
  
### **Symptoms**
  - Data randomly changes
  - Duplicate records
  - Wrong activity attribution

## Sequence Overlap

### **Id**
sequence-overlap
### **Summary**
Multiple sequences hit same prospect
### **Severity**
medium
### **Tools Affected**
  - apollo
  - outreach
  - salesloft
### **Situation**
Same person in multiple sequences from different reps
### **Why**
  Without coordination:
  - Marketing + SDR + AE all emailing
  - Different tools, no visibility
  - Prospect gets 5 emails in a day
  - Looks unprofessional, hurts brand
  
  Annoys prospects and kills deals.
  
### **Solution**
  1. Use CRM sequence exclusions
  2. Coordinate territory rules
  3. Check before adding to sequence
  4. Single outreach tool if possible
  5. Marketing/sales SLA on timing
  
### **Symptoms**
  - Prospects complain about spam
  - Confused messaging
  - Angry unsubscribes