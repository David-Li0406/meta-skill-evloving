# Meeting Memo Handler

Process voice memos (🎤) into structured meeting notes.

## Detection

**Pattern:** `- [time] - 🎤 [transcription]`

Long voice memos (>200 words) with meeting signals → meeting note.

## Extraction Goals

From raw transcription, extract:

| Section | What to Extract |
|---------|-----------------|
| **Title** | Meeting topic or key subject |
| **Attendees** | Names and roles mentioned |
| **Notes** | Key information, context, project details |
| **Decisions Made** | Conclusions or agreements reached |
| **Action Items** | Tasks as checkboxes (Dataview compatible!) |

## Transcription Cleanup Rules

Before inserting, apply basic cleanup:
- **Remove filler words:** "um", "uh", "like" (when filler), "you know", "sort of"
- **Fix grammar:** Correct obvious errors, add missing words
- **Add punctuation:** Proper periods, commas, question marks
- **Break into paragraphs:** At natural topic changes or speaker switches
- **Preserve tone:** Keep conversational style and ALL content

**DO NOT summarize or truncate.** The entire transcription must be preserved.

## Note Creation

**Step 1: Create note with extracted content**

```
para_create({
  template: "meeting",
  title: "GMS Project Kickoff - Jackie",
  dest: "00 Inbox",
  args: {},
  content: {
    "Attendees": "- Jackie (Team Lead)\n- Josh Green (Tech Lead)\n- Nathan",
    "Notes": "### Key Points\n- GMS = Gift Card Management System\n- Reseller integration with Black Hawk\n- Deadline: July",
    "Decisions Made": "- Estimates in days, not story points\n- All-in day: Thursday",
    "Action Items": "- [ ] Get MacBook bun number to Jackie\n- [ ] Test VPN from home\n- [ ] Look at Miro board"
  },
  response_format: "json"
})
```

**Step 2: Set frontmatter**

```
para_frontmatter_set({
  file: "00 Inbox/🗣️ Note Title.md",
  set: {
    meeting_type: "general",
    meeting_date: "2026-01-06",
    area: "[[Career & Contracting]]",
    company: "Bunnings"
  }
})
```

**Step 3: Append Raw Transcription**

The meeting template does NOT have a Raw Transcription section. Add it after `## Follow-up`:

```
para_insert({
  file: "00 Inbox/🗣️ Note Title.md",
  heading: "Follow-up",
  content: "\n---\n\n## Raw Transcription\n\n> [Full cleaned transcription in blockquote format]",
  mode: "after"
})
```

## Template Output

```markdown
---
type: meeting
meeting_type: general
meeting_date: 2026-01-06
area: "[[Career & Contracting]]"
company: Bunnings
template_version: 1
---

# GMS Project Kickoff - Jackie

## Attendees

- Jackie (Team Lead, on leave until 27th)
- Josh Green (Tech Lead, Perth)
- June (Frontend/Backend dev)

## Notes

- GMS = Gift Card Management System
- Reseller integration with Black Hawk
- Deadline: July (likely to extend)

## Decisions Made

- Estimates in days, not story points
- All-in day: Thursday

## Action Items

- [ ] Get MacBook bun number to Jackie
- [ ] Test VPN from home tonight
- [ ] Look at Miro board for resellers

## Follow-up

-

---

## Raw Transcription

> [Full cleaned transcription preserved here...]
```

## Reference Example

See: `02 Areas/🤝🏻 Contract - Bunnings/🗣️ IT Onboarding - Bunnings.md`
