---
name: lead-scoring-methodology
description: Build and validate dual-track lead scoring for Managed Services and Agency/Temp opportunities in the UK police sector. Covers score architecture, signal weights, urgency detection, framework access scoring, and validation frameworks.
---

# Dual-Track Lead Scoring for UK Police Sector

> **⚠️ Strategy Note (January 2025)**: The sales strategy has evolved. Rather than classifying opportunities as "MS vs Agency" at the signal stage, we now treat all job postings as warm leads and present Peel's full capability. The conversation determines the service, not pre-classification.
>
> This skill remains valuable reference for understanding signal interpretation (urgency language, posting age, role fit), but the dual-track scoring model may be simplified to a single priority score. See `docs/SALES-STRATEGY.md` for the current approach.

Build and validate effective lead scoring for both **Managed Services** and **Agency/Temp Recruitment** opportunities.


## Core Thesis

### For Managed Services:
> **"Service Fit" is driven by regulatory failure. A police force buys managed investigator teams because HMICFRS has graded their investigation capacity as "Inadequate."**

### For Agency/Temp:
> **The agency equivalent of HMICFRS "Inadequate" is: job posting aged 30+ days + urgency language ("immediate start", "ASAP", "backlog") + target role type (PIP2, Digital Forensics).**


## Dual-Track Scoring Architecture

### Score Structure

| Track | Score Range | Pillars |
|-------|-------------|---------|
| **Managed Services Score** | 0-100 | Service Fit (40%), Signal (30%), Relationship (20%), Timing (10%) |
| **Agency Score** | 0-100 | Urgency (35%), Role Fit (25%), Framework Access (20%), Timing (20%) |

### Shared vs Track-Specific Signals

| Signal Type | Managed | Agency | Notes |
|-------------|---------|--------|-------|
| HMICFRS "Inadequate" | +40 | +15 | Primary for managed; context for agency |
| HMICFRS "Requires Improvement" | +25 | +10 | Both tracks benefit |
| "Immediate start" + "Must hold vetting" | +10 | **+25** | Primary agency signal |
| Posting age 60+ days | +10 | **+25** | Agency distress signal |
| Volume (10+ similar roles) | **+30** | +20 | Structural crisis = managed opportunity |
| Q4 fiscal period | +20 | +15 | Both tracks benefit |
| Framework lock-out (BLC without Tier 2) | -10 | **-30** | Critical for agency |


## TRACK 2: Agency/Temp Scoring

**Total Score = Urgency + Role Fit + Framework Access + Timing (0-100)**

### Pillar 1: Urgency Score (35 Points)

The primary driver for agency opportunities. Combines linguistic analysis with posting behaviour.

#### Urgency Language Triggers

| Signal | Score | Time-to-Fill | Meaning |
|--------|-------|--------------|---------|
| **"Immediate start" + "Must hold vetting"** | **+25** | 7-9 days | Distress signal — cannot wait for vetting |
| "ASAP" / "Urgent" | +15 | 10-14 days | Resource left unexpectedly or backlog critical |
| "Backlog" / "Legacy cases" / "Review team" | +15 | 14-21 days | Finite scope work ideal for agency |
| "Cover" / "Maternity" / "Sickness" | +10 | Variable | Tactical backfill need |
| "Immediate start" BUT "Vetting can be applied for" | +3 | 60-90 days | False flag — vetting will delay regardless |

**The "Immediate Start" Paradox:** In policing, where vetting takes 60-90 days, "immediate start" is code for: "We need someone who already holds valid NPPV3 or SC clearance."

#### Posting Age (Critical Signal)

| Posting Age | Status | Score | Action |
|-------------|--------|-------|--------|
| 0-14 days | Fresh posting | +0 | Monitor |
| 15-30 days | Recruitment difficulty emerging | +10 | Prepare candidates |
| **30-60 days** | Month without success; budget pressure | **+20** | Active outreach |
| **60+ days** | Permanent recruitment failed | **+25** | Priority engagement |
| **Reposted (same role)** | Vetting failure or collapse | **+25** | Immediate contact |
| **Reposted with broadened requirements** | Desperation | **+30** | Guaranteed opportunity |

### Pillar 2: Role Fit Score (25 Points)

Certain roles indicate broader agency openness and higher value opportunities.

#### Role Suitability Matrix

