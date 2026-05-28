---
name: gtd
description: Research and execute tasks from Computer and Deep Work projects with intelligent caching and delegation
---

# GTD - Get Things Done

Research and execute tasks from Computer and Deep Work projects with intelligent caching and delegation.

## Tool Selection

| Tool | When to Use | MCP Function |
|------|-------------|--------------|
| **Firecrawl** | URL scraping, quick single-page reads | `mcp__firecrawl-mcp__firecrawl_scrape` |
| **Tavily** | Deep research, multi-source comprehensive searches | `mcp__tavily__tavily_search` |
| **BrowserBase** | Browser automation, login-required sites, interactive pages | `mcp__browserbase__*` |
| **Zapier Gmail** | Draft/send emails, search inbox for context | `mcp__zapier__gmail_*` |
| **Zapier Calendar** | Schedule events, block time | `mcp__zapier__google_calendar_*` |
| **Zapier Docs** | Create/find documents | `mcp__zapier__google_docs_*` |

### Tool Details

**Firecrawl** - Fast URL resolution and page scraping:
- Use for: URL tasks, quick page summaries, video metadata
- Function: `mcp__firecrawl-mcp__firecrawl_scrape`
- Best for: Single pages, YouTube videos, articles, GitHub repos

**Tavily** - Deep research with comprehensive results:
- Use for: "Research X" tasks, DD (Deep Dive) requests, competitive analysis
- Function: `mcp__tavily__tavily_search`
- Best for: Multi-source research, current events, company research, market analysis

**BrowserBase** - Browser automation for interactive tasks:
- Use for: Login-required sites, JavaScript-heavy pages, form filling, screenshots
- Functions: `mcp__browserbase__*` (navigate, click, type, screenshot, etc.)
- Best for: Social media monitoring, authenticated sites, complex web apps, visual verification

**Zapier Gmail** - Email operations via Google Workspace:
- `mcp__zapier__gmail_send_email` - Send drafted emails
- `mcp__zapier__gmail_create_draft` - Save as draft for user review
- `mcp__zapier__gmail_find_email` - Search inbox for context (prior conversations)

---

## ⚠️ CRITICAL: Email Formatting Rules

**Zapier Gmail requires HTML formatting.** Plain text newlines (`\n`) are IGNORED and will render as one giant paragraph.

### Always Include These Parameters
```javascript
{
  body_type: "html",  // REQUIRED for paragraph breaks
  body: "<p>First paragraph</p><p>Second paragraph</p>",
  // ... other fields
}
```

### HTML Formatting Reference

| Need | Use |
|------|-----|
| Paragraph break | `</p><p>` or `<p>...</p>` |
| Line break within paragraph | `<br>` |
| Bullet list | `<ul><li>Item</li></ul>` |
| Bold | `<strong>text</strong>` |
| Link | `<a href="url">text</a>` |
| Signature line break | `Name<br>Title` |

### Signature Formats

**External emails** (cold outreach, follow-ups, meeting requests):
```html
<p>-Andrew<br>
___<br>
<a href="https://www.tiny.com">www.tiny.com</a></p>
```

**Internal/colleague emails** (delegate, ask questions):
```html
<p>Thanks,<br>
Andrew</p>
```

**Intro emails** (casual, connecting two people):
```html
<p>-Andrew</p>
```

### Common Mistakes to AVOID

1. **Plain newlines** - `\n` does nothing, use `<br>` or `<p>`
2. **Missing body_type** - Defaults to plain text, breaks all formatting
3. **Wall of text** - Always break into 3-5 short paragraphs max
4. **Over-formatting** - Keep HTML minimal, no inline styles

---

## Research Cache System

**All research results are cached** to `~/claudesync/servers/super-things/data/research-cache.json`:
- Results persist for 7 days
- Use `/gtd resume` to continue a previous session
- Say "details N" to expand cached findings

## Workflow

### Step 1: Check for Previous Session
```bash
cat ~/claudesync/servers/super-things/data/research-cache.json
```
If recent session exists (< 24h), ask: "Continue previous session or start fresh?"

### Step 2: Fetch Tasks
- Computer: `mcp__things-mcp__things_get_project` with `LDhUsibk3dp2ZPioQySSiu`
- Deep Work: `mcp__things-mcp__things_get_project` with `WamuBi2sFwbUwpXz9NZetP`

