---
name: swe-onboard-feature
version: 1.0.0
description: Interactive 5-stage feature onboarding wizard
workflow:
  aware: true
  callable_from:
    - WF_ONBOARD
    - WF_START
  default_return: WF_START
  supports_standalone: true
  auto_transition: true
---

# Onboard Feature Skill

Interactive wizard for registering new features in the workflow system.

## Stages

### Stage 1: Basic Info
- Feature key (e.g., BACKEND, AUTH)
- Feature name (e.g., "Backend API")
- Root path(s)

### Stage 2: Tech Stack
- Type (web_app, library, api, cli, cms)
- Primary language
- Framework

### Stage 3: Analysis Mode
- [A] Full DAA Swarm (10 agents, 2-5 min)
- [B] Quick Scan (30 sec)
- [C] Manual Configuration

### Stage 4: Architecture Confirmation
- Detected layers
- Data flow
- Dependencies

### Stage 5: Memory Creation
- Create FEATURE_[KEY]
- Create DOM_[KEY]_* (if domains found)
- Create SYS_[KEY]_* (if systems found)
- Update INDEX_FEATURES

## Exit

`> **Skill /swe-onboard-feature complete** - Feature [KEY] registered`
