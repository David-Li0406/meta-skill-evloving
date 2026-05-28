# Team Communications - Sharp Edges

## Slack Black Hole - Information Lost In Scroll

### **Id**
slack-black-hole
### **Severity**
high
### **Situation**
  Decision made in Slack thread after long discussion. Everyone agrees.
  Three weeks later: "Wait, what did we decide?" Search turns up nothing
  useful. Different people remember different conclusions. The decision
  has to be remade. This happens every month.
  
### **Why**
  Slack is designed for conversation, not storage. Important decisions
  buried in threads become unfindable. Slack search is weak for context.
  When information lives only in chat, it effectively doesn't exist
  for anyone who wasn't there at the moment.
  
### **Solution**
  1. Decision capture ritual:
     """
     AFTER ANY SLACK DECISION:
  
     In thread, post:
     "📝 Decision captured: [Link to doc/wiki]"
  
     The doc contains:
     - What was decided
     - Why (key points from discussion)
     - Who was involved
     - Date
     - Any open items
     """
  
  2. Create decision log:
     """
     DECISION LOG TEMPLATE:
  
     | Date | Decision | Context | Participants |
     |------|----------|---------|--------------|
     | 3/15 | Use Stripe | Cost and API quality | @jane @mike |
     | 3/12 | Rebrand Q2 | Market positioning | @ceo @marketing |
  
     One place to check: "Have we decided this before?"
     """
  
  3. Slack-to-doc automation:
     """
     Use /capture or Zapier:
     - Bookmark important threads
     - Auto-export to Notion
     - Weekly review of bookmarks
  
     "If it matters, it leaves Slack."
     """
  
  4. Culture of documentation:
     """
     NORM:
     "Slack is for discussion. Wiki is for decisions."
  
     When someone says "we decided X" without link:
     "Can you link the doc where that's captured?"
     """
  
### **Symptoms**
  - Didn't we already decide this?
  - Important decisions only in Slack
  - New hires can't find context
  - Repeated discussions
### **Detection Pattern**
slack|chat|decision|document

## Meeting Creep - Calendar Colonization

### **Id**
meeting-creep
### **Severity**
high
### **Situation**
  Company starts with few meetings. "Let's sync weekly." Turns into
  daily standups. Then sprint planning. Then retros. Then 1:1s. Then
  cross-team syncs. Engineer looks at calendar: 20 hours of meetings
  per week. Actual work happens at night. Burnout follows.
  
### **Why**
  Meetings are easy to add, hard to remove. Each one feels necessary
  when added. Cumulative effect isn't felt until calendar is full.
  "This meeting is important" is always true in isolation. The problem
  is aggregate: a culture that defaults to sync.
  
### **Solution**
  1. Meeting audit:
     """
     QUARTERLY MEETING AUDIT:
  
     For every recurring meeting, answer:
     1. What decision does this enable?
     2. Could this be async?
     3. Who really needs to be here?
     4. What's the cost (hours × people × weeks)?
  
     If can't answer #1, cancel it.
     """
  
  2. Meeting budgets:
     """
     MEETING BUDGET BY ROLE:
  
     IC: Max 10 hours/week in meetings
     Manager: Max 15 hours/week
     Director: Max 20 hours/week
  
     Track it. Protect it. Over budget? Cancel something.
     """
  
  3. Async-first escalation:
     """
     BEFORE SCHEDULING MEETING:
  
     1. Can I write this in a doc? (Probably yes)
     2. Can I send a Loom? (Good for explanation)
     3. Do we need real-time discussion? (Rarely)
     4. Okay, schedule meeting
  
     Every meeting should pass the "Loom test."
     """
  
  4. No-meeting days:
     """
     PROTECTED TIME:
     - One or two no-meeting days per week
     - Company-wide, not optional
     - Maker time is sacred
  
     "Tuesday and Thursday are no-meeting days.
     If you schedule a meeting, you need VP approval."
     """
  
### **Symptoms**
  - I have no time to do actual work
  - Calendars full of recurring meetings
  - Meetings about meetings
  - Work happening evenings/weekends
### **Detection Pattern**
meeting|calendar|standup|sync

## Transparency Theater - Open But Not Honest