### Step 3: Categorize Tasks

| # | Category | Pattern | Tool | Action |
|---|----------|---------|------|--------|
| 1 | **URL tasks** | Contains http://, https://, youtu.be | Firecrawl | Scrape page, summarize content |
| 2 | **Research/DD** | "Research X", "DD on X", "Look into X" | Tavily | Deep multi-source search |
| 3 | **Browser tasks** | "Check X dashboard", "Screenshot X", login-required | BrowserBase | Navigate, interact, capture |
| 4 | **Delegate** | D command or "Delegate to X" | Zapier Gmail | Draft delegation email |
| 5 | **Introduction** | "Intro X to Y", "Connect X with Y" | Zapier Gmail | Draft intro email, CC both |
| 6 | **Cold outreach** | "Email [business]", "Reach out to X", "Contact Y" | Zapier Gmail | Draft acquisition/outreach email |
| 7 | **Follow-up** | "Follow up with X", "Check in with Y", "Bump X" | Zapier Gmail | Draft follow-up email |
| 8 | **Reply** | "Reply to X", "Respond to [email]" | Zapier Gmail | Draft reply email |
| 9 | **Meeting request** | "Schedule call with X", "Set up meeting with Y" | Zapier Gmail | Draft meeting request email |
| 10 | **Contact lookup** | "Find email for X", "Get contact for Y" | Gmail → Tavily | Search inbox, then web |
| 11 | **Calendar** | "Block time for X", "Schedule Y", "Add to calendar" | Zapier Calendar | Create calendar event |
| 12 | **Documents** | "Create doc for X", "Find document about Y" | Zapier Docs/Drive | Create or find document |
| 13 | **Buy/Order** | "Buy X", "Order Y", "Purchase Z tickets" | Tavily | Search for product, return link+price |
| 14 | **Book appointment** | "Book X appointment", "Schedule Y scan" | Tavily | Find booking page/phone |
| 15 | **Sign up/Register** | "Sign up for X", "Register for Y conference" | Tavily | Find registration page |
| 16 | **Watch/Read** | "Watch X video", "Read Y article", "Review Z" | Firecrawl | Scrape and summarize content |
| 17 | **Send to person** | "Send X to Y", "Share Z with W" | Zapier Gmail | Draft sharing email |
| 18 | **Ask person** | "Ask X about Y", "Ask X to do Z" | Zapier Gmail | Draft question email |
| 19 | **Find/Search** | "Find X", "Look for Y", "Search for Z" | Gmail/Tavily | Search inbox or web |
| 20 | **Cancel/Unsubscribe** | "Cancel X subscription", "Unsubscribe from Y" | Gmail/Tavily | Find cancellation page |
| 21 | **Invite** | "Invite X to Y", "Add X to event" | Zapier Gmail | Draft invitation email |
| 22 | **Create content** | "Create X playlist", "Draft Y tweet", "Write Z" | Claude + Tavily | Research then draft |
| 23 | **Travel/Booking** | "Book flight to X", "Find hotel in Y", "Restaurant Z" | Tavily | Search and compare options |
| 24 | **Quick analysis** | "Calculate X", "Compare Y vs Z", "Analyze options" | Claude thinking | No tools, direct analysis |
| 25 | **Not helpable** | Physical tasks, calls, in-person meetings | Skip | Mark for manual handling |

### Step 4: Execute Research (Batched)

**Rate limit protection**: Max 8 parallel agents per batch.

For each task type:

**URL Tasks** (Firecrawl):
1. Scrape URL with `mcp__firecrawl-mcp__firecrawl_scrape`
2. Extract title, description, key content
3. Summarize with TLDR bullets
4. Cache results immediately

**Research Tasks** (Tavily):
1. Search with `mcp__tavily__tavily_search`
2. Synthesize findings from multiple sources
3. Include specific facts, numbers, names
4. Cache results immediately

**Browser Tasks** (BrowserBase):
1. Launch browser session with `mcp__browserbase__*`
2. Navigate to target URL
3. Handle login if needed (use saved credentials or ask user)
4. Perform action (screenshot, extract data, fill form)
5. Cache results with screenshots if relevant

