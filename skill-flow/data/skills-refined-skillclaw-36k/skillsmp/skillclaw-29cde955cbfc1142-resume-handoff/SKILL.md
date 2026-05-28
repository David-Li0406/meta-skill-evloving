---
name: resume-handoff
description: Use this skill when you need to resume work from a handoff document, ensuring all relevant context and next steps are understood and validated.
---

# Resume work from a handoff document

You are tasked with resuming work from a handoff document through an interactive process. These handoffs contain critical context, learnings, and next steps from previous work sessions that need to be understood and continued.

## Initial Response

When this command is invoked:

1. **If the path to a handoff document was provided**:
   - Skip the default message and immediately read the handoff document FULLY.
   - Read any research or plan documents linked under `thoughts/shared/plans` or `thoughts/shared/research`. Do NOT use a sub-agent to read these critical files.
   - Begin the analysis process by ingesting relevant context from the handoff document and any additional files it mentions.
   - Propose a course of action to the user and confirm, or ask for clarification on direction.

2. **If a ticket number (like ENG-XXXX) was provided**:
   - Run `humanlayer thoughts sync` to ensure your `thoughts/` directory is up to date.
   - Locate the most recent handoff document for the ticket in `thoughts/shared/handoffs/ENG-XXXX`, where `ENG-XXXX` is the ticket number.
   - List the directory's contents:
     - **If there are zero files or the directory does not exist**: inform the user: "I'm sorry, I can't seem to find that handoff document. Can you please provide me with a path to it?"
     - **If there is only one file**: proceed with that handoff.
     - **If there are multiple files**: use the date and time in the file name (format `YYYY-MM-DD_HH-MM-SS`) to proceed with the _most recent_ handoff document.
   - Read the handoff document FULLY and any linked research or plan documents.
   - Begin the analysis process and propose a course of action to the user, confirming or asking for clarification.

3. **If no parameters are provided**, respond with:
   ```
   I'll help you resume work from a handoff document. Please provide the path to the document or a ticket number.
   ```