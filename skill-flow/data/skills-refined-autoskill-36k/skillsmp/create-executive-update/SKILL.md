---
name: create-executive-update
description: Generates a high-level executive summary of product progress and insights.
trigger_phrases:
  - "executive update"
  - "product status report"
  - "summary for leadership"
---

# Skill: Create Executive Update

## Overview
This skill generates a concise, high-level summary of product progress, key metrics, and strategic insights for a leadership audience.

## When to Use
- When you need to provide a regular status update to executives or stakeholders.
- When you need to summarize the key outcomes of a recent launch or a quarter.
- When you need to distill complex information into a brief, digestible format.

## Core Logic
1.  **Analyze Recent Data:**
    - The system SHALL scan recent files in `outputs/` and `history/` to gather data. This includes:
        - Recent VOC syntheses (`outputs/insights/`).
        - Project status from recent PRDs or triage reports (`outputs/delivery/`, `outputs/roadmap/`).
        - Key metrics and KPIs from success reports.
        - Decisions from `history/decisions/`.

2.  **Synthesize Key Points:**
    - The system SHALL identify the most important information for a leadership audience. This includes:
        - **Achievements:** What was recently accomplished or launched?
        - **Key Learnings:** What are the most significant insights from recent data?
        - **Challenges & Risks:** What are the primary blockers or risks?
        - **Forward-Looking Statement:** What is the focus for the upcoming period?

3.  **Format for Executive Consumption:**
    - The system SHALL generate a draft of the update in `outputs/exec_updates/update-[YYYY-MM-DD].md`.
    - The format MUST be brief, using bullet points, and focusing on impact. It should be easily readable in under 2 minutes.
    - The report should lead with the most important information (the "bottom line up front").