**Email/Intro Tasks** (Zapier):
1. Search inbox for prior context: `mcp__zapier__gmail_find_email`
2. Draft email based on task + context
3. Present draft for approval
4. On approval: `mcp__zapier__gmail_send_email`

### Step 5: Display Results (Rich TLDR Format)

**Time estimates** (show before research):
```
Research tasks found: [N]

Estimated time breakdown:
├─ URL tasks (5): ~10 min (fast scrapes)
├─ Research tasks (3): ~25 min total
│   ├─ "Research competitor pricing" (~15 min)
│   ├─ "Find best practices for X" (~10 min)
├─ Email tasks (2): ~5 min
└─ Total: ~40 min

Proceed with research? [Y/n]
```

**Time estimation rules:**
- URL tasks: ~2 min each (fast Firecrawl scrape)
- Research tasks: ~5-20 min each depending on complexity
  - Simple lookup: ~5 min ("What is X", "Find X contact")
  - Analysis: ~10 min ("Compare X vs Y", "Find best X")
  - Deep research: ~15-20 min ("Comprehensive analysis of X")
- Email tasks: ~2-3 min each (draft generation)
- Browser tasks: ~5-10 min each (navigation, interaction)

**After research:**
```
Research Complete: [N] tasks processed

┌─ 1 ─────────────────────────────────────────────────────────
│  [Task Title]
│
│  • Key finding 1 with specific details
│  • Key finding 2 with numbers/facts
│  • Key finding 3 with actionable insight
│  • Additional bullet if needed
│  • Source: [where info came from]
│
├─ 2 ─────────────────────────────────────────────────────────
│  https://example.com/article (URL task)
│
│  • Article title: "How to Build X"
│  • Main thesis: [summary of what the link contains]
│  • Key points from the actual page content
│  • Why this was saved (inferred from context)
│  • Source: Firecrawl (visited link)
│
├─ 3 ─────────────────────────────────────────────────────────
│  Research competitor pricing
│
│  • Found 5 competitors: Acme ($15/mo), Beta ($25/mo)...
│  • Enterprise tiers range $100-500/seat
│  • Key differentiator: only Gamma has API at base tier
│  • Annual discounts: 15-25% typical
│  • Sources: Tavily (G2, Capterra, pricing pages)
```

**Display rules:**
- Use as many bullets as needed to capture key findings
- Keep each bullet concise but informative (TLDR style)
- For URL tasks: summarize actual content from the page
- Always include sources and which tool was used

## Triage Commands

After research display, user responds with commands:

| Command | Action | Example |
|---------|--------|---------|
| `C` | Complete task in Things | `1: C` |
| `C [note]` | Complete with note | `1: C already handled last week` |
| `D [person]` | Delegate - draft email via Zapier | `2: D Brianna` |
| `D [person] [modifier]` | Delegate with context | `2: D Brianna within the next week` |
| `DD` | Deep Dive - use **Tavily** for expanded research | `3: DD` |
| `DD [focus]` | Deep Dive with specific focus | `3: DD focus on enterprise pricing` |

**Example triage response:**
```
1: C
2: D Brianna please handle by Friday
3: DD focus on North American competitors only
4-6: C
7: D John can you review this contract
8: C noted for future reference
```

**Default behavior**: Tasks without commands are kept in Things with notes updated.

## Command Execution

### C (Complete)
Mark task complete in Things using `mcp__things-mcp__things_update_todo`.

### D (Delegate)
1. Parse: `D [person] [optional modifier]`
2. Search inbox for person's email: `mcp__zapier__gmail_find_email`
3. Draft email via Zapier:
   ```
   To: [person's email]
   Subject: Task: [task title]

   Hi [Person],

   Could you help with this? [task description]

   [Include research findings if relevant]

   [modifier context if provided, e.g., "Ideally by Friday"]

   Thanks,
   Andrew
   ```
4. Show draft for approval
5. On approval: Send via `mcp__zapier__gmail_send_email`
6. Mark Things task complete

### DD (Deep Dive)
1. Parse: `DD [optional focus]`
2. Launch **Tavily** deep research with expanded queries
3. Use multiple search queries to get comprehensive coverage
4. If focus provided, concentrate searches on that aspect
5. Update cache with expanded findings
6. Display new results with Tavily sources

