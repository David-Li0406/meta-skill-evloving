---
name: synthesize-customer-voice
description: Aggregates and synthesizes customer feedback from various sources.
trigger_phrases:
  - "synthesize customer voice"
  - "customer feedback summary"
  - "what are customers saying"
---

# Skill: Synthesize Customer Voice

## Overview
This skill converts raw Voice of Customer (VOC) data from various sources into decision-grade themes, insights, and opportunities. It follows a strict protocol to ensure that all findings are evidence-based.

## When to Use
- When you have raw customer feedback (e.g., interview transcripts, support tickets, survey results).
- When you need to understand the core themes and pain points emerging from the feedback.
- When preparing for roadmap planning, feature prioritization, or strategic reviews.

## Core Logic
1.  **Identify and Collect Inputs:**
    - The system SHALL scan the `inputs/voc/` and `inputs/jira/` directories for relevant source files (e.g., `.md`, `.csv`).
    - The system SHALL present the list of found files to the user and ask for confirmation or additional inputs.

2.  **Extract Key Information:**
    - For each confirmed source file, the system SHALL read the content.
    - The system SHALL identify and extract key themes, verbatim quotes, sentiment (positive, negative, neutral), and recurring issues or requests.
    - This process should create a structured representation of the feedback.

3.  **Synthesize and Generate Report:**
    - The system SHALL aggregate the extracted information from all sources.
    - It SHALL identify the top 3-5 recurring themes based on frequency and sentiment.
    - It SHALL generate a concise summary report in `outputs/insights/voc-synthesis-[YYYY-MM-DD].md`.
    - The report MUST include sections for:
        - An executive summary.
        - Detailed breakdown of each theme with supporting verbatim quotes.
        - A list of potential opportunities or feature requests.
        - Source attribution for all evidence.