### **Id**
transparency-theater
### **Severity**
medium
### **Situation**
  Company announces: "We're transparent! Everything is open!" All-hands
  meetings happen. Metrics dashboards shared. But: real problems are
  never discussed. Layoffs announced suddenly. Revenue issues hidden
  until crisis. People feel gaslit - "But I thought we were transparent?"
  
### **Why**
  There's a difference between data transparency and truth transparency.
  Sharing metrics isn't the same as sharing reality. When companies
  perform transparency without practicing it, trust erodes faster than
  if they'd never claimed transparency at all.
  
### **Solution**
  1. Transparency audit:
     """
     WHAT SHOULD BE TRANSPARENT:
  
     ALWAYS SHARE:
     - Company metrics (revenue, burn, runway)
     - Strategic challenges and concerns
     - Major decisions and reasoning
     - What leadership is worried about
  
     OKAY TO HOLD TEMPORARILY:
     - Personnel issues (privacy)
     - Active negotiations (timing)
     - Unconfirmed rumors (accuracy)
  
     NEVER HIDE:
     - Financial distress
     - Existential risks
     - Coming layoffs (give max notice)
     """
  
  2. Lowlights ritual:
     """
     IN EVERY ALL-HANDS:
  
     "Here's what's keeping me up at night..."
  
     Not just highlights. The problems. The concerns.
     The things that aren't working. Employees know
     when things are hard - not sharing insults them.
     """
  
  3. Premortem practice:
     """
     SHARE THE RISKS:
  
     "If we fail this quarter, it'll be because of:
     1. [Risk 1]
     2. [Risk 2]
     3. [Risk 3]
  
     Here's what we're doing about each."
  
     This is real transparency.
     """
  
  4. Anonymous feedback channels:
     """
     CREATE SAFE CHANNELS:
     - Anonymous form for concerns
     - Regular review of submissions
     - Response in all-hands
     - No retaliation (and prove it)
  
     "Last week, someone asked about runway.
     Here's the honest answer..."
     """
  
### **Symptoms**
  - "We're transparent" without sharing problems
  - Surprise announcements
  - Metrics shared but not context
  - Disconnect between messaging and reality
### **Detection Pattern**
transparent|open|honest|all-hands

## Async Anxiety - Fear of Missing Out on Slack

### **Id**
async-anxiety
### **Severity**
medium
### **Situation**
  Team adopts async communication. But people are still on Slack all
  day. Anxious about missing something. Responding to messages immediately.
  Notifications never off. The async tools exist, but the sync behavior
  persists. No one gets deep work done.
  
### **Why**
  Async tools don't create async culture. Without explicit norms about
  response times and expectations, people assume they need to be always
  available. Fear of being seen as unresponsive keeps everyone tethered.
  The tool is async but the culture is still sync.
  
### **Solution**
  1. Explicit response time norms:
     """
     RESPONSE TIME EXPECTATIONS:
  
     Slack DM: Within 4 hours during work hours
     Slack Channel: Within 24 hours
     Email: Within 24-48 hours
     [URGENT] tag: Within 2 hours
  
     OUTSIDE WORK HOURS: No expectation
  
     "Not responding immediately is not only okay,
     it's expected."
     """
  
  2. Status discipline:
     """
     USE STATUS INDICATORS:
  
     🔴 Focus time - no interruptions
     🟡 Available but async preferred
     🟢 Available for sync
     ⚫ Offline - not working
  
     Respect others' status. Model it yourself.
     """
  
  3. Batch communication:
     """
     RECOMMENDED PATTERNS:
  
     Check Slack: 2-3 times per day
     Not: Always open in background
  
     Respond: In batches, not immediately
     Not: One-by-one as they arrive
  
     Deep work: Notifications off, status set
     Not: Half-attention always available
     """
  
  4. Leader modeling:
     """
     LEADERS MUST MODEL:
     - Delayed responses (not instant)
     - Offline weekends
     - Focus time visible on calendar
     - Not Slacking at 11pm
  
     "The CEO responds in 4 hours, not 4 minutes.
     You can too."
     """
  
### **Symptoms**
  - Slack always open
  - Immediate responses expected
  - People working all hours
  - Guilt about not responding fast enough
### **Detection Pattern**
async|response time|always on|notifications