## URL/Link Handling

**Critical**: If a task contains a URL, use **Firecrawl** to scrape:

1. Scrape with `mcp__firecrawl-mcp__firecrawl_scrape`
2. Extract and summarize the actual page content
3. Include:
   - What the page/video/article is about
   - Key points and takeaways
   - Why the user likely saved this
4. Mark source as "Firecrawl (visited link)"

Example URL task handling:
```
Task: "https://youtu.be/abc123"

Using Firecrawl to scrape YouTube page:
1. Get video title, description, duration
2. If transcript available, summarize key points
3. Infer why saved (topic, speaker, relevance)

Output:
• Video: "The Future of AI" by Sam Altman (45 min)
• Key points: GPT-5 roadmap, multimodal focus, AGI timeline
• Discusses compute scaling concerns
• Likely saved for: AI strategy research
• Source: Firecrawl (visited link)
```

## Email Templates by Type

**IMPORTANT**: All emails MUST use `body_type: "html"` and HTML tags for formatting.

---

### 1. Delegate Emails (D command)

**Trigger**: `D [person] [optional context]`
- Example: `D Brianna please handle by Friday`
- Example: `D John can you review this contract`

**Template**:
```html
body_type: "html"

<p>Hi [Person],</p>

<p>Could you help with this? [task description]</p>

<p>[Research findings if relevant - formatted as <ul><li> bullets]</p>

<p>[Modifier context if provided, e.g., "Ideally by Friday"]</p>

<p>Thanks,<br>
Andrew</p>
```

**Rules**:
- Subject: "Task: [shortened title]"
- Include research findings if task was researched
- Add deadline/urgency from modifier naturally
- **No Tiny signature** - these are internal/colleague emails

---

### 2. Introduction Emails

**Trigger**: "Intro X to Y", "Connect X with Y" tasks

**Template**:
```html
body_type: "html"

<p>Hi [Person A],</p>

<p>Wanted to intro you to [Person B]. [Person B] is the [role] of [Company] and based in [Location]. I think you guys would hit it off.</p>

<p>[Person B], meet my friend [Person A]. [Person A] runs [Company] and [brief personal context]. You guys should grab a coffee.</p>

<p>I'll leave you to it :-)</p>

<p>-Andrew</p>
```

**Rules**:
- Subject: "Introduction: [Person A] <> [Person B]"
- CC both parties
- Keep casual/friendly tone ("my friend", "hit it off", "grab a coffee")
- Include location for context
- Search inbox for context on both people first

---

### 3. Cold Outreach / Acquisition Emails

**Trigger**: "Email [business/person]", "Reach out to X", "Contact Y about Z"

**For acquisition/business interest:**
```html
body_type: "html"

<p>Hi [Name],</p>

<p>Not sure if you're familiar with me, but I own Tiny, a public holding company. We own about 30 businesses across a variety of industries and we're based in Victoria.</p>

<p>I was wondering if you'd ever consider selling [Company]. We're interested in the [industry/space] :-)</p>

<p>-Andrew</p>
```

**For casual coffee/meeting (when traveling):**
```html
body_type: "html"

<p>Hi [Name],</p>

<p>I'm Andrew Wilkinson - I run a holding company called Tiny that acquires and operates great businesses long-term. I'm in [Location] until [Date] and came across [Business]. [Specific compliment about what impressed you].</p>

<p>I'd love to buy you a coffee while I'm here and learn more about the business. Not sure if you've ever thought about what's next, but if you're ever open to exploring options, I'd be interested in talking.</p>

<p>No pressure either way - just thought it was worth reaching out while I'm on the island.</p>

<p>-Andrew<br>
___<br>
<a href="https://www.tiny.com">www.tiny.com</a></p>
```

**Rules**:
- Subject: Short, intriguing (e.g., "Coffee while I'm in [City]?", "[Company]?")
- Keep it brief - 2-3 paragraphs max
- Casual tone with smiley where appropriate :-)
- Direct ask, low pressure
- Include Tiny signature for external outreach

---

### 4. Follow-up Emails

