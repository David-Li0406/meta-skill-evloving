# Template Catalog

Complete catalog of all 11 PARA templates with their structure and content requirements.

---

## Template Classification

### Content-Heavy (Extensive body sections)

| Template | Body Sections | Focus |
|----------|---------------|-------|
| project | 9 | Goal tracking, milestones, next actions |
| resource | 11 | Progressive summarization, connections |
| weekly-review | 13 | Reflection phases, planning |
| daily | 10 | Intentions, log, reflection |
| trip-research | 7 | Decision framework, options |

### Metadata-Heavy (Frontmatter-focused)

| Template | Body Sections | Focus |
|----------|---------------|-------|
| task | 4 | Action metadata, dependencies |
| booking | 3 | Transaction tracking |
| checklist | 2 | Process items |
| itinerary-day | 3 | Day planning |
| capture | 5 | Quick resonance tagging |

### Hybrid (Balance of both)

| Template | Body Sections | Focus |
|----------|---------------|-------|
| area | 7 | Purpose, standards, routines |

---

## Template Details

### project

**Purpose:** Track time-bound initiatives with clear outcomes.

**Required Args:**
- `Project title` - Name of the project
- `Target completion date (YYYY-MM-DD)` - When it should be done
- `Area` - Which area this belongs to (wikilink format)

**Auto-filled:**
- `created` - Today's date
- `start_date` - Today's date

**Body Sections:**
1. Project Overview - Summary table
2. Why This Matters - Problem statement, urgency
3. Success Criteria - Measurable checkboxes (3-5 items)
4. Objectives - Key milestones
5. Key Resources - Links to related notes
6. Stakeholders - People involved
7. Progress Log - Timeline of updates
8. Next Actions - Immediate physical actions
9. Risks & Blockers - What could prevent completion
10. Notes - Additional context

---

### area

**Purpose:** Define ongoing responsibilities without end dates.

**Required Args:**
- `Area title` - Name of the area

**Auto-filled:**
- `created` - Today's date

**Body Sections:**
1. Overview - What this area encompasses
2. Standards to Maintain - Quality expectations (checklist)
3. Current Projects - Dataview query auto-populated
4. Key Metrics - Success measures table
5. Related Resources - Reference materials
6. Routines & Habits - Daily/weekly/monthly activities
7. Review Questions - Weekly review prompts
8. Notes - Ongoing observations

---

### resource

**Purpose:** Capture and distill knowledge from external sources.

**Required Args:**
- `Resource title` - Title of the resource
- `Source type (book/article/video/course/podcast/etc.)` - Content type
- `Primary area this relates to` - Related area (wikilink format)

**Optional Args:**
- `Source URL (optional)` - Link to source
- `Author (optional)` - Creator name

**Auto-filled:**
- `created` - Today's date

**Body Sections:**
1. Source Information - Metadata table
2. Summary - Core message (2-3 sentences)
3. Key Insights - Most valuable ideas (numbered)
4. Notable Quotes - Passages worth remembering
5. Progressive Summary
   - Layer 1: Captured Notes
   - Layer 2: Bold Passages
   - Layer 3: Highlighted Core
   - Layer 4: Executive Summary
6. Connections - Related notes, contradictions, supports
7. Action Items - What to DO with this knowledge
8. Questions Raised - What you still want to know
9. Personal Reflection - How this changes your thinking

---

### task

**Purpose:** Track actionable items with specific outcomes.

**Required Args:**
- `Task title` - Name of the task
- `Priority (low/medium/high/urgent)` - Task priority
- `Effort (small/medium/large)` - Effort estimate

**Optional Args:**
- `Task type (task/reminder/habit/chore)` - Category (default: task)
- `Project (optional)` - Parent project (wikilink format)
- `Area (optional)` - Related area (wikilink format)
- `Start date (YYYY-MM-DD)` - When to start
- `Due date (YYYY-MM-DD)` - When it's due

**Auto-filled:**
- `created` - Today's date

**Body Sections:**
1. Quick Info - Metadata table
2. Description - What is this task, desired outcome
3. Success Criteria - Definition of done
4. Dependencies - Depends on, blocks, type
5. Task Details - Type-specific fields
6. Notes - Context, resources needed
7. Related - Links to project/area

---

### capture

**Purpose:** Quick inbox capture with resonance tagging.

**Required Args:**
- `Title` - Brief descriptive title
- `Content` - The raw content being saved
- `Captured from (thought/article/conversation/etc.)` - Source type
- `Resonance (inspiring/useful/personal/surprising)` - Why it matters
- `Urgency (high/medium/low)` - Time sensitivity

