---
name: generate-strategic-charter-and-prd
description: Creates a strategic charter for a new initiative or a PRD for an existing pain point.
trigger_phrases:
  - "create strategic charter"
  - "define initiative strategy"
  - "generate product vision"
  - "create prd"
  - "create tickets"
---

# Skill: Generate Strategic Charter and/or PRD

## Overview
This skill drafts either a high-level strategic charter for a new product initiative or a detailed Product Requirements Document (PRD) for a specific feature or pain point.

## When to Use
- **Charter:** At the beginning of a new initiative, to define the "why" and "what".
- **PRD:** When an approved charter or a well-understood problem needs to be translated into actionable requirements for the engineering team.
- When you need to create tickets based on a PRD.

## Core Logic
### For a Strategic Charter
1.  **Gather Strategic Context:**
    - The system SHALL process relevant inputs, such as market analysis, user research summaries, or company goal documents.
    - The system SHALL ask clarifying questions to understand the core problem and desired outcomes.

2.  **Define Charter Components:**
    - The system SHALL define the key sections of the charter:
        - **Vision:** The high-level, aspirational goal.
        - **Mission:** A more concrete statement of what will be built and for whom.
        - **Problem Statement:** A clear description of the pain point being solved, backed by evidence.
        - **Goals & Objectives:** Measurable success metrics (e.g., OKRs).
        - **Scope (In/Out):** Clear boundaries for the initiative.

3.  **Draft the Charter Document:**
    - The system SHALL generate a draft of the charter in `outputs/strategy/charter-[initiative-name]-[YYYY-MM-DD].md`.

### For a PRD
1.  **Gather Feature Context:**
    - The system SHALL process a charter, a set of user stories, a Jira ticket, or a description of a customer pain point.

2.  **Define PRD Components:**
    - The system SHALL break down the problem into detailed requirements, including:
        - **Functional Requirements:** What the system must do.
        - **Non-Functional Requirements:** Performance, security, etc.
        - **Edge Cases:** How the system handles errors and unexpected inputs.
        - **Telemetry:** What needs to be measured to track success.

3.  **Draft the PRD Document:**
    - The system SHALL generate a draft of the PRD in `outputs/delivery/prds/[feature-name]-prd-[YYYY-MM-DD].md`.