**Trigger**: "Follow up with X", "Check in with Y", "Bump [person]"

**Template**:
```html
body_type: "html"

<p>Hi [Name],</p>

<p>Just wanted to follow up on [previous topic/meeting]. [Specific reference to last interaction]</p>

<p>[Any update or new context if relevant]</p>

<p>[Soft re-ask or next step]</p>

<p>-Andrew<br>
___<br>
<a href="https://www.tiny.com">www.tiny.com</a></p>
```

**Rules**:
- Search inbox first for last conversation (`mcp__zapier__gmail_find_email`)
- Reference specific details from prior exchange
- Keep shorter than original outreach

---

### 5. Reply/Response Drafts

**Trigger**: "Reply to X", "Respond to [email about Y]"

**Template** (varies based on context):
```html
body_type: "html"

<p>[Opening acknowledgment]</p>

<p>[Main response content]</p>

<p>[Next steps or closing]</p>

<p>-Andrew<br>
___<br>
<a href="https://www.tiny.com">www.tiny.com</a></p>
```

**Rules**:
- Always search inbox for the thread first
- Match tone/formality of incoming email
- Keep response proportional to original

---

### 6. Research Sharing Emails

**Trigger**: After DD (Deep Dive), user wants to share findings

**Template**:
```html
body_type: "html"

<p>Hi [Name],</p>

<p>I looked into [topic] - here's what I found:</p>

<ul>
<li>[Finding 1 with specifics]</li>
<li>[Finding 2 with numbers/facts]</li>
<li>[Finding 3 with actionable insight]</li>
</ul>

<p>[Conclusion or recommendation]</p>

<p>Let me know if you want me to dig deeper on any of this.</p>

<p>-Andrew<br>
___<br>
<a href="https://www.tiny.com">www.tiny.com</a></p>
```

**Rules**:
- Use `<ul><li>` for bullet points
- Include sources inline if relevant
- Summarize, don't dump raw research

---

### 7. Meeting Request Emails

**Trigger**: "Schedule call with X", "Set up meeting with Y", "Book time with Z"

**Template**:
```html
body_type: "html"

<p>Hi [Name],</p>

<p>[Context for why meeting - 1 sentence]</p>

<p>Would you have 30 minutes in the next week or two to [specific purpose: chat, catch up, discuss X]?</p>

<p>Happy to work around your schedule.</p>

<p>-Andrew<br>
___<br>
<a href="https://www.tiny.com">www.tiny.com</a></p>
```

**Rules**:
- Keep short - just the ask
- Suggest timeframe but stay flexible
- Include specific purpose for the meeting
- Don't over-explain

---

### 8. Send/Share Emails

**Trigger**: "Send X to Y", "Share Z with W"

**Template**:
```html
body_type: "html"

<p>Hi [Name],</p>

<p>Wanted to share this with you - [context for why]:</p>

<p>[Link or content]</p>

<p>-Andrew</p>
```

**Rules**:
- Find/locate the thing first (link, file, info)
- Brief context for why sharing
- Keep simple and direct

---

### 9. Ask/Question Emails

**Trigger**: "Ask X about Y", "Ask X to do Z"

**Template**:
```html
body_type: "html"

<p>Hi [Name],</p>

<p>[Question or request in natural language]</p>

<p>Thanks,<br>
Andrew</p>
```

**Rules**:
- Keep short and direct
- One question/request per email ideally
- No Tiny signature for internal asks

---

### 10. Invitation Emails

**Trigger**: "Invite X to Y", "Add X to event"

**Template**:
```html
body_type: "html"

<p>Hi [Name],</p>

<p>Would love to have you at [Event] - [brief description].</p>

<p>Details:<br>
Date: [Date]<br>
Location: [Place]<br>
[Any other relevant info]</p>

<p>Let me know if you can make it!</p>

<p>-Andrew</p>
```

**Rules**:
- Include all key details (date, time, location)
- Brief context on why inviting
- Clear call to action

---

## Non-Email Action Types

### Company/Founder Research

**Trigger**: "Research [Company]", "DD on [Business]", "Look into [Founder]"

**Action**: Use Tavily for deep research