| Role Type | Agency Suitability | Score | Market Notes |
|-----------|-------------------|-------|--------------|
| **Digital Forensics Examiner** | Very High | +20 | 12-18 month backlogs; structural crisis |
| **PIP2 Investigator** | Very High | +20 | When forces advertise, detective resilience has collapsed |
| **Financial Investigator** | High | +15 | POCA specialism; project-based |
| **Disclosure Officer** | High | +15 | CPIA bottleneck; 64,015 Crown Court case backlog |
| **Intelligence Analyst** | Medium-High | +12 | Often operation-specific surge |
| **HOLMES Indexer** | High (niche) | +15 | Major Incident Room = force in "Crisis Mode" |
| **Statement Taker** | Medium | +8 | Civilianisation of investigation |
| **PIP1 Investigator** | Medium | +8 | Volume crime; lower margin |

**PIP2 as Distress Signal:** A PIP2 Investigator vacancy is the strongest possible signal. Suggests deficit of dozens of permanent officers — deep systemic gap that managed services could fill.

### Pillar 3: Framework Access Score (20 Points)

**Critical:** Framework lock-out is the primary agency-specific negative signal.

#### Framework Landscape

| Framework | Forces | Implication |
|-----------|--------|-------------|
| **BlueLight Commercial (Adecco)** | ~37 committed forces | Must be Tier 2 supplier OR target niche roles where Adecco fails |
| **YPO 942 (Randstad)** | Essex, Kent, Norfolk, Suffolk, Beds, Cambs, Herts | Register as specialist supplier |
| **CCS RM6277** | Available to all; variable uptake | Direct Award for small/urgent |
| **Matrix SCM** | Various; platform-based | Register on platform; compete on speed |

#### Framework Scoring

| Situation | Score | Notes |
|-----------|-------|-------|
| Neutral Vendor framework (Matrix, Crown) | +15 | Open competition |
| Peel is Tier 2 on force's framework | +10 | Access confirmed |
| Force uses BLC without Peel Tier 2 access | **-30** | Major lock-out (reduce to -10 for niche roles) |
| Off-contract spend detected (>£100k) | +20 | "Permeable" force |
| MSP mandate confirmed | -20 | Locked to primary vendor |

### Pillar 4: Timing Score (20 Points)

Agency demand has different seasonal patterns than managed services.

#### Seasonal Patterns

| Season | Driver | Score | Notes |
|--------|--------|-------|-------|
| **Summer (June-Sept)** | Annual leave cover; festivals | **+20** | Peak agency demand |
| **Post-Christmas (Jan-Feb)** | New Year resignations; backlog | +15 | High demand |
| **September** | Back-to-school surge; summer case backlog | +15 | Investigation catch-up |
| **Q4 Fiscal (Jan-Mar)** | Budget flush | +15 | Both tracks benefit |
| December | Holiday period | -10 | Decision paralysis |


## Land-and-Expand Identification

Agency placements create trust and access for managed service relationships.

### Conversion Triggers

| Trigger | Action |
|---------|--------|
| Agency placement at force with Managed Score 60+ | Tag as "Land-and-Expand" |
| 3+ agency placements at same force in 12 months | Auto-escalate review |
| Force returns for repeat business within 90 days | Relationship building |
| Volume signals (10+ roles) | Structural gap = managed opportunity |
| Scope expansion requests | Ready for managed conversation |


## Validation Framework

### Shadow Scoring Method

Before rollout, validate both tracks:

1. **Select Data Set:** Last 5 Closed-Won + Last 5 Closed-Lost per track
2. **Back-Test:** Calculate scores at first engagement
3. **Analyse Correlation:**
   - Managed: Did wins have high HMICFRS-driven Fit scores?
   - Agency: Did wins have high urgency + posting age scores?
4. **Calibrate:** Adjust weights based on findings

### Lift Analysis

```
Lift = (Conversion rate of top 20% by score) / (Overall conversion rate)
```

| Lift | Interpretation |
|------|----------------|
| 3-5× | Good scoring model |
| 2-3× | Adequate, room for improvement |
| <2× | Model not adding value |


## Quick Reference: Score Components

### Managed Services (100 pts)

| Component | Max | Primary Signals |
|-----------|-----|-----------------|
| Service Fit | 40 | HMICFRS rating, backlog, framework access |
| Signal | 30 | Website visits, content downloads, form submissions |
| Relationship | 20 | Multi-threading, recency, decision maker access |
| Timing | 10 | Q4 fiscal, active tenders |

### Agency (100 pts)

| Component | Max | Primary Signals |
|-----------|-----|-----------------|
| Urgency | 35 | Language triggers, posting age, reposting |
| Role Fit | 25 | PIP2, Digital Forensics, Disclosure, volume |
| Framework Access | 20 | BLC status, Tier 2, off-contract spend, IR35 |
| Timing | 20 | Seasonal demand, candidate availability |
