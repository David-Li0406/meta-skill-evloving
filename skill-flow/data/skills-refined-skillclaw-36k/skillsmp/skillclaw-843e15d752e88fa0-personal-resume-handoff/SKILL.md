---
name: personal:resume-handoff
description: Use this skill when you want to continue work from a previous session's handoff document, analyzing context and next steps.
---

# Resume Work from a Handoff Document

You are tasked with resuming work from a handoff document through an interactive process. These handoffs contain critical context, learnings, and next steps from previous work sessions that need to be understood and continued.

## Initial Response

1. **If the path to a handoff document was provided**:
   - Immediately read the handoff document FULLY.
   - Immediately read any research or plan documents that it links to under `.coding-agent/plans` or `.coding-agent/research`. Do NOT use a sub-agent to read these critical files.
   - Begin the analysis process by ingesting relevant context from the handoff document and reading additional files it mentions.
   - Then propose a course of action to the user and confirm, or ask for clarification on direction.

2. **If a ticket number (like ENG-XXXX) was provided**:
   - Locate the most recent handoff document for the ticket. Handoffs will be located in `.coding-agent/handoffs/ENG-XXXX` where `ENG-XXXX` is the ticket number. **List this directory's contents.**
   - There may be zero, one, or multiple files in the directory.
   - **If there are zero files in the directory, or the directory does not exist**: tell the user: "I'm sorry, I can't seem to find that handoff document. Can you please provide me with a path to it?"
   - **If there is only one file in the directory**: proceed with that handoff.
   - **If there are multiple files in the directory**: using the date and time specified in the file name (in the format `YYYY-MM-DD_HH-MM-SS`), proceed with the most recent handoff document.
   - Immediately read the handoff document FULLY.
   - Immediately read any research or plan documents that it links to under `.coding-agent/plans` or `.coding-agent/research`; do NOT use a sub-agent to read these critical files.
   - Begin the analysis process by ingesting relevant context from the handoff document and reading additional files it mentions.
   - Then propose a course of action to the user and confirm, or ask for clarification on direction.

3. **If no parameters provided**, respond with:
```
I'll help you resume work from a handoff document. Let me find the available handoffs.

Which handoff would you like to resume from?
```
Then wait for the user's input.