**Return format**:
```
Company: [Name]
Industry: [Sector]
Location: [HQ]
Founder(s): [Names + backgrounds]
Revenue: [If available]
Key facts:
- [Fact 1]
- [Fact 2]
- [Fact 3]
Why interesting: [Relevance to Tiny]
```

**Rules**:
- Always try to find: revenue, employee count, funding, founders
- Check for recent news/press
- Note any acquisition signals (founder age, no recent funding, etc.)

---

### Contact Lookup

**Trigger**: "Find email for X", "Get contact for Y", "Look up Z's email"

**Action**:
1. Search inbox first (`mcp__zapier__gmail_find_email`)
2. If not found, use Tavily for "[Name] email" or "[Name] [Company] contact"
3. Check LinkedIn via BrowserBase if needed

**Return format**:
```
Found: [email@domain.com]
Source: [inbox/LinkedIn/website]
Confidence: [high/medium/low]
```

---

### Calendar Tasks

**Trigger**: "Block time for X", "Schedule Y", "Add Z to calendar"

**Action**: Use `mcp__zapier__google_calendar_create_detailed_event`

**Rules**:
- Default duration: 30 min for calls, 60 min for meetings
- Include context in description
- Ask for time if not specified

---

### Document Tasks

**Trigger**: "Create doc for X", "Find document about Y", "Draft proposal for Z"

**Action**:
- Find: `mcp__zapier__google_docs_find_a_document` or `mcp__zapier__google_drive_find_a_file`
- Create: `mcp__zapier__google_docs_create_document_from_text`

**Rules**:
- Search before creating (might already exist)
- Use descriptive titles
- Include date in title for time-sensitive docs

---

### Buy/Order/Purchase Tasks

**Trigger**: "Buy X", "Order Y", "Purchase Z tickets"

**Action**:
1. Search for product/tickets online via Tavily
2. Find best source (Amazon, official site, etc.)
3. Provide link + price + recommendation

**Return format**:
```
Product: [Name]
Best option: [Link]
Price: $X
Notes: [Any relevant info - shipping, availability, etc.]
```

**Rules**:
- For tickets: Check official source first, then resellers
- Include price comparison if relevant
- Flag if out of stock or unavailable

---

### Book/Schedule Appointments

**Trigger**: "Book X appointment", "Schedule Y scan", "Book fitness class"

**Action**:
1. Research the service provider via Tavily
2. Find booking page/phone number
3. If online booking available, provide direct link
4. If phone only, provide number and suggested script

**Return format**:
```
Provider: [Name]
Booking: [Link] or [Phone number]
Hours: [If relevant]
Next steps: [What to do]
```

**Rules**:
- Prefer online booking links over phone
- Include wait times if known
- Note any prep requirements (fasting, etc.)

---

### Sign Up/Register Tasks

**Trigger**: "Sign up for X", "Register for Y conference"

**Action**:
1. Find official registration page via Tavily
2. Check dates, pricing, availability
3. Provide registration link

**Return format**:
```
Event/Service: [Name]
Dates: [If applicable]
Cost: $X
Register: [Link]
Deadline: [If applicable]
```

---

### Watch/Read/Review Tasks

**Trigger**: "Watch X video", "Read Y article", "Review Z website"

**Action**:
1. Use Firecrawl to scrape the content
2. Summarize key points
3. Note why it was likely saved

**Return format**:
```
Title: [Name]
Type: [Video/Article/Book/Website]
Summary:
- [Key point 1]
- [Key point 2]
- [Key point 3]
Why saved: [Inferred relevance]
Link: [URL]
```

**Rules**:
- For books: Include where to buy (Amazon, etc.)
- For videos: Include duration
- Mark as "watched/read" summary, not full content

---

### Find/Search Tasks

**Trigger**: "Find X", "Look for Y", "Search for Z"

**Action**:
1. Search inbox first if it's an email/document
2. Use Tavily for web searches
3. Use Firecrawl for specific URLs

**Return format**:
```
Found: [Result]
Source: [Where found]
Link: [If applicable]
```

---

### Cancel/Unsubscribe Tasks

**Trigger**: "Cancel X subscription", "Unsubscribe from Y"

**Action**:
1. Search inbox for account emails to find service
2. Find cancellation page/process via Tavily
3. Provide instructions or link