**Auto-filled:**
- `created` - Timestamp with time

**Body Sections:**
1. Capture - Raw content
2. Why I Saved This - Resonance explanation
3. Context - Source, date
4. Processing Notes - PARA decision, destination, tags
5. Connections - Related notes
6. Next Actions - Process within 48 hours

---

### daily

**Purpose:** Daily planning and reflection journal.

**Required Args:** None (auto-generates from date)

**Auto-filled:**
- `title` - Today's date (YYYY-MM-DD)
- `created` - Today's date

**Body Sections:**
1. Morning Intentions
   - Today's Focus - ONE thing for success
   - Top 3 Priorities - Checkboxes
   - Energy & Mood - Rating
2. Daily Log
   - Captures - Quick thoughts
   - Meetings & Conversations - Key takeaways
   - Progress Made - Accomplishments
   - Blockers & Challenges - What got in the way
3. Evening Reflection
   - What Went Well - Celebrate wins
   - What Could Be Improved - Learning opportunities
   - Gratitude - Three things
   - Tomorrow's Setup - Next day prep
4. Links - Related notes, active projects, areas

---

### weekly-review

**Purpose:** Weekly GTD-style review and planning.

**Required Args:** None (auto-generates from week)

**Auto-filled:**
- `title` - Week identifier (YYYY-Www)
- `created` - Today's date
- `week` - ISO week number

**Body Sections:**
1. Phase 1: Clear the Mind
   - Brain Dump - Everything out of head
   - Inbox Status - Processing checklist
2. Phase 2: Review Calendar
   - Past Week - Day-by-day key events
   - Upcoming Week - What's scheduled
3. Phase 3: Review Projects
   - Active Projects Status - Dataview query
   - Project Review - Status table
   - Stale Projects - No updates 2+ weeks
   - Projects to Archive
4. Phase 4: Review Areas
   - Area Check-In - Attention table
5. Phase 5: Review Goals
   - This Week's Wins
   - This Week's Challenges
   - Lessons Learned
6. Phase 6: Express
   - Ideas Ready to Create
   - Patterns Noticed
7. Phase 7: Plan Next Week
   - Top 3 Priorities
   - Projects to Focus On
   - Habits to Maintain
   - Appointments to Schedule
8. Weekly Statistics - Metrics table
9. Notes - Additional reflections

---

### booking

**Purpose:** Track transactions and payment confirmations.

**Required Args:**
- `Booking title` - Description of booking
- `Booking type (flight/hotel/event/rental/other)` - Category
- `Amount` - Cost
- `Currency` - Payment currency
- `Booking reference` - Confirmation number

**Optional Args:**
- `Payment method` - How paid
- `Start date` - When it begins
- `End date` - When it ends

**Body Sections:**
1. Booking Details - Metadata table
2. Payment Information - Transaction details
3. Notes - Additional information

---

### checklist

**Purpose:** Reusable process templates.

**Required Args:**
- `Checklist title` - Name of the checklist
- `Category` - Type of checklist

**Body Sections:**
1. Checklist Items - Grouped by category
2. Notes - Process tips

---

### itinerary-day

**Purpose:** Day-by-day travel planning.

**Required Args:**
- `Day title` - Day description
- `Date (YYYY-MM-DD)` - Specific date
- `Location` - Where you'll be

**Body Sections:**
1. Schedule - Time-based activities
2. Logistics - Transport, accommodation
3. Notes - Additional details

---

### trip-research

**Purpose:** Decision framework for travel options.

**Required Args:**
- `Trip title` - Name of the trip
- `Destination` - Where you're going
- `Travel dates` - When

**Body Sections:**
1. Overview - Trip summary
2. Options Comparison - Decision matrix
3. Research Notes - Findings
4. Budget - Cost breakdown
5. Logistics - Flights, accommodation, transport
6. Packing List - What to bring
7. Notes - Additional context

---

## Content Generation Priority

When generating content, prioritize sections in this order:

### High Impact (Generate first)
- Why This Matters / Purpose
- Success Criteria / Definition of Done
- Next Actions / Immediate steps
- Key Insights / Summary

### Medium Impact (Add detail)
- Objectives / Milestones
- Risks & Blockers
- Connections / Related notes
- Action Items

### Lower Impact (Optional)
- Progress Log (start with initial entry)
- Notes (leave for organic growth)
- Statistics / Metrics (placeholder)
