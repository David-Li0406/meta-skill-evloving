---
name: triage-backlog
description: Prioritizes and categorizes backlog items based on defined criteria.
trigger_phrases:
  - "triage backlog"
  - "prioritize tasks"
  - "what's on fire"
---

# Skill: Triage Backlog

## Overview
This skill processes backlog items from sources like Jira exports and applies a consistent prioritization framework. It helps identify the most critical items to focus on.

## When to Use
- When you have a list of backlog items to prioritize.
- When you need to prepare for sprint planning or a backlog grooming session.
- When you need to identify "quick wins" or items of high strategic value.

## Core Logic
1.  **Process Input Files:**
    - The system SHALL ingest backlog data from specified files in `inputs/jira/` or other `inputs/` subdirectories (e.g., `.csv` from a Jira export).
    - The system SHALL parse the items, identifying fields like `summary`, `priority`, `story_points`, `labels`, and `description`.

2.  **Apply Prioritization Rules:**
    - The system SHALL apply a set of prioritization rules. These rules should be configurable but can default to a framework like RICE (Reach, Impact, Confidence, Effort) or ICE.
    - For each item, the system SHALL calculate a priority score.
    - It SHALL use keywords in the summary/description to help determine impact (e.g., 'crash', 'data loss' = high impact).

3.  **Output Ranked Backlog:**
    - The system SHALL generate a report in `outputs/roadmap/backlog-triage-[YYYY-MM-DD].md`.
    - The report MUST contain a ranked list of the backlog items, ordered by their calculated priority score.
    - The report SHOULD include a summary of the triage, such as "Identified 5 critical items and 10 high-priority items."