**Return format**:
```
Service: [Name]
Cancel here: [Link to cancellation page]
Process: [Steps if not straightforward]
Note: [Any retention offers, refund info, etc.]
```

**Rules**:
- Look for "cancel subscription" or "manage account" pages
- Note if phone call required
- Flag any early termination fees

---

### Create/Draft Content Tasks

**Trigger**: "Create X playlist", "Draft Y tweet", "Write Z post"

**Action**:
1. Research/gather relevant info
2. Create the content
3. Present for review

**For tweets/social posts**:
```
Draft tweet:
"[Content under 280 chars]"

Alt versions:
1. [Variation 1]
2. [Variation 2]
```

**Rules**:
- For playlists: Suggest songs, provide Spotify/Apple Music links
- For tweets: Keep punchy, offer variations
- For blog posts: Outline first, then draft

---

### Travel/Booking Tasks

**Trigger**: "Book flight to X", "Find hotel in Y", "Reserve restaurant Z"

**Action**:
1. Search for options via Tavily
2. Compare prices/ratings
3. Provide top recommendations

**Return format**:
```
Destination: [Place]
Dates: [If specified]

Option 1: [Name]
- Price: $X
- Rating: X/5
- Link: [Booking link]

Option 2: [Name]
- Price: $Y
- Rating: Y/5
- Link: [Booking link]

Recommendation: [Which one and why]
```

**Rules**:
- For flights: Check Google Flights, airline direct
- For hotels: Check hotel direct, Expedia, Booking.com
- For restaurants: Check Resy, OpenTable, direct
- Note cancellation policies

---

### Quick Analysis

**Trigger**: "Calculate X", "Compare Y vs Z", "Analyze options for W"

**Action**: Claude thinking (no external tools needed)

**Return format**:
```
Analysis: [Topic]

Option A: [Details]
- Pro: [X]
- Con: [Y]

Option B: [Details]
- Pro: [X]
- Con: [Y]

Recommendation: [Pick with reasoning]
```

---

### Social Media / Screenshots

**Trigger**: "Check X's Twitter", "Screenshot Y's LinkedIn", "See what Z posted"

**Action**: Use BrowserBase to navigate and screenshot

**Rules**:
- Take screenshot for visual verification
- Extract key text/posts
- Note follower counts, recent activity

---

## Cache Management

### Cache Structure
```json
{
  "last_updated": "ISO-timestamp",
  "sessions": {
    "session-uuid": {
      "started_at": "ISO-timestamp",
      "tasks_researched": 32,
      "results": [
        {
          "task_id": "Things-UUID",
          "task_title": "Research X",
          "researched_at": "ISO-timestamp",
          "tool_used": "tavily|firecrawl|zapier",
          "findings": "Full research text with all bullets...",
          "sources": ["url1", "url2"],
          "user_decision": "complete|delegate|deepdive|pending",
          "notes_updated": true
        }
      ]
    }
  }
}
```

### Cache Operations
- **Write**: After each research batch completes
- **Read**: On `/gtd resume` or "details N" request
- **Cleanup**: Remove sessions older than 7 days

## Resume Previous Session

If user says `/gtd resume`:
1. Read cache file
2. Find most recent session
3. Display previous results (from cache, not re-researched)
4. Allow user to continue triage where they left off

## Parallel Execution Rules

**Rate limit protection:**
- Max 8 parallel agents per batch
- Wait for batch completion before launching next
- Retry rate-limited tasks in next batch
- Use haiku model for research agents (faster, cheaper)

```
Batch 1: [task 1-8] → wait → check failures
Batch 2: [task 9-16 + retries] → wait → check
Batch 3: [remaining + retries] → etc.
```

## Project IDs
- Computer: `LDhUsibk3dp2ZPioQySSiu`
- Deep Work: `WamuBi2sFwbUwpXz9NZetP`

## Execution

Now execute the GTD workflow:
1. Check for previous session in cache
2. Fetch tasks from both projects
3. Categorize tasks by type (URL → Firecrawl, Research → Tavily, Email → Zapier)
4. Execute research with appropriate tools
5. Cache results immediately
6. Display rich TLDR summaries with tool sources
7. Process C/D/DD commands
8. Update cache with decisions
