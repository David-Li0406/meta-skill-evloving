---
name: structured-research-and-recording
description: Use this skill when you need to conduct structured research and document the decision-making process for future reference.
---

# Skill body

## Overview

This skill allows you to execute a structured research workflow while simultaneously recording the context and decisions made during the process. It is triggered when the user expresses a desire to investigate or document information.

## Steps

1. **Initiate Research**:
   - Listen for user prompts such as "調べて" (investigate), "調査して" (research), or similar phrases.
   - Extract the research theme from the user's statement.

2. **Execute Research Command**:
   - Run the command: `/mutils:incremental-research [調査テーマ]` to start the research process.

3. **Document Findings**:
   - As research progresses, document the findings in a Markdown file, ensuring to include:
     - **Summary**: A brief overview of the research topic.
     - **Background and Motivation**: Explain why the research is necessary.
     - **Research Process**: Detail the steps taken, including any hypotheses and their evolution.
     - **Conclusions**: Summarize the final outcomes and decisions made.

4. **Quality Standards**:
   - Ensure that the documentation allows others to reconstruct the context by including:
     - Key discussion points.
     - Considered options and reasons for their acceptance or rejection.
     - The rationale behind the final decisions.

5. **Output Destination**:
   - Determine where to save the documentation based on user needs:
     - **File**: For long-term storage or reference.
     - **PR Body**: For decisions related to code changes.
     - **Conversation**: For immediate reference without the need for formal documentation.

6. **User Confirmation**:
   - If the research theme is unclear, confirm with the user before proceeding.

## Example

Refer to the provided examples for a structured approach to documenting decision-making and research findings.