---
name: add-event
description: Guidelines for adding an event to a venue's calendar in OlyBars. Use this when the user (Developer or Venue Owner persona) wants to schedule a new event.
---

# Add Event Skill

This skill guides you through the process of adding an `AppEvent` to the OlyBars database.

## When to use this skill
- When the user explicitly asks to "add an event", "schedule a show", or "put something on the calendar".
- When operating in the context of the "Schmidt" dashboard or Venue Owner workflows.

## Prerequisite Information
Before creating an event, you MUST gather the following information from the user (simulate the "Schmidt" conversational flow):

1.  **Venue Identity**: Which venue is this for? (Implicit if in a specific venue context, otherwise ask).
    *   *Constraint*: Must match a valid `venueId` in `venues_master.json`.
2.  **Event Title**: What is the name of the event?
3.  **Event Type**: What kind of event is it?
    *   *Allowed Values*: `karaoke`, `trivia`, `live_music`, `bingo`, `openmic`, `other`.
4.  **Date**: When is it happening? (YYYY-MM-DD format).
5.  **Time**: What time does it start? (HH:MM 24-hour format).
6.  **Description**: Brief details about the event. (Optional, can be polished by Artie later).

## Execution Procedure

### 1. Conversation Logic (The "Schmidt" Flow)
### 1. Conversation Logic (The "Schmidt" Flow)
**Trigger**: User selects "Add Event" chip or types "Add event".
**Schmidt Response**: "How would you like to provide the details?"
    -   *Option A*: "Paste the details or a link."
    -   *Option B*: "Upload a flyer/schedule." (Requires UI Support).
    -   *Option C*: "Interactive Interview."

#### Path A: The Direct Paste (Quick)
1.  **User Input**: User provides text (e.g., "Karaoke Night, Friday at 8pm").
2.  **Processing**: Agent drafts event from text.
3.  **Commit**: User confirms.

#### Path B: Upload Mode (Planned)
*Note: The Chat UI does not currently support file uploads. This path is pending UI updates.*

#### Path C: The Interview Mode (Interactive)
1.  **Schmidt Prompt**: "I'll ask you a few questions to build the listing. First, what is the **Event Title**?"
2.  **User Input**: "Trivia Night"
3.  **Schmidt Prompt**: "Got it. What **date and time** does Trivia Night start?"
4.  **User Input**: "Next Tuesday at 7pm"
5.  **Schmidt Prompt**: "And finally, which **category** fits best? (Trivia, Karaoke, Live Music, Other)"
6.  **User Input**: "Trivia"
7.  **Confirmation**: Schmidt displays the "Pending Action" card.
8.  **Commit**: User clicks "Confirm & Save".

### 2. Technical Implementation (Agent Directives)
*   **Hook**: `useArtieOps.ts`
    -   State: `event_input`
    -   Action: `SUBMIT_EVENT_TEXT`
    -   Draft Skill: `add_calendar_event`
*   **Service**: `VenueOpsService.submitCalendarEvent` -> `EventService.submitEvent`.
*   **Validation**: Ensure `title`, `date`, `time` are present before submission.

### 3. Developer Mode (Manual Injection)
If you are acting as the Developer Agent manually injecting data:
1.  **Script**: Create a script in `server/src/scripts/add-event.ts`.
2.  **Inject**: Run `npx tsx server/src/scripts/add-event.ts`.

## Best Practices
- **Validation**: Ensure the `date` is not in the past.
- **Conflict Check**: Warn if there is already an event at that venue at the same time (if visible in context).
- **Tone**: If simulating "Schmidt" or "Artie", keep the tone helpful and efficient.