## Announcement Fatigue - When Everything Is News

### **Id**
announcement-fatigue
### **Severity**
medium
### **Situation**
  Marketing hired someone - announcement. New Slack emoji - announcement.
  Coffee machine fixed - announcement. Every week, multiple #general posts.
  People stop reading. Then: real news (fundraising, major change) gets
  lost in the noise. "I didn't see that" becomes common.
  
### **Why**
  Attention is finite. When routine events are announced with the same
  fanfare as significant news, people can't distinguish importance.
  The announcement channel becomes noise. Real signals get buried.
  The company loses its broadcast channel.
  
### **Solution**
  1. Announcement tiers:
     """
     TIER 1 (#general, email, all-hands):
     - Fundraising, acquisition, major pivot
     - Leadership changes
     - Layoffs or major org changes
     - Company-wide policy changes
  
     TIER 2 (#general only):
     - New hires (leadership level)
     - Major product launches
     - Big customer wins
  
     TIER 3 (Team channels + weekly update):
     - Team new hires
     - Process changes
     - Minor launches
  
     TIER 4 (Weekly digest or not at all):
     - Office updates
     - Minor tool changes
     - Social events
     """
  
  2. Weekly digest format:
     """
     WEEKLY COMPANY DIGEST:
  
     📣 ANNOUNCEMENTS (if any)
     👋 NEW FACES
     🎉 WINS
     📅 UPCOMING
  
     One email/post. All the routine stuff.
     Save #general for real news.
     """
  
  3. Quality gate for announcements:
     """
     BEFORE POSTING TO #GENERAL:
  
     Would this affect everyone's work?
     Would someone be upset they missed it?
     Does this need action from most people?
  
     If not all yes: wrong channel.
     """
  
  4. Announcement calendar:
     """
     PACE ANNOUNCEMENTS:
     - No more than 2-3 #general posts/week
     - Space out timing
     - Major news: not Friday afternoon
  
     Protect the channel's signal strength.
     """
  
### **Symptoms**
  - 
  - I didn't see that announcement
  - Real news gets buried
  - People muting announcement channels
### **Detection Pattern**
announcement|#general|news|update

## Knowledge Graveyard - Docs That Nobody Reads

### **Id**
knowledge-graveyard
### **Severity**
high
### **Situation**
  Company invests in Notion/Confluence. Beautiful structure created.
  Policies documented. Processes written. Six months later: outdated,
  unused, unsearchable. New hires still ask questions that should be
  answered in docs. The wiki becomes a graveyard of good intentions.
  
### **Why**
  Documentation is easy to create, hard to maintain. Without ownership,
  docs decay. Without discoverability, they're never found. Without
  integration into workflow, they're forgotten. The effort of creating
  isn't matched by effort to maintain and use.
  
### **Solution**
  1. Document ownership:
     """
     EVERY DOC HAS:
     - Owner (named person)
     - Review date (quarterly minimum)
     - Last updated date (visible)
  
     NO ORPHAN DOCS:
     "If no one owns it, delete it."
     """
  
  2. Active maintenance:
     """
     QUARTERLY DOC REVIEW:
  
     All doc owners review their docs:
     - Still accurate?
     - Still needed?
     - Update or archive
  
     Dead docs: Move to /archive
     "Better no doc than wrong doc."
     """
  
  3. Integration into workflow:
     """
     MAKE DOCS UNAVOIDABLE:
  
     - Onboarding: Links to key docs
     - Slack bot: Search wiki on questions
     - Meeting notes: Link to relevant docs
     - "Read the doc" culture
  
     "Have you checked the wiki?"
     should be common phrase.
     """
  
  4. Searchability focus:
     """
     OPTIMIZE FOR SEARCH:
  
     - Clear titles (what someone would search)
     - Tags and categories
     - Opening summary with keywords
     - Cross-links to related docs
  
     TEST: Can new hire find X in 2 minutes?
     If no: fix structure or content.
     """
  
### **Symptoms**
  - Outdated documentation
  - New hires asking questions answered in docs
  - No one knowing what's in wiki
  - Duplicative documents
### **Detection Pattern**
documentation|wiki|notion|confluence|knowledge

## Remote Second-Class - Hybrid Inequity

