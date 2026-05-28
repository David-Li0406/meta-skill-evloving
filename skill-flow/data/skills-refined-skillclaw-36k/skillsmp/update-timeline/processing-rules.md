# Processing Rules - Deep Understanding Requirements

This document separates MECHANICAL steps (follow exactly) from INTERPRETIVE steps (use judgment).

---

## Part 1: Mechanical Steps (FOLLOW EXACTLY)

These steps are deterministic. Execute them precisely as written.

### Hyprnote Processing
```
1. Read _meta.json
2. Extract: title, created_at, id
3. Read _transcript.json
4. Extract words array: transcripts[0].words
5. Reconstruct text: words.map(w => w.text).join('').trim()
6. Group by channel: separate words where channel=0 vs channel=1
7. Check: does _memo.md exist in same folder?
8. If yes: read _memo.md, strip YAML frontmatter
```

### Notion Processing
```
1. Read entire .md file into memory
2. Extract date from filename: parse YYYY-MM-DDTHH_MM_SSZ pattern
```

### WhatsApp Processing
```
1. Read entire _chat.txt
2. Parse each line matching: [MM/DD/YY, HH:MM:SS] Sender: Message
3. Store as: {timestamp, sender, message}
4. List all files in folder except _chat.txt
5. For each .jpg/.png file: Read image (Claude will see visual content)
6. For each .pdf file: Read PDF
7. For each .md/.docx file: Read document
```

### Hailer Processing
```
1. List all .md files in data/messaging/hailer/ (exclude readme.md)
2. For each file: read entire content
3. Parse format: lines alternate between "Username", "HH:MM", "Message"
4. Combine all messages into single chronological list
```

---

## Part 2: Interpretive Guidelines (USE JUDGMENT)

These require understanding and judgment. Follow the guidelines but adapt as needed.

### Writing Summaries

**Goal:** 2-4 sentences answering: What? Why? Outcome?

**Good summary:**
> "Team discussed corporate structure options for US expansion. Jared recommended Delaware C-Corp with Finnish Oy subsidiary based on tax and grant implications. Decided to proceed with LOI approach before formal incorporation."

**Bad summary:**
> "Meeting about corporate structure." (too vague)
> "The team met to discuss things." (no content)

### Extracting Key Elements

**Decisions:** Look for language like "let's do", "agreed", "decided", "will go with"
- Format: "Decided to [action] because [reason]"

**Action Items:** Look for commitments, assignments, next steps
- Format: "[Person] will [action]" or "Need to [action]"

**Key Insights:** Surprising information, strategic observations, lessons learned
- Not every entry has these - only include if genuinely insightful

### Identifying Participants

- List names mentioned in conversation
- Add role if stated or obvious: "Jorma (Helsinki CPO)", "Esa-Pekka (procurement expert)"
- Core team: Iivo (technical), Aaro (business), Jared (US market)

### Rating Relevance

| Rating | Criteria | Examples |
|--------|----------|----------|
| **High** | Core business | Customer calls, procurement discussions, product decisions |
| **Medium** | Supporting topics | Incorporation, team coordination, tooling |
| **Low** | Tangential | Personal chat, unrelated discussions |

### Grouping WhatsApp/Hailer into Clusters

**Signals for new cluster:**
- Time gap >24 hours
- Explicit topic change ("btw", "switching topics", "another thing")
- New participants joining conversation
- Shift from discussion to action or vice versa

**Cluster naming:** Use descriptive title reflecting main topic
- Good: "Helsinki Opportunity & Corporate Structure"
- Bad: "Messages from Jan 6-7"

### Cross-References

Note when entries relate to each other:
- "This call is discussed in WhatsApp same day"
- "Follow-up to Dec 26 meeting with Esa-Pekka"
- "Referenced in later call"

---

## Part 3: Validation Checklist (VERIFY BEFORE FINISHING)

Run through this checklist for the complete output:

### Per-Entry Checks
- [ ] Summary is 2-4 sentences with actual content
- [ ] Summary doesn't just repeat the title
- [ ] Participants listed (at least one name)
- [ ] Relevance rating included (High/Medium/Low)

### Hyprnote-Specific
- [ ] If _memo.md exists → memo content appears in entry
- [ ] Untitled sessions have inferred descriptive title

### WhatsApp-Specific
- [ ] Every image has visual description (not just filename)
- [ ] Every document (.pdf, .md, .docx) has content summary
- [ ] Each cluster has date range in header
- [ ] Clusters are logically grouped (not arbitrary time slices)

### Hailer-Specific
- [ ] All messages from all files included
- [ ] Participants extracted from message headers

### Global Checks
- [ ] Entries sorted chronologically (oldest first in output)
- [ ] Grouped by month
- [ ] No duplicate entries
- [ ] YAML frontmatter has accurate counts

**If any check fails:** Fix the issue, then re-validate.