### **Id**
remote-second-class
### **Severity**
high
### **Situation**
  Company is "hybrid." Office people have hallway conversations, whiteboard
  sessions, lunch decisions. Remote folks join meetings via laptop propped
  on table, can't see the whiteboard, miss the pre-meeting chat. Decisions
  get made in office without remote input. Remote people feel left out.
  
### **Why**
  Hybrid is hard because proximity creates advantage. It's natural to
  include the person next to you and forget the person on screen.
  Without deliberate systems, hybrid devolves into office-first with
  remote as afterthought. Remote workers disengage and leave.
  
### **Solution**
  1. Remote-first default:
     """
     EVEN IF SOME ARE IN OFFICE:
  
     - Default to video for all meetings
     - Everyone joins from their laptop
     - No side conversations in room
     - Whiteboard = shared digital tool
  
     "If one person is remote, everyone is remote."
     """
  
  2. Document everything:
     """
     HALLWAY CONVERSATIONS:
  
     If decision made in person:
     - Post summary in relevant channel
     - Invite remote input before finalizing
     - Never finalize without async window
  
     "No hallway decisions."
     """
  
  3. Equalize access:
     """
     REMOTE WORKERS GET:
     - Same equipment quality
     - Same information access
     - Same meeting experience
     - Async-friendly timing on announcements
  
     Budget for: Good camera, mic, monitor, chair.
     """
  
  4. Inclusion rituals:
     """
     IN EVERY MEETING:
  
     - Call on remote attendees specifically
     - Chat for questions (equalizer)
     - Recording for async review
     - Rotate meeting times for time zones
  
     "We're not inclusive by accident."
     """
  
### **Symptoms**
  - Remote workers missing context
  - In-office decisions made without remote input
  - Meeting quality worse for remote
  - Remote turnover higher than office
### **Detection Pattern**
remote|hybrid|office|distributed

## Onboarding Info-Dump - Drinking From The Firehose

### **Id**
onboarding-info-dump
### **Severity**
medium
### **Situation**
  New hire starts. Day 1: 50 tabs to read. Day 2: 10 meetings. Day 3:
  "Jump in!" Week 2: Overwhelmed, context-less, making mistakes that
  existing docs would have prevented - if they'd found them. New hire
  feels incompetent. The setup failed them.
  
### **Why**
  Information exists but the path through it doesn't. Onboarding often
  dumps everything at once instead of sequencing learning. New hires
  can't absorb it all. Critical information gets lost in the flood.
  They feel stupid when they're actually under-supported.
  
### **Solution**
  1. Staged information:
     """
     ONBOARDING PHASES:
  
     WEEK 1: SURVIVE
     - How to communicate (Slack, email)
     - Who to ask for help
     - Essential tools access
     - First task (small win)
  
     WEEK 2: ORIENT
     - Team context
     - Current projects
     - Key people to know
     - How decisions are made
  
     WEEK 3-4: CONTRIBUTE
     - Full context documents
     - Independent work begins
     - Feedback loop established
     """
  
  2. Onboarding buddy:
     """
     BUDDY ROLE:
     - Not manager (psychological safety)
     - Available for "dumb" questions
     - Check-ins: daily week 1, then weekly
     - Cultural guide, not just technical
  
     "Who do you ask about the thing that's
     too small to bother your manager with?"
     """
  
  3. Scavenger hunt approach:
     """
     INSTEAD OF: "Read these 20 docs"
  
     TRY: "Find the answer to these 5 questions"
     - Where is our product roadmap?
     - What are this month's OKRs?
     - How do you request time off?
     - What's the process for deploying code?
     - Who do you talk to about X?
  
     Learning by doing, not reading.
     """
  
  4. 30-60-90 check-ins:
     """
     STRUCTURED FEEDBACK:
  
     30 days: How's it going? What's confusing?
     60 days: Are you getting enough support?
     90 days: Ready for full independence?
  
     Written feedback from new hire:
     "What wasn't clear during onboarding?"
  
     Use this to improve the process.
     """
  
### **Symptoms**
  - New hires overwhelmed
  - Same questions from every new person
  - Long time to productivity
  - Onboarding docs unused
### **Detection Pattern**
onboarding|new hire|first day|ramp up